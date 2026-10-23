"""Per-file settings across closure selection and atomic publication."""

from pathlib import Path

import pytest
from test_cli import conversion, invoke, written


@pytest.mark.parametrize(
    "references", [("a.md",), ("a.md#run",), ("a.md#run", "a.md#run")]
)
def test_linked_destination_owns_its_settings(
    tmp_path: Path, references: tuple[str, ...]
) -> None:
    written(
        tmp_path,
        "a.md",
        conversion("entry", 2) + "# A\n\n## Run\n\n[Target](other/b.md#run).\n",
    )
    written(
        tmp_path,
        "other/b.md",
        conversion("target", 2) + "# B\n\n## Run\n\nTarget content.\n",
    )
    written(tmp_path, "other/sibling.md", "# Sibling\n\nNot discovered.\n")
    run = invoke("-r", str(tmp_path), *references)
    assert run.status == 0, run.stderr
    assert "# Entry\n" in run.stdout and "# Target\n" in run.stdout
    assert "[Target](#run-1)" in run.stdout
    assert run.stdout.count("Target content.") == 1
    assert "Not discovered." not in run.stdout
    assert "prosiform-group" not in run.stdout


def test_diamond_cycle_and_unannotated_sibling_keep_source_ownership(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "entry.md",
        conversion("entry", 1) + "# Entry\n\n[A](a.md#run) [B](b.md#run)\n",
    )
    written(
        tmp_path,
        "a.md",
        conversion("shared", 2) + "# A\n\n## Run\n\n[C](nested/c.md#run)\n",
    )
    written(tmp_path, "b.md", "# B\n\n## Run\n\n[C](nested/c.md#run)\n")
    written(
        tmp_path,
        "nested/c.md",
        conversion("shared", 2) + "# C\n\n## Run\n\n[A](../a.md#run)\n\nUnique body.\n",
    )
    run = invoke("-r", str(tmp_path), "entry.md")
    assert run.status == 0, run.stderr
    assert run.stdout.count("Unique body.") == 1
    assert (
        "# Shared\n" in run.stdout
        and "# B\n" in run.stdout
        and "# Entry\n" in run.stdout
    )
    assert "### A\n" in run.stdout and "### C\n" in run.stdout


@pytest.mark.parametrize("active", [False, True])
def test_deferred_only_metadata_does_not_join_or_conflict(
    tmp_path: Path, active: bool
) -> None:
    written(
        tmp_path,
        "a.md",
        conversion("shared", 2)
        + "# A\n\n[¬ Later](b.md)\n"
        + ("[Now](b.md)\n" if active else ""),
    )
    written(tmp_path, "b.md", conversion("shared", 3) + "# B\n\nLater content.\n")
    run = invoke("-r", str(tmp_path), "-d", "json", "a.md")
    assert run.status == (1 if active else 0), run.stderr
    if active:
        assert run.diagnostics()[0]["code"] == "E_GROUP_DEPTH_CONFLICT"
    else:
        assert "Later content." not in run.stdout
        assert "[¬ Later](b.md)" in run.stdout


@pytest.mark.parametrize("mode", ["stdout", "file", "check"])
@pytest.mark.parametrize("form", ["text", "json"])
def test_conflicting_depths_are_stable_and_atomic(
    tmp_path: Path, mode: str, form: str
) -> None:
    written(tmp_path, "a.md", conversion("shared", 2) + "# A\n")
    written(tmp_path, "b.md", conversion("shared", 3) + "# B\n")
    output = tmp_path / "output.md"
    output.write_text("preserved\n")
    options = [] if mode == "stdout" else ["-o", str(output)]
    if mode == "check":
        options.append("-c")
    forward = invoke("-r", str(tmp_path), "-d", form, *options, "a.md", "b.md")
    reverse = invoke("-r", str(tmp_path), "-d", form, *options, "b.md", "a.md")
    assert forward.status == reverse.status == 1
    assert forward.stdout == reverse.stdout == ""
    assert forward.stderr == reverse.stderr
    assert output.read_text() == "preserved\n"
    if form == "json":
        diagnostic = forward.diagnostics()[0]
        assert diagnostic["code"] == "E_GROUP_DEPTH_CONFLICT"
        assert diagnostic["location"] == {"file": "a.md", "line": 4, "column": 26}
        assert diagnostic["related"][0] == {
            "file": "b.md",
            "line": 4,
            "column": 26,
            "message": "metadata.prosiform-group-depth for group 'shared' is 3",
        }
    else:
        assert "a.md:4:26" in forward.stderr and "b.md:4:26" in forward.stderr


@pytest.mark.parametrize(
    "group", ["rules", "other.name", "x\\y", "*group*", "a # b", " spaced "]
)
def test_group_names_have_no_directory_requirement(tmp_path: Path, group: str) -> None:
    for path, text in [("x/notes.md", "First."), ("y/notes.md", "Second.")]:
        written(
            tmp_path, path, conversion(group, 2) + "# Notes\n\n## Run\n\n" + text + "\n"
        )
    run = invoke("-r", str(tmp_path), "x/notes.md", "y/notes.md")
    assert run.status == 0, run.stderr
    assert "### X Notes\n" in run.stdout and "### Y Notes\n" in run.stdout
    assert "First." in run.stdout and "Second." in run.stdout


def test_group_and_file_heading_identities_remain_distinct(tmp_path: Path) -> None:
    written(tmp_path, "a.md", conversion("same", 2) + "# A\n\n[Other](same.md)\n")
    written(tmp_path, "same.md", "# Same\n\nSeparate file.\n")
    run = invoke("-r", str(tmp_path), "a.md")
    assert run.status == 0, run.stderr
    assert run.stdout.count("# Same\n") == 2
    assert "[Other](#same-1)" in run.stdout


def test_exact_group_strings_are_distinct(tmp_path: Path) -> None:
    for name, group in [("a", "rules"), ("b", "Rules"), ("c", " rules ")]:
        written(tmp_path, name + ".md", conversion(group, 2) + "# " + name + "\n")
    run = invoke("-r", str(tmp_path), "a.md", "b.md", "c.md")
    assert run.status == 0, run.stderr
    assert run.stdout.count("# Rules\n") == 3


@pytest.mark.parametrize("option", ["-g", "-grules:2", "--group"])
def test_structural_cli_arguments_are_usage_errors(tmp_path: Path, option: str) -> None:
    run = invoke("-r", str(tmp_path), "-d", "json", option, "rules:2", "a.md")
    assert run.status == 2
    assert run.stdout == ""
    assert run.diagnostics()[0]["code"] == "E_INVALID_USAGE"
