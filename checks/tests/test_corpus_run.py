"""Assert the corpus run decides the whole corpus and retires its own markers.

The corpus states the contract and the contract is delivered epic by
epic, so a fixture may declare behaviour the build has yet to produce.
Such a fixture names the work that delivers it, and the run reads that
name: its failure is reported as awaited and leaves the verdict green,
while a run in which it meets its manifest fails, so the marker cannot
outlive the work it waits on.

The same markers answer a request: asked which fixtures await one named
piece of work, the corpus reports them from the manifests alone, so a
session starting that work reads what it unblocks before it changes
anything.

The build under test is a canned program each case configures, as in the
runner's own tests: the comparison belongs to the runner and what these
cases exercise is the verdict drawn from it. A corpus with no build
configured fails rather than passing over its fixtures, which is the one
outcome a green suite must never be able to carry.
"""

import json
import shlex
from pathlib import Path

import pytest
from corpus import (
    Outcome,
    Verdict,
    awaiting,
    main,
    outcome,
    report,
    requested,
    summary,
    unblocked,
    unblocked_report,
)
from manifests import MANIFEST_NAME, errors, missing_files, read
from runner import BUILD, Difference, Result

BODY = b"# Guide\n"


def write_fixture(
    directory: Path,
    *,
    bundle: bytes = BODY,
    awaits: str | None = None,
) -> Path:
    """A fixture directory declaring a successful run, optionally awaiting work."""
    (directory / "source").mkdir(parents=True, exist_ok=True)
    (directory / "source" / "guide.md").write_bytes(BODY)
    (directory / "expected").mkdir(parents=True, exist_ok=True)
    (directory / "expected" / "guide.bundle.md").write_bytes(bundle)

    lines = ['description = "A fixture written for one run of the corpus."', ""]
    if awaits is not None:
        lines.extend([f"awaiting = {json.dumps(awaits)}", ""])
    lines.extend(
        [
            "clauses = [",
            '  "Validation and failure contract",',
            "]",
            "",
            "[invocation]",
            'cwd = "source"',
            'arguments = ["guide.md"]',
            "",
            "[expected]",
            "exit_status = 0",
            'bundles = ["expected/guide.bundle.md"]',
            "diagnostics = []",
        ]
    )
    (directory / MANIFEST_NAME).write_text("\n".join(lines) + "\n", encoding="utf-8")

    manifest = read(directory / MANIFEST_NAME)
    assert errors(manifest) == []
    assert missing_files(directory, manifest) == []
    return directory


def replaying(directory: Path, bundle: bytes) -> str:
    """A configured build that writes one canned bundle and succeeds."""
    canned = directory / "canned"
    canned.mkdir(parents=True, exist_ok=True)
    written = canned / "bundle"
    written.write_bytes(bundle)
    script = f"cat {shlex.quote(str(written))} > guide.bundle.md"
    return shlex.join(["/bin/sh", "-c", script])


def verdict_of(
    directory: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    produced: bytes,
    awaits: str | None,
) -> Verdict:
    """One fixture's verdict, against a build replaying the bytes named."""
    fixture = write_fixture(directory / "fixture", awaits=awaits)
    monkeypatch.setenv(BUILD, replaying(directory, produced))
    return outcome(fixture).verdict


def stand_in(name: str, *, passed: bool, awaits: str | None) -> Outcome:
    """One outcome, written directly rather than drawn from a run."""
    differences = (
        () if passed else (Difference("expected.bundles", "the bytes differ"),)
    )
    return Outcome(Result(name, differences, 0, b"", b""), awaits)


def test_a_manifest_names_the_work_it_awaits(tmp_path: Path) -> None:
    fixture = write_fixture(tmp_path / "fixture", awaits="I00:E03")
    assert awaiting(read(fixture / MANIFEST_NAME)) == "I00:E03"


def test_a_manifest_awaiting_nothing_names_nothing(tmp_path: Path) -> None:
    fixture = write_fixture(tmp_path / "fixture")
    assert awaiting(read(fixture / MANIFEST_NAME)) is None


def test_a_fixture_meeting_its_manifest_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    verdict = verdict_of(tmp_path, monkeypatch, produced=BODY, awaits=None)
    assert verdict is Verdict.PASSED


def test_a_fixture_differing_from_its_manifest_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    verdict = verdict_of(tmp_path, monkeypatch, produced=b"# Other\n", awaits=None)
    assert verdict is Verdict.FAILED


def test_a_fixture_awaiting_work_and_differing_is_awaited(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    verdict = verdict_of(tmp_path, monkeypatch, produced=b"# Other\n", awaits="I00:E03")
    assert verdict is Verdict.AWAITED


def test_a_fixture_awaiting_work_it_already_meets_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    verdict = verdict_of(tmp_path, monkeypatch, produced=BODY, awaits="I00:E03")
    assert verdict is Verdict.UNEXPECTED_PASS


@pytest.mark.parametrize(
    ("verdict", "fails"),
    [
        (Verdict.PASSED, False),
        (Verdict.AWAITED, False),
        (Verdict.FAILED, True),
        (Verdict.UNEXPECTED_PASS, True),
    ],
)
def test_which_verdicts_fail_the_run(verdict: Verdict, fails: bool) -> None:
    assert verdict.fails_the_run is fails


def test_an_awaited_fixture_names_the_work_on_its_line() -> None:
    line = stand_in("extraction/nested", passed=False, awaits="I00:E03").line()
    assert line == "extraction/nested: awaited, awaiting I00:E03"


def test_a_failing_fixture_is_named_by_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fixture = write_fixture(tmp_path / "fixture")
    monkeypatch.setenv(BUILD, replaying(tmp_path, b"# Other\n"))
    lines = report([outcome(fixture)])
    named = [line for line in lines if line.startswith(str(fixture))]
    assert named, lines
    assert any("the bytes differ" in line for line in lines)


def test_an_unexpected_pass_names_the_marker_to_remove() -> None:
    detail = stand_in("extraction/nested", passed=True, awaits="I00:E03").detail()
    assert "meets its manifest while awaiting I00:E03" in detail[0]
    assert f"extraction/nested/{MANIFEST_NAME}" in detail[1]


def test_a_passing_fixture_carries_no_detail() -> None:
    assert stand_in("identity/whole", passed=True, awaits=None).detail() == []


def test_an_awaited_fixture_carries_no_detail() -> None:
    assert stand_in("extraction/nested", passed=False, awaits="I00:E03").detail() == []


def test_the_summary_counts_every_verdict() -> None:
    outcomes = [
        stand_in("a", passed=True, awaits=None),
        stand_in("b", passed=False, awaits=None),
        stand_in("c", passed=False, awaits="I00:E04"),
        stand_in("d", passed=True, awaits="I00:E03"),
    ]
    assert summary(outcomes) == (
        "corpus check: 4 fixture(s), 1 pass, 1 fail, 1 awaited, 1 unexpected pass"
    )


def test_a_corpus_that_holds_passes_and_awaited_fixtures_succeeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_fixture(tmp_path / "corpus" / "one")
    write_fixture(tmp_path / "corpus" / "two", bundle=b"# Other\n", awaits="I00:E03")
    monkeypatch.setenv(BUILD, replaying(tmp_path, BODY))
    assert main(tmp_path / "corpus") == 0


def test_a_corpus_holding_a_failing_fixture_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_fixture(tmp_path / "corpus" / "one")
    write_fixture(tmp_path / "corpus" / "two", bundle=b"# Other\n")
    monkeypatch.setenv(BUILD, replaying(tmp_path, BODY))
    assert main(tmp_path / "corpus") == 1


def test_a_corpus_holding_an_unexpected_pass_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_fixture(tmp_path / "corpus" / "one", awaits="I00:E03")
    monkeypatch.setenv(BUILD, replaying(tmp_path, BODY))
    assert main(tmp_path / "corpus") == 1


def test_an_unconfigured_build_fails_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    write_fixture(tmp_path / "corpus" / "one")
    monkeypatch.delenv(BUILD, raising=False)
    assert main(tmp_path / "corpus") == 1
    assert BUILD in capsys.readouterr().err


def test_an_unconfigured_build_runs_no_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    fixture = write_fixture(tmp_path / "corpus" / "one")
    monkeypatch.delenv(BUILD, raising=False)
    main(tmp_path / "corpus")
    assert str(fixture) not in capsys.readouterr().out


def test_an_empty_corpus_fails_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "corpus").mkdir()
    monkeypatch.setenv(BUILD, replaying(tmp_path, BODY))
    assert main(tmp_path / "corpus") == 1


def test_the_whole_corpus_runs_against_the_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    for name in ("one", "two", "three"):
        write_fixture(tmp_path / "corpus" / name)
    monkeypatch.setenv(BUILD, replaying(tmp_path, BODY))
    assert main(tmp_path / "corpus") == 0
    printed = capsys.readouterr().out
    assert "3 fixture(s), 3 pass" in printed
    for name in ("one", "two", "three"):
        assert str(tmp_path / "corpus" / name) in printed


def awaiting_corpus(tmp_path: Path) -> Path:
    """A corpus of three fixtures, two of them awaiting different work."""
    corpus = tmp_path / "corpus"
    write_fixture(corpus / "met")
    write_fixture(corpus / "one", bundle=b"# Other\n", awaits="I00:E03")
    write_fixture(corpus / "two", bundle=b"# Other\n", awaits="I00:E04:W02")
    return corpus


def test_the_report_names_what_one_piece_of_work_unblocks(tmp_path: Path) -> None:
    corpus = awaiting_corpus(tmp_path)
    assert unblocked("I00:E03", corpus) == [corpus / "one"]
    assert unblocked("I00:E04:W02", corpus) == [corpus / "two"]


def test_the_report_names_no_fixture_awaiting_other_work(tmp_path: Path) -> None:
    corpus = awaiting_corpus(tmp_path)
    assert unblocked_report("I00:E03", corpus) == [
        "one",
        "awaiting I00:E03: 1 fixture(s)",
    ]


def test_work_no_fixture_awaits_unblocks_nothing(tmp_path: Path) -> None:
    corpus = awaiting_corpus(tmp_path)
    assert unblocked_report("I00:E99", corpus) == ["awaiting I00:E99: 0 fixture(s)"]


def test_a_marker_naming_an_epic_is_not_the_task_within_it(tmp_path: Path) -> None:
    corpus = awaiting_corpus(tmp_path)
    assert unblocked("I00:E04", corpus) == []


def test_the_report_answers_without_a_build(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = awaiting_corpus(tmp_path)
    monkeypatch.delenv(BUILD, raising=False)
    assert main(corpus, awaited="I00:E03") == 0
    printed = capsys.readouterr().out
    assert "one" in printed
    assert "two" not in printed


def test_a_request_names_the_work_it_asks_about() -> None:
    assert requested(["--awaiting", "I00:E03"]) == "I00:E03"


def test_a_run_naming_no_work_runs_the_corpus() -> None:
    assert requested([]) is None
