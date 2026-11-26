"""Assert discovery finds every document the repository owns and no fixture.

A document counts when git tracks it, and the fixture corpus is excepted.
A fixture's source carries references a run is meant to refuse and its
expected bundle is output rather than a document a reader follows, so a
check that resolved either would fail by design. The exception is the
corpus itself rather than a list of names: a fixture is a directory
holding a manifest, so one added anywhere is excepted and a document
added anywhere else is read. A tracked bundle outside the corpus is output
on the same ground, and is excepted too.

A document present and untracked is named by each reading check's run as
unread, and fails nothing. Those runs are held over a working tree of their
own, a copy of the checks in a fresh repository carrying an untracked
document, an ignored one and an untracked fixture, since the repository's
own tree carries whatever its contributor happens to have written.

The reading the checks share is held to the input it would read wrongly: a
code span and an indented block holding a link form, an opener that never
closes, and a list's continuation, which is content however far it is
indented.
"""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from documents import (
    BUNDLE,
    MARKDOWN,
    ROOT,
    corpus,
    documents,
    strip_code_spans,
    strip_indented_blocks,
    strip_literal,
    tracked,
)

FOUND = documents()
TRACKED = tracked()
FIXTURES = corpus(TRACKED)


def relative(paths: list[Path]) -> set[str]:
    return {path.relative_to(ROOT).as_posix() for path in paths}


def test_the_repository_owns_a_document() -> None:
    assert FOUND


def test_every_document_found_is_markdown_git_tracks() -> None:
    names = relative(FOUND)
    assert names <= set(TRACKED)
    assert all(Path(name).suffix in MARKDOWN for name in names)


def test_no_document_inside_a_fixture_is_found() -> None:
    assert FIXTURES, "the corpus holds no fixture, so the exception checks nothing"
    inside = {
        name
        for name in relative(FOUND)
        for fixture in FIXTURES
        if name.startswith(f"{fixture}/")
    }
    assert inside == set(), f"a fixture's own files entered the check: {sorted(inside)}"


def test_no_tracked_bundle_is_found() -> None:
    bundles = {path for path in TRACKED if path.endswith(BUNDLE)}
    outside = {
        path
        for path in bundles
        if not any(path.startswith(f"{fixture}/") for fixture in FIXTURES)
    }
    assert outside, (
        "no bundle is tracked outside the corpus, so the exception checks nothing"
    )
    assert relative(FOUND) & bundles == set()


def test_every_tracked_document_outside_a_fixture_is_found() -> None:
    outside = {
        path
        for path in TRACKED
        if Path(path).suffix in MARKDOWN
        and not path.endswith(BUNDLE)
        and not any(path.startswith(f"{fixture}/") for fixture in FIXTURES)
    }
    assert relative(FOUND) == outside


def test_a_document_that_is_not_a_readme_is_found() -> None:
    assert any(path.name != "README.md" for path in FOUND), (
        "discovery found the READMEs alone, so the check reads no other document"
    )


CHECKS = Path(__file__).resolve().parent.parent
READING_CHECKS = ("links.py", "tables.py")


@pytest.fixture
def working_tree(tmp_path: Path) -> Path:
    """A repository whose index holds the checks and one document.

    Its working tree also carries an untracked document holding a reference
    that resolves nowhere, a document git ignores, and an untracked fixture
    holding a document of its own.
    """
    (tmp_path / "checks").mkdir()
    for name in ("documents.py", *READING_CHECKS):
        shutil.copy(CHECKS / name, tmp_path / "checks" / name)
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "pyproject.toml").write_text(
        '[project]\nrequires-python = ">=3.11"\n'
    )
    (tmp_path / "Makefile").write_text("")
    (tmp_path / "README.md").write_text(
        "| Declared | Value |\n| --- | --- |\n| Python | >=3.11 |\n"
    )
    (tmp_path / ".gitignore").write_text("ignored.md\n")
    (tmp_path / "ignored.md").write_text("[gone](missing.md)\n")
    (tmp_path / "draft.md").write_text("[gone](missing.md)\n")
    fixture = tmp_path / "fixtures" / "new"
    fixture.mkdir(parents=True)
    (fixture / "manifest.toml").write_text("")
    (fixture / "source.md").write_text("[gone](missing.md)\n")
    git = ["git", "-C", str(tmp_path)]
    subprocess.run([*git, "init", "-q"], check=True)
    subprocess.run(
        [*git, "add", "checks", "src", "Makefile", "README.md", ".gitignore"],
        check=True,
    )
    return tmp_path


@pytest.mark.parametrize("check", READING_CHECKS)
def test_a_reading_check_names_an_untracked_document_as_unread(
    working_tree: Path, check: str
) -> None:
    run = subprocess.run(
        [sys.executable, str(working_tree / "checks" / check)],
        cwd=working_tree,
        capture_output=True,
        text=True,
        check=False,
    )
    assert run.returncode == 0, run.stderr
    unread = [line for line in run.stdout.splitlines() if line.startswith("unread ")]
    assert unread == ["unread draft.md — present and untracked"]
    assert "1 untracked document(s) unread" in run.stdout


def test_a_code_span_is_blanked_and_its_line_keeps_its_length() -> None:
    line = "Beside `code` text."
    assert strip_code_spans(line) == "Beside        text."


def test_a_code_span_closes_on_a_run_of_its_own_width() -> None:
    assert strip_code_spans("``a ` b`` c") == " " * 10 + "c"


def test_a_backtick_run_that_never_closes_is_the_text_it_is_written_as() -> None:
    assert strip_code_spans("``opened and `closed` after") == (
        "``opened and          after"
    )


def test_a_code_span_spanning_lines_keeps_the_lines_it_covers() -> None:
    assert strip_code_spans("a `one\ntwo` b") == "a" + " " * 5 + "\n" + " " * 5 + "b"


def test_an_indented_block_after_a_blank_line_is_blanked() -> None:
    text = "Prose.\n\n    an example\n    a second line\n\nProse.\n"
    assert strip_indented_blocks(text) == "Prose.\n\n\n\n\nProse."


def test_a_list_continuation_is_content_however_far_it_is_indented() -> None:
    text = "- A bullet.\n\n    - A nested bullet.\n"
    assert strip_indented_blocks(text) == text.rstrip("\n")


def test_an_indented_block_closes_at_the_first_line_indented_less() -> None:
    text = "Prose.\n\n    an example\nProse again.\n"
    assert strip_indented_blocks(text) == "Prose.\n\n\nProse again."


def test_every_literal_form_is_blanked_together() -> None:
    text = "A `span` and:\n\n    an example\n\n```\nfenced\n```\n\nEnd.\n"
    blanked = strip_literal(text)
    assert "span" not in blanked
    assert "an example" not in blanked
    assert "fenced" not in blanked
    assert "End." in blanked
