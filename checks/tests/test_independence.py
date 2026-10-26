"""Assert the independence check reads a claim against the contract's vocabulary.

The check's input is a corpus of fixtures, a design, a glossary, the
documented invocation and the register of the corpus's own words, so each
case here supplies its own rather than the repository's: a manifest
carrying a word no source states, a design clause naming one, and the
interface terms the contract declares, which must pass. The codes a build
reports are supplied directly, so no case runs a build, and a code the
build reports that the contract declares nowhere is read against the
vocabulary like every other entry of the report.

The rule is positive, so the cases that matter are the two directions of
it. A word none of the four sources states is reported whatever it names,
which is how a term the check never heard of is caught. A word one of them
states is admitted however a sentence inflects it, which is what keeps the
corpus's own prose out of the report.
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
    vocabulary,
    words,
)

DESIGN = """# A design

## File heading

- **Link text:** The visible text of the heading the destination names.

## Block boundaries

Insert blank-line separation between maximal emitted regions. A Python
prototype establishes the contract.
"""

GLOSSARY = """# Glossary

## The act and the artifact

| Term | Definition |
| --- | --- |
| **bundle** (n.) | The single validated document produced by one run. |
| **deferral** | An author's statement that a reference is compiled elsewhere. |

## Terms deliberately not used

| Avoided | Why |
| --- | --- |
| **compositor** | A compositor sets type. It arranges; it resolves nothing. |
"""

DOCUMENTATION = """## Invocation

| Option | Effect |
| --- | --- |
| `-r DIR` | the allowed source root |
| `-d {text,json}` | the diagnostic format on standard error |
"""

ORDINARY = """an and another artefact beside build by can check claim clause
command conformance continuous copy cover declaration declare differ different
directory disk do document documentation environment execute exit family fixture
give hold host install installation integration invoke is it machine mapping
mechanism merely my never no note observable observe on once one path platform
rather reach reader at based inside of held remove report repository
resolution run runner smoke code nowhere behaviour behavioural non
something state status surface than that the them this throughout to two
uncovered unfixturable unnamed unreachable was whose work wrapper""".split()

ACCOUNTED = [
    text
    for declared in (*CLAIMS, *SECTIONS, *RECORDED)
    for text in (declared.name, declared.reason, declared.observable)
]

REGISTER = "\n".join(
    [
        "# Corpus vocabulary",
        "",
        "## Ordinary English",
        "",
        "| Word | What it does |",
        "| --- | --- |",
    ]
    + [
        f"| **{word}** | a word a claim of this corpus states. |"
        for word in dict.fromkeys(
            ORDINARY + [word for text in ACCOUNTED for word in words(text)]
        )
    ]
)


@pytest.fixture
def stated() -> set[str]:
    """The vocabulary a claim of this corpus is entitled to state."""
    return vocabulary(DESIGN, GLOSSARY, DOCUMENTATION, REGISTER)


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
    """A corpus whose declarations state the contract's words and no other."""
    return fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("Two emitted regions and one blank line between them."),
    )


def test_a_declaration_naming_a_word_no_source_states_is_reported(
    tmp_path: Path, stated: set[str]
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("The traceback is emitted beside the regions."),
    )
    found = corpus_references(corpus, stated)
    assert [reference.found for reference in found] == ["traceback"]
    assert found[0].where == "family/a-boundary-between-emitted-regions"


def test_a_corpus_stating_the_contract_s_words_alone_passes(
    clean: Path, stated: set[str]
) -> None:
    assert corpus_references(clean, stated) == []


def test_a_fixture_identity_naming_an_implementation_is_reported(
    tmp_path: Path, stated: set[str]
) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-the-rust-build-emits",
        manifest("Two emitted regions and one blank line between them."),
    )
    found = corpus_references(corpus, stated)
    assert [reference.found for reference in found] == ["rust"]


def test_a_report_entry_naming_an_implementation_is_reported(
    clean: Path, stated: set[str]
) -> None:
    design = DESIGN.replace("## Block boundaries", "## Block boundaries, npm")
    found = report_references(design, clean, stated, ())
    assert {reference.found for reference in found} == {"npm"}
    assert all(
        reference.where.startswith("the conformance report, line ")
        for reference in found
    )


def test_a_report_of_a_corpus_stating_the_contract_s_words_passes(
    clean: Path, stated: set[str]
) -> None:
    assert report_references(DESIGN, clean, stated, ()) == []


def test_a_reported_code_the_contract_declares_nowhere_is_read(
    clean: Path, stated: set[str]
) -> None:
    found = report_references(DESIGN, clean, stated, ("RUST",))
    assert [reference.found for reference in found] == ["RUST"]
    assert found[0].where.startswith("the conformance report, line ")


def test_the_contract_declares_its_interface_terms() -> None:
    declared = declared_names(DOCUMENTATION)
    assert "E_ROOT_NOT_FOUND" in declared
    assert "W_RESOURCE_PORTABILITY" in declared
    assert "warning" in declared
    assert "4" in declared
    assert "-d {text,json}" in declared


def test_an_interface_term_the_contract_declares_is_admitted(stated: set[str]) -> None:
    claim = "The run reports E_ROOT_NOT_FOUND."
    assert scan(claim, "where", stated) == []


def test_a_term_the_glossary_defines_is_admitted(stated: set[str]) -> None:
    assert scan("The deferral names the bundle.", "where", stated) == []


def test_a_word_the_register_admits_is_admitted(stated: set[str]) -> None:
    assert scan("A region beside another region.", "where", stated) == []


def test_a_word_the_register_does_not_admit_is_reported(stated: set[str]) -> None:
    assert [
        reference.found for reference in scan("A region alongside it.", "where", stated)
    ] == ["alongside"]


def test_a_word_is_read_as_the_contract_states_it_rather_than_as_inflected() -> None:
    assert "document" in forms("documents")
    assert "emit" in forms("emitted")
    assert "separate" in forms("separating")
    assert "plain" in forms("plainly")
    assert "identity" in forms("identities")


def test_an_inflection_of_a_stated_word_is_admitted(stated: set[str]) -> None:
    claim = "Emitting the regions names the destinations the headings state."
    assert scan(claim, "where", stated) == []


def test_a_hyphenated_compound_is_read_as_its_parts(stated: set[str]) -> None:
    assert scan("A blank-line separation.", "where", stated) == []
    assert [
        reference.found for reference in scan("A rust-emitted region.", "where", stated)
    ] == ["rust"]


def test_a_word_the_design_writes_only_capitalised_names_a_build(
    stated: set[str],
) -> None:
    assert [
        reference.found
        for reference in scan("A Python prototype runs.", "where", stated)
    ] == ["Python"]


def test_case_is_folded_on_the_reading_side(stated: set[str]) -> None:
    assert scan("Regions. Emitted regions. REGIONS.", "where", stated) == []


def test_a_language_named_by_a_sign_is_a_word() -> None:
    assert words("a c++ build and a c# build") == ["c++", "build", "and", "c#", "build"]
    assert words("a run of the build") == ["run", "of", "the", "build"]


def test_a_code_span_in_a_claim_names_the_fixture_s_tree(stated: set[str]) -> None:
    assert scan("The document at `My Note.md` is bundled.", "where", stated) == []


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


def test_the_tree_a_declaration_names_is_not_read_as_words(
    tmp_path: Path, stated: set[str]
) -> None:
    declared = manifest("Two emitted regions and one blank line between them.")
    declared["invocation"]["cwd"] = "rustsource"
    declared["invocation"]["arguments"] = ["modules/guide.md#alpha"]
    corpus = fixture(tmp_path / "fixtures", "a-boundary", declared)
    assert corpus_references(corpus, stated) == []
