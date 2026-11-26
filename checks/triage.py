#!/usr/bin/env python3
"""Name each stale fixture under the drift category its difference falls in.

A behaviour change moves what the build produces while the corpus states
what it produced before, so a red run names many fixtures at once. This
module runs the fixtures through the corpus run and reports each fixture
the run fails under one category of `Drift`, so a change accepts the drift
it intended and leaves every other category for a reader. It reports and
classifies, and writes nothing: whether a difference is drift or a defect
is the reader's judgement.

The verdicts are the corpus run's own, read through `corpus.run_all`, so a
fixture that passes or awaits later work is no drift, and a fixture the run
fails is read by its result's `state`. A run that failed in itself is no
drift, as `runner.Result.state` states, so such a fixture is named apart
from every category. `classify` owns which category a moved output falls
in.

`--only CATEGORY` reports the fixtures in that category alone. Fixtures
named by identity are triaged alone, as `manifests.selected` resolves them.
A tree the corpus run passes produces no report. The build under test comes
from configuration, as the corpus run requires.
"""

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from difflib import SequenceMatcher
from enum import Enum
from pathlib import Path

from corpus import Outcome, Verdict, run_all
from manifests import (
    CORPUS,
    MANIFEST_NAME,
    UnknownFixture,
    fixtures,
    read,
    selected,
)
from runner import (
    BUNDLE_SUFFIX,
    DIAGNOSTICS,
    EXIT_STATUS,
    RUN_FOLDER_SUFFIX,
    STDOUT_TEXT,
    BuildNotConfigured,
    Result,
    State,
    build_under_test,
)


class Drift(Enum):
    """The categories a moved output falls in, each holding its report label.

    `STATUS` holds a run whose exit status differs from the manifest's;
    `STREAMS` one whose diagnostics or standard output differ; `LAYOUT` one
    writing another number of bundles than the manifest declares, or
    writing them outside one folder of its own; `NAMES` one writing the
    declared number of bundles under another name. The last four hold a run
    writing every declared bundle under its name with other content: lines
    only `INSERTED`, only `REMOVED`, each `REWRITTEN` one for one in place,
    or `BOTH` added and removed. The order is the order `classify` tries
    them in.
    """

    STATUS = "status"
    STREAMS = "streams"
    LAYOUT = "layout"
    NAMES = "names"
    INSERTED = "inserted"
    REMOVED = "removed"
    REWRITTEN = "rewritten"
    BOTH = "both"


def edits(expected: bytes, produced: bytes) -> set[Drift]:
    """The content categories of the edits turning one bundle into the other.

    Lines keep their endings, so a newline spelled another way or a final
    newline gained or lost is a line rewritten in place.
    """
    matcher = SequenceMatcher(
        None,
        expected.splitlines(keepends=True),
        produced.splitlines(keepends=True),
        autojunk=False,
    )
    found = set()
    for tag, start, end, begin, finish in matcher.get_opcodes():
        if tag == "insert":
            found.add(Drift.INSERTED)
        elif tag == "delete":
            found.add(Drift.REMOVED)
        elif tag == "replace":
            one_for_one = end - start == finish - begin
            found.add(Drift.REWRITTEN if one_for_one else Drift.BOTH)
    return found


def classify(result: Result, fixture: Path) -> Drift:
    """The category of one moved output: the first in `Drift`'s order that holds.

    A fixture whose run reports another status, other diagnostics or other
    output is that, whatever its bundles carry, and the run's bundles are
    read by layout and name before content. A run writing every bundle
    under its name is filed under the content category its edits share,
    and under `BOTH` when they share none. `result` must be in
    `State.MOVED`.
    """
    named = {one.expectation for one in result.differences}
    if EXIT_STATUS in named:
        return Drift.STATUS
    if named & {DIAGNOSTICS, STDOUT_TEXT}:
        return Drift.STREAMS
    declared = read(fixture / MANIFEST_NAME)["expected"].get("bundles", [])
    expected = {Path(path).name: (fixture / path).read_bytes() for path in declared}
    folders = {one.folder for one in result.written}
    if len(result.written) != len(expected) or None in folders or len(folders) > 1:
        return Drift.LAYOUT
    produced = {one.name: one.data for one in result.written}
    entries = {
        f"{str(folder).removesuffix(RUN_FOLDER_SUFFIX)}{BUNDLE_SUFFIX}"
        for folder in folders
    }
    if produced.keys() != expected.keys() or not entries <= expected.keys():
        return Drift.NAMES
    found = set().union(
        *(edits(data, produced[name]) for name, data in expected.items())
    )
    return found.pop() if len(found) == 1 else Drift.BOTH


@dataclass(frozen=True)
class Triage:
    """The fixtures a corpus run fails, sorted by what their runs did.

    `drifted` holds each fixture whose output moved, by identity, with its
    category; `failed` holds the identity of each whose run failed in
    itself.
    """

    drifted: tuple[tuple[str, Drift], ...]
    failed: tuple[str, ...]


def triage(found: Sequence[Path], outcomes: Sequence[Outcome]) -> Triage:
    """The fixtures the corpus run fails among `found`, each with its outcome.

    A fixture the run fails while its result meets the manifest fails for
    its sources or its marker, which no category describes, so it is left
    to the corpus run's report.
    """
    drifted = []
    failed = []
    for fixture, one in zip(found, outcomes, strict=True):
        if one.verdict is not Verdict.FAILED:
            continue
        if one.result.state is State.FAILED_IN_ITSELF:
            failed.append(one.result.fixture)
        elif one.result.state is State.MOVED:
            drifted.append((one.result.fixture, classify(one.result, fixture)))
    order = list(Drift)
    drifted.sort(key=lambda entry: (order.index(entry[1]), entry[0]))
    return Triage(tuple(drifted), tuple(failed))


def report(triaged: Triage, only: Drift | None = None) -> list[str]:
    """One line per fixture: each drifted one under its category, then each failed.

    A category selected reports its fixtures alone.
    """
    lines = [
        f"{name}: {drift.value}"
        for name, drift in triaged.drifted
        if only is None or drift is only
    ]
    if only is None:
        lines.extend(
            f"{name}: {State.FAILED_IN_ITSELF.value}" for name in triaged.failed
        )
    return lines


@dataclass(frozen=True)
class Request:
    """What one invocation of triage asks for.

    `only` holds the category reported alone, or nothing when every one is;
    `names` holds the identities of the fixtures to triage, and is empty when
    every fixture is.
    """

    only: Drift | None = None
    names: tuple[str, ...] = ()


def requested(argv: list[str]) -> Request:
    """The request a command line makes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only",
        choices=[one.value for one in Drift],
        help="report the fixtures in this drift category alone",
    )
    parser.add_argument(
        "names",
        nargs="*",
        default=[],
        metavar="IDENTITY",
        help="triage only the fixtures carrying these identities, each a path "
        "under fixtures/",
    )
    parsed = parser.parse_args(argv)
    only = None if parsed.only is None else Drift(parsed.only)
    return Request(only, tuple(parsed.names))


def main(corpus: Path = CORPUS, request: Request | None = None) -> int:
    """Triage the corpus or the fixtures named, and print the report.

    A request naming an identity no fixture carries, or a run with no
    build configured, fails before any fixture runs.
    """
    asked = request or Request()
    try:
        found = selected(asked.names, corpus) if asked.names else fixtures(corpus)
    except UnknownFixture as unknown:
        print(f"triage: {unknown}", file=sys.stderr)
        return 1
    try:
        build_under_test()
    except BuildNotConfigured as absent:
        print(f"triage: {absent}", file=sys.stderr)
        return 1
    for line in report(triage(found, run_all(found, corpus)), asked.only):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(request=requested(sys.argv[1:])))
