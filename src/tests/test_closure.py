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

from prosiform.closure import (
    Declarations,
    Malformed,
    OutsideRoot,
    Probed,
    Reference,
    boundary,
    bundled,
    conflicting,
    deferred,
    dispatched,
    identity,
    inside,
    operators,
    parallel,
    rebased,
    resolvable,
    resolve,
    spaced,
    unmarked,
    withholding,
    withholding_target,
)
from prosiform.profile import parse


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


def test_a_link_text_opening_with_the_deferral_mark_is_deferred() -> None:
    assert deferred("¬ Record Epic Delivery")


def test_a_link_text_carrying_the_mark_elsewhere_is_not_deferred() -> None:
    assert not deferred("the ¬ operator")


def test_a_link_text_with_no_mark_is_not_deferred() -> None:
    assert not deferred("Record Epic Delivery")


def test_a_link_text_opening_with_the_dispatch_mark_is_dispatched() -> None:
    assert dispatched("⇉ Record Epic Delivery")


def test_a_link_text_carrying_the_dispatch_mark_elsewhere_is_not_dispatched() -> None:
    assert not dispatched("the ⇉ operator")


def test_a_dispatch_mark_is_no_deferral_and_the_two_marks_are_told_apart() -> None:
    assert not deferred("⇉ the rules")
    assert not dispatched("¬ the rules")


def test_a_mark_opening_the_text_with_no_space_after_it_is_no_operator() -> None:
    assert not dispatched("⇉Record Epic Delivery")
    assert not deferred("¬Record Epic Delivery")
    assert not dispatched("⇉")
    assert not deferred("¬\tRecord Epic Delivery")


def test_two_dispatch_marks_opening_one_text_conflict() -> None:
    assert conflicting("⇉⫽ the rules")
    assert conflicting("⫽⇉ the rules")
    assert conflicting(" ⇉⫽⇉ the rules")


def test_a_deferral_and_a_dispatch_mark_written_together_are_admitted() -> None:
    """A deferral says when, a dispatch says who, so together they agree."""
    assert not conflicting("¬⇉ the rules")
    assert not conflicting("¬⫽ the rules")
    assert conflicting("⇉⫽ the rules")
    assert conflicting("¬⇉⫽ the rules")


def test_one_operator_alone_does_not_conflict() -> None:
    assert not conflicting("¬ the rules")
    assert not conflicting("⇉ the rules")
    assert not conflicting("¬ and ⇉ the rules")


def test_a_mark_with_no_space_after_it_ends_the_operators_a_text_opens_with() -> None:
    assert operators("¬⇉the rules") == ()
    assert operators("⇉¬the rules") == ()
    assert operators("¬ ⫽the rules") == ("¬",)


def test_operators_are_each_operator_one_text_opens_with() -> None:
    assert operators("¬ the rules") == ("¬",)
    assert operators("⇉ the rules") == ("⇉",)
    assert operators("the ¬ rules") == ()


def test_the_marks_of_a_compound_operator_are_one_group() -> None:
    assert operators("¬⇉ the rules") == ("¬", "⇉")
    assert operators("¬⫽ the rules") == ("¬", "⫽")
    assert operators(" ¬⫽  the reviews") == ("¬", "⫽")


def test_an_unspaced_withholding_mark_is_published_as_written() -> None:
    assert unmarked("¬  the rules") == "the rules"
    assert unmarked("¬the rules") == "¬the rules"
    assert unmarked("⇉ the rules") == "the rules"
    assert unmarked("⫽ the rules") == "the rules"
    assert unmarked("⫽the rules") == "⫽the rules"


def test_the_marks_of_one_operator_go_together() -> None:
    assert unmarked("¬⇉ the rules") == "the rules"
    assert unmarked("¬⫽ the rules") == "the rules"
    assert unmarked("¬⇉Rules") == "¬⇉Rules"


def test_a_link_resolves_against_the_directory_of_the_document_carrying_it() -> None:
    assert inside("docs/guide.md", "other.md").path == "docs/other.md"


def test_a_link_walking_out_of_its_own_directory_normalizes_against_it() -> None:
    assert inside("docs/guide.md", "../notes.md").path == "notes.md"


def test_a_link_resolves_from_its_file_and_keeps_its_walk() -> None:
    found = inside("docs/guide.md", "notes.md")
    assert found.path == "docs/notes.md"
    assert found.walk == "docs/notes.md"


def test_a_link_above_the_working_directory_is_refused() -> None:
    with pytest.raises(OutsideRoot):
        inside("guide.md", "../outside.md")


def test_a_parent_step_resolves_from_the_file_carrying_it() -> None:
    found = inside("modes/plan-mode.md", "../artifacts/epic.md")
    assert found.path == "artifacts/epic.md"
    assert found.walk == "modes/../artifacts/epic.md"


def test_a_parent_step_from_the_working_directory_is_refused() -> None:
    with pytest.raises(OutsideRoot):
        inside("plan-mode.md", "../artifacts/epic.md")


def test_a_fragment_alone_names_a_section_of_the_document_carrying_it() -> None:
    found = inside("docs/guide.md", "#run-it")
    assert (found.path, found.fragment) == ("docs/guide.md", "run-it")


def test_a_reference_a_source_carries_keeps_the_text_it_was_written_as() -> None:
    assert inside("docs/guide.md", "#run-it").original == "#run-it"


def test_an_identity_is_the_document_a_whole_document_reference_names() -> None:
    assert identity(resolve("docs/guide.md")) == "docs/guide.md"


def test_an_identity_names_the_section_where_the_reference_does() -> None:
    assert identity(resolve("docs/guide.md#alpha")) == "docs/guide.md#alpha"


def test_a_fragment_alone_takes_its_identity_from_the_base_it_is_read_against() -> None:
    assert identity(resolve("#alpha"), "docs/guide.md") == "docs/guide.md#alpha"


def test_two_spellings_of_one_section_share_an_identity() -> None:
    assert identity(resolve("./%67uide.md#alpha")) == identity(
        resolve("guide.md#alpha")
    )


def test_a_reference_resolving_under_the_root_is_a_dependency() -> None:
    found = bundled("docs/guide.md", "rules.md#alpha", "the rules")
    assert found is not None
    assert (found.path, found.fragment) == ("docs/rules.md", "alpha")


def test_a_fragment_of_its_own_document_is_a_dependency() -> None:
    found = bundled("docs/guide.md", "#alpha", "alpha")
    assert found is not None
    assert (found.path, found.fragment) == ("docs/guide.md", "alpha")


def test_a_withheld_reference_under_the_root_is_no_dependency() -> None:
    assert bundled("guide.md", "rules.md", "¬ the rules") is None
    assert bundled("guide.md", "rules.md", "⇉ the rules") is None


def test_the_same_reference_unmarked_is_a_dependency() -> None:
    found = bundled("guide.md", "rules.md", "the rules")
    assert found is not None
    assert found.path == "rules.md"


def test_a_mark_written_inside_a_link_text_withholds_nothing() -> None:
    assert bundled("guide.md", "rules.md", "the ¬ operator") is not None


@pytest.mark.parametrize(
    "destination",
    [
        "../rules.md",
        "/rules.md",
        "C:/rules.md",
        "https://example.com/rules.md",
        "//example.com/rules.md",
        "plan.png",
        "rules.md?view=raw",
    ],
)
def test_a_reference_the_bundle_compiles_none_of_names_no_dependency(
    destination: str,
) -> None:
    assert bundled("guide.md", destination, "the rules") is None


@pytest.mark.parametrize("opening", ["¬ the rules", "⇉ the rules"])
def test_a_withheld_reference_under_the_root_is_a_withheld_target(
    opening: str,
) -> None:
    found = withholding_target("docs/guide.md", "rules.md", opening)
    assert found is not None
    assert found.path == "docs/rules.md"


def test_an_unmarked_reference_withholds_nothing() -> None:
    assert withholding_target("guide.md", "rules.md", "the rules") is None


@pytest.mark.parametrize(
    "destination",
    [
        "../rules.md",
        "/rules.md",
        "C:/rules.md",
        "https://example.com/rules.md",
        "//example.com/rules.md",
        "plan.png",
        "rules.md?view=raw",
    ],
)
def test_a_mark_on_a_reference_the_run_carries_none_of_withholds_nothing(
    destination: str,
) -> None:
    assert withholding_target("guide.md", destination, "¬ the rules") is None
    assert withholding_target("guide.md", destination, "⇉ the rules") is None


@pytest.mark.parametrize(
    ("document", "destination", "expected"),
    [
        ("topic/guide.md", "../shared/rules.md", "shared/rules.md"),
        ("topic/guide.md", "../shared/rules.md#here", "shared/rules.md#here"),
        ("topic/guide.md", "rules.md", "topic/rules.md"),
        ("guide.md", "#beta", "guide.md#beta"),
        ("guide.md", "rules.md#", "rules.md#"),
        ("guide.md", "notes%23draft.md#run", "notes%23draft.md#run"),
    ],
)
@pytest.mark.parametrize("opening", ["¬ the rules", "⇉ the rules"])
def test_a_withheld_destination_names_its_target_from_the_root(
    document: str, destination: str, expected: str, opening: str
) -> None:
    found = withholding_target(document, destination, opening)
    assert found is not None
    assert rebased(found, destination) == expected


def test_a_link_text_opening_with_a_guillemet_states_no_operator() -> None:
    assert operators("» the rules") == ()


def test_a_link_opening_with_the_parallel_mark_states_a_parallel_dispatch() -> None:
    assert parallel("⫽ the reviews")
    assert dispatched("⫽ the reviews")
    assert operators("⫽ the reviews") == ("⫽",)
    assert not parallel("⇉ the reviews")


def test_a_parallel_dispatch_withholds_its_target() -> None:
    assert withholding("⫽ the reviews")
    assert bundled("guide.md", "plan.md#reviews", "⫽ the reviews") is None
    found = withholding_target("guide.md", "plan.md#reviews", "⫽ the reviews")
    assert found is not None
    assert (found.path, found.fragment) == ("plan.md", "reviews")


def test_a_parallel_mark_with_no_space_after_it_is_no_operator() -> None:
    assert not parallel("⫽the reviews")
    assert not parallel("the ⫽ reviews")
    assert operators("⫽⇉the reviews") == ()


@pytest.mark.parametrize("opening", ["⫽⇉ the reviews", "⇉⫽ the reviews"])
def test_the_parallel_mark_conflicts_with_the_dispatch_mark(opening: str) -> None:
    assert conflicting(opening)


def test_the_parallel_mark_beside_a_deferral_states_one_compilation() -> None:
    assert not conflicting("¬⫽ the reviews")


@pytest.mark.parametrize("opening", ["¬ ⇉ the rules", "¬ ⫽ the reviews"])
def test_a_blank_between_the_marks_of_a_compound_operator_is_refused(
    opening: str,
) -> None:
    assert spaced(opening)


def probing(answers: dict[str, Probed]) -> tuple[Declarations, list[Reference]]:
    """A record answering from a table, and the occurrences its probe was handed."""
    asked: list[Reference] = []

    def probe(found: Reference) -> Probed:
        asked.append(found)
        return answers[found.path]

    return Declarations(probe), asked


def test_a_link_naming_a_declaring_document_is_a_dependency() -> None:
    declarations, _ = probing({"rules.md": Probed.DECLARING})
    found = bundled("guide.md", "rules.md", "the rules", declarations)
    assert found is not None and found.path == "rules.md"


def test_a_link_naming_a_silent_document_is_text() -> None:
    declarations, _ = probing({"rules.md": Probed.SILENT})
    assert bundled("guide.md", "rules.md", "the rules", declarations) is None
    assert resolvable("guide.md", "rules.md", declarations) is None


def test_a_link_naming_no_document_is_text() -> None:
    declarations, _ = probing({"rules.md": Probed.ABSENT})
    assert bundled("guide.md", "rules.md", "the rules", declarations) is None
    assert declarations.answer(Reference("rules.md", "rules.md")) is Probed.ABSENT


def test_a_withheld_link_naming_a_silent_document_withholds_nothing() -> None:
    declarations, _ = probing({"rules.md": Probed.SILENT})
    assert (
        withholding_target("guide.md", "rules.md", "¬ the rules", declarations) is None
    )


def test_a_target_is_probed_once_however_many_links_name_it() -> None:
    declarations, asked = probing({"rules.md": Probed.DECLARING})
    bundled("guide.md", "rules.md", "the rules", declarations)
    bundled("guide.md", "rules.md#alpha", "alpha", declarations)
    withholding_target("guide.md", "./rules.md", "¬ the rules", declarations)
    assert [one.path for one in asked] == ["rules.md"]


def test_a_citation_naming_no_markdown_document_is_never_probed() -> None:
    declarations, asked = probing({})
    assert bundled("guide.md", "image.png", "the image", declarations) is None
    assert bundled("guide.md", "https://example.test/a.md", "a", declarations) is None
    assert asked == []


def test_the_probe_is_handed_the_occurrence_that_asked() -> None:
    declarations, asked = probing({"docs/rules.md": Probed.DECLARING})
    resolvable(
        "docs/guide.md",
        "rules.md",
        declarations,
        origin="docs/guide.md:3",
        reached=("docs/guide.md",),
    )
    [occurrence] = asked
    assert occurrence.origin == "docs/guide.md:3"
    assert occurrence.chain == ("docs/guide.md", "docs/rules.md")


def bounded(document: str, text: str) -> str:
    return boundary(document, parse(text))


def test_a_document_naming_no_local_markdown_path_has_its_own_directory() -> None:
    text = "# Guide\n\n[Site](https://example.com/a.md) ![Map](map.png)\n"
    assert bounded("skills/plan/guide.md", text) == "skills/plan"
    assert bounded("guide.md", "# Guide\n") == ""


def test_the_boundary_is_the_deepest_directory_holding_every_named_path() -> None:
    text = "[Review](modes/review.md) [Rules](rules/common.md) [Self](#guide)\n"
    assert bounded("skill/guide.md", text) == "skill"
    assert bounded("skill/guide.md", "[A](rules/a.md) [B](rules/b.md)\n") == (
        "skill/rules"
    )


def test_a_link_above_the_writing_directory_widens_the_boundary_to_hold_it() -> None:
    text = "# Review\n\n[Rules](../rules.md) [Self](#review)\n"
    assert bounded("skill/modes/review.md", text) == "skill"


def test_the_boundary_reads_every_link_the_document_writes() -> None:
    text = (
        "# Guide\n\n## Kept\n\n[A](a/one.md)\n\n"
        "## Elsewhere\n\n[¬ Later](../b/two.md)\n\n"
        '```mermaid\nflowchart LR\n  X\n  click X "../c/three.md"\n```\n'
    )
    assert bounded("skill/guide.md", text) == ""


def test_the_boundary_refuses_no_link_it_was_derived_from() -> None:
    document = "skill/modes/review.md"
    links = ["../rules.md", "deep/er/note.md", "#review", "../../top.md"]
    found = bounded(document, " ".join(f"[x]({link})" for link in links) + "\n")
    for link in links:
        named = inside(document, link).path
        assert found == "" or named.startswith(f"{found}/")


def test_a_path_above_the_working_directory_names_nothing_the_boundary_holds() -> None:
    assert bounded("skill/guide.md", "[Out](../../outside.md)\n") == "skill"
