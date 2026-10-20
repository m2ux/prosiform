"""Assert a diagnostic carries the contract's fields and renders both ways.

The record is one shape and the two renderings read it. Text writes a
heading and one line per further field, so a reader sees the code and the
message first; JSON writes the same fields as data, one object on one
line, so a caller parses standard error without separating records from
prose.

A chain is the one field that is a sequence rather than a value. JSON
carries it as the list it is, because a caller reading a route wants its
hops; text writes those hops along one line, because a reader reads a
diagnostic as lines of a field apiece.

A field a diagnostic does not carry is absent from both renderings, which
is what makes an absent field a statement that the defect has no value
for it.
"""

import json
from io import StringIO

from prosiform.diagnostics import ERROR, JSON, TEXT, WARNING, Diagnostic, Reporter

REACHED = ("entry.md", "docs/notes.md#detail", "docs/other.md#nowhere")


def reaching() -> Diagnostic:
    """One failure reached through two references, carrying every field."""
    return Diagnostic(
        ERROR,
        "the reference 'other.md#nowhere' names no heading of the document",
        code="E_TARGET_NOT_FOUND",
        reference="other.md#nowhere",
        resolved="docs/other.md",
        source="docs/notes.md:5",
        chain=REACHED,
        remedy="name a heading the document carries",
    )


def test_a_diagnostic_carries_only_the_fields_it_was_given() -> None:
    carried = Diagnostic(ERROR, "no root", code="E_ROOT_NOT_FOUND").fields()
    assert set(carried) == {"severity", "message", "code"}


def test_the_fields_are_ordered_as_the_contract_names_them() -> None:
    assert list(reaching().fields()) == [
        "severity",
        "message",
        "code",
        "reference",
        "resolved",
        "source",
        "chain",
        "remedy",
    ]


def test_json_carries_the_chain_as_the_sequence_of_hops_it_is() -> None:
    assert json.loads(reaching().as_json())["chain"] == list(REACHED)


def test_text_writes_the_chain_hop_by_hop_on_one_line() -> None:
    written = reaching().as_text().splitlines()
    assert written[0].startswith("E_TARGET_NOT_FOUND: ")
    assert "  chain: entry.md → docs/notes.md#detail → docs/other.md#nowhere" in written


def test_a_diagnostic_reaching_nothing_renders_no_chain() -> None:
    bare = Diagnostic(WARNING, "a resource", code="W_RESOURCE_PORTABILITY")
    assert "chain" not in json.loads(bare.as_json())
    assert "chain" not in bare.as_text()


def test_each_json_diagnostic_is_one_line_of_its_own() -> None:
    stream = StringIO()
    reporter = Reporter(stream, JSON)
    reporter.emit(reaching())
    reporter.emit(Diagnostic(WARNING, "a resource", code="W_RESOURCE_PORTABILITY"))
    lines = stream.getvalue().splitlines()
    assert len(lines) == 2
    assert [json.loads(line)["code"] for line in lines] == [
        "E_TARGET_NOT_FOUND",
        "W_RESOURCE_PORTABILITY",
    ]


def test_the_format_the_run_chose_decides_every_diagnostic() -> None:
    stream = StringIO()
    Reporter(stream, TEXT).emit(reaching())
    assert stream.getvalue().startswith("E_TARGET_NOT_FOUND: ")
