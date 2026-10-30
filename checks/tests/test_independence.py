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
"""

import json
from pathlib import Path
from typing import Any

import pytest
from conformance import CLAIMS, RECORDED, SECTIONS
from independence import (
    claims,
    corpus_references,
    declared_names,
    forms,
    report_references,
    scan,
    shaped,
    stated,
)

REPORT_TEXT = " ".join(
    text
    for declared in (*CLAIMS, *SECTIONS, *RECORDED)
    for text in (declared.name, declared.reason, declared.observable)
)

DESIGN = (
    """# A design

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
| **deferral** | An author's statement that a reference is compiled elsewhere. |
"""

DOCUMENTATION = """## Invocation

| Option | Effect |
| --- | --- |
| `-r DIR` | the allowed source root |
| `-d {text,json}` | the diagnostic format on standard error |
"""


@pytest.fixture
def names() -> set[str]:
    """The terms the contract names."""
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
    tmp_path: Path, names: set[str]
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("The KeyError is emitted beside the regions."),
    )
    found = corpus_references(corpus, names)
    assert [reference.found for reference in found] == ["KeyError"]
    assert found[0].where == "family/a-boundary-between-emitted-regions"


def test_a_corpus_naming_the_contract_s_terms_alone_passes(
    clean: Path, names: set[str]
) -> None:
    assert corpus_references(clean, names) == []


def test_a_fixture_identity_naming_an_implementation_is_reported(
    tmp_path: Path, names: set[str]
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-the-Pydantic-build-emits",
        manifest("Two emitted regions and one blank line between them."),
    )
    found = corpus_references(corpus, names)
    assert [reference.found for reference in found] == ["Pydantic"]


def test_a_language_the_design_names_is_admitted(names: set[str]) -> None:
    assert scan("A Python prototype and a Rust build.", "where", names) == []


def test_a_report_entry_naming_an_implementation_is_reported(
    clean: Path, names: set[str]
) -> None:
    design = DESIGN.replace("## Block boundaries", "## Block boundaries, Pydantic")
    found = report_references(design, clean, names, ())
    assert {reference.found for reference in found} == {"Pydantic"}
    assert all(
        reference.where.startswith("the conformance report, line ")
        for reference in found
    )


def test_a_report_of_a_corpus_naming_the_contract_s_terms_passes(
    clean: Path, names: set[str]
) -> None:
    assert report_references(DESIGN, clean, names, ()) == []


def test_a_reported_code_the_contract_declares_nowhere_is_read(
    clean: Path, names: set[str]
) -> None:
    found = report_references(DESIGN, clean, names, ("E_PROTOTYPE_FAULT",))
    assert [reference.found for reference in found] == ["E_PROTOTYPE_FAULT"]
    assert found[0].where.startswith("the conformance report, line ")


def test_the_contract_declares_its_interface_terms() -> None:
    declared = declared_names(DOCUMENTATION)
    assert "E_ROOT_NOT_FOUND" in declared
    assert "W_RESOURCE_PORTABILITY" in declared
    assert "warning" in declared
    assert "4" in declared
    assert "-d {text,json}" in declared


def test_an_interface_term_the_contract_declares_is_admitted(names: set[str]) -> None:
    claim = "The run reports E_ROOT_NOT_FOUND."
    assert scan(claim, "where", names) == []


def test_a_term_the_glossary_defines_is_admitted(names: set[str]) -> None:
    assert scan("The deferral names the bundle.", "where", names) == []


def test_a_word_a_sentence_is_written_in_is_passed_over(names: set[str]) -> None:
    assert scan("A region alongside another, however ordinary.", "where", names) == []


def test_a_type_name_is_reported(names: set[str]) -> None:
    assert [
        reference.found
        for reference in scan("The PathBuilder reads the regions.", "where", names)
    ] == ["PathBuilder"]


def test_a_constant_shaped_term_is_reported(names: set[str]) -> None:
    assert [
        reference.found
        for reference in scan("The build reports E_PROTOTYPE_FAULT.", "where", names)
    ] == ["E_PROTOTYPE_FAULT"]


def test_a_dotted_term_is_reported(names: set[str]) -> None:
    assert [
        reference.found
        for reference in scan("The prosiform.group key is read.", "where", names)
    ] == ["prosiform.group"]


def test_a_dotted_path_a_claim_names_is_not_read_as_a_term(
    tmp_path: Path, names: set[str]
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary",
        manifest("The document at guide.md is bundled beside note.md."),
    )
    assert corpus_references(corpus, names) == []


def test_the_parts_of_a_dotted_term_are_read_with_the_term(names: set[str]) -> None:
    assert [
        reference.found
        for reference in scan("The My.Note key is read.", "where", names)
    ] == ["My.Note"]


def test_case_is_folded(names: set[str]) -> None:
    assert scan("A python prototype runs.", "where", names) == []


def test_a_term_is_read_as_the_contract_names_it_rather_than_as_inflected() -> None:
    assert "document" in forms("documents")
    assert "emit" in forms("emitted")
    assert "identity" in forms("identities")


def test_an_inflection_of_a_named_term_is_admitted(names: set[str]) -> None:
    claim = "Emitting the regions names the destinations the headings state."
    assert scan(claim, "where", names) == []


def test_a_shape_is_what_a_capital_an_underscore_or_a_dot_is() -> None:
    assert shaped("KeyError")
    assert shaped("E_ROOT_NOT_FOUND")
    assert shaped("prosiform.group")
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
    tmp_path: Path, names: set[str]
) -> None:
    declared = manifest("Two emitted regions and one blank line between them.")
    declared["invocation"]["cwd"] = "rustsource"
    declared["invocation"]["arguments"] = ["modules/guide.md#alpha"]
    corpus = fixture(tmp_path / "fixtures", "a-boundary", declared)
    assert corpus_references(corpus, names) == []
