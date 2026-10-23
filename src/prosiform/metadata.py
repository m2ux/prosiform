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

INVALID_FRONTMATTER = "E_INVALID_FRONTMATTER"
INVALID_CONVERSION_METADATA = "E_INVALID_CONVERSION_METADATA"
RESOURCE_LIMIT = "E_RESOURCE_LIMIT"
GROUP = "prosiform-group"
DEPTH = "prosiform-group-depth"
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
class Conversion:
    """Immutable paired settings and their original value locations."""

    group: str | None = None
    depth: int | None = None
    group_location: Location | None = None
    depth_location: Location | None = None


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
    if tag in (None, "!"):
        kind = next(
            (
                name
                for name, pattern in PATTERNS.items()
                if plain and tag != "!" and pattern.fullmatch(value)
            ),
            "str",
        )
    else:
        kind = tag.removeprefix(PREFIX)
        if tag != PREFIX + kind or kind not in (*PATTERNS, "str"):
            raise _fail(INVALID_FRONTMATTER, "custom or non-Core scalar tag", location)
        if kind != "str" and not PATTERNS[kind].fullmatch(value):
            raise _fail(INVALID_FRONTMATTER, f"invalid {kind} scalar", location)
    canonical: Hashable = value
    if kind == "null":
        canonical = "null"
    elif kind == "bool":
        canonical = value.lower()
    elif kind == "int":
        canonical = (
            Decimal(int(value, 8 if value.startswith("0o") else 16))
            if value.startswith(("0o", "0x"))
            else Decimal(value)
        )
    elif kind == "float":
        canonical = (
            value.lower().replace("+", "")
            if "inf" in value.lower() or "nan" in value.lower()
            else _finite_float(value)
        )
    return kind, canonical


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
            f"-B raw source bytes {len(raw)} exceed limit {max_bytes}; "
            "reduce source bytes or raise -B",
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
                        f"-N YAML collection depth {len(stack) + 1} exceeds "
                        f"limit {max_depth}; reduce nesting or raise -N",
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
        if key.value == "metadata":
            metadata = value
    if metadata is None:
        return Conversion()
    if metadata.kind != "map":
        raise _fail(
            INVALID_CONVERSION_METADATA,
            "metadata must be a string mapping",
            metadata.location,
        )
    fields: dict[str, _Node] = {}
    for key, value in zip(metadata.children[::2], metadata.children[1::2], strict=True):
        if key.kind != "str":
            raise _fail(
                INVALID_CONVERSION_METADATA,
                "metadata keys must be strings",
                key.location,
            )
        name = "metadata." + key.value
        if key.value.startswith("prosiform-") and key.value not in (GROUP, DEPTH):
            raise _fail(
                INVALID_CONVERSION_METADATA, f"unknown field {name}", key.location
            )
        if value.kind != "str":
            raise _fail(
                INVALID_CONVERSION_METADATA, f"{name} must be a string", value.location
            )
        fields[key.value] = value
    if GROUP not in fields and DEPTH not in fields:
        return Conversion()
    if GROUP not in fields or DEPTH not in fields:
        present = GROUP if GROUP in fields else DEPTH
        raise _fail(
            INVALID_CONVERSION_METADATA,
            f"metadata.{present} requires its paired field",
            fields[present].location,
        )
    group, depth = fields[GROUP], fields[DEPTH]
    if not group.value.strip() or any(
        char in ":/\u0085\u2028\u2029"
        or ord(char) < 32
        or 127 <= ord(char) <= 159
        or 0xD800 <= ord(char) <= 0xDFFF
        or ord(char) in (0xFFFE, 0xFFFF)
        for char in group.value
    ):
        raise _fail(
            INVALID_CONVERSION_METADATA,
            "metadata.prosiform-group must be printable, single-line and nonblank, "
            "without ':' or '/'",
            group.location,
        )
    if not re.fullmatch("[1-6]", depth.value):
        raise _fail(
            INVALID_CONVERSION_METADATA,
            "metadata.prosiform-group-depth must be a string digit from 1 through 6",
            depth.location,
        )
    return Conversion(group.value, int(depth.value), group.location, depth.location)
