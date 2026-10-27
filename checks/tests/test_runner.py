"""Assert the runner decides a fixture from its manifest and locates a difference.

Each fixture here is written for the run that reads it and validated
against the corpus schema first, so the runner is exercised on real
manifests without any corpus fixture's expected bytes standing in as a
result it was never compared against.

The build under test is a canned program the test configures: it replays
bytes on standard output, bytes on standard error and an exit status, and
knows nothing of the contract. That is the point. The runner invokes
whatever configuration names, so the comparison is the whole of what these
tests exercise, and a fixture's verdict against a real build is a thing
only a real build can produce.
"""

import json
import shlex
import shutil
from pathlib import Path
from typing import Any

import pytest
from manifests import (
    CORPUS,
    MANIFEST_NAME,
    errors,
    identity,
    missing_files,
    present_files,
    read,
)
from runner import (
    ABSENT,
    BUILD,
    BUILD_TIMEOUT,
    DIAGNOSTICS,
    EXIT_STATUS,
    INVOCATION,
    MANIFEST,
    STDOUT,
    STDOUT_TEXT,
    BuildNotConfigured,
    Result,
    run_fixture,
)

RUNNER = Path(__file__).resolve().parent.parent / "runner.py"

IMPLEMENTATION_NAMES = (
    "python",
    "pytest",
    "pyproject",
    "cargo",
    "rust",
    "node",
    "npm",
    "src/prosiform",
    "import prosiform",
)

OUTSIDE_ROOT = {
    "severity": "error",
    "code": "E_SOURCE_OUTSIDE_ROOT",
    "reference": "../outside.md",
    "source": "guide.md:3",
}
NESTED_TARGET = {
    "severity": "error",
    "code": "E_NESTED_SECTION_TARGET",
    "reference": "guide.md#nested",
}
INVALID_USAGE = {
    "severity": "error",
    "code": "E_INVALID_USAGE",
}
TARGET_NOT_FOUND = {
    "severity": "error",
    "code": "E_TARGET_NOT_FOUND",
    "reference": "procedure.md#review",
    "resolved": "procedure.md",
}
ROOT_NOT_FOUND = {
    "severity": "error",
    "code": "E_ROOT_NOT_FOUND",
}


def write_fixture(
    directory: Path,
    *,
    arguments: tuple[str, ...] = ("guide.md",),
    exit_status: int = 0,
    stdout: bytes = b"",
    stdout_contains: tuple[str, ...] = (),
    diagnostics: tuple[dict[str, Any], ...] = (),
    absent: tuple[str, ...] = (),
    complete: bool = True,
    source: bool = True,
    root: str | None = "source",
    fault: str | None = None,
) -> Path:
    """A fixture directory declaring the result its run must produce.

    A fixture declaring that the run cannot find its allowed source root
    carries no source tree, which is what `source` leaves out. A fixture
    declaring a run supplied no allowed source root names none, which is
    what `root` leaves out.
    """
    if source:
        (directory / "source").mkdir(parents=True, exist_ok=True)
        (directory / "source" / "guide.md").write_bytes(b"# Guide\n")
    (directory / "expected").mkdir(parents=True, exist_ok=True)
    (directory / "expected" / "stdout.md").write_bytes(stdout)

    declared = ", ".join(json.dumps(argument) for argument in arguments)
    lines = [
        'description = "A fixture written for one run of the runner."',
        "",
        "clauses = [",
        '  "Validation and failure contract",',
        "]",
        "",
    ]
    if fault is not None:
        lines.extend([f"fault = {json.dumps(fault)}", ""])
    lines.append("[invocation]")
    if root is not None:
        lines.append(f"cwd = {json.dumps(root)}")
    lines.extend(
        [
            f"arguments = [{declared}]",
            "",
            "[expected]",
        ]
    )
    if stdout_contains:
        declared_text = ", ".join(json.dumps(entry) for entry in stdout_contains)
        lines.append(f"stdout_contains = [{declared_text}]")
    else:
        lines.append('stdout = "expected/stdout.md"')
    if complete:
        lines.append(f"exit_status = {exit_status}")
    if absent:
        declared_absent = ", ".join(json.dumps(name) for name in absent)
        lines.append(f"absent = [{declared_absent}]")
    if diagnostics:
        for diagnostic in diagnostics:
            lines.append("")
            lines.append("[[expected.diagnostics]]")
            lines.extend(
                f"{name} = {json.dumps(value)}" for name, value in diagnostic.items()
            )
    else:
        lines.append("diagnostics = []")
    (directory / MANIFEST_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = read(directory / MANIFEST_NAME)
    if complete:
        assert errors(manifest) == []
        assert missing_files(directory, manifest) == []
        assert present_files(directory, manifest) == []
    return directory


def replaying(directory: Path, stdout: bytes, stderr: bytes, status: int) -> str:
    """A configured build that replays one canned result and nothing else."""
    canned = directory / "canned"
    canned.mkdir(parents=True, exist_ok=True)
    out = canned / "stdout"
    err = canned / "stderr"
    out.write_bytes(stdout)
    err.write_bytes(stderr)
    script = (
        f"cat {shlex.quote(str(out))}; cat {shlex.quote(str(err))} >&2; exit {status}"
    )
    return shlex.join(["/bin/sh", "-c", script])


def publishing(name: str, text: str) -> str:
    """A configured build that writes one file into the directory it runs in."""
    script = f"printf %s {shlex.quote(text)} > {shlex.quote(name)}"
    return shlex.join(["/bin/sh", "-c", script])


def recording(record: Path) -> str:
    """A configured build that writes the arguments it was given, one per line."""
    script = (
        'for argument in "$0" "$@"; do printf "%s\\n" "$argument"; done '
        f"> {shlex.quote(str(record))}"
    )
    return shlex.join(["/bin/sh", "-c", script])


def diagnostic_lines(*diagnostics: dict[str, Any]) -> bytes:
    """A diagnostic stream: one JSON object per line."""
    return b"".join(
        json.dumps(diagnostic).encode("utf-8") + b"\n" for diagnostic in diagnostics
    )


def configure(monkeypatch: pytest.MonkeyPatch, command: str) -> None:
    monkeypatch.setenv(BUILD, command)


def detail_of(result: Result, expectation: str) -> str:
    """Everything the report says about one expectation."""
    differences = [
        difference
        for difference in result.differences
        if difference.expectation == expectation
    ]
    assert differences, f"no difference named {expectation}: {result.report()}"
    return "\n".join(
        difference.summary + "\n" + "\n".join(difference.detail)
        for difference in differences
    )


def test_a_passing_fixture_is_decided_from_its_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture", exit_status=0, stdout=b"# Guide\n")
    configure(monkeypatch, replaying(tmp_path, b"# Guide\n", b"", 0))
    result = run_fixture(fixture)
    assert result.passed, result.report()
    assert result.report().endswith(": pass")


def test_a_failure_fixture_is_decided_from_its_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=1,
        stdout=b"",
        diagnostics=(OUTSIDE_ROOT,),
    )
    configure(
        monkeypatch,
        replaying(tmp_path, b"", diagnostic_lines(dict(OUTSIDE_ROOT)), 1),
    )
    result = run_fixture(fixture)
    assert result.passed, result.report()


def test_a_diagnostic_carrying_more_than_the_manifest_declares_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A manifest binds the fields it declares, so a fuller diagnostic still holds."""
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=1,
        diagnostics=(NESTED_TARGET,),
    )
    emitted = dict(NESTED_TARGET)
    emitted["message"] = "a fragment naming a container-nested heading"
    emitted["remedy"] = "name a document-level heading"
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 1))
    result = run_fixture(fixture)
    assert result.passed, result.report()


def test_the_run_receives_the_allowed_root_and_the_diagnostic_format(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture", arguments=("guide.md#alpha", "other.md")
    )
    record = tmp_path / "argv"
    configure(monkeypatch, recording(record))
    run_fixture(fixture)
    assert record.read_text(encoding="utf-8").splitlines() == [
        "-o",
        "-",
        "-d",
        "json",
        "guide.md#alpha",
        "other.md",
    ]


def test_the_verdict_follows_the_configured_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Configuration alone decides what runs, and the program need not be the tool."""
    fixture = write_fixture(tmp_path / "fixture", exit_status=0)
    configure(monkeypatch, "/bin/true")
    assert run_fixture(fixture).passed
    configure(monkeypatch, "/bin/false")
    assert not run_fixture(fixture).passed


def test_an_unconfigured_build_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """No build, no verdict: an absent configuration is never a passing fixture."""
    fixture = write_fixture(tmp_path / "fixture")
    monkeypatch.delenv(BUILD, raising=False)
    with pytest.raises(BuildNotConfigured):
        run_fixture(fixture)
    monkeypatch.setenv(BUILD, "   ")
    with pytest.raises(BuildNotConfigured):
        run_fixture(fixture)


def test_a_malformed_fixture_is_refused_without_invoking_the_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture", complete=False)
    record = tmp_path / "argv"
    configure(monkeypatch, recording(record))
    result = run_fixture(fixture)
    assert not result.passed
    assert "exit_status" in detail_of(result, MANIFEST)
    assert not record.exists()


def test_a_path_the_run_leaves_absent_holds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A declared path the run never creates is the expectation being met."""
    fixture = write_fixture(
        tmp_path / "fixture",
        arguments=("-c", "-o", "bundle.md", "guide.md"),
        absent=("bundle.md",),
    )
    configure(monkeypatch, "/bin/true")
    result = run_fixture(fixture)
    assert result.passed, result.report()
    assert not (fixture / "bundle.md").exists()


def test_a_path_the_run_creates_names_the_expectation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A run that writes the file it was told to validate without writing fails."""
    fixture = write_fixture(
        tmp_path / "fixture",
        arguments=("-c", "-o", "bundle.md", "guide.md"),
        absent=("bundle.md",),
    )
    configure(monkeypatch, publishing("../bundle.md", "# Guide\n"))
    result = run_fixture(fixture)
    assert not result.passed
    detail = detail_of(result, ABSENT)
    assert "the run created bundle.md" in detail
    assert "8 bytes written" in detail


def test_a_path_the_run_creates_is_removed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A corpus run leaves the fixture directory the manifest declares."""
    fixture = write_fixture(
        tmp_path / "fixture",
        arguments=("-c", "-o", "bundle.md", "guide.md"),
        absent=("bundle.md",),
    )
    configure(monkeypatch, publishing("../bundle.md", "# Guide\n"))
    assert not run_fixture(fixture).passed
    assert not (fixture / "bundle.md").exists()


def test_a_fixture_already_holding_a_declared_absent_path_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A declaration the directory contradicts says nothing about the run."""
    fixture = write_fixture(
        tmp_path / "fixture",
        arguments=("-c", "-o", "bundle.md", "guide.md"),
        absent=("bundle.md",),
    )
    (fixture / "bundle.md").write_bytes(b"# Guide\n")
    record = tmp_path / "argv"
    configure(monkeypatch, recording(record))
    result = run_fixture(fixture)
    assert not result.passed
    assert "bundle.md is a path the fixture holds" in detail_of(result, MANIFEST)
    assert not record.exists()
    assert (fixture / "bundle.md").exists()


def test_a_fixture_declaring_an_absent_root_is_decided_from_its_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The one fixture whose allowed source root is a path it does not hold."""
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=1,
        diagnostics=(ROOT_NOT_FOUND,),
        source=False,
        root=None,
    )
    configure(
        monkeypatch, replaying(tmp_path, b"", diagnostic_lines(ROOT_NOT_FOUND), 1)
    )
    result = run_fixture(fixture)
    assert result.passed, result.report()
    assert not (fixture / "source").exists()


def test_a_fixture_naming_a_root_it_does_not_hold_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every other fixture names a root that is a directory it carries."""
    fixture = write_fixture(tmp_path / "fixture")
    shutil.rmtree(fixture / "source")
    record = tmp_path / "argv"
    configure(monkeypatch, recording(record))
    result = run_fixture(fixture)
    assert not result.passed
    assert "source is not a directory" in detail_of(result, MANIFEST)
    assert not record.exists()


def test_a_fixture_naming_no_root_is_run_with_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A manifest naming no root declares a run supplied no allowed source root."""
    fixture = write_fixture(
        tmp_path / "fixture",
        root=None,
        source=False,
        exit_status=2,
        diagnostics=(INVALID_USAGE,),
    )
    record = tmp_path / "argv"
    configure(monkeypatch, recording(record))
    run_fixture(fixture)
    assert record.read_text(encoding="utf-8").splitlines() == [
        "-o",
        "-",
        "-d",
        "json",
        "guide.md",
    ]


def test_the_runner_names_no_implementation_or_language() -> None:
    """A mechanical guard on AC2: the runner carries no build's name.

    It catches the obvious regression. The whole of the criterion is the
    read of the runner recorded with this task.
    """
    source = RUNNER.read_text(encoding="utf-8").lower()
    assert [name for name in IMPLEMENTATION_NAMES if name in source] == []


def test_a_fixture_is_identified_by_its_path_under_the_corpus() -> None:
    assert identity(CORPUS / "identity" / "whole-document") == "identity/whole-document"


def test_a_differing_exit_status_names_the_expectation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture", exit_status=0)
    configure(monkeypatch, replaying(tmp_path, b"", b"", 1))
    result = run_fixture(fixture)
    assert not result.passed
    assert "expected 0, the run exited 1" in detail_of(result, EXIT_STATUS)


def test_differing_stdout_bytes_are_located(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture", stdout=b"# Guide\n\nAlpha\n")
    configure(monkeypatch, replaying(tmp_path, b"# Guide\n\nBeta\n", b"", 0))
    detail = detail_of(run_fixture(fixture), STDOUT)
    assert "15 bytes expected, 14 produced" in detail
    assert "first difference at byte 9, expected line 3 column 1" in detail
    assert "Alpha" in detail
    assert "Beta" in detail


def test_stdout_differing_only_in_newline_spelling_is_located(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The preservation invariant turns on newline spelling, so a report shows it."""
    fixture = write_fixture(tmp_path / "fixture", stdout=b"# Guide\r\n")
    configure(monkeypatch, replaying(tmp_path, b"# Guide\n", b"", 0))
    detail = detail_of(run_fixture(fixture), STDOUT)
    assert "first difference at byte 7, expected line 1 column 8" in detail
    assert "expected b'# Guide\\r\\n'" in detail
    assert "produced b'# Guide\\n'" in detail


def test_stdout_missing_its_trailing_newline_is_located(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture", stdout=b"# Guide\n")
    configure(monkeypatch, replaying(tmp_path, b"# Guide", b"", 0))
    detail = detail_of(run_fixture(fixture), STDOUT)
    assert "first difference at byte 7" in detail
    assert "the run's output ends 1 byte early" in detail
    assert "expected b'# Guide\\n'" in detail


def test_stdout_carrying_more_than_expected_is_located(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture", stdout=b"# Guide\n")
    configure(monkeypatch, replaying(tmp_path, b"# Guide\ntrailing\n", b"", 0))
    detail = detail_of(run_fixture(fixture), STDOUT)
    assert "the run's output carries 9 bytes beyond the end" in detail


def test_an_output_carrying_the_declared_text_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A response whose whole is the build's own is stated by what it carries."""
    fixture = write_fixture(
        tmp_path / "fixture",
        arguments=("-v",),
        stdout_contains=("prosiform ", "(skill-markdown-v3)"),
    )
    configure(
        monkeypatch,
        replaying(tmp_path, b"prosiform 9.4.1 (skill-markdown-v3)\n", b"", 0),
    )
    result = run_fixture(fixture)
    assert result.passed, result.report()


def test_an_output_missing_the_declared_text_names_what_is_absent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The same declaration refuses a response that states another profile."""
    fixture = write_fixture(
        tmp_path / "fixture",
        arguments=("-v",),
        stdout_contains=("prosiform ", "(skill-markdown-v3)"),
    )
    configure(
        monkeypatch,
        replaying(tmp_path, b"prosiform 9.4.1 (skill-markdown-v2)\n", b"", 0),
    )
    detail = detail_of(run_fixture(fixture), STDOUT_TEXT)
    assert "the output does not carry 1 declared text" in detail
    assert "'(skill-markdown-v3)' is absent" in detail
    assert "skill-markdown-v2" in detail


def test_an_output_declared_as_text_is_not_held_to_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Two builds whose responses differ in every other byte both hold."""
    fixture = write_fixture(
        tmp_path / "fixture",
        arguments=("-v",),
        stdout_contains=("prosiform ",),
    )
    configure(monkeypatch, replaying(tmp_path, b"prosiform 0.1.0\n", b"", 0))
    assert run_fixture(fixture).passed
    configure(
        monkeypatch, replaying(tmp_path, b"prosiform 17.0.3-rc4 (a build)\n", b"", 0)
    )
    assert run_fixture(fixture).passed


def test_a_message_carrying_the_declared_text_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=2,
        diagnostics=({**INVALID_USAGE, "message_contains": ["#a-section", "-f"]},),
    )
    emitted = dict(INVALID_USAGE)
    emitted["message"] = (
        "the fragment-only reference '#a-section' needs -f "
        "to name the document it resolves against"
    )
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 2))
    result = run_fixture(fixture)
    assert result.passed, result.report()


def test_a_message_declaration_tells_two_faults_under_one_code_apart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One code names several faults, so the fixture states which one it is."""
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=2,
        diagnostics=({**INVALID_USAGE, "message_contains": ["#a-section", "-f"]},),
    )
    emitted = dict(INVALID_USAGE)
    emitted["message"] = "the command line names no entry reference"
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 2))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "diagnostic 1's message does not carry 2 declared texts" in detail
    assert "'#a-section' is absent" in detail
    assert "'-f' is absent" in detail
    assert "names no entry reference" in detail


def test_a_diagnostic_carrying_no_message_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=2,
        diagnostics=({**INVALID_USAGE, "message_contains": ["-f"]},),
    )
    configure(
        monkeypatch, replaying(tmp_path, b"", diagnostic_lines(dict(INVALID_USAGE)), 2)
    )
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "diagnostic 1 carries no message" in detail
    assert "expected text '-f'" in detail


def test_a_diagnostic_declaring_no_message_text_reads_no_message(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Absence compares nothing, so a fixture stating only a code still holds."""
    fixture = write_fixture(
        tmp_path / "fixture", exit_status=2, diagnostics=(INVALID_USAGE,)
    )
    emitted = dict(INVALID_USAGE)
    emitted["message"] = "any wording this build chooses"
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 2))
    assert run_fixture(fixture).passed


def test_a_missing_diagnostic_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=1,
        diagnostics=(OUTSIDE_ROOT, NESTED_TARGET),
    )
    configure(
        monkeypatch,
        replaying(tmp_path, b"", diagnostic_lines(dict(OUTSIDE_ROOT)), 1),
    )
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "the run emits 1 diagnostic where 2 diagnostics are expected" in detail
    assert (
        "position 2: error E_NESTED_SECTION_TARGET expected, the run emits none"
        in detail
    )


def test_an_extra_diagnostic_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture", exit_status=1, diagnostics=(OUTSIDE_ROOT,)
    )
    stream = diagnostic_lines(dict(OUTSIDE_ROOT), dict(NESTED_TARGET))
    configure(monkeypatch, replaying(tmp_path, b"", stream, 1))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "the run emits 2 diagnostics where 1 diagnostic is expected" in detail
    assert (
        "position 2: error E_NESTED_SECTION_TARGET produced, "
        "which no expectation declares" in detail
    )


def test_diagnostics_out_of_order_are_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=1,
        diagnostics=(OUTSIDE_ROOT, NESTED_TARGET),
    )
    stream = diagnostic_lines(dict(NESTED_TARGET), dict(OUTSIDE_ROOT))
    configure(monkeypatch, replaying(tmp_path, b"", stream, 1))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "the expected diagnostics are emitted in another order" in detail
    assert (
        "expected 1 error E_SOURCE_OUTSIDE_ROOT, 2 error E_NESTED_SECTION_TARGET"
        in detail
    )
    assert (
        "produced 1 error E_NESTED_SECTION_TARGET, 2 error E_SOURCE_OUTSIDE_ROOT"
        in detail
    )


def test_a_diagnostic_carrying_another_code_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture", exit_status=1, diagnostics=(OUTSIDE_ROOT,)
    )
    stream = diagnostic_lines(dict(NESTED_TARGET))
    configure(monkeypatch, replaying(tmp_path, b"", stream, 1))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert (
        "position 1: error E_SOURCE_OUTSIDE_ROOT expected, "
        "error E_NESTED_SECTION_TARGET produced" in detail
    )


def test_a_declared_diagnostic_field_that_differs_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture", exit_status=1, diagnostics=(OUTSIDE_ROOT,)
    )
    emitted = dict(OUTSIDE_ROOT)
    emitted["reference"] = "outside.md"
    del emitted["source"]
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 1))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "diagnostic 1 carries another reference" in detail
    assert "expected '../outside.md'" in detail
    assert "produced 'outside.md'" in detail
    assert "diagnostic 1 carries no source" in detail


def test_a_declared_resolved_identity_that_differs_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture", exit_status=1, diagnostics=(TARGET_NOT_FOUND,)
    )
    emitted = dict(TARGET_NOT_FOUND)
    emitted["resolved"] = "docs/procedure.md"
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 1))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "diagnostic 1 carries another resolved" in detail
    assert "expected 'procedure.md'" in detail
    assert "produced 'docs/procedure.md'" in detail


def test_a_declared_inclusion_chain_that_differs_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    declared = {**OUTSIDE_ROOT, "chain": ["guide.md", "../outside.md"]}
    fixture = write_fixture(
        tmp_path / "fixture", exit_status=1, diagnostics=(declared,)
    )
    emitted = dict(declared)
    emitted["chain"] = ["guide.md"]
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 1))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "diagnostic 1 carries another chain" in detail


def test_a_declared_inclusion_chain_the_run_omits_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    declared = {**OUTSIDE_ROOT, "chain": ["guide.md", "../outside.md"]}
    fixture = write_fixture(
        tmp_path / "fixture", exit_status=1, diagnostics=(declared,)
    )
    emitted = dict(OUTSIDE_ROOT)
    configure(monkeypatch, replaying(tmp_path, b"", diagnostic_lines(emitted), 1))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "diagnostic 1 carries no chain" in detail


def test_a_standard_error_line_that_is_not_a_diagnostic_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture", exit_status=0)
    configure(monkeypatch, replaying(tmp_path, b"", b"resolving guide.md\n", 0))
    detail = detail_of(run_fixture(fixture), DIAGNOSTICS)
    assert "standard error carries a line that is not a JSON diagnostic" in detail
    assert "line 1: b'resolving guide.md'" in detail


def test_every_expectation_that_differed_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(
        tmp_path / "fixture",
        exit_status=0,
        stdout=b"# Guide\n",
        diagnostics=(OUTSIDE_ROOT,),
    )
    configure(monkeypatch, replaying(tmp_path, b"# Other\n", b"", 1))
    result = run_fixture(fixture)
    named = {difference.expectation for difference in result.differences}
    assert named == {EXIT_STATUS, STDOUT, DIAGNOSTICS}
    report = result.report()
    assert report.startswith(f"{identity(fixture)}: fail")
    for expectation in named:
        assert f"  {expectation}: " in report


def test_a_run_that_does_not_complete_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture")
    monkeypatch.setenv(BUILD_TIMEOUT, "0.2")
    configure(monkeypatch, shlex.join(["/bin/sh", "-c", "sleep 5"]))
    result = run_fixture(fixture)
    assert not result.passed
    assert "the run did not complete within 0.2 seconds" in detail_of(
        result, INVOCATION
    )


def test_the_run_receives_the_fault_the_manifest_names(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A declared fault reaches the run beside the root and the diagnostic format."""
    fixture = write_fixture(tmp_path / "fixture", fault="source-changed")
    record = tmp_path / "argv"
    configure(monkeypatch, recording(record))
    run_fixture(fixture)
    written = record.read_text(encoding="utf-8").splitlines()
    assert written[-5:] == [
        "-d",
        "json",
        "-x",
        "source-changed",
        "guide.md",
    ]
    assert written[:2] == ["-o", "-"]


def test_a_run_meeting_no_fault_asks_for_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture")
    record = tmp_path / "argv"
    configure(monkeypatch, recording(record))
    run_fixture(fixture)
    assert "-x" not in record.read_text(encoding="utf-8").splitlines()


def test_a_fixture_declaring_a_fault_runs_in_a_copy_of_itself(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A fault writes to the tree it runs over, and the fixture is left as it was."""
    fixture = write_fixture(tmp_path / "fixture", fault="source-changed")
    configure(monkeypatch, publishing("guide.md", "other bytes"))
    result = run_fixture(fixture)
    assert result.passed, result.report()
    assert (fixture / "source" / "guide.md").read_bytes() == b"# Guide\n"


def test_a_fault_points_the_run_at_the_copy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The allowed source root the run is given is the copy's, not the fixture's."""
    fixture = write_fixture(tmp_path / "fixture", fault="internal")
    record = tmp_path / "argv"
    configure(
        monkeypatch, shlex.join(["/bin/sh", "-c", f"pwd > {shlex.quote(str(record))}"])
    )
    run_fixture(fixture)
    written = record.read_text(encoding="utf-8").splitlines()
    given = Path(written[0])
    assert given.name == "source"
    assert given != (fixture / "source").resolve()
