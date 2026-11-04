"""Verify the illustration against parsed Markdown and an actual compiler run."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree

from markdown_it import MarkdownIt

from prosiform.source import content

RECORD = Path(__file__).resolve().parent
PROJECT = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location(
    "examples", PROJECT / "scripts" / "render-example.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
cases = json.loads((PROJECT / "scripts" / "examples.json").read_text())
ns = {"s": "http://www.w3.org/2000/svg"}


def normalized(text):
    return " ".join(text.split())


with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    for name, body in cases["run"]["files"].items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
    result = subprocess.run(
        [str(PROJECT / "src" / ".venv" / "bin" / "pf"), "SKILL.md"],
        cwd=root,
        text=True,
        capture_output=True,
        check=True,
    )
    bundles = list(root.rglob("*.bundle.md"))
    assert len(bundles) == 1
    bundle = bundles[0].read_text()
    (RECORD / "compiled.md").write_text(bundle)
    expected_links = ["#review-mode", "#tests", "#tests"]
    parsed_links = [
        child.attrGet("href")
        for token in MarkdownIt().parse(bundle)
        for child in token.children or []
        if child.type == "link_open"
    ]
    assert parsed_links == expected_links, parsed_links
    assert bundle.count("### Tests\n") == 1
    print("PASS: compiler publishes one bundle; all three links name its headings")

    for name, body in {**cases["run"]["files"], "compiled": bundle}.items():
        panel, _, anchors, links = module.overview_panel(0, 0, 608, name, body)
        node = ElementTree.fromstring("<svg>" + panel + "</svg>")
        shown = normalized(" ".join("".join(row.itertext()) for row in node.iter("text")))
        parsed = MarkdownIt().parse(content(body).text)
        for token in parsed:
            if token.type == "inline":
                visible = "".join(
                    child.content
                    for child in token.children or []
                    if child.type in {"text", "code_inline"}
                )
                assert normalized(visible) in shown, (name, visible)
        hrefs = [
            child.attrGet("href")
            for token in parsed
            for child in token.children or []
            if child.type == "link_open"
        ]
        assert [href for href, _, _ in links] == hrefs
        if name == "compiled":
            assert all(href[1:] in anchors for href in hrefs)
    print("PASS: every source and bundle paragraph, heading and link is represented")

    sources = sorted(cases["run"]["files"])
    drawn = module.draw_overview(root, sources, bundles[0].relative_to(root).as_posix())
    actual = (PROJECT / "docs" / "images" / "run.svg").read_text()
    assert drawn == actual
    svg = ElementTree.fromstring(actual)
    assert svg.attrib["aria-labelledby"] == "title desc"
    assert svg.find("s:title", ns).text and svg.find("s:desc", ns).text
    assert svg.find("s:g", ns).attrib["font-family"] == "monospace"
    assert len(svg.findall('.//s:tspan[@fill="#58a6ff"]', ns)) == 6
    panels = svg.findall('.//s:rect[@fill="#161b22"]', ns)
    for text in svg.findall(".//s:text", ns):
        x, y = float(text.attrib["x"]), float(text.attrib["y"])
        assert 0 < y < float(svg.attrib["height"])
        containing = [
            float(panel.attrib["x"]) + float(panel.attrib["width"])
            for panel in panels
            if float(panel.attrib["x"]) <= x
            < float(panel.attrib["x"]) + float(panel.attrib["width"])
            and float(panel.attrib["y"]) <= y
            < float(panel.attrib["y"]) + float(panel.attrib["height"])
        ]
        column_end = min(containing, default=float(svg.attrib["width"]))
        end = x + len("".join(text.itertext())) * float(text.attrib["font-size"]) * 0.6
        assert end <= column_end, (text.text, end, column_end)
    print("PASS: deterministic SVG; accessible description; portable monospace font; text within columns")

    for name in cases:
        if name == "run":
            continue
        path = "docs/images/" + name + ".svg"
        baseline = subprocess.run(
            ["git", "show", "HEAD:" + path], cwd=PROJECT, capture_output=True, check=True
        ).stdout
        assert (PROJECT / path).read_bytes() == baseline, name
    print("PASS: the other eight generated diagrams match the baseline byte for byte")

    for name, source, image_width in [
        ("after.png", PROJECT / "docs/images/run.svg", 1800),
        ("readme-width.png", PROJECT / "docs/images/run.svg", 900),
    ]:
        image_height = round(float(svg.attrib["height"]) * image_width / 1800)
        subprocess.run(
            ["ksvgtopng5", str(image_width), str(image_height), str(source), str(RECORD / name)],
            env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
            check=True,
        )
    print("PASS: full-size and 900-pixel previews rendered at their native aspect ratio")
