"""Hold the ledger check to the entry and exposure-set schemas.

An entry reproduces without the session that recorded it only while every
field a reader re-runs it from is present, so each required field is removed
in turn and the check must name it. The triage state is one of the four the
schema declares, with a reason. The exposure set carries both halves, and its
example half names every mode entry the worked example carries.
"""

import copy
from pathlib import Path
from typing import Any

import pytest

import ledger

ENTRY: dict[str, Any] = {
    "date": "2026-10-26",
    "invocation": {"command": "pf modes/plan-mode.md", "cwd": "example/work-planner"},
    "sources": [
        {
            "repository": "m2ux/prosiform",
            "revision": "6554db86" + "0" * 32,
            "path": "example/work-planner",
        }
    ],
    "observed": "The bundle omits the publish step's protocol.",
    "expected": "The bundle carries the protocol the publish step links.",
    "triage": {"state": "build defect", "reason": "The link resolves in source."},
}

REQUIRED = [
    ("date",),
    ("invocation",),
    ("invocation", "command"),
    ("invocation", "cwd"),
    ("sources",),
    ("sources", 0, "repository"),
    ("sources", 0, "revision"),
    ("sources", 0, "path"),
    ("observed",),
    ("expected",),
    ("triage",),
    ("triage", "state"),
    ("triage", "reason"),
]


def without(field: tuple[str | int, ...]) -> dict[str, Any]:
    """The entry with one field removed."""
    entry = copy.deepcopy(ENTRY)
    parent: Any = entry
    for part in field[:-1]:
        parent = parent[part]
    del parent[field[-1]]
    return entry


def test_a_complete_entry_is_accepted() -> None:
    assert ledger.entry_errors(ENTRY) == []


def test_an_entry_may_cite_a_run() -> None:
    assert ledger.entry_errors({**ENTRY, "run": "2026-10-26-plan-mode"}) == []


@pytest.mark.parametrize("field", REQUIRED, ids=lambda f: ".".join(map(str, f)))
def test_an_entry_missing_a_required_field_is_rejected(
    field: tuple[str | int, ...],
) -> None:
    errors = ledger.entry_errors(without(field))
    assert any(f"'{field[-1]}' is a required property" in error for error in errors)


def test_an_entry_bundling_no_source_is_rejected() -> None:
    assert ledger.entry_errors({**ENTRY, "sources": []})


def test_a_source_named_by_an_abbreviated_revision_is_rejected() -> None:
    entry = copy.deepcopy(ENTRY)
    entry["sources"][0]["revision"] = "6554db86"
    assert ledger.entry_errors(entry)


def test_an_invocation_other_than_pf_is_rejected() -> None:
    entry = copy.deepcopy(ENTRY)
    entry["invocation"]["command"] = "make check"
    assert ledger.entry_errors(entry)


@pytest.mark.parametrize(
    "state", ["design change", "corpus gap", "build defect", "no change"]
)
def test_each_declared_triage_state_is_accepted(state: str) -> None:
    entry = copy.deepcopy(ENTRY)
    entry["triage"]["state"] = state
    assert ledger.entry_errors(entry) == []


def test_an_unknown_triage_state_is_rejected() -> None:
    entry = copy.deepcopy(ENTRY)
    entry["triage"]["state"] = "wont fix"
    assert any(
        error.startswith("triage.state:") for error in ledger.entry_errors(entry)
    )


@pytest.mark.parametrize("reason", ["", "   "])
def test_a_blank_triage_reason_is_rejected(reason: str) -> None:
    entry = copy.deepcopy(ENTRY)
    entry["triage"]["reason"] = reason
    assert any(
        error.startswith("triage.reason:") for error in ledger.entry_errors(entry)
    )


def exposure() -> dict[str, Any]:
    """The recorded exposure set, parsed."""
    return ledger.read(ledger.EXPOSURE)


def test_the_recorded_exposure_set_is_accepted() -> None:
    assert ledger.exposure_errors(exposure()) == []


@pytest.mark.parametrize("half", ["example", "workspace"])
def test_an_exposure_set_missing_a_half_is_rejected(half: str) -> None:
    declaration = exposure()
    del declaration[half]
    errors = ledger.exposure_errors(declaration)
    assert any(f"'{half}' is a required property" in error for error in errors)


@pytest.mark.parametrize("half", ["example", "workspace"])
def test_an_exposure_set_with_an_empty_half_is_rejected(half: str) -> None:
    assert ledger.exposure_errors({**exposure(), half: []})


def test_an_exposure_set_omitting_a_mode_entry_is_rejected() -> None:
    declaration = exposure()
    omitted = declaration["example"].pop()
    errors = ledger.exposure_errors(declaration)
    assert any(omitted["command"].split(" ")[1] in error for error in errors)


def test_an_exposure_set_naming_an_absent_entry_is_rejected() -> None:
    declaration = exposure()
    declaration["example"].append(
        {"cwd": "example/work-planner", "command": "pf modes/absent-mode.md"}
    )
    assert any(
        "names no file" in error for error in ledger.exposure_errors(declaration)
    )


def test_the_recorded_ledger_is_accepted() -> None:
    assert ledger.check() == []


def test_an_empty_ledger_with_a_valid_exposure_set_is_accepted(
    tmp_path: Path,
) -> None:
    assert ledger.check(entries=tmp_path / "entries") == []


def test_an_entry_file_departing_from_the_schema_is_named(tmp_path: Path) -> None:
    (tmp_path / "2026-10-26-unreadable.toml").write_text(
        'date = "2026-10-26"\n', encoding="utf-8"
    )
    failures = ledger.check(entries=tmp_path)
    assert failures and all(
        failure.startswith("2026-10-26-unreadable.toml:") for failure in failures
    )
