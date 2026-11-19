"""Stub presets: trial material the run's entry names select in every bundle."""

from pathlib import Path

import pytest
from test_cli import DECLARED, FROM_BUNDLE, invoke, written
from test_metadata import parse

from prosiform.diagnostics import Location
from prosiform.metadata import InvalidMetadata

STAGE = (
    "---\nprosiform:\n  recorded:\n"
    "    stub: Reads the recorded reference.\n"
    "    subst: [{reference.md: stub.md}]\n---\n"
    "# Stage\n\n1. Read the [Reference](reference.md).\n"
)


def tree(root: Path, entry: str) -> None:
    written(root, "entry.md", DECLARED + "# Entry\n\n" + entry + "\n")
    written(root, "stage.md", STAGE)
    written(root, "reference.md", DECLARED + "# Reference\n\nLIVE\n")
    written(root, "stub.md", DECLARED + "# Reference\n\nRECORDED\n")


ONE_LINE = "must be a non-empty string holding no line break"


def codes(stderr: str) -> list[str]:
    return [line.split(":")[0] for line in stderr.splitlines() if line[:2] in "W_E_"]


def test_a_stub_preset_holds_its_line() -> None:
    result = parse("prosiform:\n  recorded: {stub: Reads the recorded reference.}")
    assert [one.stub for one in result.presets] == ["Reads the recorded reference."]
    assert result.alternatives == ()


@pytest.mark.parametrize(
    ("fields", "says", "at"),
    [
        ("{stub: A., choice: B.}", "holds both choice and stub", (3, 24)),
        ("{choice: B., stub: A.}", "holds both choice and stub", (3, 26)),
        ('{stub: ""}', ONE_LINE, (3, 20)),
        ('{stub: "a\\nb"}', ONE_LINE, (3, 20)),
        ("{stub: [a]}", ONE_LINE, (3, 20)),
    ],
)
def test_a_malformed_stub_is_refused(
    fields: str, says: str, at: tuple[int, int]
) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform:\n  recorded: " + fields)
    diagnostic = caught.value.diagnostic
    assert diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert says in diagnostic.message
    assert diagnostic.location == Location("rules/a.md", *at)


@pytest.mark.parametrize("name", ["default", "Default"])
def test_a_stub_in_default_is_refused(name: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(f"prosiform:\n  {name}:\n    stub: Every run.")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert f"prosiform.{name}.stub is refused" in caught.value.diagnostic.message


def test_the_entry_name_selects_a_stub_below_a_dispatch(tmp_path: Path) -> None:
    tree(tmp_path, "Hand over [⇉ Stage](stage.md).")
    run = invoke('[Entry](entry.md "Recorded")', cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert codes(run.stderr) == ["W_SUBST_USED"]
    (dispatched,) = (text for name, text in run.bundles.items() if "stage" in name)
    assert "RECORDED" in dispatched and "LIVE" not in dispatched
    assert "stage--p-" in run.bundle


def test_a_run_naming_no_stub_is_silent(tmp_path: Path) -> None:
    tree(tmp_path, "Hand over [⇉ Stage](stage.md).")
    run = invoke("entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert run.stderr == ""
    assert "[⇉ Stage](stage.bundle.md)" in run.bundle


def test_a_link_title_naming_a_stub_selects_it(tmp_path: Path) -> None:
    tree(tmp_path, '1. Read the [Stage](stage.md "recorded").')
    run = invoke("entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert "RECORDED" in run.bundle and "LIVE" not in run.bundle


def test_an_entry_name_leaves_an_ordinary_preset_unselected(tmp_path: Path) -> None:
    tree(tmp_path, "Hand over [⇉ Stage](stage.md).")
    written(
        tmp_path,
        "stage.md",
        STAGE.replace("    stub: Reads the recorded reference.\n", ""),
    )
    run = invoke('[Entry](entry.md "recorded")', cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert codes(run.stderr) == ["W_PRESET_UNUSED"]


def test_a_used_stub_pair_warns_once_across_bundles(tmp_path: Path) -> None:
    tree(tmp_path, "Read the [Stage](stage.md), then hand over [⇉ Stage](stage.md).")
    run = invoke('[Entry](entry.md "recorded")', cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert codes(run.stderr) == ["W_SUBST_USED"]


@pytest.mark.parametrize(
    ("authored", "published"),
    [
        ("[¬ Stage](stage.md)", f'[Stage]({FROM_BUNDLE}stage.md "recorded")'),
        (
            '[¬ Stage](stage.md "draft")',
            f'[Stage]({FROM_BUNDLE}stage.md "draft, recorded")',
        ),
        (
            "[¬ Stage](stage.md 'recorded')",
            f"[Stage]({FROM_BUNDLE}stage.md 'recorded')",
        ),
        ('[¬ Stage](stage.md "")', f'[Stage]({FROM_BUNDLE}stage.md "recorded")'),
        (
            "[¬ Stage][s]\n\n[s]: stage.md (x)",
            f"[Stage]({FROM_BUNDLE}stage.md (x, recorded))",
        ),
    ],
)
def test_a_deferral_carries_the_runs_names(
    tmp_path: Path, authored: str, published: str
) -> None:
    tree(tmp_path, authored)
    run = invoke('[Entry](entry.md "recorded")', cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert published in run.bundle


def test_a_deferring_click_carries_the_runs_names(tmp_path: Path) -> None:
    tree(
        tmp_path,
        "```mermaid\nflowchart LR\n  A[¬ A] --> B[¬ B] --> C[¬ C]\n"
        '  click A "stage.md"\n'
        '  click B "stage.md" "draft"\n'
        '  click C href "stage.md" "" _blank\n```',
    )
    run = invoke('[Entry](entry.md "recorded")', cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert f'click A "{FROM_BUNDLE}stage.md" "recorded"\n' in run.bundle
    assert f'click B "{FROM_BUNDLE}stage.md" "draft, recorded"\n' in run.bundle
    assert f'click C href "{FROM_BUNDLE}stage.md" "recorded" _blank\n' in run.bundle


def test_a_deferral_omits_a_name_its_target_declares_otherwise(
    tmp_path: Path,
) -> None:
    tree(tmp_path, "[¬ Stage](stage.md)")
    written(
        tmp_path,
        "stage.md",
        "---\nprosiform:\n  recorded: {}\n---\n# Stage\n\nBody.\n",
    )
    run = invoke('[Entry](entry.md "recorded")', cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert f"[Stage]({FROM_BUNDLE}stage.md)" in run.bundle


def test_a_deferred_directive_carries_the_runs_names(tmp_path: Path) -> None:
    tree(tmp_path, "## Compose\n\n[¬↳ Read](stage.md#step)")
    written(
        tmp_path,
        "stage.md",
        STAGE.replace("# Stage\n", "# Stage\n\n## Parent\n\n### Step\n"),
    )
    run = invoke('[Entry](entry.md "recorded")', cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert f'({FROM_BUNDLE}stage.md#step "recorded")' in run.bundle
