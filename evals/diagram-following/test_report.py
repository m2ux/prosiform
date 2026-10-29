"""Hold the report to its rows, its roll-ups and its baseline differences.

Each test lays out a run's records by hand: a `run.json` and one
`session.json` per session, carrying only what the runner writes. The
recorded run holds two models over four cells, passes and several failure
classes among them, a session ended at its timeout with no usage or cost
recorded, and two sessions not started. The baseline holds two of those
cells, and one the run lacks.
"""

import json
from pathlib import Path
from typing import Any

import pytest
from report import (
    FAILURES,
    REPORT_JSON,
    REPORT_MD,
    RUN,
    SESSION,
    TIMEOUT,
    baseline_of,
    main,
    markdown,
    report,
)

HAIKU = "claude-haiku-5-5"
SONNET = "claude-sonnet-5-5"
USAGE = {
    "input_tokens": 1000,
    "output_tokens": 200,
    "cache_creation_input_tokens": 300,
    "cache_read_input_tokens": 400,
}

# Each session: model, workflow, scenario, form, failure, exit status, cost.
RECORDED: list[tuple[str, str, str, str, str | None, int | str, float | None]] = [
    (HAIKU, "linear", "straight-through", "bundle", None, 0, 0.10),
    (HAIKU, "linear", "straight-through", "bundle", None, 0, 0.20),
    (HAIKU, "linear", "straight-through", "bundle", None, 0, 0.30),
    (HAIKU, "linear", "straight-through", "bundle", "unfinished", TIMEOUT, None),
    (HAIKU, "looping", "two-rounds", "prose", None, 0, 0.40),
    (HAIKU, "looping", "two-rounds", "prose", "loop_miscount", 0, 0.20),
    (HAIKU, "branching", "high-severity", "tree", "skipped_state", 0, 0.30),
    (HAIKU, "branching", "high-severity", "tree", "missing_action", 0, 0.10),
    (SONNET, "linear", "straight-through", "bundle", None, 0, 0.50),
    (SONNET, "linear", "straight-through", "bundle", None, 0, 0.30),
]
NOT_STARTED = [
    {
        "model": SONNET,
        "workflow": "looping",
        "scenario": "two-rounds",
        "form": "prose",
        "repetition": repetition,
    }
    for repetition in (1, 2)
]


def counts(**nonzero: int) -> dict[str, int]:
    """Every failure class's count, zero but for those named."""
    return {failure: nonzero.get(failure, 0) for failure in FAILURES}


def base_cell(
    model: str, form: str, workflow: str, scenario: str, passed: int, **failed: int
) -> dict[str, Any]:
    """One baseline cell, its sessions its passes and failures."""
    total = passed + sum(failed.values())
    return {
        "model": model,
        "form": form,
        "workflow": workflow,
        "scenario": scenario,
        "sessions": total,
        "passed": passed,
        "pass_rate": round(passed / total, 4),
        "failures": counts(**failed),
    }


BASELINE = {
    "run_id": "reviewed",
    "date": "2026-10-20T09:00:00+00:00",
    "models": [HAIKU, SONNET],
    "repetitions": 4,
    "cost_usd": 3.5,
    "cells": [
        base_cell(HAIKU, "bundle", "linear", "straight-through", 2, unfinished=2),
        base_cell(HAIKU, "prose", "looping", "two-rounds", 2),
        base_cell(SONNET, "tree", "branching", "low-severity", 1, wrong_branch=1),
    ],
}


@pytest.fixture
def recorded(tmp_path: Path) -> Path:
    """A run's directory holding the recorded sessions and its run record."""
    directory = tmp_path / "results" / "recorded"
    repetitions: dict[tuple[str, ...], int] = {}
    for model, workflow, scenario, form, failure, status, cost in RECORDED:
        cell = (model, workflow, scenario, form)
        repetitions[cell] = repetitions.get(cell, 0) + 1
        place = directory.joinpath(*cell, str(repetitions[cell]))
        place.mkdir(parents=True)
        session = {
            "model": model,
            "workflow": workflow,
            "scenario": scenario,
            "form": form,
            "repetition": repetitions[cell],
            "command": ["claude", "-p"],
            "exit_status": status,
            "duration_seconds": 12.5,
            "usage": None if cost is None else USAGE,
            "cost_usd": cost,
            "result": None,
            "verdict": {
                "passed": failure is None,
                "failure": failure,
                "divergence": None if failure is None else 1,
                "expected": [],
                "actual": [],
                "actions": [],
            },
        }
        (place / SESSION).write_text(json.dumps(session))
    run = {
        "run_id": "recorded",
        "date": "2026-10-27T10:00:00+00:00",
        "options": {"models": f"{HAIKU},{SONNET}", "repetitions": 4},
        "command": ["claude", "-p"],
        "sessions": len(RECORDED) + len(NOT_STARTED),
        "started": len(RECORDED),
        "cost_usd": 2.75,
        "not_started": NOT_STARTED,
    }
    (directory / RUN).write_text(json.dumps(run))
    return directory


@pytest.fixture
def baseline(tmp_path: Path) -> Path:
    """A baseline file holding the reviewed run's cells."""
    path = tmp_path / "baseline.json"
    path.write_text(json.dumps(BASELINE))
    return path


def row(rows: list[dict[str, Any]], *values: str) -> dict[str, Any]:
    """The one row whose key begins with these values."""
    [found] = [
        item for item in rows if list(item.values())[: len(values)] == list(values)
    ]
    return found


def test_each_cell_gives_its_pass_rate_failures_timeouts_tokens_and_cost(
    recorded: Path, tmp_path: Path
) -> None:
    built = report(recorded, tmp_path / "absent.json")
    assert [list(cell.values())[:4] for cell in built["cells"]] == [
        [HAIKU, "bundle", "linear", "straight-through"],
        [HAIKU, "prose", "looping", "two-rounds"],
        [HAIKU, "tree", "branching", "high-severity"],
        [SONNET, "bundle", "linear", "straight-through"],
    ]
    cell = row(built["cells"], HAIKU, "bundle")
    assert (cell["sessions"], cell["passed"], cell["pass_rate"]) == (4, 3, 0.75)
    assert cell["failures"] == counts(unfinished=1)
    assert cell["timeouts"] == 1
    assert cell["tokens"] == {
        "input": 1000,
        "output": 200,
        "cache_creation": 300,
        "cache_read": 400,
    }
    assert cell["cost_usd"] == 0.2
    tree = row(built["cells"], HAIKU, "tree")
    assert tree["pass_rate"] == 0
    assert tree["failures"] == counts(skipped_state=1, missing_action=1)
    assert tree["timeouts"] == 0


def test_the_roll_ups_gather_each_model_and_form_and_each_model(
    recorded: Path, tmp_path: Path
) -> None:
    built = report(recorded, tmp_path / "absent.json")
    assert [list(item.values())[:2] for item in built["by_form"]] == [
        [HAIKU, "bundle"],
        [HAIKU, "prose"],
        [HAIKU, "tree"],
        [SONNET, "bundle"],
    ]
    haiku = row(built["by_model"], HAIKU)
    assert (haiku["sessions"], haiku["passed"], haiku["pass_rate"]) == (8, 4, 0.5)
    assert haiku["failures"] == counts(
        unfinished=1, loop_miscount=1, skipped_state=1, missing_action=1
    )
    assert haiku["timeouts"] == 1
    assert haiku["cost_usd"] == round(1.6 / 7, 6)
    sonnet = row(built["by_model"], SONNET)
    assert (sonnet["sessions"], sonnet["pass_rate"], sonnet["cost_usd"]) == (2, 1, 0.4)


def test_the_report_gives_the_run_cost_and_the_sessions_not_started(
    recorded: Path, tmp_path: Path
) -> None:
    built = report(recorded, tmp_path / "absent.json")
    assert built["run_id"] == "recorded"
    assert built["models"] == [HAIKU, SONNET] and built["repetitions"] == 4
    assert (built["sessions"], built["started"]) == (12, 10)
    assert built["cost_usd"] == 2.75
    assert built["not_started"] == NOT_STARTED


def test_without_a_baseline_no_row_is_compared(recorded: Path, tmp_path: Path) -> None:
    built = report(recorded, tmp_path / "absent.json")
    assert built["baseline"] is None
    for name in ("cells", "by_form", "by_model"):
        assert built["baseline_only"][name] == []
        for item in built[name]:
            assert item["in_baseline"] is None and item["difference"] is None


def test_each_row_carries_its_difference_from_the_baseline(
    recorded: Path, baseline: Path
) -> None:
    built = report(recorded, baseline)
    assert built["baseline"] == {
        "run_id": "reviewed",
        "date": "2026-10-20T09:00:00+00:00",
        "cost_usd": 3.5,
    }
    cell = row(built["cells"], HAIKU, "bundle")
    assert cell["in_baseline"] is True
    assert cell["difference"] == {
        "pass_rate": 0.25,
        "failures": counts(unfinished=-1),
    }
    prose = row(built["cells"], HAIKU, "prose")
    assert prose["difference"] == {
        "pass_rate": -0.5,
        "failures": counts(loop_miscount=1),
    }
    haiku = row(built["by_model"], HAIKU)
    assert haiku["difference"] == {
        "pass_rate": round(0.5 - 4 / 6, 4),
        "failures": counts(
            unfinished=-1, loop_miscount=1, skipped_state=1, missing_action=1
        ),
    }
    sonnet = row(built["by_model"], SONNET)
    assert sonnet["difference"] == {
        "pass_rate": 0.5,
        "failures": counts(wrong_branch=-1),
    }


def test_a_baseline_without_the_errored_class_still_compares(
    recorded: Path, tmp_path: Path
) -> None:
    """A baseline written before `errored` existed reads its absence as zero."""
    old = json.loads(json.dumps(BASELINE))
    for cell in old["cells"]:
        cell["failures"].pop("errored")
    path = tmp_path / "old-baseline.json"
    path.write_text(json.dumps(old))
    built = report(recorded, path)
    cell = row(built["cells"], HAIKU, "bundle")
    assert cell["in_baseline"] is True
    assert cell["difference"]["failures"]["errored"] == 0
    assert cell["difference"] == {
        "pass_rate": 0.25,
        "failures": counts(unfinished=-1),
    }


def test_rows_absent_from_either_side_are_marked(
    recorded: Path, baseline: Path
) -> None:
    built = report(recorded, baseline)
    for item in (
        row(built["cells"], HAIKU, "tree"),
        row(built["cells"], SONNET, "bundle"),
        row(built["by_form"], SONNET, "bundle"),
    ):
        assert item["in_baseline"] is False and item["difference"] is None
    assert built["baseline_only"] == {
        "cells": [
            {
                "model": SONNET,
                "form": "tree",
                "workflow": "branching",
                "scenario": "low-severity",
            }
        ],
        "by_form": [{"model": SONNET, "form": "tree"}],
        "by_model": [],
    }


def test_the_command_writes_the_report_beside_the_run(
    recorded: Path, baseline: Path
) -> None:
    assert main([str(recorded), "--baseline", str(baseline)]) == 0
    assert json.loads((recorded / REPORT_JSON).read_text()) == report(
        recorded, baseline
    )
    text = (recorded / REPORT_MD).read_text()
    assert "- **Sessions:** 10 of 12 started; 2 not started." in text
    assert "- **Baseline:** `reviewed`, 2026-10-20T09:00:00+00:00" in text
    assert (
        f"| `{HAIKU}` | `bundle` | `linear` | `straight-through` | 4 | 3 | 75% "
        "| +25 pts | unfinished 1 (-1) | 1 | 1000 / 200 / 300 / 400 | 0.2 |"
    ) in text
    assert (
        f"| `{SONNET}` | `bundle` | `linear` | `straight-through` | 2 | 2 | 100% "
        "| new | none | 0 |"
    ) in text
    assert f"- `{SONNET}` / `tree` / `branching` / `low-severity`" in text
    assert f"- `{SONNET}` / `looping` / `two-rounds` / `prose` / `2`" in text


def test_a_refused_run_gives_its_state_and_reason_and_no_row(
    tmp_path: Path, baseline: Path
) -> None:
    """A run every session of which errored has no pass rate to compare."""
    directory = tmp_path / "results" / "refused"
    directory.mkdir(parents=True)
    run = {
        "run_id": "refused",
        "date": "2026-10-27T11:00:00+00:00",
        "options": {"models": HAIKU, "repetitions": 1},
        "command": ["claude", "-p"],
        "state": "refused",
        "reason": "You've hit your weekly limit · resets Monday",
        "sessions": 1,
        "started": 1,
        "cost_usd": 0.0,
        "not_started": [],
    }
    (directory / RUN).write_text(json.dumps(run))
    built = report(directory, baseline)
    assert built["state"] == "refused"
    assert built["reason"] == "You've hit your weekly limit · resets Monday"
    assert built["baseline"] is None
    for name in ("cells", "by_form", "by_model"):
        assert built[name] == [] and built["baseline_only"][name] == []
    text = markdown(built)
    assert "- **State:** `refused`" in text
    assert "You've hit your weekly limit · resets Monday" in text
    assert "not compared" in text
    assert "Pass rate" not in text and "## By Model" not in text


def test_writing_the_baseline_follows_the_comparison_with_the_one_it_replaces(
    recorded: Path, baseline: Path
) -> None:
    compared = report(recorded, baseline)
    assert main([str(recorded), "--baseline", str(baseline), "--write-baseline"]) == 0
    assert json.loads((recorded / REPORT_JSON).read_text()) == compared
    written = json.loads(baseline.read_text())
    assert written == baseline_of(compared)
    assert written["run_id"] == "recorded" and written["repetitions"] == 4
    assert written["models"] == [HAIKU, SONNET] and written["cost_usd"] == 2.75
    assert set(written["cells"][0]) == {
        "model",
        "form",
        "workflow",
        "scenario",
        "sessions",
        "passed",
        "pass_rate",
        "failures",
    }
    again = report(recorded, baseline)
    for name in ("cells", "by_form", "by_model"):
        assert again["baseline_only"][name] == []
        for item in again[name]:
            assert item["difference"] == {"pass_rate": 0, "failures": counts()}
