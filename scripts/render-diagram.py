"""Bundle one Markdown entry document and render its source-to-output diagram."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shlex
import subprocess
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

FONT = "IBM Plex Mono"
BG, CARD, BORDER = "#0d1117", "#161b22", "#303b49"
TEXT, MUTED, LINK, AMBER = "#e6edf3", "#b1c6df", "#58a6ff", "#e3b341"


def txt(x, y, value, size=20, color=TEXT, weight=400):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
        f'font-weight="{weight}">{html.escape(value)}</text>'
    )


def lines(body, width):
    """Render Markdown headings, paragraphs, lists and link labels without clipping."""
    rows = []
    for raw in body.splitlines():
        if not raw:
            rows.append(("", 13, 18, 0, False, False))
            continue
        heading = re.match(r"^(#{1,6}) (.*)", raw)
        level = len(heading[1]) if heading else 0
        value = heading[2] if heading else raw
        value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
        value = re.sub(r"^- ", "• ", value)
        size = 30 if level == 1 else 26 if level == 2 else 23 if level else 20
        available = max(20, int((width - 50 - level * 14) / (size * 0.62)))
        for i, part in enumerate(
            textwrap.wrap(
                value, available, break_long_words=False, break_on_hyphens=False
            )
            or [""]
        ):
            rows.append(
                (part, size + 17, size, level, "[" in raw, i == 0 and bool(level))
            )
    return rows


def card(x, y, width, title, body, output=False):
    rows = lines(body, width)
    height = 72 + sum(r[1] for r in rows) + 20
    result = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="12" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>',
        txt(x + 24, y + 36, title, 21, MUTED),
    ]
    result.append(f'<path d="M{x} {y + 54} H{x + width}" stroke="{BORDER}"/>')
    at = y + 74
    for value, step, size, level, islink, label in rows:
        at += step
        if value:
            if label:
                result.append(txt(x + 12, at, "H" + str(level), 11, MUTED))
            color = AMBER if "¬" in value else LINK if islink else TEXT
            result.append(
                txt(x + 38 + level * 12, at, value, size, color, 500 if level else 400)
            )
    return "\n".join(result), height


def split_entry_points(stdout):
    paragraph, separator, body = stdout.partition("\n\n")
    if paragraph.startswith("This bundle was built for ") and paragraph.endswith(
        "everything else is material it references."
    ):
        return paragraph, body if separator else ""
    return "", stdout


def compact_markdown(body):
    """Keep parsed headings and links; collapse other content to a placeholder."""
    from markdown_it import MarkdownIt

    from prosiform.source import Unterminated, content

    try:
        body = content(body).text
    except Unterminated:
        return "…"
    tokens = MarkdownIt("commonmark").parse(body)
    rows = []

    def omit():
        if not rows or rows[-1] != "…":
            rows.append("…")

    for index, token in enumerate(tokens):
        if token.type == "inline":
            previous = tokens[index - 1] if index else None
            if previous is not None and previous.type == "heading_open":
                rows.append("#" * int(previous.tag[1:]) + " " + token.content)
                continue
            children = iter(token.children or [])
            for child in children:
                if child.type == "link_open":
                    label = []
                    for part in children:
                        if part.type == "link_close":
                            break
                        label.append(
                            " "
                            if part.type in ("softbreak", "hardbreak")
                            else part.content
                        )
                    rows.append(
                        "[" + "".join(label) + "](" + str(child.attrGet("href")) + ")"
                    )
                elif child.type == "image":
                    rows.append(
                        "![" + child.content + "](" + str(child.attrGet("src")) + ")"
                    )
                elif child.content.strip(" \t\r\n.,;:!?()[]-"):
                    omit()
        elif token.type in ("fence", "code_block", "html_block", "hr"):
            omit()
    return "\n\n".join(rows)


def svg(inputs, root_name, stdout, branch_name, revision, compact=False):
    blocks = []
    header = [txt(32, 48, branch_name + " " + revision[:12], 20, AMBER)]
    top = 80
    # The file tree includes the inputs listed for this case.
    nodes = {}
    for path in sorted(inputs):
        node = nodes
        for part in path.split("/"):
            node = node.setdefault(part, {})
    tree_rows = [root_name + "/"]

    def branch(node, prefix=""):
        for i, (name, children) in enumerate(node.items()):
            last = i == len(node) - 1
            tree_rows.append(
                prefix + ("└─ " if last else "├─ ") + name + ("/" if children else "")
            )
            branch(children, prefix + ("   " if last else "│  "))

    branch(nodes)
    tree = "\n".join(tree_rows)
    treeblock, treeheight = card(32, top, 410, "Participating files", tree)
    blocks.append(treeblock)
    at = top
    for path, content in inputs.items():
        if compact:
            content = compact_markdown(content)
        block, h = card(466, at, 690, path, content)
        blocks.append(block)
        at += h + 22
    _, bundle_body = split_entry_points(stdout)
    expected = (
        (compact_markdown(bundle_body) if compact else bundle_body)
        if stdout
        else "No bundle published."
    )
    outblock, outh = card(1230, top, 880, "Compiler output", expected, True)
    blocks.append(outblock)
    middle = top + 100
    blocks.append(
        f'<path d="M1172 {middle} H1190 V{middle - 12} L1218 {middle + 16} '
        f'L1190 {middle + 44} V{middle + 32} H1172Z" fill="{LINK}"/>'
    )
    height = max(at, top + outh, top + treeheight) + 65
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="2142" height="{height}" '
        f'viewBox="0 0 2142 {height}" role="img" aria-labelledby="title desc">'
        '<title id="title">Source documents and compiled bundle</title>'
        '<desc id="desc">Source documents and actual compiler output.</desc>'
        f'<rect width="2142" height="{height}" fill="{BG}"/>'
        f'<g font-family="{FONT}" xml:space="preserve">'
        + "".join(header + blocks)
        + "</g></svg>\n"
    )


def main():
    import io
    from unittest.mock import patch

    from prosiform import cli

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "document", type=Path, help="Markdown entry document, such as SKILL.md"
    )
    parser.add_argument(
        "--root",
        type=Path,
        help="Allowed source root; defaults to the document directory",
    )
    parser.add_argument(
        "--group",
        action="append",
        default=[],
        metavar="SLUG:DEPTH",
        help="Grouping rule; repeat for distinct slugs",
    )
    parser.add_argument("--section", help="Select a fragment of the entry document")
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Show headings and links; replace other content with … in both panels",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output prefix, such as /tmp/skill-diagram",
    )
    parser.add_argument(
        "--branch", help="Compiler branch; required for a detached compiler checkout"
    )
    parser.add_argument("--revision", help="Require this full compiler commit SHA")
    options = parser.parse_args()
    checkout = Path(cli.__file__).resolve().parents[2]

    def git(*arguments):
        return subprocess.check_output(
            ["git", "-C", str(checkout), *arguments], text=True
        ).strip()

    revision = git("rev-parse", "HEAD")
    if options.revision and revision != options.revision:
        parser.error("Compiler revision does not match --revision")
    if git("status", "--porcelain", "--untracked-files=no"):
        parser.error("Compiler checkout must have clean tracked files")
    branch_name = options.branch or git("branch", "--show-current")
    if not branch_name:
        parser.error("Detached compiler checkout: supply --branch")
    if git("rev-parse", "refs/heads/" + branch_name) != revision:
        parser.error("Compiler branch must point to the checked-out commit")
    document = options.document.absolute()
    root = (options.root or document.parent).absolute()
    try:
        entry = document.relative_to(root).as_posix()
    except ValueError:
        parser.error("The entry document must be under --root")
    if options.section:
        entry += "#" + options.section
    arguments = ["--root", str(root)]
    for group in options.group:
        arguments.extend(["--group", group])
    arguments.append(entry)
    captured = {}
    read_source = cli.read_source

    def record(source_root, path):
        data = read_source(source_root, path)
        captured[path] = data
        return data

    stdout, stderr = io.StringIO(), io.StringIO()
    with patch.object(cli, "read_source", side_effect=record):
        status = cli.main(arguments, stdout=stdout, stderr=stderr)
    body, diagnostics = stdout.getvalue(), stderr.getvalue()
    inputs = {
        path: data.decode("utf-8", errors="replace")
        for path, data in sorted(captured.items())
    }
    rendered = svg(
        inputs, root.name, body, branch_name, revision, compact=options.compact
    )
    ET.fromstring(rendered)
    output = options.output.absolute()
    destinations = {
        suffix: Path(str(output) + suffix)
        for suffix in [
            ".svg",
            ".stdout.md",
            ".stderr.txt",
            ".command.txt",
            ".review.md",
            ".run.json",
        ]
    }
    source_paths = {(root / path).resolve() for path in captured}
    source_paths.add(document.resolve())
    if any(path.resolve() in source_paths for path in destinations.values()):
        parser.error("Output files must not overwrite source documents")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = shlex.join(["prosiform", *arguments])
    fence = chr(96) * 3
    review = [
        "# " + document.name,
        "",
        "Compiler: " + branch_name + " " + revision,
        "",
        "Source files opened by the compiler appear beside the bundle body. "
        "The opening compiler paragraph appears under Entry Points, with links "
        "into the exact stdout file. Opened files can include deferred targets; "
        "their presence does not imply their content is bundled. Images simplify "
        "Markdown presentation; the stdout file preserves exact content and "
        "link destinations."
        + (
            " Compact view replaces body content with … "
            "while retaining headings and links."
            if options.compact
            else ""
        ),
        "",
        "![Source documents and compiled bundle](" + destinations[".svg"].name + ")",
        "",
        "### Command",
        "",
        fence + "bash",
        command,
        fence,
    ]
    entry_points, _ = split_entry_points(body)
    if entry_points:
        review.extend(
            [
                "",
                "### Entry Points",
                "",
                entry_points.replace(
                    "](#", "](" + destinations[".stdout.md"].name + "#"
                ),
            ]
        )
    review.extend(["", "### Diagnostics", "", "Exit status: " + str(status)])
    if diagnostics:
        review.extend(["", fence + "text", diagnostics.rstrip(), fence])
    record_data = dict(
        compiler_branch=branch_name,
        compiler_revision=revision,
        compact=options.compact,
        command=command,
        exit_code=status,
        sources={
            path: hashlib.sha256(data).hexdigest() for path, data in captured.items()
        },
        stdout_sha256=hashlib.sha256(body.encode()).hexdigest(),
        stderr_sha256=hashlib.sha256(diagnostics.encode()).hexdigest(),
    )
    artifacts = {
        ".svg": rendered,
        ".stdout.md": body,
        ".stderr.txt": diagnostics,
        ".command.txt": command + "\n",
        ".review.md": "\n".join(review) + "\n",
        ".run.json": json.dumps(record_data, indent=2) + "\n",
    }
    for suffix, content in artifacts.items():
        destinations[suffix].write_text(content)
    print("Rendered " + str(destinations[".svg"]))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
