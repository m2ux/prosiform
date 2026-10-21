"""Assert the documentation check holds the documented invocation to the command.

The check exists so documentation and command cannot drift apart, so the
cases below drift them: a row the command does not offer, an argument the
command offers that no row names, a row whose wording has moved away from
the help text, an exit status meaning that no longer matches, a profile
identifier the guide stopped naming, and a statement the contract
requires that the guide stopped carrying. Each is one fault and is
named as the fault it is.

The build under test is a canned program each case configures, as in the
runner's own tests, and the documentation is written beside it. The pair
starts as a document generated from that program's own help output, so a
passing case is the agreement itself rather than a document written to
agree. A configured build is the one thing the check cannot do without: a
run with none fails rather than reporting documentation it never compared.

The repository's own invocation guide is read too, for the one property a canned
document cannot show — that the tables the check looks for are the tables
the invocation guide carries. What those tables say is held to the installed
command by `make invocation`, which runs the whole check against the build
the gate configures.
"""

import shlex
from pathlib import Path

import pytest
from documents import tables
from invocation import (
    EXIT,
    INVOCATION,
    OPTION,
    STATEMENTS,
    Unreadable,
    check,
    documented_arguments,
    documented_statuses,
)
from runner import BUILD, BuildNotConfigured

HELP = """usage: tool --root DIR [OPTIONS] REF [REF ...]

Bundle the local Markdown closure of one or more entry references into one
validated document.

positional arguments:
  REF                   an entry reference: a root-relative document, a
                        document and a fragment, or a fragment alone with
                        --from

options:
  --root DIR            the allowed source root; required, and resolved from
                        the working directory
  -o, --output FILE     publish the validated bundle to FILE, atomically;
                        default or - is standard output
  --diagnostics {text,json}
                        the diagnostic format on standard error; default text
  --help                show this usage, the defaults, and the exit-status
                        meanings

exit statuses:
  0  successful compilation, validation, or informational response
  2  invalid usage or option combination
"""

VERSION = "tool 0.1.0 (skill-markdown-v1)\n"

PROFILE = "skill-markdown-v1"


def canned(directory: Path) -> str:
    """A build replaying one help output and one version line, and nothing else."""
    help_text = directory / "help"
    version_text = directory / "version"
    help_text.write_text(HELP, encoding="utf-8")
    version_text.write_text(VERSION, encoding="utf-8")
    script = (
        'case "$1" in '
        f"--help) cat {shlex.quote(str(help_text))} ;; "
        f"--version) cat {shlex.quote(str(version_text))} ;; "
        "*) exit 2 ;; "
        "esac"
    )
    return shlex.join(["/bin/sh", "-c", script, "tool"])


def documentation() -> str:
    """An invocation guide agreeing with every compared part of the canned help."""
    lines = [
        "# tool",
        "",
        "# Invocation",
        "",
        f"A run parses its sources under the `{PROFILE}` profile.",
        "",
        "| Option | Effect |",
        "| --- | --- |",
    ]
    for argument in documented_arguments(HELP):
        lines.append(f"| `{argument.invocation}` | {argument.effect} |")
    lines += ["", "| Exit | Meaning |", "| --- | --- |"]
    for status, meaning in documented_statuses(HELP):
        lines.append(f"| `{status}` | {meaning} |")
    lines += ["", "### What the documented invocation states", ""]
    lines += [sentence for _, sentence in STATEMENTS]
    return "\n".join(lines) + "\n"


@pytest.fixture
def documented(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """The canned build configured and its agreeing documentation in place."""
    monkeypatch.setenv(BUILD, canned(tmp_path))
    usage = tmp_path / "invocation.md"
    usage.write_text(documentation(), encoding="utf-8")
    monkeypatch.setattr("invocation.INVOCATION", usage)
    return usage


def faults(usage: Path, find: str, replacement: str = "") -> list[str]:
    """The faults the check reports once one place of the documentation moves."""
    text = usage.read_text()
    assert find in text, f"the documentation carries no {find!r} to move"
    usage.write_text(text.replace(find, replacement), encoding="utf-8")
    return check()[1]


def test_documentation_generated_from_the_help_output_passes(documented: Path) -> None:
    passed, failures = check()
    assert failures == []
    assert passed


def test_every_compared_surface_is_reported_as_passing(documented: Path) -> None:
    passed, _ = check()
    assert len([line for line in passed if " option " in line]) == 5
    assert len([line for line in passed if " status " in line]) == 2
    assert len([line for line in passed if " profile " in line]) == 1
    assert len([line for line in passed if " statement " in line]) == len(STATEMENTS)


def test_a_documented_option_the_command_does_not_expose_fails(
    documented: Path,
) -> None:
    row = (
        "| `--root DIR` | the allowed source root; required, and resolved from "
        "the working directory |"
    )
    invented = "| `--depth N` | how deep a run follows a link |"
    reported = faults(documented, row, f"{row}\n{invented}")
    assert any("--depth N" in fault and "no such option" in fault for fault in reported)


def test_an_option_the_command_exposes_and_no_table_names_fails(
    documented: Path,
) -> None:
    row = (
        "| `--diagnostics {text,json}` | the diagnostic format on standard "
        "error; default text |\n"
    )
    reported = faults(documented, row)
    assert any(
        "--diagnostics {text,json}" in fault and "no table names it" in fault
        for fault in reported
    )


def test_a_row_whose_wording_left_the_help_text_fails(documented: Path) -> None:
    reported = faults(
        documented, "default or - is standard output", "default - is standard output"
    )
    assert any(
        "-o, --output FILE" in fault and "the command's help reads" in fault
        for fault in reported
    )


def test_an_exit_status_meaning_that_no_longer_matches_fails(
    documented: Path,
) -> None:
    reported = faults(
        documented, "invalid usage or option combination", "Invalid usage"
    )
    assert any("the command's help reads" in fault for fault in reported)


def test_a_guide_that_stopped_naming_the_profile_fails(documented: Path) -> None:
    reported = faults(documented, f"the `{PROFILE}`", "the declared")
    assert any(PROFILE in fault and "names it nowhere" in fault for fault in reported)


@pytest.mark.parametrize(("states", "sentence"), STATEMENTS)
def test_a_statement_the_guide_stopped_carrying_fails(
    documented: Path, states: str, sentence: str
) -> None:
    reported = faults(documented, sentence)
    assert any(states in fault for fault in reported)


def test_a_run_with_no_build_configured_fails(
    documented: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv(BUILD, raising=False)
    with pytest.raises(BuildNotConfigured):
        check()


def test_a_build_whose_help_describes_no_argument_fails(
    documented: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(BUILD, "/bin/true")
    with pytest.raises(Unreadable):
        check()


def test_the_repository_carries_the_tables_the_check_compares() -> None:
    carried = tables(INVOCATION.read_text())
    assert [table for table in carried if OPTION in table.headers]
    assert [table for table in carried if EXIT in table.headers]
