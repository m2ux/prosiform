#!/usr/bin/env python3
"""Report why each corpus fixture differs from the expectations it declares.

A build under test produces output; the fixture declares the output it
expects. This module runs each fixture through the corpus runner and
classifies the difference, so a maintainer reads what kind of drift the
tree carries before deciding to accept it.

The classification is deliberately domain-free. It reads the declared
expectation and the produced output as text and answers four questions:
did the run's exit status move, did the run fail in itself, do the
diagnostics differ, and how do the bytes differ. Only the last is a
comparison of text, and it is reported as one of:

    identical         the run met the fixture (nothing to review)
    order             the same lines, differently ordered or separated
    only-insertions   every expected line survives; the run added lines
    only-deletions    every produced line is in the expectation
    both              lines were added and lines were removed
    rewritten         lines differ in place, so content changed

A status move or a failure in the run itself is reported before any byte
comparison, because a build that crashes or returns another exit status
has more wrong with it than its output, and accepting the output of such
a run records the fault as the expectation.

This is the gate a regeneration should pass. Regenerating every fixture
a red run names turns the build's behaviour into the corpus's truth, so a
defect the build carries becomes the fixture that states it. Reading the
triage first is what separates drift a change intended from a fault a
change introduced.

Usage:

    triage.py [--json] [--only CATEGORY] [FIXTURE ...]

    PROSIFORM_BUILD names the build under test, as the corpus requires.

With no fixture named, every fixture the run reports as failing is
reported. A fixture named on the command line is reported whatever its
verdict, so one fixture can be read while a change is in hand.
"""

import argparse
import difflib
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from manifests import CORPUS, MANIFEST_NAME, fixtures, identity, read
from runner import BuildNotConfigured, Result, run_fixture


class Drift(Enum):
    """What one fixture's difference is, read from the run and the text."""

    IDENTICAL = "identical"
    STATUS = "status"
    CRASH = "crash"
    DIAGNOSTICS = "diagnostics"
    ORDER = "order"
    INSERTIONS = "only-insertions"
    DELETIONS = "only-deletions"
    BOTH = "both"
    REWRITTEN = "rewritten"

    @property
    def needs_review(self) -> bool:
        """Whether a human must read the difference before accepting it.

        An identical fixture needs nothing. Everything else is reported,
        and the categories ordered before the text comparison are the ones
        a regeneration must not paper over.
        """
        return self is not Drift.IDENTICAL


@dataclass(frozen=True)
class Finding:
    """One fixture, the category its difference falls in, and the evidence."""

    fixture: str
    drift: Drift
    detail: tuple[str, ...] = ()


def lines(text: str) -> list[str]:
    """The lines of one document, with trailing blank lines dropped."""
    found = text.splitlines()
    while found and not found[-1].strip():
        found.pop()
    return found


def compare(produced: str, expected: str) -> tuple[Drift, tuple[str, ...]]:
    """The category two texts fall in, and the differing lines to show for it.

    The lines are compared as a multiset, so the question asked is whether
    a line survived rather than where it sits. A line the expectation
    holds and the run does not is a deletion; a line the run writes and the
    expectation does not hold is an insertion. Equal multisets in another
    order are the arrangement moving; a rewrite in place is both at once
    across a line count that did not change.
    """
    if produced == expected:
        return Drift.IDENTICAL, ()
    wrote, wanted = lines(produced), lines(expected)
    if wrote == wanted:
        return Drift.ORDER, ()
    written, declared = Counter(wrote), Counter(wanted)
    added, removed = written - declared, declared - written
    shown = tuple(
        one[1:]
        for one in difflib.unified_diff(wanted, wrote, "expected", "produced", n=0)
        if one[:1] in "+-" and one[:3] not in ("+++", "---")
    )[:8]
    if added and not removed:
        return Drift.INSERTIONS, shown
    if removed and not added:
        return Drift.DELETIONS, shown
    if len(wrote) == len(wanted):
        return Drift.REWRITTEN, shown
    return Drift.BOTH, shown


def produced_stdout(result: Result, fixture: Path) -> tuple[str, str] | None:
    """The produced and declared standard output, where the fixture declares bytes."""
    manifest = read(fixture / MANIFEST_NAME)
    declared = manifest.get("expected", {}).get("stdout")
    if not isinstance(declared, str):
        return None
    return result.stdout.decode("utf-8", "replace"), (
        (fixture / declared).read_text(encoding="utf-8")
    )


def declares_failure(manifest: dict) -> bool:
    """Whether the fixture declares the internal error as the outcome it expects.

    One fixture exercises the status an unexpected failure returns, so the
    error appearing in its run is the expectation rather than a fault the
    fixture reports.
    """
    return any(
        one.get("code") == "E_UNEXPECTED_INTERNAL_ERROR"
        for one in manifest.get("expected", {}).get("diagnostics", [])
    )


def classify(result: Result, fixture: Path) -> Finding:
    """One fixture's verdict, read as the category its difference falls in."""
    name = identity(fixture)
    manifest = read(fixture / MANIFEST_NAME)
    expected = manifest.get("expected", {})
    stderr = result.stderr.decode("utf-8", "replace")
    if "E_UNEXPECTED_INTERNAL_ERROR" in stderr and not declares_failure(manifest):
        return Finding(name, Drift.CRASH, tuple(stderr.strip().splitlines()[:1]))
    wanted = expected.get("exit_status")
    if result.exit_status != wanted:
        return Finding(
            name,
            Drift.STATUS,
            (f"declared {wanted}, produced {result.exit_status}",),
        )
    if result.passed:
        return Finding(name, Drift.IDENTICAL)
    both = produced_stdout(result, fixture)
    if both is None:
        codes = [one for one in result.differences if "diagnostics" in one.expectation]
        detail = tuple(one.summary for one in codes) or tuple(
            one.expectation for one in result.differences
        )
        return Finding(name, Drift.DIAGNOSTICS, detail[:4])
    drift, detail = compare(*both)
    if drift is Drift.IDENTICAL:
        return Finding(name, Drift.DIAGNOSTICS, ("stdout met; diagnostics differ",))
    return Finding(name, drift, detail)


def report(findings: list[Finding], verbose: bool) -> int:
    """One line per fixture, in category order, and a count per category."""
    counts: dict[Drift, int] = {}
    for one in findings:
        counts[one.drift] = counts.get(one.drift, 0) + 1
    for drift in Drift:
        if drift in counts:
            print(f"{drift.value:16} {counts[drift]}")
    print()
    for one in findings:
        if not one.drift.needs_review:
            continue
        print(f"{one.drift.value:16} {one.fixture}")
        if verbose:
            for line in one.detail:
                print(f"{'':18} {line}")
    return (
        0
        if not any(one.drift in (Drift.CRASH, Drift.STATUS) for one in findings)
        else 1
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="*", help="fixtures to report")
    parser.add_argument(
        "--json", action="store_true", help="report each finding as one JSON object"
    )
    parser.add_argument(
        "--only", action="append", default=[], help="report one category only"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show the differing lines"
    )
    arguments = parser.parse_args()
    if "PROSIFORM_BUILD" not in os.environ:
        print("triage: PROSIFORM_BUILD names the build under test", file=sys.stderr)
        return 2
    chosen = (
        [CORPUS / one for one in arguments.fixture]
        if arguments.fixture
        else list(fixtures())
    )
    try:
        findings = [
            classify(run_fixture(one), one)
            for one in sorted(chosen, key=lambda one: one.as_posix())
        ]
    except BuildNotConfigured as absent:
        print(f"triage: {absent}", file=sys.stderr)
        return 2
    if arguments.only:
        wanted = {one for one in arguments.only}
        findings = [one for one in findings if one.drift.value in wanted]
    if arguments.json:
        for one in findings:
            print(
                json.dumps(
                    {
                        "fixture": one.fixture,
                        "drift": one.drift.value,
                        "detail": list(one.detail),
                    }
                )
            )
        return (
            1
            if any(one.drift in (Drift.CRASH, Drift.STATUS) for one in findings)
            else 0
        )
    return report(findings, arguments.verbose)


if __name__ == "__main__":
    raise SystemExit(main())
