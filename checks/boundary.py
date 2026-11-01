#!/usr/bin/env python3
"""Report the boundary each work-planner example document derives from its links.

A document's boundary is the deepest directory holding every local Markdown
path its own links name, normalised from the document's directory; a document
naming none has its own directory. This check reads every Markdown document
`documents.py` finds under `example/work-planner/`, which is the skill's
directory and so the working directory a run is invoked from, and prints the
boundary the build derives for each one.

The boundary is derived from the links, so it holds every one of them. The
check holds the build to that: each local Markdown path a document's links
name must sit in the boundary derived for that document, and a link outside it
is reported by file and line. A link the path grammar refuses names no path
and is not asked.

The boundary is the build's own answer, so the check reads it from the build
in the locked environment rather than restating the rule. Frontmatter is
dropped before the document is parsed, as a capture drops it, and is never
decoded: what the declaration says decides nothing about which paths the
links name.
"""

import sys
from pathlib import Path

import documents

from prosiform.closure import PARENT, SEPARATOR, boundary, climb, named
from prosiform.profile import parse
from prosiform.source import MARK, frontmatter, lines, regions, uses

TREE = "example/work-planner/"
WORKING = documents.ROOT / TREE
HERE = "."


def body(text: str) -> tuple[str, int]:
    """One document's content after its frontmatter, and the line it starts on."""
    content = text.removeprefix(MARK)
    found = frontmatter(text)
    if found is None:
        return content, 1
    _span, closer = found
    return "".join(lines(content)[closer + 1 :]), closer + 2


def held(path: str, within: str) -> bool:
    """Whether a working-directory-relative path sits in one directory.

    Either may open with parent segments. A directory that is only parent
    segments holds every path climbing no further than it does; any other
    holds the paths climbing as far and continuing below it.
    """
    climbs = climb(within)
    below = [part for part in within.split(SEPARATOR)[climbs:] if part]
    parts = path.split(SEPARATOR)
    if not below:
        return climb(path) <= climbs
    return (
        parts[:climbs] == [PARENT] * climbs
        and parts[climbs : climbs + len(below)] == below
        and len(parts) > climbs + len(below)
    )


def scope() -> list[Path]:
    """Every Markdown document of the example, in path order."""
    return [
        path
        for path in documents.documents()
        if path.relative_to(documents.ROOT).as_posix().startswith(TREE)
    ]


def main() -> int:
    paths = scope()
    outside: list[str] = []
    print(f"boundary check: {len(paths)} document(s) under {TREE}")
    for path in paths:
        name = path.relative_to(WORKING).as_posix()
        text, first = body(path.read_text())
        tokens = parse(text)
        derived = boundary(name, tokens)
        print(f"  {name}: {derived or HERE}")
        for use in uses(tokens, tuple(regions(tokens))):
            found = None if use.resource else named(name, use.destination)
            if found is not None and not held(found.path, derived):
                at = "" if use.line is None else f":{use.line + first - 1}"
                outside.append(
                    f"  {name}{at}: {use.destination!r} names {found.path!r}, "
                    f"outside the boundary {derived or HERE!r}"
                )
    for line in outside:
        print(line)
    print(f"boundary check: {len(outside)} link(s) outside their boundary")
    return 1 if outside else 0


if __name__ == "__main__":
    sys.exit(main())
