"""Assert what the scan removes and leaves, and what each heading is named.

A removal rule only ever observed removing is half tested, so each case
the contract excludes is here beside the cases it includes: an indented
delimiter, a delimiter carrying a trailing space, a TOML fence, JSON
metadata, a `---` under a blank line, a `---` inside a code fence and one
below the first line each leave the document exactly as the file holds
it. Every case states the content the scan returns and the line that
content begins on, because the coordinate is as much the result as the
text is.

The index is asserted on the same terms. A heading is written in each
syntax that carries one appearance — a code span, an emphasis
delimiter, a link label, an autolink, an entity, an image and a line
break — and the case states the one text a reader reads, because a
derivation reading bytes rather than events would differ on exactly
those. Each case is the text the renderer this profile tracks derives
for that heading. The ordinal cases state the count one document keeps,
the ordinal it passes over, and that a second document begins it again.
"""

import pytest

from prosiform.profile import parse
from prosiform.source import (
    MARK,
    Ambiguous,
    Heading,
    Nested,
    Source,
    Unterminated,
    Use,
    bare,
    content,
    decode,
    fragments,
    hashed,
    index,
    lines,
    nesting,
    occurrences,
    opening_heading,
    owner,
    regions,
    section,
    slug,
    uses,
    visible,
)

BODY = "An opening paragraph.\n\n## Run\n\nCarry the procedure out.\n"


def test_a_document_carrying_no_transport_metadata_is_its_own_content() -> None:
    assert content(BODY) == Source(BODY, 1)


def test_one_leading_mark_is_removed() -> None:
    assert content(MARK + BODY) == Source(BODY, 1)


def test_a_second_mark_is_content() -> None:
    assert content(MARK + MARK + BODY) == Source(MARK + BODY, 1)


def test_a_mark_shifts_no_coordinate() -> None:
    assert content(MARK + BODY).first_line == 1


def test_a_mark_elsewhere_in_the_document_is_content() -> None:
    carried = f"A paragraph carrying {MARK} inside it.\n"
    assert content(carried) == Source(carried, 1)


def test_a_block_closed_by_three_hyphens_is_removed() -> None:
    assert content(f"---\ntitle: Guide\n---\n{BODY}") == Source(BODY, 4)


def test_a_block_closed_by_three_dots_is_removed() -> None:
    assert content(f"---\ntitle: Guide\n...\n{BODY}") == Source(BODY, 4)


def test_a_mark_before_the_opener_is_removed_with_the_block() -> None:
    assert content(f"{MARK}---\ntitle: Guide\n---\n{BODY}") == Source(BODY, 4)


def test_crlf_terminated_delimiters_are_recognized_and_their_closer_removed() -> None:
    assert content(f"---\r\ntitle: Guide\r\n---\r\n{BODY}") == Source(BODY, 4)


def test_a_crlf_body_reaches_the_content_spelled_as_the_file_spells_it() -> None:
    assert content("---\ntitle: Guide\n---\r\nRun it.\r\n") == Source("Run it.\r\n", 4)


def test_an_empty_block_is_removed() -> None:
    assert content(f"---\n---\n{BODY}") == Source(BODY, 3)


def test_the_blank_lines_following_a_block_are_preserved() -> None:
    assert content(f"---\ntitle: Guide\n---\n\n\n{BODY}") == Source(f"\n\n{BODY}", 4)


def test_a_block_closing_on_the_last_line_leaves_no_content() -> None:
    assert content("---\ntitle: Guide\n---\n") == Source("", 4)


def test_a_block_whose_closer_carries_no_terminator_leaves_no_content() -> None:
    assert content("---\ntitle: Guide\n---") == Source("", 4)


def test_the_first_closing_delimiter_closes_the_block() -> None:
    assert content(f"---\na: 1\n---\n{BODY}---\n") == Source(f"{BODY}---\n", 4)


def test_the_body_after_a_removal_is_byte_identical_to_its_source() -> None:
    source = f"{MARK}---\ntitle: Guide\n---\n{BODY}"
    assert source.endswith(content(source).text)


@pytest.mark.parametrize(
    "opening",
    [
        " ---",
        "   ---",
        "\t---",
        "--- ",
        "---\t",
        "----",
        "--",
        "+++",
        "{",
        "***",
        "···",
    ],
)
def test_a_first_line_that_is_not_the_delimiter_opens_no_block(opening: str) -> None:
    source = f"{opening}\ntitle: Guide\n---\n{BODY}"
    assert content(source) == Source(source, 1)


def test_a_blank_line_before_the_delimiter_makes_it_body() -> None:
    source = f"\n---\n\n{BODY}"
    assert content(source) == Source(source, 1)


def test_a_yaml_example_inside_a_code_block_is_content() -> None:
    source = f"# Guide\n\n```yaml\n---\ntitle: Guide\n---\n```\n\n{BODY}"
    assert content(source) == Source(source, 1)


def test_a_thematic_break_below_the_first_line_is_content() -> None:
    source = f"# Guide\n\n---\n\n{BODY}"
    assert content(source) == Source(source, 1)


def test_an_empty_document_opens_no_block() -> None:
    assert content("") == Source("", 1)


@pytest.mark.parametrize(
    "source",
    [
        "---\ntitle: Guide\n",
        "---\n",
        "---",
        "---\ntitle: Guide\n ---\n",
        "---\ntitle: Guide\n--- \n",
        "---\ntitle: Guide\n....\n",
    ],
)
def test_a_recognized_opener_with_no_closer_fails(source: str) -> None:
    with pytest.raises(Unterminated) as raised:
        content(source)
    assert raised.value.line == 1


def test_the_recorded_line_maps_a_parsed_location_to_the_file() -> None:
    source = content(f"---\ntitle: Guide\n---\n{BODY}")
    assert source.line(1) == 4
    assert source.line(3) == 6
    assert source.line(None) is None


def test_an_unstripped_source_maps_each_location_to_itself() -> None:
    assert content(BODY).line(3) == 3


@pytest.mark.parametrize(
    ("text", "counted"),
    [
        ("a\nb\n", 2),
        ("a\nb", 2),
        ("", 0),
        ("\n", 1),
        ("a\r\nb\r\n", 2),
        ("a\x0cb\n", 1),
        ("a b\n", 1),
    ],
)
def test_a_line_ends_at_a_line_feed_and_nowhere_else(text: str, counted: int) -> None:
    assert len(lines(text)) == counted
    assert "".join(lines(text)) == text


@pytest.mark.parametrize(
    ("physical", "written"),
    [("---\n", "---"), ("---\r\n", "---"), ("---", "---"), ("---\r", "---")],
)
def test_a_line_is_compared_without_its_terminator(physical: str, written: str) -> None:
    assert bare(physical) == written


def test_valid_utf8_decodes_to_the_text_it_encodes() -> None:
    assert decode("Lire la procédure.\n".encode()) == "Lire la procédure.\n"


def test_a_mark_decodes_to_one_character() -> None:
    assert decode(b"\xef\xbb\xbf# Guide\n") == f"{MARK}# Guide\n"


@pytest.mark.parametrize(
    "data",
    [b"# Guide\n\n\xe9\n", b"\xff\xfe# Guide\n", b"\xc3", b"\xed\xa0\x80"],
)
def test_bytes_that_are_not_valid_utf8_fail_rather_than_decoding(data: bytes) -> None:
    with pytest.raises(UnicodeDecodeError):
        decode(data)


def indexed(text: str) -> tuple[Heading, ...]:
    """The heading index of one complete source document."""
    return index(parse(text))


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("guide", "guide"),
        ("Guide", "guide"),
        ("docs/note", "docsnote"),
        ("modes/plan-mode", "modesplan-mode"),
        ("Plan Mode", "plan-mode"),
        ("plan_[v2]", "plan_v2"),
        ("A Title: Two Parts", "a-title-two-parts"),
        ("What's new: v1.0!", "whats-new-v10"),
        ("Café Münster", "café-münster"),
        ("Two  spaces", "two--spaces"),
    ],
)
def test_a_fragment_is_the_slug_a_renderer_generates(text: str, expected: str) -> None:
    assert slug(text) == expected


def test_a_slug_an_earlier_heading_took_carries_the_renderer_ordinal() -> None:
    assert fragments(["Run", "Run", "Stop", "Run"]) == [
        "run",
        "run-1",
        "stop",
        "run-2",
    ]


def test_an_ordinal_a_heading_already_carries_is_passed_over() -> None:
    assert fragments(["Run", "Run-1", "Run", "Run", "Run-1"]) == [
        "run",
        "run-1",
        "run-2",
        "run-3",
        "run-1-1",
    ]


def test_the_ordinal_count_belongs_to_the_sequence_it_was_begun_on() -> None:
    assert fragments(["Run"]) == fragments(["Run"]) == ["run"]


@pytest.mark.parametrize(
    ("heading", "expected"),
    [
        ("# Run the procedure", "Run the procedure"),
        ("# A `code` span", "A code span"),
        ("# **Bold** and _thin_", "Bold and thin"),
        ("# ~~Struck~~ through", "Struck through"),
        ("# A [label](guide.md) names it", "A label names it"),
        ("# Caf&eacute; Münster", "Café Münster"),
        ("# &#x263A; and &amp;", "☺ and &"),
        ("# An ![A diagram](plan.png) overview", "An  overview"),
        ("# <https://example.com/a> names it", "https://example.com/a names it"),
        ("Run\nthe procedure\n===\n", "Run\nthe procedure"),
    ],
)
def test_a_heading_shows_the_text_its_events_carry(heading: str, expected: str) -> None:
    assert [one.text for one in indexed(heading)] == [expected]


def test_a_heading_index_carries_each_heading_in_source_order() -> None:
    carried = indexed("# Guide\n\n## Run\n\n### Detail\n\n## Stop\n")
    assert [(one.level, one.text) for one in carried] == [
        (1, "Guide"),
        (2, "Run"),
        (3, "Detail"),
        (2, "Stop"),
    ]


def test_a_container_nested_heading_is_indexed_with_the_rest() -> None:
    carried = indexed("# Guide\n\n> ## Quoted\n\n- ### Listed\n\n## Run\n")
    assert [one.text for one in carried] == ["Guide", "Quoted", "Listed", "Run"]


def test_a_heading_takes_the_slug_its_own_text_produces() -> None:
    carried = indexed("# Run\n\n> ## Run\n\n## Run\n")
    assert [one.fragment for one in carried] == ["run", "run", "run"]


def test_a_heading_carries_the_line_of_the_content_it_opens_on() -> None:
    carried = indexed("An opening paragraph.\n\n## Run\n")
    assert [one.line for one in carried] == [3]


def test_a_setext_heading_is_indexed_at_the_level_it_opens() -> None:
    carried = indexed("Guide\n=====\n\nRun\n---\n")
    assert [(one.level, one.fragment) for one in carried] == [(1, "guide"), (2, "run")]


def test_a_document_carrying_no_heading_indexes_nothing() -> None:
    assert indexed("An opening paragraph.\n") == ()


def test_a_heading_spelling_an_ordinal_takes_the_slug_of_that_text() -> None:
    carried = indexed("## Run\n\n## Run 1\n")
    assert [one.fragment for one in carried] == ["run", "run-1"]


def spans(text: str, fragment: str) -> list[str] | None:
    """The type of each region one fragment selects from a source."""
    found = section(parse(text), fragment)
    return None if found is None else [token.type for token in found]


def test_a_container_is_one_region_and_what_it_holds_opens_none() -> None:
    text = "# Guide\n\n> ## Nested\n>\n> Inside.\n\nAfter.\n"
    opened = [token.type for token in regions(parse(text))]
    assert opened == ["heading_open", "blockquote_open", "paragraph_open"]


def test_a_section_runs_to_the_next_heading_of_equal_level() -> None:
    text = "## Run\n\nDo it.\n\n## Stop\n\nStop it.\n"
    assert spans(text, "run") == ["heading_open", "paragraph_open"]


def test_a_section_runs_to_the_next_heading_of_higher_level() -> None:
    text = "## Run\n\nDo it.\n\n# Guide\n\nAbout it.\n"
    assert spans(text, "run") == ["heading_open", "paragraph_open"]


def test_a_section_carries_the_deeper_headings_beneath_it() -> None:
    text = "## Run\n\nDo it.\n\n### Detail\n\nThe detail.\n\n## Stop\n"
    assert spans(text, "run") == [
        "heading_open",
        "paragraph_open",
        "heading_open",
        "paragraph_open",
    ]


def test_a_section_the_document_outlasts_runs_to_its_end() -> None:
    text = "## Run\n\nDo it.\n\n### Detail\n\nThe detail.\n"
    assert spans(text, "run") == [
        "heading_open",
        "paragraph_open",
        "heading_open",
        "paragraph_open",
    ]


def test_a_heading_a_blockquote_carries_ends_no_section() -> None:
    text = "## Run\n\n> ## Quoted\n>\n> Inside.\n\n## Stop\n"
    assert spans(text, "run") == ["heading_open", "blockquote_open"]


def test_a_heading_a_list_item_carries_ends_no_section() -> None:
    text = "## Run\n\n- ## Listed\n\n## Stop\n"
    assert spans(text, "run") == ["heading_open", "bullet_list_open"]


def test_heading_like_text_in_a_fence_ends_no_section() -> None:
    text = "## Run\n\n```\n## Not a heading\n```\n\n## Stop\n"
    assert spans(text, "run") == ["heading_open", "fence"]


def test_a_fragment_naming_a_container_nested_heading_roots_no_section() -> None:
    text = "## Run\n\n> ## Quoted\n>\n> Inside.\n"
    with pytest.raises(Nested) as refused:
        section(parse(text), "quoted")
    assert refused.value.fragment == "quoted"


def test_a_fragment_naming_no_heading_of_the_document_selects_nothing() -> None:
    assert section(parse("## Run\n\nDo it.\n"), "stop") is None


def test_heading_like_text_in_a_fence_names_no_section() -> None:
    assert section(parse("## Run\n\n```\n## Stop\n```\n"), "stop") is None


def test_a_setext_heading_roots_a_section() -> None:
    text = "Run\n---\n\nDo it.\n\nStop\n----\n"
    assert spans(text, "run") == ["heading_open", "paragraph_open"]


def test_a_fragment_two_headings_of_one_source_produce_names_neither() -> None:
    text = "## Run\n\nFirst.\n\n## Run\n\nSecond.\n"
    with pytest.raises(Ambiguous) as refused:
        section(parse(text), "run")
    assert refused.value.fragment == "run"
    assert refused.value.lines == (1, 5)


def test_an_ordinal_names_no_heading_of_a_source() -> None:
    text = "## Run\n\nFirst.\n\n## Run\n\nSecond.\n"
    assert section(parse(text), "run-1") is None


def test_an_ambiguity_is_reported_before_a_nested_target() -> None:
    text = "## Run\n\nFirst.\n\n> ## Run\n>\n> Quoted.\n"
    with pytest.raises(Ambiguous):
        section(parse(text), "run")


def selected(text: str) -> list[Use]:
    """Every reference use the whole of one document carries."""
    tokens = parse(text)
    return list(uses(tokens, list(regions(tokens))))


def test_a_link_is_read_as_its_destination_and_its_opening_text() -> None:
    found = selected("[¬ the rules](rules.md)\n")
    assert [(one.destination, one.opening) for one in found] == [
        ("rules.md", "¬ the rules")
    ]


def test_an_apparent_link_inside_a_code_span_is_no_link() -> None:
    assert selected("A `[¬ the rules](rules.md)` example.\n") == []


def test_an_apparent_link_inside_a_code_block_is_no_link() -> None:
    assert selected("~~~\n[¬ the rules](rules.md)\n~~~\n") == []


def test_an_image_is_a_use_naming_a_resource() -> None:
    found = selected("![a diagram](diagram.png)\n")
    assert [(one.destination, one.opening, one.resource) for one in found] == [
        ("diagram.png", "a diagram", True)
    ]


def test_a_link_is_no_resource_use() -> None:
    assert selected("[¬ the rules](rules.md)\n")[0].resource is False


def test_an_image_opens_with_its_alternative_content_s_first_text() -> None:
    found = selected("![¬ the architecture](plan.png)\n")
    assert found[0].opening == "¬ the architecture"


def test_an_image_opening_on_a_link_opens_with_nothing() -> None:
    found = selected("![[¬ the rules](rules.md) shown](plan.png)\n")
    assert [(one.destination, one.opening) for one in found] == [("plan.png", "")]


def test_an_apparent_image_inside_a_code_span_is_no_use() -> None:
    assert selected("A `![a diagram](diagram.png)` example.\n") == []


def test_a_link_a_container_carries_is_one_of_its_region_s_links() -> None:
    found = selected("> Quoting [¬ the rules](rules.md).\n")
    assert [one.destination for one in found] == ["rules.md"]


def test_a_link_whose_text_opens_on_markup_opens_with_nothing() -> None:
    assert selected("[**bold**](rules.md)\n")[0].opening == ""


def test_a_link_is_located_at_the_line_its_block_opens_on() -> None:
    assert selected("# Guide\n\nSee [¬ the rules](rules.md).\n")[0].line == 3


def test_a_link_outside_the_given_regions_is_not_reported() -> None:
    text = "# One\n\nSee [¬ a](a.md).\n\n# Two\n\nSee [¬ b](b.md).\n"
    tokens = parse(text)
    chosen = section(tokens, "two")
    assert chosen is not None
    assert [one.destination for one in uses(tokens, chosen)] == ["b.md"]


def test_a_position_above_the_first_section_root_belongs_to_the_document() -> None:
    tokens = parse("A preamble line.\n\n# Guide\n\nGuide body.\n")
    assert owner(tokens, 0) is None


def test_a_position_inside_a_section_belongs_to_that_section() -> None:
    tokens = parse("# Guide\n\n## Alpha\n\nAlpha body.\n")
    holder = owner(tokens, 4)
    assert holder is not None
    assert visible(tokens[tokens.index(holder) + 1]) == "Alpha"


def test_a_position_belongs_to_the_innermost_section_containing_it() -> None:
    tokens = parse("# Guide\n\n## Alpha\n\n### Detail\n\nDetail body.\n")
    holder = owner(tokens, 6)
    assert holder is not None
    assert visible(tokens[tokens.index(holder) + 1]) == "Detail"


def test_a_position_inside_a_container_belongs_to_the_section_holding_it() -> None:
    tokens = parse("# Guide\n\n## Alpha\n\n> - Quoted body.\n")
    holder = owner(tokens, 4)
    assert holder is not None
    assert visible(tokens[tokens.index(holder) + 1]) == "Alpha"


def test_a_heading_a_container_carries_roots_no_section_to_own_by() -> None:
    tokens = parse("# Guide\n\n> ## Quoted\n>\n> Quoted body.\n")
    holder = owner(tokens, 4)
    assert holder is not None
    assert visible(tokens[tokens.index(holder) + 1]) == "Guide"


def test_a_document_nesting_no_container_nests_nothing() -> None:
    assert nesting(parse("# Guide\n\nGuide body.\n")) == 0


def test_container_nesting_counts_block_quotes_and_list_items() -> None:
    assert nesting(parse("> > > deep\n")) == 3
    assert nesting(parse("- a\n  - b\n    - c\n")) == 3
    assert nesting(parse("> - quoted item\n")) == 2


def test_container_nesting_is_the_deepest_run_rather_than_the_last() -> None:
    assert nesting(parse("> > deep\n\nshallow\n")) == 2


def test_link_and_image_uses_are_counted_once_per_occurrence() -> None:
    tokens = parse("# Guide\n\n[a](a.md) and [a](a.md) and ![p](p.png).\n")
    assert occurrences(tokens, tuple(regions(tokens))) == 3


def test_a_use_outside_the_given_regions_is_not_counted() -> None:
    text = "# One\n\n[a](a.md)\n\n# Two\n\n[b](b.md)\n"
    tokens = parse(text)
    chosen = section(tokens, "two")
    assert chosen is not None
    assert occurrences(tokens, chosen) == 1


def test_a_document_opening_on_a_top_level_heading_names_it() -> None:
    first = opening_heading(parse("# docs/guide\n\nBody.\n\n# Later\n"))
    assert first is not None
    assert first.text == "docs/guide"
    assert first.line == 1


def test_a_document_whose_first_heading_is_deeper_opens_on_none() -> None:
    assert opening_heading(parse("## Guide\n\nBody.\n\n# Later\n")) is None


def test_a_top_level_heading_a_container_carries_opens_no_document() -> None:
    assert opening_heading(parse("> # Guide\n\nBody.\n")) is None


def test_a_document_carrying_no_heading_opens_on_none() -> None:
    assert opening_heading(parse("Body with no heading.\n")) is None


def test_a_heading_the_document_reaches_after_prose_is_still_its_first() -> None:
    first = opening_heading(parse("An entry line.\n\n# notes\n\nBody.\n"))
    assert first is not None
    assert first.text == "notes"
    assert first.line == 3


def test_a_heading_like_line_inside_code_is_no_heading() -> None:
    assert opening_heading(parse("    # notes\n")) is None
    assert opening_heading(parse("~~~text\n# notes\n~~~\n")) is None


def test_a_content_hash_is_taken_over_the_bytes_the_file_held() -> None:
    assert hashed(b"# Guide\n") == hashed(b"# Guide\n")
    assert hashed(b"# Guide\n") != hashed(b"# Guide\r\n")
    assert len(hashed(b"")) == 64
