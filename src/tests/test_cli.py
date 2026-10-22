"""Assert the command's grammar, its stream split and its exit statuses.

The corpus is where a contract clause is declared, and these are the cases
a fixture cannot reach: a response whose text belongs to this build rather
than to the contract, a write the stream refuses, and the status a request
this build cannot carry out returns. Each case names a run, its status,
and what each of the two streams carried.

A source changing while the run reads it is reached from both sides. The
corpus states the outcome, over a run asked for the `source-changed`
fault, and the recheck is held here on the terms a fixture cannot name:
the comparison itself, over a tree written between the two reads, and a
whole run whose source is written as the run reads it, which publishes
nothing to either stream or to a named file. The faults the contract
declares are held here too, each on the status and the diagnostic it
returns.
"""

import json
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from importlib.metadata import version
from io import StringIO
from pathlib import Path
from typing import IO, Any

import pytest

from prosiform import PROFILE
from prosiform.access import read_source
from prosiform.bundle import (
    AMBIGUOUS_FILE_GROUP,
    HEADING_DEPTH_OVERFLOW,
    Group,
    assemble,
)
from prosiform.bundle import (
    CODES as BUNDLE_CODES,
)
from prosiform.candidate import (
    CODES as CANDIDATE_CODES,
)
from prosiform.candidate import (
    UNSAFE_BUNDLE_BOUNDARY,
)
from prosiform.cli import (
    CODES,
    EMPTY_GROUP_RULE,
    ENTRY_DESTINATION,
    GENERATED_INPUT,
    INPUT_FAILURE,
    INTERNAL_ERROR,
    INVALID_ENCODING,
    INVALID_GROUP_RULE,
    INVALID_USAGE,
    PUBLICATION_FAILED,
    PUBLICATION_FAILURE,
    RESOURCE_PORTABILITY,
    ROOT_NOT_FOUND,
    SOURCE_CHANGED,
    SOURCE_OUTSIDE_ROOT,
    SOURCE_SYMLINK,
    SUCCESS,
    TARGET_NOT_FOUND,
    UNEXPECTED_INTERNAL_ERROR,
    UNSUPPORTED_ENTRY_SUFFIX,
    USAGE_FAILURE,
    Failure,
    canonical,
    main,
    read_document,
    recheck,
)
from prosiform.closure import resolve
from prosiform.limits import (
    CODES as LIMITS_CODES,
)
from prosiform.limits import (
    FILES,
    NESTING,
    RESOURCE_LIMIT,
)
from prosiform.profile import (
    CODES as PROFILE_CODES,
)
from prosiform.profile import (
    HEADROOM,
    PARSER_REFERENCE_LIMIT,
    RAW_HTML,
    UNSUPPORTED_CONSTRUCT,
)
from prosiform.source import (
    CODES as SOURCE_CODES,
)
from prosiform.source import (
    NESTED_SECTION_TARGET,
    UNTERMINATED_FRONTMATTER,
    Capture,
    hashed,
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
    assert run.stdout == f"prosiform {version('prosiform')} ({PROFILE})\n"
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


def test_the_codes_response_names_every_code_the_build_can_emit() -> None:
    run = invoke("--codes")
    assert run.status == SUCCESS
    assert run.stdout == "".join(f"{code}\n" for code in sorted(CODES))
    assert run.stderr == ""


def test_the_codes_reported_are_the_codes_the_build_declares() -> None:
    declared = {
        GENERATED_INPUT,
        INVALID_ENCODING,
        INVALID_GROUP_RULE,
        INVALID_USAGE,
        PUBLICATION_FAILED,
        ROOT_NOT_FOUND,
        SOURCE_CHANGED,
        SOURCE_OUTSIDE_ROOT,
        SOURCE_SYMLINK,
        TARGET_NOT_FOUND,
        UNEXPECTED_INTERNAL_ERROR,
        UNSUPPORTED_ENTRY_SUFFIX,
        EMPTY_GROUP_RULE,
        ENTRY_DESTINATION,
        RESOURCE_PORTABILITY,
    }
    for published in (
        BUNDLE_CODES,
        CANDIDATE_CODES,
        LIMITS_CODES,
        PROFILE_CODES,
        SOURCE_CODES,
    ):
        declared.update(published)
    assert CODES == tuple(sorted(declared))


def test_an_informational_response_needs_no_source_root() -> None:
    assert invoke("--version").status == SUCCESS
    assert invoke("--help").status == SUCCESS
    assert invoke("--codes").status == SUCCESS


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


@pytest.mark.parametrize("option", ["--manifest", "--watch", "--cache"])
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


def test_a_fragment_only_reference_selects_from_the_referring_document(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    assert invoke("--root", str(root), "--from", "guide.md", "#run").stdout == (
        invoke("--root", str(root), "guide.md#run").stdout
    )


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


def test_a_grouping_rule_the_closure_leaves_idle_is_reported_as_arranging_nothing(
    root: Path,
) -> None:
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--group", "docs:2", "guide.md"
    )
    assert run.status == SUCCESS
    assert [one["code"] for one in run.diagnostics()] == [
        EMPTY_GROUP_RULE,
        ENTRY_DESTINATION,
    ]
    warned = run.diagnostics()[0]
    assert warned["severity"] == "warning"
    assert "'docs'" in warned["message"]


def test_a_grouping_rule_the_closure_carries_a_document_under_arranges_it(
    root: Path,
) -> None:
    written(root, "docs/note.md", "# Note\n\n## Run\n\nDo it.\n")
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--group",
        "docs:2",
        "docs/note.md",
    )
    assert run.status == SUCCESS
    assert EMPTY_GROUP_RULE not in [one["code"] for one in run.diagnostics()]


def test_each_idle_grouping_rule_is_reported_and_an_arranging_one_is_not(
    root: Path,
) -> None:
    written(root, "notes/kept.md", "# Kept\n\n## Run\n\nDo it.\n")
    written(root, "other/unused.md", "# Unused\n")
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--group",
        "docs:2",
        "--group",
        "notes:2",
        "--group",
        "other:2",
        "notes/kept.md",
    )
    assert run.status == SUCCESS
    warned = [
        one["message"] for one in run.diagnostics() if one["code"] == EMPTY_GROUP_RULE
    ]
    assert len(warned) == 2
    assert "'docs'" in warned[0]
    assert "'other'" in warned[1]


def test_an_entry_naming_a_member_of_one_heading_opens_on_its_subsection(
    root: Path,
) -> None:
    written(root, "notes/bare.md", "# Bare\n")
    run = invoke("--root", str(root), "--group", "notes:2", "notes/bare.md")
    assert run.status == SUCCESS
    assert run.stdout.startswith("This bundle was built for [Bare](#bare);")


def test_an_entry_naming_the_absorbed_title_of_a_member_opens_on_its_subsection(
    root: Path,
) -> None:
    written(root, "notes/second.md", "# Second\n\n## Outcomes\n\nText.\n")
    run = invoke("--root", str(root), "--group", "notes:2", "notes/second.md#second")
    assert run.status == SUCCESS
    assert run.stdout.startswith("This bundle was built for [Second](#second);")


def test_a_reference_into_a_member_of_one_heading_reaches_its_subsection(
    root: Path,
) -> None:
    written(root, "notes/bare.md", "# Bare\n")
    written(root, "guide.md", "# Guide\n\nSee [Bare](notes/bare.md).\n")
    run = invoke("--root", str(root), "--group", "notes:2", "guide.md")
    assert run.status == SUCCESS
    assert "See [Bare](#bare)." in run.stdout


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
        "#guide",
    )
    assert run.status == USAGE_FAILURE


def test_an_output_path_naming_a_dependency_source_is_invalid_usage(
    root: Path,
) -> None:
    (root / "guide.md").write_text("# Guide\n\nIt needs [the note](docs/note.md).\n")
    note = root / "docs" / "note.md"
    run = invoke("--root", str(root), "--output", str(note), "guide.md")
    assert run.status == USAGE_FAILURE
    assert "input source" in run.stderr
    assert note.read_text() == "# Note\n"


def test_a_source_reached_through_a_link_is_no_identity_the_output_check_holds(
    root: Path, tmp_path: Path
) -> None:
    outside = tmp_path.parent / "outside.md"
    outside.write_text("# Outside\n")
    (root / "alias.md").symlink_to(outside)
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--output",
        str(outside),
        "alias.md",
    )
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_SYMLINK]


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


def test_an_entry_reference_stands_at_the_head_of_its_own_chain(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac gone](missing.md).\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md#nowhere")
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["chain"] == ["guide.md#nowhere"]


def test_a_failure_names_every_reference_that_reached_it(root: Path) -> None:
    written(root, "entry.md", "# Entry\n\nSee [notes](docs/notes.md#detail).\n")
    written(
        root,
        "docs/notes.md",
        "# Notes\n\n## Detail\n\nSee [other](other.md#nowhere).\n",
    )
    written(root, "docs/other.md", "# Other\n\n## Here\n\nContent.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "entry.md")
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [TARGET_NOT_FOUND]
    reported = run.diagnostics()[0]
    assert reported["chain"] == [
        "entry.md",
        "docs/notes.md#detail",
        "docs/other.md#nowhere",
    ]
    assert reported["reference"] == "other.md#nowhere"
    assert reported["resolved"] == "docs/other.md"
    assert reported["source"] == "docs/notes.md:5"


def test_a_document_a_dependency_reached_reports_the_route_to_it(root: Path) -> None:
    written(root, "entry.md", "# Entry\n\nSee [notes](docs/notes.md).\n")
    written(root, "docs/notes.md", "# Notes\n\n<div>raw</div>\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "entry.md")
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [RAW_HTML]
    assert run.diagnostics()[0]["chain"] == ["entry.md", "docs/notes.md"]


def test_a_usage_failure_reaching_no_document_carries_no_chain(root: Path) -> None:
    run = invoke("--root", str(root), "--diagnostics", "json", "--group", "x", "g.md")
    assert run.status == USAGE_FAILURE
    assert "chain" not in run.diagnostics()[0]


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


@pytest.mark.parametrize(
    "reference", ["../outside.md", "/guide.md", "C:/guide.md", "//host/guide.md"]
)
def test_an_entry_the_root_cannot_contain_is_an_input_failure(
    root: Path, reference: str
) -> None:
    written(root.parent, "outside.md", "# Outside\n")
    run = invoke("--root", str(root), "--diagnostics", "json", reference)
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
    written(
        root,
        "guide.md",
        "---\ntitle: Guide\n---\n# Guide\n\n## Run\n\n<div>raw</div>\n",
    )
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--from", "guide.md", "#run"
    )
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["source"] == "guide.md:8"


def test_a_stripped_source_the_profile_accepts_bundles(root: Path) -> None:
    written(root, "guide.md", "﻿---\ntitle: Guide\n...\n# Guide\n")
    assert invoke("--root", str(root), "guide.md").status == SUCCESS


def test_a_crlf_source_is_read_without_newline_translation(root: Path) -> None:
    (root / "guide.md").write_bytes(b"---\r\ntitle: Guide\r\n---\r\n# Guide\r\n")
    read = read_document(root, resolve("guide.md")).source
    assert read.text == "# Guide\r\n"
    assert read.first_line == 4


def test_a_successful_run_publishes_the_bundle_and_nothing_else(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == SUCCESS
    assert [one["code"] for one in run.diagnostics()] == [ENTRY_DESTINATION]
    assert run.stdout == (
        "This bundle was built for [Guide](#guide); "
        "everything else is material it references.\n"
        "\n# Guide\n\n## Run\n\nDo it.\n"
    )


def test_a_successful_run_reports_each_entry_reference_and_its_destination(
    root: Path,
) -> None:
    written(root, "notes.md", "# Notes\n\n### Step\n\nFirst.\n")
    written(root, "rules.md", "# Rules\n\n### Step\n\nSecond.\n")
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "notes.md#step",
        "rules.md#step",
    )
    assert run.status == SUCCESS
    assert [
        (one["severity"], one["code"], one["reference"], one["resolved"])
        for one in run.diagnostics()
    ] == [
        ("warning", ENTRY_DESTINATION, "Step", "step"),
        ("warning", ENTRY_DESTINATION, "Step", "step-1"),
    ]


def test_an_entry_destination_is_reported_in_the_format_the_run_declares(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    run = invoke("--root", str(root), "--diagnostics", "text", "guide.md")
    assert run.status == SUCCESS
    assert run.stderr == (
        f"{ENTRY_DESTINATION}: the entry reference 'Guide' resolves to the "
        "destination 'guide', which the bundle's entry line links it to\n"
        "  reference: Guide\n"
        "  resolved: guide\n"
    )


def test_a_validation_only_run_reports_the_destinations_it_resolved(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    run = invoke("--root", str(root), "--check", "--diagnostics", "json", "guide.md")
    assert run.status == SUCCESS
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [ENTRY_DESTINATION]


def test_a_run_that_cannot_publish_reports_no_entry_destination(
    root: Path, tmp_path: Path
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
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


def test_two_sources_sharing_a_basename_stay_distinguishable(root: Path) -> None:
    written(root, "docs/note.md", "# Note\n\nUnder docs.\n")
    written(root, "notes/note.md", "# Note\n\nUnder notes.\n")
    run = invoke("--root", str(root), "docs/note.md", "notes/note.md")
    assert run.status == SUCCESS
    assert "# Docs/Note\n" in run.stdout
    assert "# Notes/Note\n" in run.stdout


def test_groups_are_ordered_by_root_relative_path(root: Path) -> None:
    written(root, "docs/note.md", "# Note\n")
    written(root, "guide.md", "# Guide\n")
    ordered = invoke("--root", str(root), "guide.md", "docs/note.md").stdout
    assert ordered.index("# Docs/Note\n") < ordered.index("# Guide\n")


def test_one_document_named_twice_is_one_group(root: Path) -> None:
    written(root, "guide.md", "# Guide\n")
    run = invoke("--root", str(root), "guide.md", "sub/../guide.md")
    assert run.stdout.count("# Guide\n") == 1


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


def test_a_structural_ancestor_beyond_the_sixth_level_fails_by_its_own_name(
    root: Path,
) -> None:
    written(
        root,
        "references/alpha.md",
        "# Conventions\n\n## Standards\n\n### Formatting\n\n#### Headings\n\n"
        "##### Levels\n\n###### The Sixth\n\nThe note the sixth level carries.\n",
    )
    written(
        root,
        "references/beta.md",
        "# Conventions\n\n## Standards\n\nWhat this document holds to.\n",
    )
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--group",
        "references:1",
        "references/alpha.md#the-sixth",
        "references/beta.md#standards",
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == HEADING_DEPTH_OVERFLOW
    assert "'Levels' at level 7" in reported["message"]


def test_a_fragment_selects_the_section_its_heading_roots(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\nDo it.\n\n## Stop\n\nStop it.\n")
    run = invoke("--root", str(root), "guide.md#run")
    assert run.status == SUCCESS
    assert run.stdout == (
        "This bundle was built for [Run](#run); everything else is material it "
        "references.\n\n# Guide\n\n### Run\n\nDo it.\n"
    )


def test_a_fragment_naming_a_container_nested_heading_is_refused(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n> ## Nested\n>\n> Inside.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md#nested")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [NESTED_SECTION_TARGET]
    assert [one["reference"] for one in run.diagnostics()] == ["guide.md#nested"]


def test_a_fragment_naming_no_heading_is_a_missing_target(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md#stop")
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [TARGET_NOT_FOUND]


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
    assert "# Guide\n" not in run.stdout
    assert "# Docs/Note\n" in run.stdout


def test_a_named_output_file_carries_the_bundle(root: Path, tmp_path: Path) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    destination = tmp_path / "bundle.md"
    run = invoke("--root", str(root), "--output", str(destination), "guide.md")
    assert run.status == SUCCESS
    assert run.stdout == ""
    assert destination.read_text() == (
        "This bundle was built for [Guide](#guide); "
        "everything else is material it references.\n\n# Guide\n\nBody.\n"
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


def test_a_marked_resource_is_emitted_with_its_mark(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [¬ the diagram](plan.png).\n")
    (root / "plan.png").write_text("Never opened.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "[¬ the diagram](plan.png)" in run.stdout


def test_a_marked_image_is_emitted_with_its_mark(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee ![\u00ac the architecture](plan.png).\n")
    (root / "plan.png").write_text("Never opened.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "![¬ the architecture](plan.png)" in run.stdout


def test_an_image_naming_a_markdown_document_carries_no_document(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee ![the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nThe rules.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "![the rules](rules.md)" in run.stdout
    assert "The rules." not in run.stdout


def test_an_image_naming_a_markdown_document_warns_once_on_portability(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee ![the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nThe rules.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == SUCCESS
    codes = [one["code"] for one in run.diagnostics()]
    assert codes.count(RESOURCE_PORTABILITY) == 1


def test_a_bundle_naming_no_resource_does_not_warn_on_portability(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the spec](https://e.test/s.pdf).\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == SUCCESS
    assert RESOURCE_PORTABILITY not in [one["code"] for one in run.diagnostics()]


def test_an_unmarked_image_is_emitted_as_authored(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee ![the architecture](plan.png).\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "![the architecture](plan.png)" in run.stdout


def test_a_marked_reference_carrying_a_scheme_is_emitted_as_authored(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [¬ the spec](https://e.test/s.md).\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "[¬ the spec](https://e.test/s.md)" in run.stdout


def test_an_unmarked_resource_is_emitted_as_authored(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the spec](https://e.test/s.md).\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "[the spec](https://e.test/s.md)" in run.stdout


def test_a_reference_under_the_root_is_bundled_and_rewritten(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "[the rules](#rules)" in run.stdout
    assert "Every rule." in run.stdout


def test_a_reference_to_a_section_under_the_root_carries_that_section(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the step](process.md#step).\n")
    written(root, "process.md", "# Process\n\n## Draft\n\nNo.\n\n## Step\n\nYes.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "[the step](#step)" in run.stdout
    assert "Yes." in run.stdout
    assert "No." not in run.stdout


def test_a_reference_outside_the_root_is_emitted_as_authored(tmp_path: Path) -> None:
    allowed = tmp_path / "source"
    allowed.mkdir()
    (tmp_path / "rules.md").write_text("# Rules\n\n<div>raw</div>\n")
    (allowed / "guide.md").write_text("# Guide\n\nSee [the rules](../rules.md).\n")
    run = invoke("--root", str(allowed), "guide.md")
    assert run.status == SUCCESS
    assert "[the rules](../rules.md)" in run.stdout
    assert "raw" not in run.stdout


def test_a_root_relative_reference_inside_a_source_is_emitted_as_authored(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the rules](/rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "[the rules](/rules.md)" in run.stdout
    assert "Every rule." not in run.stdout


def test_a_drive_path_inside_a_source_is_emitted_as_authored(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the rules](C:/rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "[the rules](C:/rules.md)" in run.stdout
    assert "Every rule." not in run.stdout


def test_a_mark_on_a_reference_outside_the_root_changes_nothing(
    tmp_path: Path,
) -> None:
    allowed = tmp_path / "source"
    allowed.mkdir()
    (tmp_path / "rules.md").write_text("# Rules\n\nEvery rule.\n")
    (allowed / "guide.md").write_text(
        "# Guide\n\nSee [\u00ac the rules](../rules.md).\n"
    )
    run = invoke("--root", str(allowed), "guide.md")
    assert run.status == SUCCESS
    assert "[\u00ac the rules](../rules.md)" in run.stdout


def test_a_reference_under_the_root_naming_no_document_publishes_nothing(
    root: Path,
) -> None:
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    written(
        root,
        "guide.md",
        "# Guide\n\nSee [the rules](rules.md) and [the steps](procedure.md).\n",
    )
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["code"] == TARGET_NOT_FOUND
    assert run.diagnostics()[0]["reference"] == "procedure.md"
    assert run.stdout == ""


def test_a_reference_under_the_root_naming_no_heading_publishes_nothing(
    root: Path,
) -> None:
    written(root, "procedure.md", "# Procedure\n\n## Steps\n\nCarry each out.\n")
    written(root, "guide.md", "# Guide\n\nSee [the review](procedure.md#review).\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["code"] == TARGET_NOT_FOUND
    assert run.diagnostics()[0]["resolved"] == "procedure.md"
    assert run.stdout == ""


def test_a_marked_reference_under_the_root_is_not_compiled(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule the procedure requires.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "# Rules" not in run.stdout
    assert "Every rule the procedure requires." not in run.stdout


def test_a_deferred_link_carries_the_mark_its_author_wrote(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "See [\u00ac the rules](rules.md)." in run.stdout


@pytest.mark.parametrize(
    "written_as",
    ["[\u00acthe rules](rules.md)", "[\u00ac\tthe rules](rules.md)"],
)
def test_the_bytes_between_the_mark_and_the_text_are_carried(
    root: Path, written_as: str
) -> None:
    written(root, "guide.md", f"# Guide\n\nSee {written_as}.\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert written_as in run.stdout


def test_a_deferral_stands_where_another_reference_carried_its_target(
    root: Path,
) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\nSee [\u00ac the rules](rules.md) and [the house](house.md).\n",
    )
    written(root, "house.md", "# House\n\nIt requires [the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "# Rules" in run.stdout
    assert "See [\u00ac the rules](rules.md)" in run.stdout
    assert "It requires [the rules](#rules)" in run.stdout


def test_a_deferred_fragment_of_its_own_document_is_not_compiled(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSee [\u00ac B](#beta).\n\n## Beta\n\nBody.\n",
    )
    run = invoke("--root", str(root), "guide.md#alpha")
    assert run.status == SUCCESS
    assert "See [\u00ac B](guide.md#beta)." in run.stdout
    assert "Body." not in run.stdout


def test_a_deferred_reference_naming_no_document_fails(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md).\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [TARGET_NOT_FOUND]
    assert run.stdout == ""


def test_a_deferred_reference_naming_no_heading_fails(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md#absent).\n")
    written(root, "rules.md", "# Rules\n\n## Here\n\nEvery rule.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == TARGET_NOT_FOUND
    assert reported["reference"] == "rules.md#absent"
    assert reported["resolved"] == "rules.md"
    assert reported["chain"] == ["guide.md", "rules.md#absent"]
    assert run.stdout == ""


def test_a_deferred_reference_leaving_the_root_is_not_confirmed(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](../outside.md).\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "See [\u00ac the rules](../outside.md)." in run.stdout


def test_a_deferred_destination_is_the_target_path_from_the_root(root: Path) -> None:
    written(
        root,
        "topic/guide.md",
        "# Guide\n\nSee [\u00ac the rules](../shared/rules.md#here).\n",
    )
    written(root, "shared/rules.md", "# Rules\n\n## Here\n\nEvery rule.\n")
    run = invoke("--root", str(root), "topic/guide.md")
    assert run.status == SUCCESS
    assert "See [\u00ac the rules](shared/rules.md#here)." in run.stdout


def test_a_document_only_a_deferral_names_contributes_nothing(root: Path) -> None:
    written(
        root,
        "topic/guide.md",
        "# Guide\n\nSee [\u00ac the rules](../shared/rules.md).\n",
    )
    written(root, "shared/rules.md", "# Rules\n\nEvery rule the guide defers.\n")
    run = invoke("--root", str(root), "topic/guide.md")
    assert run.status == SUCCESS
    assert "# shared/rules" not in run.stdout
    assert "Every rule the guide defers." not in run.stdout


def test_a_heading_a_container_carries_confirms_a_deferral(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md#inner).\n")
    written(root, "rules.md", "# Rules\n\n- item\n\n  ## Inner\n\n  Every rule.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "See [\u00ac the rules](rules.md#inner)." in run.stdout


def test_a_link_to_the_section_carrying_it_resolves_to_that_section(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSee [A](guide.md#alpha).\n")
    run = invoke("--root", str(root), "guide.md#alpha")
    assert run.status == SUCCESS
    assert "See [A](#alpha)." in run.stdout
    assert run.stdout.count("### Alpha") == 1


def test_identity_is_compared_after_the_path_and_the_fragment_resolve(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSee [A](./%67uide.md#alpha).\n")
    run = invoke("--root", str(root), "guide.md#alpha")
    assert run.status == SUCCESS
    assert "See [A](#alpha)." in run.stdout


def test_a_preamble_link_to_its_own_document_resolves_to_that_document(
    root: Path,
) -> None:
    written(root, "guide.md", "See [the guide](guide.md).\n\n## Alpha\n\nBody.\n")
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "See [the guide](#guide)." in run.stdout


def test_a_section_link_to_its_whole_document_is_an_ancestor_inclusion(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSee [it](guide.md).\n")
    assert invoke("--root", str(root), "guide.md#alpha").status == SUCCESS


def test_a_link_to_another_section_of_one_file_is_no_self_reference(
    root: Path,
) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSee [B](guide.md#beta).\n\n## Beta\n\nBody.\n",
    )
    assert invoke("--root", str(root), "guide.md#alpha").status == SUCCESS


def test_classification_is_the_same_before_and_after_consolidation(
    root: Path,
) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nBody.\n\n### Detail\n\nSee [A](guide.md#alpha).\n",
    )
    child = invoke("--root", str(root), "guide.md#detail")
    consolidated = invoke("--root", str(root), "guide.md#alpha")
    assert child.status == SUCCESS
    assert consolidated.status == SUCCESS
    assert child.stdout.partition("\n\n")[2] == consolidated.stdout.partition("\n\n")[2]


def test_a_self_reference_resolves_the_same_after_consolidation(
    root: Path,
) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\n### Detail\n\nSee [D](guide.md#detail).\n",
    )
    run = invoke("--root", str(root), "guide.md")
    assert run.status == SUCCESS
    assert "See [D](#detail)." in run.stdout


def chained(root: Path) -> None:
    """A root holding a three-document chain of marked dependencies."""
    written(root, "alpha.md", "# Alpha\n\nSee [b](beta.md).\n")
    written(root, "beta.md", "# Beta\n\nSee [g](gamma.md).\n")
    written(root, "gamma.md", "# Gamma\n\nThe end.\n")


@pytest.mark.parametrize(
    ("option", "value"),
    [
        ("--max-files", "2"),
        ("--max-file-bytes", "16"),
        ("--max-input-bytes", "60"),
        ("--max-output-bytes", "64"),
        ("--max-targets", "2"),
        ("--max-links", "1"),
        ("--max-expansion-depth", "1"),
    ],
)
def test_a_crossed_budget_fails_the_run_and_names_the_option(
    root: Path, option: str, value: str
) -> None:
    chained(root)
    run = invoke(
        "--root", str(root), "--diagnostics", "json", option, value, "alpha.md"
    )
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RESOURCE_LIMIT
    assert option in reported["message"]
    assert run.stdout == ""


def test_a_crossed_nesting_budget_fails_rather_than_reinterpreting_the_source(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n" + "> " * 12 + "The bottom.\n")
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--max-nesting", "3", "guide.md"
    )
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["code"] == RESOURCE_LIMIT


def test_a_parsing_safety_budget_an_unselected_construct_crosses_names_the_source(
    root: Path,
) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSelected.\n\n## Beta\n\n" + "> " * 12 + "Deep.\n",
    )
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--max-nesting",
        "3",
        "guide.md#alpha",
    )
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RESOURCE_LIMIT
    assert reported["source"] == "guide.md"
    assert reported["reference"] == "guide.md"
    assert reported["chain"] == ["guide.md#alpha"]
    assert "cannot be safely indexed" in reported["message"]


def test_a_source_byte_budget_is_an_indexing_failure_too(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSelected.\n")
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--max-file-bytes",
        "8",
        "guide.md#alpha",
    )
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RESOURCE_LIMIT
    assert reported["source"] == "guide.md"
    assert "cannot be safely indexed" in reported["message"]


def test_a_run_wide_budget_names_no_single_source(root: Path) -> None:
    chained(root)
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--max-files", "2", "alpha.md"
    )
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RESOURCE_LIMIT
    assert "source" not in reported
    assert "cannot be safely indexed" not in reported["message"]


def scoped(root: Path) -> None:
    """A document whose unselected section carries every defect at once."""
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSee [gamma](other.md#gamma).\n\n"
        "## Beta\n\nSee [¬ gone](missing.md) and [¬ here](guide.md#beta).\n\n"
        "<div>raw</div>\n",
    )
    written(
        root,
        "other.md",
        "# Other\n\n## Gamma\n\nCited.\n\n## Delta\n\n<div>raw</div>\n",
    )


def test_an_unselected_broken_link_does_not_fail_the_run(root: Path) -> None:
    scoped(root)
    run = invoke("--root", str(root), "guide.md#alpha")
    assert run.status == SUCCESS
    assert "### Alpha" in run.stdout


def test_an_unselected_self_link_does_not_fail_the_run(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSelected.\n\n## Beta\n\nSee [¬ here](guide.md#beta).\n",
    )
    assert invoke("--root", str(root), "guide.md#alpha").status == SUCCESS


def test_the_same_sibling_fails_once_the_closure_includes_it(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSee [beta](guide.md#beta).\n\n"
        "## Beta\n\nSee [gone](missing.md).\n",
    )
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md#alpha")
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == TARGET_NOT_FOUND
    assert reported["reference"] == "missing.md"


def test_a_profile_refusal_a_named_document_did_not_select_does_not_fail(
    root: Path,
) -> None:
    scoped(root)
    assert invoke("--root", str(root), "guide.md#alpha").status == SUCCESS


def test_a_profile_refusal_a_reached_document_did_not_select_does_not_fail(
    root: Path,
) -> None:
    scoped(root)
    run = invoke("--root", str(root), "guide.md#alpha")
    assert run.status == SUCCESS
    assert "### Gamma" in run.stdout
    assert "Delta" not in run.stdout


def test_a_profile_refusal_the_run_selected_still_fails(root: Path) -> None:
    scoped(root)
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md#beta")
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RAW_HTML
    assert reported["chain"] == ["guide.md#beta"]


def test_a_refusal_in_a_reached_document_the_closure_selected_fails(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [other](other.md).\n")
    written(root, "other.md", "# Other\n\n<div>raw</div>\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RAW_HTML
    assert reported["source"] == "other.md:3"
    assert reported["chain"] == ["guide.md", "other.md"]


def test_a_target_at_the_expansion_depth_is_bundled(root: Path) -> None:
    chained(root)
    run = invoke("--root", str(root), "--max-expansion-depth", "2", "alpha.md")
    assert run.status == SUCCESS
    assert "# Gamma" in run.stdout


def test_a_crossed_budget_publishes_no_output_file(root: Path, tmp_path: Path) -> None:
    chained(root)
    destination = tmp_path / "bundle.md"
    run = invoke(
        "--root",
        str(root),
        "--max-output-bytes",
        "64",
        "-o",
        str(destination),
        "alpha.md",
    )
    assert run.status == INPUT_FAILURE
    assert not destination.exists()


@pytest.mark.parametrize("value", ["0", "-1", "1.5", "0x10", " 1", ""])
def test_a_budget_override_that_is_no_positive_decimal_integer_is_refused(
    root: Path, value: str
) -> None:
    run = invoke("--root", str(root), f"--max-files={value}", "guide.md")
    assert run.status == USAGE_FAILURE


def test_a_budget_stands_at_the_number_the_profile_declares(root: Path) -> None:
    assert FILES.default == 256
    assert invoke("--root", str(root), "guide.md").status == SUCCESS


def test_a_candidate_disagreeing_with_its_provenance_publishes_nothing(
    root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n\nMore body.\n")
    destination = tmp_path / "bundle.md"
    assembling = assemble

    def dropping(line: str, groups: Sequence[Group]) -> str:
        return assembling(line, groups).replace("\n\nMore body.", "")

    monkeypatch.setattr("prosiform.cli.assemble", dropping)
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "-o",
        str(destination),
        "guide.md",
    )
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert not destination.exists()
    assert [one["code"] for one in run.diagnostics()] == [UNEXPECTED_INTERNAL_ERROR]
    assert "no accidental omissions" in run.diagnostics()[0]["message"]


def unnamed(*arguments: object) -> tuple[str, list[tuple[str, str]]]:
    """Composition raising an error the contract names no outcome for."""
    raise RuntimeError("the composition reached a state the contract never names")


def test_an_error_the_contract_does_not_name_is_an_internal_error_as_data(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("prosiform.cli.compose", unnamed)
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert [(one["severity"], one["code"]) for one in run.diagnostics()] == [
        ("error", UNEXPECTED_INTERNAL_ERROR)
    ]


def test_an_error_the_contract_does_not_name_is_an_internal_error_as_text(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("prosiform.cli.compose", unnamed)
    run = invoke("--root", str(root), "--diagnostics", "text", "guide.md")
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert run.stderr.splitlines() == [
        f"{UNEXPECTED_INTERNAL_ERROR}: unexpected internal error: "
        "RuntimeError('the composition reached a state the contract never names')"
    ]


def captured_for(root: Path, path: str) -> dict[str, Capture]:
    """What one source was when it was read, as discovery captures it."""
    return {path: Capture(canonical(root, path), hashed(read_source(root, path)))}


def test_a_source_nothing_wrote_passes_the_recheck(root: Path) -> None:
    recheck(root, captured_for(root, "guide.md"), {})


def test_a_source_written_after_the_read_fails_the_recheck(root: Path) -> None:
    captured = captured_for(root, "guide.md")
    (root / "guide.md").write_text("# Guide\n\nA line the run never read.\n")
    with pytest.raises(Failure) as raised:
        recheck(root, captured, {"guide.md": ("guide.md",)})
    assert raised.value.diagnostic.code == SOURCE_CHANGED
    assert raised.value.status == INPUT_FAILURE


def test_a_source_removed_after_the_read_fails_the_recheck(root: Path) -> None:
    captured = captured_for(root, "guide.md")
    (root / "guide.md").unlink()
    with pytest.raises(Failure) as raised:
        recheck(root, captured, {"guide.md": ("guide.md",)})
    assert raised.value.diagnostic.code == SOURCE_CHANGED


def test_a_source_resolving_elsewhere_fails_the_recheck(tmp_path: Path) -> None:
    for name in ("one", "two"):
        (tmp_path / name).mkdir()
        (tmp_path / name / "guide.md").write_text("# Guide\n")
    os.symlink(tmp_path / "one", tmp_path / "now")
    root = tmp_path / "now"
    captured = captured_for(root, "guide.md")
    (tmp_path / "now").unlink()
    os.symlink(tmp_path / "two", tmp_path / "now")
    with pytest.raises(Failure) as raised:
        recheck(root, captured, {"guide.md": ("guide.md",)})
    assert raised.value.diagnostic.code == SOURCE_CHANGED
    assert str(tmp_path / "two" / "guide.md") in raised.value.diagnostic.message


def writing_once(root: Path, write: Callable[[Path], object]) -> Callable[..., bytes]:
    """A read that writes the source tree once, as a run's first read returns."""
    reads: list[str] = []

    def reading(at: Path, path: str) -> bytes:
        data = read_source(at, path)
        reads.append(path)
        if len(reads) == 1:
            write(root / path)
        return data

    return reading


def test_a_source_written_during_the_run_publishes_nothing(
    root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "prosiform.cli.read_source",
        writing_once(root, lambda path: path.write_text("# Guide\n\nRewritten.\n")),
    )
    output = tmp_path / "bundle.md"
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--output",
        str(output),
        "guide.md",
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_CHANGED]
    assert not output.exists()


def test_a_source_removed_during_the_run_publishes_nothing(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(
        "prosiform.cli.read_source",
        writing_once(root, lambda path: path.unlink()),
    )
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_CHANGED]


def test_a_title_the_allowed_source_root_cannot_contain_names_no_document(
    root: Path,
) -> None:
    (root.parent / "outside.md").write_text("# Outside\n")
    (root / "titled.md").write_text("# ../outside\n\nBody.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "titled.md")
    assert run.status == SUCCESS
    assert [one["code"] for one in run.diagnostics()] == [ENTRY_DESTINATION]


def test_an_unsafe_boundary_is_an_input_failure(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text(
        "# Guide\n\n- The first list.\n\n[notes]: notes.md\n\n- The second list.\n"
    )
    run = invoke("--root", str(tmp_path), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    one = run.diagnostics()[0]
    assert one["code"] == UNSAFE_BUNDLE_BOUNDARY
    assert one["reference"] == "guide.md"
    assert one["source"] == "guide.md"
    assert "is placed inside the list that" in one["message"]
    assert one["remedy"]


def test_an_unsafe_boundary_publishes_no_file(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "guide.md").write_text(
        "# Guide\n\n- The first list.\n\n[notes]: notes.md\n\n- The second list.\n"
    )
    destination = tmp_path / "bundle.md"
    run = invoke(
        "--root",
        str(source),
        "--diagnostics",
        "json",
        "--output",
        str(destination),
        "guide.md",
    )
    assert run.status == INPUT_FAILURE
    assert not destination.exists()


def surrounded(brackets: int) -> str:
    """One source whose dependency sits under a run of open brackets."""
    return f"# Guide\n\nThe guide cites {'[' * brackets}the plan](plan.md).\n"


def test_a_lookup_the_parser_declines_fails_the_run(root: Path) -> None:
    written(root, "guide.md", surrounded(1 + HEADROOM + 1))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--max-nesting", "1", "guide.md"
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == PARSER_REFERENCE_LIMIT
    assert reported["source"] == "guide.md:3"
    assert reported["chain"] == ["guide.md"]


def test_a_ceiling_reached_by_the_last_valid_reference_bundles_it(root: Path) -> None:
    written(root, "guide.md", surrounded(1 + HEADROOM))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--max-nesting", "1", "guide.md"
    )
    assert run.status == SUCCESS
    assert "The plan." in run.stdout
    assert [one["code"] for one in run.diagnostics()] == [ENTRY_DESTINATION]


def test_the_source_changed_fault_fails_the_run_and_publishes_nothing(
    root: Path, tmp_path: Path
) -> None:
    """The fault writes to the tree, and the run's own recheck is what fails it."""
    output = tmp_path / "bundle.md"
    run = invoke(
        "--root",
        str(root),
        "--diagnostics",
        "json",
        "--fault",
        "source-changed",
        "--output",
        str(output),
        "guide.md",
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_CHANGED]
    assert not output.exists()
    assert (root / "guide.md").read_bytes() != b"# Guide\n"


def test_the_internal_fault_names_the_run_and_publishes_nothing(root: Path) -> None:
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--fault", "internal", "guide.md"
    )
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [UNEXPECTED_INTERNAL_ERROR]


def test_a_run_asking_for_no_fault_meets_none(root: Path) -> None:
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == SUCCESS
    assert (root / "guide.md").read_bytes() == b"# Guide\n"


def test_a_fault_the_contract_does_not_declare_is_a_usage_failure(root: Path) -> None:
    run = invoke(
        "--root", str(root), "--diagnostics", "json", "--fault", "other", "guide.md"
    )
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_a_declined_lookup_names_the_reference_under_the_default_budgets(
    root: Path,
) -> None:
    written(root, "guide.md", surrounded(NESTING.default + HEADROOM + 1))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == PARSER_REFERENCE_LIMIT
    assert reported["reference"] == "plan.md"
    assert reported["source"] == "guide.md:3"


def test_a_budget_spent_on_the_last_valid_reference_bundles_it(root: Path) -> None:
    written(root, "guide.md", surrounded(NESTING.default + HEADROOM))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke("--root", str(root), "--diagnostics", "json", "guide.md")
    assert run.status == SUCCESS
    assert "The plan." in run.stdout
    assert PARSER_REFERENCE_LIMIT not in run.stderr


@pytest.mark.parametrize("folder", ["docs", "DoCs"])
@pytest.mark.parametrize("merged", [False, True])
def test_actual_bundle_reuse_is_refused(
    tmp_path: Path, folder: str, merged: bool
) -> None:
    source = tmp_path / folder / "gUiDe.md"
    source.parent.mkdir()
    source.write_text("# Guide\n\n## Install\n\nContent.\n")
    grouping = ("--group", f"{folder}:2") if merged else ()
    first = invoke("--root", str(tmp_path), *grouping, f"{folder}/gUiDe.md")
    assert first.status == SUCCESS
    (tmp_path / "bundle.md").write_text(first.stdout)
    second = invoke("--root", str(tmp_path), "--diagnostics", "json", "bundle.md")
    assert second.status == INPUT_FAILURE
    assert second.stdout == ""
    assert second.diagnostics()[0]["code"] == GENERATED_INPUT
    assert second.diagnostics()[0]["source"] == "bundle.md:1"


@pytest.mark.parametrize(
    "text",
    [
        "~~~markdown\n{declaration}\n~~~\n",
        "> {declaration}\n\n# Notes\n",
        "# Notes\n\n{declaration}\n",
        "This bundle was built for prose; everything else is material it references.\n",
        "This bundle was built for [Notes](https://example.com); "
        "everything else is material it references.\n",
    ],
)
def test_authored_declaration_examples_bundle(tmp_path: Path, text: str) -> None:
    declaration = (
        "This bundle was built for [Notes](#notes); "
        "everything else is material it references."
    )
    (tmp_path / "notes.md").write_text(text.format(declaration=declaration))
    result = invoke("--root", str(tmp_path), "notes.md")
    assert result.status == SUCCESS


def test_generated_input_reports_location_after_frontmatter(tmp_path: Path) -> None:
    (tmp_path / "bundle.md").write_text(
        "---\ntitle: Bundle\n---\n\n"
        "This bundle was built for [Notes](#notes); "
        "everything else is material it references.\n"
        "\n# Notes\n\n## Findings\n\nContent.\n"
    )
    result = invoke(
        "--root", str(tmp_path), "--diagnostics", "json", "bundle.md#findings"
    )
    assert result.status == INPUT_FAILURE
    assert result.diagnostics()[0]["code"] == GENERATED_INPUT
    assert result.diagnostics()[0]["source"] == "bundle.md:5"
