"""File-owned dependency authority, bootstrap access and source identity."""

from pathlib import Path
from typing import Any

import pytest
from test_cli import invoke, written

from prosiform import cli
from prosiform.access import read_source


def declared(text: str) -> str:
    return f"---\nprosiform: {{}}\n---\n{text}"


def test_entries_and_linked_files_default_to_invocation_directory(
    tmp_path: Path,
) -> None:
    written(tmp_path, "entry/a.md", declared("# A\n\n[B](../linked/b.md)\n"))
    written(tmp_path, "linked/b.md", declared("# B\n\n[C](../c.md)\n"))
    written(tmp_path, "c.md", declared("# C\n\nShared cwd.\n\n[Above](../c.md)\n"))
    run = invoke("entry/a.md", cwd=tmp_path)
    assert run.status == 0
    assert "Shared cwd." in run.bundle
    assert "[Above](../c.md)" in run.bundle


def test_links_resolve_from_their_own_file_and_a_fragment_names_its_document(
    tmp_path: Path,
) -> None:
    written(
        tmp_path,
        "entries/a.md",
        declared("# A\n\n[Self](#a) [B](../library/b.md)\n"),
    )
    written(tmp_path, "library/b.md", declared("# B\n\n[C](../other/c.md)\n"))
    written(tmp_path, "other/c.md", declared("# C\n\nSeparate library.\n"))
    run = invoke("entries/a.md", cwd=tmp_path)
    assert run.status == 0
    assert "Separate library." in run.bundle
    assert "[Self](#a)" in run.bundle


def test_parent_entry_bootstrap_and_referrer(tmp_path: Path) -> None:
    written(tmp_path, "a.md", "# A\n\n## Part\n\nParent content.\n")
    (tmp_path / "caller").mkdir()
    run = invoke("-f", "../a.md", "#part", cwd=tmp_path / "caller")
    assert run.status == 0
    assert "Parent content." in run.bundle


def test_same_named_targets_in_distinct_directories_keep_a_stable_order(
    tmp_path: Path,
) -> None:
    written(tmp_path, "one/a.md", declared("# A\n\n[Target](x.md)\n"))
    written(tmp_path, "one/x.md", declared("# X\n\nFirst target.\n"))
    written(tmp_path, "two/b.md", declared("# B\n\n[Target](x.md)\n"))
    written(tmp_path, "two/x.md", declared("# X\n\nSecond target.\n"))
    forward = invoke("one/a.md", "two/b.md", cwd=tmp_path)
    reverse = invoke("two/b.md", "one/a.md", cwd=tmp_path)
    assert forward.status == reverse.status == 0
    # The entry documents lead in the order they are named, and each
    # target follows in the order the bundle first links to it.
    assert forward.bundle.index("# A\n") < forward.bundle.index("# B\n")
    assert reverse.bundle.index("# B\n") < reverse.bundle.index("# A\n")
    assert forward.bundle.index("First target.") < forward.bundle.index(
        "Second target."
    )
    assert reverse.bundle.index("Second target.") < reverse.bundle.index(
        "First target."
    )
    assert "[Target](#x)" in forward.bundle and "[Target](#x-1)" in forward.bundle


def test_files_in_distinct_directories_are_headed_by_working_directory_paths(
    tmp_path: Path,
) -> None:
    for name in ("one", "two"):
        written(tmp_path, f"{name}/same.md", declared("Body.\n"))
    run = invoke("one/same.md", "two/same.md", cwd=tmp_path)
    assert run.status == 0
    assert run.bundle == "# One/Same\n\nBody.\n\n# Two/Same\n\nBody.\n"


def test_a_shared_target_cycle_is_captured_once(tmp_path: Path) -> None:
    written(tmp_path, "one/a.md", declared("# A\n\n[C](../shared/c.md)\n"))
    written(tmp_path, "two/b.md", declared("# B\n\n[C](../shared/c.md)\n"))
    written(
        tmp_path,
        "shared/c.md",
        declared("# C\n\n[A](../one/a.md) [B](../two/b.md)\n\nOnce.\n"),
    )
    run = invoke("one/a.md", "two/b.md", cwd=tmp_path)
    assert run.status == 0
    assert run.bundle.count("Once.") == 1


def test_deferred_target_is_cwd_relative_and_uri_escaped(tmp_path: Path) -> None:
    written(
        tmp_path,
        "entry/a.md",
        declared("# A\n\n[¬ Later](../library/b%20%25%23%3F.md)\n"),
    )
    written(tmp_path, "library/b %#?.md", declared("# B\n\nHidden.\n"))
    run = invoke("entry/a.md", cwd=tmp_path)
    assert run.status == 0
    assert "[Later](library/b%20%25%23%3F.md)" in run.bundle
    assert "Hidden." not in run.bundle


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


def test_a_replaced_source_directory_prevents_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(tmp_path, "library/a.md", "# A\n")
    original = cli.compose

    def replace_directory(*args: Any, **kwargs: Any) -> Any:
        result = original(*args, **kwargs)
        (tmp_path / "library").rename(tmp_path / "old")
        written(tmp_path, "library/a.md", "# A\n")
        return result

    monkeypatch.setattr(cli, "compose", replace_directory)
    run = invoke("-d", "json", "library/a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.bundle == ""
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


def test_members_in_distinct_directories_are_named_by_their_paths(
    tmp_path: Path,
) -> None:
    for folder in ("one", "two"):
        written(
            tmp_path,
            f"{folder}/same.md",
            "---\nprosiform: {group: rules, group-depth: 2}\n---\n"
            "# Same\n\n## Run\n\nContent.\n",
        )
    run = invoke("one/same.md", "two/same.md", cwd=tmp_path)
    assert run.status == 0
    assert "### One Same\n" in run.bundle and "### Two Same\n" in run.bundle


@pytest.mark.parametrize("linked", [False, True])
def test_a_cached_target_still_verifies_each_access_route(
    tmp_path: Path, linked: bool
) -> None:
    written(tmp_path, "b.md", declared("# B\n"))
    (tmp_path / "real").mkdir()
    (tmp_path / "alias").symlink_to("real", target_is_directory=True)
    if linked:
        written(tmp_path, "a.md", "# A\n\n[B](b.md) [Alias](alias/../b.md)\n")
        entries = ["b.md", "a.md"]
    else:
        entries = ["b.md", "alias/../b.md"]
    run = invoke("-d", "json", *entries, cwd=tmp_path)
    assert run.status == 1
    assert run.bundle == ""
    assert run.diagnostics()[0]["code"] == cli.SOURCE_SYMLINK
