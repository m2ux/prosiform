"""Effective dispatch selections govern compilation, analysis and publication."""

import argparse
from pathlib import Path

import pytest
from test_cli import DECLARED, invoke, written

from prosiform import cli
from prosiform.closure import BundleSelection, Reference, Substitution

PRESETS = (
    "---\nprosiform:\n"
    "  default:\n    subst: [{body.md: default.md}]\n"
    "  checks:\n    subst: [{body.md: checked.md}]\n"
    "  draft:\n    subst: [{body.md: drafted.md}]\n---\n"
)


def tree(root: Path, links: str) -> None:
    """A dispatch entry and a target with three independently observable bodies."""
    written(root, "entry.md", DECLARED + "# Entry\n\n" + links + "\n")
    written(root, "task.md", PRESETS + "# Task\n\n[Body](body.md)\n")
    for name in ("default", "checked", "drafted"):
        written(root, name + ".md", DECLARED + "# Body\n\n" + name.upper() + "\n")


def name(*presets: str, path: str = "task.md") -> str:
    """The contract filename for a target with the stated matched declarations."""
    return cli.bundle_file(BundleSelection(path, presets=frozenset(presets)))


def test_distinct_effective_selections_compile_distinct_bodies(tmp_path: Path) -> None:
    tree(
        tmp_path,
        '[⇉ Checked](task.md "checks")\n\n[⇉ Draft](task.md "draft")',
    )
    run = invoke("entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    checked, drafted = name("checks"), name("draft")
    assert set(run.bundles) == {"entry.bundle.md", checked, drafted}
    assert f"]({checked}" in run.bundle and f"]({drafted}" in run.bundle
    assert "CHECKED" in run.bundles[checked]
    assert "DRAFTED" not in run.bundles[checked]
    assert "DRAFTED" in run.bundles[drafted]
    assert "CHECKED" not in run.bundles[drafted]


@pytest.mark.parametrize("reversed_order", [False, True])
def test_equivalent_requests_compile_once_under_the_contract_name(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, reversed_order: bool
) -> None:
    links = [
        '[⇉ First](task.md "checks,draft")',
        '[⇉ Second](./task.md# "DRAFT, checks,unknown,default,checks,,")',
        '[⇉ Third](task.md " draft,checks ")',
    ]
    if reversed_order:
        links.reverse()
    tree(tmp_path, "\n\n".join(links))
    written(
        tmp_path,
        "task.md",
        "---\nprosiform:\n"
        "  checks:\n    subst: [{body.md: checked.md}]\n"
        "  draft: {}\n---\n# Task\n\n[Body](body.md)\n",
    )
    observed: list[BundleSelection] = []
    compile_bundle = cli.compiled

    def observing(
        root: Path,
        requested: list[Reference],
        options: argparse.Namespace,
        substitution: Substitution,
    ) -> cli.Compiled:
        result = compile_bundle(root, requested, options, substitution)
        observed.append(result.selection)
        return result

    monkeypatch.setattr(cli, "compiled", observing)
    run = invoke("entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    expected = (
        "task--p-13c9f40cda0225cb29b9fa2332a291e8950291238a73b75fed0cd1521986f6e8"
        ".bundle.md"
    )
    assert set(run.bundles) == {"entry.bundle.md", expected}
    assert run.bundle.count(f"]({expected}") == 3
    assert observed == [
        BundleSelection("entry.md"),
        BundleSelection("task.md", presets=frozenset({"checks", "draft"})),
    ]


def test_unmatched_and_default_requests_share_the_empty_effective_selection(
    tmp_path: Path,
) -> None:
    tree(
        tmp_path,
        '[⇉ First](task.md)\n\n[⇉ Second](task.md "default, unknown, ,DEFAULT")',
    )
    run = invoke("entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert set(run.bundles) == {"entry.bundle.md", "task.bundle.md"}
    assert run.bundle.count("](task.bundle.md") == 2
    assert "DEFAULT" in run.bundles["task.bundle.md"]


def branching(root: Path, ending: str) -> None:
    """The default task reaches another preset of itself through a separate bundle."""
    written(
        root,
        "task.md",
        "---\nprosiform:\n"
        "  default:\n    subst: [{next.md: default-next.md}]\n"
        "  checks:\n    subst: [{next.md: selected-next.md}]\n---\n"
        "# Task\n\n[⇉ Next](next.md)\n",
    )
    written(
        root,
        "default-next.md",
        DECLARED + '# Default Next\n\n[⇉ Selected](task.md "checks")\n',
    )
    written(root, "selected-next.md", DECLARED + "# Selected Next\n\n" + ending)


def test_a_distinct_variant_of_the_entry_is_a_new_hop(tmp_path: Path) -> None:
    branching(tmp_path, "Finished.\n")
    run = invoke("-d", "json", "task.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert set(run.bundles) == {
        "task.bundle.md",
        name("checks"),
        "default-next.bundle.md",
        "selected-next.bundle.md",
    }
    assert "default-next.bundle.md" in run.bundles["task.bundle.md"]
    assert "selected-next.bundle.md" in run.bundles[name("checks")]
    assert not any(one["code"] == "E_DISPATCH_CYCLE" for one in run.diagnostics())


def test_depth_counts_distinct_variants_of_one_destination(tmp_path: Path) -> None:
    branching(tmp_path, "[⇉ Tail](tail.md)\n")
    written(tmp_path, "tail.md", DECLARED + "# Tail\n")
    run = invoke("-d", "json", "task.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    warnings = [one for one in run.diagnostics() if one["code"] == "W_DISPATCH_DEPTH"]
    assert len(warnings) == 1
    assert warnings[0]["chain"] == [
        "task.md",
        "default-next.md",
        "task.md",
        "selected-next.md",
        "tail.md",
    ]
    assert len(run.bundles) == 5


def test_a_return_to_an_equivalent_entry_selection_is_a_cycle(tmp_path: Path) -> None:
    branching(tmp_path, '[⇉ Return](task.md "default,unknown")\n')
    run = invoke("-d", "json", "task.md", cwd=tmp_path)
    assert run.status == 1, run.stderr
    assert run.bundles == {}
    [refusal] = run.diagnostics()
    assert refusal["code"] == "E_DISPATCH_CYCLE"
    assert refusal["chain"] == [
        "task.md",
        "default-next.md",
        "task.md",
        "selected-next.md",
        "task.md",
    ]


def test_a_named_entry_and_its_equivalent_dispatch_close_one_cycle(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "task.md",
        "---\nprosiform:\n  checks: {}\n---\n"
        '# Task\n\n[⇉ Same](./task.md# "CHECKS,unknown,default,checks")\n',
    )
    run = invoke("-d", "json", "task.md", "--presets", "checks", cwd=tmp_path)
    assert run.status == 1, run.stderr
    assert run.bundles == {}
    [refusal] = run.diagnostics()
    assert refusal["code"] == "E_DISPATCH_CYCLE"
    assert refusal["chain"] == ["task.md", "task.md"]


def test_each_effective_entry_dispatch_can_raise_one_depth_warning(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "entry.md",
        DECLARED + '# Entry\n\n[⇉ One](task.md "checks") [⇉ Two](task.md "draft")\n\n'
        '[⇉ Again](task.md "CHECKS,unknown")\n',
    )
    written(
        tmp_path,
        "task.md",
        "---\nprosiform:\n  checks: {}\n  draft: {}\n---\n# Task\n\n[⇉ Next](a.md)\n",
    )
    for source, target in (("a", "b"), ("b", "c")):
        written(
            tmp_path,
            source + ".md",
            DECLARED + f"# {source.upper()}\n\n[⇉ Next]({target}.md)\n",
        )
    written(tmp_path, "c.md", DECLARED + "# C\n")
    run = invoke("-d", "json", "entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    warnings = [one for one in run.diagnostics() if one["code"] == "W_DISPATCH_DEPTH"]
    assert len(warnings) == 2
    assert len(run.bundles) == 6


def test_variants_count_the_file_budget_from_their_own_closures(tmp_path: Path) -> None:
    tree(
        tmp_path,
        '[⇉ Checked](task.md "checks")\n\n[⇉ Draft](task.md "draft")',
    )
    for source in ("checked", "drafted"):
        written(
            tmp_path,
            source + ".md",
            DECLARED + f"# {source}\n\n[Leaf]({source}-leaf.md)\n",
        )
        written(tmp_path, source + "-leaf.md", DECLARED + "# Leaf\n")
    within = invoke("--budget", "files=3", "entry.md", cwd=tmp_path)
    assert within.status == 0, within.stderr
    assert len(within.bundles) == 3
    crossed = invoke("-d", "json", "--budget", "files=2", "entry.md", cwd=tmp_path)
    assert crossed.status == 1, crossed.stderr
    assert crossed.bundles == {}
    [refusal] = crossed.diagnostics()
    assert refusal["code"] == "E_RESOURCE_LIMIT"


def test_the_output_budget_applies_to_each_variant_bundle(tmp_path: Path) -> None:
    tree(
        tmp_path,
        '[⇉ Checked](task.md "checks")\n\n[⇉ Draft](task.md "draft")',
    )
    measured = invoke("entry.md", cwd=tmp_path)
    assert measured.status == 0, measured.stderr
    assert len(measured.bundles) == 3
    budget = max(len(text.encode("utf-8")) for text in measured.bundles.values())
    assert sum(len(text.encode("utf-8")) for text in measured.bundles.values()) > budget
    run = invoke("--budget", f"output-bytes={budget}", "entry.md", cwd=tmp_path)
    assert run.status == 0, run.stderr
    assert run.bundles == measured.bundles


@pytest.mark.parametrize("check", [False, True])
@pytest.mark.parametrize("placement", ["inline", "parallel", "heading"])
def test_distinct_variants_colliding_on_a_filename_preserve_the_previous_set(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, check: bool, placement: str
) -> None:
    tree(
        tmp_path,
        '[⇉ Checked](task.md "checks")\n\n[⇉ Draft](task.md "draft")',
    )
    if placement != "inline":
        heading = "## " if placement == "heading" else ""
        written(
            tmp_path,
            "entry.md",
            DECLARED
            + "# Entry\n\n"
            + heading
            + '[⫽ Checked](task.md "checks") [⫽ Draft](task.md "draft")\n',
        )
    output = tmp_path / "output"
    folder = output / "entry.bundles"
    folder.mkdir(parents=True)
    sentinel = folder / "previous.bundle.md"
    sentinel.write_text("The earlier published set.\n")
    original_name = cli.bundle_file

    def colliding(selected: BundleSelection) -> str:
        return (
            "collision.bundle.md"
            if selected.path == "task.md"
            else original_name(selected)
        )

    monkeypatch.setattr(cli, "bundle_file", colliding)
    mode = ["-c"] if check else []
    run = invoke("-d", "json", "-o", str(output), *mode, "entry.md", cwd=tmp_path)
    assert run.status == 3, run.stderr
    [refusal] = run.diagnostics()
    assert refusal["code"] == "E_PUBLICATION_FAILED"
    assert 'with presets ["checks"]' in refusal["message"]
    assert 'with presets ["draft"]' in refusal["message"]
    assert list(folder.iterdir()) == [sentinel]
    assert sentinel.read_text() == "The earlier published set.\n"
