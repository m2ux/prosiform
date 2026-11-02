"""YAML schema, bounds and original-coordinate invariants."""

import json
import time
from dataclasses import FrozenInstanceError

import pytest

from prosiform.diagnostics import Location
from prosiform.limits import FILE_BYTES, SCALAR_DIGITS
from prosiform.metadata import (
    Conversion,
    InvalidMetadata,
    Membership,
    Preset,
    Subst,
    decode,
)


def parse(
    text: str,
    *,
    depth: int = 64,
    prefix: str = "---\n",
    max_bytes: int | None = None,
) -> Conversion:
    before = prefix.encode()
    payload = text.encode()
    raw = before + payload + b"\n---\nbody"
    return decode(
        raw,
        file="rules/a.md",
        span=(len(before), len(before) + len(payload)),
        max_bytes=len(raw) if max_bytes is None else max_bytes,
        max_depth=depth,
    )


def preset(fields: str) -> str:
    """A `prosiform` mapping whose `default` preset holds the given flow fields."""
    return "prosiform: {default: {" + fields + "}}"


def paired(value: str) -> str:
    """A `prosiform` mapping whose `default` preset holds this `group` value."""
    return preset("group: " + value)


def joined(conversion: Conversion) -> tuple[str, int] | None:
    """The group the `default` preset joins, with its depth, where it states one."""
    one = conversion.default.membership
    return None if one is None else (one.group, one.depth)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "# comment\n",
        "{}",
        "name: test",
        "metadata: {owner: yes}",
        "metadata: {date: 2026-10-23, binary: 0b10, underscored: 1_000}",
    ],
)
def test_absent_settings(text: str) -> None:
    assert parse(text) == Conversion()
    assert not parse(text).declared


def test_absent_frontmatter_declares_nothing() -> None:
    absent = decode(b"# Body\n", file="a.md", span=None, max_bytes=7, max_depth=1)
    assert not absent.declared


@pytest.mark.parametrize("text", ["prosiform: {}", "prosiform:\n  {}"])
def test_an_empty_block_declares(text: str) -> None:
    assert parse(text) == Conversion(declared=True)


def test_a_grouped_block_declares() -> None:
    assert parse(paired("{rules: 2}")).declared


def test_every_key_names_a_preset_holding_a_mapping() -> None:
    result = parse(
        "prosiform:\n"
        "  default: {group: {rules: 2}}\n"
        "  Target: {subst: [{checks.md: stub.md}]}"
    )
    assert [one.name for one in result.presets] == ["default", "Target"]
    assert joined(result) == ("rules", 2)
    assert result.presets[1].substs == (
        Subst("checks.md", "stub.md", Location("rules/a.md", 4, 20)),
    )


@pytest.mark.parametrize("value", ['"x"', "1", "null", "true", "[]", "[a]"])
def test_a_preset_key_holding_anything_but_a_mapping_is_refused(value: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform:\n  Target: " + value)
    diagnostic = caught.value.diagnostic
    assert diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert "prosiform.Target must be a mapping" in diagnostic.message
    assert diagnostic.location == Location("rules/a.md", 3, 11)


@pytest.mark.parametrize("field", ["group", "subst"])
def test_a_field_outside_its_preset_names_the_preset_it_belongs_in(
    field: str,
) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(f"prosiform: {{{field}: x}}")
    message = caught.value.diagnostic.message
    assert f"prosiform.{field} must be a mapping" in message
    assert f"prosiform.default.{field}" in message


def test_a_document_declaring_no_default_is_compiled_under_an_empty_one() -> None:
    result = parse("prosiform: {Target: {group: {rules: 2}}}")
    assert result.default == Preset("default")
    assert parse("prosiform: {}").default == Preset("default")


def test_an_empty_preset_states_nothing() -> None:
    assert parse("prosiform: {default: {}}") == Conversion(
        declared=True, presets=(Preset("default"),)
    )


def test_subst_holds_a_list() -> None:
    assert parse(preset("subst: []")).default == Preset("default")
    with pytest.raises(InvalidMetadata) as caught:
        parse(preset("subst: x"))
    assert "prosiform.default.subst must be a list" in str(caught.value)


def test_group_and_marks() -> None:
    result = parse(
        'prosiform:\r\n  default:\r\n    group:\r\n      " règles ": 2\r\n',
        prefix="\ufeff---\r\n",
    ).default
    assert result.membership == Membership(
        "default",
        " règles ",
        2,
        Location("rules/a.md", 5, 7),
        Location("rules/a.md", 5, 19),
    )
    with pytest.raises(FrozenInstanceError):
        result.membership.group = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    "value",
    [
        "{modes: 1, targets: 2}",
        "{3: 1}",
        "{null: 1}",
        "{true: 1}",
        "{2.0: 1}",
        "{}",
        "modes",
        "[modes, 1]",
    ],
)
def test_a_malformed_group_pair_is_refused_at_its_value(value: str) -> None:
    text = paired(value)
    with pytest.raises(InvalidMetadata) as caught:
        parse(text)
    diagnostic = caught.value.diagnostic
    assert diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert "prosiform.default.group must" in diagnostic.message
    column = text.rindex(value) + 1
    assert diagnostic.location == Location("rules/a.md", 2, column)


def test_a_subst_entry_is_a_colon_pair() -> None:
    text = preset(
        "subst: [{rules.md: stub.md}, {a.md#Checks: b/c%20d.md}, "
        '{"rules.md#Step 1: Setup": stub.md}]'
    )
    assert parse(text).default.substs == (
        Subst(
            "rules.md",
            "stub.md",
            Location("rules/a.md", 2, text.index("{rules") + 1),
        ),
        Subst(
            "a.md#Checks",
            "b/c%20d.md",
            Location("rules/a.md", 2, text.index("{a.md") + 1),
        ),
        Subst(
            "rules.md#Step 1: Setup",
            "stub.md",
            Location("rules/a.md", 2, text.index('{"rules') + 1),
        ),
    )


@pytest.mark.parametrize(
    "entries,at,entry,said",
    [
        ('"rules.md=stub.md"', 0, '"rules.md=stub.md"', "must be a mapping"),
        (
            "{rules.md: stub.md}, {a.md: b.md, c.md: d.md}",
            1,
            "{a.md: b.md, c.md: d.md}",
            "must be a mapping",
        ),
        ("{}", 0, "{}", "must be a mapping"),
        ("[rules.md, stub.md]", 0, "[rules.md, stub.md]", "must be a mapping"),
        ("3", 0, "3", "must be a mapping"),
        ("null", 0, "null", "must be a mapping"),
        (
            "{3: stub.md}",
            0,
            "{3: stub.md}",
            "must name its original reference with a string key",
        ),
        ("{rules.md: 3}", 0, "{rules.md: 3}", "must map a nonempty original"),
        ("{rules.md: null}", 0, "{rules.md: null}", "must map a nonempty original"),
        ("{rules.md: [a.md]}", 0, "{rules.md: [a.md]}", "must map a nonempty"),
        ('{rules.md: ""}', 0, '{rules.md: ""}', "must map a nonempty original"),
        ('{"": stub.md}', 0, '{"": stub.md}', "must map a nonempty original"),
    ],
)
def test_a_subst_entry_that_is_no_colon_pair_is_refused_naming_it(
    entries: str, at: int, entry: str, said: str
) -> None:
    text = preset("subst: [" + entries + "]")
    with pytest.raises(InvalidMetadata) as caught:
        parse(text)
    diagnostic = caught.value.diagnostic
    assert diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert f"prosiform.default.subst[{at}] {said}" in diagnostic.message
    assert diagnostic.location == Location("rules/a.md", 2, text.rindex(entry) + 1)


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
        "prosiform: {default: {1: x}}",
        preset("group: rules"),
        preset("group: 2"),
        paired('{rules: "2"}'),
        preset("unknown: x"),
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
        parse(paired("{" + json.dumps(group) + ": 2}"))


@pytest.mark.parametrize("group", ["-", "_", "--", "- _", "_-_"])
def test_a_group_name_whose_title_case_is_empty_is_refused(group: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(paired("{" + json.dumps(group) + ": 2}"))
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    message = caught.value.diagnostic.message
    assert "prosiform.default.group must name a group carrying a word" in message


@pytest.mark.parametrize("group", ["a", "-a-", "x_1", "!"])
def test_a_group_name_carrying_a_word_is_admitted(group: str) -> None:
    assert joined(parse(paired("{" + json.dumps(group) + ": 2}"))) == (group, 2)


@pytest.mark.parametrize("depth", ["0", "7", "22", "٢", "2.0", " 2"])
def test_depth_grammar(depth: str) -> None:
    with pytest.raises(InvalidMetadata):
        parse(paired("{rules: " + json.dumps(depth) + "}"))


@pytest.mark.parametrize("depth", range(1, 7))
def test_depth_values(depth: int) -> None:
    assert joined(parse(paired(f"{{rules: {depth}}}"))) == ("rules", depth)


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
    text = preset('subst: [{x: y}], prosiform-bad: "x"')
    with pytest.raises(InvalidMetadata) as caught:
        parse(text)
    column = text.index("prosiform-bad") + 1
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, column)
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
    text = preset('subst: [{"\t": y}], prosiform-bad: x')
    with pytest.raises(InvalidMetadata) as caught:
        parse(text)
    column = text.index("prosiform-bad") + 1
    assert caught.value.diagnostic.location == Location("rules/a.md", 2, column)


def test_yaml_marked_syntax_error() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("a: [\n}")
    assert caught.value.diagnostic.location == Location("rules/a.md", 3, 1)


def test_single_line_bom_coordinate() -> None:
    raw = "\ufeffprosiform: {default: {prosiform-bad: x}}".encode()
    with pytest.raises(InvalidMetadata) as caught:
        decode(raw, file="a", span=(3, len(raw)), max_bytes=len(raw), max_depth=3)
    assert caught.value.diagnostic.location == Location("a", 1, 24)


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
    "text",
    [
        'prosiform:\r\n  root: "."',
        'prosiform:\r\n  root: ""',
        "prosiform:\r\n  root: null",
        'prosiform:\r\n  root: "/tmp"\r\n  default: {group: {rules: 2}}',
    ],
)
def test_a_declared_root_is_refused_at_its_key(text: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(text, prefix="\ufeff---\r\n")
    diagnostic = caught.value.diagnostic
    assert diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert diagnostic.location == Location("rules/a.md", 3, 3)
    assert "prosiform.root is refused" in diagnostic.message
    assert "remove the field" in diagnostic.message


def test_a_root_within_a_preset_is_refused_at_its_key() -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse('prosiform:\n  default:\n    root: "."')
    diagnostic = caught.value.diagnostic
    assert diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert diagnostic.location == Location("rules/a.md", 4, 5)
    assert "prosiform.default.root is refused" in diagnostic.message


@pytest.mark.parametrize(
    "depth", ["true", "false", "null", "[]", "{}", "0", "7", "-1", "2.0", "2e0", "'2'"]
)
def test_integer_depth_schema(depth: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(paired(f"{{rules: {depth}}}"))
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert "prosiform.default.group for group 'rules' must be" in str(caught.value)


@pytest.mark.parametrize("depth", ["+2", "02", "0x2", "0o2", "!!int 2"])
def test_core_integer_depth(depth: str) -> None:
    assert joined(parse(paired(f"{{rules: {depth}}}"))) == ("rules", 2)


@pytest.mark.parametrize(
    "text",
    [
        "metadata: null",
        "metadata: [true, {1: [2]}]",
        'metadata: {prosiform-group: rules, depth: "2"}',
        "metadata: {root: .., group: {rules: 2}}",
        "root: ..\ngroup: {rules: 2}",
    ],
)
def test_unreserved_fields_have_no_conversion_meaning(text: str) -> None:
    assert parse(text) == Conversion()


@pytest.mark.parametrize(
    "key",
    [
        "prosiform-group",
        "version",
        "r",
        "depth",
        "dispatch",
        "group-heading",
        "unknown",
    ],
)
def test_reserved_mapping_has_exact_keys(key: str) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse(preset(f"{key}: x"))
    assert caught.value.diagnostic.code == "E_INVALID_CONVERSION_METADATA"
    assert f"unknown field prosiform.default.{key}" in str(caught.value)


def test_root_mapping_nesting_budget() -> None:
    assert parse("prosiform: {}", depth=2).declared
    with pytest.raises(InvalidMetadata) as caught:
        parse("prosiform: {}", depth=1)
    assert caught.value.diagnostic.code == "E_RESOURCE_LIMIT"


@pytest.mark.parametrize(
    "literal",
    [
        "0x" + "f" * SCALAR_DIGITS,
        "0o" + "7" * SCALAR_DIGITS,
        "1e" + "9" * (SCALAR_DIGITS - 1),
    ],
)
def test_a_scalar_whose_canonical_form_is_quadratic_has_a_ceiling(
    literal: str,
) -> None:
    with pytest.raises(InvalidMetadata) as caught:
        parse("other: " + literal)
    assert caught.value.diagnostic.code == "E_RESOURCE_LIMIT"
    assert str(SCALAR_DIGITS) in str(caught.value)


@pytest.mark.parametrize(
    "literal",
    [
        "0x" + "f" * (SCALAR_DIGITS - 2),
        "0o" + "7" * (SCALAR_DIGITS - 2),
        "1e" + "9" * (SCALAR_DIGITS - 3),
        "9" * (SCALAR_DIGITS * 4),
        "1." + "9" * (SCALAR_DIGITS * 4),
    ],
)
def test_a_scalar_within_the_ceiling_is_read(literal: str) -> None:
    assert parse("other: " + literal) == Conversion()


def test_one_scalar_beyond_the_ceiling_is_refused_inside_the_byte_budget() -> None:
    """A source the byte budget admits completes inside it, whatever it holds.

    A scalar of a million hex digits fits a source of a megabyte and costs
    sixteen seconds to canonicalise on its own, which is work the byte
    budget never counted. The ceiling is what turns that into a refusal the
    run reaches in a fraction of the second, so the figure here is the time
    the source may take and not a value it may hold.
    """
    budget = FILE_BYTES.default
    payload = "other: 0x" + "f" * (budget - 40)
    assert len(payload) < budget
    began = time.perf_counter()
    with pytest.raises(InvalidMetadata) as caught:
        parse(payload, max_bytes=budget)
    assert caught.value.diagnostic.code == "E_RESOURCE_LIMIT"
    assert time.perf_counter() - began < 5


def test_metadata_has_no_conversion_meaning() -> None:
    assert parse("metadata: {dispatch: One rule.}") == Conversion()
