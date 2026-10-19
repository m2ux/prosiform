"""Assert the schema describes a complete fixture declaration and nothing else.

A fixture declares its source tree, its invocation, its expected standard
output, its expected exit status and its expected diagnostics in one
manifest. The schema requires all five, so a manifest leaving one out is
rejected as malformed rather than running with an expectation nobody
stated. A diagnostic's code comes from the catalogue its severity
selects, so a fixture cannot expect a failure the contract does not
define, and cannot declare a warning where an error belongs.

A fixture declaring behaviour the build has yet to deliver names the work
that delivers it. The schema states that name's shape, so the marker is
read by a tool rather than by a person, and a flag or a sentence in its
place is rejected.
"""

from typing import Any

import pytest
from manifests import catalogue, errors

DECLARATIONS = {
    "source tree": ("invocation", "root"),
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
        "invocation": {"root": "source", "arguments": ["guide.md"]},
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
        "invocation": {"root": "source", "arguments": ["guide.md"]},
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
    manifest["runner"] = "prototype"
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
