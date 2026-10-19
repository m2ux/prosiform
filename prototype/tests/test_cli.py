"""Assert the command's grammar, its stream split and its exit statuses.

The corpus is where a contract clause is declared, and these are the cases
a fixture cannot reach: a response whose text belongs to this build rather
than to the contract, a write the stream refuses, and the status a request
this build cannot carry out returns. Each case names a run, its status,
and what each of the two streams carried.
"""

import json
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import IO, Any

import pytest
from prosiform import PROFILE
from prosiform.cli import (
    INPUT_FAILURE,
    INTERNAL_ERROR,
    INVALID_GROUP_RULE,
    PUBLICATION_FAILURE,
    SOURCE_OUTSIDE_ROOT,
    SUCCESS,
    TARGET_NOT_FOUND,
    USAGE_FAILURE,
    main,
)


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
    assert run.stdout == f"prosiform 0.0.0 ({PROFILE})\n"
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
    assert run.status == INTERNAL_ERROR


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
    assert run.status == INTERNAL_ERROR


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
    run = invoke("--root", str(tmp_path / "absent"), "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""


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
    assert run.status == INTERNAL_ERROR


def test_standard_output_is_the_default_output_destination(root: Path) -> None:
    assert invoke("--root", str(root), "--output", "-", "guide.md").status == (
        invoke("--root", str(root), "guide.md").status
    )


def test_a_run_the_build_cannot_carry_out_returns_the_internal_error_status(
    root: Path,
) -> None:
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert [one["severity"] for one in run.diagnostics()] == ["error"]
    assert "code" not in run.diagnostics()[0]


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
    "source",
    [
        "# Guide\n\n<div>raw</div>\n",
        "# Guide\n\nA paragraph carrying <span>raw</span> markup.\n",
        "# Guide\n\nSee [[page]] for the procedure.\n",
        "# Guide\n\n![[page]]\n",
        "# Guide\n\nA claim[^1] needing support.\n",
        "# Guide\n\n## Run {#custom-id}\n",
    ],
)
def test_a_construct_the_profile_refuses_fails_the_run(root: Path, source: str) -> None:
    written(root, "guide.md", source)
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["severity"] for one in run.diagnostics()] == ["error"]
    assert "code" not in run.diagnostics()[0]
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
def test_a_source_the_profile_accepts_reaches_the_absent_stage(
    root: Path, source: str
) -> None:
    written(root, "guide.md", source)
    assert invoke("--root", str(root), "guide.md").status == INTERNAL_ERROR


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


def test_an_entry_suffix_is_classified_case_insensitively(root: Path) -> None:
    written(root, "GUIDE.MARKDOWN", "# Guide\n")
    assert invoke("--root", str(root), "GUIDE.MARKDOWN").status == INTERNAL_ERROR


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
