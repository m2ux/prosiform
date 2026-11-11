"""Compile the project-lifecycle example and hold what it writes.

Each case runs the build over `example/project-lifecycle/` where it stands
and compares the folder the run writes with the one committed under the
example's `expected/` folder, byte for byte, so the example and the bundles
it documents cannot drift apart. A case's expected folder is the output of
`pf -o expected/<case> <arguments>`, run from the example's folder.

The remaining cases hold the claims the example's README makes: the hook
links the skill's bundle publishes are the hooks the build compiles, an
adapter missing a hook section fails the hook's build, and an adapter is
added without editing a mode.
"""

import json
import re
import shutil
from contextlib import chdir
from io import StringIO
from pathlib import Path

import pytest

from prosiform.cli import main

EXAMPLE = Path(__file__).resolve().parents[2] / "example" / "project-lifecycle"
"""The example under test, read where it stands."""

EXPECTED = EXAMPLE / "expected"
"""One folder per case, holding what that case's run writes."""

HOOKS = ("on-plan", "on-deliver", "on-verify")

CASES = {
    "skill": (("SKILL.md",), set()),
    **{hook: ((f"sdlc/port.md#{hook}",), {"W_PRESET_UNUSED"}) for hook in HOOKS},
    **{
        f"{hook}-waterfall": (
            (f"sdlc/port.md#{hook}", "--presets", "waterfall"),
            {"W_SUBST_USED"},
        )
        for hook in HOOKS
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


@pytest.mark.parametrize("case", sorted(CASES))
def test_a_case_writes_the_bundles_committed_for_it(tmp_path: Path, case: str) -> None:
    arguments, codes = CASES[case]
    status, diagnostics = compile_in(EXAMPLE, tmp_path, *arguments)
    assert status == 0, diagnostics
    assert {one["code"] for one in diagnostics} == codes
    assert tree(tmp_path) == tree(EXPECTED / case)


def test_every_case_has_a_committed_folder_and_every_folder_a_case() -> None:
    assert {folder.name for folder in EXPECTED.iterdir()} == set(CASES)


def test_each_hook_the_skill_publishes_compiles_under_each_sdlc(
    tmp_path: Path,
) -> None:
    [bundle] = tree(EXPECTED / "skill").values()
    published = re.findall(r"\]\((sdlc/port\.md#[a-z-]+)\)", bundle.decode())
    assert sorted(published) == sorted(f"sdlc/port.md#{hook}" for hook in HOOKS)
    for n, hook in enumerate(published):
        for presets in ((), ("--presets", "waterfall")):
            folder = tmp_path / f"{n}{len(presets)}"
            status, diagnostics = compile_in(EXAMPLE, folder, hook, *presets)
            assert status == 0, (hook, presets, diagnostics)


def test_an_adapter_missing_a_hook_section_fails_that_hook(tmp_path: Path) -> None:
    copy = example_copy(tmp_path)
    adapter = copy / "sdlc" / "waterfall.md"
    text = adapter.read_text()
    adapter.write_text(text[: text.index("## Verify")])
    status, diagnostics = compile_in(
        copy, tmp_path / "out", "sdlc/port.md#on-verify", "--presets", "waterfall"
    )
    assert status == 1
    assert "E_TARGET_NOT_FOUND" in {one["code"] for one in diagnostics}


def test_an_adapter_binds_through_one_preset_and_no_mode_changes(
    tmp_path: Path,
) -> None:
    copy = example_copy(tmp_path)
    modes = tree(copy / "modes")
    (copy / "sdlc" / "iterative.md").write_text(
        "---\nprosiform: {}\n---\n\n# Iterative\n\n"
        "## Plan\n\nPlan the next increment.\n\n"
        "## Deliver\n\nBuild the increment.\n\n"
        "## Verify\n\nDemonstrate the increment.\n"
    )
    port = copy / "sdlc" / "port.md"
    port.write_text(
        port.read_text().replace(
            "---\n\n# SDLC Port",
            "  iterative:\n    subst:\n      - {ad-hoc.md: iterative.md}\n"
            "---\n\n# SDLC Port",
        )
    )
    folder = tmp_path / "out"
    status, diagnostics = compile_in(
        copy, folder, "sdlc/port.md#on-deliver", "--presets", "iterative"
    )
    assert status == 0, diagnostics
    [bundle] = tree(folder).values()
    assert "Build the increment." in bundle.decode()
    assert tree(copy / "modes") == modes
