"""Assert a reference normalizes to the path identity the design declares.

Each case names a step of the resolution sequence and the behaviour that
step exists for. The order is what the cases are really about: a split
performed after decoding reads an encoded delimiter as a delimiter, a
second decoding reads an author's literal escape as an escape, and a
normalization performed over undecoded segments widens a path by a level
its author never wrote. Each of those is a different document, so each
has a case here.

Both directions are carried. A form the profile admits resolves to the
identity it names, and a form outside the profile raises the refusal its
kind declares rather than reaching a filesystem.
"""

import pytest
from prosiform.closure import Malformed, OutsideRoot, inside, marked, resolve


def test_a_reference_names_its_document_and_no_section() -> None:
    found = resolve("guide.md")
    assert (found.path, found.fragment, found.external) == ("guide.md", None, False)


def test_an_empty_fragment_is_the_same_whole_document_reference() -> None:
    assert resolve("guide.md#").fragment is None


def test_a_fragment_is_the_section_it_names() -> None:
    assert resolve("guide.md#run").fragment == "run"


def test_an_encoded_number_sign_is_a_filename_character() -> None:
    found = resolve("notes%23draft.md#run")
    assert (found.path, found.fragment) == ("notes#draft.md", "run")


def test_an_encoded_question_mark_is_a_filename_character() -> None:
    assert resolve("notes%3Fdraft.md").path == "notes?draft.md"


def test_an_escape_is_decoded_exactly_once() -> None:
    assert resolve("notes%2523draft.md").path == "notes%23draft.md"


def test_escapes_spelling_one_character_decode_together() -> None:
    assert resolve("caf%C3%A9.md").path == "caf\u00e9.md"


def test_a_fragment_is_decoded_and_looked_up_as_it_is_spelled() -> None:
    assert resolve("guide.md#Run%20It").fragment == "Run It"


def test_a_relative_segment_normalizes_against_the_root() -> None:
    assert resolve("sub/../guide.md").path == "guide.md"
    assert resolve("./guide.md").path == "guide.md"


def test_a_relative_segment_normalizes_against_the_referring_directory() -> None:
    assert resolve("note.md", "docs").path == "docs/note.md"
    assert resolve("../guide.md", "docs").path == "guide.md"
    assert resolve("../notes/note.md", "docs/deep").path == "docs/notes/note.md"


def test_a_scheme_is_classified_rather_than_resolved() -> None:
    found = resolve("https://example.com/guide.md?view=raw#run")
    assert found.external is True
    assert found.original == "https://example.com/guide.md?view=raw#run"


def test_an_authority_is_classified_rather_than_resolved() -> None:
    assert resolve("//example.com/guide.md").external is True


def test_a_drive_path_is_a_path_the_root_cannot_contain() -> None:
    with pytest.raises(OutsideRoot):
        resolve("C:/guide.md")


@pytest.mark.parametrize("reference", ["/guide.md", "../outside.md", "sub/../../x.md"])
def test_a_path_the_root_cannot_contain_is_refused(reference: str) -> None:
    with pytest.raises(OutsideRoot):
        resolve(reference)


def test_a_walk_above_the_referring_directory_leaves_the_root() -> None:
    with pytest.raises(OutsideRoot):
        resolve("../../outside.md", "docs")


@pytest.mark.parametrize("reference", ["guide.md?view=raw", "guide.md?", "guide.md?#"])
def test_a_query_is_refused(reference: str) -> None:
    with pytest.raises(Malformed):
        resolve(reference)


@pytest.mark.parametrize("reference", ["notes%2.md", "notes%zz.md", "notes%"])
def test_an_escape_that_is_not_two_hexadecimal_digits_is_refused(
    reference: str,
) -> None:
    with pytest.raises(Malformed):
        resolve(reference)


@pytest.mark.parametrize("reference", ["notes%C0%AF.md", "notes%FF.md"])
def test_an_escape_sequence_that_is_not_utf8_is_refused(reference: str) -> None:
    with pytest.raises(Malformed):
        resolve(reference)


@pytest.mark.parametrize("reference", ["notes%00.md", "notes%0A.md", "guide.md#a%00b"])
def test_a_control_character_is_refused(reference: str) -> None:
    with pytest.raises(Malformed):
        resolve(reference)


@pytest.mark.parametrize("reference", ["sub%2Fguide.md", "sub%5Cguide.md"])
def test_a_separator_a_segment_decodes_to_is_refused(reference: str) -> None:
    with pytest.raises(Malformed):
        resolve(reference)


def test_a_backslash_separator_is_refused() -> None:
    with pytest.raises(Malformed):
        resolve("sub\\guide.md")


def test_a_link_text_opening_with_the_mark_is_a_dependency() -> None:
    assert marked("¬ Record Epic Delivery")


def test_a_link_text_carrying_the_mark_elsewhere_is_a_mention() -> None:
    assert not marked("the ¬ operator")


def test_a_link_text_with_no_mark_is_a_mention() -> None:
    assert not marked("Record Epic Delivery")


def test_a_link_resolves_against_the_directory_of_the_document_carrying_it() -> None:
    assert inside("docs/guide.md", "other.md").path == "docs/other.md"


def test_a_link_walking_out_of_its_own_directory_normalizes_against_it() -> None:
    assert inside("docs/guide.md", "../notes.md").path == "notes.md"


def test_a_link_above_the_root_names_a_document_the_root_cannot_contain() -> None:
    with pytest.raises(OutsideRoot):
        inside("guide.md", "../outside.md")


def test_a_fragment_alone_names_a_section_of_the_document_carrying_it() -> None:
    found = inside("docs/guide.md", "#run-it")
    assert (found.path, found.fragment) == ("docs/guide.md", "run-it")


def test_a_reference_a_source_carries_keeps_the_text_it_was_written_as() -> None:
    assert inside("docs/guide.md", "#run-it").original == "#run-it"
