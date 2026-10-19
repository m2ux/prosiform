"""Assert the command's grammar, its stream split and its exit statuses.

The corpus is where a contract clause is declared, and these are the cases
a fixture cannot reach: a response whose text belongs to this build rather
than to the contract, a write the stream refuses, and the status a request
this build cannot carry out returns. Each case names a run, its status,
and what each of the two streams carried.
"""

import json
import os
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import IO, Any

import pytest
from prosiform import PROFILE
from prosiform.bundle import AMBIGUOUS_FILE_GROUP, HEADING_DEPTH_OVERFLOW
from prosiform.cli import (
    INPUT_FAILURE,
    INTERNAL_ERROR,
    INVALID_ENCODING,
    INVALID_GROUP_RULE,
    INVALID_USAGE,
    PUBLICATION_FAILED,
    PUBLICATION_FAILURE,
    ROOT_NOT_FOUND,
    SOURCE_OUTSIDE_ROOT,
    SUCCESS,
    TARGET_NOT_FOUND,
    UNEXPECTED_INTERNAL_ERROR,
    UNSUPPORTED_ENTRY_SUFFIX,
    USAGE_FAILURE,
    main,
    read_entry,
)
from prosiform.profile import RAW_HTML, UNSUPPORTED_CONSTRUCT
from prosiform.source import UNTERMINATED_FRONTMATTER


@dataclass(frozen=True)
class Run:
    """One invocation: the status it returned and what each stream carried."""

    status: int
    stdout: str
    stderr: str

    def diagnostics(self) -> list[dict[str, Any]]:
        """The diagnostics standard error carries, each line parsed as JSON."""
        return [json.loads(line) for line in self.stderr.splitlines() if line.strip()]


def invoke(*arguments: str, stdout: IO[str] | None = None) -> Run:
    """One run of the command against captured streams."""
    out = StringIO() if stdout is None else stdout
    err = StringIO()
    status = main(list(arguments), out, err)
    written = out.getvalue() if isinstance(out, StringIO) else ""
    return Run(status, written, err.getvalue())


class Refusing(StringIO):
    """A stream that refuses everything written to it."""

    def write(self, text: str) -> int:
        raise OSError(32, "Broken pipe")


@pytest.fixture
def root(tmp_path: Path) -> Path:
    """A source root carrying one document and one directory of documents."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "note.md").write_text("# Note\n")
    (tmp_path / "guide.md").write_text("# Guide\n")
    return tmp_path


def test_the_version_response_names_the_version_and_the_profile() -> None:
    run = invoke("--version")
    assert run.status == SUCCESS
    assert run.stdout == f"prosiform 0.1.0 ({PROFILE})\n"
    assert run.stderr == ""


def test_the_help_response_shows_usage_defaults_and_exit_statuses() -> None:
    run = invoke("--help")
    assert run.status == SUCCESS
    assert run.stdout.startswith("usage: prosiform --root DIR [OPTIONS] REF [REF ...]")
    assert "default text" in run.stdout
    assert "exit statuses:" in run.stdout
    for status in ("0", "1", "2", "3", "4"):
        assert f"\n  {status}  " in run.stdout
    assert run.stderr == ""


def test_an_informational_response_needs_no_source_root() -> None:
    assert invoke("--version").status == SUCCESS
    assert invoke("--help").status == SUCCESS


def test_every_option_the_contract_declares_is_accepted(root: Path) -> None:
    run = invoke(
        "--root",
        str(root),
        "--from",
        "guide.md",
        "--output",
        str(root.parent / "bundle.md"),
        "--group",
        "docs:2",
        "--check",
        "--diagnostics",
        "json",
        "guide.md",
    )
    assert run.status == SUCCESS


@pytest.mark.parametrize(
    "option",
    ["--max-files", "--max-output-bytes", "--max-nesting", "--manifest", "--watch"],
)
def test_an_option_the_contract_does_not_declare_is_refused(
    root: Path, option: str
) -> None:
    run = invoke("--root", str(root), option, "8", "guide.md")
    assert run.status == USAGE_FAILURE


def test_a_missing_source_root_is_invalid_usage() -> None:
    run = invoke("guide.md")
    assert run.status == USAGE_FAILURE
    assert run.stdout == ""
    assert "--root" in run.stderr


def test_a_run_naming_no_entry_reference_is_invalid_usage(root: Path) -> None:
    run = invoke("--root", str(root))
    assert run.status == USAGE_FAILURE
    assert run.stdout == ""


def test_a_fragment_only_reference_needs_a_referring_document(root: Path) -> None:
    run = invoke("--root", str(root), "#a-section")
    assert run.status == USAGE_FAILURE
    assert "--from" in run.stderr


def test_a_fragment_only_reference_with_a_referring_document_is_valid(
    root: Path,
) -> None:
    run = invoke("--root", str(root), "--from", "guide.md", "#a-section")
    assert run.status == INTERNAL_ERROR


@pytest.mark.parametrize("depth", ["0", "7", "9", "60"])
def test_a_grouping_depth_outside_one_through_six_is_invalid_usage(
    root: Path, depth: str
) -> None:
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--group",
        f"docs:{depth}",
        "guide.md",
    )
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_GROUP_RULE]


@pytest.mark.parametrize("depth", ["1", "6"])
def test_a_grouping_depth_at_the_boundary_is_accepted(root: Path, depth: str) -> None:
    run = invoke("--root", str(root), "--group", f"docs:{depth}", "guide.md")
    assert run.status == SUCCESS


@pytest.mark.parametrize("declaration", ["docs", "docs:", ":2", "docs:two", "a/b:2"])
def test_a_malformed_grouping_rule_is_invalid_usage(
    root: Path, declaration: str
) -> None:
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--group", declaration, "guide.md"
    )
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_GROUP_RULE]


def test_a_slug_named_by_two_grouping_rules_is_invalid_usage(root: Path) -> None:
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--group",
        "docs:2",
        "--group",
        "docs:3",
        "guide.md",
    )
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_GROUP_RULE]


def test_a_grouping_slug_naming_no_directory_is_an_input_failure(root: Path) -> None:
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--group", "notes:2", "guide.md"
    )
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_GROUP_RULE]


def test_a_source_root_naming_no_directory_is_an_input_failure(tmp_path: Path) -> None:
    run = invoke(
        "--root", str(tmp_path / "absent"), "--diagnostics", "json", "guide.md"
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [ROOT_NOT_FOUND]


def test_a_usage_failure_is_reported_before_an_input_failure(tmp_path: Path) -> None:
    run = invoke("--root", str(tmp_path / "absent"), "--group", "docs:9", "guide.md")
    assert run.status == USAGE_FAILURE


@pytest.mark.parametrize("value", ["yaml", "", "TEXT", "jsonl"])
def test_a_diagnostic_format_the_contract_does_not_declare_is_invalid_usage(
    root: Path, value: str
) -> None:
    run = invoke("--root", str(root), "--diagnostics", value, "guide.md")
    assert run.status == USAGE_FAILURE
    assert run.stdout == ""


def test_an_output_path_naming_an_input_source_is_invalid_usage(root: Path) -> None:
    run = invoke("--root", str(root), "--output", str(root / "guide.md"), "guide.md")
    assert run.status == USAGE_FAILURE
    assert "input source" in run.stderr


def test_an_output_path_naming_the_referring_document_is_invalid_usage(
    root: Path,
) -> None:
    run = invoke(
        "--root",
        str(root),
        "--from",
        "guide.md",
        "--output",
        str(root / "guide.md"),
        "#a-section",
    )
    assert run.status == USAGE_FAILURE


def test_an_output_path_naming_no_input_source_is_accepted(
    root: Path, tmp_path: Path
) -> None:
    run = invoke(
        "--root", str(root), "--output", str(tmp_path / "bundle.md"), "guide.md"
    )
    assert run.status == SUCCESS


def test_standard_output_is_the_default_output_destination(root: Path) -> None:
    assert invoke("--root", str(root), "--output", "-", "guide.md").status == (
        invoke("--root", str(root), "guide.md").status
    )


def test_a_run_the_build_cannot_carry_out_returns_the_internal_error_status(
    root: Path,
) -> None:
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md#run")
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert [one["severity"] for one in run.diagnostics()] == ["error"]
    assert [one["code"] for one in run.diagnostics()] == [UNEXPECTED_INTERNAL_ERROR]


def test_a_validation_only_run_publishes_nothing(root: Path) -> None:
    run = invoke("--root", str(root), "--check", "guide.md")
    assert run.stdout == ""


def test_a_validation_only_run_with_an_output_file_creates_no_file(
    root: Path, tmp_path: Path
) -> None:
    destination = tmp_path / "bundle.md"
    run = invoke(
        "--root", str(root), "--check", "--output", str(destination), "guide.md"
    )
    assert run.status != USAGE_FAILURE
    assert run.stdout == ""
    assert not destination.exists()


def test_a_refused_write_is_a_publication_failure() -> None:
    run = invoke("--version", stdout=Refusing())
    assert run.status == PUBLICATION_FAILURE
    assert "standard output" in run.stderr
    assert run.stderr.startswith(f"{PUBLICATION_FAILED}: ")


def test_a_failing_run_writes_its_diagnostics_as_data(root: Path) -> None:
    run = invoke("--root", str(root), "--diagnostics", "json", "--group", "x", "g.md")
    assert run.stdout == ""
    assert len(run.diagnostics()) == 1
    assert set(run.diagnostics()[0]) <= {
        "severity",
        "message",
        "code",
        "reference",
        "source",
        "remedy",
    }


def test_a_failing_run_writes_its_diagnostics_as_text(root: Path) -> None:
    run = invoke("--root", str(root), "--group", "docs:9", "guide.md")
    assert run.stdout == ""
    assert run.stderr.startswith(f"{INVALID_GROUP_RULE}: ")


def written(root: Path, name: str, text: str) -> None:
    """One source document under the allowed source root."""
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@pytest.mark.parametrize(
    ("source", "code"),
    [
        ("# Guide\n\n<div>raw</div>\n", RAW_HTML),
        ("# Guide\n\nA paragraph carrying <span>raw</span> markup.\n", RAW_HTML),
        ("# Guide\n\nSee [[page]] for the procedure.\n", UNSUPPORTED_CONSTRUCT),
        ("# Guide\n\n![[page]]\n", UNSUPPORTED_CONSTRUCT),
        ("# Guide\n\nA claim[^1] needing support.\n", UNSUPPORTED_CONSTRUCT),
        ("# Guide\n\n## Run {#custom-id}\n", UNSUPPORTED_CONSTRUCT),
    ],
)
def test_a_construct_the_profile_refuses_fails_the_run(
    root: Path, source: str, code: str
) -> None:
    written(root, "guide.md", source)
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["severity"] for one in run.diagnostics()] == ["error"]
    assert [one["code"] for one in run.diagnostics()] == [code]
    assert run.diagnostics()[0]["source"].startswith("guide.md:")


@pytest.mark.parametrize(
    "source",
    [
        "# Guide\n\nA code span naming `[[page]]` is prose about a wiki link.\n",
        "# Guide\n\nAn escaped \\[\\[page\\]\\] is literal text.\n",
        "# Guide\n\nA paragraph mentioning {#custom-id} names no section.\n",
        "# Guide\n\n```html\n<div>raw</div>\n```\n",
        "# Guide\n\n- [ ] open\n- [x] done\n\n[x]: page.md\n",
    ],
)
def test_a_source_the_profile_accepts_bundles(root: Path, source: str) -> None:
    written(root, "guide.md", source)
    assert invoke("--root", str(root), "guide.md").status == SUCCESS


def test_the_referring_document_is_read_under_the_profile(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n<div>raw</div>\n")
    run = invoke("--root", str(root), "--from", "guide.md", "#a-section")
    assert run.status == INPUT_FAILURE
    assert "guide.md" in run.stderr


def test_a_refusal_names_the_construct_and_where_it_sits(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [[page]] for the procedure.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    reported = run.diagnostics()[0]
    assert reported["reference"] == "[[page]]"
    assert reported["source"] == "guide.md:3"
    assert "wiki link" in reported["message"]


def test_an_entry_suffix_outside_the_profile_is_an_input_failure(root: Path) -> None:
    written(root, "notes.txt", "# Notes\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "notes.txt")
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["reference"] == "notes.txt"
    assert [one["code"] for one in run.diagnostics()] == [UNSUPPORTED_ENTRY_SUFFIX]


def test_an_entry_suffix_is_classified_case_insensitively(root: Path) -> None:
    written(root, "GUIDE.MARKDOWN", "# Guide\n")
    assert invoke("--root", str(root), "GUIDE.MARKDOWN").status == SUCCESS


def test_an_entry_naming_no_document_is_an_input_failure(root: Path) -> None:
    run = invoke("--root", str(root), "--diagnostics", "json", "absent.md")
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [TARGET_NOT_FOUND]


def test_an_entry_normalizing_outside_the_root_is_an_input_failure(
    root: Path,
) -> None:
    written(root.parent, "outside.md", "# Outside\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "../outside.md")
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_OUTSIDE_ROOT]


def test_a_fragment_reference_reads_the_whole_document_it_names(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\n<div>raw</div>\n")
    run = invoke("--root", str(root), "guide.md#run")
    assert run.status == INPUT_FAILURE


@pytest.mark.parametrize(
    "arguments",
    [
        (),
        ("#a-section",),
        ("--diagnostics", "yaml", "guide.md"),
        ("--watch", "guide.md"),
    ],
)
def test_a_fault_in_the_command_line_carries_the_invalid_usage_code(
    root: Path, arguments: tuple[str, ...]
) -> None:
    run = invoke("--root", str(root), "--diagnostics", "json", *arguments)
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_a_missing_source_root_carries_the_invalid_usage_code() -> None:
    run = invoke("--diagnostics", "json", "guide.md")
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_an_output_path_naming_an_input_source_carries_the_invalid_usage_code(
    root: Path,
) -> None:
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--output",
        str(root / "guide.md"),
        "guide.md",
    )
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_a_source_that_is_not_valid_utf8_is_an_input_failure(root: Path) -> None:
    (root / "guide.md").write_bytes(b"# Guide\n\nA byte that is not UTF-8: \xe9\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == INVALID_ENCODING
    assert reported["source"] == "guide.md"
    assert "UTF-8" in reported["message"]


def test_a_source_that_is_not_valid_utf8_reaches_no_generic_handler(
    root: Path,
) -> None:
    (root / "guide.md").write_bytes(b"\xff\xfe# Guide\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert "unexpected internal error" not in run.diagnostics()[0]["message"]


def test_an_unterminated_frontmatter_opener_is_an_input_failure(root: Path) -> None:
    written(root, "guide.md", "---\ntitle: Guide\n\n# Guide\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == UNTERMINATED_FRONTMATTER
    assert reported["source"] == "guide.md:1"


def test_transport_metadata_reaches_no_parse(root: Path) -> None:
    written(root, "guide.md", "﻿---\ntitle: Guide\n---\n# Guide\n\n<div>raw</div>\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert "raw HTML" in run.diagnostics()[0]["message"]


def test_a_diagnostic_below_a_stripped_block_names_the_line_of_the_file(
    root: Path,
) -> None:
    written(root, "guide.md", "---\ntitle: Guide\n---\n# Guide\n\nSee [[page]] now.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.diagnostics()[0]["source"] == "guide.md:6"


def test_a_diagnostic_below_a_mark_alone_names_the_line_of_the_file(
    root: Path,
) -> None:
    written(root, "guide.md", "﻿# Guide\n\nSee [[page]] now.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.diagnostics()[0]["source"] == "guide.md:3"


@pytest.mark.parametrize(
    ("source", "at"),
    [
        (" ---\ntitle: Guide\n---\n\nSee [[page]] now.\n", 5),
        ("--- \ntitle: Guide\n---\n\nSee [[page]] now.\n", 5),
        ('+++\ntitle = "Guide"\n+++\n\nSee [[page]] now.\n', 5),
        ('{\n  "title": "Guide"\n}\n\nSee [[page]] now.\n', 5),
        ("***\ntitle: Guide\n---\n\nSee [[page]] now.\n", 5),
        ("\n---\ntitle: Guide\n---\n\nSee [[page]] now.\n", 6),
    ],
)
def test_a_first_line_that_is_no_opener_shifts_no_coordinate(
    root: Path, source: str, at: int
) -> None:
    written(root, "guide.md", source)
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.diagnostics()[0]["source"] == f"guide.md:{at}"


def test_a_crlf_delimited_block_is_stripped_by_the_command(root: Path) -> None:
    (root / "guide.md").write_bytes(b"---\r\ntitle: Guide\r\n---\r\nSee [[page]].\r\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["source"] == "guide.md:4"


def test_a_referring_document_is_stripped_too(root: Path) -> None:
    written(root, "guide.md", "---\ntitle: Guide\n---\n# Guide\n\n<div>raw</div>\n")
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--from", "guide.md", "#run"
    )
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["source"] == "guide.md:6"


def test_a_stripped_source_the_profile_accepts_bundles(root: Path) -> None:
    written(root, "guide.md", "﻿---\ntitle: Guide\n...\n# Guide\n")
    assert invoke("--root", str(root), "guide.md").status == SUCCESS


def test_a_crlf_source_is_read_without_newline_translation(root: Path) -> None:
    (root / "guide.md").write_bytes(b"---\r\ntitle: Guide\r\n---\r\n# Guide\r\n")
    read = read_entry(root, "guide.md", "guide.md")
    assert read.text == "# Guide\r\n"
    assert read.first_line == 4


def test_a_successful_run_publishes_the_bundle_and_nothing_else(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == SUCCESS
    assert run.stderr == ""
    assert run.stdout == (
        "This bundle was built for [guide](#guide); "
        "everything else is material it references.\n"
        "\n# guide\n\n## Run\n\nDo it.\n"
    )


def test_two_sources_sharing_a_basename_stay_distinguishable(root: Path) -> None:
    written(root, "docs/note.md", "# Note\n\nUnder docs.\n")
    written(root, "notes/note.md", "# Note\n\nUnder notes.\n")
    run = invoke("--root", str(root), "docs/note.md", "notes/note.md")
    assert run.status == SUCCESS
    assert "# docs/note\n" in run.stdout
    assert "# notes/note\n" in run.stdout


def test_groups_are_ordered_by_root_relative_path(root: Path) -> None:
    written(root, "docs/note.md", "# Note\n")
    written(root, "guide.md", "# Guide\n")
    ordered = invoke("--root", str(root), "guide.md", "docs/note.md").stdout
    assert ordered.index("# docs/note\n") < ordered.index("# guide\n")


def test_one_document_named_twice_is_one_group(root: Path) -> None:
    written(root, "guide.md", "# Guide\n")
    run = invoke("--root", str(root), "guide.md", "sub/../guide.md")
    assert run.stdout.count("# guide\n") == 1


def test_two_paths_differing_only_by_suffix_are_an_ambiguous_file_group(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n")
    written(root, "guide.markdown", "# Guide\n")
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "guide.md", "guide.markdown"
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [AMBIGUOUS_FILE_GROUP]


def test_a_heading_beyond_the_sixth_level_fails_and_publishes_nothing(
    root: Path,
) -> None:
    written(root, "guide.md", "# Another Name\n\n###### Deep\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [HEADING_DEPTH_OVERFLOW]


def test_a_fragment_reference_names_content_this_build_cannot_select(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md#run")
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [UNEXPECTED_INTERNAL_ERROR]


def test_an_empty_fragment_is_a_whole_document_reference(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    assert invoke("--root", str(root), "guide.md#").stdout == (
        invoke("--root", str(root), "guide.md").stdout
    )


def test_a_referring_document_contributes_no_group(root: Path) -> None:
    written(root, "guide.md", "# Guide\n")
    written(root, "docs/note.md", "# Note\n")
    run = invoke("--root", str(root), "--from", "guide.md", "docs/note.md")
    assert run.status == SUCCESS
    assert "# guide\n" not in run.stdout
    assert "# docs/note\n" in run.stdout


def test_a_named_output_file_carries_the_bundle(root: Path, tmp_path: Path) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    destination = tmp_path / "bundle.md"
    run = invoke("--root", str(root), "--output", str(destination), "guide.md")
    assert run.status == SUCCESS
    assert run.stdout == ""
    assert destination.read_text() == (
        "This bundle was built for [guide](#guide); "
        "everything else is material it references.\n\n# guide\n\nBody.\n"
    )


def test_a_named_output_file_is_published_through_one_rename(
    root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(root, "guide.md", "# Guide\n")
    published = tmp_path / "published"
    published.mkdir()
    destination = published / "bundle.md"
    renamed: list[tuple[str, str]] = []
    replace = os.replace

    def record(source: Any, target: Any) -> None:
        renamed.append((str(source), str(target)))
        replace(source, target)

    monkeypatch.setattr(os, "replace", record)
    assert invoke("--root", str(root), "-o", str(destination), "guide.md").status == (
        SUCCESS
    )
    assert [target for _, target in renamed] == [str(destination)]
    assert [path.name for path in published.iterdir()] == ["bundle.md"]


def test_a_failed_run_leaves_the_output_file_alone(root: Path, tmp_path: Path) -> None:
    written(root, "guide.md", "# Guide\n\n<div>raw</div>\n")
    destination = tmp_path / "bundle.md"
    destination.write_text("earlier bytes\n")
    assert invoke("--root", str(root), "-o", str(destination), "guide.md").status == (
        INPUT_FAILURE
    )
    assert destination.read_text() == "earlier bytes\n"


def test_an_output_path_the_run_cannot_write_is_a_publication_failure(
    root: Path, tmp_path: Path
) -> None:
    written(root, "guide.md", "# Guide\n")
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "-o",
        str(tmp_path / "absent" / "bundle.md"),
        "guide.md",
    )
    assert run.status == PUBLICATION_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [PUBLICATION_FAILED]


def test_a_validation_only_run_bundles_and_publishes_nothing(
    root: Path, tmp_path: Path
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    destination = tmp_path / "bundle.md"
    run = invoke("--root", str(root), "--check", "-o", str(destination), "guide.md")
    assert run.status == SUCCESS
    assert run.stdout == ""
    assert not destination.exists()


def test_a_validation_only_run_still_reports_a_bundle_it_cannot_build(
    root: Path,
) -> None:
    written(root, "guide.md", "# Another Name\n\n###### Deep\n")
    run = invoke("--root", str(root), "--check", "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [HEADING_DEPTH_OVERFLOW]
