"""Run one corpus fixture and decide its result from the manifest alone.

A fixture declares an invocation and the bundles, exit status and
diagnostics that invocation must produce. This module performs the run and
compares each against the declaration, so a verdict comes from the manifest
and the fixture's files and from nothing else.

The build under test is named by configuration and invoked as a
subprocess: the environment variable `PROSIFORM_BUILD` holds its command
line, split as a shell splits one. Nothing here imports a package, names a
module or names a language, so the same comparison binds every
implementation of the contract. There is no default build and no
fallback: an absent configuration raises `BuildNotConfigured`, so a
fixture is never reported as holding against a build that never ran.

The runner uses the working directory the manifest names and asks
for diagnostics as data through `-d json`. A manifest omits that option, so a
diagnostic's code is compared as a value rather than as prose. A manifest
declaring no argument and no fault is the bare command, which reports no
diagnostic, so the runner invokes the build with nothing added. The runner
names no output folder, so a run writes where its own invocation sends it:
the working directory, or the folder the manifest's `-o` names.

A difference names the expectation it belongs to and locates itself within
it. Every file the run creates under the fixture or its working directory
is what the run wrote. A run writes its bundles into one folder of its own,
named for its entry bundle with the `.bundles` suffix, so each file is
compared by its name within that folder with the bundles the manifest
declares: a declared bundle the run did not write, a file no declaration
names, a file written outside a folder of the run's own, and a folder
named for no declared bundle are each a difference. Each file and folder
is read and removed, so every run starts from a directory holding no
output. A bundle is compared as bytes and
located by byte offset, since the preservation invariant turns on newline
spelling and the trailing newline; each rendered window spells its control
bytes, so a CRLF against an LF is visible rather than invisible. Standard
output carries no bundle, so it is empty unless the manifest declares the
text it carries. Diagnostics are compared in order on the fields the
manifest declares, so one that is missing, extra or out of order is
reported as what it is.

Two of the contract's outcomes are facts about the run rather than about
any document it reads, so no source tree states them. A manifest names
the fault its run meets and the runner asks the run for it, which the
contract's command line spells `-x NAME`: the fault is the run's
own, so what a fixture observes is the build's own detection rather than
a report the corpus asked for. A fault writes to the tree it runs over,
so a fixture declaring one runs in a copy of itself and the corpus
leaves the fixture as it found it.

Where the whole of an outcome is a build's own, the manifest declares the
text it must carry instead: `expected.stdout_contains` for a response such
as the one reporting a version, and a diagnostic's `message_contains` where
one error code names several distinct faults. Each entry is a substring the
output must contain, so what identifies the outcome is compared and the
wording around it is left to the build. A declaration absent compares
nothing.
"""

import json
import os
import shlex
import shutil
import subprocess
import tempfile
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from manifests import (
    MANIFEST_NAME,
    errors,
    identity,
    missing_files,
    read,
)

BUILD = "PROSIFORM_BUILD"
BUILD_TIMEOUT = "PROSIFORM_BUILD_TIMEOUT"
DEFAULT_TIMEOUT = 60.0

MANIFEST = "manifest"
FAULT = "fault"
INVOCATION = "invocation"
EXIT_STATUS = "expected.exit_status"
BUNDLES = "expected.bundles"
BUNDLE_SUFFIX = ".bundle.md"
RUN_FOLDER_SUFFIX = ".bundles"
STDOUT_TEXT = "expected.stdout_contains"
DIAGNOSTICS = "expected.diagnostics"

DECLARED_FIELDS = ("reference", "resolved", "source", "chain")
MESSAGE_TEXT = "message_contains"
MESSAGE = "message"
EXCERPT = 96
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


def compare_bundle(name: str, expected: bytes, produced: bytes) -> list[Difference]:
    """One written bundle against the expected bytes, located by byte offset."""
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
    return [Difference(BUNDLES, f"{name}: the bytes differ", tuple(detail))]


def excerpt(data: bytes) -> str:
    """A run of bytes for a report, shortened to a readable head."""
    if len(data) <= EXCERPT:
        return render(data)
    return f"{render(data[:EXCERPT])} and {count(len(data) - EXCERPT, 'byte')} more"


def absent_text(text: str, declared: Sequence[str]) -> list[str]:
    """Each declared entry the text does not carry."""
    return [entry for entry in declared if entry not in text]


def compare_stdout(declared: Sequence[str], produced: bytes) -> list[Difference]:
    """Standard output against the text the manifest declares it carries.

    A manifest declaring none declares an empty stream, since a run writes
    its bundles to files and standard output carries only a response.
    """
    if not declared:
        if not produced:
            return []
        return [
            Difference(
                STDOUT_TEXT,
                f"standard output carries {count(len(produced), 'byte')} where "
                "the manifest declares none",
                (f"produced {excerpt(produced)}",),
            )
        ]
    missing = absent_text(produced.decode("utf-8", errors="replace"), declared)
    if not missing:
        return []
    detail = [f"{entry!r} is absent" for entry in missing]
    detail.append(f"produced {excerpt(produced)}")
    summary = f"the output does not carry {count(len(missing), 'declared text')}"
    return [Difference(STDOUT_TEXT, summary, tuple(detail))]


def entries(*directories: Path) -> set[Path]:
    """Every file and folder under the directories, a linked one left unentered."""
    return {
        Path(walked, name)
        for directory in directories
        for walked, folders, names in os.walk(directory)
        for name in [*folders, *names]
    }


@dataclass(frozen=True)
class Written:
    """One file a run created: the folder of the run it sits in, and its bytes."""

    folder: str | None
    name: str
    data: bytes


def collected(created: set[Path]) -> list[Written]:
    """Each file the run created, by folder and name, removed with its folder."""
    folders = {path for path in created if path.is_dir() and not path.is_symlink()}
    written = []
    for path in sorted(created - folders):
        owned = path.parent.name if path.parent in folders else None
        written.append(Written(owned, path.name, path.read_bytes()))
        path.unlink()
    for folder in sorted(folders, key=lambda one: len(one.parts), reverse=True):
        folder.rmdir()
    return written


def compare_bundles(
    fixture: Path, declared: Sequence[str], written: Sequence[Written]
) -> list[Difference]:
    """The files the run wrote against the bundles the manifest declares, by name.

    A declared bundle is matched by its name within the folder the run
    wrote its bundles into, and that folder is named for one of them with
    the `.bundles` suffix.
    """
    expected = {Path(path).name: (fixture / path).read_bytes() for path in declared}
    produced: dict[str, bytes] = {}
    differences = []
    folders = sorted({one.folder for one in written if one.folder is not None})
    if len(folders) > 1:
        differences.append(
            Difference(
                BUNDLES, f"the run wrote into {len(folders)} folders", tuple(folders)
            )
        )
    for folder in folders:
        named = folder.removesuffix(RUN_FOLDER_SUFFIX)
        if expected and (named == folder or f"{named}{BUNDLE_SUFFIX}" not in expected):
            differences.append(
                Difference(
                    BUNDLES,
                    f"the run wrote its bundles into {folder}, which names no "
                    f"bundle the manifest declares",
                )
            )
    for one in written:
        if one.folder is None:
            differences.append(
                Difference(
                    BUNDLES, f"the run wrote {one.name} outside a folder of its own"
                )
            )
        if one.name in produced:
            differences.append(Difference(BUNDLES, f"the run wrote {one.name} twice"))
        elif one.name not in expected:
            differences.append(
                Difference(
                    BUNDLES,
                    f"the run wrote {one.name}, which the manifest declares no bundle "
                    f"for",
                    (
                        f"{count(len(one.data), 'byte')} written, "
                        f"beginning {render(one.data[:WINDOW])}",
                    ),
                )
            )
        produced[one.name] = one.data
    for name, data in expected.items():
        if name in produced:
            differences.extend(compare_bundle(name, data, produced[name]))
        else:
            differences.append(Difference(BUNDLES, f"the run wrote no {name}"))
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


def compare_message(
    index: int, declared: Sequence[str], produced: dict[str, Any]
) -> list[Difference]:
    """One diagnostic's message against the text the manifest declares it carries."""
    if MESSAGE not in produced:
        return [
            Difference(
                DIAGNOSTICS,
                f"diagnostic {index} carries no message",
                tuple(f"expected text {entry!r}" for entry in declared),
            )
        ]
    message = str(produced[MESSAGE])
    missing = absent_text(message, declared)
    if not missing:
        return []
    detail = [f"{entry!r} is absent" for entry in missing]
    detail.append(f"produced {message!r}")
    summary = (
        f"diagnostic {index}'s message does not carry "
        f"{count(len(missing), 'declared text')}"
    )
    return [Difference(DIAGNOSTICS, summary, tuple(detail))]


def compare_fields(
    index: int, expected: dict[str, Any], produced: dict[str, Any]
) -> list[Difference]:
    """One diagnostic's further fields, on the fields the manifest declares."""
    differences = []
    declared_text = expected.get(MESSAGE_TEXT)
    if declared_text:
        differences.extend(compare_message(index, declared_text, produced))
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


@contextmanager
def worked(fixture: Path, fault: str | None) -> Iterator[Path]:
    """The directory the run happens in, which a fault makes a copy.

    A fault writes to the tree it runs over, so a fixture declaring one
    is copied and the copy is what the build is pointed at. The fixture
    itself is read and left as it was, and the copy goes with the run.
    """
    if fault is None:
        yield fixture
        return
    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / fixture.name
        shutil.copytree(fixture, copy, symlinks=True)
        yield copy


def run_fixture(fixture: Path) -> Result:
    """One fixture run against the configured build and compared with its manifest."""
    name = identity(fixture)
    manifest = read(fixture / MANIFEST_NAME)
    malformed = errors(manifest) + missing_files(fixture, manifest)
    if malformed:
        difference = Difference(
            MANIFEST,
            "the fixture is not one the schema describes",
            tuple(malformed),
        )
        return Result(name, (difference,), None, b"", b"")

    invocation = manifest["invocation"]
    expected = manifest["expected"]
    declared = manifest.get(FAULT)
    requested = ["-x", declared] if declared is not None else []
    allowed = build_timeout()
    with worked(fixture, declared) as working:
        named = invocation.get("cwd")
        invoked_from = working if named is None else (working / named).resolve()
        bare = not invocation["arguments"] and declared is None
        argv = [
            *build_under_test(),
            *([] if bare else ["-d", "json", *requested]),
            *invocation["arguments"],
        ]
        held = (working, invoked_from) if invoked_from.is_dir() else (working,)
        before = entries(*held)
        try:
            completed = subprocess.run(
                argv,
                cwd=invoked_from,
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
        finally:
            written = collected(entries(*held) - before)

        differences = [
            *compare_exit_status(expected["exit_status"], completed.returncode),
            *compare_bundles(fixture, expected.get("bundles", []), written),
            *compare_stdout(expected.get("stdout_contains", []), completed.stdout),
            *compare_diagnostics(expected["diagnostics"], completed.stderr),
        ]
    return Result(
        name,
        tuple(differences),
        completed.returncode,
        completed.stdout,
        completed.stderr,
    )
