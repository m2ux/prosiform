"""Assert the bundle's structure: its file groups and its entry line.

The corpus declares what a run publishes. These are the cases beneath
it: the heading one path generates, the escaping that keeps that heading
literal, the regions a selection carries into a group, and the two
decisions a group makes about its own headings.
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
)
from prosiform.profile import parse
from prosiform.source import lines


def grouped(path: str, text: str) -> Group:
    """One file group, from the path that names it and the source it carries."""
    return group(path, parse(text), lines(text))


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("guide.md", "guide"),
        ("guide.markdown", "guide"),
        ("GUIDE.MARKDOWN", "GUIDE"),
        ("docs/note.md", "docs/note"),
        ("docs/sub/note.md", "docs/sub/note"),
        ("notes.v2.md", "notes.v2"),
        ("guide", "guide"),
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
    assert one.text.splitlines()[0] == "# notes/draft \\#"
    assert one.headings[0] == "notes/draft #"


def test_the_entry_line_names_one_reference_and_its_destination() -> None:
    assert entry_line([("guide", "guide")]) == (
        "This bundle was built for [guide](#guide); "
        "everything else is material it references."
    )


def test_the_entry_line_names_every_reference_the_run_was_given() -> None:
    line = entry_line([("a", "a"), ("b", "b"), ("c", "c")])
    assert line.startswith("This bundle was built for [a](#a), [b](#b) and [c](#c);")


def test_the_entry_line_escapes_the_text_of_the_heading_it_names() -> None:
    assert "[plan\\_\\[v2\\]](#plan_v2)" in entry_line([("plan_[v2]", "plan_v2")])


def test_a_group_opens_on_its_file_heading() -> None:
    assert grouped("docs/note.md", "Body.\n").text == "# docs/note\n\nBody."


def test_a_title_the_path_already_names_is_absorbed() -> None:
    carried = grouped("guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    assert carried.text == "# guide\n\n## Run\n\nDo it."
    assert carried.headings == ("guide", "Run")


def test_a_path_segment_is_slugged_as_the_title_it_is_compared_with_is() -> None:
    carried = grouped("My Note.md", "# My Note\n\n## Run\n\nDo it.\n")
    assert carried.text == "# My Note\n\n## Run\n\nDo it."
    assert carried.headings == ("My Note", "Run")


def test_a_hyphenated_segment_absorbs_the_title_spelling_it_with_spaces() -> None:
    carried = grouped("docs/my-note.md", "# My Note\n\n## Run\n")
    assert carried.text == "# docs/my-note\n\n## Run"


def test_a_title_naming_another_segment_of_the_path_is_not_absorbed() -> None:
    carried = grouped("docs/note.md", "# Docs\n\n## Run\n")
    assert carried.text == "# docs/note\n\n## Docs\n\n### Run"


def test_an_absorbed_group_keeps_its_source_heading_levels() -> None:
    text = "# Guide\n\n## Run\n\n### Detail\n"
    assert grouped("guide.md", text).text == "# guide\n\n## Run\n\n### Detail"


def test_a_title_the_path_does_not_name_is_kept_and_shifted() -> None:
    carried = grouped("guide.md", "# Another Name\n\n## Run\n")
    assert carried.text == "# guide\n\n## Another Name\n\n### Run"
    assert carried.headings == ("guide", "Another Name", "Run")


def test_a_second_h1_leaves_the_title_unabsorbed() -> None:
    text = "# Guide\n\nOne.\n\n# Guide\n"
    assert grouped("guide.md", text).text == "# guide\n\n## Guide\n\nOne.\n\n## Guide"


def test_an_h1_that_is_not_the_first_heading_leaves_the_title_unabsorbed() -> None:
    text = "## Run\n\n# Guide\n"
    assert grouped("guide.md", text).text == "# guide\n\n### Run\n\n## Guide"


def test_a_container_nested_title_is_not_absorbed() -> None:
    assert absorbed(parse("> # Guide\n"), "guide") is None


def test_a_document_carrying_no_heading_keeps_its_file_heading_alone() -> None:
    assert grouped("guide.md", "Body only.\n").text == "# guide\n\nBody only."


def test_a_preamble_sits_after_the_file_heading_and_before_the_first_heading() -> None:
    text = "# Guide\n\nLead text.\n\n## Run\n"
    assert grouped("guide.md", text).text == "# guide\n\nLead text.\n\n## Run"


def test_a_blank_line_above_the_first_region_is_not_carried() -> None:
    assert grouped("guide.md", "\n\n# Guide\n\nBody.\n").text == "# guide\n\nBody."


def test_a_removed_reference_definition_leaves_no_blank_line_behind_it() -> None:
    text = "# Guide\n\n- [x] done\n\n[x]: page.md\n"
    assert grouped("guide.md", text).text == "# guide\n\n- [x] done"


def test_an_unused_reference_definition_is_removed_with_the_used_ones() -> None:
    text = "# Guide\n\nBody.\n\n[a]: one.md\n[b]: two.md\n"
    assert grouped("guide.md", text).text == "# guide\n\nBody."


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
    assert carried.text == f"# guide\n\n{written}"


def test_the_separation_between_two_regions_is_one_blank_line() -> None:
    text = "# Guide\n\nOne.\n\n\n\n\nTwo.\n"
    assert grouped("guide.md", text).text == "# guide\n\nOne.\n\nTwo."


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
    assert carried.text == f"# guide\n\n## Another Name\n\n{expected}"


def test_a_container_keeps_the_heading_like_text_a_code_example_holds() -> None:
    written = "> ```markdown\n> ## Not A Heading\n> ```"
    carried = grouped("guide.md", f"# Another Name\n\n{written}\n")
    assert carried.text == f"# guide\n\n## Another Name\n\n{written}"


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
    assert carried.text == f"# guide\n\n## Another Name\n\n{expected}"


def test_a_group_that_shifts_by_nothing_leaves_a_setext_heading_alone() -> None:
    carried = grouped("guide.md", "# Guide\n\nRun\n---\n")
    assert carried.text == "# guide\n\nRun\n---"


def test_a_converted_heading_keeps_a_number_sign_run_ending_its_text() -> None:
    carried = grouped("guide.md", "# Another Name\n\nSharp #\n---\n")
    assert carried.text == "# guide\n\n## Another Name\n\n### Sharp \\#"


def test_a_converted_heading_shows_the_text_its_source_lines_carried() -> None:
    carried = grouped("guide.md", "# Another Name\n\nRun\nand stop\n---\n")
    assert carried.headings == ("guide", "Another Name", "Run and stop")


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
    assert grouped("guide.md", text).text == "# guide\n\n###### Deep"


def test_a_bundle_ends_in_exactly_one_newline() -> None:
    bundled = assemble("Line.", [grouped("guide.md", "# Guide\n")])
    assert bundled == "Line.\n\n# guide\n"
