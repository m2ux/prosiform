"""Captured settings, source coordinates and publication boundaries."""

from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import pytest
from test_cli import invoke

from prosiform import cli
from prosiform.access import read_source
from prosiform.closure import resolve
from prosiform.diagnostics import Location
from prosiform.limits import BUDGETS, Limits
from prosiform.metadata import InvalidMetadata
from prosiform.source import content, hashed


def settings(group: str) -> str:
    return f"prosiform:\n  group: {group}\n  group-depth: 2\n"


@pytest.mark.parametrize("ending", ["\n", "\r\n"])
@pytest.mark.parametrize("closer", ["---", "..."])
@pytest.mark.parametrize("mark", ["", "\ufeff"])
def test_settings_and_body_share_physical_coordinates(
    ending: str, closer: str, mark: str
) -> None:
    text = mark + ("---\n" + settings("règles") + closer + "\n# Body\n").replace(
        "\n", ending
    )
    source = content(text, file="rules/a.md")
    assert source.text == "# Body" + ending
    assert source.line(1) == 6
    assert source.conversion.group == "règles"
    assert source.conversion.depth == 2
    assert source.conversion.group_location == Location("rules/a.md", 3, 10)
    with pytest.raises(FrozenInstanceError):
        source.conversion.group = "other"  # type: ignore[misc]


def test_settings_are_per_source_and_not_inherited() -> None:
    assert content("---\n" + settings("one") + "---\n").conversion.group == "one"
    assert content("---\n" + settings("two") + "---\n").conversion.group == "two"
    assert content("# Plain\n").conversion.group is None


def test_root_declaration_belongs_to_captured_bytes(tmp_path: Path) -> None:
    path = tmp_path / "a.md"
    (tmp_path.parent / "library").mkdir(exist_ok=True)
    raw = b"---\nprosiform:\n  root: ../library\n---\n# A\n"
    path.write_bytes(raw)
    opened = cli.read_document(
        tmp_path, resolve("a.md"), Limits({b: b.default for b in BUDGETS})
    )
    path.write_bytes(raw.replace(b"../library", b"../other"))
    assert opened.source.conversion.root == "../library"
    assert opened.source.conversion.root_location == Location("a.md", 3, 9)
    assert opened.capture.digest == hashed(raw)
    assert content("# Linked\n").conversion.root is None
    with pytest.raises(cli.Failure) as caught:
        cli.recheck(tmp_path, {"a.md": opened.capture})
    assert caught.value.diagnostic.code == cli.SOURCE_CHANGED


def test_duplicate_key_reports_original_locations() -> None:
    with pytest.raises(InvalidMetadata) as error:
        content("\ufeff---\r\nname: first\r\nname: second\r\n...\r\n", file="a.md")
    diagnostic = error.value.diagnostic
    assert diagnostic.location == Location("a.md", 3, 1)
    assert diagnostic.related is not None
    assert diagnostic.related[0].line == 2


def test_capture_hash_covers_frontmatter_and_body(tmp_path: Path) -> None:
    path = tmp_path / "a.md"
    raw = ("\ufeff---\n" + settings("one") + "---\n# A\n").encode()
    path.write_bytes(raw)
    opened = cli.read_document(
        tmp_path, resolve("a.md"), Limits({b: b.default for b in BUDGETS})
    )
    path.write_text("---\n" + settings("two") + "---\n# A\n")
    assert opened.size == len(raw)
    assert opened.capture.digest == hashed(raw)
    assert opened.source.conversion.group == "one"
    with pytest.raises(cli.Failure) as error:
        cli.recheck(tmp_path, {"a.md": opened.capture})
    assert error.value.diagnostic.code == cli.SOURCE_CHANGED


def test_metadata_is_not_a_markdown_dependency(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text(
        '---\ndescription: "# Hidden [!missing](missing.md)"\n'
        'metadata: {owner: "[!missing](missing.md)"}\n---\n# A\n\nBody.\n'
    )
    run = invoke("a.md", cwd=tmp_path)
    assert run.status == 0
    assert "Hidden" not in run.stdout
    assert "missing" not in run.stdout
    assert "Body." in run.stdout


@pytest.mark.parametrize("diagnostics", ["text", "json"])
def test_metadata_error_preserves_output_and_coordinates(
    tmp_path: Path, diagnostics: str
) -> None:
    (tmp_path / "a.md").write_bytes(
        b"\xef\xbb\xbf---\r\nprosiform: 7\r\n...\r\n# A\r\n"
    )
    output = tmp_path / "out.md"
    output.write_text("existing\n")
    run = invoke("-d", diagnostics, "-o", str(output), "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.stdout == ""
    assert output.read_text() == "existing\n"
    if diagnostics == "json":
        diagnostic = run.diagnostics()[0]
        assert diagnostic["code"] == "E_INVALID_CONVERSION_METADATA"
        assert diagnostic["location"] == {"file": "a.md", "line": 2, "column": 12}
    else:
        assert "location: a.md:2:12" in run.stderr


@pytest.mark.parametrize("option", ["-B", "-I"])
def test_raw_byte_budget_precedes_yaml_and_encoding(
    tmp_path: Path, option: str
) -> None:
    (tmp_path / "a.md").write_bytes(b"---\na: [\n---\n\xff")
    run = invoke("-d", "json", option, "3", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == "E_RESOURCE_LIMIT"
    assert option in run.diagnostics()[0]["message"]


def test_yaml_collection_depth_is_bounded(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("---\na: {b: {c: value}}\n---\n# A\n")
    run = invoke("-d", "json", "-N", "2", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == "E_RESOURCE_LIMIT"
    assert run.diagnostics()[0]["location"]["line"] == 2


def test_deferred_source_is_captured_once_and_contributes_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "a.md").write_text("# A\n\n[¬ One](b.md#one) [¬ Two](b.md#two)\n")
    (tmp_path / "b.md").write_text(
        "---\n" + settings("b") + "---\n# One\n\n## Two\n\nHidden.\n"
    )
    original = read_source
    reads: list[str] = []

    def read(root: Path, name: str, **kwargs: Any) -> bytes:
        reads.append(name)
        return original(root, name, **kwargs)

    monkeypatch.setattr(cli, "read_source", read)
    run = invoke("-F", "2", "a.md", cwd=tmp_path)
    assert run.status == 0
    assert "Hidden." not in run.stdout
    # One discovery read and one publication recheck for each captured source.
    assert reads.count("a.md") == 2
    assert reads.count("b.md") == 2


@pytest.mark.parametrize("option", ["-B", "-I", "-F"])
def test_deferred_source_counts_towards_raw_budgets(
    tmp_path: Path, option: str
) -> None:
    a = "# A\n\n[¬ B](b.md)\n"
    (tmp_path / "a.md").write_text(a)
    (tmp_path / "b.md").write_text("---\nname: " + "x" * 100 + "\n---\n# B\n")
    bound = "1" if option == "-F" else str(len(a.encode()) + 1)
    run = invoke("-d", "json", option, bound, "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.diagnostics()[0]["code"] == "E_RESOURCE_LIMIT"
    assert option in run.diagnostics()[0]["message"]


def test_deferred_metadata_failure_is_an_input_failure(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("# A\n\n[¬ B](b.md)\n")
    (tmp_path / "b.md").write_text("---\na: [\n---\n# B\n")
    run = invoke("-d", "json", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.stdout == ""
    assert run.diagnostics()[0]["code"] == "E_INVALID_FRONTMATTER"
    assert run.diagnostics()[0]["location"]["file"] == "b.md"


def test_deferred_metadata_change_is_rechecked_with_its_chain(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "a.md").write_text("# A\n\n[¬ B](b.md)\n")
    (tmp_path / "b.md").write_text("---\n" + settings("one") + "---\n# B\n")
    reads = 0

    def read(root: Path, name: str, **kwargs: Any) -> bytes:
        nonlocal reads
        if name == "b.md":
            reads += 1
            if reads == 2:
                (root / name).write_text("---\n" + settings("two") + "---\n# B\n")
        return read_source(root, name, **kwargs)

    monkeypatch.setattr(cli, "read_source", read)
    run = invoke("-d", "json", "a.md", cwd=tmp_path)
    assert run.status == 1
    assert run.stdout == ""
    diagnostic = run.diagnostics()[0]
    assert diagnostic["code"] == "E_SOURCE_CHANGED"
    assert diagnostic["chain"] == ["a.md", "b.md"]
