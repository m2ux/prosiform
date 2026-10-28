#!/usr/bin/env python3
"""Assert each diagram link form the corpus bundles renders as a followable link.

A diagram link is followed when a reader clicks it in the rendered diagram,
so a bundle proves its rewritten destinations only once Mermaid has drawn
them. This check renders the expected bundle of each fixture `RENDERED`
names, the one its manifest declares, with mermaid-cli, which draws every
`mermaid` fence to an SVG in a headless browser, and reads every anchor
the drawings carry. The corpus holds the build to that same bundle byte
for byte, so the bundle rendered is the one the build publishes.

A Gantt diagram's link is no anchor: Mermaid binds it as a click handler
that calls `window.open` once the page runs. Each fixture `CLICKED` names
is proven in a running page instead: `click.mjs` renders each `mermaid`
fence of its expected bundle with the Mermaid and the browser mermaid-cli
ships, binds the handlers, clicks each clickable task and records the URL
each click opens.

A fixture passes when its drawings carry, or its clicks open, exactly the
destinations its entry lists, one per link its bundle rewrote, and each
opens `#<slug>` for a heading the bundle carries. A destination missing is
a link Mermaid did not render as one; an extra one is a link the bundle
did not rewrite; a click opening anything but one URL is a handler Mermaid
did not bind as one link.

`MERMAID_CLI` holds the mermaid-cli command line, split as a shell splits
one. Its last word names `mmdc`, and the words before it are what runs a
command where `mmdc` is reachable, so the click program runs under them as
`node`. mermaid-cli and the browser it drives are no dependency of the
build, so `make check` leaves this check out, and with nothing configured
the run fails rather than passing over the fixtures.
"""

import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import tomllib
import xml.etree.ElementTree as ElementTree
from pathlib import Path

import links

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"
CONFIGURATION = "MERMAID_CLI"
PUPPETEER = '{"args": ["--no-sandbox"]}\n'
SVG = "{http://www.w3.org/2000/svg}"
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
HREF = "href"
MANIFEST = "manifest.toml"
CLICK_PROGRAM = Path(__file__).resolve().parent / "click.mjs"
NODE = "node"
MERMAID_FENCE = re.compile(r"^```mermaid[^\n]*\n(.*?)^```", re.MULTILINE | re.DOTALL)

RENDERED: dict[str, list[str]] = {
    "rewriting/a-flowchart-click-in-each-form": ["#plan", "#build", "#test", "#ship"],
    "rewriting/a-diagram-click-destination": ["#open"],
    "rewriting/a-diagram-short-click-destination": ["#open", "#closing"],
    "rewriting/a-swimlanes-diagram-click-in-each-form": [
        "#draft",
        "#review",
        "#approve",
        "#merge",
    ],
    "rewriting/a-state-diagram-click-in-each-form": ["#pending", "#done"],
    "rewriting/a-diagram-link-keyword-in-any-case": ["#open", "#closed"],
    "rewriting/a-class-diagram-click-in-each-form": ["#order", "#line", "#price"],
    "rewriting/a-class-diagram-link-destination": ["#ticket", "#review"],
    "rewriting/a-sequence-diagram-link-destination": ["#client"],
    "rewriting/a-sequence-diagram-links-line-destinations": ["#server", "#operations"],
    "rewriting/a-sequence-diagram-link-and-links-line-anchors": [
        "#client",
        "#server",
        "#operations",
    ],
    "rewriting/a-sequence-diagram-menu-keywords-in-any-case": ["#client", "#server"],
    "rewriting/a-sequence-diagram-destination-naming-a-section": ["#setup", "#limits"],
    "rewriting/a-sequence-diagram-links-line-repeating-a-key": ["#server"],
}

CLICKED: dict[str, list[str]] = {
    "rewriting/a-gantt-diagram-click-destination": ["#freeze", "#publish"],
}


def expected_bundle(fixture: Path) -> Path:
    """The one bundle a fixture's manifest declares its run writes."""
    with (fixture / MANIFEST).open("rb") as handle:
        (declared,) = tomllib.load(handle)["expected"]["bundles"]
    return fixture / str(declared)


def anchors(svg: Path) -> list[str]:
    """The href of each anchor one rendered diagram carries, in document order."""
    root = ElementTree.parse(svg).getroot()
    return [
        anchor.get(XLINK_HREF, anchor.get(HREF, "")) for anchor in root.iter(f"{SVG}a")
    ]


def rendered(command: list[str], bundle: Path, work: Path) -> list[str]:
    """Every anchor the bundle's diagrams carry once mermaid-cli has drawn them."""
    configuration = work / "puppeteer.json"
    configuration.write_text(PUPPETEER)
    subprocess.run(
        [*command, "-q", "-p", str(configuration), "-i", str(bundle)]
        + ["-o", str(work / "rendered.md")],
        check=True,
    )
    drawn = sorted(work.glob("rendered-*.svg"))
    return [href for svg in drawn for href in anchors(svg)]


def clicked(command: list[str], bundle: str) -> tuple[list[str], list[str]]:
    """The URL each click on a clickable task of the bundle's diagrams opens.

    A click opening anything but one URL is a defect of its own, returned
    beside the URLs the clicks that opened one did.
    """
    definitions = [fence.group(1) for fence in MERMAID_FENCE.finditer(bundle)]
    result = subprocess.run(
        [*command[:-1], NODE, str(CLICK_PROGRAM), command[-1]],
        input=json.dumps(definitions),
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    clicks = [click for diagram in json.loads(result.stdout) for click in diagram]
    found = [click[0] for click in clicks if len(click) == 1]
    defects = [
        f"a click opens {click!r}, where one link opens one URL"
        for click in clicks
        if len(click) != 1
    ]
    return found, defects


def held(expected: list[str], found: list[str], bundle: str) -> list[str]:
    """What one fixture's drawings or clicks fail to hold, as one line per defect."""
    headings = links.fragments_of(bundle)
    defects = [
        f"{href!r} opens no heading the bundle carries"
        for href in found
        if not href.startswith("#") or href[1:] not in headings
    ]
    if sorted(found) != sorted(expected):
        defects.append(f"renders {found!r}, where its links take {expected!r}")
    return defects


def main() -> int:
    configured = os.environ.get(CONFIGURATION, "").strip()
    if not configured:
        print(f"render check: {CONFIGURATION} names no mermaid-cli command line")
        return 1
    command = shlex.split(configured)
    failed = 0
    for name, expected in [*RENDERED.items(), *CLICKED.items()]:
        bundle = expected_bundle(FIXTURES / name)
        text = bundle.read_text()
        if name in CLICKED:
            found, defects = clicked(command, text)
        else:
            with tempfile.TemporaryDirectory() as work:
                found = rendered(command, bundle, Path(work))
            defects = []
        defects += held(expected, found, text)
        print(f"{name}: {'pass' if not defects else 'fail'} {found}")
        for defect in defects:
            print(f"  {defect}")
        failed += bool(defects)
    total = len(RENDERED) + len(CLICKED)
    print(f"render check: {total} fixture(s), {total - failed} pass, {failed} fail")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
