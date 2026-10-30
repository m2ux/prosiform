#!/usr/bin/env python3
"""Draw authored sources and the bundles a run of them produces.

Each case in `examples.json` names an entry and the files around it. The
build runs for real over a copy of that tree, and the drawing shows the
files it opened beside the bundles it published, so a picture cannot state
a result the build does not produce.

The style is the one `docs/images/compilation.svg` sets: a dark panel per
file, heading levels marked at the left margin, and links in blue.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent
CASES = HERE / "examples.json"

FONT = "IBM Plex Mono"
BG, CARD, BORDER = "#0d1117", "#161b22", "#303b49"
TEXT, MUTED, LINK, AMBER = "#e6edf3", "#b1c6df", "#58a6ff", "#e3b341"

WIDTH = 2142
SOURCE_X, SOURCE_Y = 32, 80
COLUMN, TREE_WIDTH, PANEL_WIDTH = 1000, 1000, 1000
OUTPUT_X = 1110


def txt(
    x: int, y: int, value: str, size: int = 20, color: str = TEXT, weight: int = 400
) -> str:
    """One line of text, escaped."""
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}">{html.escape(value)}</text>'
    )


def rows_of(body: str, width: int) -> list[tuple[str, int, int, int, bool]]:
    """Each line to draw: its text, step height, size, heading level and link flag."""
    rows: list[tuple[str, int, int, int, bool]] = []
    section = 0
    for raw in body.splitlines():
        if not raw.strip():
            rows.append(("", 11, 18, 0, False))
            continue
        heading = re.match(r"^(#{1,6}) (.*)", raw)
        level = len(heading[1]) if heading else 0
        if heading:
            section = level
        indent = level or (section + 1 if section else 0)
        value = heading[2] if heading else raw
        links = bool(re.search(r"\[[^\]]+\]\([^)]+\)", raw))
        value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
        value = re.sub(r"^- ", "• ", value)
        size = 30 if level == 1 else 26 if level == 2 else 23 if level else 20
        available = max(20, int((width - 62 - indent * 12) / (size * 0.62)))
        wrapped = textwrap.wrap(
            value, available, break_long_words=False, break_on_hyphens=False
        ) or [""]
        for index, part in enumerate(wrapped):
            rows.append((part, size + 17, size, level, links and index == len(wrapped) - 1))
    return rows


def card(x: int, y: int, width: int, title: str, body: str) -> tuple[str, int]:
    """One panel: a titled box holding the lines of one file's content."""
    rows = rows_of(body, width)
    height = 72 + sum(row[1] for row in rows) + 20
    out = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" '
        f'fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>',
        txt(x + 24, y + 36, title, 21, MUTED),
        f'<path d="M{x} {y + 54} H{x + width}" stroke="{BORDER}"/>',
    ]
    at = y + 74
    for value, step, size, level, is_link in rows:
        at += step
        if not value:
            continue
        if level:
            out.append(txt(x + 12, at, f"H{level}", 11, MUTED))
        operator = "¬" in value or "⇉" in value or "⫽" in value
        color = AMBER if operator else LINK if is_link else TEXT
        out.append(txt(x + 38 + level * 12, at, value, size, color, 500 if level else 400))
    return "\n".join(out), height


def tree_of(paths: list[str], root: str) -> str:
    """One file tree, every directory a path implies."""
    nodes: dict = {}
    for path in sorted(paths):
        node = nodes
        for part in path.split("/"):
            node = node.setdefault(part, {})
    lines = [f"{root}/"]

    def branch(node: dict, prefix: str = "") -> None:
        for index, (name, children) in enumerate(node.items()):
            last = index == len(node) - 1
            lines.append(
                prefix + ("└─ " if last else "├─ ") + name + ("/" if children else "")
            )
            branch(children, prefix + ("   " if last else "│  "))

    branch(nodes)
    return "\n".join(lines)


def arrow(x: int, y: int) -> str:
    """The compile arrow between the two columns."""
    return (
        f'<path d="M{x} {y} H{x + 18} V{y - 12} L{x + 46} {y + 16} '
        f'L{x + 18} {y + 44} V{y + 32} H{x}Z" fill="{LINK}"/>'
    )


def draw(root: Path, sources: list[str], bundles: list[str]) -> str:
    """The drawing of one run: the sources it read and the bundles it wrote."""
    block, tree_height = card(
        SOURCE_X, SOURCE_Y, TREE_WIDTH, "Files", tree_of(sources, root.name)
    )
    left = [block]
    at = SOURCE_Y + tree_height + 22
    for path in sources:
        block, height = card(
            SOURCE_X, at, COLUMN, path, (root / path).read_text(encoding="utf-8")
        )
        left.append(block)
        at += height + 22
    right = []
    at = SOURCE_Y
    if not bundles:
        right.append(txt(OUTPUT_X + 24, 116, "nothing published", 21, MUTED))
    for name in bundles:
        block, height = card(
            OUTPUT_X, at, PANEL_WIDTH, name, (root / name).read_text(encoding="utf-8")
        )
        right.append(block)
        at += height + 22
    height = max(at, SOURCE_Y + tree_height) + 65
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc">'
        '<title id="title">Authored sources and compiled bundles</title>'
        f'<desc id="desc">The files a run read, beside the bundles it wrote.</desc>'
        f'<rect width="{WIDTH}" height="{height}" fill="{BG}"/>'
        f'<g font-family="{FONT}" xml:space="preserve">'
        + "".join(left + right)
        + arrow(OUTPUT_X - 58, 180)
        + "</g></svg>\n"
    )


def render(name: str, case: dict, build: list[str], output: Path) -> int:
    """Run one case's build over its tree, and write its drawing."""
    work = Path(tempfile.mkdtemp())
    try:
        for path, body in case["files"].items():
            target = work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body)
        result = subprocess.run(
            [*build, case["entry"]], cwd=work, capture_output=True, text=True
        )
        bundles = sorted(
            path.relative_to(work).as_posix()
            for path in work.rglob("*.bundle.md")
        )
        sources = sorted(
            path.relative_to(work).as_posix()
            for path in work.rglob("*.md")
            if path.relative_to(work).as_posix() not in bundles
        )
        drawn = draw(work, sources, bundles)
        ElementTree.fromstring(drawn)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(drawn)
        print(f"{name}: {output}, exit {result.returncode}, {len(bundles)} bundle(s)")
        if result.returncode != 0:
            print(result.stderr.rstrip())
        return result.returncode
    finally:
        shutil.rmtree(work)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "case",
        nargs="*",
        help="case name; every case in examples.json when none is named",
    )
    parser.add_argument("--output", type=Path, help="directory; defaults to docs/images")
    parser.add_argument(
        "--build",
        default="pf",
        help="the build's command line, split as a shell splits one",
    )
    options = parser.parse_args()
    cases = json.loads(CASES.read_text())
    named = options.case or sorted(cases)
    unknown = [one for one in named if one not in cases]
    if unknown:
        parser.error(f"no case named {', '.join(unknown)}")
    output = options.output or HERE.parent / "docs" / "images"
    failures = 0
    for name in named:
        failures += render(name, cases[name], options.build.split(), output / f"{name}.svg") != 0
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
