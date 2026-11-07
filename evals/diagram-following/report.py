"""Report a diagram-following run and its difference from the baseline.

A run's directory holds `run.json` and, per session, a `session.json` under
`<model>/<workflow>/<scenario>/<form>/<repetition>/`. The report reads them
and writes `report.json` and `report.md` beside `run.json`.

A row gathers the sessions sharing a key. The report holds three levels:

- `cells`: one model, form, workflow and scenario;
- `by_form`: one model and form, across scenarios;
- `by_model`: one model, across forms and scenarios.

Each row gives its `sessions`, how many `passed`, the `pass_rate`, the
count of each failure class in `failures`, zero included, how many ended
at their timeout in `timeouts`, the mean `tokens` of each kind over the
sessions recording tokens, and the mean `cost_usd` over the sessions
recording a cost; a mean is null when no session records it. The report
also gives the run's id, date, models, repetitions, matrix size, sessions
started, tokens, the sessions it did not start, `managed`, the counts of
managed plugins, environment settings and hooks every session carried and
their fingerprint, as `run.json` records them, and its `cost_usd`: the
sum of every session's reported cost, errored sessions included, null when
no session reports one, as a harness reporting no cost leaves it.

Each failing session is listed in `failing` with its class and the
disposition the run's triage gave it, read from `dispositions.json` beside
`run.json`. That file maps a session's place in the matrix,
`<model>/<workflow>/<scenario>/<form>/<repetition>`, to its `disposition`,
one of `miss`, `defect` and `unclear`, and the `evidence` that decided it.
A failing session the file does not name carries a null disposition, so an
untriaged failure reads as one; a disposition outside the three, or an
entry naming no failing session, is refused.

The baseline is `evidence/baseline.json`, or the file `--baseline`
names. It holds a reviewed run's id, date, models, repetitions and cost,
and its `cells`, each with its key, `sessions`, `passed`, `pass_rate` and
`failures`; its `by_form` and `by_model` rows are summed from those cells.
With a baseline present, each row carries `in_baseline`, whether the
baseline holds a row of the same key, and when it does a `difference`: the
run's pass rate and failure counts less the baseline's. `baseline_only`
lists, per level, the keys of the baseline's rows the run lacks. With no
baseline, `in_baseline` and `difference` are null and `baseline_only` is
empty.

A run's `state` is `completed`, or `refused` for one every started session
of which took the `errored` verdict. A refused run is no result to compare:
the report names the state and the reason `run.json` records, the `reason`
being one session's own `result` text, and holds no row, so no pass rate
is given and nothing is compared with a baseline.

`--write-baseline` writes the run's cells as the baseline file, after the
report has been compared with the baseline it replaces. A run whose report
holds no cell, a refused run among them, writes no baseline and leaves the
file as it was.
"""

import argparse
import json
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

from score import Failure
from workflow import ROOT, CorpusError

SESSION = "session.json"
RUN = "run.json"
STATE = "state"
REASON = "reason"
COMPLETED = "completed"
REFUSED = "refused"
REPORT_JSON = "report.json"
REPORT_MD = "report.md"
DISPOSITIONS = "dispositions.json"
DISPOSITION_NAMES = ("miss", "defect", "unclear")
BASELINE = ROOT / "evidence" / "baseline.json"
TIMEOUT = "timeout"

FAILURES = tuple(str(failure) for failure in Failure)
LEVELS = {
    "cells": ("model", "form", "workflow", "scenario"),
    "by_form": ("model", "form"),
    "by_model": ("model",),
}
COUNTS = ("sessions", "passed", "pass_rate", "failures")

Row = dict[str, Any]


def names(value: str) -> list[str]:
    """A comma-separated option's names."""
    return [name.strip() for name in value.split(",") if name.strip()]


def sessions(run_directory: Path) -> list[Row]:
    """Every session record a run's directory holds, in path order."""
    return [
        json.loads(path.read_text()) for path in sorted(run_directory.rglob(SESSION))
    ]


def mean(values: Iterable[float], places: int) -> float | None:
    """The mean of some values, rounded, or null when there are none."""
    held = list(values)
    return round(sum(held) / len(held), places) if held else None


def rate(passed: int, total: int) -> float:
    """A pass rate, rounded to four places."""
    return round(passed / total, 4)


def tally(records: list[Row]) -> Row:
    """One row's figures over its session records."""
    passed = sum(1 for record in records if record["verdict"]["passed"])
    failures = dict.fromkeys(FAILURES, 0)
    for record in records:
        if record["verdict"]["failure"] is not None:
            failures[record["verdict"]["failure"]] += 1
    counts = [record["tokens"] for record in records if record.get("tokens")]
    costs = [record["cost_usd"] for record in records if record.get("cost_usd")]
    return {
        "sessions": len(records),
        "passed": passed,
        "pass_rate": rate(passed, len(records)),
        "failures": failures,
        "timeouts": sum(1 for record in records if record["exit_status"] == TIMEOUT),
        "tokens": mean(counts, 1),
        "cost_usd": mean(costs, 6),
    }


def grouped(
    rows: Iterable[Row], key: tuple[str, ...]
) -> dict[tuple[str, ...], list[Row]]:
    """Rows or records gathered by their values of a key, in key order."""
    groups: dict[tuple[str, ...], list[Row]] = {}
    for row in rows:
        groups.setdefault(tuple(row[field] for field in key), []).append(row)
    return dict(sorted(groups.items()))


def level(records: list[Row], key: tuple[str, ...]) -> list[Row]:
    """One level's rows over a run's session records."""
    return [
        {**dict(zip(key, values, strict=True)), **tally(group)}
        for values, group in grouped(records, key).items()
    ]


def summed(cells: list[Row], key: tuple[str, ...]) -> dict[tuple[str, ...], Row]:
    """A baseline's rows at one level, summed from its cells."""
    rows = {}
    for values, group in grouped(cells, key).items():
        total = sum(cell["sessions"] for cell in group)
        passed = sum(cell["passed"] for cell in group)
        rows[values] = {
            "sessions": total,
            "passed": passed,
            "pass_rate": rate(passed, total),
            "failures": {
                failure: sum(cell["failures"].get(failure, 0) for cell in group)
                for failure in FAILURES
            },
        }
    return rows


def difference(row: Row, base: Row) -> Row:
    """A row's pass rate and failure counts less its baseline row's."""
    return {
        "pass_rate": round(row["pass_rate"] - base["pass_rate"], 4),
        "failures": {
            failure: row["failures"][failure] - base["failures"].get(failure, 0)
            for failure in FAILURES
        },
    }


def compare(
    rows: list[Row], key: tuple[str, ...], base: dict[tuple[str, ...], Row] | None
) -> list[Row]:
    """Mark a level's rows against the baseline; give its keys the run lacks."""
    for row in rows:
        found = None if base is None else base.get(tuple(row[f] for f in key))
        row["in_baseline"] = None if base is None else found is not None
        row["difference"] = None if found is None else difference(row, found)
    if base is None:
        return []
    held = {tuple(row[field] for field in key) for row in rows}
    return [
        dict(zip(key, values, strict=True))
        for values in sorted(base)
        if values not in held
    ]


def report(run_directory: Path, baseline: Path = BASELINE) -> Row:
    """A run's report, compared with the baseline when that file exists.

    A refused run is reported as the refusal it is: its state and the
    reason `run.json` records, with no row and no baseline comparison, so
    its pass rates are never read as a result.
    """
    run = json.loads((run_directory / RUN).read_text())
    base = json.loads(baseline.read_text()) if baseline.is_file() else None
    state = run.get(STATE, COMPLETED)
    recorded = sessions(run_directory)
    records = [] if state == REFUSED else recorded
    costs = [record["cost_usd"] for record in recorded if record.get("cost_usd")]
    built: Row = {
        "run_id": run["run_id"],
        "date": run["date"],
        "state": state,
        "reason": run.get(REASON),
        "models": names(run["options"]["models"]),
        "repetitions": run["options"]["repetitions"],
        "sessions": run["sessions"],
        "started": run["started"],
        "harness": run.get("harness"),
        "managed": run["managed"],
        "tokens": run["tokens"],
        "cost_usd": round(sum(costs), 6) if costs else None,
        "not_started": run["not_started"],
        "failing": failing(run_directory, records),
        "baseline": None
        if base is None or state == REFUSED
        else {field: base[field] for field in ("run_id", "date")},
        "baseline_only": {},
    }
    for name, key in LEVELS.items():
        rows = level(records, key)
        base_rows = (
            None if base is None or state == REFUSED else summed(base["cells"], key)
        )
        built["baseline_only"][name] = compare(rows, key, base_rows)
        built[name] = rows
    return built


def place(record: Row) -> str:
    """A session's place in the matrix, as one path-like name."""
    return "/".join(
        str(record[field])
        for field in ("model", "workflow", "scenario", "form", "repetition")
    )


def failing(run_directory: Path, records: list[Row]) -> list[Row]:
    """Each failing session with its class and the disposition triage gave it."""
    path = run_directory / DISPOSITIONS
    given: dict[str, Row] = json.loads(path.read_text()) if path.is_file() else {}
    failed = {
        place(record): record["verdict"]["failure"]
        for record in records
        if record["verdict"]["failure"] is not None
    }
    for name, entry in given.items():
        if name not in failed:
            raise CorpusError(f"{DISPOSITIONS} names {name}, which did not fail")
        if entry.get("disposition") not in DISPOSITION_NAMES:
            raise CorpusError(
                f"{DISPOSITIONS} gives {name} {entry.get('disposition')!r}, "
                f"not one of {', '.join(DISPOSITION_NAMES)}"
            )
    return [
        {
            "session": name,
            "failure": failure,
            "disposition": given.get(name, {}).get("disposition"),
            "evidence": given.get(name, {}).get("evidence"),
        }
        for name, failure in failed.items()
    ]


def baseline_of(built: Row) -> Row:
    """The baseline a report's run gives: its identity and cells."""
    key = LEVELS["cells"]
    return {
        **{
            field: built[field]
            for field in (
                "run_id",
                "date",
                "models",
                "repetitions",
                "harness",
                "tokens",
            )
        },
        "cells": [
            {field: cell[field] for field in (*key, *COUNTS)} for cell in built["cells"]
        ],
    }


def percent(value: float) -> str:
    """A rate as a whole percentage."""
    return f"{value * 100:.0f}%"


def number(value: float | None) -> str:
    """A mean as the report prints it, a dash when there is none."""
    return "—" if value is None else f"{value:g}"


def change(row: Row) -> str:
    """A row's pass-rate difference from the baseline, in percentage points."""
    if row["in_baseline"] is None:
        return "—"
    if row["difference"] is None:
        return "new"
    return f"{row['difference']['pass_rate'] * 100:+.0f} pts"


def failures(row: Row) -> str:
    """A row's nonzero failure counts, each with its difference when nonzero."""
    shown = []
    for failure in FAILURES:
        count = row["failures"][failure]
        moved = row["difference"]["failures"][failure] if row["difference"] else 0
        if count or moved:
            shown.append(f"{failure} {count}" + (f" ({moved:+d})" if moved else ""))
    return ", ".join(shown) or "none"


def table(rows: list[Row], key: tuple[str, ...]) -> list[str]:
    """One level's rows as a Markdown table."""
    headers = [
        *(field.capitalize() for field in key),
        "Sessions",
        "Passed",
        "Pass rate",
        "Change",
        "Failures",
        "Timeouts",
        "Mean tokens",
        "Mean cost (USD)",
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + " --- |" * len(headers),
    ]
    for row in rows:
        cells = [
            *(f"`{row[field]}`" for field in key),
            str(row["sessions"]),
            str(row["passed"]),
            percent(row["pass_rate"]),
            change(row),
            failures(row),
            str(row["timeouts"]),
            number(row["tokens"]),
            number(row["cost_usd"]),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def managed_line(managed: Row) -> str:
    """The managed configuration every session carried, counted and unnamed."""
    if managed["fingerprint"] is None:
        return "- **Managed configuration:** none."
    return (
        f"- **Managed configuration:** {managed['plugins']} plugin(s), "
        f"{managed['environment']} environment setting(s) and "
        f"{managed['hooks']} hook(s), carried by every session; "
        f"fingerprint `{managed['fingerprint']}`."
    )


def markdown(built: Row) -> str:
    """A report as Markdown: the run, then each level, then what is missing."""
    base = built["baseline"]
    lines = [
        f"# Diagram-Following Report: {built['run_id']}",
        "",
        f"- **Run:** `{built['run_id']}`, {built['date']}; models "
        + ", ".join(f"`{model}`" for model in built["models"])
        + f"; {built['repetitions']} repetitions.",
        f"- **Sessions:** {built['started']} of {built['sessions']} started; "
        f"{len(built['not_started'])} not started.",
        f"- **Tokens:** {built['tokens']}.",
        managed_line(built["managed"]),
        "- **Cost:** no session reported a cost."
        if built["cost_usd"] is None
        else f"- **Cost:** USD {built['cost_usd']:g}.",
    ]
    if built["state"] == REFUSED:
        lines += [
            f"- **State:** `{REFUSED}` — every session reported an error, so the "
            "run entered no state and its pass rates are no result.",
            f"- **Reason:** {built['reason']}",
            "- **Baseline:** not compared, since a refused run has no pass rate.",
            "",
            "No row is given and nothing is compared with a baseline. Run the "
            "matrix again once the agent accepts sessions.",
        ]
        return "\n".join(lines) + "\n"
    lines += [
        "- **Baseline:** none."
        if base is None
        else f"- **Baseline:** `{base['run_id']}`, {base['date']}. "
        f"Change is this run's pass rate less "
        "the baseline's, and a failure count's change follows it in brackets.",
    ]
    titles = {
        "by_model": "By Model",
        "by_form": "By Model and Form",
        "cells": "By Model, Form and Scenario",
    }
    for name, title in titles.items():
        lines += ["", f"## {title}", "", *table(built[name], LEVELS[name])]
    absent = [
        " / ".join(f"`{value}`" for value in keys.values())
        for name in titles
        for keys in built["baseline_only"][name]
    ]
    if absent:
        lines += ["", "## Baseline Only", "", *(f"- {item}" for item in absent)]
    if built["failing"]:
        lines += [
            "",
            "## Failing Sessions",
            "",
            "| Session | Class | Disposition | Evidence |",
            "| --- | --- | --- | --- |",
        ]
        lines += [
            f"| `{item['session']}` | `{item['failure']}` | "
            f"{item['disposition'] or 'untriaged'} | {item['evidence'] or '—'} |"
            for item in built["failing"]
        ]
    if built["not_started"]:
        lines += ["", "## Not Started", ""]
        lines += [
            "- "
            + " / ".join(
                f"`{item[field]}`"
                for field in ("model", "workflow", "scenario", "form", "repetition")
            )
            for item in built["not_started"]
        ]
    return "\n".join(lines) + "\n"


def write(run_directory: Path, baseline: Path = BASELINE) -> Row:
    """Write a run's report beside its records and return it."""
    built = report(run_directory, baseline)
    (run_directory / REPORT_JSON).write_text(json.dumps(built, indent=2) + "\n")
    (run_directory / REPORT_MD).write_text(markdown(built))
    return built


def options(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """The report's options: the run directory and the baseline."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_directory", type=Path, help="results/<run-id>")
    parser.add_argument(
        "--baseline", type=Path, default=BASELINE, help="the baseline file"
    )
    parser.add_argument(
        "--write-baseline",
        action="store_true",
        help="write this run's cells as the baseline file",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Report a run from the command line, and write its baseline if asked."""
    arguments = options(argv)
    built = write(arguments.run_directory, arguments.baseline)
    if arguments.write_baseline:
        if not built["cells"]:
            reason = f": {built['reason']}" if built["reason"] else ""
            raise CorpusError(
                f"run {built['run_id']} measured no cell, so it writes no "
                f"baseline{reason}"
            )
        arguments.baseline.write_text(json.dumps(baseline_of(built), indent=2) + "\n")
    print(arguments.run_directory / REPORT_MD)
    return 0


if __name__ == "__main__":
    sys.exit(main())
