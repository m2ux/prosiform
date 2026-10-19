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

A fenced block holds examples rather than content, so it is blanked out before
a document is read for references or for tables.
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
