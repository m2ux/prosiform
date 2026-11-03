"""Hold the runbook to the scorer, the report and the runner it names.

The rubric decides every class the scorer gives, so a class the scorer adds
without a rubric row would reach a run with nothing to decide it. Each
runbook passes the runner its arguments through `ARGS`, so an option the
runner does not accept would stop a run at its first command.
"""

import re
from pathlib import Path

import pytest
from report import DISPOSITION_NAMES
from run import options
from score import Failure

RUNBOOK = Path(__file__).with_name("RUNBOOK.md")
ROW = re.compile(r"^\| `([a-z_]+)` \|", re.MULTILINE)
PASSED = re.compile(r"ARGS='([^']*)'")
OPTION = re.compile(r"(?<!\S)(--[a-z][a-z-]*)")


def section(heading: str) -> str:
    """The runbook's text under one heading, up to the next of its level or above."""
    text = RUNBOOK.read_text()
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
