"""Entry-derived folders and names through the real CLI and its atomic publication.

A run writes its bundles into a folder under the output folder named for
its entry with the `.bundles` suffix, and the entry's bundle in it carries
that name with the bundle suffix.
"""

import os
from contextlib import chdir
from io import StringIO
from pathlib import Path
from typing import Any

import pytest
from test_cli import Run, written
from test_file_roots import rooted

from prosiform import cli


def bundle(folder: Path, name: str) -> Path:
    """The entry bundle a run named so writes under one output folder."""
    return folder / f"{name}.bundles" / f"{name}.bundle.md"


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
    output = "Skill_modes_Run_it" + ("__part" if fragment else "")
    assert run.status == 0 and run.stdout == ""
    assert "Selected." in bundle(tmp_path, output).read_text()


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
    assert len(list(tmp_path.glob("dir_a*.bundles/dir_a*.bundle.md"))) == 1


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
    published = sorted(path.name for path in tmp_path.glob("*/*.bundle.md"))
    assert published == ([] if check else [name])


def test_a_declared_root_does_not_rename_an_entry_s_output(tmp_path: Path) -> None:
    written(tmp_path, "entries/a.md", rooted("../library", "# A\n\n[B](b.md)\n"))
    written(tmp_path, "library/b.md", rooted(".", "# B\n"))
    run = invoke(tmp_path, "entries/a.md")
    assert run.status == 0
    assert bundle(tmp_path, "entries_a").is_file()


def test_a_parent_relative_entry_s_name_is_filename_text(tmp_path: Path) -> None:
    written(tmp_path, "entries/a.md", "# A\n")
    (tmp_path / "work").mkdir()
    run = invoke(tmp_path / "work", "../entries/a.md")
    assert run.status == 0
    assert bundle(tmp_path / "work", ".._entries_a").is_file()


def test_fragment_referrer_and_check_mode(tmp_path: Path) -> None:
    written(tmp_path, "dir/a.md", rooted(".", "# A\n\n## Part\n\nContent.\n"))
    assert invoke(tmp_path, "-c", "-f", "dir/a.md", "#part").status == 0
    assert not (tmp_path / "dir_a__part.bundles").exists()
    assert invoke(tmp_path, "-f", "dir/a.md", "#part").status == 0
    assert "Content." in bundle(tmp_path, "dir_a__part").read_text()


@pytest.mark.parametrize("deferred", [False, True])
@pytest.mark.parametrize("check", [False, True])
def test_derived_folder_cannot_hold_any_captured_source(
    tmp_path: Path, deferred: bool, check: bool
) -> None:
    mark = "¬ " if deferred else ""
    written(tmp_path, "a.md", f"# A\n\n[{mark}Captured](a.bundles/a.bundle.md)\n")
    written(tmp_path, "a.bundles/a.bundle.md", "# Captured\n\nPreserve.\n")
    run = invoke(tmp_path, *(["-c"] if check else []), "a.md")
    assert run.status == 2 and run.stdout == ""
    assert bundle(tmp_path, "a").read_text() == "# Captured\n\nPreserve.\n"


def test_derived_publication_swaps_the_folder_in_whole(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "a.md", "# A\n\nComplete.\n")
    written(tmp_path, "a.bundles/a.bundle.md", "Existing.")
    original = os.rename
    calls = []

    def rename(source: Path, target: Path) -> None:
        calls.append((Path(source).name, Path(target).name))
        original(source, target)

    monkeypatch.setattr(os, "rename", rename)
    assert invoke(tmp_path, "a.md").status == 0
    [(aside, moved), (staged, placed)] = calls
    assert aside == "a.bundles" and moved.startswith(".pf.old.")
    assert staged.startswith(".pf.new.") and placed == "a.bundles"
    assert "Complete." in bundle(tmp_path, "a").read_text()
    assert sorted(path.name for path in tmp_path.iterdir()) == ["a.bundles", "a.md"]


def test_atomic_failure_preserves_existing_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "a.md", "# A\n")
    written(tmp_path, "a.bundles/a.bundle.md", "Existing.")
    original = os.rename

    def refuse(source: Path, target: Path) -> None:
        if ".new." in str(source):
            raise OSError("publication refused")
        original(source, target)

    monkeypatch.setattr(os, "rename", refuse)
    run = invoke(tmp_path, "a.md")
    assert run.status == 3 and run.stdout == ""
    assert bundle(tmp_path, "a").read_text() == "Existing."
    assert sorted(path.name for path in tmp_path.iterdir()) == ["a.bundles", "a.md"]


@pytest.mark.parametrize("flags", [("-x", "source-changed"), ("-O", "1")])
def test_failed_validation_preserves_existing_derived_output(
    tmp_path: Path, flags: tuple[str, ...]
) -> None:
    written(tmp_path, "a.md", "# A\n")
    written(tmp_path, "a.bundles/a.bundle.md", "Existing.")
    run = invoke(tmp_path, *flags, "a.md")
    assert run.status == 1 and run.stdout == ""
    assert bundle(tmp_path, "a").read_text() == "Existing."


def test_filename_length_failure_is_publication_failure(tmp_path: Path) -> None:
    name = "a" * 150 + "/" + "b" * 150 + ".md"
    written(tmp_path, name, "# A\n")
    run = invoke(tmp_path, "-d", "json", name)
    assert run.status == 3 and run.stdout == ""
    assert run.diagnostics()[0]["code"] == cli.PUBLICATION_FAILED


@pytest.mark.parametrize("dangling", [False, True])
def test_a_link_at_the_run_folder_is_replaced_and_never_followed(
    tmp_path: Path, dangling: bool
) -> None:
    written(tmp_path, "a.md", "# A\n\nComplete.\n")
    precious = tmp_path / "precious"
    if not dangling:
        written(tmp_path, "precious/data.txt", "Keep.\n")
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "a.bundles").symlink_to("../precious")
    run = invoke(tmp_path, "-o", "out", "a.md")
    assert run.status == 0 and run.stdout == ""
    folder = tmp_path / "out" / "a.bundles"
    assert folder.is_dir() and not folder.is_symlink()
    assert "Complete." in (folder / "a.bundle.md").read_text()
    assert sorted(path.name for path in (tmp_path / "out").iterdir()) == ["a.bundles"]
    if dangling:
        assert not precious.exists()
    else:
        assert sorted(path.name for path in precious.iterdir()) == ["data.txt"]
        assert (precious / "data.txt").read_text() == "Keep.\n"


def test_a_run_folder_name_the_filesystem_accepts_publishes(tmp_path: Path) -> None:
    name = "n" * 240
    written(tmp_path, f"{name}.md", "# Long\n")
    run = invoke(tmp_path, f"{name}.md")
    assert run.status == 0 and run.stdout == ""
    assert bundle(tmp_path, name).read_text() == "# Long\n"
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        f"{name}.bundles",
        f"{name}.md",
    ]


@pytest.mark.parametrize("check", [False, True])
def test_two_targets_deriving_one_name_are_refused_naming_both(
    tmp_path: Path, check: bool
) -> None:
    written(tmp_path, "e.md", "# E\n\n1. [⇉ x](a/b.md)\n2. [⇉ y](a_b.md)\n")
    written(tmp_path, "a/b.md", "# B\n")
    written(tmp_path, "a_b.md", "# B too\n")
    run = invoke(tmp_path, "-d", "json", *(["-c"] if check else []), "e.md")
    assert run.status == 3 and run.stdout == ""
    [refused] = run.diagnostics()
    assert refused["code"] == cli.PUBLICATION_FAILED
    assert "'a/b.md'" in refused["message"] and "'a_b.md'" in refused["message"]
    assert "a_b.bundle.md" in refused["message"]
    assert not (tmp_path / "e.bundles").exists()


@pytest.mark.parametrize("check", [False, True])
def test_an_output_folder_that_does_not_exist_fails_the_check_as_the_run(
    tmp_path: Path, check: bool
) -> None:
    written(tmp_path, "a.md", "# A\n")
    run = invoke(tmp_path, "-d", "json", *(["-c"] if check else []), "-o", "zz", "a.md")
    assert run.status == 3 and run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [cli.PUBLICATION_FAILED]
    assert sorted(path.name for path in tmp_path.iterdir()) == ["a.md"]


def test_a_source_changed_between_two_bundles_reads_publishes_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "a.md", "# A\n\n[⇉ plan](plan.md)\n")
    written(tmp_path, "plan.md", "# Plan\n")
    original = cli.compiled
    reads = []

    def edit_after_the_entry(*arguments: Any, **options: Any) -> cli.Compiled:
        one = original(*arguments, **options)
        reads.append(one.name)
        if len(reads) == 1:
            (tmp_path / "plan.md").write_text("# Plan, edited\n")
        return one

    monkeypatch.setattr(cli, "compiled", edit_after_the_entry)
    run = invoke(tmp_path, "-d", "json", "a.md")
    assert reads == ["a.bundle.md", "plan.bundle.md"]
    assert run.status == 1 and run.stdout == ""
    [refused] = run.diagnostics()
    assert refused["code"] == cli.SOURCE_CHANGED
    assert "plan.md" in refused["message"]
    assert not (tmp_path / "a.bundles").exists()


def test_a_failing_run_under_the_cleanup_fault_writes_nothing(tmp_path: Path) -> None:
    written(tmp_path, "a.md", "# A\n\nComplete.\n")
    run = invoke(tmp_path, "-x", "cleanup-refused", "-O", "1", "a.md")
    assert run.status == 1 and run.stdout == ""
    assert sorted(path.name for path in tmp_path.iterdir()) == ["a.md"]


def test_a_dangling_link_under_the_cleanup_fault_is_retained_and_warned(
    tmp_path: Path,
) -> None:
    written(tmp_path, "a.md", "# A\n\nComplete.\n")
    (tmp_path / "a.bundles").symlink_to("nowhere")
    run = invoke(tmp_path, "-d", "json", "-x", "cleanup-refused", "a.md")
    assert run.status == 0 and run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [cli.EARLIER_SET_RETAINED]
    assert "Complete." in bundle(tmp_path, "a").read_text()
    assert not (tmp_path / "nowhere").exists()


@pytest.mark.parametrize("check", [False, True])
def test_a_derived_name_longer_than_the_filesystem_allows_names_its_selection(
    tmp_path: Path, check: bool
) -> None:
    name = "n" * 247
    written(tmp_path, f"{name}.md", "# Long\n")
    run = invoke(tmp_path, "-d", "json", *(["-c"] if check else []), f"{name}.md")
    assert run.status == 3 and run.stdout == ""
    [refused] = run.diagnostics()
    assert refused["code"] == cli.PUBLICATION_FAILED
    assert f"'{name}.md'" in refused["message"]
    assert f"'{name}.bundle.md'" in refused["message"]
    assert ".pf." not in refused["message"]
    assert sorted(path.name for path in tmp_path.iterdir()) == [f"{name}.md"]
