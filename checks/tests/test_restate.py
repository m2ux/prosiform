"""Assert restatement writes a stale fixture's bundles and refuses the rest.

A corpus is written for each case with one fixture per behaviour, and the
build under test is a shell script each fixture's source tree carries, so
one configured build gives every fixture the run its case needs. What these
cases exercise is what restatement writes, what it leaves byte for byte, and
which fixtures it refuses and names.
"""

import ast
import json
import subprocess
from pathlib import Path

import pytest
from manifests import MANIFEST_NAME, errors, missing_files, read
from restate import Request, main, requested
from runner import BUILD

CHECKS = Path(__file__).resolve().parent.parent
BODY = b"# Guide\n"
HELPER = b"# Helper\n"
FOLDER = "guide.bundles"
BUILD_SCRIPT = "/bin/sh build.sh"
WARNING = '{"severity": "warning", "code": "W_UNUSED_PRESET"}'


def bundle(text: bytes, name: str = "guide.bundle.md") -> str:
    """A build step writing `text` as one bundle in the run's folder."""
    return f"mkdir -p {FOLDER}; printf %b {json.dumps(text.decode())} > {FOLDER}/{name}"


def manifest_text(bundles: list[str]) -> str:
    """A manifest carrying a non-ASCII clause, a second clause and the bundles."""
    listed = "".join(f"  {json.dumps(one)},\n" for one in bundles)
    return (
        'description = "A fixture written for one restatement run."\n'
        "\n"
        "clauses = [\n"
        '  "Validation and failure contract — Exit statuses",\n'
        '  "Headings and anchors — Generated headings",\n'
        "]\n"
        "\n"
        "[invocation]\n"
        'cwd = "source"\n'
        'arguments = ["guide.md"]\n'
        "\n"
        "[expected]\n"
        "exit_status = 0\n"
        f"bundles = [\n{listed}]\n"
        "diagnostics = []\n"
    )


def write_fixture(
    directory: Path, script: str, expected: dict[str, bytes] | None = None
) -> Path:
    """A fixture declaring its bundles, its source carrying the build its run takes."""
    declared = expected or {"guide.bundle.md": BODY}
    (directory / "source").mkdir(parents=True)
    (directory / "source" / "guide.md").write_bytes(BODY)
    (directory / "source" / "build.sh").write_text(script + "\n", encoding="utf-8")
    (directory / "expected").mkdir()
    for name, data in declared.items():
        (directory / "expected" / name).write_bytes(data)
    bundles = [f"expected/{name}" for name in declared]
    (directory / MANIFEST_NAME).write_text(manifest_text(bundles), encoding="utf-8")
    manifest = read(directory / MANIFEST_NAME)
    assert errors(manifest) == []
    assert missing_files(directory, manifest) == []
    return directory


def tree(root: Path) -> dict[str, bytes]:
    """Every file under `root`, by path, with its bytes."""
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and ".git" not in path.relative_to(root).parts
    }


def git(root: Path, *arguments: str) -> str:
    """One git command's output, run in `root`."""
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout


@pytest.fixture
def configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(BUILD, BUILD_SCRIPT)


@pytest.mark.usefixtures("configured")
def test_a_dry_run_names_the_stale_fixture_and_leaves_the_tree_clean(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = tmp_path / "corpus"
    write_fixture(corpus / "met", bundle(BODY))
    write_fixture(corpus / "stale", bundle(b"# Other\n"))
    git(corpus, "init", "--quiet")
    git(corpus, "add", ".")
    git(
        corpus,
        "-c",
        "user.name=corpus",
        "-c",
        "user.email=corpus@example.invalid",
        "commit",
        "--quiet",
        "--message",
        "corpus",
    )
    assert main(corpus) == 0
    assert capsys.readouterr().out.splitlines() == ["would restate stale: rewritten"]
    assert git(corpus, "status", "--porcelain", "--untracked-files=all") == ""


@pytest.mark.usefixtures("configured")
def test_writing_replaces_the_bundles_and_leaves_the_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = tmp_path / "corpus"
    fixture = write_fixture(
        corpus / "stale",
        bundle(b"# Guide\nmore\n")
        + "; "
        + bundle(b"# Helper\nmore\n", "helper.bundle.md"),
        {"guide.bundle.md": BODY, "helper.bundle.md": HELPER},
    )
    before = tree(fixture)
    assert main(corpus, Request(write=True)) == 0
    assert capsys.readouterr().out.splitlines() == ["restated stale: inserted"]
    after = tree(fixture)
    assert after["expected/guide.bundle.md"] == b"# Guide\nmore\n"
    assert after["expected/helper.bundle.md"] == b"# Helper\nmore\n"
    changed = {
        path
        for path in before.keys() | after.keys()
        if before.get(path) != after.get(path)
    }
    assert changed == {"expected/guide.bundle.md", "expected/helper.bundle.md"}
    assert main(corpus) == 0
    assert capsys.readouterr().out == ""


@pytest.mark.usefixtures("configured")
def test_a_renamed_bundle_edits_only_its_name_in_the_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = tmp_path / "corpus"
    fixture = write_fixture(
        corpus / "renamed",
        bundle(BODY) + "; " + bundle(HELPER, "aide.bundle.md"),
        {"guide.bundle.md": BODY, "helper.bundle.md": HELPER},
    )
    manifest = (fixture / MANIFEST_NAME).read_bytes()
    assert main(corpus, Request(write=True)) == 0
    assert capsys.readouterr().out.splitlines() == ["restated renamed: names"]
    assert (fixture / MANIFEST_NAME).read_bytes() == manifest.replace(
        b'"expected/helper.bundle.md"', b'"expected/aide.bundle.md"'
    )
    assert "—".encode() in (fixture / MANIFEST_NAME).read_bytes()
    assert sorted(path.name for path in (fixture / "expected").iterdir()) == [
        "aide.bundle.md",
        "guide.bundle.md",
    ]
    assert (fixture / "expected" / "aide.bundle.md").read_bytes() == HELPER
    assert main(corpus) == 0
    assert capsys.readouterr().out == ""


REFUSED = {
    "failed": (bundle(b"# Other\n") + "; exit 4", "run failed in itself"),
    "status": (bundle(b"# Other\n") + "; exit 1", "status"),
    "streams": (bundle(b"# Other\n") + f"; echo '{WARNING}' >&2", "streams"),
    "layout": (
        bundle(b"# Other\n") + "; " + bundle(BODY, "more.bundle.md"),
        "layout",
    ),
}


@pytest.mark.usefixtures("configured")
@pytest.mark.parametrize("case", sorted(REFUSED))
def test_a_fixture_a_reader_decides_is_refused_and_named(
    case: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    script, reason = REFUSED[case]
    corpus = tmp_path / "corpus"
    write_fixture(corpus / case, script)
    write_fixture(corpus / "stale", bundle(b"# Other\n"))
    before = tree(corpus)
    assert main(corpus, Request(write=True)) == 1
    assert capsys.readouterr().out.splitlines() == [
        "restated stale: rewritten",
        f"refused {case}: {reason}",
    ]
    after = tree(corpus)
    assert {path for path in before if before[path] != after[path]} == {
        "stale/expected/guide.bundle.md"
    }


@pytest.mark.usefixtures("configured")
def test_a_dry_run_refusal_fails_the_run(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = tmp_path / "corpus"
    write_fixture(corpus / "failed", REFUSED["failed"][0])
    assert main(corpus) == 1
    assert capsys.readouterr().out.splitlines() == [
        "refused failed: run failed in itself"
    ]


@pytest.mark.usefixtures("configured")
def test_named_fixtures_are_restated_alone(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = tmp_path / "corpus"
    write_fixture(corpus / "one", bundle(b"# Other\n"))
    write_fixture(corpus / "two", bundle(b"# Other\n"))
    assert main(corpus, Request(write=True, names=("two",))) == 0
    assert capsys.readouterr().out.splitlines() == ["restated two: rewritten"]
    assert (corpus / "one" / "expected" / "guide.bundle.md").read_bytes() == BODY


@pytest.mark.usefixtures("configured")
def test_an_identity_no_fixture_carries_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    corpus = tmp_path / "corpus"
    write_fixture(corpus / "met", bundle(BODY))
    assert main(corpus, Request(names=("absent",))) == 1
    assert "absent" in capsys.readouterr().err


def test_restatement_without_a_build_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(BUILD, raising=False)
    corpus = tmp_path / "corpus"
    write_fixture(corpus / "met", bundle(BODY))
    assert main(corpus) == 1


def test_a_command_line_selects_writing_and_fixtures() -> None:
    assert requested(["--write", "one/two"]) == Request(True, ("one/two",))
    assert requested([]) == Request()


@pytest.mark.parametrize("command", ["triage.py", "restate.py"])
def test_each_command_reads_the_corpus_run_and_its_runner(command: str) -> None:
    imported = {
        node.module
        for node in ast.walk(ast.parse((CHECKS / command).read_text(encoding="utf-8")))
        if isinstance(node, ast.ImportFrom)
    }
    assert {"corpus", "runner", "manifests"} <= imported
