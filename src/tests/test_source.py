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
from markdown_it.token import Token

from prosiform import source as source_module
from prosiform.profile import parse
from prosiform.source import (
    MARK,
    Ambiguous,
    Diagram,
    Heading,
    Nested,
    Source,
    Unterminated,
    Use,
    bare,
    clicks,
    content,
    decode,
    diagram_type,
    fragments,
    hashed,
    index,
    lines,
    linking,
    nesting,
    occurrences,
    regions,
    section,
    slug,
    uses,
    within,
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


DIAGRAM = (
    "# Lifecycle\n"
    "\n"
    "```mermaid\n"
    "flowchart LR\n"
    "    Open --> Closed\n"
    '    click Open href "states/open.md"\n'
    '    click Closed "states/closed.md"\n'
    "```\n"
)


def test_a_diagram_href_click_is_a_use_on_the_line_it_is_written() -> None:
    found = selected(DIAGRAM)
    assert (found[0].destination, found[0].line) == ("states/open.md", 6)


def test_a_diagram_short_click_is_a_use_on_the_line_it_is_written() -> None:
    found = selected(DIAGRAM)
    assert (found[1].destination, found[1].line) == ("states/closed.md", 7)


def test_each_diagram_click_is_one_link_use_opening_with_nothing() -> None:
    assert [(one.opening, one.resource) for one in selected(DIAGRAM)] == [
        ("", False),
        ("", False),
    ]


@pytest.mark.parametrize(
    "written",
    [
        'click A href "a.md" "the tooltip"',
        'click A href "a.md" "the tooltip" _blank',
        'click A href "a.md" _self',
        'click A "a.md" "the tooltip" _parent',
        'click A "a.md" _top',
        'click A "a.md";',
    ],
)
def test_a_click_s_trailing_tooltip_and_target_leave_its_destination(
    written: str,
) -> None:
    found = selected(f"```mermaid\nflowchart LR\n    {written}\n```\n")
    assert [(one.destination, one.line) for one in found] == [("a.md", 3)]


@pytest.mark.parametrize(
    "written",
    [
        'click A callback "the tooltip"',
        "click A callback",
        'click A call callback("a.md")',
        'click A href "a.md" trailing',
        "A --> B[\"click A href 'a.md'\"]",
    ],
)
def test_a_line_naming_no_click_destination_is_no_use(written: str) -> None:
    assert selected(f"```mermaid\nflowchart LR\n    {written}\n```\n") == []


@pytest.mark.parametrize("info", ["", "text", "mermaid-like", "graph"])
def test_a_click_in_a_fence_holding_no_diagram_is_no_use(info: str) -> None:
    assert selected(f'```{info}\nclick A href "a.md"\n```\n') == []


def test_a_diagram_fence_reads_its_info_string_s_first_word() -> None:
    found = selected('~~~ mermaid title\nflowchart LR\nclick A "a.md"\n~~~\n')
    assert [one.destination for one in found] == ["a.md"]


def test_a_click_offset_spans_its_destination_in_the_fence_line() -> None:
    tokens = parse('- item\n\n  ```mermaid\n  click A href "a.md" "tip"\n  ```\n')
    fence = next(token for token in tokens if token.type == "fence")
    [click] = list(clicks(fence))
    written = fence.content.splitlines()[0]
    assert click.line == 4
    assert written[click.offset : click.offset + len(click.destination)] == "a.md"


def diagram_links(written: str, kind: str = "flowchart LR") -> list[tuple[str, int]]:
    """Each destination one diagram line names, with its offset in that line."""
    fence = next(
        token
        for token in parse(f"```mermaid\n{kind}\n{written}\n```\n")
        if token.type == "fence"
    )
    return [(click.destination, click.offset) for click in clicks(fence)]


@pytest.mark.parametrize(
    "written",
    [
        'link Cls "a.md"',
        'link Cls "a.md" "the tooltip"',
        'link Cls "a.md" "the tooltip" _blank',
        'link Cls "a.md" _self',
        'link Cls "a.md";',
    ],
)
def test_a_class_link_names_its_quoted_destination(written: str) -> None:
    assert diagram_links(written, "classDiagram") == [("a.md", 10)]


@pytest.mark.parametrize(
    ("written", "kind"),
    [
        ('Click A HREF "a.md"', "flowchart LR"),
        ('CLICK A "a.md" "the tooltip" _BLANK', "stateDiagram-v2"),
        ('cLiCk A hReF "a.md"', "gantt"),
        ('LINK A "a.md"', "classDiagram"),
        ('Link A "a.md" _Self', "classDiagram"),
    ],
)
def test_a_diagram_link_keyword_matches_in_any_case(written: str, kind: str) -> None:
    assert [one for one, _at in diagram_links(written, kind)] == ["a.md"]


def test_a_class_link_takes_no_href() -> None:
    assert diagram_links('link Cls href "a.md"', "classDiagram") == []


@pytest.mark.parametrize(
    ("written", "destination"),
    [
        ("link Alice: Spec @ docs/spec.md", "docs/spec.md"),
        ("link Alice: Spec @docs/spec.md   ", "docs/spec.md"),
        ("LINK Alice: Spec @ docs/spec.md;", "docs/spec.md"),
        ("link Alice: Spec @ docs/a@b.md", "docs/a@b.md"),
        ("Link Alice Smith: The spec @ docs/spec.md", "docs/spec.md"),
    ],
)
def test_a_sequence_menu_entry_names_the_text_after_its_first_at(
    written: str, destination: str
) -> None:
    [(found, at)] = diagram_links(written, "sequenceDiagram")
    assert found == destination
    assert written[at : at + len(found)] == destination


def test_a_sequence_menu_line_names_each_string_value_in_written_order() -> None:
    written = 'links Alice: {"Spec": "docs/spec.md", "Notes":"docs/notes.md"}'
    found = diagram_links(written, "sequenceDiagram")
    assert [one for one, _at in found] == ["docs/spec.md", "docs/notes.md"]
    assert [written[at : at + len(one)] for one, at in found] == [
        "docs/spec.md",
        "docs/notes.md",
    ]


def test_a_sequence_menu_line_keyword_matches_in_any_case() -> None:
    written = 'LINKS Alice: {"Spec": "docs/spec.md"};'
    found = diagram_links(written, "sequenceDiagram")
    assert [one for one, _at in found] == ["docs/spec.md"]


@pytest.mark.parametrize(
    "written",
    [
        'links Alice: ["docs/spec.md"]',
        'links Alice: "docs/spec.md"',
        'links Alice: {"Spec": "docs/spec.md"',
        'links Alice: {"Spec": "docs/spec.md"} trailing',
        "links Alice: docs/spec.md",
    ],
)
def test_a_sequence_menu_line_holding_no_json_object_names_nothing(
    written: str,
) -> None:
    assert diagram_links(written, "sequenceDiagram") == []


def test_a_sequence_menu_value_holding_an_escape_names_nothing() -> None:
    written = 'links Alice: {"Spec": "docs\\/spec.md", "Notes": "docs/notes.md"}'
    found = diagram_links(written, "sequenceDiagram")
    assert [one for one, _at in found] == ["docs/notes.md"]


def diagram_read(written: str, kind: str = "sequenceDiagram") -> Diagram:
    """What one diagram line of one diagram type links to."""
    fence = next(
        token
        for token in parse(f"```mermaid\n{kind}\n{written}\n```\n")
        if token.type == "fence"
    )
    return linking(fence)


@pytest.mark.parametrize(
    "written",
    [
        'links Alice: {"Count": 2, "Spec": "s.md"}',
        'links Alice: {"Spec": "s.md", "Nested": {"a": "x.md"}}',
        'links Alice: {"Spec": null}',
        'links Alice: {"Spec": "s.md", "Spec": ["s.md"]}',
    ],
)
def test_a_sequence_menu_value_that_is_no_string_breaks_its_line(
    written: str,
) -> None:
    read = diagram_read(written)
    assert read.clicks == ()
    assert read.broken == (3,)


def test_a_value_no_string_a_later_key_replaces_breaks_nothing() -> None:
    written = 'links Alice: {"Spec": 2, "Spec": {"a": [1, "}"]}, "Spec": "s.md"}'
    read = diagram_read(written)
    assert [(one.destination, one.offset) for one in read.clicks] == [
        ("s.md", written.index("s.md"))
    ]
    assert read.broken == ()


def test_a_repeated_menu_key_names_its_last_value_alone() -> None:
    written = 'links Alice: {"Spec": "a.md", "Notes": "n.md", "Spec": "b.md"}'
    found = diagram_links(written, "sequenceDiagram")
    assert found == [("n.md", written.index("n.md")), ("b.md", written.index("b.md"))]


def test_a_repeated_menu_key_whose_last_value_holds_an_escape_names_nothing() -> None:
    written = 'links Alice: {"Spec": "a.md", "Spec": "b\\/c.md"}'
    assert diagram_links(written, "sequenceDiagram") == []


def test_a_menu_constant_json_parse_refuses_names_nothing() -> None:
    read = diagram_read('links Alice: {"Spec": NaN}')
    assert read == Diagram()


@pytest.mark.parametrize(
    ("written", "destination", "kept"),
    [
        ("link Alice: Spec @ a.md;b.md", "a.md", ";b.md"),
        ("link Alice: Spec @ a.md ; ", "a.md", " ; "),
        ("link Alice: Spec @ a.md # a comment", "a.md", " # a comment"),
        ("link Alice: Spec @ a.md#intro", "a.md", "#intro"),
        ("link Alice: Spec @ a.md#35;intro", "a.md#intro", ""),
        ("link Alice: Spec @ #35;intro;x.md", "#intro", ";x.md"),
    ],
)
def test_a_sequence_menu_entry_ends_where_mermaid_ends_its_statement(
    written: str, destination: str, kept: str
) -> None:
    [click] = diagram_read(written).clicks
    assert click.destination == destination
    assert written[click.offset + len(click.written) :] == kept


def test_a_sequence_menu_entry_whose_at_follows_its_end_names_nothing() -> None:
    assert diagram_links("link Alice: Spec; @ a.md", "sequenceDiagram") == []
    assert diagram_links("link Alice: Spec # @ a.md", "sequenceDiagram") == []
    assert diagram_links("link Alice: Spec @ ;a.md", "sequenceDiagram") == []


def test_a_sequence_menu_line_ends_where_mermaid_ends_its_statement() -> None:
    written = 'links Alice: {"Spec": "a.md#35;intro"}; links Bob: {"B": "b.md"}'
    [click] = diagram_read(written).clicks
    assert (click.destination, click.written) == ("a.md#intro", "a.md#35;intro")
    assert diagram_links('links Alice: {"Spec": "a.md;b.md"}', "sequenceDiagram") == []
    assert diagram_links('links Alice: {"Spec": "a.md#b"}', "sequenceDiagram") == []


@pytest.mark.parametrize(
    ("written", "kind"),
    [
        ("link --> done : retry @ ops.md", "stateDiagram-v2"),
        ("link A: label @ ops.md", "flowchart LR"),
        ('links A: {"Ops": "ops.md"}', "classDiagram"),
        ("link A: label @ ops.md", "classDiagram"),
        ('link Cls "a.md"', "sequenceDiagram"),
        ('link Cls "a.md"', "flowchart LR"),
        ('link Cls "a.md"', "stateDiagram-v2"),
    ],
)
def test_a_link_form_is_read_in_its_own_diagram_alone(written: str, kind: str) -> None:
    assert diagram_links(written, kind) == []


@pytest.mark.parametrize(
    ("content", "kind"),
    [
        ("classDiagram\n", "classDiagram"),
        ("classDiagram-v2\n", "classDiagram"),
        ("  sequenceDiagram\n", "sequenceDiagram"),
        ("---\ntitle: Exchange\n---\nsequenceDiagram\n", "sequenceDiagram"),
        ("%%{init: {'theme': 'dark'}}%%\nclassDiagram\n", "classDiagram"),
        ("%% a comment\n%% another\nsequenceDiagram\n", "sequenceDiagram"),
        ("\n\nsequenceDiagram\n", "sequenceDiagram"),
        ("flowchart LR\n", ""),
        ("stateDiagram-v2\n", ""),
        ("title sequenceDiagram\n", ""),
    ],
)
def test_a_diagram_type_is_read_as_mermaid_detects_it(content: str, kind: str) -> None:
    assert diagram_type(content) == kind


def test_a_sequence_diagram_under_front_matter_reads_its_menu() -> None:
    text = "---\ntitle: Exchange\n---\nsequenceDiagram\nlink A: Spec @ s.md\n"
    fence = next(
        token for token in parse(f"```mermaid\n{text}```\n") if token.type == "fence"
    )
    assert [(one.destination, one.line) for one in clicks(fence)] == [("s.md", 6)]


def test_a_menu_line_is_json_decoded_once_per_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    decode = source_module.decoded

    def counted(text: str) -> object:
        calls.append(text)
        return decode(text)

    monkeypatch.setattr(source_module, "decoded", counted)
    read = diagram_read('links Alice: {"A": "a.md", "B": "b.md", "A": "c.md"}')
    assert len(read.clicks) == 2
    assert len(calls) == 1


def test_a_fence_s_diagram_is_read_once_however_often_it_is_asked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[int] = []
    read = source_module.read_diagram

    def counted(fence: Token) -> Diagram:
        calls.append(id(fence))
        return read(fence)

    monkeypatch.setattr(source_module, "read_diagram", counted)
    text = '```mermaid\nsequenceDiagram\nlinks A: {"A": "a.md"}\n```\n'
    tokens = parse(text)
    for _ in range(3):
        assert [one.destination for one in uses(tokens, list(regions(tokens)))] == [
            "a.md"
        ]
    assert occurrences(tokens, list(regions(tokens))) == 1
    assert len(calls) == 1


@pytest.mark.parametrize(
    ("written", "kind", "anchor"),
    [
        ('click A href "a.md"', "flowchart LR", "#"),
        ('link Cls "a.md"', "classDiagram", "#"),
        ("link Alice: Spec @ a.md", "sequenceDiagram", "#35;"),
        ('links Alice: {"Spec": "a.md", "Notes": "b.md"}', "sequenceDiagram", "#35;"),
    ],
)
def test_each_diagram_link_form_spells_its_anchor(
    written: str, kind: str, anchor: str
) -> None:
    fence = next(
        token
        for token in parse(f"```mermaid\n{kind}\n{written}\n```\n")
        if token.type == "fence"
    )
    found = list(clicks(fence))
    assert found
    assert {click.anchor for click in found} == {anchor}


def test_each_sequence_menu_destination_is_one_use_on_its_line() -> None:
    text = (
        "```mermaid\n"
        "sequenceDiagram\n"
        "link Alice: Spec @ spec.md\n"
        'links Bob: {"A": "a.md", "B": "b.md"}\n'
        "```\n"
    )
    assert [(one.destination, one.line) for one in selected(text)] == [
        ("spec.md", 3),
        ("a.md", 4),
        ("b.md", 4),
    ]
    tokens = parse(text)
    assert occurrences(tokens, list(regions(tokens))) == 3


def test_diagram_and_inline_uses_arrive_in_source_order() -> None:
    text = '[a](a.md)\n\n```mermaid\nclick A "b.md"\n```\n\n[c](c.md)\n'
    assert [one.destination for one in selected(text)] == ["a.md", "b.md", "c.md"]


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
    assert found[0].destination == "plan.png"
    assert found[0].opening == ""


def test_a_link_inside_image_alternative_content_is_a_use_of_its_own() -> None:
    found = selected("A picture ![of the [¬ rules](rules.md) it names](plan.png).\n")
    assert [(one.destination, one.opening, one.resource) for one in found] == [
        ("plan.png", "of the ", True),
        ("rules.md", "¬ rules", False),
    ]


def test_an_image_inside_image_alternative_content_is_a_use_of_its_own() -> None:
    found = selected("![a ![inner](inner.png) outer](plan.png)\n")
    assert [(one.destination, one.resource) for one in found] == [
        ("plan.png", True),
        ("inner.png", True),
    ]


def test_a_link_inside_image_alternative_content_is_located_at_its_block() -> None:
    text = "# Guide\n\nA picture ![of the [¬ rules](rules.md) it names](plan.png).\n"
    assert selected(text)[1].line == 3


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


def test_a_use_inside_image_alternative_content_is_counted() -> None:
    text = "# Guide\n\nA picture ![of the [¬ rules](rules.md) it names](plan.png).\n"
    assert occurrences(parse(text), tuple(regions(parse(text)))) == 2


def test_each_diagram_click_is_counted_once_per_occurrence() -> None:
    tokens = parse(DIAGRAM + "\nSee [open](states/open.md).\n")
    assert occurrences(tokens, tuple(regions(tokens))) == 3


def test_a_diagram_click_outside_the_given_regions_is_not_counted() -> None:
    text = '# One\n\n```mermaid\nclick A "a.md"\n```\n\n# Two\n\nPlain.\n'
    tokens = parse(text)
    chosen = section(tokens, "two")
    assert chosen is not None
    assert occurrences(tokens, chosen) == 0


def test_a_use_outside_the_given_regions_is_not_counted() -> None:
    text = "# One\n\n[a](a.md)\n\n# Two\n\n[b](b.md)\n"
    tokens = parse(text)
    chosen = section(tokens, "two")
    assert chosen is not None
    assert occurrences(tokens, chosen) == 1


def test_the_tokens_within_the_given_regions_exclude_the_rest() -> None:
    text = "# One\n\n<div>raw</div>\n\n# Two\n\nPlain.\n"
    tokens = parse(text)
    chosen = section(tokens, "two")
    assert chosen is not None
    assert "html_block" not in [token.type for token in within(tokens, chosen)]
    assert "html_block" in [token.type for token in within(tokens, list(tokens))]


def test_a_container_and_what_it_holds_are_within_one_region() -> None:
    tokens = parse("# One\n\n> - held\n")
    chosen = section(tokens, "one")
    assert chosen is not None
    held = [token.type for token in within(tokens, chosen)]
    assert "blockquote_open" in held
    assert "list_item_open" in held


def test_a_content_hash_is_taken_over_the_bytes_the_file_held() -> None:
    assert hashed(b"# Guide\n") == hashed(b"# Guide\n")
    assert hashed(b"# Guide\n") != hashed(b"# Guide\r\n")
    assert len(hashed(b"")) == 64


def unfollowed(content: str) -> list[tuple[str, str, int]]:
    """Each link one diagram renders that no diagram link line writes."""
    fence = next(
        token
        for token in parse(f"```mermaid\n{content}```\n")
        if token.type == "fence"
    )
    return [
        (one.form, one.destination, one.line) for one in linking(fence).unfollowed
    ]


KANBAN_TICKET = "Kanban ticket's link"
LABEL_ANCHOR = "HTML anchor in a node label"


def test_a_kanban_ticket_renders_the_link_its_front_matter_base_builds() -> None:
    content = (
        "---\nconfig:\n  kanban:\n    ticketBaseUrl: 'people/#TICKET#.md'\n---\n"
        "kanban\n  Todo\n    [Write]@{ ticket: user, priority: 'High' }\n"
    )
    assert unfollowed(content) == [(KANBAN_TICKET, "people/user.md", 9)]


def test_a_kanban_ticket_renders_the_link_an_init_directive_base_builds() -> None:
    content = (
        "---\nconfig:\n  kanban:\n    ticketBaseUrl: 'people/#TICKET#.md'\n---\n"
        "%%{init: {'kanban': {'ticketBaseUrl': 'https://t.example/#TICKET#'}}}%%\n"
        "kanban\n  Todo\n    [Write]@{ ticket: MC-1 }\n"
    )
    assert unfollowed(content) == [(KANBAN_TICKET, "https://t.example/MC-1", 10)]


@pytest.mark.parametrize(
    "content",
    [
        "kanban\n  Todo\n    [Write]@{ ticket: user }\n",
        "---\nconfig:\n  kanban:\n    ticketBaseUrl: 'p/#TICKET#.md'\n---\n"
        "kanban\n  Todo\n    [Write]@{ priority: 'High' }\n",
        "---\nconfig:\n  kanban:\n    ticketBaseUrl: 'p/#TICKET#.md'\n---\n"
        "flowchart LR\n  A[Write]@{ ticket: user }\n",
    ],
)
def test_a_ticket_with_no_base_or_outside_a_kanban_renders_no_link(
    content: str,
) -> None:
    assert unfollowed(content) == []


@pytest.mark.parametrize(
    ("written", "destination"),
    [
        ("A[\"<a href='people/user.md'>User</a>\"] --> B", "people/user.md"),
        ('A[<a href="people/user.md">User</a>] --> B', "people/user.md"),
        ('A["<A class=x HREF=people/user.md>User</A>"]', "people/user.md"),
    ],
)
def test_an_html_anchor_in_a_node_label_renders_its_href(
    written: str, destination: str
) -> None:
    content = f"flowchart LR\n{written}\n"
    assert unfollowed(content) == [(LABEL_ANCHOR, destination, 3)]


def test_an_html_anchor_in_a_comment_renders_nothing() -> None:
    assert unfollowed("flowchart LR\n%% <a href='people/user.md'>User</a>\n") == []
