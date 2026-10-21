"""Assert the independence check refuses an implementation reference and nothing else.

The check's input is a corpus of fixtures, a design and the documented
invocation, so each case here supplies its own rather than the
repository's: a manifest carrying an implementation module name, a design
whose clause names one, and the interface terms the contract declares,
which must pass. The codes a build reports are supplied directly, so no
case runs a build, and a code the build reports that the contract declares
nowhere is scanned like every other entry of the report.

The contract's declared names are held apart from the inventory rather
than subtracted from the scan, so the last cases read that inventory
against the names a contract declares: the repository's own names match
none of it, and a declared name that did would fail the check.
"""

import json
from pathlib import Path
from typing import Any

import pytest
from independence import (
    corpus_references,
    declared_names,
    declared_references,
    inventory,
    report_references,
    scan,
)

DESIGN = """# A design

## Entry line

- **Link text:** The visible text of the heading the destination names.

## Block boundaries

Insert blank-line separation between maximal emitted regions.
"""

DOCUMENTATION = """## Invocation

| Option | Effect |
| --- | --- |
| `--root DIR` | the allowed source root |
| `--diagnostics {text,json}` | the diagnostic format on standard error |
"""


def manifest(description: str, clause: str = "Block boundaries") -> dict[str, Any]:
    """One fixture's declaration, as its manifest states it."""
    return {
        "description": description,
        "clauses": [clause],
        "invocation": {"arguments": ["guide.md"]},
        "expected": {
            "exit_status": 0,
            "stdout": "expected/stdout.md",
            "diagnostics": [],
        },
    }


def as_toml(declared: dict[str, Any]) -> str:
    """The declaration as the TOML a fixture carries."""
    lines = [f"description = {json.dumps(declared['description'])}", ""]
    lines.append("clauses = [")
    lines += [f"  {json.dumps(name)}," for name in declared["clauses"]]
    lines += ["]", ""]
    lines += ["[invocation]", 'arguments = ["guide.md"]', ""]
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
    """A corpus whose declarations state the behaviour and name no build."""
    return fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("Two emitted regions are separated by one blank line."),
    )


def test_a_declaration_naming_an_implementation_module_fails(tmp_path: Path) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-between-emitted-regions",
        manifest("The boundary is inserted by prosiform/emit.py."),
    )
    found = corpus_references(corpus)
    assert [reference.found for reference in found] == ["prosiform/emit.py"]
    assert found[0].where == "family/a-boundary-between-emitted-regions"
    assert found[0].names == "a source file of an implementation"


def test_a_corpus_stating_behaviour_alone_passes(clean: Path) -> None:
    assert corpus_references(clean) == []


def test_every_kind_of_term_is_named_by_what_it_is() -> None:
    named = {reference.found: reference.names for reference in scan(TERMS, "where")}
    assert named["Python"] == "an implementation language or runtime"
    assert named["module"] == "the machinery of modules and packaging"
    assert named["traceback"] == "the wording a build gives its own fault"
    assert named["bundle.rs"] == "a source file of an implementation"
    assert named["__main__"] == "an identifier a language reserves"
    assert named["ValueError"] == "a fault class of an implementation"


TERMS = (
    "A Python module raised ValueError in bundle.rs under __main__ "
    "and printed a traceback."
)


def test_a_fixture_identity_naming_an_implementation_fails(tmp_path: Path) -> None:
    corpus = fixture(
        tmp_path / "fixtures",
        "a-boundary-the-rust-build-inserts",
        manifest("Two emitted regions are separated by one blank line."),
    )
    found = corpus_references(corpus)
    assert [reference.found for reference in found] == ["rust"]


def test_a_report_entry_naming_an_implementation_fails(clean: Path) -> None:
    design = DESIGN.replace("Block boundaries", "Block boundaries in the Rust build")
    found = report_references(design, clean, ())
    assert {reference.found for reference in found} == {"Rust"}
    assert all(
        reference.where.startswith("the conformance report, line ")
        for reference in found
    )


def test_a_report_of_a_corpus_stating_behaviour_alone_passes(clean: Path) -> None:
    assert report_references(DESIGN, clean, ()) == []


def test_a_reported_code_the_contract_declares_nowhere_is_scanned(
    clean: Path,
) -> None:
    found = report_references(DESIGN, clean, ("RUST",))
    assert [reference.found for reference in found] == ["RUST"]
    assert found[0].where.startswith("the conformance report, line ")


def test_the_contract_declares_its_interface_terms() -> None:
    declared = declared_names(DOCUMENTATION)
    assert "E_ROOT_NOT_FOUND" in declared
    assert "W_ENTRY_DESTINATION" in declared
    assert "4" in declared
    assert "--diagnostics {text,json}" in declared


def test_the_inventory_names_none_of_the_contract_s_declared_names() -> None:
    assert declared_references(DOCUMENTATION) == []


def test_a_declared_name_that_named_an_implementation_would_fail() -> None:
    documentation = DOCUMENTATION.replace("--root DIR", "--python-path DIR")
    found = declared_references(documentation)
    assert [reference.found for reference in found] == ["python"]
    assert found[0].where == "the contract's declared name --python-path DIR"


def test_a_term_is_a_whole_word_rather_than_a_substring() -> None:
    assert scan("A node in the bundle, and a crated object.", "where") == []
    assert [reference.found for reference in scan("Node.js reads it.", "where")] == [
        "Node.js"
    ]
    assert [reference.found for reference in scan("The node.js build", "where")] == [
        "node.js"
    ]


def test_a_term_is_stated_once_in_the_inventory() -> None:
    assert len(inventory()) == len({pattern.pattern for pattern, _ in inventory()})


def test_a_span_several_patterns_describe_is_read_as_the_term_it_is() -> None:
    found = scan("Node.js reads it.", "where")
    assert [reference.names for reference in found] == [
        "an implementation language or runtime"
    ]
