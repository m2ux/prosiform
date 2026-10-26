"""File-owned dependency authority, bootstrap access and source identity."""

from pathlib import Path
from typing import Any

import pytest
from test_cli import invoke, written

from prosiform import cli
from prosiform.access import read_source
from prosiform.bundle import AMBIGUOUS_FILE_GROUP


def rooted(root: str, text: str) -> str:
    return f'---\nprosiform: {{root: "{root}"}}\n---\n{text}'


def test_entries_and_linked_files_default_to_invocation_directory(
    tmp_path: Path,
) -> None:
    written(tmp_path, "entry/a.md", "# A\n\n[B](../linked/b.md)\n")
    written(tmp_path, "linked/b.md", "# B\n\n[C](../c.md)\n")
    written(tmp_path, "c.md", "# C\n\nShared cwd.\n\n[Above](../c.md)\n")
    run = invoke("entry/a.md", cwd=tmp_path)
    assert run.status == 0
    assert "Shared cwd." in run.stdout
    assert "[Above](../c.md)" in run.stdout


def test_library_root_outside_source_and_fragment_self_reference(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "entries/a.md",
        rooted("../library", "# A\n\n[Self](#a) [B](../library/b.md)\n"),
    )
    written(tmp_path, "library/b.md", rooted("../other", "# B\n\n[C](../other/c.md)\n"))
    written(tmp_path, "other/c.md", "# C\n\nSeparate library.\n")
    run = invoke("entries/a.md", cwd=tmp_path)
    assert run.status == 0
    assert "Separate library." in run.stdout
    assert "[Self](#a)" in run.stdout


def test_parent_entry_bootstrap_and_referrer(tmp_path: Path) -> None:
    written(tmp_path, "a.md", "# A\n\n## Part\n\nParent content.\n")
    (tmp_path / "caller").mkdir()
    run = invoke("-f", "../a.md", "#part", cwd=tmp_path / "caller")
    assert run.status == 0
    assert "Parent content." in run.stdout


def test_distinct_roots_have_distinct_targets_and_stable_order(tmp_path: Path) -> None:
    written(tmp_path, "one/a.md", rooted(".", "# A\n\n[Target](x.md)\n"))
    written(tmp_path, "one/x.md", rooted("..", "# X\n\nFirst target.\n"))
    written(tmp_path, "two/b.md", rooted(".", "# B\n\n[Target](x.md)\n"))
    written(tmp_path, "two/x.md", rooted("..", "# X\n\nSecond target.\n"))
    forward = invoke("one/a.md", "two/b.md", cwd=tmp_path)
    reverse = invoke("two/b.md", "one/a.md", cwd=tmp_path)
    assert forward.status == reverse.status == 0
    # The first entry document leads, so the two orders differ in which
    # document opens the bundle; every other arrangement follows the
    # sources and the two agree below the leader.
    assert forward.stdout.index("# A\n") < forward.stdout.index("# B\n")
    assert reverse.stdout.index("# B\n") < reverse.stdout.index("# A\n")
    assert "First target." in forward.stdout and "Second target." in forward.stdout
    assert (
        forward.stdout[forward.stdout.index("# One/X") :]
        == (reverse.stdout[reverse.stdout.index("# One/X") :])
    )


def test_equal_displayed_files_under_distinct_roots_are_ambiguous(
    tmp_path: Path,
) -> None:
    for name in ("one", "two"):
        written(tmp_path, f"{name}/same.md", rooted(".", "# Same\n"))
    run = invoke("-d", "json", "one/same.md", "two/same.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == AMBIGUOUS_FILE_GROUP


def test_shared_target_cycle_retains_its_own_root(tmp_path: Path) -> None:
    written(tmp_path, "one/a.md", rooted("../shared", "# A\n\n[C](../shared/c.md)\n"))
    written(tmp_path, "two/b.md", rooted("../shared", "# B\n\n[C](../shared/c.md)\n"))
    written(
        tmp_path,
        "shared/c.md",
        rooted("..", "# C\n\n[A](../one/a.md) [B](../two/b.md)\n\nOnce.\n"),
    )
    run = invoke("one/a.md", "two/b.md", cwd=tmp_path)
    assert run.status == 0
    assert run.stdout.count("Once.") == 1


def test_deferred_target_is_cwd_relative_and_uri_escaped(tmp_path: Path) -> None:
    written(
        tmp_path,
        "entry/a.md",
        rooted("../library", "# A\n\n[¬Later](../library/b%20%25%23%3F.md)\n"),
    )
    written(tmp_path, "library/b %#?.md", "# B\n\nHidden.\n")
    run = invoke("entry/a.md", cwd=tmp_path)
    assert run.status == 0
    assert "[Later](library/b%20%25%23%3F.md)" in run.stdout
    assert "Hidden." not in run.stdout


@pytest.mark.parametrize("root", ["missing", "file.md"])
def test_missing_or_non_directory_root_has_original_location(
    tmp_path: Path, root: str
) -> None:
    written(tmp_path, "file.md", "# File\n")
    written(tmp_path, "a.md", rooted(root, "# A\n"))
    run = invoke("-d", "json", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == cli.ROOT_NOT_FOUND
    assert run.diagnostics()[0]["location"] == {"file": "a.md", "line": 2, "column": 19}


@pytest.mark.parametrize("entry", ["alias/a.md", "alias/../a.md"])
def test_bootstrap_checks_components_before_normalization(
    tmp_path: Path, entry: str
) -> None:
    written(tmp_path, "a.md", "# A\n")
    (tmp_path / "real").mkdir()
    (tmp_path / "alias").symlink_to("real", target_is_directory=True)
    run = invoke("-d", "json", entry, cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == cli.SOURCE_SYMLINK


def test_root_walk_checks_symlinks_before_parent_segments(tmp_path: Path) -> None:
    (tmp_path / "real").mkdir()
    (tmp_path / "alias").symlink_to("real", target_is_directory=True)
    written(tmp_path, "a.md", rooted("alias/..", "# A\n"))
    run = invoke("-d", "json", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == cli.SOURCE_SYMLINK


def test_outside_root_link_is_an_unopened_citation(tmp_path: Path) -> None:
    written(tmp_path, "a.md", rooted("library", "# A\n\n[Outside](../missing.md)\n"))
    (tmp_path / "library").mkdir()
    run = invoke("a.md", cwd=tmp_path)
    assert run.status == 0
    assert "[Outside](../missing.md)" in run.stdout


def test_a_link_beside_its_file_outside_the_root_is_an_unopened_citation(
    tmp_path: Path,
) -> None:
    written(tmp_path, "a.md", rooted("library", "# A\n\n[Beside](b.md)\n"))
    written(tmp_path, "b.md", "# B\n\nBeside the entry.\n")
    written(tmp_path, "library/b.md", "# B\n\nInside the root.\n")
    run = invoke("a.md", cwd=tmp_path)
    assert run.status == 0
    assert "[Beside](b.md)" in run.stdout
    assert "Beside the entry." not in run.stdout
    assert "Inside the root." not in run.stdout


def test_root_replacement_prevents_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "a.md", rooted("library", "# A\n"))
    (tmp_path / "library").mkdir()
    original = cli.compose

    def replace_root(*args: Any, **kwargs: Any) -> Any:
        result = original(*args, **kwargs)
        (tmp_path / "library").rename(tmp_path / "old")
        (tmp_path / "library").mkdir()
        return result

    monkeypatch.setattr(cli, "compose", replace_root)
    run = invoke("-d", "json", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.stdout == ""
    assert run.diagnostics()[0]["code"] == cli.SOURCE_CHANGED


def test_raw_limit_stops_before_complete_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "a.md", "# A\n" + "x" * 10000)
    original = read_source
    sizes = []

    def read(*args: Any, **kwargs: Any) -> bytes:
        data = original(*args, **kwargs)
        sizes.append(len(data))
        return data

    monkeypatch.setattr(cli, "read_source", read)
    run = invoke("-B", "8", "-d", "json", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == "E_RESOURCE_LIMIT"
    assert sizes == [9]


def test_root_option_is_invalid_usage(tmp_path: Path) -> None:
    run = invoke("-r", ".", "a.md", cwd=tmp_path)
    assert run.status == 2


def test_equal_member_names_across_roots_are_ambiguous(tmp_path: Path) -> None:
    for folder in ("one", "two"):
        written(
            tmp_path,
            f"{folder}/same.md",
            "---\nprosiform: {root: ., group: rules, group-depth: 2}\n---\n"
            "# Same\n\n## Run\n\nContent.\n",
        )
    run = invoke("-d", "json", "one/same.md", "two/same.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == AMBIGUOUS_FILE_GROUP


@pytest.mark.parametrize("linked", [False, True])
def test_a_cached_target_still_verifies_each_access_route(
    tmp_path: Path, linked: bool
) -> None:
    written(tmp_path, "b.md", "# B\n")
    (tmp_path / "real").mkdir()
    (tmp_path / "alias").symlink_to("real", target_is_directory=True)
    if linked:
        written(tmp_path, "a.md", "# A\n\n[B](b.md) [Alias](alias/../b.md)\n")
        entries = ["b.md", "a.md"]
    else:
        entries = ["b.md", "alias/../b.md"]
    run = invoke("-d", "json", *entries, cwd=tmp_path)
    assert run.status == 1
    assert run.stdout == ""
    assert run.diagnostics()[0]["code"] == cli.SOURCE_SYMLINK
