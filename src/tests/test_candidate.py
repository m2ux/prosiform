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

from prosiform.bundle import Group, assemble
from prosiform.candidate import (
    DEPTH_SAFETY,
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
    UNSAFE_BUNDLE_BOUNDARY,
    Invalid,
    Unsafe,
    protocols,
    validate,
)
from prosiform.cli import (
    assembled,
    destination_map,
)
from prosiform.closure import Reference
from prosiform.limits import BUDGETS, NESTING, Limits
from prosiform.profile import REFERENCES, parse
from prosiform.provenance import (
    FILENAME_WRAPPER,
    PROSIFORM_SECTION,
    Ancestor,
    Carried,
    Generated,
    Instruction,
    Origin,
    Range,
    Record,
)
from prosiform.rewrite import Definition, definitions
from prosiform.source import Source, fragments, lines, regions

BUDGET = Limits({budget: budget.default for budget in BUDGETS}).of(NESTING)


@dataclass
class Built:
    """One compiled candidate, with every part the validation pass reads."""

    bundled: str
    groups: list[Group]
    assigned: list[str]
    targets: dict[tuple[str, str | None], str]
    read: dict[str, Source]
    parsed: dict[str, list[Token]]

    def validate(self) -> None:
        """Run the validation pass over this candidate as a compilation does."""
        validate(
            self.bundled,
            self.groups,
            self.assigned,
            self.targets,
            self.read,
            self.parsed,
            BUDGET,
        )


def built(
    documents: dict[str, str], references: Sequence[str], whole: bool = True
) -> Built:
    """One candidate compiled from the sources and entry references given.

    The parts are produced by the command's own assembly, so the pass
    under test is given what a compilation gives it rather than a second
    construction written for the test.

    Every document is selected whole as well, which is what a run
    bundling the tree produces. A candidate carrying structural
    ancestors is the exception: an ancestor is a heading a selection
    left unselected, so a whole document leaves none, and such a case
    selects the references it names and nothing more.
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
    if whole:
        for path in documents:
            selected.setdefault(path, []).append(Reference(path, path))
    selected = dict(sorted(selected.items()))
    headed = assembled(read, parsed, defined, selected, requested, None, {})
    assigned = fragments([one for each in headed for one in each.headings])
    targets = destination_map(headed, assigned)
    groups = assembled(read, parsed, defined, selected, requested, targets, {})
    bundled = assemble(groups)
    return Built(bundled, groups, assigned, targets, read, parsed)


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

The guide names [the note](note.md) and [a site](https://example.com).

## Rules

A literal [runner] stays literal.
"""

NOTE = """# Note

The note says so.
"""

HEADED = """# Note

The note says so.

## Detail

The detail the note holds.
"""

RULES = """# Rules

Each rule the quoted procedure names.
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


def test_a_candidate_carrying_compiled_and_literal_references_validates() -> None:
    built({"guide.md": LINKED, "note.md": NOTE}, ["guide.md"]).validate()


def test_a_candidate_whose_definition_was_removed_validates() -> None:
    built({"guide.md": DEFINED, "rules.md": RULES}, ["guide.md"]).validate()


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
    one = built({"guide.md": DEFINED, "rules.md": RULES}, ["guide.md"])
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


DIAGRAMMED = """# Guide

```mermaid
flowchart LR
    Open([Open]) --> Note([Note])
    %% the note links nowhere yet
    click Open href "note.md"
```
"""


def test_a_candidate_carrying_a_rewritten_diagram_destination_validates() -> None:
    one = built({"guide.md": DIAGRAMMED, "note.md": NOTE}, ["guide.md"])
    one.validate()
    assert 'click Open href "#note"' in one.bundled


def test_a_diagram_destination_pointing_elsewhere_fails() -> None:
    one = built({"guide.md": DIAGRAMMED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace('href "#note"', 'href "#guide"')
    assert refused(one).invariant == REFERENCE_PRESERVATION


def test_a_diagram_destination_left_as_its_source_wrote_it_fails() -> None:
    one = built({"guide.md": DIAGRAMMED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace('href "#note"', 'href "note.md"')
    assert refused(one).invariant == REFERENCE_PRESERVATION


def test_a_dropped_diagram_click_fails() -> None:
    one = built({"guide.md": DIAGRAMMED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace('click Open href "#note"', "%% no click")
    assert refused(one).invariant == NO_NEW_LINKS


def test_an_added_diagram_click_fails() -> None:
    one = built({"guide.md": DIAGRAMMED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace(
        "%% the note links nowhere yet", 'click Note href "#note"'
    )
    assert refused(one).invariant == NO_NEW_LINKS


SEQUENCED = """# Guide

```mermaid
sequenceDiagram
    participant Open
    link Open: The note @ note.md
    links Open: {"Note": "note.md"}
```
"""


def test_a_candidate_carrying_rewritten_sequence_menu_destinations_validates() -> None:
    one = built({"guide.md": SEQUENCED, "note.md": NOTE}, ["guide.md"])
    one.validate()
    assert "link Open: The note @ #35;note\n" in one.bundled
    assert 'links Open: {"Note": "#35;note"}' in one.bundled


def test_a_sequence_menu_entry_spelling_its_anchor_bare_names_nothing() -> None:
    one = built({"guide.md": SEQUENCED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace("@ #35;note", "@ #note")
    assert refused(one).invariant == NO_NEW_LINKS


def test_a_sequence_menu_value_spelling_its_anchor_bare_names_nothing() -> None:
    one = built({"guide.md": SEQUENCED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace('"#35;note"', '"#note"')
    assert refused(one).invariant == NO_NEW_LINKS


def test_a_sequence_menu_entry_naming_another_heading_fails() -> None:
    one = built({"guide.md": SEQUENCED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace("@ #35;note", "@ #35;guide")
    assert refused(one).invariant == REFERENCE_PRESERVATION


def test_a_click_spelling_its_anchor_as_an_entity_fails() -> None:
    one = built({"guide.md": DIAGRAMMED, "note.md": NOTE}, ["guide.md"])
    one.bundled = one.bundled.replace('href "#note"', 'href "#35;note"')
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
    one = built({"guide.md": GUIDE, "note.md": HEADED}, ["guide.md"])
    wrapped = next(each for each in one.groups if each.order != "guide.md")
    one.groups = [promoted(wrapped) if each is wrapped else each for each in one.groups]
    assert refused(one).invariant == GROUP_ISOLATION


def test_a_region_recorded_twice_fails() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    one.groups = [doubled(one.groups[0])]
    assert refused(one).invariant == EXACTLY_ONCE


def test_a_filename_wrapper_does_not_stand_in_for_a_missing_region() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md"])
    emptied = replace(one.groups[0].record, parts=())
    one.groups = [replace(one.groups[0], record=emptied)]
    assert refused(one).invariant == NO_EXPANSION


def overflowing(one: Group) -> Group:
    """The group with one carried heading recorded beyond the sixth level."""
    first = one.record.carried()[0]
    deepened = replace(
        first,
        level=7,
        origins=(replace(first.origins[0], level=7 - first.origins[0].shift),),
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
        first,
        level=1,
        origins=(replace(first.origins[0], level=1 - first.origins[0].shift),),
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
    return replace(one, record=replace(one.record, parts=(first, *one.record.parts)))


def test_a_generated_record_carries_no_source_range() -> None:
    one = built({"guide.md": GUIDE, "note.md": NOTE}, ["guide.md"])
    wrapped = next(each for each in one.groups if each.order != "guide.md")
    wrapper = wrapped.record.headings[0]
    assert isinstance(wrapper, Generated)
    assert not hasattr(wrapper, "origin")


def test_a_carried_record_names_the_source_heading_it_answers_to() -> None:
    one = built({"guide.md": GUIDE}, ["guide.md#rules"])
    carried = one.groups[0].record.carried()
    assert carried[0] == Carried(
        "Rules", 2, (Origin("guide.md", 5, 2, "rules", 0),), (("guide.md", "rules"),)
    )


def test_a_range_names_the_lines_of_its_source_it_occupies() -> None:
    one = built({"guide.md": DEFINED, "rules.md": RULES}, ["guide.md"])
    quote = Range("guide.md", (2, 5), (4,))
    assert quote in one.groups[0].record.ranges


def test_a_definition_line_is_recorded_as_removed_rather_than_absent() -> None:
    one = built({"guide.md": DEFINED, "rules.md": RULES}, ["guide.md"])
    quote = next(one for one in one.groups[0].record.ranges if one.lines == (2, 5))
    assert quote.kept() == [2, 3]


UNTERMINATED = """# Guide

A worked example:

~~~markdown
## Stop

An example the document never closes.
"""

ADJACENT = """# Guide

- The item the first list carries.

[notes]: notes.md

- The item the second list carries.
"""

NESTED = """# Guide

- The item the outer list carries.
  - The item nested inside it.

[notes]: notes.md

- The item the list below carries.
"""

MARKUP = """# Guide

- The item the list carries.

[notes]: notes.md

    <div>Markup the source wrote as a code example.</div>
"""

TERMINATED = """# Guide

~~~yaml
blocks:
  - the first
  - the second
~~~

- The item the list below the example carries.
"""


def unsafely(one: Built) -> Unsafe:
    """The boundary the validation pass refuses this candidate for."""
    with pytest.raises(Unsafe) as raised:
        one.validate()
    return raised.value


def test_a_group_an_unterminated_code_example_absorbs_fails() -> None:
    one = built({"guide.md": UNTERMINATED, "note.md": NOTE}, ["guide.md"])
    boundary = unsafely(one)
    assert boundary.code == UNSAFE_BUNDLE_BOUNDARY
    assert boundary.container == "code example"
    assert boundary.absorbed == "the heading for 'note.md'"
    assert boundary.carried == "the region at lines (4, 8) of 'guide.md'"


def test_an_unterminated_code_example_is_refused_rather_than_closed() -> None:
    one = built({"guide.md": UNTERMINATED, "note.md": NOTE}, ["guide.md"])
    unsafely(one)
    assert one.bundled.count("~~~") == 1


def test_a_list_the_list_above_it_absorbs_fails() -> None:
    boundary = unsafely(built({"guide.md": ADJACENT}, ["guide.md"]))
    assert boundary.container == "list"
    assert boundary.absorbed == "the region at lines (6, 7) of 'guide.md'"


def test_a_region_a_nested_container_absorbs_fails() -> None:
    assert unsafely(built({"guide.md": NESTED}, ["guide.md"])).container == "list"


def test_a_code_example_a_list_reads_as_markup_fails() -> None:
    boundary = unsafely(built({"guide.md": MARKUP}, ["guide.md"]))
    assert boundary.container == "list"
    assert boundary.path == "guide.md"


def test_a_terminated_example_whose_entries_look_like_a_list_validates() -> None:
    built({"guide.md": TERMINATED}, ["guide.md"]).validate()


OUTLINED = """## Alpha

Alpha body.

### One

One body.
"""


def test_a_structural_ancestor_holds_as_the_heading_it_records() -> None:
    built({"guide.md": OUTLINED}, ["guide.md#one"], whole=False).validate()


def test_an_ancestor_the_group_drops_fails() -> None:
    one = built({"guide.md": OUTLINED}, ["guide.md#one"], whole=False)
    carried = one.groups[0]
    kept = carried.record.ancestors()[0]
    one.groups = [
        replace(
            carried,
            parts=tuple(part for part in carried.parts if part != "### Alpha"),
            record=replace(
                carried.record,
                headings=tuple(
                    each for each in carried.record.headings if each is not kept
                ),
                parts=tuple(each for each in carried.record.parts if each is not kept),
            ),
        )
    ]
    one.bundled = one.bundled.replace("### Alpha\n\n", "", 1)
    one.assigned = [name for name in one.assigned if name != "alpha"]
    assert refused(one).invariant == OUTLINE_PRESERVATION


def test_an_ancestor_placing_no_part_fails() -> None:
    one = built({"guide.md": OUTLINED}, ["guide.md#one"], whole=False)
    carried = one.groups[0]
    stray = Ancestor("Beta", 3, (Origin("guide.md", 99, 2, "beta", 1),))
    one.groups = [
        replace(
            carried,
            record=replace(carried.record, headings=(*carried.record.headings, stray)),
        )
    ]
    assert refused(one).invariant == NO_EXPANSION


def test_a_structural_ancestor_does_not_stand_in_for_a_missing_region() -> None:
    one = built({"guide.md": OUTLINED}, ["guide.md#one"], whole=False)
    carried = one.groups[0]
    body = carried.record.ranges[-1]
    one.groups = [
        replace(
            carried,
            record=replace(
                carried.record,
                parts=tuple(each for each in carried.record.parts if each is not body),
            ),
        )
    ]
    assert refused(one).invariant == NO_EXPANSION


def test_an_ancestor_emitted_as_something_other_than_a_heading_fails() -> None:
    one = built({"guide.md": OUTLINED}, ["guide.md#one"], whole=False)
    carried = one.groups[0]
    one.groups = [
        replace(
            carried,
            parts=tuple(
                "Alpha" if part == "### Alpha" else part for part in carried.parts
            ),
        )
    ]
    one.bundled = one.bundled.replace("### Alpha", "Alpha", 1)
    one.assigned = [name for name in one.assigned if name != "alpha"]
    assert refused(one).invariant == NO_EXPANSION


def test_an_ancestor_publishing_a_live_link_fails() -> None:
    one = built({"guide.md": OUTLINED}, ["guide.md#one"], whole=False)
    carried = one.groups[0]
    linked = "### [Alpha](#one)"
    one.groups = [
        replace(
            carried,
            parts=tuple(
                linked if part == "### Alpha" else part for part in carried.parts
            ),
        )
    ]
    one.bundled = one.bundled.replace("### Alpha", linked, 1)
    assert refused(one).invariant == NO_NEW_LINKS


NESTED_IMAGE = """# Guide

A picture ![of the [shared rules](rules.md) it names](plan.png).
"""

RULES = """# Rules

Every rule the procedure requires.
"""


def test_a_link_inside_image_alternative_content_validates() -> None:
    built({"guide.md": NESTED_IMAGE, "rules.md": RULES}, ["guide.md"]).validate()


def test_a_link_inside_image_alternative_content_the_bundle_altered_fails() -> None:
    one = built({"guide.md": NESTED_IMAGE, "rules.md": RULES}, ["guide.md"])
    carried = one.groups[0]
    one.groups = [
        replace(
            carried,
            parts=tuple(
                part.replace("[shared rules](#rules)", "[other rules](#rules)")
                for part in carried.parts
            ),
        ),
        *one.groups[1:],
    ]
    one.bundled = one.bundled.replace(
        "[shared rules](#rules)", "[other rules](#rules)", 1
    )
    assert refused(one).invariant == REFERENCE_PRESERVATION


def instructing(destination: str) -> None:
    """Hold one instruction linking one destination to the Prosiform protocols."""
    line = f"[Dispatch]({destination}) `plan.bundle.md` to a sub-agent."
    text = f"# Prosiform\n\n## Dispatch\n\nProtocol.\n\n# Guide\n\n{line}\n"
    tokens = parse(text, BUDGET)
    headings = (
        Generated("Prosiform", 1, PROSIFORM_SECTION),
        Generated("Dispatch", 2, PROSIFORM_SECTION),
        Generated("Guide", 1, FILENAME_WRAPPER),
    )
    record = Record("guide.md", None, headings, ())
    reached = {
        fragment: (record, heading)
        for fragment, heading in zip(
            ["prosiform", "dispatch", "guide"], headings, strict=True
        )
    }
    protocols(reached, Instruction(line), list(regions(tokens))[-1], tokens)


def test_an_instruction_linking_its_protocol_holds() -> None:
    instructing("#dispatch")


@pytest.mark.parametrize("destination", ["#guide", "#nowhere"])
def test_an_instruction_linking_no_protocol_of_the_prosiform_section_is_invalid(
    destination: str,
) -> None:
    with pytest.raises(Invalid) as caught:
        instructing(destination)
    assert caught.value.invariant == TARGET_INTEGRITY
