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
        "prosiform: {}",
        "metadata: {owner: yes}",
        "metadata: {date: 2026-10-23, binary: 0b10, underscored: 1_000}",
    ],
)
def test_absent_settings(text: str) -> None:
    assert parse(text) == Conversion()


def test_group_and_marks() -> None:
    result = parse(
        'prosiform:\r\n  group: " règles "\r\n  group-depth: 2\r\n',
        prefix="\ufeff---\r\n",
    )
    assert result.group == " règles "
    assert result.depth == 2
    assert result.group_location == Location("rules/a.md", 3, 10)
    assert result.depth_location == Location("rules/a.md", 4, 16)
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
        "prosiform: null",
        "prosiform: []",
        "prosiform: x",
        "prosiform: {1: x}",
        "prosiform: {owner: true}",
        "prosiform: {prosiform-unknown: x}",
        "prosiform: {group: rules}",
        "prosiform: {group-depth: 2}",
        'prosiform: {group: rules, group-depth: "2"}',
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
        parse("prosiform: {group: " + json.dumps(group) + ", group-depth: 2}")


@pytest.mark.parametrize("depth", ["0", "7", "22", "٢", "2.0", " 2"])
def test_depth_grammar(depth: str) -> None:
    with pytest.raises(InvalidMetadata):
        parse("prosiform: {group: rules, group-depth: " + json.dumps(depth) + "}")


@pytest.mark.parametrize("depth", range(1, 7))
def test_depth_values(depth: int) -> None:
    assert parse(f"prosiform: {{group: rules, group-depth: {depth}}}").depth == depth


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
        parse('prosiform: {group: "x", prosiform-bad: "x"}')
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, 25)
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
        parse('prosiform: {group: "\t", prosiform-bad: x}')
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, 25)


def test_yaml_marked_syntax_error() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("a: [\n}")
    assert caught.value.diagnostic.location == Location("rules/a.md", 3, 1)


def test_single_line_bom_coordinate() -> None:
    raw = "\ufeffprosiform: {prosiform-bad: x}".encode()
    with pytest.raises(InvalidMetadata) as caught:
        decode(raw, file="a", span=(3, len(raw)), max_bytes=len(raw), max_depth=2)
    assert caught.value.diagnostic.location == Location("a", 1, 14)


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


@pytest.mark.parametrize(
    "root",
    [".", "..", "../library", "a/../b", "rules/", " règles ", " ", "a%20b", "a#b?c"],
)
def test_root_declaration_preserves_value_and_location(root: str) -> None:
    result = parse("prosiform:\r\n  root: " + json.dumps(root), prefix="\ufeff---\r\n")
    assert result.root == root
    assert result.root_location == Location("rules/a.md", 3, 9)
    assert result.group is None
    assert result.depth is None
    with pytest.raises(FrozenInstanceError):
        result.root = "other"  # type: ignore[misc]


@pytest.mark.parametrize(
    "root",
    [
        "",
        "/tmp",
        "//host/share",
        "C:/rules",
        "C:rules",
        "https://host/rules",
        "file:rules",
        "~",
        "~/rules",
        "~user/rules",
        "$HOME/rules",
        "${HOME}/rules",
        "%HOME%/rules",
        "a\\b",
        "a\0b",
        "a\nb",
        "a\tb",
        "a\x7fb",
        "a\u0085b",
    ],
)
def test_invalid_root_declaration(root: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform:\r\n  root: " + json.dumps(root), prefix="\ufeff---\r\n")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert caught.value.diagnostic.location == Location("rules/a.md", 3, 9)


@pytest.mark.parametrize("field", ["root", "group"])
@pytest.mark.parametrize("value", ["null", "true", "2", "2.0", "[]", "{}"])
def test_string_fields_reject_other_core_types(field: str, value: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(f"prosiform: {{{field}: {value}, group-depth: 2}}")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


@pytest.mark.parametrize(
    "depth", ["true", "false", "null", "[]", "{}", "0", "7", "-1", "2.0", "2e0", "'2'"]
)
def test_integer_depth_schema(depth: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(f"prosiform: {{group: rules, group-depth: {depth}}}")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


@pytest.mark.parametrize("depth", ["+2", "02", "0x2", "0o2", "!!int 2"])
def test_core_integer_depth(depth: str) -> None:
    assert parse(f"prosiform: {{group: rules, group-depth: {depth}}}").depth == 2


def test_root_is_independent_of_group_pair() -> None:
    result = parse("prosiform: {root: .., group: rules, group-depth: 2}")
    assert (result.root, result.group, result.depth) == ("..", "rules", 2)
    for declaration in ("group: rules", "group-depth: 2"):
        with pytest.raises(InvalidMetadata):
            parse(f"prosiform: {{root: .., {declaration}}}")
    assert parse("prosiform: {group: rules, group-depth: 2}").root is None


@pytest.mark.parametrize(
    "text",
    [
        "metadata: null",
        "metadata: [true, {1: [2]}]",
        'metadata: {prosiform-group: rules, prosiform-group-depth: "2"}',
        "metadata: {root: .., group: rules, group-depth: 2}",
        "root: ..\ngroup: rules\ngroup-depth: 2",
    ],
)
def test_unreserved_fields_have_no_conversion_meaning(text: str) -> None:
    assert parse(text) == Conversion()


@pytest.mark.parametrize(
    "key",
    ["prosiform-group", "prosiform-group-depth", "version", "r", "depth", "unknown"],
)
def test_reserved_mapping_has_exact_keys(key: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(f"prosiform: {{{key}: x}}")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


def test_group_heading_false_is_recorded() -> None:
    found = parse("prosiform: {group: artifacts, group-depth: 2, group-heading: false}")
    assert found.heading is False


def test_an_absent_group_heading_means_the_heading_is_present() -> None:
    assert parse("prosiform: {group: artifacts, group-depth: 2}").heading is None


def test_group_heading_requires_the_group_fields() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform: {group-heading: false}")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


def test_root_mapping_nesting_budget() -> None:
    assert parse("prosiform: {root: ..}", depth=2).root == ".."
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform: {root: ..}", depth=1)
    assert caught.value.diagnostic.code == "E_RESOURCE_LIMIT"


def test_a_dispatch_text_is_recorded_with_its_location() -> None:
    found = parse('prosiform:\n  dispatch: "Each mark is the sub-agent\'s."\n')
    assert found.dispatch == "Each mark is the sub-agent's."
    assert found.dispatch_location == Location("rules/a.md", 3, 13)


@pytest.mark.parametrize(
    "text",
    [
        "prosiform: {dispatch: 2}",
        "prosiform: {dispatch: null}",
        "prosiform: {dispatch: true}",
        "prosiform: {dispatch: []}",
        "prosiform: {dispatch: {}}",
    ],
)
def test_a_dispatch_text_is_a_string(text: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(text)
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


@pytest.mark.parametrize(
    "dispatch",
    ["", "   ", "\t", "two\nlines", "a: b", "a/b", "a\x7fb", "a\u0085b", "a\u2028b"],
)
def test_a_dispatch_text_is_printable_single_line_and_nonblank(dispatch: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform: {dispatch: " + json.dumps(dispatch) + "}")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


def test_a_dispatch_text_is_independent_of_the_group_pair() -> None:
    found = parse("prosiform: {group: rules, group-depth: 2, dispatch: One rule.}")
    assert (found.group, found.dispatch) == ("rules", "One rule.")
    assert parse("prosiform: {dispatch: One rule.}").group is None


def test_an_absent_dispatch_text_is_no_declaration() -> None:
    assert parse("prosiform: {root: ..}").dispatch is None
    assert parse("prosiform: {root: ..}").dispatch_location is None


def test_an_unknown_key_still_fails_beside_an_admitted_dispatch_text() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform: {dispatch: One rule., dispatched: x}")
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"


def test_metadata_has_no_conversion_meaning_beside_a_dispatch_text() -> None:
    assert parse("metadata: {dispatch: One rule.}") == Conversion()
    assert (
        parse("prosiform: {dispatch: One rule.}\nmetadata: {dispatch: Other.}").dispatch
        == "One rule."
    )
