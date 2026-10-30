"""Render a bundle's Mermaid fences and report each sequence participant's menu.

Usage: python3 render-menus.py <mmdc> <bundle.md> <work-dir>

Runs mermaid-cli's mmdc over the bundle, which renders each mermaid fence
to an SVG in headless Chromium, then reads every sequence participant's
popup menu from those SVGs: each entry's label and the href it opens.

Exits 0 when every menu entry's href is '#<slug>' for a slug one of the
bundle's headings generates, and 1 otherwise or when no menu renders.
"""

import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ElementTree

SVG = "{http://www.w3.org/2000/svg}"
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
HEADING = re.compile(r"^#{1,6} +(.*?) *#* *$", re.MULTILINE)
DISCARDED = re.compile(r"[^\w\- ]")
PUPPETEER = '{"args": ["--no-sandbox"]}\n'


def slug(text: str) -> str:
    return DISCARDED.sub("", text.strip().lower()).replace(" ", "-")


def main(mmdc: str, bundle: str, work: str) -> int:
    out = pathlib.Path(work)
    out.mkdir(parents=True, exist_ok=True)
    config = out / "puppeteer.json"
    config.write_text(PUPPETEER)
    rendered = out / "rendered.md"
    subprocess.run(
        [mmdc, "-p", str(config), "-i", bundle, "-o", str(rendered)], check=True
    )
    text = pathlib.Path(bundle).read_text()
    slugs = {slug(one) for one in HEADING.findall(text)}
    ok = True
    menus = 0
    for svg in sorted(out.glob("rendered-*.svg")):
        root = ElementTree.parse(svg).getroot()
        names = {
            node.get("id", "").removeprefix("root-"): node.get("data-id", "")
            for node in root.iter(f"{SVG}g")
            if node.get("data-type") == "participant"
        }
        for group in root.iter(f"{SVG}g"):
            if group.get("class") != "actorPopupMenu":
                continue
            menus += 1
            index = group.get("id", "").removeprefix("actor").split("_")[0]
            name = names.get(index, f"actor{index}")
            print(f"{svg.name} {name}:")
            entries = list(group.iter(f"{SVG}text"))
            anchors = list(group.iter(f"{SVG}a"))
            if len(anchors) != len(entries) or not anchors:
                ok = False
                print(f"  {len(entries)} entry(ies), {len(anchors)} opening a link")
            for anchor in anchors:
                href = anchor.get(XLINK_HREF, "")
                label = "".join(anchor.itertext()).strip()
                follows = href.startswith("#") and href[1:] in slugs
                ok = ok and follows
                print(f"  {label!r} -> {href!r} {'heading' if follows else 'NO HEADING'}")
    if menus == 0:
        print("no participant menu rendered")
        return 1
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
