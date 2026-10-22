"""Assert the conformance report reads a design and a corpus as it states.

The report's input is a design document and a directory of fixtures, so
each case here supplies both: a design stating clauses in every form the
reader recognises, and a corpus naming some of them. A clause the corpus
names appears in the mapping against the fixture naming it, and one no
fixture names appears in the uncovered list, which is what a report run
against a deliberately unfixtured clause shows.

The declared surface is read from the same corpus. A code or an exit status
a fixture reaches is listed with that fixture; one only a fixture awaiting
later work declares is unfixturable, and the work it awaits is the reason;
one no fixture declares at all fails the report. The installation claims no
run observes are listed there too, each with the reason it is unreachable
and the smoke-run property that would observe it, and the closing summary
counts them. A case supplies a run observing a claimed property, which is
the condition under which a claim fails the report rather than printing.

The codes a build reports for itself are the surface's other side, so each
case supplies them directly and runs no build. A declared code the build
reports is listed as reported; a declared code it reports nowhere and a
reported code the contract declares nowhere each fail the report and are
listed; and an exit status, which is no code, states nothing either way.

Two further kinds of name are accounted for rather than measured. A section
the report declares as stating no behaviour carries no clause at all, it or
the rules beneath it, and is listed with the reason. A behavioural clause no
source tree and one invocation can state stays in the mapping, leaves the
uncovered list, and is listed with the reason and what states it instead.
The design below carries one of each so the report can be read against them.
"""

import json
from pathlib import Path
from typing import Any

import conformance
import pytest
from conformance import CLAIMS, RECORDED, SECTIONS, clauses, listed, render, report
from manifests import catalogue, severities

DESIGN = """# A design

Prose above the first section.

## Entry line

The bundle opens with a preamble of its own.

- **Link text:** The visible text of the heading the destination names.
- **Order:** Several entries are named in bundle order.

## Block boundaries

Insert blank-line separation between maximal emitted regions.

## Frontmatter policy

1. Accept and remove one optional leading UTF-8 BOM.
2. Close at the next physical line exactly equal to `---`.

## Resource limits

| Option | Default |
| --- | --- |
| `-F` | `256` |
| `-L` | `32,768` |

```text
- **Fenced:** a bullet inside a fence is an example rather than a rule.
```

## Design status

This section states what the project has decided about its builds.

- **Builds:** two of them carry the behaviour this contract states.

## Input and output contract

- **Entry references:** Accept one or more local document references.

## Agent delivery contract

Successful compilation establishes that the candidate passed validation.

- **Broken pipes:** Report transport failure through a nonzero exit.
"""


def declared_codes() -> tuple[str, ...]:
    """Every code the contract declares, as a build reporting all of them lists."""
    return tuple(
        sorted(code for severity in severities() for code in catalogue(severity))
    )


REPORTED = declared_codes()


def fixture(
    directory: Path,
    name: str,
    declared: list[str],
    status: int = 0,
    diagnostics: list[dict[str, str]] | None = None,
    awaiting: str | None = None,
) -> None:
    """One fixture in a corpus written for a test."""
    home = directory / "family" / name
    home.mkdir(parents=True)
    manifest: dict[str, Any] = {
        "description": name,
        "clauses": declared,
        "invocation": {"arguments": ["guide.md"]},
        "expected": {
            "exit_status": status,
            "stdout": "expected/stdout.md",
            "diagnostics": diagnostics or [],
        },
    }
    if awaiting is not None:
        manifest["awaiting"] = awaiting
    home.joinpath("manifest.toml").write_text(as_toml(manifest), encoding="utf-8")


def as_toml(manifest: dict[str, Any]) -> str:
    """The manifest as the TOML a fixture carries."""
    lines = [f"description = {json.dumps(manifest['description'])}", ""]
    lines.append("clauses = [")
    lines += [f"  {json.dumps(name)}," for name in manifest["clauses"]]
    lines += ["]", ""]
    if "awaiting" in manifest:
        lines += [f"awaiting = {json.dumps(manifest['awaiting'])}", ""]
    lines += ["[invocation]", 'arguments = ["guide.md"]', ""]
    lines += [
        "[expected]",
        f"exit_status = {manifest['expected']['exit_status']}",
        'stdout = "expected/stdout.md"',
    ]
    if not manifest["expected"]["diagnostics"]:
        lines.append("diagnostics = []")
    for diagnostic in manifest["expected"]["diagnostics"]:
        lines += ["", "[[expected.diagnostics]]"]
        lines += [f"{key} = {json.dumps(value)}" for key, value in diagnostic.items()]
    return "\n".join(lines) + "\n"


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    """A corpus naming some of the design's clauses and not others."""
    directory = tmp_path / "fixtures"
    fixture(
        directory,
        "an-entry-line-naming-one-entry",
        ["Entry line — Link text", "Block boundaries, an unclosed fence"],
        diagnostics=[{"severity": "warning", "code": "W_ENTRY_DESTINATION"}],
    )
    fixture(
        directory,
        "a-limit-crossed",
        ["Resource limits — -F"],
        status=1,
        diagnostics=[{"severity": "error", "code": "E_RESOURCE_LIMIT"}],
    )
    fixture(
        directory,
        "a-source-changing-under-the-run",
        ["Frontmatter policy — step 1"],
        status=4,
        diagnostics=[{"severity": "error", "code": "E_SOURCE_CHANGED"}],
        awaiting="I00:E11:W24",
    )
    return directory


def names(design: str) -> list[str]:
    return [clause.name for clause in clauses(design)]


def test_a_clause_is_a_heading_or_an_enumerated_rule_under_one() -> None:
    assert names(DESIGN) == [
        "Entry line",
        "Entry line — Link text",
        "Entry line — Order",
        "Block boundaries",
        "Frontmatter policy",
        "Frontmatter policy — step 1",
        "Frontmatter policy — step 2",
        "Resource limits",
        "Resource limits — -F",
        "Resource limits — -L",
        "Input and output contract",
        "Input and output contract — Entry references",
        "Agent delivery contract",
        "Agent delivery contract — Broken pipes",
    ]


def test_a_clause_a_fixture_names_carries_that_fixture(corpus: Path) -> None:
    mapped = dict(
        (clause.name, where)
        for clause, where in report(DESIGN, corpus, REPORTED).mapping
    )
    entry = "family/an-entry-line-naming-one-entry"
    assert mapped["Entry line — Link text"] == (entry,)
    assert mapped["Resource limits — -F"] == ("family/a-limit-crossed",)


def test_a_clause_the_case_follows_carries_the_fixture_naming_it(
    corpus: Path,
) -> None:
    mapped = dict(
        (clause.name, where)
        for clause, where in report(DESIGN, corpus, REPORTED).mapping
    )
    assert mapped["Block boundaries"] == ("family/an-entry-line-naming-one-entry",)


def test_a_clause_no_fixture_names_is_uncovered(corpus: Path) -> None:
    uncovered = [clause.name for clause in report(DESIGN, corpus, REPORTED).uncovered]
    assert "Resource limits — -L" in uncovered
    assert "Entry line — Order" in uncovered
    assert "Entry line — Link text" not in uncovered


def test_a_declaration_naming_no_clause_fails_the_report(tmp_path: Path) -> None:
    directory = tmp_path / "fixtures"
    fixture(directory, "a-fixture-naming-nothing", ["Entry line — Invented"])
    found = report(DESIGN, directory, REPORTED)
    assert found.unnamed == (
        ("Entry line — Invented", ("family/a-fixture-naming-nothing",)),
    )
    assert found.failures


def test_a_name_a_fixture_reaches_carries_that_fixture(corpus: Path) -> None:
    surface = {entry.name: entry for entry in report(DESIGN, corpus, REPORTED).surface}
    assert surface["E_RESOURCE_LIMIT"].reached == ("family/a-limit-crossed",)
    assert surface["1"].reached == ("family/a-limit-crossed",)


def test_a_name_only_an_awaiting_fixture_declares_is_unfixturable(
    corpus: Path,
) -> None:
    surface = {entry.name: entry for entry in report(DESIGN, corpus, REPORTED).surface}
    assert surface["E_SOURCE_CHANGED"].unfixturable
    assert surface["E_SOURCE_CHANGED"].awaited == {
        "I00:E11:W24": ("family/a-source-changing-under-the-run",)
    }
    assert surface["4"].unfixturable


def test_a_name_no_fixture_declares_fails_the_report(corpus: Path) -> None:
    found = report(DESIGN, corpus, REPORTED)
    undeclared = [entry.name for entry in found.surface if entry.undeclared]
    assert "E_RAW_HTML" in undeclared
    assert any("E_RAW_HTML" in failure for failure in found.failures)


def test_an_installation_claim_is_listed_with_its_reason(corpus: Path) -> None:
    printed = render(report(DESIGN, corpus, REPORTED)).splitlines()
    claim = CLAIMS[0]
    assert f"installation claim {claim.name}: unfixturable, {claim.reason}" in printed


def test_an_installation_claim_names_the_property_that_would_observe_it(
    corpus: Path,
) -> None:
    printed = render(report(DESIGN, corpus, REPORTED)).splitlines()
    for claim in CLAIMS:
        where = printed.index(
            f"installation claim {claim.name}: unfixturable, {claim.reason}"
        )
        assert printed[where + 1] == (
            f"    observable once the smoke run observes a command {claim.observes}"
        )


def test_a_claim_names_a_property_no_run_observes(corpus: Path) -> None:
    assert [claim.name for claim in listed()] == [claim.name for claim in CLAIMS]
    assert not [
        failure
        for failure in report(DESIGN, corpus, REPORTED).failures
        if failure.startswith("installation claim")
    ]


def test_a_claim_the_run_observes_fails_the_report(
    corpus: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    claim = CLAIMS[0]
    monkeypatch.setattr(conformance, "OBSERVED", (claim.observes,))
    found = report(DESIGN, corpus, REPORTED)
    assert any(
        failure
        == (
            f"installation claim {claim.name} names a command {claim.observes}, "
            "which the smoke run observes, so the listing states a limit the "
            "corpus no longer has"
        )
        for failure in found.failures
    )


def test_a_claim_the_run_observes_leaves_the_listing(
    corpus: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    claim = CLAIMS[0]
    monkeypatch.setattr(conformance, "OBSERVED", (claim.observes,))
    printed = render(report(DESIGN, corpus, REPORTED))
    assert f"installation claim {claim.name}:" not in printed
    assert printed.splitlines()[-1].endswith(
        f", {len(CLAIMS) - 1} installation claim(s) no run observes"
    )


def test_the_summary_counts_the_installation_claims(corpus: Path) -> None:
    printed = render(report(DESIGN, corpus, REPORTED)).splitlines()
    assert printed[-1].endswith(
        f", {len(listed())} installation claim(s) no run observes"
    )


def test_a_declared_code_the_build_reports_is_listed_as_reported(
    corpus: Path,
) -> None:
    found = report(DESIGN, corpus, REPORTED)
    entry = {entry.name: entry for entry in found.surface}["E_RESOURCE_LIMIT"]
    assert entry.reported is True
    assert (
        "error E_RESOURCE_LIMIT: 1 fixture(s), the build reports it"
        in render(found).splitlines()
    )
    assert not any("E_RESOURCE_LIMIT" in failure for failure in found.failures)


def test_a_declared_code_the_build_reports_nowhere_fails_the_report(
    corpus: Path,
) -> None:
    reported = tuple(code for code in REPORTED if code != "E_RESOURCE_LIMIT")
    found = report(DESIGN, corpus, reported)
    assert [entry.name for entry in found.unreported] == ["E_RESOURCE_LIMIT"]
    assert (
        "error E_RESOURCE_LIMIT is declared by the contract and the build "
        "reports it nowhere" in found.failures
    )
    assert (
        "error E_RESOURCE_LIMIT: 1 fixture(s), the build reports it nowhere"
        in render(found).splitlines()
    )


def test_a_reported_code_the_contract_declares_nowhere_fails_the_report(
    corpus: Path,
) -> None:
    found = report(DESIGN, corpus, REPORTED + ("E_INVENTED",))
    assert found.surplus == ("E_INVENTED",)
    assert (
        "E_INVENTED is reported by the build and the contract declares it nowhere"
        in found.failures
    )
    assert (
        "reported code E_INVENTED: the contract declares it nowhere"
        in render(found).splitlines()
    )


def test_an_exit_status_states_nothing_about_what_the_build_reports(
    corpus: Path,
) -> None:
    found = report(DESIGN, corpus, ())
    statuses = [entry for entry in found.surface if entry.kind == "exit status"]
    assert statuses
    assert all(entry.reported is None for entry in statuses)
    assert "exit status 1: 1 fixture(s)" in render(found).splitlines()
    assert not any(failure.startswith("exit status 1") for failure in found.failures)


def test_the_summary_counts_both_directions_of_the_comparison(corpus: Path) -> None:
    found = report(DESIGN, corpus, ("E_RESOURCE_LIMIT", "E_INVENTED"))
    assert (
        f", {len(found.unreported)} declared code(s) the build reports nowhere, "
        f"1 reported code(s) the contract declares nowhere, "
        in render(found).splitlines()[-1]
    )


def test_the_report_is_reproduced_on_a_second_run(corpus: Path) -> None:
    assert render(report(DESIGN, corpus, REPORTED)) == render(
        report(DESIGN, corpus, REPORTED)
    )


def test_a_section_stating_no_behaviour_carries_no_clause() -> None:
    named = [clause.name for clause in clauses(DESIGN)]
    assert "Design status" not in named
    assert "Design status — Builds" not in named


def test_a_section_stating_no_behaviour_is_listed_with_its_reason(
    corpus: Path,
) -> None:
    printed = render(report(DESIGN, corpus, REPORTED)).splitlines()
    for section in SECTIONS:
        assert f"section {section.name}: non-behavioural, {section.reason}" in printed


def test_a_clause_no_run_states_is_not_uncovered(corpus: Path) -> None:
    found = report(DESIGN, corpus, REPORTED)
    named = [clause.name for clause, _ in found.mapping]
    uncovered = [clause.name for clause in found.uncovered]
    assert "Agent delivery contract — Broken pipes" in named
    assert "Agent delivery contract — Broken pipes" not in uncovered
    assert "Input and output contract" not in uncovered
    assert "Input and output contract — Entry references" in uncovered


def test_a_clause_no_run_states_is_listed_with_what_states_it(corpus: Path) -> None:
    printed = render(report(DESIGN, corpus, REPORTED)).splitlines()
    for clause in RECORDED:
        where = printed.index(f"clause {clause.name}: unfixturable, {clause.reason}")
        assert printed[where + 1] == f"    {clause.observable}"


def test_the_summary_counts_what_the_report_accounts_for(corpus: Path) -> None:
    printed = render(report(DESIGN, corpus, REPORTED)).splitlines()
    assert (
        f", {len(RECORDED)} clause(s) no run states, "
        f"{len(SECTIONS)} section(s) stating no behaviour, "
        f"{len(listed())} installation claim(s) no run observes"
    ) in printed[-1]
