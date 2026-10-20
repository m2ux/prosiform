"""Assert that each candidate-validation invariant can fail, and on what.

A validation pass nobody can break reports a guarantee nobody has, so
every check below is given a candidate or a provenance record that
disagrees with the other, and the invariant it names is asserted. The
corpus states what a correct run publishes; these are the cases beneath
it, where the candidate and its provenance are made to disagree on
purpose, which no source document can bring about against a build that
works.
"""

from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Any

import pytest
from markdown_it.token import Token

from prosiform.bundle import Group, assemble, entry_line
from prosiform.candidate import (
    DEPTH_SAFETY,
    ENTRY_LINE_INTEGRITY,
    EXACTLY_ONCE,
    GROUP_ISOLATION,
    NO_DEFINITION_LEAKAGE,
    NO_EXPANSION,
    NO_NEW_LINKS,
    NO_OMISSIONS,
    ONE_DESTINATION,
    OUTLINE_PRESERVATION,
    PRESERVATION,
    REFERENCE_PRESERVATION,
    TARGET_INTEGRITY,
    Invalid,
    validate,
)
from prosiform.cli import (
    assembled,
    destination_map,
    entries_named,
)
from prosiform.closure import Reference
from prosiform.limits import BUDGETS, NESTING, Limits
from prosiform.profile import REFERENCES, parse
from prosiform.provenance import Carried, Generated, Origin, Range
from prosiform.rewrite import Definition, definitions
from prosiform.source import Source, fragments, lines

BUDGET = Limits({budget: budget.default for budget in BUDGETS}).of(NESTING)


@dataclass
class Built:
    """One compiled candidate, with every part the validation pass reads."""

    bundled: str
    groups: list[Group]
    assigned: list[str]
    targets: dict[tuple[str, str | None], str]
    requested: list[Reference]
    read: dict[str, Source]
    parsed: dict[str, list[Token]]

    def validate(self) -> None:
        """Run the validation pass over this candidate as a compilation does."""
        validate(
            self.bundled,
            self.groups,
            self.assigned,
            self.targets,
            None,
            self.requested,
            self.read,
            self.parsed,
            BUDGET,
        )


def built(documents: dict[str, str], references: Sequence[str]) -> Built:
    """One candidate compiled from the sources and entry references given.

    The parts are produced by the command's own assembly, so the pass
    under test is given what a compilation gives it rather than a second
    construction written for the test.
    """
    read = {path: Source(text) for path, text in documents.items()}
    parsed: dict[str, list[Token]] = {}
    defined: dict[str, dict[str, Definition]] = {}
    for path, text in documents.items():
        environment: dict[str, Any] = {}
        parsed[path] = parse(text, BUDGET, environment)
        defined[path] = definitions(environment.get(REFERENCES, {}), lines(text))
    requested = [named(one) for one in references]
    selected: dict[str, list[Reference]] = {}
    for one in requested:
        selected.setdefault(one.path, []).append(one)
    for path in documents:
        selected.setdefault(path, []).append(Reference(path, path))
    selected = dict(sorted(selected.items()))
    headed = assembled(read, parsed, defined, selected, requested, None)
    assigned = fragments([one for each in headed for one in each.headings])
    targets = destination_map(list(selected), headed, assigned)
    groups = assembled(read, parsed, defined, selected, requested, targets)
    bundled = assemble(entry_line(entries_named(groups, assigned)), groups)
    return Built(bundled, groups, assigned, targets, requested, read, parsed)


def named(reference: str) -> Reference:
    """One entry reference, as the command line names a document or a section."""
    path, _, fragment = reference.partition("#")
    return Reference(reference, path, fragment or None)


def refused(one: Built) -> Invalid:
    """The refusal the validation pass raises over this candidate."""
    with pytest.raises(Invalid) as raised:
        one.validate()
    return raised.value


GUIDE = """# Guide

Opening prose the bundle carries as written.

## Rules

Each rule is a rule.

## Notes

Each rule is a rule.
"""

LINKED = """# Guide

The guide names [¬the note](note.md) and [a site](https://example.com).

## Rules

A literal [runner] stays literal.
"""

NOTE = """# Note

The note says so.
"""

DEFINED = """# Guide

> The quoted procedure names [the shared rules][rules].
>
> [rules]: rules.md

The guide carries nothing else.
"""

FENCED = """# Guide

A worked example:

```text
   indented, with   runs   of spaces

and a blank line inside the fence
```
"""


def test_a_candidate_agreeing_with_its_provenance_validates() -> None:
    built({"guide.md": GUIDE}, ["guide.md"]).validate()


def test_a_candidate_carrying_marked_and_literal_references_validates() -> None:
    built({"guide.md": LINKED, "note.md": NOTE}, ["guide.md"]).validate()


def test_a_candidate_whose_definition_was_removed_validates() -> None:
    built({"guide.md": DEFINED}, ["guide.md"]).validate()


def test_repeated_identical_prose_in_two_regions_is_not_duplication() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md#rules", "guide.md#notes"])
    one.validate()
    assert one.bundled.count("Each rule is a rule.") == 2


def test_a_missing_selected_region_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.bundled = one.bundled.replace("\n\nEach rule is a rule.", "", 1)
    assert refused(one).invariant == NO_OMISSIONS


def test_a_region_the_provenance_does_not_account_for_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.bundled = f"{one.bundled}\nAn unaccounted paragraph.\n"
    assert refused(one).invariant == NO_EXPANSION


def test_a_destination_reaching_another_heading_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md#rules"])
    one.targets = dict(one.targets) | {("guide.md", "rules"): one.assigned[0]}
    assert refused(one).invariant == TARGET_INTEGRITY


def test_a_destination_reaching_no_heading_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md#rules"])
    one.targets = dict(one.targets) | {("guide.md", "rules"): "nowhere"}
    assert refused(one).invariant == TARGET_INTEGRITY


def test_a_destination_map_the_candidate_does_not_generate_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.assigned = [*one.assigned[:-1], "renamed"]
    assert refused(one).invariant == ONE_DESTINATION


def test_an_emitted_heading_the_provenance_does_not_record_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.bundled = f"{one.bundled}\n## An unrecorded heading\n"
    assert refused(one).invariant == NO_EXPANSION


def test_a_surviving_definition_fails() -> None:
    one = built({"guide.md": DEFINED}, ["guide.md"])
    one.bundled = f"{one.bundled}\n[rules]: rules.md\n"
    assert refused(one).invariant == NO_DEFINITION_LEAKAGE


def test_literal_bracketed_text_becoming_a_link_fails() -> None:
    one = built({"guide.md": LINKED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace(
        "A literal [runner] stays literal.",
        "A literal [runner](runner.md) stays literal.",
    )
    assert refused(one).invariant == NO_NEW_LINKS


def test_a_rewritten_link_showing_other_text_fails() -> None:
    one = built({"guide.md": LINKED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace("[the note]", "[the other note]")
    assert refused(one).invariant == REFERENCE_PRESERVATION


def test_an_unmarked_link_pointing_elsewhere_fails() -> None:
    one = built({"guide.md": LINKED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace("https://example.com", "https://elsewhere.test")
    assert refused(one).invariant == REFERENCE_PRESERVATION


def test_reformatted_untouched_bytes_fail() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.bundled = one.bundled.replace(
        "Opening prose the bundle carries as written.",
        "Opening prose the bundle carries as  written.",
    )
    assert refused(one).invariant == PRESERVATION


def test_a_repaired_code_example_fails() -> None:
    one = built({"guide.md": FENCED}, ["guide.md"])
    one.bundled = one.bundled.replace("   indented, with   runs   of spaces", "tidied")
    assert refused(one).invariant == PRESERVATION


def test_a_blank_line_removed_from_inside_a_code_example_fails() -> None:
    one = built({"guide.md": FENCED}, ["guide.md"])
    one.bundled = one.bundled.replace(
        "of spaces\n\nand a blank line", "of spaces\nand a blank line"
    )
    assert refused(one).invariant == PRESERVATION


def test_a_heading_emitted_at_another_level_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.bundled = one.bundled.replace("\n## Rules", "\n### Rules")
    assert refused(one).invariant == OUTLINE_PRESERVATION


def test_a_recorded_level_beyond_the_sixth_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.groups = [overflowing(one.groups[0])]
    assert refused(one).invariant == DEPTH_SAFETY


def test_a_source_heading_recorded_at_the_group_level_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.groups = [promoted(one.groups[0])]
    assert refused(one).invariant == GROUP_ISOLATION


def test_a_region_recorded_twice_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.groups = [doubled(one.groups[0])]
    assert refused(one).invariant == EXACTLY_ONCE


def test_an_entry_line_naming_another_destination_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md#rules"])
    one.bundled = one.bundled.replace("](#rules)", "](#notes)", 1)
    assert refused(one).invariant == ENTRY_LINE_INTEGRITY


def test_a_filename_wrapper_does_not_stand_in_for_a_missing_region() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    emptied = replace(one.groups[0].record, ranges=())
    one.groups = [replace(one.groups[0], record=emptied)]
    assert refused(one).invariant == NO_EXPANSION


def overflowing(one: Group) -> Group:
    """The group with one carried heading recorded beyond the sixth level."""
    first = one.record.carried()[0]
    deepened = replace(
        first, level=7, origin=replace(first.origin, level=7 - one.record.shift)
    )
    return replace(
        one,
        record=replace(
            one.record,
            headings=tuple(
                deepened if each is first else each for each in one.record.headings
            ),
        ),
    )


def promoted(one: Group) -> Group:
    """The group with one carried heading recorded at its filename heading's level."""
    first = one.record.carried()[0]
    raised = replace(
        first, level=1, origin=replace(first.origin, level=1 - one.record.shift)
    )
    return replace(
        one,
        record=replace(
            one.record,
            headings=tuple(
                raised if each is first else each for each in one.record.headings
            ),
        ),
    )


def doubled(one: Group) -> Group:
    """The group with one source range recorded twice."""
    first = one.record.ranges[0]
    return replace(one, record=replace(one.record, ranges=(first, *one.record.ranges)))


def test_a_generated_record_carries_no_source_range() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    wrapper = one.groups[0].record.headings[0]
    assert isinstance(wrapper, Generated)
    assert not hasattr(wrapper, "origin")


def test_a_carried_record_names_the_source_heading_it_answers_to() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md#rules"])
    carried = one.groups[0].record.carried()
    assert carried[0] == Carried("Rules", 2, Origin("guide.md", 5, 2, "rules"))


def test_a_range_names_the_lines_of_its_source_it_occupies() -> None:
    one = built({"guide.md": DEFINED}, ["guide.md"])
    assert one.groups[0].record.ranges[0] == Range("guide.md", (2, 5), (4,))


def test_a_definition_line_is_recorded_as_removed_rather_than_absent() -> None:
    one = built({"guide.md": DEFINED}, ["guide.md"])
    assert one.groups[0].record.ranges[0].kept() == [2, 3]
