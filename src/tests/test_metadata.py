"""YAML schema, bounds and original-coordinate invariants."""

import json
from dataclasses import FrozenInstanceError

import pytest

from prosiform.diagnostics import Location
from prosiform.metadata import (
    Conversion,
    InvalidMetadata,
    decode,
)


def parse(text: str, *, depth: int = 64, prefix: str = "---\n") -> Conversion:
    before = prefix.encode()
    payload = text.encode()
    raw = before + payload + b"\n---\nbody"
    return decode(
        raw,
        file="rules/a.md",
        span=(len(before), len(before) + len(payload)),
        max_bytes=len(raw),
        max_depth=depth,
    )


@pytest.mark.parametrize(
    "text",
    [
        "",
        "# comment\n",
        "{}",
        "name: test",
        "metadata: {}",
        "metadata: {owner: yes}",
        "metadata: {date: 2026-10-23, binary: 0b10, underscored: 1_000}",
    ],
)
def test_absent_settings(text: str) -> None:
    assert parse(text) == Conversion()


def test_group_and_marks() -> None:
    result = parse(
        'metadata:\r\n  prosiform-group: " règles "\r\n'
        '  prosiform-group-depth: "2"\r\n',
        prefix="\ufeff---\r\n",
    )
    assert result.group == " règles "
    assert result.depth == 2
    assert result.group_location == Location("rules/a.md", 3, 20)
    assert result.depth_location == Location("rules/a.md", 4, 26)
    with pytest.raises(FrozenInstanceError):
        result.group = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    "text",
    [
        "null",
        "[]",
        "hello",
        "1: value",
        "a: [",
        "a: !custom x",
        "a: !!int wrong",
        "a: !!seq {}",
        "a: !!map []",
        "a: !!timestamp 2020-01-01",
        "a: &a value\nb: *a",
        "a: {<<: {x: y}}",
        'a: {"<<": x}',
        "%YAML 1.1\n---\na: yes",
        "a: x\n---\nb: y",
        "a: x\na: y",
        "a: {x: 1, x: 2}",
        "a: {0x10: x, 16: y}",
        "a: {.NaN: x, .nan: y}",
        "a: {1.0: x, 1e0: y}",
        "a: {012: x, 12: y}",
        "a: {? [x, y]: one, ? [x, y]: two}",
        "a: {? {x: 1, y: 2}: one, ? {y: 2, x: 1}: two}",
    ],
)
def test_frontmatter_failures(text: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(text)
    assert caught.value.diagnostic.code == "E_INVALID_FRONTMATTER"


@pytest.mark.parametrize(
    "text",
    [
        "metadata: null",
        "metadata: []",
        "metadata: x",
        "metadata: {1: x}",
        "metadata: {owner: true}",
        "metadata: {prosiform-unknown: x}",
        "metadata: {prosiform-group: rules}",
        'metadata: {prosiform-group-depth: "2"}',
        "metadata: {prosiform-group: rules, prosiform-group-depth: 2}",
    ],
)
def test_schema_failures(text: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(text)
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


@pytest.mark.parametrize(
    "group",
    [
        "",
        " ",
        "a:b",
        "a/b",
        "a\nb",
        "a\tb",
        "a\u0085b",
        "a\u2028b",
        "a\u2029b",
        "a\x7fb",
    ],
)
def test_group_grammar(group: str) -> None:
    with pytest.raises(InvalidMetadata):
        parse(
            "metadata: {prosiform-group: "
            + json.dumps(group)
            + ', prosiform-group-depth: "2"}'
        )


@pytest.mark.parametrize("depth", ["0", "7", "22", "٢", "2.0", " 2"])
def test_depth_grammar(depth: str) -> None:
    with pytest.raises(InvalidMetadata):
        parse(
            "metadata: {prosiform-group: rules, prosiform-group-depth: "
            + json.dumps(depth)
            + "}"
        )


@pytest.mark.parametrize("depth", range(1, 7))
def test_depth_values(depth: int) -> None:
    assert (
        parse(
            f'metadata: {{prosiform-group: rules, prosiform-group-depth: "{depth}"}}'
        ).depth
        == depth
    )


def test_core_key_types_are_distinct() -> None:
    assert (
        parse("other: {false: a, 0: b, 0.0: c, '0': d, null: e, [x]: f}")
        == Conversion()
    )


def test_byte_limit_precedes_decoding() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        decode(b"\xff", file="a", span=(0, 1), max_bytes=0, max_depth=1)
    assert caught.value.diagnostic.code == "E_RESOURCE_LIMIT"
    assert (
        decode(b"body", file="a", span=None, max_bytes=4, max_depth=1) == Conversion()
    )


def test_depth_boundary_and_early_stop() -> None:
    assert parse("a: [[x]]", depth=3) == Conversion()
    with pytest.raises(InvalidMetadata) as caught:
        parse("a: [[x]]", depth=2)
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, 5)
    assert caught.value.diagnostic.code == "E_RESOURCE_LIMIT"
    with pytest.raises(InvalidMetadata):
        parse("a: " + "[" * 10000, depth=64)


def test_duplicate_diagnostic_formats() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("é: first\r\né: second", prefix="\ufeff---\r\n")
    diagnostic = caught.value.diagnostic
    assert diagnostic.location == Location("rules/a.md", 3, 1)
    payload = json.loads(diagnostic.as_json())
    assert payload["related"] == [
        {
            "file": "rules/a.md",
            "line": 2,
            "column": 1,
            "message": "first key occurrence",
        }
    ]
    assert "rules/a.md:3:1" in diagnostic.as_text()
    assert "rules/a.md:2:1" in diagnostic.as_text()


def test_error_marks_and_no_related() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse('metadata: {é: "x", prosiform-bad: "x"}')
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, 20)
    assert "related" not in caught.value.diagnostic.fields()


def test_large_integer() -> None:
    assert parse("other: " + "9" * 5000) == Conversion()


@pytest.mark.parametrize(
    "first,second",
    [
        ("-0.0", "0e999"),
        ("1.2300", "123e-2"),
        ("1e" + "9" * 5000, "1.0e" + "9" * 5000),
        ("0x" + "f" * 5000, "0x" + "F" * 5000),
    ],
)
def test_extreme_canonical_duplicates(first: str, second: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(f"other:\n  ? {first}\n  : x\n  ? {second}\n  : y")
    assert "duplicate" in str(caught.value)


def test_tab_and_unicode_column() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse('metadata: {é: "\t", prosiform-bad: x}')
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, 20)


def test_yaml_marked_syntax_error() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("a: [\n}")
    assert caught.value.diagnostic.location == Location("rules/a.md", 3, 1)


def test_single_line_bom_coordinate() -> None:
    raw = "\ufeffmetadata: {prosiform-bad: x}".encode()
    with pytest.raises(InvalidMetadata) as caught:
        decode(raw, file="a", span=(3, len(raw)), max_bytes=len(raw), max_depth=2)
    assert caught.value.diagnostic.location == Location("a", 1, 13)


def test_reader_error_coordinate() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("name: fine\r\nvalue: \x01", prefix="\ufeff---\r\n")
    assert caught.value.diagnostic.location == Location("rules/a.md", 3, 8)


@pytest.mark.parametrize("payload", [r'other: "\U00110000"', r'other: "\uD800"'])
def test_invalid_unicode_escape(payload: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(payload)
    assert caught.value.diagnostic.code == "E_INVALID_FRONTMATTER"
    assert caught.value.diagnostic.location is not None
    assert caught.value.diagnostic.location.line == 2


def test_escaped_null_in_unrelated_field() -> None:
    assert parse(r'other: "\0"') == Conversion()


def test_out_of_range_escape_mark_survives_parser_cleanup() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(r'other: "\U00110000"')
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, 11)
