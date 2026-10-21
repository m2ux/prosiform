"""The documents the repository's checks read, and the reading they share.

A document counts when git tracks it, which is the rule `layout.py` applies to
a tree: an untracked file is invisible to a fresh checkout. The documents are
found rather than listed, so a tree added later is read by every check that
reads them, without any of those checks being edited.

The fixture corpus is excepted. A fixture is a directory holding a manifest,
which is what the corpus check calls one, and a fixture's source deliberately
carries references a run is meant to refuse, while its expected bundle is
output rather than a document a reader follows. The corpus is discovered the
same way the documents are, so a fixture added anywhere is excepted and a
document added anywhere else is read.

Literal content holds examples rather than content, so it is blanked out
before a document is read. A fenced block goes before a document is read for
references or for tables; a reference scan blanks indented blocks and code
spans beside it, because a link form written in either is the spelling of a
link rather than a link, which is the rule the product applies to the same
bytes. A heading's slug and a table's cell reduce a code span to its code
instead, since that is what the rendering leaves behind.
"""

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

README = "README.md"
MANIFEST = "manifest.toml"
MARKDOWN = (".md", ".markdown")
FENCE = re.compile(r"^(?:```|~~~)", re.MULTILINE)
INDENTED = re.compile(r"^(?: {4}|\t)")
LIST_ITEM = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:\s|$)")
BACKTICK_RUN = re.compile(r"`+")
CELL_SEPARATOR = re.compile(r"(?<!\\)\|")
DELIMITER_CELL = re.compile(r"^:?-{3,}:?$")


def tracked() -> list[str]:
    """Every path git tracks, each relative to the repository root."""
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def corpus(paths: list[str]) -> list[str]:
    """Each fixture directory among those paths, named by the manifest it holds."""
    return [
        Path(path).parent.as_posix() for path in paths if Path(path).name == MANIFEST
    ]


def documents() -> list[Path]:
    """Every Markdown document git tracks outside the corpus, in path order."""
    paths = tracked()
    fixtures = corpus(paths)
    return sorted(
        ROOT / path
        for path in paths
        if Path(path).suffix in MARKDOWN
        and not any(path.startswith(f"{fixture}/") for fixture in fixtures)
    )


def readmes() -> list[Path]:
    """Every README among those documents, which is where the project's tables sit."""
    return [path for path in documents() if path.name == README]


def strip_code_fences(text: str) -> str:
    """Blank out fenced blocks, whose contents are examples rather than content."""
    out, fenced = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return "\n".join(out)


def strip_indented_blocks(text: str) -> str:
    """Blank out indented blocks, whose contents are examples rather than content.

    A block opens at a four-space or tab indent on a line following a blank
    one, and closes at the first line indented less than that. A line below a
    list marker is that list's own content however far it is indented, so a
    nested bullet carrying a link is read as the link it is.
    """
    out: list[str] = []
    indented_block = False
    listed = False
    after_blank = True
    for line in text.splitlines():
        if not line.strip():
            out.append("")
            after_blank = True
            continue
        indented = bool(INDENTED.match(line))
        if indented_block and not indented:
            indented_block = False
        if not indented_block:
            if LIST_ITEM.match(line):
                listed = True
            elif not indented:
                listed = False
            indented_block = indented and after_blank and not listed
        out.append("" if indented_block else line)
        after_blank = False
    return "\n".join(out)


def strip_code_spans(text: str) -> str:
    """Blank out code spans, whose contents are code rather than content.

    A span opens at a backtick run and closes at the next run of the same
    length, which is the rule the product's own scan applies. An opener that
    never closes is the literal backticks it is written as, and the scan
    carries on past it. Each blanked character becomes a space and every
    newline survives, so a line-anchored pattern reads the lines the document
    has.
    """
    out = list(text)
    runs = [run.span() for run in BACKTICK_RUN.finditer(text)]
    index = 0
    while index < len(runs):
        opening, after = runs[index]
        width = after - opening
        for later, (closing, closed) in enumerate(runs[index + 1 :], index + 1):
            if closed - closing != width:
                continue
            for at in range(opening, closed):
                if out[at] != "\n":
                    out[at] = " "
            index = later + 1
            break
        else:
            index += 1
    return "".join(out)


def strip_literal(text: str) -> str:
    """Blank out every literal form: a fenced block, an indented block, a code span.

    What survives is what a renderer turns into content, so a link form
    written to show the syntax is passed over and a link beside it is read.
    """
    return strip_code_spans(strip_indented_blocks(strip_code_fences(text)))


MARKDOWN_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def plain(cell: str) -> str:
    """A cell reduced to its text: a link to its label, a code span to its code.

    Runs of whitespace collapse to single spaces, so a cell wrapped
    across a table's source lines compares as the one line it states.
    """
    return " ".join(MARKDOWN_LINK.sub(r"\1", cell).replace("`", "").split())


def cells(line: str) -> list[str]:
    """The cells of one pipe-table row, without their surrounding pipes."""
    return [part.strip() for part in CELL_SEPARATOR.split(line.strip())[1:-1]]


@dataclass(frozen=True)
class Table:
    """One pipe table: its header cells and its body rows."""

    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

    def records(self) -> list[dict[str, str]]:
        """Each body row as its header cell to its value."""
        return [dict(zip(self.headers, row, strict=False)) for row in self.rows]


def is_delimiter(line: str) -> bool:
    row = cells(line)
    return bool(row) and all(DELIMITER_CELL.match(cell) for cell in row)


def tables(text: str) -> list[Table]:
    """Every pipe table the document carries, outside its fenced blocks.

    A table is a header row, a delimiter row, and the rows that follow until
    the first line that does not open with a pipe.
    """
    lines = strip_code_fences(text).splitlines()
    found: list[Table] = []
    index = 0
    while index + 1 < len(lines):
        if not lines[index].strip().startswith("|") or not is_delimiter(
            lines[index + 1]
        ):
            index += 1
            continue
        headers = tuple(cells(lines[index]))
        index += 2
        rows: list[tuple[str, ...]] = []
        while index < len(lines) and lines[index].strip().startswith("|"):
            rows.append(tuple(cells(lines[index])))
            index += 1
        found.append(Table(headers, tuple(rows)))
    return found


def rows(text: str, header: str) -> list[dict[str, str]]:
    """Every row of the tables a header cell marks as enumerating one surface.

    A table is located by what its header names rather than by the document
    or the section it sits in, so an enumeration moves within a document
    without the check reading it being edited.
    """
    return [
        record
        for table in tables(text)
        if header in table.headers
        for record in table.records()
    ]
