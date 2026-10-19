"""Assert discovery finds every document the repository owns and no fixture.

A document counts when git tracks it, and the fixture corpus is excepted.
A fixture's source carries references a run is meant to refuse and its
expected bundle is output rather than a document a reader follows, so a
check that resolved either would fail by design. The exception is the
corpus itself rather than a list of names: a fixture is a directory
holding a manifest, so one added anywhere is excepted and a document
added anywhere else is read.
"""

from pathlib import Path

from documents import MARKDOWN, ROOT, corpus, documents, readmes, tracked

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


def test_every_tracked_document_outside_a_fixture_is_found() -> None:
    outside = {
        path
        for path in TRACKED
        if Path(path).suffix in MARKDOWN
        and not any(path.startswith(f"{fixture}/") for fixture in FIXTURES)
    }
    assert relative(FOUND) == outside


def test_a_document_that_is_not_a_readme_is_found() -> None:
    assert relative(FOUND) - relative(readmes()), (
        "discovery found the READMEs alone, so the check reads no other document"
    )


def test_the_readmes_are_the_documents_named_readme() -> None:
    assert relative(readmes()) == {
        name for name in relative(FOUND) if Path(name).name == "README.md"
    }
