"""Bundle one Markdown entry document and render its source-to-output diagram."""

from __future__ import annotations

import contextlib
import argparse
import hashlib
import html
import json
import re
import shlex
import subprocess
import tempfile
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
    section_level = 0
    for raw in body.splitlines():
        if not raw:
            rows.append(("", 13, 18, 0, False, False, 0))
            continue
        heading = re.match(r"^(#{1,6}) (.*)", raw)
        level = len(heading[1]) if heading else 0
        if heading:
            section_level = level
        indent = level if heading else section_level + 1 if section_level else 0
        value = heading[2] if heading else raw
        value = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", value)
        value = re.sub(r"^- ", "• ", value)
        size = 30 if level == 1 else 26 if level == 2 else 23 if level else 20
        available = max(20, int((width - 62 - indent * 12) / (size * 0.62)))
        for i, part in enumerate(
            textwrap.wrap(
                value, available, break_long_words=False, break_on_hyphens=False
            )
            or [""]
        ):
            rows.append(
                (
                    part,
                    size + 17,
                    size,
                    level,
                    "[" in raw,
                    i == 0 and bool(level),
                    indent,
                )
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
    for value, step, size, level, islink, label, indent in rows:
        at += step
        if value:
            if label:
                result.append(txt(x + 12, at, "H" + str(level), 11, MUTED))
            color = AMBER if "¬" in value else LINK if islink else TEXT
            result.append(
                txt(x + 38 + indent * 12, at, value, size, color, 500 if level else 400)
            )
    return "\n".join(result), height


def compact_markdown(body):
    """Keep parsed headings and links; omit other content."""
    from markdown_it import MarkdownIt

    from prosiform.source import Unterminated, content

    try:
        body = content(body).text
    except Unterminated:
        return ""
    tokens = MarkdownIt("commonmark").parse(body)
    rows = []

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
    return "\n\n".join(rows)


def limit_section_content(body, section_level):
    """Show content through the selected level and titles one level deeper."""
    if section_level is None:
        return body
    from markdown_it import MarkdownIt

    from prosiform.source import Unterminated, content

    try:
        source = content(body)
    except Unterminated:
        return body
    tokens = MarkdownIt("commonmark").parse(source.text)
    original = body.splitlines(keepends=True)
    removed = set()
    offset = source.first_line - 1
    headings = [token for token in tokens if token.type == "heading_open" and token.map]
    for index, token in enumerate(headings):
        level = int(token.tag[1:])
        if level <= section_level:
            continue
        start = token.map[1] if level == section_level + 1 else token.map[0]
        end = len(original) - offset
        for following in headings[index + 1 :]:
            if int(following.tag[1:]) <= section_level + 1:
                end = following.map[0]
                break
        removed.update(range(start + offset, end + offset))
    return "".join(line for index, line in enumerate(original) if index not in removed)


def svg(
    inputs,
    root_name,
    bundle,
    branch_name,
    revision,
    compact=False,
    input_section_level=None,
    compiled_section_level=None,
):
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
        content = limit_section_content(content, input_section_level)
        block, h = card(466, at, 690, path, content)
        blocks.append(block)
        at += h + 22
    bundle_body = bundle
    if compact:
        bundle_body = compact_markdown(bundle_body)
    expected = (
        limit_section_content(bundle_body, compiled_section_level)
        if bundle
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
        "--cwd",
        type=Path,
        help="Invocation working directory; defaults to the document directory",
    )
    parser.add_argument("--section", help="Select a fragment of the entry document")
    for panel in ("input", "compiled"):
        parser.add_argument(
            f"--{panel}-section-level",
            type=int,
            choices=range(1, 7),
            metavar="N",
            help=f"Show {panel} content through HN and titles through H(N+1)",
        )
    parser.add_argument(
        "--max-output-bytes",
        type=int,
        help="Compiler output-size budget; defaults to the compiler's limit",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Show headings and links; omit other content in both panels",
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
    root = (options.cwd or document.parent).absolute()
    try:
        entry = document.relative_to(root).as_posix()
    except ValueError:
        parser.error("The entry document must be under --cwd")
    if options.section:
        entry += "#" + options.section
    arguments = []
    if options.max_output_bytes is not None:
        arguments.extend(["-O", str(options.max_output_bytes)])
    arguments.append(entry)
    captured = {}
    read_source = cli.read_source

    def record(source_root, path, **kwargs):
        data = read_source(source_root, path, **kwargs)
        captured[path] = data
        return data

    stdout, stderr = io.StringIO(), io.StringIO()
    with (
        tempfile.TemporaryDirectory() as folder,
        contextlib.chdir(root),
        patch.object(cli, "read_source", side_effect=record),
    ):
        status = cli.main(["-o", folder, *arguments], stdout=stdout, stderr=stderr)
        written = sorted(Path(folder).iterdir())
        body = written[0].read_bytes().decode() if written else ""
    diagnostics = stderr.getvalue()
    inputs = {
        path: data.decode("utf-8", errors="replace")
        for path, data in sorted(captured.items())
    }
    rendered = svg(
        inputs,
        root.name,
        body,
        branch_name,
        revision,
        compact=options.compact,
        input_section_level=options.input_section_level,
        compiled_section_level=options.compiled_section_level,
    )
    ET.fromstring(rendered)
    output = options.output.absolute()
    destinations = {
        suffix: Path(str(output) + suffix)
        for suffix in [
            ".svg",
            ".bundle.md",
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
    command = shlex.join(["pf", "-o", "<folder>", *arguments])
    fence = chr(96) * 3
    review = [
        "# " + document.name,
        "",
        "Compiler: " + branch_name + " " + revision,
        "",
        "Source files opened by the compiler appear beside the bundle body. "
        "Opened files can include deferred targets; "
        "their presence does not imply their content is bundled. Images simplify "
        "Markdown presentation; the bundle file preserves exact content and "
        "link destinations."
        + (
            " Compact view omits body content while retaining headings and links."
            if options.compact
            else ""
        )
        + "".join(
            f" {panel} content is shown through H{level}; "
            f"H{level + 1} sections show titles only."
            for panel, level in (
                ("Input", options.input_section_level),
                ("Compiled", options.compiled_section_level),
            )
            if level is not None
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
    review.extend(["", "### Diagnostics", "", "Exit status: " + str(status)])
    if diagnostics:
        review.extend(["", fence + "text", diagnostics.rstrip(), fence])
    record_data = dict(
        compiler_branch=branch_name,
        compiler_revision=revision,
        compact=options.compact,
        input_section_level=options.input_section_level,
        compiled_section_level=options.compiled_section_level,
        command=command,
        exit_code=status,
        sources={
            path: hashlib.sha256(data).hexdigest() for path, data in captured.items()
        },
        bundle_sha256=hashlib.sha256(body.encode()).hexdigest(),
        stderr_sha256=hashlib.sha256(diagnostics.encode()).hexdigest(),
    )
    artifacts = {
        ".svg": rendered,
        ".bundle.md": body,
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
