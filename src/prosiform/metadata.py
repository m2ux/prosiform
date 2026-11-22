"""Decode captured YAML metadata into conversion settings.

`decode` owns payload validation; `_preset` validates each preset,
and the scalar readers own Core type resolution and equality.
"""

import re
from bisect import bisect_right
from collections.abc import Hashable
from dataclasses import dataclass, field
from decimal import Decimal
from typing import cast

from ruamel.yaml import YAML
from ruamel.yaml.error import MarkedYAMLError, StreamMark, YAMLError
from ruamel.yaml.events import (
    AliasEvent,
    CollectionEndEvent,
    CollectionStartEvent,
    DocumentStartEvent,
    MappingStartEvent,
    ScalarEvent,
)
from ruamel.yaml.reader import ReaderError
from ruamel.yaml.scanner import Scanner, ScannerError

from prosiform.diagnostics import ERROR, Diagnostic, Location, RelatedLocation
from prosiform.heading import worded
from prosiform.limits import FILE_BYTES, NESTING, SCALAR_DIGITS
from prosiform.tags import PICK

INVALID_FRONTMATTER = "E_INVALID_FRONTMATTER"
INVALID_CONVERSION_METADATA = "E_INVALID_CONVERSION_METADATA"
RESOURCE_LIMIT = "E_RESOURCE_LIMIT"
GROUP = "group"
SUBST = "subst"
CHOICE = "choice"
STUB = "stub"
BRIEF = "brief"
LEVEL = "level"
LEVELS = "levels"
FIELDS = (GROUP, SUBST, CHOICE, STUB, BRIEF, LEVEL, LEVELS)
"""Preset field names recognized by `_preset`."""
DEFAULT = "default"
"""The name read by `Conversion.default`."""
ROOT = "root"
PREFIX = "tag:yaml.org,2002:"
PATTERNS = {
    "null": re.compile(r"(?:~|null|Null|NULL|)"),
    "bool": re.compile(r"(?:true|True|TRUE|false|False|FALSE)"),
    "int": re.compile(r"(?:[-+]?[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+)"),
    "float": re.compile(
        r"(?:[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?"
        r"|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))"
    ),
}
PREFIXED = ("0o", "0x")


class _MarkedScanner(Scanner):
    """A YAML scanner retaining diagnostic coordinates for scalar escapes."""

    def scan_flow_scalar_non_spaces(
        self, double: bool, start_mark: StreamMark
    ) -> list[str]:
        """Preserve a malformed escape's mark before parser cleanup resets it."""
        try:
            return cast(
                list[str], super().scan_flow_scalar_non_spaces(double, start_mark)
            )
        except ValueError as error:
            raise ScannerError(
                "while scanning a scalar",
                start_mark,
                "invalid Unicode scalar escape",
                self.reader.get_mark(),
            ) from error


@dataclass(frozen=True)
class Membership:
    """A preset's group membership and the coordinates of its declaration.

    `preset` names the declaring preset, `group` the group and `depth`
    its heading depth. `group_location` and `depth_location` locate
    the two values.
    """

    preset: str
    group: str
    depth: int
    group_location: Location
    depth_location: Location


@dataclass(frozen=True)
class Subst:
    """One substitution entry as written, with its source coordinate.

    `original` and `substitute` hold the two references; `location`
    locates their entry.
    """

    original: str
    substitute: str
    location: Location


@dataclass(frozen=True)
class Preset:
    """One named preset's values.

    `name` identifies the preset. `membership` holds its group pair,
    and `substs` its substitution entries in declaration order.
    `choice` holds an alternative's choice line, `stub` a stand-in's
    line and `brief` a section fragment. `level` holds a capability
    level and `levels` the declared level-to-model pairs in order.
    """

    name: str
    membership: Membership | None = None
    substs: tuple[Subst, ...] = ()
    choice: str | None = None
    stub: str | None = None
    brief: str | None = None
    level: str | None = None
    levels: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Conversion:
    """One source's immutable settings and the run context attached to them.

    `declared` records the presence of a prosiform mapping. `presets`
    holds the presets in declaration order. `run` holds the run's names
    and `models` its level-to-model pairs.
    """

    declared: bool = False
    presets: tuple[Preset, ...] = ()
    run: frozenset[str] = frozenset()
    models: tuple[tuple[str, str], ...] = ()

    @property
    def default(self) -> Preset:
        """The declared `default` preset, or an empty preset where it is absent."""
        return next(
            (preset for preset in self.presets if preset.name == DEFAULT),
            Preset(DEFAULT),
        )

    @property
    def alternatives(self) -> tuple[Preset, ...]:
        """Each preset holding a choice line, in declaration order."""
        return tuple(preset for preset in self.presets if preset.choice is not None)

    def carried(self) -> frozenset[str]:
        """The run names eligible for a deferral's title.

        A name matching a non-stub preset of this document is excluded,
        because publishing it would select a preset the current reference
        did not select. `cli.entry_stubs` owns run stub selection.
        """
        declared = {
            preset.name.casefold() for preset in self.presets if preset.stub is None
        }
        return frozenset(name for name in self.run if name not in declared)


class InvalidMetadata(Exception):
    """A failure ready for either diagnostic renderer."""

    def __init__(self, diagnostic: Diagnostic) -> None:
        super().__init__(diagnostic.message)
        self.diagnostic = diagnostic


@dataclass
class _Node:
    kind: str
    location: Location
    value: str = ""
    children: list["_Node"] = field(default_factory=list)
    identity: int = 0


def _fail(
    code: str, message: str, location: Location, first: Location | None = None
) -> InvalidMetadata:
    related = (
        None
        if first is None
        else (
            RelatedLocation(
                first.file, first.line, first.column, "first key occurrence"
            ),
        )
    )
    return InvalidMetadata(
        Diagnostic(ERROR, message, code, location=location, related=related)
    )


def _scalar(
    value: str, tag: str | None, plain: bool, location: Location
) -> tuple[str, Hashable]:
    """A scalar's Core type and equality value, within the work bound.

    Surrogate code points are invalid frontmatter. A notation `costly`
    identifies is limited to `limits.SCALAR_DIGITS` before `_canonical`
    constructs its value, because conversion costs quadratic time in
    its digits.
    """
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise _fail(INVALID_FRONTMATTER, "invalid Unicode scalar value", location)
    kind = _kind(value, tag, plain, location)
    if costly(kind, value) and len(value) > SCALAR_DIGITS:
        raise _fail(
            RESOURCE_LIMIT,
            f"one {kind} scalar carries {len(value)} characters, more than the "
            f"{SCALAR_DIGITS} a scalar of this notation may carry, because its "
            f"canonical form costs time quadratic in its digits; write the same "
            f"value in decimal or as a string, or keep it within "
            f"{SCALAR_DIGITS} characters",
            location,
        )
    return kind, _canonical(value, kind)


def costly(kind: str, value: str) -> bool:
    """Whether one scalar's canonical form costs more than a pass over its literal."""
    if kind == "int":
        return value.startswith(PREFIXED)
    return kind == "float" and ("e" in value.lower() and "inf" not in value.lower())


def _kind(value: str, tag: str | None, plain: bool, location: Location) -> str:
    """The YAML 1.2 Core type of a scalar, without constructing its value.

    An explicit Core tag determines the type and validates its literal.
    An untagged plain scalar uses `PATTERNS`; other scalars and the
    non-specific ! tag are strings. Other tags are invalid frontmatter.
    """
    if tag in (None, "!"):
        return next(
            (
                name
                for name, pattern in PATTERNS.items()
                if plain and tag != "!" and pattern.fullmatch(value)
            ),
            "str",
        )
    kind = tag.removeprefix(PREFIX)
    if tag != PREFIX + kind or kind not in (*PATTERNS, "str"):
        raise _fail(INVALID_FRONTMATTER, "custom or non-Core scalar tag", location)
    if kind != "str" and not PATTERNS[kind].fullmatch(value):
        raise _fail(INVALID_FRONTMATTER, f"invalid {kind} scalar", location)
    return kind


def _canonical(value: str, kind: str) -> Hashable:
    """One scalar's value as equality is decided, from a scalar already bounded."""
    if kind == "null":
        return "null"
    if kind == "bool":
        return value.lower()
    if kind == "int":
        return _decimal_integer(value)
    if kind == "float":
        if "inf" in value.lower() or "nan" in value.lower():
            return value.lower().replace("+", "")
        return _finite_float(value)
    return value


def _decimal_integer(value: str) -> Decimal:
    """The exact decimal value of a bounded Core integer literal.

    Decimal text is normalized directly; base-prefixed text is converted
    through its integer value. `_scalar` owns the work bound.
    """
    if not value.startswith(("0o", "0x")):
        return Decimal(value)
    return Decimal(int(value, 8 if value.startswith("0o") else 16))


def _finite_float(value: str) -> tuple[str, int]:
    """Exact decimal equality without floating-point or decimal exponent limits."""
    coefficient, _, exponent = value.lower().partition("e")
    power = 0
    digits = exponent.lstrip("+-")
    for offset in range(0, len(digits), 9):
        chunk = digits[offset : offset + 9]
        power = power * 10 ** len(chunk) + int(chunk)
    if exponent.startswith("-"):
        power = -power
    negative = coefficient.startswith("-")
    coefficient = coefficient.lstrip("+-")
    whole, _, fraction = coefficient.partition(".")
    digits = (whole + fraction).lstrip("0")
    if not digits:
        return ("0", 0)
    significant = digits.rstrip("0")
    power += len(digits) - len(significant) - len(fraction)
    return (("-" if negative else "") + significant, power)


def decode(
    raw: bytes,
    *,
    file: str,
    span: tuple[int, int] | None,
    max_bytes: int,
    max_depth: int,
) -> Conversion:
    """Decode a recognized payload's half-open byte span, without delimiters.

    None means absent frontmatter. The caller supplies captured bytes and budgets.
    The raw limit includes body and BOM and is checked before UTF-8 decoding.

    Parse one YAML 1.2 mapping with an iterative collection stack bounded
    by max_depth. Aliases, custom tags and merge keys are refused. Interned
    tag-aware identities detect duplicate keys, including collection keys.
    A prosiform mapping is decoded through `_preset`; `_scalar` owns scalar
    validation and canonical equality.
    """
    if len(raw) > max_bytes:
        raise _fail(
            RESOURCE_LIMIT,
            f"{FILE_BYTES.name} raw source bytes {len(raw)} exceed limit "
            f"{max_bytes}; reduce source bytes or raise --budget {FILE_BYTES.name}",
            Location(file, 1, 1),
        )
    if span is None:
        return Conversion()
    start, end = span
    if not 0 <= start <= end <= len(raw):
        raise ValueError("frontmatter span must be within captured source bytes")
    prefix = raw[:start].decode("utf-8")
    text = raw[start:end].decode("utf-8")
    starts = [0] + [match.end() for match in re.finditer("\n", prefix + text)]

    def at(index: int) -> Location:
        offset = len(prefix) + index
        line = bisect_right(starts, offset)
        return Location(file, line, offset - starts[line - 1] + 1)

    stack: list[_Node] = []
    root: _Node | None = None
    identities: dict[tuple[str, Hashable], int] = {}
    documents = 0

    def finish(node: _Node, canonical: Hashable) -> None:
        nonlocal root
        identity = (node.kind, canonical)
        node.identity = identities.setdefault(identity, len(identities) + 1)
        if stack:
            stack[-1].children.append(node)
        else:
            root = node

    parser = YAML(typ="safe", pure=True)
    parser.Scanner = _MarkedScanner
    parser.version = (1, 2)
    try:
        for event in parser.parse(text):
            location = at(event.start_mark.index)
            if isinstance(event, DocumentStartEvent):
                documents += 1
                if documents > 1 or event.version not in (None, (1, 2)):
                    raise _fail(
                        INVALID_FRONTMATTER, "expected one YAML 1.2 document", location
                    )
            elif isinstance(event, AliasEvent):
                raise _fail(
                    INVALID_FRONTMATTER, "YAML aliases are not allowed", location
                )
            elif isinstance(event, CollectionStartEvent):
                kind = "map" if isinstance(event, MappingStartEvent) else "seq"
                if event.tag not in (None, "!", PREFIX + kind):
                    raise _fail(
                        INVALID_FRONTMATTER,
                        "custom or mismatched collection tag",
                        location,
                    )
                if len(stack) >= max_depth:
                    raise _fail(
                        RESOURCE_LIMIT,
                        f"{NESTING.name} YAML collection depth {len(stack) + 1} "
                        f"exceeds limit {max_depth}; reduce nesting or raise "
                        f"--budget {NESTING.name}",
                        location,
                    )
                stack.append(_Node(kind, location))
            elif isinstance(event, CollectionEndEvent):
                node = stack.pop()
                canonical: Hashable
                if node.kind == "map":
                    seen: dict[int, Location] = {}
                    pairs = list(
                        zip(node.children[::2], node.children[1::2], strict=True)
                    )
                    for key, _ in pairs:
                        if key.kind == "str" and key.value == "<<":
                            raise _fail(
                                INVALID_FRONTMATTER,
                                "YAML merge keys are not allowed",
                                key.location,
                            )
                        if key.identity in seen:
                            raise _fail(
                                INVALID_FRONTMATTER,
                                f"duplicate YAML key {key.value!r}",
                                key.location,
                                seen[key.identity],
                            )
                        seen[key.identity] = key.location
                    canonical = frozenset(
                        (key.identity, value.identity) for key, value in pairs
                    )
                else:
                    canonical = tuple(child.identity for child in node.children)
                finish(node, canonical)
            elif isinstance(event, ScalarEvent):
                kind, canonical = _scalar(
                    event.value, event.tag, event.implicit[0], location
                )
                finish(_Node(kind, location, event.value), canonical)
    except MarkedYAMLError as error:
        mark = error.problem_mark or error.context_mark
        raise _fail(
            INVALID_FRONTMATTER,
            error.problem or "invalid YAML",
            at(mark.index if mark else 0),
        ) from error
    except ReaderError as error:
        raise _fail(
            INVALID_FRONTMATTER, "invalid YAML character", at(error.position)
        ) from error
    except YAMLError as error:
        raise _fail(INVALID_FRONTMATTER, "invalid YAML", at(0)) from error
    if root is None:
        return Conversion()
    if root.kind != "map":
        raise _fail(
            INVALID_FRONTMATTER, "frontmatter root must be a mapping", root.location
        )
    metadata: _Node | None = None
    for key, value in zip(root.children[::2], root.children[1::2], strict=True):
        if key.kind != "str":
            raise _fail(
                INVALID_FRONTMATTER,
                "frontmatter root keys must be strings",
                key.location,
            )
        if key.value == "prosiform":
            metadata = value
    if metadata is None:
        return Conversion()
    if metadata.kind != "map":
        raise _fail(
            INVALID_CONVERSION_METADATA,
            "prosiform must be a mapping",
            metadata.location,
        )
    presets: list[Preset] = []
    for key, value in zip(metadata.children[::2], metadata.children[1::2], strict=True):
        if key.kind != "str":
            raise _fail(
                INVALID_CONVERSION_METADATA,
                "prosiform keys must be strings",
                key.location,
            )
        name = "prosiform." + key.value
        if key.value == ROOT:
            raise _refused_root(name, key.location)
        if key.value == PICK:
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} is refused: {PICK} is the title token leaving the pick "
                "to an agent, so no reference could select the preset; "
                "rename the preset",
                key.location,
            )
        if value.kind != "map":
            within = {CHOICE: "<alternative>", STUB: "<stub>"}.get(key.value, DEFAULT)
            remedy = (
                f"; write the field within a preset, as prosiform.{within}.{key.value}"
                if key.value in FIELDS
                else ""
            )
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} must be a mapping, since every prosiform key names a "
                f"preset holding its settings{remedy}",
                value.location,
            )
        presets.append(_preset(key.value, value))
    return Conversion(declared=True, presets=tuple(presets))


def _refused_root(name: str, location: Location) -> InvalidMetadata:
    return _fail(
        INVALID_CONVERSION_METADATA,
        f"{name} is refused: a document declares its inclusion and "
        "states no boundary; remove the field",
        location,
    )


def _preset(preset: str, mapping: _Node) -> Preset:
    """One preset's settings, each field checked where it is written."""
    fields: dict[str, _Node] = {}
    for key, value in zip(mapping.children[::2], mapping.children[1::2], strict=True):
        if key.kind != "str":
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"prosiform.{preset} keys must be strings",
                key.location,
            )
        name = f"prosiform.{preset}.{key.value}"
        if key.value == ROOT:
            raise _refused_root(name, key.location)
        if key.value not in FIELDS:
            raise _fail(
                INVALID_CONVERSION_METADATA, f"unknown field {name}", key.location
            )
        if key.value == SUBST and value.kind != "seq":
            raise _fail(
                INVALID_CONVERSION_METADATA, f"{name} must be a list", value.location
            )
        if key.value == CHOICE and preset.casefold() == DEFAULT:
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} is refused: {DEFAULT} is in force wherever its document "
                "is compiled, so it is no alternative a reference picks; write "
                "the choice within a named preset",
                key.location,
            )
        if key.value == CHOICE and not _one_line(value):
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} must be a non-empty string holding no line break, "
                "since it is printed beside its alternative as one row",
                value.location,
            )
        if key.value == STUB and preset.casefold() == DEFAULT:
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} is refused: {DEFAULT} is in force wherever its document "
                "is compiled, so it is no stub a run selects; write the stub "
                "within a named preset",
                key.location,
            )
        if key.value == STUB and not _one_line(value):
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} must be a non-empty string holding no line break, "
                "since it states in one line what the stub stands in for",
                value.location,
            )
        if key.value == BRIEF and not _fragment(value):
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} must be a fragment naming a heading of its own "
                "document, as '#given', since a brief is a section of the "
                "document a dispatch names",
                value.location,
            )
        if key.value == LEVEL and not _one_line(value):
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} must be a non-empty string holding no line break, "
                "since it names one capability level",
                value.location,
            )
        if key.value == LEVELS and not _models(value):
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} must be a mapping of each level to a model, each a "
                "non-empty string holding no line break, as {judgement: opus}",
                value.location,
            )
        if {key.value, *fields} >= {CHOICE, STUB}:
            raise _fail(
                INVALID_CONVERSION_METADATA,
                f"{name} is refused: prosiform.{preset} holds both {CHOICE} and "
                f"{STUB}, and a preset is an alternative a reference picks or a "
                "stub a run selects, never both; keep one of the two",
                key.location,
            )
        fields[key.value] = value
    named = f"prosiform.{preset}."

    held = fields[SUBST].children if SUBST in fields else []
    return Preset(
        preset,
        _membership(preset, named + GROUP, fields[GROUP]) if GROUP in fields else None,
        tuple(_subst(f"{named}{SUBST}[{at}]", entry) for at, entry in enumerate(held)),
        fields[CHOICE].value if CHOICE in fields else None,
        fields[STUB].value if STUB in fields else None,
        fields[BRIEF].value if BRIEF in fields else None,
        fields[LEVEL].value if LEVEL in fields else None,
        tuple(
            (level.value, model.value)
            for level, model in zip(
                fields[LEVELS].children[::2],
                fields[LEVELS].children[1::2],
                strict=True,
            )
        )
        if LEVELS in fields
        else (),
    )


def _fragment(node: _Node) -> bool:
    """Whether one value is a string naming a section of its own document alone."""
    return (
        _one_line(node)
        and node.value.startswith("#")
        and len(node.value) > 1
        and "#" not in node.value[1:]
    )


def _models(node: _Node) -> bool:
    """Whether a mapping has string keys and values accepted by `_one_line`."""
    return node.kind == "map" and all(_one_line(one) for one in node.children)


def _one_line(node: _Node) -> bool:
    """Whether one value is a non-empty string holding no line break."""
    return node.kind == "str" and node.value.splitlines() == [node.value]


def _single_line(text: str) -> bool:
    """Whether one name is nonblank, printable and written on one line."""
    return bool(text.strip()) and not any(
        char in "\u0085\u2028\u2029"
        or ord(char) < 32
        or 127 <= ord(char) <= 159
        or 0xD800 <= ord(char) <= 0xDFFF
        or ord(char) in (0xFFFE, 0xFFFF)
        for char in text
    )


def _level(node: _Node) -> int | None:
    """A heading level from 1 through 6 one integer scalar states, or None."""
    level = (
        _scalar(node.value, PREFIX + "int", True, node.location)[1]
        if node.kind == "int"
        else None
    )
    if not isinstance(level, Decimal) or not 1 <= level <= 6:
        return None
    return int(level)


def _pair(name: str, entry: _Node, shape: str, noun: str) -> tuple[_Node, _Node]:
    """One single-entry mapping's string key and its value, or the entry's refusal.

    `shape` completes the sentence stating what the entry must be, and
    `noun` names what its key names.
    """
    if entry.kind != "map" or len(entry.children) != 2:
        raise _fail(
            INVALID_CONVERSION_METADATA, f"{name} must be {shape}", entry.location
        )
    key, value = entry.children
    if key.kind != "str":
        raise _fail(
            INVALID_CONVERSION_METADATA,
            f"{name} must name its {noun} with a string key",
            entry.location,
        )
    return key, value


def _membership(preset: str, name: str, entry: _Node) -> Membership:
    """A named group membership validated from one preset entry.

    `_pair` owns entry shape, `_single_line` owns printable names,
    `heading.worded` identifies a word and `_level` validates depth.
    A group name carrying a colon or slash is invalid metadata.
    """
    group, depth = _pair(
        name,
        entry,
        "a mapping holding one group and its depth, as {<group>: <depth>}",
        "group",
    )
    if not _single_line(group.value) or any(char in ":/" for char in group.value):
        raise _fail(
            INVALID_CONVERSION_METADATA,
            f"{name} must name a group printable, single-line and nonblank, "
            "without ':' or '/'",
            group.location,
        )
    if not worded(group.value):
        raise _fail(
            INVALID_CONVERSION_METADATA,
            f"{name} must name a group carrying a word, since its title case "
            "is the group's heading; name the group with a character other "
            "than a hyphen, an underscore or whitespace",
            group.location,
        )
    level = _level(depth)
    if level is None:
        raise _fail(
            INVALID_CONVERSION_METADATA,
            f"{name} for group {group.value!r} must be an integer from 1 through 6",
            depth.location,
        )
    return Membership(preset, group.value, level, group.location, depth.location)


def _subst(name: str, entry: _Node) -> Subst:
    """One nonempty string-to-string substitution from an entry.

    `_pair` owns the entry shape; `cli.substs` owns reference validation.
    """
    shape = (
        "a mapping holding one original reference and its substitute, "
        "as {rules.md: stub.md}"
    )
    original, substitute = _pair(name, entry, shape, "original reference")
    if substitute.kind != "str" or not original.value or not substitute.value:
        raise _fail(
            INVALID_CONVERSION_METADATA,
            f"{name} must map a nonempty original reference to a nonempty "
            "substitute written as a string",
            entry.location,
        )
    return Subst(original.value, substitute.value, entry.location)
