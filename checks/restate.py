#!/usr/bin/env python3
"""Restate each stale fixture's expected bundles from the build under test.

A change that moves bundle text or names by design leaves every fixture
pinning the old bytes stale. This module writes what the build now produces
into those fixtures, so the change is read as a diff of the corpus rather
than typed into each fixture it reaches.

The fixtures restated are the ones `triage.triage` files under a category
`WRITABLE` names, read from the corpus run's own outcomes, so a passing or
awaited fixture is never restated. Every other fixture triage names is
refused: named, left as it is, and the exit status is nonzero, so a run over
a red build cannot record a fault or a behaviour change as an expectation.

A restatement writes the bundles under `expected/` and the manifest's
`expected.bundles` entry, as `restate` states, and nothing else.

Without `--write` nothing is written, and each fixture that would be is
named. Fixtures named by identity are restated alone, as
`manifests.selected` resolves them. The build under test comes from
configuration, as the corpus run requires.
"""

import argparse
import copy
import json
import re
import sys
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from corpus import run_all
from manifests import CORPUS, MANIFEST_NAME, UnknownFixture, fixtures, read, selected
from runner import BuildNotConfigured, State, Written, build_under_test
from triage import Drift, triage

WRITABLE = frozenset(
    {Drift.NAMES, Drift.INSERTED, Drift.REMOVED, Drift.REWRITTEN, Drift.BOTH}
)
"""The categories restatement writes.

Each holds a run that reports what its manifest declares and writes the
declared number of bundles into one folder, so what moved is how the
fixture's bundles are spelled. A category absent from this set is refused.
"""

EXPECTED_TABLE = "[expected]"
BUNDLES_KEY = re.compile(r"[ \t]*bundles[ \t]*=[ \t]*\[")


class Unrestatable(ValueError):
    """A manifest whose `expected.bundles` entry cannot be edited in place."""


def restated_bundles(
    declared: Sequence[str], written: Sequence[Written]
) -> dict[str, bytes]:
    """Each bundle path declared after restatement, in the manifest's order.

    A declared bundle the run wrote under its name keeps its path. Each
    other declared path, in the manifest's order, takes the next name the
    run wrote that no declaration carries, those names taken in sorted
    order, within the declared path's directory. Each path holds the bytes
    the run wrote under its name. `written` must hold
    as many bundles as `declared`, as every category in `WRITABLE` does.
    """
    produced = {one.name: one.data for one in written}
    unclaimed = iter(sorted(produced.keys() - {Path(path).name for path in declared}))
    paths = [
        path
        if Path(path).name in produced
        else (PurePosixPath(path).parent / next(unclaimed)).as_posix()
        for path in declared
    ]
    return {path: produced[PurePosixPath(path).name] for path in paths}


def string_spans(text: str, opening: int) -> list[tuple[int, int]]:
    """The span of each string in the array opening at `opening`, in order."""
    spans: list[tuple[int, int]] = []
    depth = 0
    at = opening
    while True:
        character = text[at]
        if character == "[":
            depth += 1
        elif character == "]":
            depth -= 1
            if depth == 0:
                return spans
        elif character == "#":
            at = text.index("\n", at)
        elif character == "'":
            end = text.index("'", at + 1)
            spans.append((at, end + 1))
            at = end
        elif character == '"':
            end = at + 1
            while text[end] != '"':
                end += 2 if text[end] == "\\" else 1
            spans.append((at, end + 1))
            at = end
        at += 1


def bundles_spans(text: str) -> list[tuple[int, int]]:
    """The span of each string the `[expected]` table's `bundles` array holds."""
    table = None
    offset = 0
    for line in text.splitlines(keepends=True):
        header = line.split("#", 1)[0].strip()
        if header.startswith("["):
            table = header
        elif table == EXPECTED_TABLE:
            found = BUNDLES_KEY.match(line)
            if found:
                return string_spans(text, offset + found.end() - 1)
        offset += len(line)
    raise Unrestatable(f"no bundles entry under {EXPECTED_TABLE}")


def rewritten(text: str, manifest: dict[str, Any], paths: Sequence[str]) -> str:
    """The manifest with its `expected.bundles` entry naming `paths`.

    Each string of the entry naming another path is replaced by the new
    one and every other byte is copied through, so the manifest is never
    re-rendered and its non-ASCII text, layout and other declarations
    stay as written. The edit is read back and must parse to the manifest
    with that entry alone changed; a manifest it cannot reach so raises
    `Unrestatable`.
    """
    declared = manifest["expected"]["bundles"]
    if list(paths) == declared:
        return text
    spans = bundles_spans(text)
    if len(spans) != len(declared):
        raise Unrestatable("its bundles entry is not one string per bundle")
    edited = text
    for (start, end), old, new in reversed(
        list(zip(spans, declared, paths, strict=True))
    ):
        if old != new:
            quoted = json.dumps(new, ensure_ascii=False)
            edited = edited[:start] + quoted + edited[end:]
    intended = copy.deepcopy(manifest)
    intended["expected"]["bundles"] = list(paths)
    try:
        parsed = tomllib.loads(edited)
    except tomllib.TOMLDecodeError:
        parsed = None
    if parsed != intended:
        raise Unrestatable("its bundles entry cannot be edited in place")
    return edited


def restate(fixture: Path, written: Sequence[Written], write: bool) -> None:
    """Restate one fixture's bundles from what its run wrote.

    The files under `expected/` take the run's bytes, a declared bundle
    the run no longer writes is removed, and the manifest's
    `expected.bundles` entry names the bundles as the run named them, as
    `restated_bundles` and `rewritten` state. Exit status, diagnostics,
    standard output text, clauses, description and the awaited work are
    the fixture's contract and are never written. Without `write` the
    restatement is decided and nothing is written. A manifest whose entry
    cannot be edited raises `Unrestatable` before anything is written.
    """
    manifest_path = fixture / MANIFEST_NAME
    text = manifest_path.read_bytes().decode("utf-8")
    manifest = read(manifest_path)
    declared = manifest["expected"].get("bundles", [])
    bundles = restated_bundles(declared, written)
    edited = rewritten(text, manifest, list(bundles))
    if not write:
        return
    for path in declared:
        if path not in bundles:
            (fixture / path).unlink()
    for path, data in bundles.items():
        (fixture / path).write_bytes(data)
    if edited != text:
        manifest_path.write_bytes(edited.encode("utf-8"))


@dataclass(frozen=True)
class Request:
    """What one invocation of restatement asks for.

    `write` holds whether the restatement is written; `names` holds the
    identities of the fixtures to restate, and is empty when every fixture
    is.
    """

    write: bool = False
    names: tuple[str, ...] = ()


def requested(argv: list[str]) -> Request:
    """The request a command line makes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the restatement; without it, name each fixture it would write",
    )
    parser.add_argument(
        "names",
        nargs="*",
        default=[],
        metavar="IDENTITY",
        help="restate only the fixtures carrying these identities, each a path "
        "under fixtures/",
    )
    parsed = parser.parse_args(argv)
    return Request(parsed.write, tuple(parsed.names))


def main(corpus: Path = CORPUS, request: Request | None = None) -> int:
    """Restate the corpus or the fixtures named, and name each fixture.

    Each fixture triage names is printed with its category, as restated,
    as one that would be, or as refused. Any refusal makes the status
    nonzero. A request naming an identity no fixture carries, or a run with
    no build configured, fails before any fixture runs.
    """
    asked = request or Request()
    try:
        found = selected(asked.names, corpus) if asked.names else fixtures(corpus)
    except UnknownFixture as unknown:
        print(f"restate: {unknown}", file=sys.stderr)
        return 1
    try:
        build_under_test()
    except BuildNotConfigured as absent:
        print(f"restate: {absent}", file=sys.stderr)
        return 1
    outcomes = run_all(found, corpus)
    runs = {
        one.result.fixture: (fixture, one.result)
        for fixture, one in zip(found, outcomes, strict=True)
    }
    triaged = triage(found, outcomes)
    done = "restated" if asked.write else "would restate"
    refused = [f"{name}: {State.FAILED_IN_ITSELF.value}" for name in triaged.failed]
    for name, drift in triaged.drifted:
        if drift not in WRITABLE:
            refused.append(f"{name}: {drift.value}")
            continue
        fixture, result = runs[name]
        try:
            restate(fixture, result.written, asked.write)
        except Unrestatable as reason:
            refused.append(f"{name}: {drift.value}, {reason}")
            continue
        print(f"{done} {name}: {drift.value}")
    for line in refused:
        print(f"refused {line}")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main(request=requested(sys.argv[1:])))
