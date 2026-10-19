"""Run one corpus fixture and decide its result from the manifest alone.

A fixture declares an invocation and the standard output, exit status and
diagnostics that invocation must produce, and the paths it must leave
absent. This module performs the run and compares each against the
declaration, so a verdict comes from the manifest and the fixture's files
and from nothing else.

The build under test is named by configuration and invoked as a
subprocess: the environment variable `PROSIFORM_BUILD` holds its command
line, split as a shell splits one. Nothing here imports a package, names a
module or names a language, so the same comparison binds every
implementation of the contract. There is no default build and no
fallback: an absent configuration raises `BuildNotConfigured`, so a
fixture is never reported as holding against a build that never ran.

The runner supplies the allowed source root and asks for diagnostics as
data, which the contract's command line spells `--root DIR` and
`--diagnostics json`. A manifest writes neither, so a diagnostic's code is
compared as a value rather than as prose.

A difference names the expectation it belongs to and locates itself within
it. Standard output is compared as bytes and located by byte offset, since
the preservation invariant turns on newline spelling and the trailing
newline; each rendered window spells its control bytes, so a CRLF against
an LF is visible rather than invisible. Diagnostics are compared in order
on the fields the manifest declares, so one that is missing, extra or out
of order is reported as what it is. A path declared absent is checked
after the run, and a file found there is reported and removed, so a run
leaves the fixture directory as the manifest declares it.
"""

import json
import os
import shlex
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from manifests import (
    MANIFEST_NAME,
    errors,
    identity,
    missing_files,
    present_files,
    read,
)

BUILD = "PROSIFORM_BUILD"
BUILD_TIMEOUT = "PROSIFORM_BUILD_TIMEOUT"
DEFAULT_TIMEOUT = 60.0

MANIFEST = "manifest"
INVOCATION = "invocation"
EXIT_STATUS = "expected.exit_status"
STDOUT = "expected.stdout"
DIAGNOSTICS = "expected.diagnostics"
ABSENT = "expected.absent"

DECLARED_FIELDS = ("reference", "source")
WINDOW = 24


class BuildNotConfigured(Exception):
    """No build under test is configured, so no fixture has a result."""


@dataclass(frozen=True)
class Difference:
    """One expectation the run did not meet, and where it differed."""

    expectation: str
    summary: str
    detail: tuple[str, ...] = ()


@dataclass(frozen=True)
class Result:
    """One fixture's verdict and the run it was decided from."""

    fixture: str
    differences: tuple[Difference, ...]
    exit_status: int | None
    stdout: bytes
    stderr: bytes

    @property
    def passed(self) -> bool:
        """Whether the run met every expectation the manifest declares."""
        return not self.differences

    def report(self) -> str:
        """The verdict as text: the fixture, then each difference and its region."""
        if self.passed:
            return f"{self.fixture}: pass"
        lines = [f"{self.fixture}: fail"]
        for difference in self.differences:
            lines.append(f"  {difference.expectation}: {difference.summary}")
            lines.extend(f"    {line}" for line in difference.detail)
        return "\n".join(lines)


def build_under_test() -> list[str]:
    """The configured build's command line, as argument tokens."""
    command = os.environ.get(BUILD, "").strip()
    if not command:
        raise BuildNotConfigured(
            f"{BUILD} names the build under test; a fixture has no result without one"
        )
    return shlex.split(command)


def build_timeout() -> float:
    """The seconds a run is allowed, from configuration."""
    configured = os.environ.get(BUILD_TIMEOUT, "").strip()
    return float(configured) if configured else DEFAULT_TIMEOUT


def render(chunk: bytes) -> str:
    """One run of bytes, with every newline and control byte spelled out."""
    return repr(chunk)


def count(total: int, noun: str) -> str:
    """A count and its noun, agreeing in number."""
    return f"{total} {noun}" if total == 1 else f"{total} {noun}s"


def first_difference(expected: bytes, produced: bytes) -> int:
    """The offset of the first differing byte, or where the shorter run ends."""
    limit = min(len(expected), len(produced))
    for offset in range(limit):
        if expected[offset] != produced[offset]:
            return offset
    return limit


def position(data: bytes, offset: int) -> tuple[int, int]:
    """The one-based line and byte column the offset sits on."""
    line = data.count(b"\n", 0, offset) + 1
    column = offset - data.rfind(b"\n", 0, offset)
    return line, column


def compare_exit_status(expected: int, produced: int) -> list[Difference]:
    """The exit status against the category the manifest declares."""
    if produced == expected:
        return []
    summary = f"expected {expected}, the run exited {produced}"
    return [Difference(EXIT_STATUS, summary)]


def compare_stdout(expected: bytes, produced: bytes) -> list[Difference]:
    """Standard output against the expected bytes, located by byte offset."""
    if expected == produced:
        return []
    offset = first_difference(expected, produced)
    line, column = position(expected, min(offset, len(expected)))
    start = max(0, offset - WINDOW)
    detail = [
        f"{count(len(expected), 'byte')} expected, {len(produced)} produced",
        f"first difference at byte {offset}, expected line {line} column {column}",
        f"expected {render(expected[start : offset + WINDOW])}",
        f"produced {render(produced[start : offset + WINDOW])}",
    ]
    if len(produced) < len(expected) and offset == len(produced):
        short = len(expected) - len(produced)
        detail.append(f"the run's output ends {count(short, 'byte')} early")
    elif len(expected) < len(produced) and offset == len(expected):
        over = len(produced) - len(expected)
        detail.append(f"the run's output carries {count(over, 'byte')} beyond the end")
    return [Difference(STDOUT, "the bytes differ", tuple(detail))]


def compare_absent(fixture: Path, declared: Sequence[str]) -> list[Difference]:
    """Each path the manifest declares the run must leave absent.

    A file found at one of them is read for the report and then removed,
    so the fixture directory after a run is the directory its manifest
    declares, whatever the build did.
    """
    differences = []
    for name in declared:
        created = fixture / name
        if not created.exists():
            continue
        detail: tuple[str, ...] = ()
        if created.is_file():
            written = created.read_bytes()
            created.unlink()
            detail = (
                f"{count(len(written), 'byte')} written, "
                f"beginning {render(written[:WINDOW])}",
            )
        differences.append(Difference(ABSENT, f"the run created {name}", detail))
    return differences


def parse_diagnostics(stderr: bytes) -> tuple[list[dict[str, Any]], list[str]]:
    """The JSON objects standard error carries, and every line that is not one."""
    parsed: list[dict[str, Any]] = []
    malformed: list[str] = []
    for number, raw in enumerate(stderr.splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            value = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            malformed.append(f"line {number}: {render(raw)}")
            continue
        if isinstance(value, dict):
            parsed.append(value)
        else:
            malformed.append(f"line {number}: {render(raw)}")
    return parsed, malformed


def designator(diagnostic: dict[str, Any]) -> str:
    """A diagnostic named by the two fields every one of them carries."""
    severity = diagnostic.get("severity", "(no severity)")
    code = diagnostic.get("code", "(no code)")
    return f"{severity} {code}"


def sequence(designators: list[str]) -> str:
    """A diagnostic order, each entry numbered by its position."""
    if not designators:
        return "none"
    return ", ".join(
        f"{number} {entry}" for number, entry in enumerate(designators, start=1)
    )


def misplacements(expected: list[str], produced: list[str]) -> list[str]:
    """Each position where the run's diagnostics depart from the expected ones."""
    lines = []
    for index in range(max(len(expected), len(produced))):
        wanted = expected[index] if index < len(expected) else None
        got = produced[index] if index < len(produced) else None
        if wanted == got:
            continue
        where = f"position {index + 1}:"
        if wanted is None:
            lines.append(f"{where} {got} produced, which no expectation declares")
        elif got is None:
            lines.append(f"{where} {wanted} expected, the run emits none")
        else:
            lines.append(f"{where} {wanted} expected, {got} produced")
    return lines


def compare_fields(
    index: int, expected: dict[str, Any], produced: dict[str, Any]
) -> list[Difference]:
    """One diagnostic's further fields, on the fields the manifest declares."""
    differences = []
    for name in DECLARED_FIELDS:
        if name not in expected:
            continue
        if name not in produced:
            differences.append(
                Difference(
                    DIAGNOSTICS,
                    f"diagnostic {index} carries no {name}",
                    (f"expected {name} {expected[name]!r}",),
                )
            )
        elif produced[name] != expected[name]:
            differences.append(
                Difference(
                    DIAGNOSTICS,
                    f"diagnostic {index} carries another {name}",
                    (
                        f"expected {expected[name]!r}",
                        f"produced {produced[name]!r}",
                    ),
                )
            )
    return differences


def compare_diagnostics(
    declared: list[dict[str, Any]], stderr: bytes
) -> list[Difference]:
    """The diagnostic stream against the list the manifest declares, in order."""
    produced, malformed = parse_diagnostics(stderr)
    differences = []
    if malformed:
        differences.append(
            Difference(
                DIAGNOSTICS,
                "standard error carries a line that is not a JSON diagnostic",
                tuple(malformed),
            )
        )
    expected_order = [designator(diagnostic) for diagnostic in declared]
    produced_order = [designator(diagnostic) for diagnostic in produced]
    if expected_order != produced_order:
        if sorted(expected_order) == sorted(produced_order):
            differences.append(
                Difference(
                    DIAGNOSTICS,
                    "the expected diagnostics are emitted in another order",
                    (
                        f"expected {sequence(expected_order)}",
                        f"produced {sequence(produced_order)}",
                    ),
                )
            )
        else:
            summary = (
                f"the run emits {count(len(produced), 'diagnostic')} "
                f"where {count(len(declared), 'diagnostic')} is expected"
                if len(declared) == 1
                else f"the run emits {count(len(produced), 'diagnostic')} "
                f"where {count(len(declared), 'diagnostic')} are expected"
            )
            differences.append(
                Difference(
                    DIAGNOSTICS,
                    summary,
                    tuple(misplacements(expected_order, produced_order)),
                )
            )
    paired = zip(declared, produced, strict=False)
    for index, (expected, got) in enumerate(paired, start=1):
        if designator(expected) == designator(got):
            differences.extend(compare_fields(index, expected, got))
    return differences


def run_fixture(fixture: Path) -> Result:
    """One fixture run against the configured build and compared with its manifest."""
    name = identity(fixture)
    manifest = read(fixture / MANIFEST_NAME)
    malformed = (
        errors(manifest)
        + missing_files(fixture, manifest)
        + present_files(fixture, manifest)
    )
    if malformed:
        difference = Difference(
            MANIFEST,
            "the fixture is not one the schema describes",
            tuple(malformed),
        )
        return Result(name, (difference,), None, b"", b"")

    invocation = manifest["invocation"]
    expected = manifest["expected"]
    root = (fixture / invocation["root"]).resolve()
    argv = [
        *build_under_test(),
        "--root",
        str(root),
        "--diagnostics",
        "json",
        *invocation["arguments"],
    ]
    allowed = build_timeout()
    try:
        completed = subprocess.run(
            argv,
            cwd=fixture,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=allowed,
            check=False,
        )
    except subprocess.TimeoutExpired:
        difference = Difference(
            INVOCATION,
            f"the run did not complete within {allowed} seconds",
            (f"command {shlex.join(argv)}",),
        )
        return Result(name, (difference,), None, b"", b"")

    differences = [
        *compare_exit_status(expected["exit_status"], completed.returncode),
        *compare_stdout((fixture / expected["stdout"]).read_bytes(), completed.stdout),
        *compare_diagnostics(expected["diagnostics"], completed.stderr),
        *compare_absent(fixture, expected.get("absent", [])),
    ]
    return Result(
        name,
        tuple(differences),
        completed.returncode,
        completed.stdout,
        completed.stderr,
    )
