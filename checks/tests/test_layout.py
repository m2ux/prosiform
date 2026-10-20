"""Assert the layout check reads git's listing as the listing of a tree.

A tree exists when git tracks a file under it, so what the check compares is
whatever `git ls-files` prints for that tree. The reading is held to a listing
carrying a blank line, which git's output ends with and which names no file,
and to the repository itself, where an ignored directory is present on disk
and absent from the listing.
"""

import subprocess
from collections.abc import Callable
from pathlib import Path

import layout
import pytest

Run = Callable[..., subprocess.CompletedProcess[str]]


def listing(output: str) -> Run:
    """A `git ls-files` that printed the supplied lines."""

    def run(*arguments: object, **keywords: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            args=["git", "ls-files"], returncode=0, stdout=output, stderr=""
        )

    return run


def test_a_listing_names_one_file_for_each_line(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(subprocess, "run", listing("docs/one.md\ndocs/two.md\n"))
    assert layout.tracked_files("docs") == ["docs/one.md", "docs/two.md"]


def test_a_blank_line_names_no_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(subprocess, "run", listing("docs/one.md\n\n\n"))
    assert layout.tracked_files("docs") == ["docs/one.md"]


def test_a_tree_git_tracks_nothing_under_holds_no_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(subprocess, "run", listing(""))
    assert layout.tracked_files("docs") == []


def test_every_required_tree_holds_a_tracked_file() -> None:
    for tree in layout.REQUIRED_TREES:
        assert layout.tracked_files(tree), f"{tree}/ holds no tracked file"


def test_a_tree_lists_the_files_under_it_and_no_others() -> None:
    assert all(name.startswith("src/") for name in layout.tracked_files("src"))


def test_a_directory_git_ignores_is_absent_from_a_tree_listing() -> None:
    ignored = layout.ROOT / "src" / ".venv"
    if not ignored.is_dir():
        pytest.skip("the build's environment is absent, so nothing ignored is present")
    assert not any(
        Path(name).parts[:2] == ("src", ".venv") for name in layout.tracked_files("src")
    ), "an untracked directory entered the listing, which a fresh checkout has not got"
