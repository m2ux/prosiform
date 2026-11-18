"""The brief a dispatch carries, as its target's presets in force name it."""

import pytest

from prosiform.cli import USAGE_FAILURE, Failure, briefed
from prosiform.closure import Briefs, Reference, brief_of, briefing
from prosiform.diagnostics import Location
from prosiform.dispatch import Hop
from prosiform.metadata import Conversion, Preset
from prosiform.tags import PICK

TARGET = Conversion(
    declared=True,
    presets=(
        Preset("default", brief="#given"),
        Preset("deep", brief="#deeper"),
        Preset("plain"),
        Preset("other", brief="#other"),
    ),
)


def test_default_s_brief_is_carried_where_no_selected_preset_names_one() -> None:
    assert brief_of(frozenset(), TARGET) == "#given"
    assert brief_of(frozenset({"plain"}), TARGET) == "#given"


def test_a_selected_preset_s_brief_holds_over_default_s() -> None:
    assert brief_of(frozenset({"deep"}), TARGET) == "#deeper"
    assert brief_of(frozenset({"deep", "plain"}), TARGET) == "#deeper"


def test_a_target_naming_no_brief_carries_none() -> None:
    assert brief_of(frozenset(), Conversion(declared=True)) is None


def test_two_selected_presets_naming_different_briefs_are_refused() -> None:
    with pytest.raises(Briefs) as caught:
        brief_of(frozenset({"deep", "other"}), TARGET)
    assert caught.value.first.name == "deep"
    assert caught.value.later.name == "other"


def test_a_brief_is_a_composing_reference_to_its_section() -> None:
    target = Reference(
        "investigate.md", "investigate.md", tags=frozenset({"plain", PICK})
    )
    found = briefing(target, TARGET)
    assert found is not None
    assert (found.path, found.fragment) == ("investigate.md", "given")
    assert found.composes
    assert found.tags == frozenset({"plain"})


def test_a_dispatch_carrying_no_brief_has_no_composing_reference() -> None:
    target = Reference("investigate.md", "investigate.md")
    assert briefing(target, Conversion(declared=True)) is None


def test_a_dispatch_selecting_two_briefs_is_invalid_usage() -> None:
    target = Reference(
        "investigate.md", "investigate.md", tags=frozenset({"deep", "other"})
    )
    with pytest.raises(Failure) as caught:
        briefed(Hop(target, Location("guide.md", 3, 1)), TARGET)
    assert caught.value.status == USAGE_FAILURE
    assert caught.value.diagnostic.code == "E_INVALID_USAGE"


def test_a_picking_dispatch_to_an_alternative_naming_a_brief_is_unresolved() -> None:
    conversion = Conversion(
        declared=True,
        presets=(Preset("Task", choice="One task.", brief="#given"),),
    )
    target = Reference(
        "stage.md",
        "stage.md",
        origin="guide.md:3",
        chain=("guide.md", "stage.md"),
        tags=frozenset({PICK}),
    )
    with pytest.raises(Failure) as caught:
        briefed(Hop(target, Location("guide.md", 3, 1)), conversion)
    diagnostic = caught.value.diagnostic
    assert diagnostic.code == "E_ALTERNATIVE_UNRESOLVED"
    assert diagnostic.reference == "stage.md"
    assert diagnostic.chain == ("guide.md", "stage.md")
    assert diagnostic.location == Location("guide.md", 3, 1)
    assert diagnostic.remedy == (
        "declare the brief in default or an ordinary preset, so it does not vary "
        "by alternative, since the picking dispatch carrying it leaves the pick "
        "to its agent"
    )
