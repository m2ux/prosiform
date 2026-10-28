#!/usr/bin/env python3
"""Assert the work-planner example writes each procedure's steps as sub-sections.

A procedure with more than one step writes each step as a heading one level
below the procedure's own, headed by its position, a full stop and its action:
`### 6. Publish` under `## Procedure`. That heading roots the anchor a link to
the step opens. A numbered list carries no anchor, a step heading deeper than
one level below its parent no longer reads as that procedure's step, and a
step heading repeated in one document takes a suffixed anchor, so a link
written to its plain slug opens the first.

The guard reads every Markdown document `documents.py` finds under
`example/work-planner/`, the skill whose guidelines state the convention, with
fenced and indented blocks blanked, since a numbered list written as an example
is not a step list. Separate documents legitimately share a step, such as
`### 1. Select` in two modes, and each is its own bundle entry, so a repeat is
read within one document.
"""

import re
import sys
from pathlib import Path

import documents

TREE = "example/work-planner/"

NUMBERED_ITEM = re.compile(r"^\d+\.(?:\s|$)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
STEP = re.compile(r"^\d+\.\s")


def failures(name: str, text: str) -> list[str]:
    """Each place the document breaks the step convention, as `name:line — why`."""
    found: list[str] = []
    levels: list[int] = []
    seen: dict[str, int] = {}
    blanked = documents.strip_indented_blocks(documents.strip_code_fences(text))
    for number, line in enumerate(blanked.splitlines(), 1):
        if NUMBERED_ITEM.match(line):
            found.append(
                f"{name}:{number} — a numbered list item; write each step as an "
                "'N. Action' heading one level below its procedure"
            )
            continue
        heading = HEADING.match(line)
        if heading is None:
            continue
        level, title = len(heading.group(1)), heading.group(2)
        parent = next((above for above in reversed(levels) if above < level), 0)
        levels.append(level)
        if not STEP.match(title):
            continue
        if level != parent + 1:
            found.append(
                f"{name}:{number} — step heading '{title}' sits {level - parent} "
                "levels below its parent; a step sits exactly one level below"
            )
        if title in seen:
            found.append(
                f"{name}:{number} — step heading '{title}' repeats line "
                f"{seen[title]}, so its anchor takes a suffix"
            )
        else:
            seen[title] = number
    return found


def scope() -> list[Path]:
    """Every Markdown document git tracks under the work-planner example."""
    return [
        path
        for path in documents.documents()
        if path.relative_to(documents.ROOT).as_posix().startswith(TREE)
    ]


def main() -> int:
    paths = scope()
    found = [
        failure
        for path in paths
        for failure in failures(
            path.relative_to(documents.ROOT).as_posix(), path.read_text()
        )
    ]
    for failure in found:
        print(f"FAIL {failure}", file=sys.stderr)
    if found:
        print(
            f"\nstep check: {len(found)} place(s) breaking the step convention",
            file=sys.stderr,
        )
        return 1
    print(
        f"step check: every procedure in {len(paths)} document(s) under {TREE} "
        "writes its steps as sub-sections"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
