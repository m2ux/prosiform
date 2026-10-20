"""Assert that a source read descends from the root and follows no link.

The corpus states what a run does about a refused source. These are the
cases the corpus cannot reach: what the walk itself refuses before any
command interprets it, and the entry kinds a fixture directory in git
cannot carry — a hard link, a directory named as a document, and a path
whose segments the normalization would never produce.
"""

import os
from pathlib import Path

import pytest

from prosiform.access import Absent, Outside, Symlinked, read_source

GUIDE = "# Guide\n"
SECRET = "# Secret\n"


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """A source tree, with a document outside it to point a link at."""
    (tmp_path / "outside").mkdir()
    (tmp_path / "outside" / "secret.md").write_text(SECRET)
    inside = tmp_path / "source"
    (inside / "docs").mkdir(parents=True)
    (inside / "docs" / "note.md").write_text(GUIDE)
    (inside / "guide.md").write_text(GUIDE)
    return inside


def test_a_document_the_root_holds_is_read_as_its_bytes(root: Path) -> None:
    assert read_source(root, "guide.md") == GUIDE.encode()
    assert read_source(root, "docs/note.md") == GUIDE.encode()


def test_a_symbolic_link_out_of_the_root_is_refused(root: Path) -> None:
    os.symlink("../outside/secret.md", root / "escaping.md")
    with pytest.raises(Symlinked):
        read_source(root, "escaping.md")


def test_a_symbolic_link_the_root_holds_the_target_of_is_refused(root: Path) -> None:
    os.symlink("guide.md", root / "alias.md")
    with pytest.raises(Symlinked):
        read_source(root, "alias.md")


def test_a_symbolic_directory_link_is_refused_at_that_segment(root: Path) -> None:
    os.symlink("../outside", root / "away")
    with pytest.raises(Symlinked):
        read_source(root, "away/secret.md")


def test_a_root_that_is_itself_a_link_is_the_caller_s_own_spelling(
    root: Path, tmp_path: Path
) -> None:
    os.symlink(root, tmp_path / "aliased-root")
    assert read_source(tmp_path / "aliased-root", "guide.md") == GUIDE.encode()


def test_a_hard_link_is_a_document_the_root_holds(root: Path) -> None:
    os.link(root / "guide.md", root / "hard.md")
    assert read_source(root, "hard.md") == GUIDE.encode()


def test_a_parent_segment_is_refused_rather_than_descended(root: Path) -> None:
    with pytest.raises(Outside):
        read_source(root, "../outside/secret.md")


def test_a_current_segment_and_an_empty_one_are_refused(root: Path) -> None:
    with pytest.raises(Outside):
        read_source(root, "./guide.md")
    with pytest.raises(Outside):
        read_source(root, "docs//note.md")


def test_an_absolute_path_is_refused_as_an_empty_leading_segment(root: Path) -> None:
    with pytest.raises(Outside):
        read_source(root, "/guide.md")


def test_a_path_naming_nothing_is_absent(root: Path) -> None:
    with pytest.raises(Absent):
        read_source(root, "missing.md")
    with pytest.raises(Absent):
        read_source(root, "missing/note.md")


def test_a_directory_named_as_a_document_is_absent(root: Path) -> None:
    with pytest.raises(Absent):
        read_source(root, "docs")


def test_a_document_named_as_a_directory_is_absent(root: Path) -> None:
    with pytest.raises(Absent):
        read_source(root, "guide.md/note.md")


def test_a_broken_link_is_refused_as_a_link_rather_than_as_a_missing_file(
    root: Path,
) -> None:
    os.symlink("nowhere.md", root / "dangling.md")
    with pytest.raises(Symlinked):
        read_source(root, "dangling.md")
