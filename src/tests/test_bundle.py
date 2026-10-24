"""Assert the bundle's structure: its file groups and its entry line.

The corpus declares what a run publishes. These are the cases beneath
it: the heading one path generates, the escaping that keeps that heading
literal, the regions a selection carries into a group, the headings a
partial selection needs above it, and the two decisions a group makes
about its own headings.
"""

import pytest

from prosiform.bundle import (
    MAX_LEVEL,
    Group,
    Overflow,
    absorbed,
    assemble,
    entry_line,
    escaped,
    group,
    heading_text,
    is_entry_line,
    openings,
    title_cased,
)
from prosiform.profile import parse
from prosiform.provenance import STRUCTURAL_ANCESTOR, Origin
from prosiform.source import Selection, lines, regions, section


def grouped(path: str, text: str) -> Group:
    """One file group, from the path that names it and the source it carries."""
    return group(path, parse(text), lines(text))


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("guide", "Guide"),
        ("docs/note", "Docs/Note"),
        ("docs/sub/note", "Docs/Sub/Note"),
        ("my-note", "My-Note"),
        ("docs/field-notes", "Docs/Field-Notes"),
        ("plan_mode", "Plan_Mode"),
        ("two words", "Two Words"),
        ("Already Titled", "Already Titled"),
        ("GUIDE", "GUIDE"),
        ("notes.v2", "Notes.v2"),
        ("café-münster", "Café-Münster"),
    ],
)
def test_a_generated_heading_capitalizes_each_word_and_keeps_every_separator(
    text: str, expected: str
) -> None:
    assert title_cased(text) == expected


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("guide.md", "Guide"),
        ("guide.markdown", "Guide"),
        ("GUIDE.MARKDOWN", "GUIDE"),
        ("docs/note.md", "Docs/Note"),
        ("docs/sub/note.md", "Docs/Sub/Note"),
        ("notes.v2.md", "Notes.v2"),
        ("guide", "Guide"),
    ],
)
def test_a_file_heading_is_the_path_without_its_markdown_suffix(
    path: str, expected: str
) -> None:
    assert heading_text(path) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("guide", "guide"),
        ("docs/note", "docs/note"),
        ("plan_[v2]", "plan\\_\\[v2\\]"),
        ("a*b", "a\\*b"),
        ("a`b", "a\\`b"),
        ("a<b>c", "a\\<b\\>c"),
        ("a&b", "a\\&b"),
        ("a~b", "a\\~b"),
        ("a!b", "a\\!b"),
        ("a\\b", "a\\\\b"),
        ("a#b", "a\\#b"),
        ("note-1.v2 (final)", "note-1.v2 (final)"),
    ],
)
def test_a_path_is_escaped_as_literal_heading_text(text: str, expected: str) -> None:
    assert escaped(text) == expected


def test_an_escaped_path_opens_no_construct() -> None:
    heading = f"# {escaped('plan_[v2](x)')}\n"
    tokens = parse(heading)
    children = tokens[1].children or []
    assert [child.type for child in children] == ["text"]
    assert children[0].content == "plan_[v2](x)"


def test_an_escaped_path_closes_no_heading() -> None:
    """A number sign ending a path is heading text, not a closing sequence."""
    heading = f"# {escaped('notes/draft #')}\n"
    tokens = parse(heading)
    children = tokens[1].children or []
    assert [child.type for child in children] == ["text"]
    assert children[0].content == "notes/draft #"


def test_a_path_ending_in_a_number_sign_keeps_it_in_its_file_heading() -> None:
    one = grouped("notes/draft #.md", "A document whose path ends in a number sign.\n")
    assert one.text.splitlines()[0] == "# Notes/Draft \\#"
    assert one.headings[0] == "Notes/Draft #"


def test_the_entry_line_names_one_reference_and_its_destination() -> None:
    assert entry_line([("guide", "guide")]) == (
        "Follow [guide](#guide). "
        "The other sections are material that procedure references."
    )


def test_the_entry_line_names_every_reference_the_run_was_given() -> None:
    assert entry_line([("a", "a"), ("b", "b"), ("c", "c")]) == (
        "Follow [a](#a), [b](#b) and [c](#c). "
        "The other sections are material those procedures reference."
    )


def test_the_entry_line_escapes_the_text_of_the_heading_it_names() -> None:
    assert "[plan\\_\\[v2\\]](#plan_v2)" in entry_line([("plan_[v2]", "plan_v2")])


def test_a_declared_dispatch_text_follows_the_entry_sentence() -> None:
    sentence = entry_line([("guide", "guide")])
    assert entry_line([("guide", "guide")], "Each mark is the sub-agent's.") == (
        f"{sentence} Each mark is the sub-agent's."
    )


def test_a_declared_dispatch_text_follows_the_sentence_for_any_entry_count() -> None:
    named = [("a", "a"), ("b", "b")]
    assert entry_line(named, "One rule.") == f"{entry_line(named)} One rule."


def test_an_absent_dispatch_text_leaves_the_entry_sentence_alone() -> None:
    assert entry_line([("guide", "guide")]) == entry_line([("guide", "guide")], None)


def test_a_dispatch_text_is_escaped_as_literal_text() -> None:
    assert "a \\[v2\\] rule" in entry_line([("g", "g")], "a [v2] rule")


def test_the_entry_line_is_recognized_wherever_its_sentence_is_published() -> None:
    assert is_entry_line(entry_line([("guide", "guide")]))
    assert is_entry_line(entry_line([("guide", "guide")], "One rule."))


def test_a_paragraph_that_does_not_carry_the_entry_sentence_is_no_entry_line() -> None:
    assert not is_entry_line("Follow the guide.")
    assert not is_entry_line("Read [guide](#guide).")


def test_a_dispatch_text_reaches_the_bundle_as_one_paragraph_where_the_sentence_is() -> None:
    carried = grouped("note.md", "Body.\n")
    line = entry_line([("Note", "note")], "One rule.")
    assert f"{line}\n" in assemble(line, [carried])


def test_a_group_opens_on_its_file_heading() -> None:
    assert grouped("docs/note.md", "Body.\n").text == "# Docs/Note\n\nBody.\n"


def test_a_title_the_path_already_names_is_absorbed() -> None:
    carried = grouped("guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    assert carried.text == "# Guide\n\n## Run\n\nDo it.\n"
    assert carried.headings == ("Guide", "Run")


def test_a_path_segment_is_slugged_as_the_title_it_is_compared_with_is() -> None:
    carried = grouped("My Note.md", "# My Note\n\n## Run\n\nDo it.\n")
    assert carried.text == "# My Note\n\n## Run\n\nDo it.\n"
    assert carried.headings == ("My Note", "Run")


def test_a_hyphenated_segment_absorbs_the_title_spelling_it_with_spaces() -> None:
    carried = grouped("docs/my-note.md", "# My Note\n\n## Run\n")
    assert carried.text == "# Docs/My-Note\n\n## Run\n"


def test_a_title_naming_another_segment_of_the_path_is_not_absorbed() -> None:
    carried = grouped("docs/note.md", "# Docs\n\n## Run\n")
    assert carried.text == "# Docs/Note\n\n## Docs\n\n### Run\n"


def test_an_absorbed_group_keeps_its_source_heading_levels() -> None:
    text = "# Guide\n\n## Run\n\n### Detail\n"
    assert grouped("guide.md", text).text == "# Guide\n\n## Run\n\n### Detail\n"


def test_a_title_the_path_does_not_name_is_kept_and_shifted() -> None:
    carried = grouped("guide.md", "# Another Name\n\n## Run\n")
    assert carried.text == "# Guide\n\n## Another Name\n\n### Run\n"
    assert carried.headings == ("Guide", "Another Name", "Run")


def test_a_second_h1_leaves_the_title_unabsorbed() -> None:
    text = "# Guide\n\nOne.\n\n# Guide\n"
    assert grouped("guide.md", text).text == "# Guide\n\n## Guide\n\nOne.\n\n## Guide\n"


def test_an_h1_that_is_not_the_first_heading_leaves_the_title_unabsorbed() -> None:
    text = "## Run\n\n# Guide\n"
    assert grouped("guide.md", text).text == "# Guide\n\n### Run\n\n## Guide\n"


def test_a_container_nested_title_is_not_absorbed() -> None:
    assert absorbed(parse("> # Guide\n"), "guide") is None


def test_a_document_carrying_no_heading_keeps_its_file_heading_alone() -> None:
    assert grouped("guide.md", "Body only.\n").text == "# Guide\n\nBody only.\n"


def test_a_preamble_sits_after_the_file_heading_and_before_the_first_heading() -> None:
    text = "# Guide\n\nLead text.\n\n## Run\n"
    assert grouped("guide.md", text).text == "# Guide\n\nLead text.\n\n## Run\n"


def test_a_blank_line_above_the_first_region_is_not_carried() -> None:
    assert grouped("guide.md", "\n\n# Guide\n\nBody.\n").text == "# Guide\n\nBody.\n"


def test_a_removed_reference_definition_leaves_no_blank_line_behind_it() -> None:
    text = "# Guide\n\n- [x] done\n\n[x]: page.md\n"
    assert grouped("guide.md", text).text == "# Guide\n\n- [x] done\n"


def test_an_unused_reference_definition_is_removed_with_the_used_ones() -> None:
    text = "# Guide\n\nBody.\n\n[a]: one.md\n[b]: two.md\n"
    assert grouped("guide.md", text).text == "# Guide\n\nBody.\n"


@pytest.mark.parametrize(
    "written",
    [
        " ---",
        "---  ",
        '+++\ntitle = "Guide"\n+++',
        "    <span>raw</span>",
        "```text\n[[page]]\n```",
        "> quoted\n> more",
        "- one\n\n- two",
    ],
)
def test_a_region_carries_the_bytes_its_source_wrote(written: str) -> None:
    carried = grouped("guide.md", f"# Guide\n\n{written}\n")
    assert carried.text == f"# Guide\n\n{written}\n"


def test_a_region_ends_with_the_newline_its_source_spelled() -> None:
    text = "# Guide\r\n\r\nOne line.\r\n\r\n- one\r\n- two\r\n"
    assert grouped("guide.md", text).text == (
        "# Guide\n\nOne line.\r\n\n- one\r\n- two\r\n"
    )


def test_a_last_line_carrying_no_terminator_ends_with_the_bundles_own() -> None:
    assert grouped("guide.md", "# Guide\r\n\r\nOne line.").text == (
        "# Guide\n\nOne line.\n"
    )


def test_a_bundle_closes_with_the_newline_its_final_part_carries() -> None:
    bundled = assemble("Line.", [grouped("guide.md", "# Guide\r\n\r\nBody.\r\n")])
    assert bundled == "Line.\n\n# Guide\n\nBody.\r\n"


def test_the_separation_between_two_regions_is_one_blank_line() -> None:
    text = "# Guide\n\nOne.\n\n\n\n\nTwo.\n"
    assert grouped("guide.md", text).text == "# Guide\n\nOne.\n\nTwo.\n"


@pytest.mark.parametrize(
    ("written", "expected"),
    [
        ("> ## Quoted", "> ### Quoted"),
        ("> > ## Quoted", "> > ### Quoted"),
        ("- item\n\n  ## Listed", "- item\n\n  ### Listed"),
        ("1. item\n\n   ## Listed", "1. item\n\n   ### Listed"),
    ],
)
def test_a_heading_a_container_carries_is_shifted_where_it_sits(
    written: str, expected: str
) -> None:
    carried = grouped("guide.md", f"# Another Name\n\n{written}\n")
    assert carried.text == f"# Guide\n\n## Another Name\n\n{expected}\n"


def test_a_heading_a_container_carries_is_one_the_group_emits() -> None:
    carried = grouped("guide.md", "# Guide\n\n> ## Quoted\n>\n> Inside.\n\n## Run\n")
    assert carried.headings == ("Guide", "Quoted", "Run")


def test_a_heading_a_code_example_holds_is_no_heading_the_group_emits() -> None:
    carried = grouped("guide.md", "# Guide\n\n> ```\n> ## Not A Heading\n> ```\n")
    assert carried.headings == ("Guide",)


def test_a_container_keeps_the_heading_like_text_a_code_example_holds() -> None:
    written = "> ```markdown\n> ## Not A Heading\n> ```"
    carried = grouped("guide.md", f"# Another Name\n\n{written}\n")
    assert carried.text == f"# Guide\n\n## Another Name\n\n{written}\n"


@pytest.mark.parametrize(
    ("written", "expected"),
    [
        ("Run\n===", "## Run"),
        ("Run\n---", "### Run"),
        ("Run the *marked* `one`\n---", "### Run the *marked* `one`"),
        ("Run\nand stop\n---", "### Run and stop"),
        ("> Quoted\n> ---", "> ### Quoted"),
    ],
)
def test_a_shifted_group_emits_a_setext_heading_as_atx(
    written: str, expected: str
) -> None:
    carried = grouped("guide.md", f"# Another Name\n\n{written}\n")
    assert carried.text == f"# Guide\n\n## Another Name\n\n{expected}\n"


def test_a_group_that_shifts_by_nothing_leaves_a_setext_heading_alone() -> None:
    carried = grouped("guide.md", "# Guide\n\nRun\n---\n")
    assert carried.text == "# Guide\n\nRun\n---\n"


def test_a_converted_heading_keeps_a_number_sign_run_ending_its_text() -> None:
    carried = grouped("guide.md", "# Another Name\n\nSharp #\n---\n")
    assert carried.text == "# Guide\n\n## Another Name\n\n### Sharp \\#\n"


def test_a_converted_heading_shows_the_text_its_source_lines_carried() -> None:
    carried = grouped("guide.md", "# Another Name\n\nRun\nand stop\n---\n")
    assert carried.headings == ("Guide", "Another Name", "Run and stop")


def test_a_shift_beyond_the_sixth_level_for_a_nested_heading_is_an_overflow() -> None:
    text = "# Another Name\n\n> ###### Deep\n"
    with pytest.raises(Overflow) as refused:
        grouped("guide.md", text)
    assert refused.value.heading == "Deep"
    assert refused.value.level == MAX_LEVEL + 1


def test_a_shift_beyond_the_sixth_level_is_an_overflow() -> None:
    text = "# Another Name\n\n###### Deep\n"
    with pytest.raises(Overflow) as refused:
        grouped("guide.md", text)
    assert refused.value.heading == "Deep"
    assert refused.value.level == MAX_LEVEL + 1


def test_an_absorbed_group_reaches_the_sixth_level_without_overflow() -> None:
    text = "# Guide\n\n###### Deep\n"
    assert grouped("guide.md", text).text == "# Guide\n\n###### Deep\n"


def test_a_bundle_ends_in_exactly_one_newline() -> None:
    bundled = assemble("Line.", [grouped("guide.md", "# Guide\n")])
    assert bundled == "Line.\n\n# Guide\n"


def test_a_group_is_its_parts_one_blank_line_apart() -> None:
    text = "# Guide\n\nOpening prose.\n\n## Rules\n"
    carried = grouped("guide.md", text)
    assert carried.parts == ("# Guide", "Opening prose.\n", "## Rules\n")
    assert carried.text == "# Guide\n\nOpening prose.\n\n## Rules\n"


def test_each_part_opens_one_blank_line_below_the_part_above_it() -> None:
    text = "# Guide\n\nOpening prose.\n\n- A rule.\n- Another rule.\n"
    carried = grouped("guide.md", text)
    bundled = assemble("Line.", [carried])
    assert openings([carried], 1) == [2, 4, 6]
    assert [lines(bundled)[at] for at in openings([carried], 1)] == [
        "# Guide\n",
        "Opening prose.\n",
        "- A rule.\n",
    ]


def test_the_parts_of_two_groups_open_in_bundle_order() -> None:
    first = grouped("guide.md", "# Guide\n\nOpening prose.\n")
    second = grouped("note.md", "# Note\n")
    bundled = assemble("Line.", [first, second])
    assert openings([first, second], 1) == [2, 4, 6]
    assert [lines(bundled)[at] for at in openings([first, second], 1)] == [
        "# Guide\n",
        "Opening prose.\n",
        "# Note\n",
    ]


def selecting(path: str, text: str, *named: str) -> Group:
    """One file group holding the sections the fragments name and nothing else."""
    tokens = parse(text)
    wanted = [
        token for fragment in named for token in (section(tokens, fragment) or ())
    ]
    chosen = tuple(
        token for token in regions(tokens) if any(token is one for one in wanted)
    )
    return group(path, tokens, lines(text), None, Selection(chosen, ()), None)


OUTLINED = """## Alpha

Alpha body.

### One

One body.

### Two

Two body.

## Beta

Beta body.
"""


def test_an_unselected_ancestor_is_emitted_as_a_heading_alone() -> None:
    carried = selecting("guide.md", OUTLINED, "one")
    assert carried.text == "# Guide\n\n### Alpha\n\n#### One\n\nOne body.\n"


def test_an_ancestor_two_selections_share_is_emitted_once() -> None:
    carried = selecting("guide.md", OUTLINED, "one", "two")
    assert carried.headings == ("Guide", "Alpha", "One", "Two")


def test_an_ancestor_stands_in_the_source_order_its_author_wrote() -> None:
    text = "## Alpha\n\n### One\n\nOne body.\n\n## Beta\n\n### Two\n\nTwo body.\n"
    carried = selecting("guide.md", text, "one", "two")
    assert carried.headings == ("Guide", "Alpha", "One", "Beta", "Two")


def test_a_selected_ancestor_is_the_content_it_is_rather_than_a_heading() -> None:
    carried = selecting("guide.md", OUTLINED, "alpha")
    assert carried.text == (
        "# Guide\n\n### Alpha\n\nAlpha body.\n\n#### One\n\nOne body."
        "\n\n#### Two\n\nTwo body.\n"
    )
    assert carried.record.ancestors() == []


def test_an_ancestor_title_is_emitted_as_literal_text() -> None:
    text = "## A & [the note](note.md) <b>b</b>\n\n### One\n\nOne body.\n"
    carried = selecting("guide.md", text, "one")
    assert carried.parts[1] == "### A \\& the note b"
    assert carried.record.ancestors()[0].text == "A & the note b"


def test_an_ancestor_title_keeps_the_mark_a_link_it_carries_was_deferred_by() -> None:
    text = "## A [¬the note](note.md) heading\n\n### One\n\nOne body.\n"
    carried = selecting("guide.md", text, "one")
    assert carried.parts[1] == "### A ¬the note heading"
    assert carried.record.ancestors()[0].text == "A ¬the note heading"


def test_an_ancestor_record_names_its_source_heading_and_original_level() -> None:
    one = selecting("guide.md", OUTLINED, "one").record.ancestors()[0]
    assert (one.text, one.level, one.kind) == ("Alpha", 3, STRUCTURAL_ANCESTOR)
    assert one.origins == (Origin("guide.md", 1, 2, "alpha", 1),)


def test_an_ancestor_accounts_for_the_part_it_emits_and_carries_no_range() -> None:
    carried = selecting("guide.md", OUTLINED, "one")
    record = carried.record
    assert len(record.parts) == len(carried.parts) - 1 == 3
    assert record.parts[0] == record.ancestors()[0]
    assert [one.lines for one in record.ranges] == [(4, 5), (6, 7)]


def test_a_title_the_file_heading_names_is_no_ancestor() -> None:
    text = "# Guide\n\n## Run\n\n### Detail\n\nDetail body.\n"
    carried = selecting("guide.md", text, "detail")
    assert carried.text == "# Guide\n\n### Run\n\n#### Detail\n\nDetail body.\n"


def test_a_heading_a_container_carries_roots_no_ancestor_chain() -> None:
    text = "## Alpha\n\n> ### Quoted\n\n### One\n\nOne body.\n"
    carried = selecting("guide.md", text, "one")
    assert carried.headings == ("Guide", "Alpha", "One")


def test_an_ancestor_at_the_sixth_level_overflows_on_what_it_places() -> None:
    """An ancestor reaching H6 holds, and the heading beneath it is the overflow."""
    text = "##### Five\n\nFive body.\n\n###### Six\n\nSix body.\n"
    with pytest.raises(Overflow) as refused:
        selecting("guide.md", text, "six")
    assert refused.value.heading == "Six"
    assert refused.value.level == MAX_LEVEL + 1
