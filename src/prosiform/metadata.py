"""Bounded YAML Core metadata from one captured source byte span.

Events supply grammar and marks. An iterative stack bounds collection depth;
interned node identities preserve YAML tag and value equality for complex keys.
No YAML objects or aliases are constructed.
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

INVALID_FRONTMATTER = "E_INVALID_FRONTMATTER"
INVALID_CONVERSION_METADATA = "E_INVALID_CONVERSION_METADATA"
RESOURCE_LIMIT = "E_RESOURCE_LIMIT"
GROUP = "group"
SUBST = "subst"
FIELDS = (GROUP, SUBST)
"""The fields a preset may hold; none is written directly under `prosiform`."""
DEFAULT = "default"
"""The preset in force wherever its document is compiled."""
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
"""The two notations whose canonical form costs more than a pass over the literal.

A decimal integer is already its own decimal value, and a float without an
exponent is read in one pass. A base-prefixed integer is exact only through
a binary value, and a float's exponent is accumulated digit by digit, so
both cost quadratic time in their digits.
"""
PREFIXED = ("0o", "0x")


class _MarkedScanner(Scanner):
    """Preserve a malformed escape's mark before parser cleanup resets it."""

    def scan_flow_scalar_non_spaces(
        self, double: bool, start_mark: StreamMark
    ) -> list[str]:
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
    """A preset's `group` pair: a merged group and the depth its document joins at.

    The depth is held to the one every contributing member of the group
    declares. Each location is where its half of the entry is written,
    and the preset is the one stating the entry, which a diagnostic
    about it names.
    """

    preset: str
    group: str
    depth: int
    group_location: Location
    depth_location: Location


@dataclass(frozen=True)
class Subst:
    """One `subst` entry: an original reference mapped to its alternative.

    Each side is held as written, a reference the reference grammar
    reads. The location is the entry's.
    """

    original: str
    alternative: str
    location: Location


@dataclass(frozen=True)
class Preset:
    """One named preset's settings.

    `membership` holds the `group` pair, the one group the declaring
    document joins; a preset stating none leaves the document its
    individual file group. `substs` holds each `subst` entry in written
    order.
    """

    name: str
    membership: Membership | None = None
    substs: tuple[Subst, ...] = ()


@dataclass(frozen=True)
class Conversion:
    """Immutable source settings: every preset one document declares.

    The settings belong to the bytes they were decoded from. `declared`
    holds where the frontmatter carries a `prosiform` mapping, an empty
    one included, and is false for a document carrying none. `presets`
    holds each preset in written order. A source the substitution mapping
    redirected is read as the substitute, so the settings decoded here are
    the substitute's: none travels from the document its key named.
    """

    declared: bool = False
    presets: tuple[Preset, ...] = ()

    @property
    def default(self) -> Preset:
        """The `default` preset, in force wherever the document is compiled.

        A document declaring no `default` is compiled under an empty one.
        """
        return next(
            (preset for preset in self.presets if preset.name == DEFAULT),
            Preset(DEFAULT),
        )


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
    """The YAML 1.2 Core type one scalar resolves to, and nothing built from it.

    Resolution reads the tag where the source wrote one and the implicit
    rule otherwise, so a base-prefixed integer and a float's exponent are
    classified here without being converted. That is what lets the caller
    hold the work ceiling before the work is asked for.
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
    """A Core integer's exact value, from any of the three notations it admits.

    A base-prefixed literal is exact only through a binary value, and
    converting a binary value to a decimal one is the cost the caller's
    ceiling bounds. A decimal literal is its own decimal value, which
    costs one pass over the digits.
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
        if value.kind != "map":
            remedy = (
                f"; write the field within a preset, as prosiform.{DEFAULT}.{key.value}"
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
        fields[key.value] = value
    named = f"prosiform.{preset}."

    held = fields[SUBST].children if SUBST in fields else []
    return Preset(
        preset,
        _membership(preset, named + GROUP, fields[GROUP]) if GROUP in fields else None,
        tuple(_subst(f"{named}{SUBST}[{at}]", entry) for at, entry in enumerate(held)),
    )


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
    """A preset's `group` pair, a single string key mapped to a depth."""
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
    """One `subst` entry, a single string key mapped to a string.

    YAML splits a plain key at a colon followed by a space, so a side
    holding one is quoted; the reference grammar reads each side as
    YAML delivers it.
    """
    shape = (
        "a mapping holding one original reference and its alternative, "
        "as {rules.md: stub.md}"
    )
    original, alternative = _pair(name, entry, shape, "original reference")
    if alternative.kind != "str" or not original.value or not alternative.value:
        raise _fail(
            INVALID_CONVERSION_METADATA,
            f"{name} must map a nonempty original reference to a nonempty "
            "alternative written as a string",
            entry.location,
        )
    return Subst(original.value, alternative.value, entry.location)
