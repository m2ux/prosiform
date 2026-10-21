#!/usr/bin/env python3
"""Assert every reference every document the repository owns resolves.

The documents are found rather than listed, so a document added later comes
into the check by being committed. The fixture corpus is excepted: a fixture's
source carries references a run is meant to refuse, and its expected bundle is
output rather than a document a reader follows. Naming documents on the command
line checks those instead, which is for reading one document while editing it.

A link form written inside literal content — a code span, a fenced block or
an indented block — is the spelling of a link rather than a link, so it is
blanked out before the document is scanned and a link beside it is resolved.

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
  `--online` such a reference counts as unresolved and the check fails,
  so an offline run cannot pass.

A host that says nothing is told apart from a reference that does not
resolve. A server error, a refusal of the caller, a timeout or a dropped
connection means the host reported nothing about the target, so after a
bounded number of attempts it is counted as unreachable and the run passes
carrying that verdict. A check that fails on a third party teaches a reader
to re-run it rather than to read it, which is the habit that lets a genuine
broken reference through.
"""

import argparse
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from documents import ROOT, documents, strip_code_fences, strip_literal

REPOSITORY_URL_PREFIX = "https://github.com/m2ux/prosiform/"

INLINE_LINK = re.compile(r"\]\(\s*<?([^()<>\s]+)>?\s*(?:\"[^\"]*\")?\s*\)")
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+)>?", re.MULTILINE)
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
CODE_SPAN = re.compile(r"`([^`]*)`")
LINK_TEXT = re.compile(r"\[([^\]]*)\]\([^)]*\)")
UNDERSCORE_EMPHASIS = re.compile(r"(?<![_\w])_{1,2}([^_\n]+)_{1,2}(?![_\w])")
SLUG_KEPT = frozenset("-_ ")

USER_AGENT = "prosiform-link-check"

ATTEMPTS = 3
DELAY = 2.0
TIMEOUT = 20
SAYS_NOTHING = re.compile(r"HTTP (?:5\d\d|403)")


@dataclass(frozen=True)
class Unreachable:
    """A host that said nothing, which is not an unresolved reference.

    A reference is unresolved when the host answered and said the target
    is not there. A host returning a server error, refusing the caller,
    timing out or dropping the connection has said nothing about the
    target, so it carries a verdict of its own and leaves the run passing.
    """

    reason: str


Outcome = str | Unreachable | None


def retried(resolve: Callable[[], Outcome]) -> Outcome:
    """One address resolved, reattempted while the host says nothing.

    The delay grows with each attempt, so a host restarting behind a load
    balancer is given longer than one that answered at once. An outcome
    the host did state is returned on the attempt that produced it.
    """
    outcome = resolve()
    for attempt in range(1, ATTEMPTS):
        if not isinstance(outcome, Unreachable):
            return outcome
        time.sleep(DELAY * attempt)
        outcome = resolve()
    return outcome


def slug(heading: str) -> str:
    """The fragment GitHub generates for a heading.

    A code span, a link and a run of emphasis reduce to their text, which is
    what the rendering they mark leaves behind. What survives is lowercased
    and holds its letters, numbers and combining marks, its hyphens and its
    underscores; punctuation and symbols, an emoji among them, are dropped.
    Each remaining space becomes a hyphen, and nothing is trimmed, so a
    heading opening with an emoji yields a leading hyphen: `## ✅ Checks`
    generates `#-checks`.

    An underscore inside a word is a character of that word rather than a
    mark, so `Snake_case` keeps it while `_underlined_` does not.
    """
    text = CODE_SPAN.sub(r"\1", heading)
    text = LINK_TEXT.sub(r"\1", text)
    text = UNDERSCORE_EMPHASIS.sub(r"\1", text)
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
    """Each reference one document carries, read once and in the order written.

    Literal content is blanked out first, so a link form written inside a
    code span, a fenced block or an indented block is the spelling of a link
    and is passed over, while a link beside it is resolved.
    """
    body = strip_literal(text)
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


def gh_api(arguments: list[str]) -> Outcome:
    """Run an authenticated GitHub API call, or report why it did not answer.

    A missing command is the caller's to fix and fails the check. A call
    that timed out or came back carrying a server status or a refusal of
    the caller is the host saying nothing, which is a verdict of its own.
    """
    try:
        result = subprocess.run(
            ["gh", "api", *arguments], capture_output=True, text=True, timeout=30
        )
    except FileNotFoundError:
        return (
            "gh is not installed, and a private reference needs an authenticated read"
        )
    except subprocess.TimeoutExpired:
        return Unreachable("gh did not answer within 30s")
    if result.returncode != 0:
        reason = (
            result.stderr.strip().splitlines()[-1] if result.stderr else "gh failed"
        )
        return Unreachable(reason) if SAYS_NOTHING.search(reason) else reason
    return None


def resolve_github(target: str) -> Outcome:
    """Resolve a tracker reference with the caller's credentials.

    A private repository answers an unauthenticated request with 404, so an
    issue, a pull request or a project board is read through the API rather
    than fetched as a page.
    """
    issue = GITHUB_ISSUE.match(target)
    if issue:
        owner, repository, kind, number = issue.groups()
        endpoint = "issues" if kind == "issues" else "pulls"
        path = f"repos/{owner}/{repository}/{endpoint}/{number}"
        return retried(lambda: gh_api([path, "--silent"]))

    project = GITHUB_USER_PROJECT.match(target)
    if project:
        scope, login, number = project.groups()
        owner_field = "user" if scope == "users" else "organization"
        query = (
            f'{{ {owner_field}(login: "{login}") '
            f"{{ projectV2(number: {number}) {{ id }} }} }}"
        )
        return retried(lambda: gh_api(["graphql", "-f", f"query={query}", "--silent"]))

    return retried(lambda: reach(target))


def verdict(status: int) -> Outcome:
    """What a status the host returned says about the target.

    A server status is the host reporting its own trouble and states
    nothing about the target. A forbidden status is the host refusing
    this caller: it turns on the address the request came from and the
    agent it named, so the same target answers one reader and refuses
    another, and it states nothing about the target either. Any other
    client status is an answer about the target, and the check holds the
    document to it.

    401 and 405 are answers a reader meets too. 405 names the methods the
    address allows, and the method the reader uses is the one this check
    falls back to, so a host refusing both is serving no reader. 401 names
    an authorization scheme, and a reference a reader must hold credentials
    to follow is one the document should say so about; it is also the status
    `gh api` returns when this check's own credentials are missing, so
    counting it as silence would let a run that read no tracker reference
    pass.
    """
    if status < 400:
        return None
    if status >= 500 or status == 403:
        return Unreachable(f"HTTP {status}")
    return f"HTTP {status}"


def fetched(target: str, method: str | None) -> int:
    """The status one request to an address returns."""
    headers = {"User-Agent": USER_AGENT}
    request = (
        urllib.request.Request(target, method=method, headers=headers)
        if method
        else urllib.request.Request(target, headers=headers)
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return int(response.status)


def reach(target: str) -> Outcome:
    """One attempt at a remote address.

    A host answering 403 or 405 to HEAD may be answering about the method
    rather than the target, so the address is asked for again with GET
    before its status is read, and a host that serves the page to GET
    resolves. A host refusing GET as well is read by `verdict`, which
    forbids the one and holds the document to the other. 401 turns on
    credentials rather than on the method, so it is decided on the answer
    to HEAD. A connection that failed, timed out or was
    dropped is the host saying nothing and takes the unreachable verdict;
    anything else the request raises is the reference's own fault and
    fails the check.
    """
    try:
        return verdict(fetched(target, "HEAD"))
    except urllib.error.HTTPError as error:
        if error.code not in (403, 405):
            return verdict(error.code)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
        return Unreachable(f"{type(error).__name__}: {error}")
    except Exception as error:  # noqa: BLE001 - reported verbatim
        return f"{type(error).__name__}: {error}"
    try:
        return verdict(fetched(target, None))
    except urllib.error.HTTPError as error:
        return verdict(error.code)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
        return Unreachable(f"{type(error).__name__}: {error}")
    except Exception as error:  # noqa: BLE001 - reported verbatim
        return f"{type(error).__name__}: {error}"


def check(document: Path, online: bool) -> tuple[list[str], list[str]]:
    """Every reference one document carries, resolved.

    The unresolved references come back beside the ones whose host said
    nothing, because the two decide the run differently.
    """
    failures: list[str] = []
    unanswered: list[str] = []
    for target in references(document.read_text()):
        reason: Outcome
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
        if isinstance(reason, Unreachable):
            unanswered.append(f"{target} — {reason.reason}")
        elif reason:
            failures.append(f"{target} — {reason}")
        else:
            print(f"ok   {kind:10} {target}")
    return failures, unanswered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "documents",
        nargs="*",
        help="documents to check, relative to the repository root, in place of "
        "every document the repository owns",
    )
    parser.add_argument(
        "--online",
        action="store_true",
        help="reach references outside this repository over the network",
    )
    arguments = parser.parse_args()

    named = [(ROOT / name).resolve() for name in arguments.documents]
    selected = named or documents()
    failures: list[str] = []
    unanswered: list[str] = []
    for document in selected:
        name = (
            document.relative_to(ROOT).as_posix()
            if document.is_relative_to(ROOT)
            else str(document)
        )
        if not document.exists():
            failures.append(f"{name} — the document to check does not exist")
            continue
        unresolved, unreached = check(document, arguments.online)
        failures += [f"{name}: {failure}" for failure in unresolved]
        unanswered += [f"{name}: {one}" for one in unreached]

    for one in unanswered:
        print(f"WARN {one}", file=sys.stderr)
    for failure in failures:
        print(f"FAIL {failure}", file=sys.stderr)
    if failures:
        print(f"\nlink check: {len(failures)} unresolved reference(s)", file=sys.stderr)
        return 1
    resolved = f"link check: every reference in {len(selected)} document(s) resolved"
    if unanswered:
        print(f"\n{resolved}, except {len(unanswered)} whose host did not answer")
        return 0
    print(f"\n{resolved}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
