"""Entry-derived destinations through the real CLI and atomic publication gate."""

import os
from contextlib import chdir
from io import StringIO
from pathlib import Path
from typing import Any

import pytest
from test_cli import Run, written
from test_file_roots import rooted

from prosiform import cli


def invoke(root: Path, *arguments: str) -> Run:
    out, err = StringIO(), StringIO()
    with chdir(root):
        status = cli.main(list(arguments), out, err)
    return Run(status, out.getvalue(), err.getvalue())


@pytest.mark.parametrize("suffix", [".md", ".markdown", ".MD", ".MARKDOWN"])
@pytest.mark.parametrize("fragment", ["", "#part", "#p%61rt"])
def test_file_and_section_names_follow_the_working_directory_path(
    tmp_path: Path, suffix: str, fragment: str
) -> None:
    name = f"Skill/modes/Run_it{suffix}"
    written(tmp_path, name, rooted("..", "# Run\n\n## Part\n\nSelected.\n"))
    run = invoke(tmp_path, name + fragment)
    output = "Skill_modes_Run_it" + ("__part" if fragment else "") + ".bundle.md"
    assert run.status == 0 and run.stdout == ""
    assert "Selected." in (tmp_path / output).read_text()


@pytest.mark.parametrize(
    "arguments",
    [
        ("dir/a.md", "dir/./a.md#"),
        ("dir/a.md#part", "dir/a.md#p%61rt"),
        ("-f", "dir/a.md", "#part", "dir/a.md#part"),
    ],
)
def test_equivalent_selections_share_one_derived_destination(
    tmp_path: Path, arguments: tuple[str, ...]
) -> None:
    written(tmp_path, "dir/a.md", "# A\n\n## Part\n\nContent.\n")
    run = invoke(tmp_path, *arguments)
    assert run.status == 0 and run.stdout == ""
    assert len(list(tmp_path.glob("dir_a*.bundle.md"))) == 1


@pytest.mark.parametrize(
    ("references", "name"),
    [
        (("a.md", "b.md"), "a+b.bundle.md"),
        (("b.md", "a.md"), "b+a.bundle.md"),
        (("a.md#one", "a.md#two"), "a__one+a__two.bundle.md"),
        (("a.md", "a.md#one", "./a.md"), "a+a__one.bundle.md"),
        (("-f", "a.md", "#two", "b.md"), "a__two+b.bundle.md"),
    ],
)
@pytest.mark.parametrize("check", [False, True])
def test_distinct_selections_join_their_names_in_entry_order(
    tmp_path: Path, references: tuple[str, ...], name: str, check: bool
) -> None:
    written(tmp_path, "a.md", "# A\n\n## One\n\nFirst.\n\n## Two\n\nSecond.\n")
    written(tmp_path, "b.md", "# B\n")
    flags = ["-c"] if check else []
    run = invoke(tmp_path, *flags, *references)
    assert run.status == 0 and run.stdout == ""
    published = sorted(path.name for path in tmp_path.glob("*.bundle.md"))
    assert published == ([] if check else [name])


def test_a_declared_root_does_not_rename_an_entry_s_output(tmp_path: Path) -> None:
    written(tmp_path, "entries/a.md", rooted("../library", "# A\n\n[B](b.md)\n"))
    written(tmp_path, "library/b.md", rooted(".", "# B\n"))
    run = invoke(tmp_path, "entries/a.md")
    assert run.status == 0
    assert (tmp_path / "entries_a.bundle.md").is_file()


def test_a_parent_relative_entry_s_name_is_filename_text(tmp_path: Path) -> None:
    written(tmp_path, "entries/a.md", "# A\n")
    (tmp_path / "work").mkdir()
    run = invoke(tmp_path / "work", "../entries/a.md")
    assert run.status == 0
    assert (tmp_path / "work" / ".._entries_a.bundle.md").is_file()


def test_fragment_referrer_and_check_mode(tmp_path: Path) -> None:
    written(tmp_path, "dir/a.md", rooted(".", "# A\n\n## Part\n\nContent.\n"))
    assert invoke(tmp_path, "-c", "-f", "dir/a.md", "#part").status == 0
    assert not (tmp_path / "dir_a__part.bundle.md").exists()
    assert invoke(tmp_path, "-f", "dir/a.md", "#part").status == 0
    assert "Content." in (tmp_path / "dir_a__part.bundle.md").read_text()


@pytest.mark.parametrize("deferred", [False, True])
@pytest.mark.parametrize("check", [False, True])
def test_derived_destination_cannot_overlap_any_captured_source(
    tmp_path: Path, deferred: bool, check: bool
) -> None:
    mark = "¬ " if deferred else ""
    written(tmp_path, "a.md", f"# A\n\n[{mark}Captured](a.bundle.md)\n")
    written(tmp_path, "a.bundle.md", "# Captured\n\nPreserve.\n")
    run = invoke(tmp_path, *(["-c"] if check else []), "a.md")
    assert run.status == 2 and run.stdout == ""
    assert (tmp_path / "a.bundle.md").read_text() == "# Captured\n\nPreserve.\n"


def test_derived_publication_is_one_atomic_replace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "a.md", "# A\n\nComplete.\n")
    written(tmp_path, "a.bundle.md", "Existing.")
    original = os.replace
    calls = []

    def replace(source: Path, target: Path) -> None:
        assert target.read_text() == "Existing."
        assert "Complete." in source.read_text()
        calls.append((source, target))
        original(source, target)

    monkeypatch.setattr(os, "replace", replace)
    assert invoke(tmp_path, "a.md").status == 0
    assert len(calls) == 1
    assert not list(tmp_path.glob(".a.bundle.md.*"))


def test_atomic_failure_preserves_existing_destination(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "a.md", "# A\n")
    written(tmp_path, "a.bundle.md", "Existing.")

    def refuse(*args: Any) -> None:
        raise OSError("publication refused")

    monkeypatch.setattr(os, "replace", refuse)
    run = invoke(tmp_path, "a.md")
    assert run.status == 3 and run.stdout == ""
    assert (tmp_path / "a.bundle.md").read_text() == "Existing."
    assert not list(tmp_path.glob(".a.bundle.md.*"))


@pytest.mark.parametrize("flags", [("-x", "source-changed"), ("-O", "1")])
def test_failed_validation_preserves_existing_derived_output(
    tmp_path: Path, flags: tuple[str, ...]
) -> None:
    written(tmp_path, "a.md", "# A\n")
    written(tmp_path, "a.bundle.md", "Existing.")
    run = invoke(tmp_path, *flags, "a.md")
    assert run.status == 1 and run.stdout == ""
    assert (tmp_path / "a.bundle.md").read_text() == "Existing."


def test_filename_length_failure_is_publication_failure(tmp_path: Path) -> None:
    name = "a" * 150 + "/" + "b" * 150 + ".md"
    written(tmp_path, name, "# A\n")
    run = invoke(tmp_path, "-d", "json", name)
    assert run.status == 3 and run.stdout == ""
    assert run.diagnostics()[0]["code"] == cli.PUBLICATION_FAILED
