#!/usr/bin/env python3
"""Report where the work-planner example departs from its authoring rules.

The example's guidelines state how an operation, a command and a link are
written. This check reads every Markdown document `documents.py` finds under
`example/work-planner/` and reports each departure by file and line, grouped
by area: modes, protocols, artifacts, references and the entry files beside
`SKILL.md`. Each finding kind is one rule the guidelines state:

- **Inputs and Outputs.** An operation, a `###` heading under `## Operations`,
  carries an `**Inputs:**` and an `**Outputs:**` line ahead of its first step,
  each one line holding `None` or a comma-separated list of links whose
  targets are contract sections.
- **Commands section.** No file has a heading titled `Commands`.
- **Command placement.** A shell command sits in an unindented fenced block
  within a step: a step sub-section, or an operation or procedure of one step
  written with no step heading.
- **File-relative links.** A cross-file link is written from the file that
  holds it: never an absolute path, a URL into this repository naming a file
  this checkout holds, or a path that resolves only from the root the file's
  front matter declares.

Fenced blocks are blanked before headings and links are read, an indented
fence included, since a heading or a link written inside one is an example.
A fenced block opens at a run of three or more backticks or tildes and closes
at a run of the same character at least as long, so a template fence holding
a command fence is one block.

The check also lists each file over about 20 KB or 8 operations, which the
guidelines ask a reviewer to read for a second subject. That list is a report,
not a finding. The check exits nonzero when any finding exists.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import documents
from links import (
    INLINE_LINK,
    REFERENCE_DEFINITION,
    REPOSITORY_URL_PREFIX,
    is_repository_tree_url,
)

TREE = "example/work-planner/"
AREAS = ("modes", "protocols", "artifacts", "references")
ENTRY = "entry files"

INPUTS = "Inputs and Outputs"
COMMANDS_SECTION = "Commands section"
COMMAND_PLACEMENT = "Command placement"
FILE_RELATIVE = "File-relative links"
KINDS = (INPUTS, COMMANDS_SECTION, COMMAND_PLACEMENT, FILE_RELATIVE)

SIZE_LIMIT = 20 * 1024
OPERATION_LIMIT = 8

FENCE_OPEN = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
STEP = re.compile(r"^\d+\.\s")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
DECLARED_ROOT = re.compile(r'^  root: "([^"]*)"', re.MULTILINE)
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
SHELL = frozenset({"bash", "sh", "shell", "zsh", "console"})
CONTRACT_LINK = r"\[[^\]]+\]\([^)\s#]*#[^)\s]+\)"
LINK_LIST = re.compile(rf"^{CONTRACT_LINK}(?:, {CONTRACT_LINK})*$")
LABELS = ("Inputs", "Outputs")


@dataclass(frozen=True)
class Finding:
    """One departure from a rule, at a line of a document."""

    path: str
    line: int
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line} — {self.kind}: {self.detail}"


@dataclass(frozen=True)
class Fence:
    """One fenced block: its opening line, its indent and its info string."""

    line: int
    indent: str
    info: str


@dataclass(frozen=True)
class Heading:
    """One heading outside literal content, with its line, level and title."""

    line: int
    level: int
    title: str


def fences(lines: list[str]) -> tuple[list[Fence], list[str]]:
    """Each fenced block, and the lines with every fenced block blanked."""
    found: list[Fence] = []
    blanked: list[str] = []
    closing: re.Pattern[str] | None = None
    for number, line in enumerate(lines, 1):
        if closing is not None:
            if closing.match(line):
                closing = None
            blanked.append("")
            continue
        opened = FENCE_OPEN.match(line)
        if opened is None or (opened.group(2)[0] == "`" and "`" in opened.group(3)):
            blanked.append(line)
            continue
        indent, run, info = opened.groups()
        found.append(Fence(number, indent, info.strip().split(" ")[0].lower()))
        closing = re.compile(rf"^\s*{re.escape(run[0])}{{{len(run)},}}\s*$")
        blanked.append("")
    return found, blanked


def front_matter(text: str) -> str:
    """The text with its front matter blanked, its lines kept."""
    matched = FRONT_MATTER.match(text)
    if matched is None:
        return text
    return "\n" * matched.group(0).count("\n") + text[matched.end() :]


def headings(lines: list[str]) -> list[Heading]:
    found: list[Heading] = []
    for number, line in enumerate(lines, 1):
        matched = HEADING.match(line)
        if matched is not None:
            found.append(
                Heading(number, len(matched.group(1)), matched.group(2).strip())
            )
    return found


def plain_title(title: str) -> str:
    return title.replace("*", "").replace("_", "").strip()


def section_end(heads: list[Heading], index: int, total: int) -> int:
    """The last line of the section the heading at that index opens."""
    level = heads[index].level
    for later in heads[index + 1 :]:
        if later.level <= level:
            return later.line - 1
    return total


def has_steps(heads: list[Heading], index: int) -> bool:
    """Whether the section the heading opens holds a step sub-section."""
    level = heads[index].level
    for later in heads[index + 1 :]:
        if later.level <= level:
            return False
        if STEP.match(later.title):
            return True
    return False


def operations(heads: list[Heading]) -> list[int]:
    """The index of each operation heading: a `###` under `## Operations`."""
    found: list[int] = []
    parent = ""
    for index, heading in enumerate(heads):
        if heading.level <= 2:
            parent = plain_title(heading.title) if heading.level == 2 else ""
        elif heading.level == 3 and parent == "Operations":
            found.append(index)
    return found


def enclosing(heads: list[Heading], line: int) -> list[int]:
    """The indices of the headings enclosing a line, outermost first."""
    stack: list[int] = []
    for index, heading in enumerate(heads):
        if heading.line > line:
            break
        while stack and heads[stack[-1]].level >= heading.level:
            stack.pop()
        stack.append(index)
    return stack


def inputs_outputs(
    name: str, lines: list[str], heads: list[Heading], index: int
) -> list[Finding]:
    """Each way one operation's Inputs and Outputs lines break their rule."""
    heading = heads[index]
    title = plain_title(heading.title)
    end = section_end(heads, index, len(lines))
    first_sub = next(
        (later.line for later in heads[index + 1 :] if later.line <= end), end + 1
    )
    found: list[Finding] = []
    for label in LABELS:
        prefix = f"**{label}:**"
        at = next(
            (
                number
                for number in range(heading.line + 1, first_sub)
                if lines[number - 1].startswith(prefix)
            ),
            None,
        )
        if at is None:
            found.append(
                Finding(
                    name,
                    heading.line,
                    INPUTS,
                    f"operation '{title}' has no {prefix} line ahead of its steps",
                )
            )
            continue
        value = lines[at - 1][len(prefix) :].strip()
        if value != "None" and not LINK_LIST.match(value):
            found.append(
                Finding(
                    name,
                    at,
                    INPUTS,
                    f"operation '{title}' {label} is not None or a comma-separated "
                    "list of links to contract sections",
                )
            )
        following = lines[at] if at < len(lines) else ""
        if following.strip() and not following.startswith("**Outputs:**"):
            found.append(
                Finding(
                    name,
                    at,
                    INPUTS,
                    f"operation '{title}' {label} runs onto line {at + 1}",
                )
            )
    return found


def in_step(heads: list[Heading], chain: list[int], ops: set[int]) -> bool:
    """Whether a line under that chain of headings sits within a step."""
    if any(STEP.match(heads[index].title) for index in chain):
        return True
    if not chain:
        return False
    innermost = chain[-1]
    single = innermost in ops or plain_title(heads[innermost].title) == "Procedure"
    return single and not has_steps(heads, innermost)


def placements(
    name: str, found: list[Fence], heads: list[Heading], ops: set[int]
) -> list[Finding]:
    """Each shell command fence that is indented or outside a step."""
    out: list[Finding] = []
    for fence in found:
        if fence.info not in SHELL:
            continue
        chain = enclosing(heads, fence.line)
        reasons = []
        if not in_step(heads, chain, ops):
            where = plain_title(heads[chain[-1]].title) if chain else "the preamble"
            reasons.append(f"sits outside a step, under '{where}'")
        if fence.indent:
            reasons.append("its fence is indented")
        if reasons:
            out.append(
                Finding(
                    name,
                    fence.line,
                    COMMAND_PLACEMENT,
                    f"a command {' and '.join(reasons)}; a command sits in an "
                    "unindented fenced block in the step that runs it",
                )
            )
    return out


def declared_root(document: Path, text: str) -> Path | None:
    matched = FRONT_MATTER.match(text)
    if matched is None:
        return None
    root = DECLARED_ROOT.search(matched.group(1))
    return None if root is None else (document.parent / root.group(1)).resolve()


def link_form(document: Path, root: Path | None, target: str) -> str | None:
    """Why one link target is not file-relative, or None when it is."""
    if is_repository_tree_url(target):
        parts = target[len(REPOSITORY_URL_PREFIX) :].partition("#")[0].split("/")
        path = "/".join(parts[2:])
        if path and (documents.ROOT / path).exists():
            return f"{target} is a repository URL to a file this checkout holds"
        return None
    if SCHEME.match(target):
        return None
    path_part = target.partition("#")[0]
    if not path_part:
        return None
    if path_part.startswith("/"):
        return f"{target} is an absolute path"
    if (
        root is not None
        and root != document.parent.resolve()
        and not (document.parent / path_part).exists()
        and (root / path_part).exists()
    ):
        return f"{target} resolves from the declared root, not from the file"
    return None


def link_findings(
    name: str, document: Path, text: str, lines: list[str]
) -> list[Finding]:
    root = declared_root(document, text)
    body = documents.strip_code_spans(documents.strip_indented_blocks("\n".join(lines)))
    found: list[Finding] = []
    for number, line in enumerate(body.splitlines(), 1):
        targets = INLINE_LINK.findall(line) + REFERENCE_DEFINITION.findall(line)
        for target in targets:
            reason = link_form(document, root, target)
            if reason is not None:
                found.append(Finding(name, number, FILE_RELATIVE, reason))
    return found


def report(document: Path, name: str, text: str) -> tuple[list[Finding], int]:
    """Every finding in one document, and the number of operations it holds."""
    found, blanked = fences(front_matter(text).splitlines())
    heads = headings(blanked)
    ops = operations(heads)
    out: list[Finding] = []
    for index in ops:
        out.extend(inputs_outputs(name, blanked, heads, index))
    out.extend(
        Finding(
            name,
            heading.line,
            COMMANDS_SECTION,
            f"a '{heading.title}' heading; no file has a Commands section",
        )
        for heading in heads
        if plain_title(heading.title) == "Commands"
    )
    out.extend(placements(name, found, heads, set(ops)))
    out.extend(link_findings(name, document, text, blanked))
    return sorted(out, key=lambda finding: finding.line), len(ops)


def area(name: str) -> str:
    """The area a document under the tree belongs to."""
    first = name[len(TREE) :].split("/")[0]
    return first if first in AREAS else ENTRY


def oversized(size: int, operation_count: int) -> bool:
    return size > SIZE_LIMIT or operation_count > OPERATION_LIMIT


def scope() -> list[Path]:
    """Every Markdown document git tracks under the work-planner example."""
    return [
        path
        for path in documents.documents()
        if path.relative_to(documents.ROOT).as_posix().startswith(TREE)
    ]


def main() -> int:
    paths = scope()
    by_area: dict[str, list[Finding]] = {name: [] for name in (*AREAS, ENTRY)}
    sizes: list[tuple[str, int, int]] = []
    for path in paths:
        name = path.relative_to(documents.ROOT).as_posix()
        text = path.read_text()
        found, count = report(path, name, text)
        by_area[area(name)].extend(found)
        size = len(text.encode())
        if oversized(size, count):
            sizes.append((name, size, count))
    total = sum(len(found) for found in by_area.values())
    print(f"authoring check: {len(paths)} document(s) under {TREE}")
    for name, found in by_area.items():
        print(f"\n{name}: {len(found)} finding(s)")
        for finding in found:
            print(f"  {finding}")
    print(
        f"\nsize report: over {SIZE_LIMIT // 1024} KB or {OPERATION_LIMIT} "
        "operations, for a reviewer to read for a second subject"
    )
    for name, size, count in sizes:
        print(f"  {name} — {size / 1024:.1f} KB, {count} operation(s)")
    print("\nfindings by area and kind:")
    print(f"  {'area':<12} " + " | ".join(KINDS))
    for name, found in by_area.items():
        counts = [str(sum(f.kind == kind for f in found)) for kind in KINDS]
        print(f"  {name:<12} " + " | ".join(counts))
    print(f"\nauthoring check: {total} finding(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
