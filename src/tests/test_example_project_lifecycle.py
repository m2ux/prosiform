"""Compile the project-lifecycle example and hold what it writes.

Each case runs the build over `example/project-lifecycle/` where it stands
and compares the folder the run writes with the one committed under the
example's `expected/` folder, byte for byte, so the example and the bundles
it documents cannot drift apart. A case's expected folder is the output of
`pf -o expected/<case> <arguments>`, run from the example's folder.

The SDLCs are read from the port's presets, so an adapter added to the port
is compiled under every hook and needs an expected folder for each.

The remaining cases hold the claims the example's README makes: the hook
links the skill's bundle publishes are the port's hooks, an adapter missing
a hook section fails the hook's build, and an adapter is added without
changing the skill's bundle.
"""

import json
import re
import shutil
from contextlib import chdir
from io import StringIO
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from prosiform.cli import main

EXAMPLE = Path(__file__).resolve().parents[2] / "example" / "project-lifecycle"
"""The example under test, read where it stands."""

EXPECTED = EXAMPLE / "expected"
"""One folder per case, holding what that case's run writes."""

PORT = "sdlc/port.md"

HOOKS = ("on-plan", "on-deliver", "on-verify")


def presets(document: Path) -> list[str]:
    """The named presets a document's frontmatter declares, `default` aside."""
    frontmatter = document.read_text().split("---\n")[1]
    declared = YAML(typ="safe").load(frontmatter)["prosiform"]
    return [name for name in declared if name != "default"]


SDLCS = presets(EXAMPLE / PORT)

CASES = {
    "skill": (("SKILL.md",), set()),
    **{hook: ((f"{PORT}#{hook}",), {"W_PRESET_UNUSED"}) for hook in HOOKS},
    **{
        f"{hook}-{sdlc}": ((f"{PORT}#{hook}", "--presets", sdlc), {"W_SUBST_USED"})
        for hook in HOOKS
        for sdlc in SDLCS
    },
}
"""Each case's arguments, and the diagnostic codes its run reports."""


def compile_in(
    root: Path, folder: Path, *arguments: str
) -> tuple[int, list[dict[str, str]]]:
    """Run the build from `root` into `folder`, returning status and diagnostics."""
    err = StringIO()
    with chdir(root):
        status = main(["-o", str(folder), "-d", "json", *arguments], StringIO(), err)
    diagnostics = [json.loads(line) for line in err.getvalue().splitlines() if line]
    return status, diagnostics


def tree(folder: Path) -> dict[str, bytes]:
    """Every file beneath `folder`, keyed by its path from it."""
    return {
        path.relative_to(folder).as_posix(): path.read_bytes()
        for path in sorted(folder.rglob("*"))
        if path.is_file()
    }


def example_copy(tmp_path: Path) -> Path:
    """A copy of the example's sources, without its expected bundles."""
    copy = tmp_path / "project-lifecycle"
    shutil.copytree(EXAMPLE, copy, ignore=shutil.ignore_patterns("expected"))
    return copy


def test_the_port_declares_an_sdlc() -> None:
    assert SDLCS, "the port declares no SDLC, so no hook is compiled under one"


@pytest.mark.parametrize("case", sorted(CASES))
def test_a_case_writes_the_bundles_committed_for_it(tmp_path: Path, case: str) -> None:
    arguments, codes = CASES[case]
    status, diagnostics = compile_in(EXAMPLE, tmp_path, *arguments)
    assert status == 0, diagnostics
    assert {one["code"] for one in diagnostics} == codes
    assert tree(tmp_path) == tree(EXPECTED / case)


def test_every_case_has_a_committed_folder_and_every_folder_a_case() -> None:
    assert {folder.name for folder in EXPECTED.iterdir()} == set(CASES)


def test_the_hooks_the_skill_publishes_are_the_ports() -> None:
    [bundle] = tree(EXPECTED / "skill").values()
    published = re.findall(rf"\]\(({re.escape(PORT)}#[a-z-]+)\)", bundle.decode())
    assert sorted(published) == sorted(f"{PORT}#{hook}" for hook in HOOKS)


def test_an_adapter_missing_a_hook_section_fails_that_hook(tmp_path: Path) -> None:
    copy = example_copy(tmp_path)
    adapter = copy / "sdlc" / "waterfall.md"
    text = adapter.read_text()
    adapter.write_text(text[: text.index("## Verify")])
    status, diagnostics = compile_in(
        copy, tmp_path / "out", f"{PORT}#on-verify", "--presets", "waterfall"
    )
    assert status == 1
    assert "E_TARGET_NOT_FOUND" in {one["code"] for one in diagnostics}


def test_an_adapter_binds_through_one_preset_and_leaves_the_skill_as_it_was(
    tmp_path: Path,
) -> None:
    copy = example_copy(tmp_path)
    (copy / "sdlc" / "iterative.md").write_text(
        "---\nprosiform: {}\n---\n\n# Iterative\n\n"
        "## Plan\n\nPlan the next increment.\n\n"
        "## Deliver\n\nBuild the increment.\n\n"
        "## Verify\n\nDemonstrate the increment.\n"
    )
    port = copy / PORT
    port.write_text(
        port.read_text().replace(
            "---\n\n# SDLC Port",
            "  iterative:\n    subst:\n      - {ad-hoc.md: iterative.md}\n"
            "---\n\n# SDLC Port",
        )
    )
    hook = tmp_path / "hook"
    status, diagnostics = compile_in(
        copy, hook, f"{PORT}#on-deliver", "--presets", "iterative"
    )
    assert status == 0, diagnostics
    [bundle] = tree(hook).values()
    assert "Build the increment." in bundle.decode()
    skill = tmp_path / "skill"
    status, diagnostics = compile_in(copy, skill, "SKILL.md")
    assert status == 0, diagnostics
    assert tree(skill) == tree(EXPECTED / "skill")
