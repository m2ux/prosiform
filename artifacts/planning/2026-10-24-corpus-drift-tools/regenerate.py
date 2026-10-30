#!/usr/bin/env python3
"""Restate a corpus fixture's expectations from the build's own run.

A corpus fixture declares an invocation and the standard output, exit
status and diagnostics that invocation must produce. When a change moves
what the build produces by design, the declaration is what goes stale,
and this module rewrites it from a run the build under test performs.
What it never rewrites is the fixture's input: the source tree, the
description, the clauses and the invocation stay as the fixture wrote
them, so what changes is what the fixture expects of an input and never
the input the expectation is about.

Three properties make the rewrite safe to run:

*Dry by default.* Without `--write` a fixture is reported and left
alone, so the set a change would rewrite is read before any of it is
written.

*Surgical.* Only the declared standard output file and the `[expected]`
block of `manifest.toml` are replaced. The manifest around that block is
copied through byte for byte, so a run never reformats the file, escapes
a non-ASCII clause, or reorders the declarations a fixture carries.

*Refuses a fault.* A run that reports an internal error is not an
expectation: the build failed, so there is nothing to restate. Such a
fixture is named and skipped, and the exit status is nonzero, so a
pipeline that regenerates on a red build cannot record a crash as truth.

Usage:

    regenerate.py [--write] [--only DRIFT] [FIXTURE ...]

    PROSIFORM_BUILD names the build under test, as the corpus requires.

With no fixture named, every fixture the build's run disagrees with is
considered. `--only` restricts the rewrite to one category of drift as
`triage.py` names it, which is how a change accepts the drift it
intended and leaves the rest for a reader.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from manifests import CORPUS, MANIFEST_NAME, fixtures, identity, read
from triage import Drift, classify, run_fixture

BUILD = "PROSIFORM_BUILD"
DECLARED = ("reference", "resolved", "source", "chain")
EXPECTED = "[expected]"


def quote(value: str) -> str:
    """One TOML basic string, keeping the characters the fixture wrote.

    A control character has no place in a basic string, so it is written as
    the escape the grammar names it by. A heading's text can carry a line
    break the candidate reads across two lines, and the declaration still
    states the exact text that heading carries.
    """
    escaped = []
    for character in value:
        if character == "\\":
            escaped.append("\\\\")
        elif character == '"':
            escaped.append('\\"')
        elif character == "\n":
            escaped.append("\\n")
        elif character == "\r":
            escaped.append("\\r")
        elif character == "\t":
            escaped.append("\\t")
        elif ord(character) < 0x20 or ord(character) == 0x7F:
            escaped.append(f"\\u{ord(character):04X}")
        else:
            escaped.append(character)
    return '"' + "".join(escaped) + '"'


def render(value: object) -> str:
    """One TOML value, as a manifest spells it."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(render(one) for one in value) + "]"
    return quote(str(value))


def diagnostics(stderr: bytes) -> list[dict]:
    """The diagnostics a run emitted, as a manifest declares them."""
    found = []
    for line in stderr.decode("utf-8", "replace").splitlines():
        if not line.strip():
            continue
        one = json.loads(line)
        kept = {key: one[key] for key in DECLARED if key in one}
        found.append({"severity": one["severity"], "code": one["code"], **kept})
    return found


def block(manifest: dict, status: int, found: list[dict]) -> str:
    """The `[expected]` block a run's outcome states."""
    expected = manifest.get("expected", {})
    lines = [EXPECTED, f"exit_status = {status}"]
    for key in ("stdout", "stdout_contains"):
        if key in expected:
            lines.append(f"{key} = {render(expected[key])}")
    if expected.get("absent"):
        lines.append(f"absent = {render(expected['absent'])}")
    for one in found:
        lines.append("")
        lines.append("[[expected.diagnostics]]")
        for key in ("severity", "code", *DECLARED):
            if key in one:
                lines.append(f"{key} = {render(one[key])}")
    return "\n".join(lines) + "\n"


def rewrite(text: str, manifest: dict, status: int, found: list[dict]) -> str:
    """The manifest with its `[expected]` block replaced and nothing else.

    A manifest that declares no block is refused rather than guessed at,
    because where the block belongs is the fixture's own shape and not
    something a run knows.
    """
    at = text.find(EXPECTED)
    if at < 0:
        raise ValueError(f"no {EXPECTED} block to replace")
    return text[:at] + block(manifest, status, found)


def restore(fixture: Path, write: bool) -> bool:
    """Restate one fixture from its run, reporting whether anything moved."""
    manifest = read(fixture / MANIFEST_NAME)
    result = run_fixture(fixture)
    found = diagnostics(result.stderr)
    text = (fixture / MANIFEST_NAME).read_text(encoding="utf-8")
    restated = rewrite(text, manifest, result.exit_status or 0, found)
    destination = manifest.get("expected", {}).get("stdout")
    moved = restated != text or (
        isinstance(destination, str)
        and (fixture / destination).read_bytes() != result.stdout
    )
    if write:
        if isinstance(destination, str):
            (fixture / destination).write_bytes(result.stdout)
        (fixture / MANIFEST_NAME).write_text(restated, encoding="utf-8")
    return moved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="*", help="fixtures to restate")
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the restatement; absent, report only",
    )
    parser.add_argument(
        "--only", action="append", default=[], help="restate one category of drift"
    )
    arguments = parser.parse_args()
    if BUILD not in os.environ:
        print(f"regenerate: {BUILD} names the build under test", file=sys.stderr)
        return 2
    chosen = (
        [CORPUS / one for one in arguments.fixture]
        if arguments.fixture
        else list(fixtures())
    )
    refused: list[str] = []
    moved: list[str] = []
    for one in sorted(chosen, key=lambda each: each.as_posix()):
        finding = classify(run_fixture(one), one)
        if arguments.only and finding.drift.value not in set(arguments.only):
            continue
        if finding.drift in (Drift.CRASH, Drift.STATUS):
            refused.append(f"{identity(one)}: {finding.drift.value}")
            continue
        if not finding.drift.needs_review:
            continue
        if restore(one, arguments.write):
            moved.append(identity(one))
    verb = "wrote" if arguments.write else "would write"
    for one in moved:
        print(f"{verb} {one}")
    for one in refused:
        print(f"refused {one}", file=sys.stderr)
    print(
        f"regenerate: {len(moved)} fixture(s) {verb}, "
        f"{len(refused)} refused, of {len(chosen)} considered",
        file=sys.stderr,
    )
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
