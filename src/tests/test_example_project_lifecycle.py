"""Compile the project-lifecycle example and hold what it writes.

The skill's entry is read as written: one link per SDLC to the lifecycle,
tagged with the preset that binds the SDLC's adapter. Each case compiles the
lifecycle under one SDLC from `example/project-lifecycle/` where it stands
and compares the folder the run writes with the one committed under the
example's `expected/` folder, byte for byte. A case's expected folder is the
output of `pf -o expected/<case> <arguments>`, run from the example's folder.

The SDLCs are read from the lifecycle's presets, so an adapter added there
is compiled and needs an expected folder of its own.

The remaining cases hold the claims the example's README makes: the entry
offers one link per SDLC, each SDLC's bundle carries its own practice and no
other, the modes read the same under every SDLC, an adapter missing a
practice fails its SDLC's build, and an adapter is added through one preset
and one link.
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

LIFECYCLE = "lifecycle.md"

DEFAULT = "ad-hoc"
"""The SDLC the untagged link names: the adapter the lifecycle's links name."""


def presets(document: Path) -> list[str]:
    """The named presets a document's frontmatter declares, `default` aside."""
    frontmatter = document.read_text().split("---\n")[1]
    declared = YAML(typ="safe").load(frontmatter)["prosiform"]
    return [name for name in declared if name != "default"]


SDLCS = presets(EXAMPLE / LIFECYCLE)

CASES = {
    DEFAULT: ((LIFECYCLE,), {"W_PRESET_UNUSED"}),
    **{
        sdlc: ((f'[↳ SDLC]({LIFECYCLE} "{sdlc}")',), {"W_SUBST_USED"}) for sdlc in SDLCS
    },
}
"""Each SDLC's arguments, and the diagnostic codes its run reports."""


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


def bundle_of(folder: Path) -> str:
    """The one bundle a run wrote beneath `folder`."""
    [bundle] = tree(folder).values()
    return bundle.decode()


def example_copy(tmp_path: Path) -> Path:
    """A copy of the example's sources, without its expected bundles."""
    copy = tmp_path / "project-lifecycle"
    shutil.copytree(EXAMPLE, copy, ignore=shutil.ignore_patterns("expected"))
    return copy


def offered(entry: str) -> list[str]:
    """The tags of each link to the lifecycle an entry writes, empty for none."""
    return re.findall(rf'\]\({re.escape(LIFECYCLE)}(?: "([^"]*)")?\)', entry)


def modes_of(bundle: str) -> str:
    """The modes group of a lifecycle's bundle, from its heading to the end."""
    return bundle[bundle.index("\n## Modes\n") :]


def test_the_lifecycle_declares_an_sdlc() -> None:
    assert SDLCS, "the lifecycle declares no SDLC, so no preset is compiled"


@pytest.mark.parametrize("case", sorted(CASES))
def test_an_sdlc_writes_the_bundles_committed_for_it(tmp_path: Path, case: str) -> None:
    arguments, codes = CASES[case]
    status, diagnostics = compile_in(EXAMPLE, tmp_path, *arguments)
    assert status == 0, diagnostics
    assert {one["code"] for one in diagnostics} == codes
    assert tree(tmp_path) == tree(EXPECTED / case)


def test_every_case_has_a_committed_folder_and_every_folder_a_case() -> None:
    assert {folder.name for folder in EXPECTED.iterdir()} == set(CASES)


def test_the_entry_offers_one_link_per_sdlc_tagged_with_its_preset() -> None:
    entry = (EXAMPLE / "SKILL.md").read_text()
    assert sorted(offered(entry)) == sorted(["", *SDLCS])


@pytest.mark.parametrize("case", sorted(CASES))
def test_an_sdlcs_bundle_names_no_other_sdlc(case: str) -> None:
    bundle = bundle_of(EXPECTED / case).lower()
    adapters = {DEFAULT: "ad hoc", **{sdlc: sdlc for sdlc in SDLCS}}
    assert adapters[case] in bundle
    assert [
        name for other, name in adapters.items() if other != case and name in bundle
    ] == []


def test_the_modes_read_the_same_under_every_sdlc() -> None:
    assert len({modes_of(bundle_of(EXPECTED / case)) for case in CASES}) == 1


def test_an_adapter_missing_a_practice_fails_its_sdlc(tmp_path: Path) -> None:
    copy = example_copy(tmp_path)
    adapter = copy / "sdlc" / "waterfall.md"
    text = adapter.read_text()
    adapter.write_text(text[: text.index("## Verify")])
    status, diagnostics = compile_in(
        copy, tmp_path / "out", f'[↳ Waterfall]({LIFECYCLE} "waterfall")'
    )
    assert status == 1
    assert "E_TARGET_NOT_FOUND" in {one["code"] for one in diagnostics}


def test_an_adapter_binds_through_one_preset_and_one_link(tmp_path: Path) -> None:
    copy = example_copy(tmp_path)
    (copy / "sdlc" / "iterative.md").write_text(
        "---\nprosiform: {}\n---\n\n# Iterative\n\n"
        "## Plan\n\nPlan the next increment.\n\n"
        "## Deliver\n\nBuild the increment.\n\n"
        "## Verify\n\nDemonstrate the increment.\n"
    )
    lifecycle = copy / LIFECYCLE
    lifecycle.write_text(
        lifecycle.read_text().replace(
            "---\n\n# Project Lifecycle",
            "  iterative:\n    subst:\n      - {sdlc/ad-hoc.md: sdlc/iterative.md}\n"
            "---\n\n# Project Lifecycle",
        )
    )
    entry = copy / "SKILL.md"
    entry.write_text(entry.read_text() + f'- [↳ Iterative]({LIFECYCLE} "iterative")\n')
    assert sorted(offered(entry.read_text())) == sorted(["", "iterative", *SDLCS])
    folder = tmp_path / "out"
    status, diagnostics = compile_in(
        copy, folder, f'[↳ Iterative]({LIFECYCLE} "iterative")'
    )
    assert status == 0, diagnostics
    bundle = bundle_of(folder)
    assert "Build the increment." in bundle
    assert modes_of(bundle) == modes_of(bundle_of(EXPECTED / DEFAULT))
