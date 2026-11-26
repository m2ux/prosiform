"""Assert the independence check reads a claim against the contract's names.

The check's input is a corpus of fixtures, a design, a glossary and the
documented invocation, so each case here supplies its own rather than the
repository's: a manifest carrying a term no source states, a design clause
naming one, and the interface terms the contract declares, which must pass.
The codes a build reports are supplied directly, so no case runs a build,
and a code the build reports that the contract declares nowhere is read
against the contract's names like every other entry.

A term names an implementation by its shape. The cases that matter are
therefore the two directions of that rule: a shaped term none of the
sources states is reported whatever it names, and a word a sentence is
written in is passed over however unfamiliar it is, because ordinary prose
is not what the check is looking for.

Two kinds of word are refused whatever their shape. The design supplied here
carries a section stating no behaviour, and a word only that section writes
in a code span is reported in a declaration, in a fixture's identity and in
the report entry naming that fixture, while a word it writes outside one,
and a code-span term a behavioural section also states, pass. The glossary supplied
here names terms it deliberately does not use, and a description or a
fixture identity stating one, in any segment of the identity's path, is
reported with the reason the glossary gives.

One case reads the design the README pins in place of the one supplied here,
so a declaration naming a build word that design marks apart from its
behaviour is shown reported over the contract the corpus is held to.
"""

import json
from pathlib import Path
from typing import Any

import pytest
from conformance import CLAIMS, RECORDED, SECTIONS
from independence import (
    INVOCATION,
    UNNAMED,
    Vocabulary,
    avoided,
    claims,
    corpus_references,
    declared_names,
    forms,
    report_references,
    scan,
    shaped,
    sources,
    stated,
)
from vocabulary import SHIPPED_GLOSSARY

REPORT_TEXT = " ".join(
    text
    for declared in (*CLAIMS, *SECTIONS, *RECORDED)
    for text in (declared.name, declared.reason, declared.observable)
)

DESIGN = (
    """# A design

## Design status

The production build ships as one `crate`; meanwhile the `oracle` stays in
use beside it. Each `build` emits the regions the sections below state.

## File heading

- **Link text:** The visible text of the heading the destination names.

## Block boundaries

Insert blank-line separation between maximal emitted regions. A Python
prototype establishes the contract, and a Rust build implements it.
"""
    + "\n\n<!-- "
    + REPORT_TEXT
    + " -->\n"
)

GLOSSARY = """# Glossary

## The act and the artifact

| Term | Definition |
| --- | --- |
| **bundle** (n.) | The single validated document produced by one run. |
| **deferral** | An author's statement that a reference is bundled elsewhere. |

## Terms deliberately not used

| Avoided | Why |
| --- | --- |
| **branch** | Collides with the version-control sense. |
| **include** | Suggests textual substitution at a point. |
"""

BRANCH = "Collides with the version-control sense."

DOCUMENTATION = """## Invocation

| Option | Effect |
| --- | --- |
| `-r DIR` | the allowed source root |
| `-d {text,json}` | the diagnostic format on standard error |
"""


@pytest.fixture
def vocabulary() -> Vocabulary:
    """The terms the contract names, and the words it refuses."""
    return stated(DESIGN, GLOSSARY, DOCUMENTATION)


def manifest(description: str, clause: str = "Block boundaries") -> dict[str, Any]:
    """One fixture's declaration, as its manifest states it."""
    return {
        "description": description,
        "clauses": [clause],
        "invocation": {"cwd": "source", "arguments": ["guide.md"]},
        "expected": {
            "exit_status": 0,
            "stdout": "expected/stdout.md",
            "diagnostics": [],
        },
    }


def as_toml(declared: dict[str, Any]) -> str:
    """The declaration as the TOML a fixture carries."""
    invocation = declared["invocation"]
    lines = [f"description = {json.dumps(declared['description'])}", ""]
    lines.append("clauses = [")
    lines += [f"  {json.dumps(name)}," for name in declared["clauses"]]
    lines += ["]", ""]
    lines += ["[invocation]", f"cwd = {json.dumps(invocation['cwd'])}"]
    lines += [f"arguments = {json.dumps(invocation['arguments'])}", ""]
    lines += [
        "[expected]",
        f"exit_status = {declared['expected']['exit_status']}",
        'stdout = "expected/stdout.md"',
        "diagnostics = []",
    ]
    return "\n".join(lines) + "\n"


def fixture(directory: Path, name: str, declared: dict[str, Any]) -> Path:
    """One fixture in a corpus written for a test."""
    home = directory / "family" / name
    home.mkdir(parents=True)
    home.joinpath("manifest.toml").write_text(as_toml(declared), encoding="utf-8")
    return directory


@pytest.fixture
def clean(tmp_path: Path) -> Path:
    """A corpus whose declarations name the contract's terms and no other."""
    return fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("Two emitted regions and one blank line between them."),
    )


def test_a_declaration_naming_a_shaped_term_no_source_states_is_reported(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("The KeyError is emitted beside the regions."),
    )
    found = corpus_references(corpus, vocabulary)
    assert [reference.found for reference in found] == ["KeyError"]
    assert found[0].where == "family/a-boundary-between-emitted-regions"


def test_a_corpus_naming_the_contract_s_terms_alone_passes(
    clean: Path, vocabulary: Vocabulary
) -> None:
    assert corpus_references(clean, vocabulary) == []


def test_a_fixture_identity_naming_an_implementation_is_reported(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-the-Pydantic-build-emits",
        manifest("Two emitted regions and one blank line between them."),
    )
    found = corpus_references(corpus, vocabulary)
    assert [reference.found for reference in found] == ["Pydantic"]


def test_a_language_the_design_names_is_admitted(vocabulary: Vocabulary) -> None:
    assert scan("A Python prototype and a Rust build.", "where", vocabulary) == []


def test_a_report_entry_naming_an_implementation_is_reported(
    clean: Path, vocabulary: Vocabulary
) -> None:
    design = DESIGN.replace("## Block boundaries", "## Block boundaries, Pydantic")
    found = report_references(design, clean, vocabulary, ())
    assert {reference.found for reference in found} == {"Pydantic"}
    assert all(
        reference.where.startswith("the conformance report, line ")
        for reference in found
    )


def test_a_report_of_a_corpus_naming_the_contract_s_terms_passes(
    clean: Path, vocabulary: Vocabulary
) -> None:
    assert report_references(DESIGN, clean, vocabulary, ()) == []


def test_a_reported_code_the_contract_declares_nowhere_is_read(
    clean: Path, vocabulary: Vocabulary
) -> None:
    found = report_references(DESIGN, clean, vocabulary, ("E_PROTOTYPE_FAULT",))
    assert [reference.found for reference in found] == ["E_PROTOTYPE_FAULT"]
    assert found[0].where.startswith("the conformance report, line ")


def test_the_contract_declares_its_interface_terms() -> None:
    declared = declared_names(DOCUMENTATION)
    assert "E_TARGET_NOT_FOUND" in declared
    assert "W_RESOURCE_PORTABILITY" in declared
    assert "warning" in declared
    assert "4" in declared
    assert "-d {text,json}" in declared


def test_an_interface_term_the_contract_declares_is_admitted(
    vocabulary: Vocabulary,
) -> None:
    claim = "The run reports E_TARGET_NOT_FOUND."
    assert scan(claim, "where", vocabulary) == []


def test_a_term_the_glossary_defines_is_admitted(vocabulary: Vocabulary) -> None:
    assert scan("The deferral names the bundle.", "where", vocabulary) == []


def test_a_word_a_sentence_is_written_in_is_passed_over(vocabulary: Vocabulary) -> None:
    assert (
        scan("A region alongside another, however ordinary.", "where", vocabulary) == []
    )


def test_a_type_name_is_reported(vocabulary: Vocabulary) -> None:
    assert [
        reference.found
        for reference in scan("The PathBuilder reads the regions.", "where", vocabulary)
    ] == ["PathBuilder"]


def test_a_constant_shaped_term_is_reported(vocabulary: Vocabulary) -> None:
    assert [
        reference.found
        for reference in scan(
            "The build reports E_PROTOTYPE_FAULT.", "where", vocabulary
        )
    ] == ["E_PROTOTYPE_FAULT"]


def test_a_dotted_term_is_reported(vocabulary: Vocabulary) -> None:
    assert [
        reference.found
        for reference in scan(
            "The prosiform.default.group key is read.", "where", vocabulary
        )
    ] == ["prosiform.default.group"]


def test_a_dotted_path_a_claim_names_is_not_read_as_a_term(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary",
        manifest("The document at guide.md is bundled beside note.md."),
    )
    assert corpus_references(corpus, vocabulary) == []


def test_the_parts_of_a_dotted_term_are_read_with_the_term(
    vocabulary: Vocabulary,
) -> None:
    assert [
        reference.found
        for reference in scan("The My.Note key is read.", "where", vocabulary)
    ] == ["My.Note"]


def test_case_is_folded(vocabulary: Vocabulary) -> None:
    assert scan("A python prototype runs.", "where", vocabulary) == []


def test_a_term_is_read_as_the_contract_names_it_rather_than_as_inflected() -> None:
    assert "document" in forms("documents")
    assert "emit" in forms("emitted")
    assert "identity" in forms("identities")


def test_an_inflection_of_a_named_term_is_admitted(vocabulary: Vocabulary) -> None:
    claim = "Emitting the regions names the destinations the headings state."
    assert scan(claim, "where", vocabulary) == []


def test_a_shape_is_what_a_capital_an_underscore_or_a_dot_is() -> None:
    assert shaped("KeyError")
    assert shaped("E_TARGET_NOT_FOUND")
    assert shaped("prosiform.default.group")
    assert not shaped("region")
    assert not shaped("Regions", opening=True)
    assert shaped("Regions")
    assert not shaped("ATX")


def test_a_claim_is_the_text_a_declaration_states() -> None:
    declared = manifest("Two emitted regions.")
    declared["expected"]["stdout_contains"] = ["prosiform "]
    declared["expected"]["diagnostics"] = [
        {"severity": "error", "code": "E_RAW_HTML", "message_contains": ["raw"]}
    ]
    assert claims(declared, "family/one") == [
        "family/one",
        "Two emitted regions.",
        "Block boundaries",
        "prosiform ",
        "raw",
    ]


def test_the_tree_a_declaration_names_is_not_read_as_terms(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    declared = manifest("Two emitted regions and one blank line between them.")
    declared["invocation"]["cwd"] = "rustsource"
    declared["invocation"]["arguments"] = ["modules/guide.md#alpha"]
    corpus = fixture(tmp_path / "fixtures", "a-boundary", declared)
    assert corpus_references(corpus, vocabulary) == []


def test_a_declaration_naming_a_word_only_a_silent_section_carries_is_reported(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("The crate emits two regions and one blank line between them."),
    )
    found = corpus_references(corpus, vocabulary)
    assert [reference.found for reference in found] == ["crate"]
    assert "'Design status' section" in found[0].reason
    assert "states no behaviour" in found[0].reason


def test_a_declaration_naming_the_pinned_design_s_build_words_is_reported(
    tmp_path: Path,
) -> None:
    design, _ = sources()
    pinned = stated(design, SHIPPED_GLOSSARY.read_text(), INVOCATION.read_text())
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("The crate and the wheel emit two regions with a blank line."),
    )
    found = corpus_references(corpus, pinned)
    assert [reference.found for reference in found] == ["crate", "wheel"]
    assert all(
        "'Production build obligations' section" in reference.reason
        for reference in found
    )


def test_a_bold_label_the_pinned_design_s_silent_sections_carry_is_admitted() -> None:
    design, _ = sources()
    pinned = stated(design, SHIPPED_GLOSSARY.read_text(), INVOCATION.read_text())
    claim = "Calibration of the iterator is no regression."
    assert scan(claim, "where", pinned) == []


def test_a_word_a_silent_section_writes_unmarked_is_admitted(
    vocabulary: Vocabulary,
) -> None:
    assert "meanwhile" not in vocabulary.names
    claim = "Meanwhile the regions are emitted with one blank line between them."
    assert scan(claim, "where", vocabulary) == []


def test_a_term_a_silent_section_marks_and_the_contract_states_is_admitted(
    vocabulary: Vocabulary,
) -> None:
    assert "build" in vocabulary.names
    assert scan("Each build emits the regions.", "where", vocabulary) == []


def test_a_word_only_a_silent_section_carries_is_refused_whatever_its_shape(
    vocabulary: Vocabulary,
) -> None:
    found = scan("Two crates and an Oracle emit the regions.", "where", vocabulary)
    assert [reference.found for reference in found] == ["crates", "Oracle"]
    assert all("'Design status'" in reference.reason for reference in found)


def test_a_report_entry_naming_a_word_only_a_silent_section_carries_is_reported(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-the-crate-emits",
        manifest("Two emitted regions and one blank line between them."),
    )
    found = report_references(DESIGN, corpus, vocabulary, ())
    assert {reference.found for reference in found} == {"crate"}
    assert all(
        reference.where.startswith("the conformance report, line ")
        for reference in found
    )


def test_a_word_naming_a_file_the_fixture_carries_is_the_tree_s(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("The oracle document is bundled beside the regions."),
    )
    corpus.joinpath("family", "a-boundary-between-emitted-regions", "oracle.md").touch()
    assert corpus_references(corpus, vocabulary) == []


def test_the_glossary_states_why_each_avoided_term_is_avoided() -> None:
    assert avoided(GLOSSARY) == {
        "branch": BRANCH,
        "include": "Suggests textual substitution at a point.",
    }


def test_a_description_stating_an_avoided_term_is_reported_with_its_reason(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("Two regions from disjoint branches and one blank line between them."),
    )
    found = corpus_references(corpus, vocabulary)
    assert [reference.found for reference in found] == ["branches"]
    assert found[0].reason == (
        f"is a term docs/glossary.md deliberately does not use: {BRANCH}"
    )


def test_an_identity_stating_an_avoided_term_is_reported_with_its_reason(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-region-from-another-branch",
        manifest("Two emitted regions and one blank line between them."),
    )
    found = corpus_references(corpus, vocabulary)
    assert [reference.found for reference in found] == ["branch"]
    assert found[0].where == "family/a-region-from-another-branch"
    assert found[0].reason == (
        f"is a term docs/glossary.md deliberately does not use: {BRANCH}"
    )


def test_an_avoided_term_in_any_segment_of_an_identity_is_reported(
    tmp_path: Path, vocabulary: Vocabulary
) -> None:
    corpus = fixture(
        tmp_path / "fixtures" / "included",
        "a-boundary-between-emitted-regions",
        manifest("Two emitted regions and one blank line between them."),
    )
    found = corpus_references(corpus.parent, vocabulary)
    assert [reference.found for reference in found] == ["included"]


def test_an_avoided_term_the_design_s_prose_states_is_still_reported(
    vocabulary: Vocabulary,
) -> None:
    claim = "The region included is emitted."
    assert scan(claim, "where", vocabulary) == []
    found = scan(claim, "where", vocabulary, avoiding=True)
    assert [reference.found for reference in found] == ["included"]


def test_a_shaped_term_keeps_its_own_reason(vocabulary: Vocabulary) -> None:
    found = scan("The PathBuilder reads the regions.", "where", vocabulary)
    assert [reference.reason for reference in found] == [UNNAMED]
