"""Hold the runbook to the scorer, the report and the runner it names.

The rubric decides every class the scorer gives, so a class the scorer adds
without a rubric row would reach a run with nothing to decide it. Each
runbook passes the runner its arguments through `ARGS`, so an option the
runner does not accept would stop a run at its first command. The baseline's
caps are the shakedown's own measurement, so a cap that does not follow its
largest session is a budget nothing measured.
"""

import re
from pathlib import Path

import pytest
from harness import HARNESSES
from report import DISPOSITION_NAMES
from run import (
    DEFAULT_HARNESS,
    DEFAULT_MODELS,
    DEFAULT_REPETITIONS,
    DEFAULT_SESSION_BUDGET,
    FORMS,
    matrix,
    options,
)
from score import Failure
from workflow import workflows

ROOT = Path(__file__).with_name("RUNBOOK.md")
MAKEFILE = Path(__file__).parent.parent.parent / "Makefile"
ROW = re.compile(r"^\| `([a-z_]+)` \|", re.MULTILINE)
PASSED = re.compile(r"ARGS='([^']*)'")
OPTION = re.compile(r"(?<!\S)(--[a-z][a-z-]*)")
FIGURE = re.compile(r"\d[\d ]{2,}")
BUDGET = re.compile(r"^EVAL_BUDGET_TOKENS := (\d+)$", re.MULTILINE)


def section(heading: str) -> str:
    """The runbook's text under one heading, up to the next of its level or above."""
    text = ROOT.read_text()
    level = heading.split(" ", 1)[0]
    start = text.index(f"\n{heading}\n")
    rest = text[start + len(heading) + 2 :]
    ends = [
        found.start()
        for found in re.finditer(rf"^#{{1,{len(level)}}} ", rest, re.MULTILINE)
    ]
    return rest[: ends[0]] if ends else rest


def accepted(capsys: pytest.CaptureFixture[str]) -> set[str]:
    """Every option the runner's own help names."""
    with pytest.raises(SystemExit):
        options(["--help"])
    return set(OPTION.findall(capsys.readouterr().out))


def test_the_rubric_decides_every_class_the_scorer_gives() -> None:
    assert set(ROW.findall(section("### By Class"))) == {str(f) for f in Failure}


def test_the_rubric_gives_the_dispositions_the_report_reads() -> None:
    assert ROW.findall(section("## Triage Rubric").split("\n### ", 1)[0]) == list(
        DISPOSITION_NAMES
    )


@pytest.mark.parametrize("runbook", ["## MVP Proof", "## Baseline", "## Edge Run"])
def test_each_runbook_passes_only_options_the_runner_accepts(
    runbook: str, capsys: pytest.CaptureFixture[str]
) -> None:
    passed = {
        option
        for args in PASSED.findall(section(runbook))
        for option in OPTION.findall(args)
    }
    assert passed
    assert passed <= accepted(capsys)


def measured(field: str) -> list[int]:
    """The figures one row of the baseline's shakedown table states."""
    baseline = section("## Baseline")
    table = baseline[baseline.index("### Shakedown") :]
    row = next(line for line in table.splitlines() if line.startswith(f"| {field} |"))
    return [int(figure.replace(" ", "")) for figure in FIGURE.findall(row)]


def recorded(field: str) -> str:
    """The value one row of the baseline's shakedown table states."""
    baseline = section("## Baseline")
    table = baseline[baseline.index("### Shakedown") :]
    row = next(line for line in table.splitlines() if line.startswith(f"| {field} |"))
    return row.split("|")[2].strip()


def test_the_default_model_is_the_one_the_runbook_records() -> None:
    """AC8: `--models` defaults to the model `RUNBOOK.md` records as the choice."""
    assert list(DEFAULT_MODELS) == [recorded("Model").split("`")[1]]


def test_the_default_harness_reaches_that_model() -> None:
    """AC8: the harness `--harness` defaults to is the one the runbook records."""
    assert DEFAULT_HARNESS == recorded("Harness").strip("`")


def test_the_session_cap_is_the_measured_largest_doubled() -> None:
    """AC10: the default cap follows the shakedown's largest session."""
    largest = measured("Fifth run")[-2]
    assert DEFAULT_SESSION_BUDGET == -(-largest * 2 // 10_000) * 10_000


def test_the_token_budget_covers_the_default_matrix_at_that_cap() -> None:
    """AC10: `EVAL_BUDGET_TOKENS` covers every session the default matrix starts."""
    found = BUDGET.search(MAKEFILE.read_text())
    assert found is not None
    sessions = DEFAULT_REPETITIONS * len(
        matrix(
            list(workflows()),
            list(DEFAULT_MODELS),
            list(FORMS),
            1,
            HARNESSES[DEFAULT_HARNESS],
        )
    )
    assert int(found.group(1)) >= sessions * DEFAULT_SESSION_BUDGET
