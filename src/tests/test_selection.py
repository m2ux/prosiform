"""Occurrence selections survive resolution and identify effective bundle variants."""

from dataclasses import replace
from pathlib import Path

import pytest
from markdown_it.token import Token

from prosiform import cli
from prosiform.closure import (
    BundleSelection,
    Reference,
    Substitution,
    bundle_selection,
    bundled,
    inside,
    matching_presets,
    resolve,
    withholding_target,
)
from prosiform.limits import in_force
from prosiform.metadata import Conversion, Preset
from prosiform.tags import read

SETTINGS = Conversion(
    declared=True,
    presets=(Preset("default"), Preset("Draft"), Preset("checks"), Preset("Straße")),
)


def test_resolution_retains_tags_with_the_normalized_destination() -> None:
    tags = read(" Checks, Draft ")
    found = resolve("./rules%20draft.md#run%20it", "docs", tags=tags)
    assert (found.path, found.fragment, found.tags) == (
        "docs/rules draft.md",
        "run it",
        tags,
    )
    local = inside("docs/guide.md", "#run-it", tags=tags)
    assert (local.path, local.fragment, local.tags) == ("docs/guide.md", "run-it", tags)


def test_substitution_keeps_the_occurrences_tags_and_context() -> None:
    found = Reference(
        "rules.md#run",
        "rules.md",
        "run",
        origin="guide.md:5",
        chain=("guide.md", "rules.md#run"),
        title="Heading context",
        composes=True,
        tags=read("checks,draft"),
    )
    alternative = resolve("stand-in.md#chosen", tags=read("other"))
    mapping = Substitution().governed({"guide.md": {("rules.md", None): alternative}})
    redirected = mapping.writing("guide.md").redirect(found)
    assert (redirected.path, redirected.fragment) == ("stand-in.md", "chosen")
    assert redirected.tags == {"checks", "draft"}
    assert (redirected.original, redirected.origin, redirected.chain) == (
        found.original,
        found.origin,
        found.chain,
    )
    assert redirected.title == found.title
    assert redirected.composes
    assert redirected.redirected


@pytest.mark.parametrize(
    "opening", ["Rules", "↳ Rules", "¬ Rules", "⇉ Rules", "⫽ Rules"]
)
def test_compiled_and_withheld_resolution_keep_their_own_selection(
    opening: str,
) -> None:
    mapping = Substitution().governed(
        {"guide.md": {("rules.md", None): resolve("stand-in.md")}}
    )
    arguments = ("guide.md", "rules.md#run", opening)
    tags = read("checks, draft")
    found = bundled(*arguments, substitution=mapping, tags=tags)
    withheld = withholding_target(*arguments, substitution=mapping, tags=tags)
    target = found if found is not None else withheld
    assert target is not None
    assert (target.path, target.fragment, target.tags) == ("stand-in.md", "run", tags)


def test_matching_uses_complete_names_and_the_destinations_declaration_order() -> None:
    assert [
        preset.name for preset in matching_presets(SETTINGS, read("CHECKS,draft"))
    ] == [
        "Draft",
        "checks",
    ]
    assert matching_presets(SETTINGS, read("Checklist,Checks and Draft")) == ()
    assert [preset.name for preset in matching_presets(SETTINGS, read("STRASSE"))] == [
        "Straße"
    ]


@pytest.mark.parametrize("names", [None, "", " , ", "unknown", "default,DEFAULT"])
def test_absent_unknown_and_default_tokens_have_default_only_identity(
    names: str | None,
) -> None:
    assert bundle_selection(resolve("guide.md", tags=read(names)), SETTINGS) == (
        BundleSelection("guide.md")
    )


def test_equivalent_selections_share_one_hashable_effective_identity() -> None:
    first = bundle_selection(
        resolve("./%67uide.md#run", tags=read("Checks,Draft")), SETTINGS
    )
    second = bundle_selection(
        resolve("guide.md#run", tags=read(" DRAFT, checks,checks,unknown,default ")),
        SETTINGS,
    )
    assert (
        first
        == second
        == BundleSelection("guide.md", "run", frozenset({"Draft", "checks"}))
    )
    assert len({first, second}) == 1
    assert first == bundle_selection(
        resolve("guide.md#run", tags=read("draft,checks")),
        replace(SETTINGS, presets=tuple(reversed(SETTINGS.presets))),
    )


def test_bundle_identity_distinguishes_destination_fragment_and_presets() -> None:
    selected = resolve("guide.md#run", tags=read("checks"))
    key = bundle_selection(selected, SETTINGS)
    assert key != bundle_selection(replace(selected, path="other.md"), SETTINGS)
    assert key != bundle_selection(replace(selected, fragment="other"), SETTINGS)
    assert key != bundle_selection(replace(selected, tags=read("draft")), SETTINGS)
    assert key == bundle_selection(
        replace(selected, original="another spelling", title="Other", origin="x:2"),
        SETTINGS,
    )


def test_empty_and_absent_fragments_share_whole_document_identity() -> None:
    assert bundle_selection(Reference("guide.md#", "guide.md", ""), SETTINGS) == (
        bundle_selection(resolve("guide.md"), SETTINGS)
    )


def test_a_substitutes_own_presets_answer_the_retained_tags() -> None:
    mapping = Substitution().governed(
        {"guide.md": {("rules.md", None): resolve("stand-in.md")}}
    )
    found = inside("guide.md", "rules.md", mapping, tags=read("checks,draft"))
    substitute_settings = Conversion(True, (Preset("checks"), Preset("other")))
    assert bundle_selection(found, substitute_settings) == BundleSelection(
        "stand-in.md", presets=frozenset({"checks"})
    )


def test_a_fragment_only_occurrence_keeps_its_tags_when_substituted() -> None:
    mapping = Substitution().governed(
        {"guide.md": {("guide.md", "run"): resolve("stand-in.md#chosen")}}
    )
    found = inside("guide.md", "#run", mapping, tags=read("checks,draft"))
    assert (found.path, found.fragment, found.tags) == (
        "stand-in.md",
        "chosen",
        frozenset({"checks", "draft"}),
    )


def source(root: Path, name: str, content: str) -> None:
    (root / name).write_text("---\nprosiform: {}\n---\n" + content)


def test_traversal_retains_occurrence_selections_and_captures_a_source_once(
    tmp_path: Path,
) -> None:
    source(
        tmp_path,
        "guide.md",
        '# Guide\n\n[One](rules.md "checks") [Two](rules.md "draft")\n',
    )
    source(tmp_path, "rules.md", "# Rules\n\n[Leaf](leaf.md)\n")
    source(tmp_path, "leaf.md", "# Leaf\n")
    read_sources, _, _, captured, references, _, _ = cli.traverse(
        tmp_path, [resolve("guide.md", tags=read("incoming"))], in_force({})
    )
    assert len(read_sources) == len(captured) == 3
    assert [one.tags for one in references if one.path == "rules.md"] == [
        {"checks"},
        {"draft"},
    ]
    assert [one.tags for one in references if one.path == "leaf.md"] == [frozenset()]


def test_traversal_keeps_each_selection_when_a_default_pair_redirects_its_target(
    tmp_path: Path,
) -> None:
    (tmp_path / "guide.md").write_text(
        "---\nprosiform:\n  default:\n    subst: [{rules.md: stand-in.md}]\n---\n"
        '# Guide\n\n[One](rules.md "checks") [Two](rules.md "draft")\n'
    )
    source(tmp_path, "stand-in.md", "# Stand-In\n")
    _, _, _, captured, references, _, _ = cli.traverse(
        tmp_path, [resolve("guide.md")], in_force({})
    )
    assert set(captured) == {"guide.md", "stand-in.md"}
    substitutes = [one for one in references if one.path == "stand-in.md"]
    assert [one.tags for one in substitutes] == [{"checks"}, {"draft"}]
    assert all(one.redirected for one in substitutes)


def test_deferred_occurrences_retain_distinct_tags_through_target_confirmation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source(
        tmp_path,
        "guide.md",
        '# Guide\n\n[¬ One](rules.md "checks") [¬ Two](rules.md "draft")\n',
    )
    source(tmp_path, "rules.md", "# Rules\n")
    confirmed: list[frozenset[str]] = []
    confirm = cli.confirm

    def observing(tokens: list[Token], reference: Reference) -> None:
        confirmed.append(reference.tags)
        confirm(tokens, reference)

    monkeypatch.setattr(cli, "confirm", observing)
    _, _, _, captured, references, _, _ = cli.traverse(
        tmp_path, [resolve("guide.md")], in_force({})
    )
    assert len(captured) == 2
    assert len(references) == 1
    assert confirmed == [{"checks"}, {"draft"}]


def test_dispatch_targets_keep_occurrence_tags_before_variant_scheduling(
    tmp_path: Path,
) -> None:
    source(
        tmp_path,
        "guide.md",
        "# Guide\n\n[⇉ One][one] [⇉ Two][two]\n\n"
        '[one]: rules.md "checks"\n[two]: rules.md "draft"\n',
    )
    source(tmp_path, "rules.md", "# Rules\n")
    _, _, _, captured, _, hops, _ = cli.traverse(
        tmp_path, [resolve("guide.md")], in_force({})
    )
    assert len(captured) == 2
    assert [hop.target.tags for hop in hops] == [{"checks"}, {"draft"}]
