"""Assert what the scan removes, what it leaves, and where the content began.

A removal rule only ever observed removing is half tested, so each case
the contract excludes is here beside the cases it includes: an indented
delimiter, a delimiter carrying a trailing space, a TOML fence, JSON
metadata, a `---` under a blank line, a `---` inside a code fence and one
below the first line each leave the document exactly as the file holds
it. Every case states the content the scan returns and the line that
content begins on, because the coordinate is as much the result as the
text is.
"""

import pytest
from prosiform.source import (
    MARK,
    Source,
    Unterminated,
    bare,
    content,
    decode,
    lines,
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
