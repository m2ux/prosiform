#!/usr/bin/env python3
"""Assert every reference a document carries resolves.

Four classes of reference, each resolved by what it names:

- a fragment alone resolves against the document's own headings;
- a repository-relative path resolves against the working tree, and its
  fragment against the headings of the Markdown file it names;
- a GitHub blob or tree URL into this repository resolves against the git
  ref it names, so a reference to the engineering branch is checked without
  the network;
- any other absolute URL is reached over the network, which `--online`
  turns on. An issue, a pull request or a project board is read through
  the GitHub API with the caller's credentials, because a private
  repository answers an unauthenticated request with 404. Without
  `--online` such a reference counts as unresolved and the check fails, so
  a pass always means every reference was resolved.
"""

import argparse
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_URL_PREFIX = "https://github.com/m2ux/prosiform/"

INLINE_LINK = re.compile(r"\]\(\s*<?([^()<>\s]+)>?\s*(?:\"[^\"]*\")?\s*\)")
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+)>?", re.MULTILINE)
FENCE = re.compile(r"^(?:```|~~~)", re.MULTILINE)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
SLUG_KEPT = frozenset("-_ ")

USER_AGENT = "prosiform-link-check"


def strip_code_fences(text: str) -> str:
    """Blank out fenced blocks, whose contents are examples rather than links."""
    out, fenced = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return "\n".join(out)


def slug(heading: str) -> str:
    """The fragment GitHub generates for a heading.

    A code span and a link reduce to their text. What survives is lowercased
    and holds its letters, numbers and combining marks, its hyphens and its
    underscores; punctuation and symbols, an emoji among them, are dropped.
    Each remaining space becomes a hyphen, and nothing is trimmed, so a
    heading opening with an emoji yields a leading hyphen: `## ✅ Checks`
    generates `#-checks`.
    """
    text = re.sub(r"`([^`]*)`", r"\1", heading)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    kept = [
        character
        for character in text.lower()
        if character in SLUG_KEPT or unicodedata.category(character)[0] in "LNM"
    ]
    return "".join(kept).replace(" ", "-")


def fragments_of(text: str) -> set[str]:
    seen: dict[str, int] = {}
    fragments = set()
    for _, heading in HEADING.findall(strip_code_fences(text)):
        base = slug(heading)
        count = seen.get(base, 0)
        seen[base] = count + 1
        fragments.add(base if count == 0 else f"{base}-{count}")
    return fragments


def references(text: str) -> list[str]:
    body = strip_code_fences(text)
    found = INLINE_LINK.findall(body) + REFERENCE_DEFINITION.findall(body)
    ordered, seen = [], set()
    for target in found:
        if target not in seen:
            seen.add(target)
            ordered.append(target)
    return ordered


def git_ref(name: str) -> str | None:
    for candidate in (f"origin/{name}", name):
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"{candidate}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return candidate
    return None


def git_show(ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else None


def git_path_exists(ref: str, path: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{ref}:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def resolve_local(document: Path, target: str) -> str | None:
    path_part, _, fragment = target.partition("#")
    if not path_part:
        if fragment and fragment not in fragments_of(document.read_text()):
            return f"no heading in {document.name} generates #{fragment}"
        return None

    resolved = (document.parent / path_part).resolve()
    if not resolved.exists():
        return f"{path_part} does not exist"
    if fragment and resolved.suffix in (".md", ".markdown"):
        if fragment not in fragments_of(resolved.read_text()):
            return f"no heading in {path_part} generates #{fragment}"
    return None


def is_repository_tree_url(target: str) -> bool:
    """A blob or tree URL into this repository, which git resolves."""
    if not target.startswith(REPOSITORY_URL_PREFIX):
        return False
    parts = target[len(REPOSITORY_URL_PREFIX) :].partition("#")[0].split("/")
    return len(parts) >= 2 and parts[0] in ("blob", "tree")


def resolve_repository_url(target: str) -> str | None:
    rest = target[len(REPOSITORY_URL_PREFIX) :]
    path_part, _, fragment = rest.partition("#")
    parts = path_part.split("/")
    ref_name, path = parts[1], "/".join(parts[2:])
    ref = git_ref(ref_name)
    if ref is None:
        return f"no git ref named {ref_name}"
    if path and not git_path_exists(ref, path):
        return f"{path} does not exist on {ref_name}"
    if fragment and path.endswith((".md", ".markdown")):
        content = git_show(ref, path)
        if content is None or fragment not in fragments_of(content):
            return f"no heading in {path} on {ref_name} generates #{fragment}"
    return None


GITHUB_ISSUE = re.compile(
    r"^https://github\.com/([^/]+)/([^/]+)/(issues|pull)/(\d+)/?$"
)
GITHUB_USER_PROJECT = re.compile(
    r"^https://github\.com/(users|orgs)/([^/]+)/projects/(\d+)/?$"
)


def gh_api(arguments: list[str]) -> str | None:
    """Run an authenticated GitHub API call, or report why it did not answer."""
    try:
        result = subprocess.run(
            ["gh", "api", *arguments], capture_output=True, text=True, timeout=30
        )
    except FileNotFoundError:
        return (
            "gh is not installed, and a private reference needs an authenticated read"
        )
    except subprocess.TimeoutExpired:
        return "gh did not answer within 30s"
    if result.returncode != 0:
        return result.stderr.strip().splitlines()[-1] if result.stderr else "gh failed"
    return None


def resolve_github(target: str) -> str | None:
    """Resolve a tracker reference with the caller's credentials.

    A private repository answers an unauthenticated request with 404, so an
    issue, a pull request or a project board is read through the API rather
    than fetched as a page.
    """
    issue = GITHUB_ISSUE.match(target)
    if issue:
        owner, repository, kind, number = issue.groups()
        endpoint = "issues" if kind == "issues" else "pulls"
        return gh_api([f"repos/{owner}/{repository}/{endpoint}/{number}", "--silent"])

    project = GITHUB_USER_PROJECT.match(target)
    if project:
        scope, login, number = project.groups()
        owner_field = "user" if scope == "users" else "organization"
        query = (
            f'{{ {owner_field}(login: "{login}") '
            f"{{ projectV2(number: {number}) {{ id }} }} }}"
        )
        return gh_api(["graphql", "-f", f"query={query}", "--silent"])

    return resolve_http(target)


def resolve_http(target: str) -> str | None:
    request = urllib.request.Request(
        target, method="HEAD", headers={"User-Agent": USER_AGENT}
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status < 400:
                return None
            return f"HTTP {response.status}"
    except urllib.error.HTTPError as error:
        if error.code in (403, 405):
            try:
                get = urllib.request.Request(target, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(get, timeout=20) as response:
                    return None if response.status < 400 else f"HTTP {response.status}"
            except Exception as retry_error:  # noqa: BLE001 - reported verbatim
                return f"{type(retry_error).__name__}: {retry_error}"
        return f"HTTP {error.code}"
    except Exception as error:  # noqa: BLE001 - reported verbatim
        return f"{type(error).__name__}: {error}"


def check(document: Path, online: bool) -> list[str]:
    failures = []
    for target in references(document.read_text()):
        if is_repository_tree_url(target):
            reason = resolve_repository_url(target)
            kind = "repository"
        elif target.startswith(("http://", "https://")):
            if not online:
                failures.append(f"{target} — remote, and --online was not given")
                continue
            reason = resolve_github(target)
            kind = "remote"
        elif ":" in target.split("/")[0]:
            failures.append(f"{target} — reference carries an unsupported scheme")
            continue
        else:
            reason = resolve_local(document, target)
            kind = "local"
        if reason:
            failures.append(f"{target} — {reason}")
        else:
            print(f"ok   {kind:10} {target}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "documents",
        nargs="*",
        default=["README.md"],
        help="documents to check, relative to the repository root",
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="reach references outside this repository over the network",
    )
    arguments = parser.parse_args()

    failures = []
    for name in arguments.documents:
        document = (ROOT / name).resolve()
        if not document.exists():
            failures.append(f"{name} — the document to check does not exist")
            continue
        failures += [
            f"{name}: {failure}" for failure in check(document, arguments.online)
        ]

    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"\nlink check: {len(failures)} unresolved reference(s)", file=sys.stderr)
        return 1
    print("\nlink check: every reference resolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
