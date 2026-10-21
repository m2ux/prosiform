#!/usr/bin/env python3
"""Run every fixture the corpus holds against the build under test.

`runner.py` decides one fixture. This module walks the corpus, runs each
fixture through that runner in path order and decides the corpus's own
verdict from the results, so the figure the corpus reports comes from a
command rather than from a driver written for one run.

The corpus declares the contract in full, so a manifest may name the work
that delivers behaviour the build does not yet meet:

    awaiting = "I00:E03"

A fixture carrying that marker is expected to fail, and its failure
leaves the corpus's verdict green. A marked fixture that meets its
manifest fails the run instead, so the marker is lifted on the change
that makes it untrue rather than outliving the work it waits on. The
marker lives in the manifest beside the expectation it qualifies: a list
held elsewhere drifts from the fixtures it names, silently and in both
directions.

A failing fixture is named by its identity — its path under `fixtures/` —
and its differences are printed under it, so a red run names which
fixture and where it differed.

`--awaiting WORK` reports the fixtures declaring that work instead of
running the corpus, so a session starting a piece of work reads which
fixtures it unblocks before it changes anything. The name is matched as
the manifest declares it, so a marker naming an epic and one naming a
task within it are separate requests. The report reads manifests alone
and needs no build.

The build under test comes from configuration and from nowhere else. An
absent `PROSIFORM_BUILD` fails the run: a corpus that skips because it
found no build sits inside a passing suite saying nothing, and a fixture
is never reported as holding against a build that never ran.
"""

import argparse
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from manifests import CORPUS, MANIFEST_NAME, fixtures, identity, read
from runner import BuildNotConfigured, Result, build_under_test, run_fixture

AWAITING = "awaiting"


class Verdict(Enum):
    """What one fixture's run means for the corpus's verdict."""

    PASSED = "pass"
    FAILED = "fail"
    AWAITED = "awaited"
    UNEXPECTED_PASS = "unexpected pass"

    @property
    def fails_the_run(self) -> bool:
        """Whether a fixture reaching this verdict fails the corpus run."""
        return self in (Verdict.FAILED, Verdict.UNEXPECTED_PASS)


@dataclass(frozen=True)
class Outcome:
    """One fixture's verdict, the run behind it and the work it awaits."""

    result: Result
    awaiting: str | None

    @property
    def verdict(self) -> Verdict:
        """The verdict the run and the marker give together."""
        if self.awaiting is None:
            return Verdict.PASSED if self.result.passed else Verdict.FAILED
        return Verdict.UNEXPECTED_PASS if self.result.passed else Verdict.AWAITED

    def line(self) -> str:
        """The fixture's one-line verdict, naming the work it awaits."""
        verdict = self.verdict.value
        if self.awaiting is None:
            return f"{self.result.fixture}: {verdict}"
        return f"{self.result.fixture}: {verdict}, awaiting {self.awaiting}"

    def detail(self) -> list[str]:
        """Why this fixture fails the run, or nothing when it does not."""
        if not self.verdict.fails_the_run:
            return []
        if self.verdict is Verdict.UNEXPECTED_PASS:
            return [
                f"{self.result.fixture}: meets its manifest while awaiting "
                f"{self.awaiting}",
                f"  remove awaiting = {self.awaiting!r} from "
                f"{self.result.fixture}/{MANIFEST_NAME}",
            ]
        return self.result.report().splitlines()


def awaiting(manifest: dict[str, Any]) -> str | None:
    """The work a manifest declares it waits on, or nothing when it waits."""
    declared = manifest.get(AWAITING)
    return declared if isinstance(declared, str) else None


def outcome(fixture: Path) -> Outcome:
    """One fixture run against the build and read against its marker."""
    return Outcome(run_fixture(fixture), awaiting(read(fixture / MANIFEST_NAME)))


def tally(outcomes: Iterable[Outcome]) -> dict[Verdict, int]:
    """How many fixtures reached each verdict."""
    counted = dict.fromkeys(Verdict, 0)
    for one in outcomes:
        counted[one.verdict] += 1
    return counted


def summary(outcomes: list[Outcome]) -> str:
    """The corpus's verdict as a count of fixtures against each verdict."""
    counted = tally(outcomes)
    parts = [f"{counted[verdict]} {verdict.value}" for verdict in Verdict]
    return f"corpus check: {len(outcomes)} fixture(s), " + ", ".join(parts)


def report(outcomes: list[Outcome]) -> list[str]:
    """Every fixture's verdict, then why each failing one failed."""
    lines = [one.line() for one in outcomes]
    for one in outcomes:
        lines.extend(one.detail())
    lines.append(summary(outcomes))
    return lines


def unblocked(work: str, corpus: Path = CORPUS) -> list[Path]:
    """Every fixture declaring it awaits the named work, in path order.

    The name is compared as the manifest declares it, so a marker naming
    an epic and one naming a task within it answer separate requests.
    """
    return [
        fixture
        for fixture in fixtures(corpus)
        if awaiting(read(fixture / MANIFEST_NAME)) == work
    ]


def unblocked_report(work: str, corpus: Path = CORPUS) -> list[str]:
    """Each fixture the named work unblocks, then how many there are."""
    found = unblocked(work, corpus)
    return [identity(fixture, corpus) for fixture in found] + [
        f"awaiting {work}: {len(found)} fixture(s)"
    ]


def requested(argv: list[str]) -> str | None:
    """The work a request names, or nothing when the corpus is to be run."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--awaiting",
        metavar="WORK",
        help="report the fixtures declaring they await this work, in place of "
        "running the corpus",
    )
    named: str | None = parser.parse_args(argv).awaiting
    return named


def main(corpus: Path = CORPUS, *, awaited: str | None = None) -> int:
    """Run the corpus, or report what one piece of work unblocks."""
    if awaited is not None:
        for line in unblocked_report(awaited, corpus):
            print(line)
        return 0
    try:
        build_under_test()
    except BuildNotConfigured as absent:
        print(f"corpus check: {absent}", file=sys.stderr)
        return 1
    found = fixtures(corpus)
    if not found:
        print(f"corpus check: no fixture under {corpus}", file=sys.stderr)
        return 1
    outcomes = [outcome(fixture) for fixture in found]
    for line in report(outcomes):
        print(line)
    return 1 if any(one.verdict.fails_the_run for one in outcomes) else 0


if __name__ == "__main__":
    sys.exit(main(awaited=requested(sys.argv[1:])))
