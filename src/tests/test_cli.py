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
from contextlib import chdir
from dataclasses import dataclass
from importlib.metadata import version
from io import StringIO
from pathlib import Path
from typing import IO, Any

import pytest

from prosiform import PROFILE
from prosiform.access import read_source
from prosiform.bundle import (
    CODES as BUNDLE_CODES,
)
from prosiform.bundle import (
    HEADING_DEPTH_OVERFLOW,
    Group,
    assemble,
)
from prosiform.candidate import (
    CODES as CANDIDATE_CODES,
)
from prosiform.candidate import (
    UNSAFE_BUNDLE_BOUNDARY,
)
from prosiform.cli import (
    CODES,
    COINCIDENT_HEADING,
    GROUP_DEPTH_CONFLICT,
    INPUT_FAILURE,
    INTERNAL_ERROR,
    INVALID_ENCODING,
    INVALID_USAGE,
    PUBLICATION_FAILED,
    PUBLICATION_FAILURE,
    RESOURCE_PORTABILITY,
    ROOT_NOT_FOUND,
    SOURCE_ACCESS,
    SOURCE_CHANGED,
    SOURCE_OUTSIDE_ROOT,
    SOURCE_SYMLINK,
    SUCCESS,
    TARGET_NOT_FOUND,
    UNEXPECTED_INTERNAL_ERROR,
    UNSUPPORTED_ENTRY_SUFFIX,
    USAGE_FAILURE,
    Failure,
    entry,
    main,
    parser,
    read_document,
    recheck,
)
from prosiform.closure import resolve
from prosiform.dispatch import CODES as DISPATCH_CODES
from prosiform.dispatch import DISPATCH_CYCLE, DISPATCH_DEPTH
from prosiform.limits import (
    BUDGETS,
    FILES,
    NESTING,
    RESOURCE_LIMIT,
    Limits,
)
from prosiform.limits import (
    CODES as LIMITS_CODES,
)
from prosiform.metadata import INVALID_CONVERSION_METADATA
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


def invoke(
    *arguments: str, stdout: IO[str] | None = None, cwd: Path | None = None
) -> Run:
    """One run requesting stdout, with any supplied output option taking precedence."""
    out = StringIO() if stdout is None else stdout
    err = StringIO()
    with chdir(Path.cwd() if cwd is None else cwd):
        status = main(["-o", "-", *arguments], out, err)
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
    run = invoke("-v")
    assert run.status == SUCCESS
    assert run.stdout == f"pf {version('prosiform')} ({PROFILE})\n"
    assert run.stderr == ""


def test_the_help_response_shows_usage_defaults_and_exit_statuses() -> None:
    run = invoke("-h")
    assert run.status == SUCCESS
    assert run.stdout.startswith("usage: pf [OPTIONS] REF [REF ...]")
    assert "default text" in run.stdout
    assert "exit statuses:" in run.stdout
    for status in ("0", "1", "2", "3", "4"):
        assert f"\n  {status}  " in run.stdout
    assert run.stderr == ""


def test_the_codes_response_names_every_code_the_build_can_emit() -> None:
    run = invoke("-C")
    assert run.status == SUCCESS
    assert run.stdout == "".join(f"{code}\n" for code in sorted(CODES))
    assert run.stderr == ""


def test_the_codes_reported_are_the_codes_the_build_declares() -> None:
    declared = {
        GROUP_DEPTH_CONFLICT,
        INVALID_ENCODING,
        INVALID_USAGE,
        PUBLICATION_FAILED,
        ROOT_NOT_FOUND,
        SOURCE_CHANGED,
        SOURCE_ACCESS,
        SOURCE_ACCESS,
        SOURCE_OUTSIDE_ROOT,
        SOURCE_SYMLINK,
        TARGET_NOT_FOUND,
        UNEXPECTED_INTERNAL_ERROR,
        UNSUPPORTED_ENTRY_SUFFIX,
        RESOURCE_PORTABILITY,
        COINCIDENT_HEADING,
    }
    for published in (
        BUNDLE_CODES,
        CANDIDATE_CODES,
        DISPATCH_CODES,
        LIMITS_CODES,
        PROFILE_CODES,
        SOURCE_CODES,
    ):
        declared.update(published)
    assert CODES == tuple(sorted(declared))


def test_an_informational_response_needs_no_source_root() -> None:
    assert invoke("-v").status == SUCCESS
    assert invoke("-h").status == SUCCESS
    assert invoke("-C").status == SUCCESS


@pytest.mark.parametrize(
    "option",
    [
        "--root",
        "--from",
        "--output",
        "--group",
        "--check",
        "--diagnostics",
        "--fault",
        "--max-files",
        "--max-file-bytes",
        "--max-input-bytes",
        "--max-output-bytes",
        "--max-targets",
        "--max-links",
        "--max-nesting",
        "--max-expansion-depth",
        "--codes",
        "--version",
        "--help",
    ],
)
def test_long_options_are_invalid_usage(option: str) -> None:
    run = invoke(option)
    assert run.status == USAGE_FAILURE
    assert INVALID_USAGE in run.stderr
    assert run.stdout == ""


@pytest.mark.parametrize(
    ("flag", "destination"),
    [
        ("-F", "max_files"),
        ("-B", "max_file_bytes"),
        ("-I", "max_input_bytes"),
        ("-O", "max_output_bytes"),
        ("-T", "max_targets"),
        ("-L", "max_links"),
        ("-N", "max_nesting"),
        ("-E", "max_expansion_depth"),
    ],
)
def test_budget_flags_select_the_planned_limit(flag: str, destination: str) -> None:
    options = parser().parse_args([flag, "123"])
    assert getattr(options, destination) == 123


@pytest.mark.parametrize(
    "arguments", [("-djson",), ("-d=json",), ("-cdjson",), ("-d", "json")]
)
def test_short_diagnostic_forms_report_usage_as_json(
    arguments: tuple[str, ...],
) -> None:
    run = invoke(*arguments, "--unknown")
    assert run.status == USAGE_FAILURE
    assert json.loads(run.stderr)["code"] == INVALID_USAGE


@pytest.mark.parametrize(
    "arguments", [("--", "-djson"), ("-o-djson",), ("-d=json", "-dtext")]
)
def test_diagnostic_selection_respects_values_terminators_and_last_option(
    arguments: tuple[str, ...],
) -> None:
    run = invoke(*arguments)
    if arguments[0] == "--":
        assert run.status == INPUT_FAILURE
        assert run.stderr.startswith(UNSUPPORTED_ENTRY_SUFFIX)
    else:
        assert run.status == USAGE_FAILURE
        assert run.stderr.startswith(INVALID_USAGE)


def test_every_option_the_contract_declares_is_accepted(root: Path) -> None:
    run = invoke(
        "-f",
        "guide.md",
        "-o",
        str(root.parent / "bundle.md"),
        "-c",
        "-d",
        "json",
        "guide.md",
        cwd=root,
    )
    assert run.status == SUCCESS


@pytest.mark.parametrize("option", ["--manifest", "--watch", "--cache"])
def test_an_option_the_contract_does_not_declare_is_refused(
    root: Path, option: str
) -> None:
    run = invoke(option, "8", "guide.md", cwd=root)
    assert run.status == USAGE_FAILURE


def test_a_missing_entry_is_invalid_usage() -> None:
    run = invoke()
    assert run.status == USAGE_FAILURE
    assert run.stdout == ""
    assert "entry reference" in run.stderr


def test_a_run_naming_no_entry_reference_is_invalid_usage(root: Path) -> None:
    run = invoke(cwd=root)
    assert run.status == USAGE_FAILURE
    assert run.stdout == ""


def test_a_fragment_only_reference_needs_a_referring_document(root: Path) -> None:
    run = invoke("#a-section", cwd=root)
    assert run.status == USAGE_FAILURE
    assert "-f" in run.stderr


def test_a_fragment_only_reference_selects_from_the_referring_document(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    assert invoke("-f", "guide.md", "#run", cwd=root).stdout == (
        invoke("guide.md#run", cwd=root).stdout
    )


def test_an_entry_naming_a_member_of_one_heading_opens_on_its_title(
    root: Path,
) -> None:
    written(root, "notes/bare.md", conversion("notes", 2) + "# Bare\n")
    run = invoke("notes/bare.md", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout == "# Bare\n"


def test_an_entry_naming_the_absorbed_title_of_a_member_opens_on_that_title(
    root: Path,
) -> None:
    written(
        root,
        "notes/second.md",
        conversion("notes", 2) + "# Second\n\n## Outcomes\n\nText.\n",
    )
    run = invoke("notes/second.md#second", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout.startswith("# Second\n\n## Outcomes\n")


def test_a_reference_into_a_member_of_one_heading_reaches_its_subsection(
    root: Path,
) -> None:
    written(root, "notes/bare.md", conversion("notes", 2) + "# Bare\n")
    written(root, "guide.md", "# Guide\n\nSee [Bare](notes/bare.md).\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "See [Bare](#bare)." in run.stdout


def test_a_source_root_naming_no_directory_is_an_input_failure(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text("---\nprosiform: {root: absent}\n---\n# Guide\n")
    run = invoke("-d", "json", "guide.md", cwd=tmp_path)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [ROOT_NOT_FOUND]


def test_a_usage_failure_is_reported_before_an_input_failure(tmp_path: Path) -> None:
    run = invoke("--unknown", "docs:9", "guide.md", cwd=tmp_path)
    assert run.status == USAGE_FAILURE


@pytest.mark.parametrize("value", ["yaml", "", "TEXT", "jsonl"])
def test_a_diagnostic_format_the_contract_does_not_declare_is_invalid_usage(
    root: Path, value: str
) -> None:
    run = invoke("-d", value, "guide.md", cwd=root)
    assert run.status == USAGE_FAILURE
    assert run.stdout == ""


def test_an_output_path_naming_an_input_source_is_invalid_usage(root: Path) -> None:
    run = invoke("-o", str(root / "guide.md"), "guide.md", cwd=root)
    assert run.status == USAGE_FAILURE
    assert "input source" in run.stderr


def test_an_output_path_naming_the_referring_document_is_invalid_usage(
    root: Path,
) -> None:
    run = invoke("-f", "guide.md", "-o", str(root / "guide.md"), "#guide", cwd=root)
    assert run.status == USAGE_FAILURE


def test_an_output_path_naming_a_dependency_source_is_invalid_usage(
    root: Path,
) -> None:
    (root / "guide.md").write_text("# Guide\n\nIt needs [the note](docs/note.md).\n")
    note = root / "docs" / "note.md"
    run = invoke("-o", str(note), "guide.md", cwd=root)
    assert run.status == USAGE_FAILURE
    assert "input source" in run.stderr
    assert note.read_text() == "# Note\n"


def test_a_source_reached_through_a_link_is_no_identity_the_output_check_holds(
    root: Path, tmp_path: Path
) -> None:
    outside = tmp_path.parent / "outside.md"
    outside.write_text("# Outside\n")
    (root / "alias.md").symlink_to(outside)
    run = invoke("-d", "json", "-o", str(outside), "alias.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_SYMLINK]


def test_an_output_path_naming_no_input_source_is_accepted(
    root: Path, tmp_path: Path
) -> None:
    run = invoke("-o", str(tmp_path / "bundle.md"), "guide.md", cwd=root)
    assert run.status == SUCCESS


def test_standard_output_is_an_explicit_output_destination(root: Path) -> None:
    run = invoke("-o", "-", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout.startswith("# Guide\n")


def test_a_validation_only_run_publishes_nothing(root: Path) -> None:
    run = invoke("-c", "guide.md", cwd=root)
    assert run.stdout == ""


def test_a_validation_only_run_with_an_output_file_creates_no_file(
    root: Path, tmp_path: Path
) -> None:
    destination = tmp_path / "bundle.md"
    run = invoke("-c", "-o", str(destination), "guide.md", cwd=root)
    assert run.status != USAGE_FAILURE
    assert run.stdout == ""
    assert not destination.exists()


def test_a_refused_write_is_a_publication_failure() -> None:
    run = invoke("-v", stdout=Refusing())
    assert run.status == PUBLICATION_FAILURE
    assert "standard output" in run.stderr
    assert run.stderr.startswith(f"{PUBLICATION_FAILED}: ")


def test_a_failing_run_writes_its_diagnostics_as_data(root: Path) -> None:
    run = invoke("-d", "json", "--unknown", "x", "g.md", cwd=root)
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
    run = invoke("--unknown", "docs:9", "guide.md", cwd=root)
    assert run.stdout == ""
    assert run.stderr.startswith(f"{INVALID_USAGE}: ")


def conversion(group: str, depth: int) -> str:
    """One source's complete conversion metadata."""
    return (
        "---\nprosiform:\n  group: "
        + json.dumps(group)
        + "\n  group-depth: "
        + str(depth)
        + "\n---\n"
    )


def written(root: Path, name: str, text: str) -> None:
    """One source document under the allowed source root."""
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_an_entry_reference_stands_at_the_head_of_its_own_chain(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac gone](missing.md).\n")
    run = invoke("-d", "json", "guide.md#nowhere", cwd=root)
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
    run = invoke("-d", "json", "entry.md", cwd=root)
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
    run = invoke("-d", "json", "entry.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [RAW_HTML]
    assert run.diagnostics()[0]["chain"] == ["entry.md", "docs/notes.md"]


def test_a_usage_failure_reaching_no_document_carries_no_chain(root: Path) -> None:
    run = invoke("-d", "json", "--unknown", "x", "g.md", cwd=root)
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
    run = invoke("-d", "json", "guide.md", cwd=root)
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
    assert invoke("guide.md", cwd=root).status == SUCCESS


def test_the_referring_document_is_read_under_the_profile(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n<div>raw</div>\n")
    run = invoke("-f", "guide.md", "#a-section", cwd=root)
    assert run.status == INPUT_FAILURE
    assert "guide.md" in run.stderr


def test_a_refusal_names_the_construct_and_where_it_sits(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [[page]] for the procedure.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    reported = run.diagnostics()[0]
    assert reported["reference"] == "[[page]]"
    assert reported["source"] == "guide.md:3"
    assert "wiki link" in reported["message"]


def test_an_entry_suffix_outside_the_profile_is_an_input_failure(root: Path) -> None:
    written(root, "notes.txt", "# Notes\n")
    run = invoke("-d", "json", "notes.txt", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["reference"] == "notes.txt"
    assert [one["code"] for one in run.diagnostics()] == [UNSUPPORTED_ENTRY_SUFFIX]


def test_an_entry_suffix_is_classified_case_insensitively(root: Path) -> None:
    written(root, "GUIDE.MARKDOWN", "# Guide\n")
    assert invoke("GUIDE.MARKDOWN", cwd=root).status == SUCCESS


def test_an_entry_naming_no_document_is_an_input_failure(root: Path) -> None:
    run = invoke("-d", "json", "absent.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [TARGET_NOT_FOUND]


@pytest.mark.parametrize("reference", ["/guide.md", "C:/guide.md", "//host/guide.md"])
def test_an_entry_the_root_cannot_contain_is_an_input_failure(
    root: Path, reference: str
) -> None:
    written(root.parent, "outside.md", "# Outside\n")
    run = invoke("-d", "json", reference, cwd=root)
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_OUTSIDE_ROOT]


def test_a_fragment_reference_reads_the_whole_document_it_names(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\n<div>raw</div>\n")
    run = invoke("guide.md#run", cwd=root)
    assert run.status == INPUT_FAILURE


@pytest.mark.parametrize(
    "arguments",
    [
        (),
        ("#a-section",),
        ("-d", "yaml", "guide.md"),
        ("--watch", "guide.md"),
    ],
)
def test_a_fault_in_the_command_line_carries_the_invalid_usage_code(
    root: Path, arguments: tuple[str, ...]
) -> None:
    run = invoke("-d", "json", *arguments, cwd=root)
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_a_missing_entry_carries_the_invalid_usage_code() -> None:
    run = invoke("-d", "json")
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_an_output_path_naming_an_input_source_carries_the_invalid_usage_code(
    root: Path,
) -> None:
    run = invoke("-d", "json", "-o", str(root / "guide.md"), "guide.md", cwd=root)
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_a_source_that_is_not_valid_utf8_is_an_input_failure(root: Path) -> None:
    (root / "guide.md").write_bytes(b"# Guide\n\nA byte that is not UTF-8: \xe9\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
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
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert "unexpected internal error" not in run.diagnostics()[0]["message"]


def test_an_unterminated_frontmatter_opener_is_an_input_failure(root: Path) -> None:
    written(root, "guide.md", "---\ntitle: Guide\n\n# Guide\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == UNTERMINATED_FRONTMATTER
    assert reported["source"] == "guide.md:1"


def test_transport_metadata_reaches_no_parse(root: Path) -> None:
    written(root, "guide.md", "﻿---\ntitle: Guide\n---\n# Guide\n\n<div>raw</div>\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert "raw HTML" in run.diagnostics()[0]["message"]


def test_a_diagnostic_below_a_stripped_block_names_the_line_of_the_file(
    root: Path,
) -> None:
    written(root, "guide.md", "---\ntitle: Guide\n---\n# Guide\n\nSee [[page]] now.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.diagnostics()[0]["source"] == "guide.md:6"


def test_a_diagnostic_below_a_mark_alone_names_the_line_of_the_file(
    root: Path,
) -> None:
    written(root, "guide.md", "﻿# Guide\n\nSee [[page]] now.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
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
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.diagnostics()[0]["source"] == f"guide.md:{at}"


def test_a_crlf_delimited_block_is_stripped_by_the_command(root: Path) -> None:
    (root / "guide.md").write_bytes(b"---\r\ntitle: Guide\r\n---\r\nSee [[page]].\r\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["source"] == "guide.md:4"


def test_a_referring_document_is_stripped_too(root: Path) -> None:
    written(
        root,
        "guide.md",
        "---\ntitle: Guide\n---\n# Guide\n\n## Run\n\n<div>raw</div>\n",
    )
    run = invoke("-d", "json", "-f", "guide.md", "#run", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["source"] == "guide.md:8"


def test_a_stripped_source_the_profile_accepts_bundles(root: Path) -> None:
    written(root, "guide.md", "﻿---\ntitle: Guide\n...\n# Guide\n")
    assert invoke("guide.md", cwd=root).status == SUCCESS


def test_a_crlf_source_is_read_without_newline_translation(root: Path) -> None:
    (root / "guide.md").write_bytes(b"---\r\ntitle: Guide\r\n---\r\n# Guide\r\n")
    read = read_document(
        root, resolve("guide.md"), Limits({b: b.default for b in BUDGETS})
    ).source
    assert read.text == "# Guide\r\n"
    assert read.first_line == 4


def test_a_successful_run_publishes_the_bundle_and_nothing_else(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\nDo it.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.diagnostics() == []
    assert run.stdout == ("# Guide\n\n## Run\n\nDo it.\n")


def test_a_run_that_cannot_publish_reports_the_publication_failure_alone(
    root: Path, tmp_path: Path
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    run = invoke(
        "-d", "json", "-o", str(tmp_path / "absent" / "bundle.md"), "guide.md", cwd=root
    )
    assert run.status == PUBLICATION_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [PUBLICATION_FAILED]


def test_two_untitled_sources_sharing_a_basename_stay_distinguishable(
    root: Path,
) -> None:
    written(root, "docs/note.md", "Under docs.\n")
    written(root, "notes/note.md", "Under notes.\n")
    run = invoke("docs/note.md", "notes/note.md", cwd=root)
    assert run.status == SUCCESS
    assert "# Docs/Note\n\nUnder docs." in run.stdout
    assert "# Notes/Note\n\nUnder notes." in run.stdout


def test_two_sources_sharing_a_title_take_distinct_destinations(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n[One](docs/note.md) [Two](notes/note.md)\n")
    written(root, "docs/note.md", "# Note\n\nUnder docs.\n")
    written(root, "notes/note.md", "# Note\n\nUnder notes.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "[One](#note) [Two](#note-1)" in run.stdout
    assert run.stdout.index("Under docs.") < run.stdout.index("Under notes.")
    assert run.stdout.count("# Note\n") == 2


def test_entry_documents_are_ordered_as_the_invocation_names_them(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n")
    written(root, "docs/note.md", "Body.\n")
    written(root, "notes/note.md", "Body.\n")
    ordered = invoke("guide.md", "notes/note.md", "docs/note.md", cwd=root).stdout
    assert ordered.index("# Guide\n") < ordered.index("# Notes/Note\n")
    assert ordered.index("# Notes/Note\n") < ordered.index("# Docs/Note\n")


def test_groups_are_ordered_by_first_link(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n[Zulu](zulu.md) then [Alpha](alpha.md).\n")
    written(root, "alpha.md", "# Alpha\n\n[Mike](mike.md)\n")
    written(root, "zulu.md", "# Zulu\n\n[Bravo](bravo.md)\n")
    written(root, "bravo.md", "# Bravo\n")
    written(root, "mike.md", "# Mike\n")
    ordered = invoke("guide.md", cwd=root).stdout
    found = [ordered.index(f"# {name}\n") for name in ("Guide", "Zulu", "Alpha")]
    found += [ordered.index(f"# {name}\n") for name in ("Bravo", "Mike")]
    assert found == sorted(found)


def test_members_are_ordered_by_first_link(root: Path) -> None:
    member = "---\nprosiform: {group: notes, group-depth: 2}\n---\n"
    written(root, "guide.md", "# Guide\n\n[Zulu](zulu.md) then [Alpha](alpha.md).\n")
    written(root, "alpha.md", member + "# Alpha\n\n## Use\n\nAlpha use.\n")
    written(root, "zulu.md", member + "# Zulu\n\n## Use\n\nZulu use.\n")
    ordered = invoke("guide.md", cwd=root).stdout
    assert ordered.index("### Zulu\n") < ordered.index("### Alpha\n")
    assert ordered.index("Zulu use.") < ordered.index("Alpha use.")


def test_one_document_named_twice_is_one_group(root: Path) -> None:
    written(root, "guide.md", "# Guide\n")
    (root / "sub").mkdir()
    run = invoke("guide.md", "sub/../guide.md", cwd=root)
    assert run.stdout.count("# Guide\n") == 1


def test_two_paths_differing_only_by_suffix_are_two_groups(root: Path) -> None:
    written(root, "guide.md", "One.\n")
    written(root, "guide.markdown", "Two.\n")
    run = invoke("-d", "json", "guide.md", "guide.markdown", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout == "# Guide\n\nOne.\n\n# Guide\n\nTwo.\n"
    assert [one["code"] for one in run.diagnostics()] == [COINCIDENT_HEADING]


def test_coinciding_file_headings_warn_once_naming_every_source(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\nRead [a](a/note.md), [b](b/note.md) and [c](c/note.md).\n",
    )
    written(root, "a/note.md", "Intro.\n\n# Note\n\nA.\n")
    written(root, "b/note.md", "---\nname: b\n---\n# NOTE\n\nB.\n")
    written(root, "c/note.md", "# Note\n\nC.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "[a](#note), [b](#note-1) and [c](#note-2)" in run.stdout
    assert run.diagnostics() == [
        {
            "severity": "warning",
            "message": "3 file headings read 'Note', which a reader tells apart "
            "only by where each stands",
            "code": COINCIDENT_HEADING,
            "remedy": "retitle or rename a document so its file heading reads apart",
            "location": {"file": "a/note.md", "line": 3, "column": 1},
            "related": [
                {
                    "file": "b/note.md",
                    "line": 4,
                    "column": 1,
                    "message": "file heading 'NOTE'",
                },
                {
                    "file": "c/note.md",
                    "line": 1,
                    "column": 1,
                    "message": "file heading 'Note'",
                },
            ],
        }
    ]


def test_a_path_heading_is_located_at_its_document(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nRead [one](one/notes.md).\n")
    written(root, "one/notes.md", "Read [two](../One/notes.md).\n")
    written(root, "One/notes.md", "Two.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "# One/Notes\n\nRead [two](#onenotes-1).\n\n# One/Notes\n" in run.stdout
    [warning] = run.diagnostics()
    assert warning["location"] == {"file": "one/notes.md", "line": 1, "column": 1}
    assert warning["related"] == [
        {
            "file": "One/notes.md",
            "line": 1,
            "column": 1,
            "message": "file heading 'One/Notes'",
        }
    ]


def test_the_parent_title_coincides_with_a_file_heading(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nRead [the other](other/guide.md).\n")
    written(root, "other/guide.md", "# Guide\n\nOther.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    [warning] = run.diagnostics()
    assert warning["location"] == {"file": "guide.md", "line": 1, "column": 1}
    assert [one["file"] for one in warning["related"]] == ["other/guide.md"]


def test_each_coinciding_set_warns_in_bundle_order(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n[1](a/b.md) [2](a/c.md) [3](z/c.md) [4](z/b.md)\n",
    )
    for name in ("a/b.md", "a/c.md", "z/c.md", "z/b.md"):
        written(root, name, "Body.\n")
    written(root, "a/b.md", "# Bee\n")
    written(root, "z/b.md", "# Bee\n")
    written(root, "a/c.md", "# Sea\n")
    written(root, "z/c.md", "# Sea\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert [one["location"]["file"] for one in run.diagnostics()] == [
        "a/b.md",
        "a/c.md",
    ]


def test_headings_an_author_repeats_warn_of_nothing(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nRead [the note](note.md).\n\n## Use\n")
    written(root, "note.md", "# Note\n\n## Use\n\n## Use\n\n### Note\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.diagnostics() == []


def test_members_whose_names_coincide_publish_and_warn(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\nRead [one](notes/note.md) and [two](notes/note.markdown).\n",
    )
    written(root, "notes/note.md", conversion("notes", 2) + "One.\n")
    written(root, "notes/note.markdown", conversion("notes", 2) + "Two.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout == (
        "# Guide\n\nRead [one](#note) and [two](#note-1).\n\n"
        "# Notes\n\n## Note\n\nOne.\n\n## Note\n\nTwo.\n"
    )
    assert run.diagnostics() == [
        {
            "severity": "warning",
            "message": "2 member headings of group 'notes' read 'Note', which a "
            "reader tells apart only by where each stands",
            "code": COINCIDENT_HEADING,
            "remedy": "rename a member so its path distinguishes it in the group",
            "location": {"file": "notes/note.md", "line": 3, "column": 10},
            "related": [
                {
                    "file": "notes/note.markdown",
                    "line": 3,
                    "column": 10,
                    "message": "member heading 'Note'",
                }
            ],
        }
    ]


def test_a_coincidence_reads_as_text(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nRead [a](a/note.md) and [b](b/note.md).\n")
    written(root, "a/note.md", "# Note\n")
    written(root, "b/note.md", "# Note\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.stderr == (
        "W_COINCIDENT_HEADING: 2 file headings read 'Note', which a reader "
        "tells apart only by where each stands\n"
        "  remedy: retitle or rename a document so its file heading reads apart\n"
        "  location: a/note.md:1:1\n"
        "  related: b/note.md:1:1: file heading 'Note'\n"
    )


def test_a_heading_beyond_the_sixth_level_fails_and_publishes_nothing(
    root: Path,
) -> None:
    written(root, "deep.md", "## Lead\n\n###### Deep\n")
    written(root, "guide.md", "# Guide\n\nIt needs [the deep one](deep.md).\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [HEADING_DEPTH_OVERFLOW]


def test_a_structural_ancestor_beyond_the_sixth_level_fails_by_its_own_name(
    root: Path,
) -> None:
    written(
        root,
        "references/alpha.md",
        conversion("references", 1)
        + "# Conventions\n\n## Standards\n\n### Formatting\n\n#### Headings\n\n"
        "##### Levels\n\n###### The Sixth\n\nThe note the sixth level carries.\n",
    )
    written(
        root,
        "references/beta.md",
        conversion("references", 1)
        + "# Conventions\n\n## Standards\n\nWhat this document holds to.\n",
    )
    run = invoke(
        "-d",
        "json",
        "references/alpha.md#the-sixth",
        "references/beta.md#standards",
        cwd=root,
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == HEADING_DEPTH_OVERFLOW
    assert "'Levels' at level 7" in reported["message"]


def test_a_fragment_selects_the_section_its_heading_roots(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n\nDo it.\n\n## Stop\n\nStop it.\n")
    run = invoke("guide.md#run", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout == ("# Guide\n\n### Run\n\nDo it.\n")


def test_a_fragment_naming_a_container_nested_heading_is_refused(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n> ## Nested\n>\n> Inside.\n")
    run = invoke("-d", "json", "guide.md#nested", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [NESTED_SECTION_TARGET]
    assert [one["reference"] for one in run.diagnostics()] == ["guide.md#nested"]


def test_a_fragment_naming_no_heading_is_a_missing_target(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Run\n")
    run = invoke("-d", "json", "guide.md#stop", cwd=root)
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [TARGET_NOT_FOUND]


def test_an_empty_fragment_is_a_whole_document_reference(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    assert invoke("guide.md#", cwd=root).stdout == (invoke("guide.md", cwd=root).stdout)


def test_a_referring_document_contributes_no_group(root: Path) -> None:
    written(root, "docs/note.md", "# Note\n")
    written(root, "guide.md", "# Guide\n")
    run = invoke("-f", "guide.md", "docs/note.md", cwd=root)
    assert run.status == SUCCESS
    assert "# Guide\n" not in run.stdout
    assert "# Note\n" in run.stdout


def test_a_named_output_file_carries_the_bundle(root: Path, tmp_path: Path) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    destination = tmp_path / "bundle.md"
    run = invoke("-o", str(destination), "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout == ""
    assert destination.read_text() == ("# Guide\n\nBody.\n")


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
    assert invoke("-o", str(destination), "guide.md", cwd=root).status == (SUCCESS)
    assert [target for _, target in renamed] == [str(destination)]
    assert [path.name for path in published.iterdir()] == ["bundle.md"]


def test_a_failed_run_leaves_the_output_file_alone(root: Path, tmp_path: Path) -> None:
    written(root, "guide.md", "# Guide\n\n<div>raw</div>\n")
    destination = tmp_path / "bundle.md"
    destination.write_text("earlier bytes\n")
    assert invoke("-o", str(destination), "guide.md", cwd=root).status == (
        INPUT_FAILURE
    )
    assert destination.read_text() == "earlier bytes\n"


def test_an_output_path_the_run_cannot_write_is_a_publication_failure(
    root: Path, tmp_path: Path
) -> None:
    written(root, "guide.md", "# Guide\n")
    run = invoke(
        "-d", "json", "-o", str(tmp_path / "absent" / "bundle.md"), "guide.md", cwd=root
    )
    assert run.status == PUBLICATION_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [PUBLICATION_FAILED]


def test_a_validation_only_run_bundles_and_publishes_nothing(
    root: Path, tmp_path: Path
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n")
    destination = tmp_path / "bundle.md"
    run = invoke("-c", "-o", str(destination), "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.stdout == ""
    assert not destination.exists()


def test_a_validation_only_run_still_reports_a_bundle_it_cannot_build(
    root: Path,
) -> None:
    written(root, "deep.md", "## Lead\n\n###### Deep\n")
    written(root, "guide.md", "# Guide\n\nIt needs [the deep one](deep.md).\n")
    run = invoke("-c", "-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [HEADING_DEPTH_OVERFLOW]


def test_an_image_naming_a_markdown_document_carries_no_document(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee ![the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nThe rules.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "![the rules](rules.md)" in run.stdout
    assert "The rules." not in run.stdout


def test_an_image_naming_a_markdown_document_warns_once_on_portability(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee ![the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nThe rules.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    codes = [one["code"] for one in run.diagnostics()]
    assert codes.count(RESOURCE_PORTABILITY) == 1


def test_a_bundle_naming_no_resource_does_not_warn_on_portability(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the spec](https://e.test/s.pdf).\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert RESOURCE_PORTABILITY not in [one["code"] for one in run.diagnostics()]


def test_an_unmarked_image_is_emitted_as_authored(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee ![the architecture](plan.png).\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "![the architecture](plan.png)" in run.stdout


def test_an_unmarked_resource_is_emitted_as_authored(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the spec](https://e.test/s.md).\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "[the spec](https://e.test/s.md)" in run.stdout


def test_a_reference_under_the_root_is_bundled_and_rewritten(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "[the rules](#rules)" in run.stdout
    assert "Every rule." in run.stdout


def test_a_reference_to_a_section_under_the_root_carries_that_section(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the step](process.md#step).\n")
    written(root, "process.md", "# Process\n\n## Draft\n\nNo.\n\n## Step\n\nYes.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "[the step](#step)" in run.stdout
    assert "Yes." in run.stdout
    assert "No." not in run.stdout


def test_a_reference_outside_the_root_is_emitted_as_authored(tmp_path: Path) -> None:
    allowed = tmp_path / "source"
    allowed.mkdir()
    (tmp_path / "rules.md").write_text("# Rules\n\n<div>raw</div>\n")
    (allowed / "guide.md").write_text("# Guide\n\nSee [the rules](../rules.md).\n")
    run = invoke("guide.md", cwd=allowed)
    assert run.status == SUCCESS
    assert "[the rules](../rules.md)" in run.stdout
    assert "raw" not in run.stdout


def test_a_root_relative_reference_inside_a_source_is_emitted_as_authored(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the rules](/rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "[the rules](/rules.md)" in run.stdout
    assert "Every rule." not in run.stdout


def test_a_drive_path_inside_a_source_is_emitted_as_authored(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [the rules](C:/rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "[the rules](C:/rules.md)" in run.stdout
    assert "Every rule." not in run.stdout


def test_a_reference_under_the_root_naming_no_document_publishes_nothing(
    root: Path,
) -> None:
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    written(
        root,
        "guide.md",
        "# Guide\n\nSee [the rules](rules.md) and [the steps](procedure.md).\n",
    )
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["code"] == TARGET_NOT_FOUND
    assert run.diagnostics()[0]["reference"] == "procedure.md"
    assert run.stdout == ""


def test_a_reference_under_the_root_naming_no_heading_publishes_nothing(
    root: Path,
) -> None:
    written(root, "procedure.md", "# Procedure\n\n## Steps\n\nCarry each out.\n")
    written(root, "guide.md", "# Guide\n\nSee [the review](procedure.md#review).\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["code"] == TARGET_NOT_FOUND
    assert run.diagnostics()[0]["resolved"] == "procedure.md"
    assert run.stdout == ""


def test_a_marked_reference_under_the_root_is_not_compiled(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule the procedure requires.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "# Rules" not in run.stdout
    assert "Every rule the procedure requires." not in run.stdout


def test_a_deferred_link_publishes_its_text_without_the_mark(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "See [the rules](rules.md)." in run.stdout


@pytest.mark.parametrize(
    "written_as",
    ["[\u00acthe rules](rules.md)", "[\u00ac\tthe rules](rules.md)"],
)
def test_the_blanks_after_the_mark_go_with_it(root: Path, written_as: str) -> None:
    written(root, "guide.md", f"# Guide\n\nSee {written_as}.\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "See [the rules](rules.md)." in run.stdout


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
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "# Rules" in run.stdout
    assert "See [the rules](rules.md)" in run.stdout
    assert "It requires [the rules](#rules)" in run.stdout


def test_a_dispatched_reference_under_the_root_is_not_compiled(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u21c9 the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule the sub-agent requires.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "# Rules" not in run.stdout
    assert "Every rule the sub-agent requires." not in run.stdout


def test_a_dispatched_link_carries_the_mark_its_author_wrote(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u21c9 the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "See [\u21c9 the rules](rules.md)." in run.stdout


def test_a_link_opening_with_both_operators_is_refused(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nRead [\u00ac \u21c9 the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    diagnostic = run.diagnostics()[0]
    assert diagnostic["code"] == UNSUPPORTED_CONSTRUCT
    assert diagnostic["reference"] == "\u00ac \u21c9 the rules"


def test_a_link_opening_with_both_operators_is_refused_where_it_names_nothing(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nRead [\u21c9 \u00ac a picture](plan.png).\n")
    (root / "plan.png").write_text("Never opened.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["code"] == UNSUPPORTED_CONSTRUCT


@pytest.mark.parametrize("key", ["dispatch", "dispatched"])
def test_an_unknown_prosiform_key_fails(root: Path, key: str) -> None:
    written(
        root,
        "guide.md",
        f"---\nprosiform:\n  {key}: One rule.\n---\n# Guide\n",
    )
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.diagnostics()[0]["code"] == INVALID_CONVERSION_METADATA


def test_metadata_carries_no_conversion_meaning(root: Path) -> None:
    declaration = "---\nmetadata:\n  dispatch: One rule.\n---\n"
    written(
        root,
        "guide.md",
        f"{declaration}# Guide\n\nSee [\u21c9 rules](rules.md).\n",
    )
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "One rule." not in run.stdout


def test_a_deferred_fragment_of_its_own_document_is_not_compiled(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSee [\u00ac B](#beta).\n\n## Beta\n\nBody.\n",
    )
    run = invoke("guide.md#alpha", cwd=root)
    assert run.status == SUCCESS
    assert "See [B](guide.md#beta)." in run.stdout
    assert "Body." not in run.stdout


def test_a_deferred_reference_naming_no_document_fails(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md).\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [TARGET_NOT_FOUND]
    assert run.stdout == ""


def test_a_deferred_reference_naming_no_heading_fails(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md#absent).\n")
    written(root, "rules.md", "# Rules\n\n## Here\n\nEvery rule.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == TARGET_NOT_FOUND
    assert reported["reference"] == "rules.md#absent"
    assert reported["resolved"] == "rules.md"
    assert reported["chain"] == ["guide.md", "rules.md#absent"]
    assert run.stdout == ""


def test_a_deferred_destination_is_the_target_path_from_the_root(root: Path) -> None:
    written(
        root,
        "topic/guide.md",
        "# Guide\n\nSee [\u00ac the rules](../shared/rules.md#here).\n",
    )
    written(root, "shared/rules.md", "# Rules\n\n## Here\n\nEvery rule.\n")
    run = invoke("topic/guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "See [the rules](shared/rules.md#here)." in run.stdout


def test_a_document_only_a_deferral_names_contributes_nothing(root: Path) -> None:
    written(
        root,
        "topic/guide.md",
        "# Guide\n\nSee [\u00ac the rules](../shared/rules.md).\n",
    )
    written(root, "shared/rules.md", "# Rules\n\nEvery rule the guide defers.\n")
    run = invoke("topic/guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "# shared/rules" not in run.stdout
    assert "Every rule the guide defers." not in run.stdout


def test_a_heading_a_container_carries_confirms_a_deferral(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [\u00ac the rules](rules.md#inner).\n")
    written(root, "rules.md", "# Rules\n\n- item\n\n  ## Inner\n\n  Every rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "See [the rules](rules.md#inner)." in run.stdout


def test_a_link_to_the_section_carrying_it_resolves_to_that_section(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSee [A](guide.md#alpha).\n")
    run = invoke("guide.md#alpha", cwd=root)
    assert run.status == SUCCESS
    assert "See [A](#alpha)." in run.stdout
    assert run.stdout.count("### Alpha") == 1


def test_identity_is_compared_after_the_path_and_the_fragment_resolve(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSee [A](./%67uide.md#alpha).\n")
    run = invoke("guide.md#alpha", cwd=root)
    assert run.status == SUCCESS
    assert "See [A](#alpha)." in run.stdout


def test_a_preamble_link_to_its_own_document_resolves_to_that_document(
    root: Path,
) -> None:
    written(root, "guide.md", "See [the guide](guide.md).\n\n## Alpha\n\nBody.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "See [the guide](#guide)." in run.stdout


def test_a_section_link_to_its_whole_document_is_an_ancestor_inclusion(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSee [it](guide.md).\n")
    assert invoke("guide.md#alpha", cwd=root).status == SUCCESS


def test_a_link_to_another_section_of_one_file_is_no_self_reference(
    root: Path,
) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSee [B](guide.md#beta).\n\n## Beta\n\nBody.\n",
    )
    assert invoke("guide.md#alpha", cwd=root).status == SUCCESS


def test_classification_is_the_same_before_and_after_consolidation(
    root: Path,
) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nBody.\n\n### Detail\n\nSee [A](guide.md#alpha).\n",
    )
    child = invoke("guide.md#detail", cwd=root)
    consolidated = invoke("guide.md#alpha", cwd=root)
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
    run = invoke("guide.md", cwd=root)
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
        ("-F", "2"),
        ("-B", "16"),
        ("-I", "60"),
        ("-O", "64"),
        ("-T", "2"),
        ("-L", "1"),
        ("-E", "1"),
    ],
)
def test_a_crossed_budget_fails_the_run_and_names_the_option(
    root: Path, option: str, value: str
) -> None:
    chained(root)
    run = invoke("-d", "json", option, value, "alpha.md", cwd=root)
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RESOURCE_LIMIT
    assert option in reported["message"]
    assert run.stdout == ""


def test_a_crossed_nesting_budget_fails_rather_than_reinterpreting_the_source(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\n" + "> " * 12 + "The bottom.\n")
    run = invoke("-d", "json", "-N", "3", "guide.md", cwd=root)
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
    run = invoke("-d", "json", "-N", "3", "guide.md#alpha", cwd=root)
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RESOURCE_LIMIT
    assert reported["source"] == "guide.md"
    assert reported["reference"] == "guide.md"
    assert reported["chain"] == ["guide.md#alpha"]
    assert "cannot be safely indexed" in reported["message"]


def test_a_source_byte_budget_is_an_indexing_failure_too(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\n## Alpha\n\nSelected.\n")
    run = invoke("-d", "json", "-B", "8", "guide.md#alpha", cwd=root)
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RESOURCE_LIMIT
    assert reported["source"] == "guide.md"
    assert "cannot be safely indexed" in reported["message"]


def test_a_run_wide_budget_names_no_single_source(root: Path) -> None:
    chained(root)
    run = invoke("-d", "json", "-F", "2", "alpha.md", cwd=root)
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
    run = invoke("guide.md#alpha", cwd=root)
    assert run.status == SUCCESS
    assert "### Alpha" in run.stdout


def test_an_unselected_self_link_does_not_fail_the_run(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSelected.\n\n## Beta\n\nSee [¬ here](guide.md#beta).\n",
    )
    assert invoke("guide.md#alpha", cwd=root).status == SUCCESS


def test_the_same_sibling_fails_once_the_closure_includes_it(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Alpha\n\nSee [beta](guide.md#beta).\n\n"
        "## Beta\n\nSee [gone](missing.md).\n",
    )
    run = invoke("-d", "json", "guide.md#alpha", cwd=root)
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == TARGET_NOT_FOUND
    assert reported["reference"] == "missing.md"


def test_a_profile_refusal_a_named_document_did_not_select_does_not_fail(
    root: Path,
) -> None:
    scoped(root)
    assert invoke("guide.md#alpha", cwd=root).status == SUCCESS


def test_a_profile_refusal_a_reached_document_did_not_select_does_not_fail(
    root: Path,
) -> None:
    scoped(root)
    run = invoke("guide.md#alpha", cwd=root)
    assert run.status == SUCCESS
    assert "### Gamma" in run.stdout
    assert "Delta" not in run.stdout


def test_a_profile_refusal_the_run_selected_still_fails(root: Path) -> None:
    scoped(root)
    run = invoke("-d", "json", "guide.md#beta", cwd=root)
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RAW_HTML
    assert reported["chain"] == ["guide.md#beta"]


def test_a_refusal_in_a_reached_document_the_closure_selected_fails(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nSee [other](other.md).\n")
    written(root, "other.md", "# Other\n\n<div>raw</div>\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    reported = run.diagnostics()[0]
    assert reported["code"] == RAW_HTML
    assert reported["source"] == "other.md:3"
    assert reported["chain"] == ["guide.md", "other.md"]


def test_a_target_at_the_expansion_depth_is_bundled(root: Path) -> None:
    chained(root)
    run = invoke("-E", "2", "alpha.md", cwd=root)
    assert run.status == SUCCESS
    assert "# Gamma" in run.stdout


def test_a_crossed_budget_publishes_no_output_file(root: Path, tmp_path: Path) -> None:
    chained(root)
    destination = tmp_path / "bundle.md"
    run = invoke("-O", "64", "-o", str(destination), "alpha.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert not destination.exists()


@pytest.mark.parametrize("value", ["0", "-1", "1.5", "0x10", " 1", ""])
def test_a_budget_override_that_is_no_positive_decimal_integer_is_refused(
    root: Path, value: str
) -> None:
    run = invoke(f"-F={value}", "guide.md", cwd=root)
    assert run.status == USAGE_FAILURE


def test_a_budget_stands_at_the_number_the_profile_declares(root: Path) -> None:
    assert FILES.default == 256
    assert invoke("guide.md", cwd=root).status == SUCCESS


def test_a_candidate_disagreeing_with_its_provenance_publishes_nothing(
    root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    written(root, "guide.md", "# Guide\n\nBody.\n\nMore body.\n")
    destination = tmp_path / "bundle.md"
    assembling = assemble

    def dropping(groups: Sequence[Group]) -> str:
        return assembling(groups).replace("\n\nMore body.", "")

    monkeypatch.setattr("prosiform.cli.assemble", dropping)
    run = invoke("-d", "json", "-o", str(destination), "guide.md", cwd=root)
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
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert [(one["severity"], one["code"]) for one in run.diagnostics()] == [
        ("error", UNEXPECTED_INTERNAL_ERROR)
    ]


def test_an_error_the_contract_does_not_name_is_an_internal_error_as_text(
    root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("prosiform.cli.compose", unnamed)
    run = invoke("-d", "text", "guide.md", cwd=root)
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert run.stderr.splitlines() == [
        f"{UNEXPECTED_INTERNAL_ERROR}: unexpected internal error: "
        "RuntimeError('the composition reached a state the contract never names')"
    ]


def captured_for(root: Path, path: str) -> dict[str, Capture]:
    """What one source was when it was read, as discovery captures it."""
    return {
        path: read_document(
            root, entry(path), Limits({b: b.default for b in BUDGETS})
        ).capture
    }


def test_a_source_nothing_wrote_passes_the_recheck(root: Path) -> None:
    recheck(root, captured_for(root, "guide.md"))


def test_a_source_written_after_the_read_fails_the_recheck(root: Path) -> None:
    captured = captured_for(root, "guide.md")
    (root / "guide.md").write_text("# Guide\n\nA line the run never read.\n")
    with pytest.raises(Failure) as raised:
        recheck(root, captured)
    assert raised.value.diagnostic.code == SOURCE_CHANGED
    assert raised.value.status == INPUT_FAILURE


def test_a_source_removed_after_the_read_fails_the_recheck(root: Path) -> None:
    captured = captured_for(root, "guide.md")
    (root / "guide.md").unlink()
    with pytest.raises(Failure) as raised:
        recheck(root, captured)
    assert raised.value.diagnostic.code == SOURCE_CHANGED


def test_a_source_resolving_elsewhere_fails_the_recheck(tmp_path: Path) -> None:
    for name in ("one", "two"):
        (tmp_path / name).mkdir()
        (tmp_path / name / "guide.md").write_text("# Guide\n")
    (tmp_path / "one").rename(tmp_path / "now")
    root = tmp_path / "now"
    captured = captured_for(root, "guide.md")
    (tmp_path / "now").rename(tmp_path / "old")
    (tmp_path / "two").rename(tmp_path / "now")
    with pytest.raises(Failure) as raised:
        recheck(root, captured)
    assert raised.value.diagnostic.code == SOURCE_CHANGED
    assert "identity changed" in raised.value.diagnostic.message


def writing_once(root: Path, write: Callable[[Path], object]) -> Callable[..., bytes]:
    """A read that writes the source tree once, as a run's first read returns."""
    reads: list[str] = []

    def reading(at: Path, path: str, **kwargs: Any) -> bytes:
        data = read_source(at, path, **kwargs)
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
    run = invoke("-d", "json", "-o", str(output), "guide.md", cwd=root)
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
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_CHANGED]


def test_a_title_the_allowed_source_root_cannot_contain_names_no_document(
    root: Path,
) -> None:
    (root.parent / "outside.md").write_text("# Outside\n")
    (root / "titled.md").write_text("# ../outside\n\nBody.\n")
    run = invoke("-d", "json", "titled.md", cwd=root)
    assert run.status == SUCCESS
    assert run.diagnostics() == []


def test_an_unsafe_boundary_is_an_input_failure(tmp_path: Path) -> None:
    (tmp_path / "guide.md").write_text(
        "# Guide\n\n- The first list.\n\n[notes]: notes.md\n\n- The second list.\n"
    )
    run = invoke("-d", "json", "guide.md", cwd=tmp_path)
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
    run = invoke("-d", "json", "-o", str(destination), "guide.md", cwd=source)
    assert run.status == INPUT_FAILURE
    assert not destination.exists()


def surrounded(brackets: int) -> str:
    """One source whose dependency sits under a run of open brackets."""
    return f"# Guide\n\nThe guide cites {'[' * brackets}the plan](plan.md).\n"


def test_a_lookup_the_parser_declines_fails_the_run(root: Path) -> None:
    written(root, "guide.md", surrounded(1 + HEADROOM + 1))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke("-d", "json", "-N", "1", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == PARSER_REFERENCE_LIMIT
    assert reported["source"] == "guide.md:3"
    assert reported["chain"] == ["guide.md"]


def test_a_ceiling_reached_by_the_last_valid_reference_bundles_it(root: Path) -> None:
    written(root, "guide.md", surrounded(1 + HEADROOM))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke("-d", "json", "-N", "1", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "The plan." in run.stdout
    assert run.diagnostics() == []


def test_the_source_changed_fault_fails_the_run_and_publishes_nothing(
    root: Path, tmp_path: Path
) -> None:
    """The fault writes to the tree, and the run's own recheck is what fails it."""
    output = tmp_path / "bundle.md"
    run = invoke(
        "-d", "json", "-x", "source-changed", "-o", str(output), "guide.md", cwd=root
    )
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [SOURCE_CHANGED]
    assert not output.exists()
    assert (root / "guide.md").read_bytes() != b"# Guide\n"


def test_the_internal_fault_names_the_run_and_publishes_nothing(root: Path) -> None:
    run = invoke("-d", "json", "-x", "internal", "guide.md", cwd=root)
    assert run.status == INTERNAL_ERROR
    assert run.stdout == ""
    assert [one["code"] for one in run.diagnostics()] == [UNEXPECTED_INTERNAL_ERROR]


def test_a_run_asking_for_no_fault_meets_none(root: Path) -> None:
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert (root / "guide.md").read_bytes() == b"# Guide\n"


def test_a_fault_the_contract_does_not_declare_is_a_usage_failure(root: Path) -> None:
    run = invoke("-d", "json", "-x", "other", "guide.md", cwd=root)
    assert run.status == USAGE_FAILURE
    assert [one["code"] for one in run.diagnostics()] == [INVALID_USAGE]


def test_a_declined_lookup_names_the_reference_under_the_default_budgets(
    root: Path,
) -> None:
    written(root, "guide.md", surrounded(NESTING.default + HEADROOM + 1))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    reported = run.diagnostics()[0]
    assert reported["code"] == PARSER_REFERENCE_LIMIT
    assert reported["reference"] == "plan.md"
    assert reported["source"] == "guide.md:3"


def test_a_budget_spent_on_the_last_valid_reference_bundles_it(root: Path) -> None:
    written(root, "guide.md", surrounded(NESTING.default + HEADROOM))
    written(root, "plan.md", "# Plan\n\nThe plan.\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "The plan." in run.stdout
    assert PARSER_REFERENCE_LIMIT not in run.stderr


def dispatching(root: Path, names: Sequence[str]) -> None:
    """A chain of documents, each dispatching the next."""
    for name, following in zip(names, names[1:], strict=False):
        written(root, name, f"# {name}\n\nRun [\u21c9 next]({following}).\n")
    written(root, names[-1], f"# {names[-1]}\n\nDone.\n")


def test_a_chain_of_three_dispatches_raises_no_warning(root: Path) -> None:
    dispatching(root, ["guide.md", "a.md", "b.md", "c.md"])
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.diagnostics() == []


def test_a_fourth_dispatch_warns_naming_the_chain(root: Path) -> None:
    dispatching(root, ["guide.md", "a.md", "b.md", "c.md", "d.md"])
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "Run [⇉ next](a.md)." in run.stdout
    [warning] = run.diagnostics()
    assert warning["code"] == DISPATCH_DEPTH
    assert warning["severity"] == "warning"
    assert warning["chain"] == ["guide.md", "a.md", "b.md", "c.md", "d.md"]
    assert warning["location"] == {"file": "guide.md", "line": 3, "column": 1}
    assert [(one["file"], one["line"]) for one in warning["related"]] == [
        ("a.md", 3),
        ("b.md", 3),
        ("c.md", 3),
    ]


def test_a_dispatched_section_of_the_entry_is_a_hop(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\nRun [⇉ Run](#run).\n\n## Run\n\nStart [⇉ a](a.md).\n",
    )
    dispatching(root, ["a.md", "b.md", "c.md"])
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    [warning] = run.diagnostics()
    assert warning["code"] == DISPATCH_DEPTH
    assert warning["chain"] == ["guide.md", "guide.md#run", "a.md", "b.md", "c.md"]


def test_a_deferred_link_in_a_dispatched_closure_is_no_hop(root: Path) -> None:
    dispatching(root, ["guide.md", "a.md", "b.md", "c.md"])
    written(root, "c.md", "# c.md\n\nLater [¬ d](d.md).\n")
    written(root, "d.md", "# d.md\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.diagnostics() == []


def test_a_dispatch_a_compiled_dependency_carries_is_a_hop(root: Path) -> None:
    dispatching(root, ["guide.md", "a.md", "b.md", "c.md"])
    written(root, "c.md", "# c.md\n\nSee [shared](shared.md).\n")
    written(root, "shared.md", "# Shared\n\nRun [⇉ d](d.md).\n")
    written(root, "d.md", "# d.md\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert [one["code"] for one in run.diagnostics()] == [DISPATCH_DEPTH]


def test_a_cycle_of_dispatches_warns_and_terminates(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nRun [⇉ a](a.md).\n")
    written(root, "a.md", "# A\n\nRun [⇉ b](b.md).\n")
    written(root, "b.md", "# B\n\nRun [⇉ a](a.md).\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    [warning] = run.diagnostics()
    assert warning["code"] == DISPATCH_CYCLE
    assert warning["chain"] == ["guide.md", "a.md", "b.md", "a.md"]


def test_a_section_dispatching_its_own_document_is_a_cycle(root: Path) -> None:
    written(
        root,
        "guide.md",
        "# Guide\n\n## Run\n\nAgain [⇉ the guide](guide.md).\n",
    )
    run = invoke("-d", "json", "guide.md#run", cwd=root)
    assert run.status == SUCCESS
    [warning] = run.diagnostics()
    assert warning["code"] == DISPATCH_CYCLE
    assert warning["chain"] == ["guide.md#run", "guide.md", "guide.md"]


def test_a_dispatched_target_whose_compilation_fails_carries_no_hop(
    root: Path,
) -> None:
    written(root, "guide.md", "# Guide\n\nRun [⇉ a](a.md).\n")
    written(root, "a.md", "# A\n\nSee [gone](gone.md).\n")
    run = invoke("-d", "json", "guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.diagnostics() == []


def test_a_dispatch_warning_reads_as_text(root: Path) -> None:
    dispatching(root, ["guide.md", "a.md", "b.md", "c.md", "d.md"])
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert run.stderr.startswith(f"{DISPATCH_DEPTH}: ")
    assert "  chain: guide.md → a.md → b.md → c.md → d.md\n" in run.stderr
    assert "  related: c.md:3:1: dispatches 'd.md'" in run.stderr


def test_a_link_opening_with_a_guillemet_is_compiled(root: Path) -> None:
    written(root, "guide.md", "# Guide\n\nSee [» the rules](rules.md).\n")
    written(root, "rules.md", "# Rules\n\nEvery rule.\n")
    run = invoke("guide.md", cwd=root)
    assert run.status == SUCCESS
    assert "Every rule." in run.stdout


@pytest.mark.parametrize("mark", ["\u00ac", "\u21c9"])
@pytest.mark.parametrize(
    "use",
    [
        "[{mark} the spec](https://e.test/s.md)",
        "[{mark} the diagram](plan.png)",
        "![{mark} the architecture](plan.png)",
        "[{mark} the rules](../outside.md)",
    ],
)
def test_an_operator_naming_no_document_under_the_root_is_refused(
    tmp_path: Path, mark: str, use: str
) -> None:
    allowed = tmp_path / "source"
    allowed.mkdir()
    (tmp_path / "outside.md").write_text("# Outside\n")
    (allowed / "plan.png").write_text("Never opened.\n")
    written(allowed, "guide.md", f"# Guide\n\nSee {use.format(mark=mark)}.\n")
    run = invoke("-d", "json", "guide.md", cwd=allowed)
    assert run.status == INPUT_FAILURE
    assert run.stdout == ""
    [diagnostic] = run.diagnostics()
    assert diagnostic["code"] == UNSUPPORTED_CONSTRUCT
    assert diagnostic["source"] == "guide.md:3"
