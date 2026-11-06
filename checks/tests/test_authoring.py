"""Audit active authoring guidance for file-only invocation.

The invocation guide is the contract an author copies: the prosiform
declaration, file-relative links, the working-directory bound, short flags,
fragment names and combined destinations. The same guide and the repository
readme recommend hyphens in source paths, because a derived filename writes
each directory separator as an underscore.

Worked commands are copied as written. Each names a file this repository
holds, passes only options the contract declares, and leaves an output
path as an output.
"""

import re
import shlex
from pathlib import Path

from documents import ROOT

GUIDE = ROOT / "invocation.md"
README = ROOT / "README.md"
BUNDLES = ROOT / "docs" / "bundles.md"
SOURCES = ROOT / "docs" / "sources.md"
SURFACES = (GUIDE, README)

# Each authoring statement, beside the document that states it. The guide
# keeps the command line; the architecture pages state the rules it links to.
INSTRUCTIONS = (
    (GUIDE, "pf [OPTIONS] --entry REF [--presets PRESETS]"),
    (SOURCES, "Every key in `prosiform` is a **preset** name"),
    (SOURCES, "the target's own declaration then decides whether it is compiled"),
    (SOURCES, "An entry reference resolves from it, and every path a diagnostic names"),
    (GUIDE, "`-o DIR`"),
    (GUIDE, "a section written as `document#fragment`"),
    (BUNDLES, "A section adds `__` and the fragment."),
    (
        BUNDLES,
        "A selection includes the effective named presets its destination declares.",
    ),
    (BUNDLES, "File and directory names use hyphens rather than underscores."),
)

HYPHENS = "hyphens rather than underscores"
FENCE = re.compile(r"```bash\n(.*?)```", re.DOTALL)
TAKES_VALUE = frozenset({"-o", "-d", "--budget"})
SWITCH = frozenset({"-c", "-C", "-v", "-h"})


def logical_lines(block: str) -> list[str]:
    """One command per line, a trailing backslash joined to the next line."""
    lines: list[str] = []
    pending = ""
    for raw in block.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        line = f"{pending} {stripped}".strip() if pending else stripped
        pending = ""
        if line.endswith("\\"):
            pending = line[:-1].rstrip()
            continue
        lines.append(line)
    if pending:
        lines.append(pending)
    return lines


def commands(path: Path) -> list[tuple[Path, list[str]]]:
    """Each `pf` command in one document, beside the directory it runs in."""
    found: list[tuple[Path, list[str]]] = []
    for block in FENCE.findall(path.read_text(encoding="utf-8")):
        cwd = ROOT
        for line in logical_lines(block):
            if line.startswith("cd "):
                cwd = ROOT / line.removeprefix("cd ").strip()
                continue
            if line == "pf" or line.startswith("pf "):
                found.append((cwd, shlex.split(line)[1:]))
    return found


def source_paths(argv: list[str]) -> list[str]:
    """The single entry destination, with operational option values excluded."""
    found: list[str] = []
    tokens = iter(argv)
    for token in tokens:
        option, equal, value = token.partition("=")
        if option == "--entry":
            assert not found, "one entry per command"
            reference = value if equal else next(tokens)
            found.append(reference.partition("#")[0])
        elif option in TAKES_VALUE or option == "--presets":
            if not equal:
                next(tokens)
        else:
            assert token in SWITCH, token
    return found


def test_the_authoring_statements_are_stated_where_they_are_owned() -> None:
    missing = [
        f"{path.relative_to(ROOT).as_posix()}: {sentence}"
        for path, sentence in INSTRUCTIONS
        if sentence not in path.read_text(encoding="utf-8")
    ]
    assert missing == []


def test_active_guidance_recommends_hyphens_rather_than_underscores() -> None:
    for path in SURFACES:
        assert HYPHENS in path.read_text(encoding="utf-8"), path.relative_to(ROOT)


def test_worked_commands_name_files_this_repository_holds() -> None:
    checked = 0
    for document in SURFACES:
        for cwd, argv in commands(document):
            for name in source_paths(argv):
                assert "_" not in name
                assert (cwd / name).is_file(), f"{document.relative_to(ROOT)}: {name}"
                checked += 1
    assert checked > 0
