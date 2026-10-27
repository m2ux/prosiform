"""Assert the schema describes a complete fixture declaration and nothing else.

A fixture declares its invocation, its expected standard output, its
expected exit status and its expected diagnostics in one manifest. The
schema requires all four, so a manifest leaving one out is rejected as
malformed rather than running with an expectation nobody stated. The
source tree the run is confined to is declared beside the invocation's
arguments, and a manifest naming none declares a run supplied no allowed
source root. A diagnostic's code comes from the catalogue its severity
selects, so a fixture cannot expect a failure the contract does not
define, and cannot declare a warning where an error belongs.

Standard output is declared one way or the other: as the bytes the run
must reproduce, or, where the whole of the response is a build's own, as
the text it must carry. A manifest declaring it both ways states its
output twice, and one declaring it neither way states nothing about the
stream, so each is rejected.

A diagnostic about a reference declares the fields that reference
carries, the inclusion chain among them, and a chain reaching nothing is
no chain. A diagnostic under a code naming several faults declares the
text its message carries, so the fixture states which fault it is.

A run that must leave a path untouched declares it, because a comparison
of the two streams says nothing about a file. The declaration carries
fixture-relative paths, one apiece, and a fixture whose run creates no
file leaves it out.

A fixture declaring behaviour the build has yet to deliver names the work
that delivers it. The schema states that name's shape, so the marker is
read by a tool rather than by a person, and a flag or a sentence in its
place is rejected.
"""

from typing import Any

import pytest
from manifests import catalogue, errors

DECLARATIONS = {
    "invocation": ("invocation", "arguments"),
    "expected standard output": ("expected", "stdout"),
    "expected exit status": ("expected", "exit_status"),
    "expected diagnostics": ("expected", "diagnostics"),
}


def complete() -> dict[str, Any]:
    """A manifest declaring all five things, with one diagnostic."""
    return {
        "description": "A reference outside the allowed source root fails.",
        "clauses": ["Reference normalization and path identity"],
        "invocation": {"cwd": "source", "arguments": ["guide.md"]},
        "expected": {
            "exit_status": 1,
            "stdout": "expected/stdout.md",
            "diagnostics": [
                {
                    "severity": "error",
                    "code": "E_SOURCE_OUTSIDE_ROOT",
                    "reference": "../outside.md",
                    "source": "guide.md:3",
                }
            ],
        },
    }


def succeeding() -> dict[str, Any]:
    """A manifest for a successful run, with one warning beside it."""
    return {
        "description": "A bundle carrying a resource reference warns on its "
        "portability and succeeds.",
        "clauses": ["Resources are text"],
        "invocation": {"cwd": "source", "arguments": ["guide.md"]},
        "expected": {
            "exit_status": 0,
            "stdout": "expected/stdout.md",
            "diagnostics": [
                {
                    "severity": "warning",
                    "code": "W_RESOURCE_PORTABILITY",
                    "reference": "diagram.png",
                    "source": "guide.md:5",
                }
            ],
        },
    }


def without(table: str, field: str) -> dict[str, Any]:
    manifest = complete()
    del manifest[table][field]
    return manifest


def test_a_complete_manifest_validates() -> None:
    assert errors(complete()) == []


def test_a_manifest_naming_no_source_tree_validates() -> None:
    """A run supplied no allowed source root is a run a manifest declares."""
    manifest = without("invocation", "cwd")
    manifest["expected"]["exit_status"] = 2
    manifest["expected"]["diagnostics"] = [
        {
            "severity": "error",
            "code": "E_INVALID_USAGE",
            "message_contains": ["-r"],
        }
    ]
    assert errors(manifest) == []


@pytest.mark.parametrize(("declaration", "field"), sorted(DECLARATIONS.items()))
def test_a_manifest_missing_one_declaration_fails(
    declaration: str, field: tuple[str, str]
) -> None:
    table, name = field
    assert errors(without(table, name)), (
        f"a manifest declaring no {declaration} passed validation"
    )


def test_a_manifest_missing_every_declaration_fails() -> None:
    manifest = complete()
    del manifest["invocation"]
    del manifest["expected"]
    assert len(errors(manifest)) == 2


def test_a_manifest_declaring_a_warning_validates() -> None:
    assert errors(succeeding()) == []


def test_an_unknown_error_code_fails() -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["code"] = "E_NOT_IN_THE_CATALOGUE"
    assert errors(manifest), "a code outside the catalogue passed validation"


def test_an_unknown_warning_code_fails() -> None:
    manifest = succeeding()
    manifest["expected"]["diagnostics"][0]["code"] = "W_NOT_IN_THE_CATALOGUE"
    assert errors(manifest), "a code outside the catalogue passed validation"


@pytest.mark.parametrize("code", sorted(catalogue("error")))
def test_every_code_in_the_error_catalogue_is_accepted(code: str) -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["code"] = code
    assert errors(manifest) == []


@pytest.mark.parametrize("code", sorted(catalogue("warning")))
def test_every_code_in_the_warning_catalogue_is_accepted(code: str) -> None:
    manifest = succeeding()
    manifest["expected"]["diagnostics"][0]["code"] = code
    assert errors(manifest) == []


@pytest.mark.parametrize("code", sorted(catalogue("warning")))
def test_an_error_naming_a_warning_code_fails(code: str) -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["code"] = code
    assert errors(manifest), f"an error diagnostic named {code} and validated"


@pytest.mark.parametrize("code", sorted(catalogue("error")))
def test_a_warning_naming_an_error_code_fails(code: str) -> None:
    manifest = succeeding()
    manifest["expected"]["diagnostics"][0]["code"] = code
    assert errors(manifest), f"a warning diagnostic named {code} and validated"


def test_a_diagnostic_naming_no_severity_fails() -> None:
    manifest = complete()
    del manifest["expected"]["diagnostics"][0]["severity"]
    assert errors(manifest), "a diagnostic belonging to no catalogue validated"


def test_a_diagnostic_naming_no_code_fails() -> None:
    manifest = complete()
    del manifest["expected"]["diagnostics"][0]["code"]
    assert errors(manifest)


def test_an_unknown_field_fails() -> None:
    manifest = complete()
    manifest["runner"] = "src"
    assert errors(manifest), "a field the schema does not describe passed validation"


def test_an_exit_status_outside_the_declared_categories_fails() -> None:
    manifest = complete()
    manifest["expected"]["exit_status"] = 5
    assert errors(manifest)


def test_an_expected_path_leaving_the_fixture_fails() -> None:
    manifest = complete()
    manifest["expected"]["stdout"] = "../elsewhere/stdout.md"
    assert errors(manifest)


def test_an_empty_diagnostic_list_is_a_declaration() -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"] = []
    assert errors(manifest) == []


def test_a_diagnostic_declaring_an_inclusion_chain_validates() -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["chain"] = ["guide.md", "../outside.md"]
    assert errors(manifest) == []


def test_an_empty_inclusion_chain_fails() -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["chain"] = []
    assert errors(manifest), "a chain reaching nothing passed validation"


def carrying_text() -> dict[str, Any]:
    """A manifest declaring the text an informational response carries."""
    manifest = complete()
    manifest["expected"]["exit_status"] = 0
    manifest["expected"]["diagnostics"] = []
    del manifest["expected"]["stdout"]
    manifest["expected"]["stdout_contains"] = ["prosiform ", "(skill-markdown-v3)"]
    return manifest


def test_a_manifest_declaring_the_text_standard_output_carries_validates() -> None:
    assert errors(carrying_text()) == []


def test_a_manifest_declaring_standard_output_both_ways_fails() -> None:
    manifest = carrying_text()
    manifest["expected"]["stdout"] = "expected/stdout.md"
    assert errors(manifest), "a manifest stating its output twice passed validation"


def test_a_manifest_declaring_standard_output_neither_way_fails() -> None:
    manifest = carrying_text()
    del manifest["expected"]["stdout_contains"]
    assert errors(manifest), "a manifest stating no output passed validation"


def test_an_empty_text_declaration_fails() -> None:
    manifest = carrying_text()
    manifest["expected"]["stdout_contains"] = []
    assert errors(manifest), "a declaration naming no text passed validation"


def test_a_text_entry_declared_twice_fails() -> None:
    manifest = carrying_text()
    manifest["expected"]["stdout_contains"] = ["prosiform ", "prosiform "]
    assert errors(manifest), "one entry declared twice passed validation"


def test_a_text_declaration_as_a_bare_string_fails() -> None:
    manifest = carrying_text()
    manifest["expected"]["stdout_contains"] = "prosiform "
    assert errors(manifest), "a bare string passed where the text is listed"


def test_a_diagnostic_declaring_the_text_its_message_carries_validates() -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["message_contains"] = ["../outside.md"]
    assert errors(manifest) == []


def test_a_diagnostic_declaring_no_message_text_validates() -> None:
    assert "message_contains" not in complete()["expected"]["diagnostics"][0]
    assert errors(complete()) == []


def test_an_empty_message_text_declaration_fails() -> None:
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["message_contains"] = []
    assert errors(manifest), "a declaration naming no text passed validation"


def test_a_whole_message_field_fails() -> None:
    """The message itself is one build's wording, so no manifest declares it."""
    manifest = complete()
    manifest["expected"]["diagnostics"][0]["message"] = "a reference outside the root"
    assert errors(manifest), "a whole message passed validation"


def test_a_manifest_declaring_an_absent_path_validates() -> None:
    manifest = complete()
    manifest["expected"]["absent"] = ["bundle.md"]
    assert errors(manifest) == []


def test_a_manifest_declaring_no_absent_path_validates() -> None:
    assert "absent" not in complete()["expected"]
    assert errors(complete()) == []


def test_an_empty_absent_list_fails() -> None:
    manifest = complete()
    manifest["expected"]["absent"] = []
    assert errors(manifest), "a declaration naming no path passed validation"


def test_an_absent_path_named_twice_fails() -> None:
    manifest = complete()
    manifest["expected"]["absent"] = ["bundle.md", "bundle.md"]
    assert errors(manifest), "one path declared twice passed validation"


def test_an_absent_path_leaving_the_fixture_fails() -> None:
    manifest = complete()
    manifest["expected"]["absent"] = ["../elsewhere/bundle.md"]
    assert errors(manifest)


def test_a_manifest_awaiting_an_epic_validates() -> None:
    manifest = complete()
    manifest["awaiting"] = "I00:E03"
    assert errors(manifest) == []


def test_a_manifest_awaiting_a_task_validates() -> None:
    manifest = complete()
    manifest["awaiting"] = "I00:E03:W02"
    assert errors(manifest) == []


def test_a_manifest_awaiting_nothing_validates() -> None:
    assert "awaiting" not in complete()
    assert errors(complete()) == []


@pytest.mark.parametrize(
    "named",
    ["", "E03", "I0:E03", "I00-E03", "I00:E03:W2", "later", "I00:E03 section"],
)
def test_awaiting_naming_no_work_fails(named: str) -> None:
    manifest = complete()
    manifest["awaiting"] = named
    assert errors(manifest), f"{named!r} passed as the work a fixture awaits"


def test_awaiting_as_a_flag_fails() -> None:
    manifest = complete()
    manifest["awaiting"] = True
    assert errors(manifest), "a bare flag passed where the work is named"


def test_a_manifest_naming_a_fault_validates() -> None:
    for named in ("source-changed", "internal"):
        manifest = complete()
        manifest["fault"] = named
        assert errors(manifest) == [], f"{named!r} refused as a fault a run performs"


def test_a_manifest_naming_no_fault_validates() -> None:
    assert "fault" not in complete()
    assert errors(complete()) == []


@pytest.mark.parametrize("named", ["", "source_changed", "SOURCE-CHANGED", "other"])
def test_a_fault_outside_the_declared_set_fails(named: str) -> None:
    manifest = complete()
    manifest["fault"] = named
    assert errors(manifest), f"{named!r} passed as a fault the contract declares"


def test_a_fault_as_a_flag_fails() -> None:
    manifest = complete()
    manifest["fault"] = True
    assert errors(manifest), "a bare flag passed where the fault is named"
