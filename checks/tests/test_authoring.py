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
import shutil
import tomllib
from io import StringIO
from pathlib import Path

import pytest
from documents import ROOT

from prosiform.cli import main as compile_main
from prosiform.cli import parser as command_parser

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


@pytest.mark.parametrize("document", SURFACES, ids=lambda path: path.name)
def test_worked_commands_compile_from_their_documented_directory(
    document: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Copy the documented source tree so publishing never edits the corpus."""
    for index, (cwd, argv) in enumerate(commands(document)):
        if not source_paths(argv):
            continue
        copied = tmp_path / str(index)
        shutil.copytree(cwd, copied)
        monkeypatch.chdir(copied)
        stdout, stderr = StringIO(), StringIO()
        assert compile_main(argv, stdout, stderr) == 0, stderr.getvalue()
        assert stdout.getvalue() == ""
        if "-c" not in argv:
            assert list(copied.glob("*.bundles/*.bundle.md"))


@pytest.mark.parametrize(
    "block",
    re.findall(
        r"```toml\n(.*?)```", (ROOT / "fixtures/README.md").read_text(), re.DOTALL
    ),
)
def test_documented_manifest_invocations_use_the_compiler_grammar(block: str) -> None:
    """The fixture-authoring templates must reach compilation, not usage refusal."""
    invocation = tomllib.loads(block).get("invocation")
    if invocation is None:
        return
    arguments = invocation["arguments"]
    parsed = command_parser().parse_args(arguments)
    if not parsed.version:
        assert parsed.entry == "guide.md"


@pytest.mark.parametrize(
    "name",
    [
        "docs/dispatch.md",
        "docs/glossary.md",
        "docs/composition.md",
        "evals/diagram-following/README.md",
    ],
)
def test_dispatch_guidance_names_the_published_heading(name: str) -> None:
    from prosiform.dispatch import PARALLEL

    text = (ROOT / name).read_text()
    assert PARALLEL in text
    assert "<section title> dispatch set" not in text
    assert "<title> dispatch set" not in text
    assert "Give each of these to its own sub-agent" not in text
    assert "under one instruction" not in text


def test_architecture_module_inventory_matches_the_package() -> None:
    text = (ROOT / "docs/architecture.md").read_text()
    documented = set(re.findall(r"^\| `([a-z]+)` \|", text, re.MULTILINE))
    implemented = {
        path.stem
        for path in (ROOT / "src/prosiform").glob("*.py")
        if path.stem != "__init__"
    }
    assert documented == implemented


def test_focused_deferred_command_uses_the_current_grammar() -> None:
    text = (ROOT / "docs/composition.md").read_text()
    [command] = re.findall(r"`(pf [^`]*fetch.md#implementation)`", text)
    parsed = command_parser().parse_args(shlex.split(command)[1:])
    assert parsed.entry == "fetch.md#implementation"


def test_budget_reproduction_supplies_one_explicit_entry() -> None:
    text = (ROOT / "docs/output-budget.md").read_text()
    lines = [line for line in text.splitlines() if line.startswith("<build> ")]
    assert len(lines) == 2
    for line in lines:
        parsed = command_parser().parse_args(shlex.split(line)[1:])
        assert parsed.entry == "work-planner/modes/plan-mode.md"
