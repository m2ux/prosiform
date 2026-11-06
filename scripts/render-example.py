#!/usr/bin/env python3
"""Draw authored sources and the bundles a run of them produces.

Each case in `examples.json` names an entry and the files around it. The
build runs for real over a copy of that tree, and the drawing shows the
files it opened beside the bundles it published, so a picture cannot state
a result the build does not produce.

Each drawing sets a dark panel per file and draws links in blue. The README's
run example traces links between source documents and within the bundle;
the other examples mark heading levels at the left margin.
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from urllib.parse import urldefrag
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

# The tree's name in every drawing. A run's working directory is a temporary
# directory whose name would otherwise appear in the picture.
ROOT_LABEL = "skill"


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
            rows.append(
                (part, size + 17, size, level, links and index == len(wrapped) - 1)
            )
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
        out.append(
            txt(x + 38 + level * 12, at, value, size, color, 500 if level else 400)
        )
    return "\n".join(out), height


def tree_of(paths: list[str], root: str) -> str:
    """One file tree, every directory a path implies.

    The root is the name the drawing shows, not the directory the run happened
    to use, so a picture states the same tree wherever it was rendered.
    """
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


def overview_panel(
    x: int, y: int, width: int, title: str, body: str, minimum: int = 0
) -> tuple[str, int, dict[str, tuple[float, float]], list[tuple[str, float, float]]]:
    """A rendered document, with coordinates for its headings and link labels."""
    from prosiform.source import content, fragments

    source = content(body)
    headings = re.findall(r"^#{1,6} (.+)$", source.text, re.MULTILINE)
    anchors = iter(fragments(headings))
    targets: dict[str, tuple[float, float]] = {}
    links: list[tuple[str, float, float]] = []
    rows = []
    at = y + 96
    if source.first_line > 1:
        metadata = " ".join(body.splitlines()[1 : source.first_line - 2])
        rows.append(txt(x + 28, at, metadata, 21, MUTED))
        at += 58
    for raw in source.text.splitlines():
        raw = raw.replace("`", "")
        if not raw:
            at += 18
            continue
        heading = re.match(r"^(#{1,6}) (.+)$", raw)
        if heading:
            level = len(heading[1])
            size = 34 if level == 1 else 29 if level == 2 else 26
            if targets:
                at += 14
            left = x + 28 + (level - 1) * 16
            rows.append(txt(left, at, heading[2], size, TEXT, 500))
            point = (left + len(heading[2]) * size * 0.6 + 16, at - size * 0.35)
            targets[next(anchors)] = point
            targets.setdefault("", point)
            at += size + 22
            continue

        # Each monospace character has one advance, including a link's label.
        size, advance = 26, 15.6
        available = int((width - 112) / advance)
        labels: list[tuple[int, int, str]] = []
        shown = ""
        end = 0
        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", raw):
            shown += raw[end : match.start()]
            start = len(shown)
            shown += match[1]
            labels.append((start, len(shown), match[2]))
            end = match.end()
        shown += raw[end:]
        wrapped = []
        offset = 0
        for line in textwrap.wrap(
            shown, available, break_long_words=False, break_on_hyphens=False
        ):
            start = shown.index(line, offset)
            stop = start + len(line)
            for _, last, _ in labels:
                if start < last < stop and shown[last:stop].strip(" .,!;:"):
                    wrapped.append(shown[start:last])
                    start = last
            wrapped.append(shown[start:stop].lstrip())
            offset = stop
        offset = 0
        for line in wrapped:
            start = shown.index(line, offset)
            stop = start + len(line)
            left = x + 28
            parts = []
            cursor = start
            for first, last, href in labels:
                a, b = max(first, start), min(last, stop)
                if a >= b:
                    continue
                parts.append(html.escape(shown[cursor:a]))
                parts.append(
                    f'<tspan fill="{LINK}" text-decoration="underline">'
                    f"{html.escape(shown[a:b])}</tspan>"
                )
                if b == last:
                    links.append((href, left + (b - start) * advance + 10, at - 9))
                cursor = b
            parts.append(html.escape(shown[cursor:stop]))
            rows.append(
                f'<text x="{left}" y="{at}" font-size="{size}" '
                f'fill="{TEXT}">{"".join(parts)}</text>'
            )
            at += 40
            offset = stop
    height = max(minimum, at - y + 12)
    panel = (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" '
        f'fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>'
        f'<path d="M{x + 12} {y} H{x + width - 12} Q{x + width} {y} '
        f"{x + width} {y + 12} V{y + 58} H{x} V{y + 12} "
        f'Q{x} {y} {x + 12} {y}" fill="#202a36"/>'
        + txt(x + 28, y + 38, title, 23, MUTED)
        + "\n".join(rows)
    )
    return panel, height, targets, links


def connector(start: tuple[float, float], end: tuple[float, float], lane: int) -> str:
    """Trace a link through a clear vertical lane to its actual target."""
    x, y = start
    tx, ty = end
    direction = 1 if tx > lane else -1
    vertical = 1 if ty > y else -1
    radius = 16
    return (
        f'<path d="M{x:g} {y:g} H{lane - radius} '
        f"Q{lane} {y:g} {lane} {y + vertical * radius:g} "
        f"V{ty - vertical * radius:g} Q{lane} {ty:g} "
        f'{lane + direction * radius} {ty:g} H{tx - direction * 12:g}" '
        f'fill="none" stroke="{LINK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<path d="M{tx:g} {ty:g} l{-direction * 12} -7 v14 Z" fill="{LINK}"/>'
    )


def draw_overview(root: Path, sources: list[str], bundle: str) -> str:
    """The README's connected source tree and complete, validated bundle."""
    width = 1800
    blocks = [
        txt(32, 64, "Linked Markdown. One complete context.", 40, TEXT, 500),
        txt(
            32,
            108,
            "Resolve the files. Keep the links. Include shared rules once.",
            23,
            MUTED,
        ),
        txt(32, 166, "01  SELECT AN ENTRY", 21, MUTED),
        txt(530, 166, "02  FOLLOW ITS LINKS", 21, MUTED),
        txt(1160, 166, "03  ONE VALIDATED BUNDLE", 21, MUTED),
    ]
    tree, tree_height, _, _ = overview_panel(
        32, 194, 430, "Source tree", tree_of(sources, ROOT_LABEL)
    )
    blocks.append(tree)
    positions = {"SKILL.md": (32, 194 + tree_height + 24, 430)}
    targets = {}
    references = []
    bottom = 194
    for path in sources:
        x, y, panel_width = positions.get(path, (530, bottom, 510))
        panel, height, anchors, links = overview_panel(
            x, y, panel_width, path, (root / path).read_text(encoding="utf-8")
        )
        blocks.append(panel)
        targets.update({(path, fragment): point for fragment, point in anchors.items()})
        references.extend((path, href, lx, ly) for href, lx, ly in links)
        if x == 530:
            bottom = y + height + 24
    source_bottom = bottom - 24
    panel, output_height, anchors, links = overview_panel(
        1160,
        194,
        608,
        bundle,
        (root / bundle).read_text(encoding="utf-8"),
        minimum=source_bottom - 194,
    )
    blocks.append(panel)
    for index, (path, href, x, y) in enumerate(references):
        target, fragment = urldefrag(href)
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
        point = targets[(target, fragment)]
        if path == "SKILL.md":
            point = (530, point[1])
            lane = 496
        else:
            lane = 1022 - (index - 1) * 18
        blocks.append(connector((x, y), point, lane))
    for index, (href, x, y) in enumerate(links):
        target, fragment = urldefrag(href)
        if target:
            raise ValueError(f"overview link leaves its bundle: {href}")
        blocks.append(connector((x, y), anchors[fragment], 1750 - index * 18))
    middle = 194 + output_height // 2
    blocks.extend(
        [
            arrow(1078, middle),
            txt(1058, middle + 80, "compile", 21, MUTED),
        ]
    )
    footer = max(source_bottom, 194 + output_height) + 52
    blocks.extend(
        [
            f'<path d="M32 {footer - 12} H1768" stroke="{BORDER}" stroke-width="2"/>',
            txt(32, footer + 34, "$ pf --entry SKILL.md", 28, LINK),
            txt(
                530,
                footer + 34,
                f"{len(sources)} source files → 1 validated bundle",
                26,
                TEXT,
            ),
        ]
    )
    height = footer + 68
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        '<title id="title">Linked Markdown compiles into one complete context</title>'
        '<desc id="desc">SKILL.md selects Review Mode. Its two Rules links reach '
        "one Tests section. The compiled bundle contains the source content once, "
        "with arrows tracing each link to its heading inside the bundle.</desc>"
        f'<rect width="{width}" height="{height}" fill="{BG}"/>'
        '<g font-family="monospace" xml:space="preserve">'
        + "\n".join(blocks)
        + "</g></svg>\n"
    )


def draw(
    root: Path, sources: list[str], bundles: list[str], diagnostics: str = ""
) -> str:
    """The drawing of one run: the sources it read, and the bundles or refusal."""
    block, tree_height = card(
        SOURCE_X, SOURCE_Y, TREE_WIDTH, "Files", tree_of(sources, ROOT_LABEL)
    )
    left = [block]
    left_at = SOURCE_Y + tree_height
    for path in sources:
        left_at += 22
        block, height = card(
            SOURCE_X, left_at, COLUMN, path, (root / path).read_text(encoding="utf-8")
        )
        left.append(block)
        left_at += height
    right = []
    right_at = SOURCE_Y
    if not bundles:
        title = "Diagnostics" if diagnostics.strip() else "Compiler output"
        body = diagnostics.strip() or "nothing published"
        block, height = card(OUTPUT_X, right_at, PANEL_WIDTH, title, body)
        right.append(block)
        right_at += height + 22
    for name in bundles:
        block, height = card(
            OUTPUT_X,
            right_at,
            PANEL_WIDTH,
            name,
            (root / name).read_text(encoding="utf-8"),
        )
        right.append(block)
        right_at += height + 22
    height = max(left_at, right_at) + 40
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
            [*build, "--entry", case["entry"]], cwd=work, capture_output=True, text=True
        )
        bundles = sorted(
            path.relative_to(work).as_posix() for path in work.rglob("*.bundle.md")
        )
        sources = sorted(
            path.relative_to(work).as_posix()
            for path in work.rglob("*.md")
            if path.relative_to(work).as_posix() not in bundles
        )
        drawn = (
            draw_overview(work, sources, bundles[0])
            if name == "run" and result.returncode == 0 and len(bundles) == 1
            else draw(work, sources, bundles, result.stderr)
        )
        ElementTree.fromstring(drawn)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(drawn)
        expected = case.get("status", 0)
        print(f"{name}: {output}, exit {result.returncode}, {len(bundles)} bundle(s)")
        if result.returncode != expected:
            print(f"{name}: expected exit {expected}", file=sys.stderr)
            return 1
        return 0
    finally:
        shutil.rmtree(work)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "case",
        nargs="*",
        help="case name; every case in examples.json when none is named",
    )
    parser.add_argument(
        "--output", type=Path, help="directory; defaults to docs/images"
    )
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
        failures += (
            render(name, cases[name], options.build.split(), output / f"{name}.svg")
            != 0
        )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
