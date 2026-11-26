"""Assert triage names each stale fixture under the category its run falls in.

A corpus is written for each case with one fixture per behaviour, and the
build under test is a shell script each fixture's source tree carries, so
one configured build gives every fixture the run its case needs. The
verdicts come from the corpus run, so what these cases exercise is the
category drawn from each verdict, the selection of one category, and the
silence of a tree the corpus run passes.
"""

import json
from pathlib import Path

import pytest
from manifests import MANIFEST_NAME, errors, missing_files, read
from runner import BUILD
from triage import Drift, Request, edits, main, requested

BODY = b"# Guide\n"
FOLDER = "guide.bundles"
BUILD_SCRIPT = "/bin/sh build.sh"


def bundle(text: bytes, name: str = "guide.bundle.md", folder: str = FOLDER) -> str:
    """A build step writing `text` as one bundle in the run's folder."""
    return f"mkdir -p {folder}; printf %b {json.dumps(text.decode())} > {folder}/{name}"


def write_fixture(
    directory: Path, script: str, *, expected: bytes = BODY, awaits: str | None = None
) -> Path:
    """A fixture declaring one bundle, its source carrying the build its run takes."""
    (directory / "source").mkdir(parents=True)
    (directory / "source" / "guide.md").write_bytes(BODY)
    (directory / "source" / "build.sh").write_text(script + "\n", encoding="utf-8")
    (directory / "expected").mkdir()
    (directory / "expected" / "guide.bundle.md").write_bytes(expected)
    lines = ['description = "A fixture written for one triage run."', ""]
    if awaits is not None:
        lines.extend([f"awaiting = {json.dumps(awaits)}", ""])
    lines.extend(
        [
            'clauses = ["Validation and failure contract"]',
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


WARNING = '{"severity": "warning", "code": "W_UNUSED_PRESET"}'

ONE_OF_EACH = {
    "a-status": (bundle(BODY) + "; exit 1", BODY),
    "b-streams": (bundle(BODY) + f"; echo '{WARNING}' >&2", BODY),
    "c-layout": (bundle(BODY) + "; " + bundle(BODY, "more.bundle.md"), BODY),
    "d-names": (bundle(BODY, "other.bundle.md"), BODY),
    "e-inserted": (bundle(b"# Guide\nmore\n"), BODY),
    "f-removed": (bundle(BODY), b"# Guide\nmore\n"),
    "g-rewritten": (bundle(b"# Other\n"), BODY),
    "h-both": (bundle(b"# Guide\nnew\nlines\n"), b"# Guide\nold\n"),
    "i-crashed": (bundle(BODY) + "; exit 4", BODY),
    "j-met": (bundle(BODY), BODY),
}


def corpus_of(root: Path, cases: dict[str, tuple[str, bytes]]) -> Path:
    """A corpus holding one fixture per case, named for it."""
    for name, (script, expected) in cases.items():
        write_fixture(root / name, script, expected=expected)
    return root


def tree(root: Path) -> dict[str, bytes]:
    """Every file under `root`, by path, with its bytes."""
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


@pytest.fixture
def configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(BUILD, BUILD_SCRIPT)


@pytest.mark.usefixtures("configured")
def test_each_fixture_is_named_under_its_own_category(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = corpus_of(tmp_path / "corpus", ONE_OF_EACH)
    before = tree(corpus)
    assert main(corpus) == 0
    assert capsys.readouterr().out.splitlines() == [
        "a-status: status",
        "b-streams: streams",
        "c-layout: layout",
        "d-names: names",
        "e-inserted: inserted",
        "f-removed: removed",
        "g-rewritten: rewritten",
        "h-both: both",
        "i-crashed: run failed in itself",
    ]
    assert tree(corpus) == before


@pytest.mark.usefixtures("configured")
def test_only_reports_the_selected_category_alone(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = corpus_of(
        tmp_path / "corpus",
        {
            name: ONE_OF_EACH[name]
            for name in ("e-inserted", "g-rewritten", "i-crashed")
        },
    )
    assert main(corpus, Request(Drift.INSERTED)) == 0
    assert capsys.readouterr().out.splitlines() == ["e-inserted: inserted"]


@pytest.mark.usefixtures("configured")
def test_a_green_corpus_produces_no_report(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = tmp_path / "corpus"
    write_fixture(corpus / "met", bundle(BODY))
    write_fixture(corpus / "awaited", bundle(b"# Other\n"), awaits="I00:E03")
    assert main(corpus) == 0
    assert capsys.readouterr().out == ""


@pytest.mark.usefixtures("configured")
def test_named_fixtures_are_triaged_alone(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = corpus_of(tmp_path / "corpus", ONE_OF_EACH)
    assert main(corpus, Request(names=("g-rewritten",))) == 0
    assert capsys.readouterr().out.splitlines() == ["g-rewritten: rewritten"]


@pytest.mark.usefixtures("configured")
def test_an_identity_no_fixture_carries_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = corpus_of(tmp_path / "corpus", {"j-met": ONE_OF_EACH["j-met"]})
    assert main(corpus, Request(names=("absent",))) == 1
    assert "absent" in capsys.readouterr().err


def test_triage_without_a_build_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(BUILD, raising=False)
    corpus = corpus_of(tmp_path / "corpus", {"j-met": ONE_OF_EACH["j-met"]})
    assert main(corpus) == 1


@pytest.mark.parametrize(
    ("expected", "produced", "found"),
    [
        (b"a\n", b"a\r\n", {Drift.REWRITTEN}),
        (b"a\n", b"a", {Drift.REWRITTEN}),
        (b"a\nb\n", b"a\nx\nb\n", {Drift.INSERTED}),
        (b"a\nb\n", b"b\n", {Drift.REMOVED}),
        (b"a\nb\n", b"x\ny\nz\n", {Drift.BOTH}),
    ],
)
def test_content_edits_are_read_line_by_line(
    expected: bytes, produced: bytes, found: set[Drift]
) -> None:
    assert edits(expected, produced) == found


def test_a_command_line_selects_a_category_and_fixtures() -> None:
    assert requested(["--only", "names", "one/two"]) == Request(
        Drift.NAMES, ("one/two",)
    )
