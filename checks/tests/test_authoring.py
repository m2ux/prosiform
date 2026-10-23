"""Audit active authoring guidance for file-only invocation.

The invocation guide is the contract an author copies: the prosiform
mapping, file-relative roots, the working-directory default, short flags,
fragment names and combined destinations. The same guide, the repository
readme and the worked examples recommend hyphens in source paths, because
a derived filename writes each directory separator as an underscore.

Worked commands are copied as written. Each names a file this repository
holds, passes no retired root option, and leaves an output path as an
output. Example sources that declare a root declare one relative to the
file.
"""

import re
from pathlib import Path

from documents import ROOT

GUIDE = ROOT / "invocation.md"
README = ROOT / "README.md"
EXAMPLES = ROOT / "example" / "README.md"
SURFACES = (GUIDE, README, EXAMPLES)

INSTRUCTIONS = (
    "pf [OPTIONS] REF [REF ...]",
    "The only keys in `prosiform` are `root`, `group` and `group-depth`",
    "An explicit root resolves from the declaring file's directory.",
    "Every absent root uses the working directory",
    "`-f DOC`",
    "`-o FILE`",
    "A section inserts `__` and the fragment before that suffix.",
    "Distinct selections require an explicit `-o` destination.",
    "File and directory names use hyphens rather than underscores.",
)

HYPHENS = "hyphens rather than underscores"
FENCE = re.compile(r"```bash\n(.*?)```", re.DOTALL)
FRONT = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
ROOT_VALUE = re.compile(r'^  root: "([^"]*)"', re.MULTILINE)
TAKES_VALUE = frozenset(
    {"-o", "-f", "-d", "-x", "-F", "-B", "-I", "-O", "-T", "-L", "-N", "-E"}
)
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
                found.append((cwd, line.split()[1:]))
    return found


def source_paths(argv: list[str]) -> list[str]:
    """Positional entries and `-f` documents, without output destinations."""
    found: list[str] = []
    index = 0
    while index < len(argv):
        token = argv[index]
        assert token != "-r" and not token.startswith("--")
        if token in TAKES_VALUE:
            value = argv[index + 1]
            if token == "-f":
                found.append(value)
            index += 2
            continue
        assert token in SWITCH or not token.startswith("-"), token
        bare = token.strip("'\"")
        if token not in SWITCH and not bare.startswith("#"):
            found.append(bare.split("#", maxsplit=1)[0])
        index += 1
    return found


def test_the_invocation_guide_states_file_owned_authoring() -> None:
    text = GUIDE.read_text(encoding="utf-8")
    missing = [sentence for sentence in INSTRUCTIONS if sentence not in text]
    assert missing == []


def test_active_guidance_recommends_hyphens_rather_than_underscores() -> None:
    for path in SURFACES:
        assert HYPHENS in path.read_text(encoding="utf-8"), path.relative_to(ROOT)


def test_worked_commands_name_files_this_repository_holds() -> None:
    checked = 0
    for document in SURFACES:
        for cwd, argv in commands(document):
            assert "-r" not in argv
            for name in source_paths(argv):
                assert "_" not in name
                assert (cwd / name).is_file(), f"{document.relative_to(ROOT)}: {name}"
                checked += 1
    assert checked > 0


def test_example_paths_use_hyphens_and_declare_file_relative_roots() -> None:
    declared = 0
    for path in sorted((ROOT / "example").rglob("*.md")):
        if path.name == "README.md":
            continue
        relative = path.relative_to(ROOT).as_posix()
        assert "_" not in relative, relative
        block = FRONT.match(path.read_text(encoding="utf-8"))
        assert block is not None, relative
        assert "prosiform:" in block.group(1), relative
        root = ROOT_VALUE.search(block.group(1))
        if root is None:
            continue
        value = root.group(1)
        assert value
        assert not value.startswith("/")
        assert not value.startswith("~")
        assert "\\" not in value
        assert "://" not in value
        declared += 1
    assert declared > 0
