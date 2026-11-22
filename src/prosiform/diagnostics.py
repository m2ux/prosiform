"""Diagnostic records and their text and JSON renderings.

`Diagnostic` holds each record, its methods render it, and `Reporter`
writes records to the supplied stream.
"""

import json
from dataclasses import asdict, dataclass
from typing import IO, Any

TEXT = "text"
JSON = "json"
FORMATS = (TEXT, JSON)

ERROR = "error"
WARNING = "warning"

INDENT = "  "
HOP = " → "

CHAIN = "chain"


@dataclass(frozen=True)
class Location:
    """A physical source coordinate: `file`, `line` and `column`."""

    file: str
    line: int
    column: int


@dataclass(frozen=True)
class RelatedLocation(Location):
    """A source coordinate with the `message` explaining its relevance."""

    message: str


@dataclass(frozen=True)
class Diagnostic:
    """One diagnostic record.

    `severity`, `code` and `message` identify the outcome. `reference`
    holds the authored reference, `resolved` its resolved identity and
    `source` the source designator. `chain` holds the inclusion route,
    `remedy` a suggested action, `location` the primary coordinate and
    `related` further annotated coordinates.
    """

    severity: str
    message: str
    code: str
    reference: str | None = None
    resolved: str | None = None
    source: str | None = None
    chain: tuple[str, ...] | None = None
    remedy: str | None = None
    location: Location | None = None
    related: tuple[RelatedLocation, ...] | None = None

    def fields(self) -> dict[str, Any]:
        """The populated fields in declaration order, with sequence data as lists.

        Fields whose value is None are absent; related coordinates are
        represented as mappings.
        """
        carried: dict[str, Any] = {
            name: value for name, value in asdict(self).items() if value is not None
        }
        if self.chain is not None:
            carried[CHAIN] = list(self.chain)
        if self.related is not None:
            carried["related"] = [asdict(item) for item in self.related]
        return carried

    def as_text(self) -> str:
        """The diagnostic as a heading followed by indented detail.

        `fields` supplies the populated values. Chain hops are joined with
        `HOP`; primary and related coordinates follow the other detail.
        """
        carried = self.fields()
        heading = carried.pop("code")
        message = carried.pop("message")
        carried.pop("severity")
        carried.pop("location", None)
        carried.pop("related", None)
        lines = [f"{heading}: {message}"]
        lines += [
            f"{INDENT}{name}: {HOP.join(value) if name == CHAIN else value}"
            for name, value in carried.items()
        ]
        if self.location is not None:
            at = self.location
            lines.append(f"{INDENT}location: {at.file}:{at.line}:{at.column}")
        for at in self.related or ():
            lines.append(
                f"{INDENT}related: {at.file}:{at.line}:{at.column}: {at.message}"
            )
        return "\n".join(lines)

    def as_json(self) -> str:
        """The populated `fields` as one JSON object on one line."""
        return json.dumps(self.fields())


class Reporter:
    """Write diagnostics to a stream in the selected format.

    `stream` is the destination and `format` selects the renderer.
    """

    def __init__(self, stream: IO[str], diagnostic_format: str = TEXT) -> None:
        self.stream = stream
        self.format = diagnostic_format

    def emit(self, diagnostic: Diagnostic) -> None:
        """Write one diagnostic, terminated by a newline of its own."""
        rendered = diagnostic.as_json() if self.format == JSON else diagnostic.as_text()
        self.stream.write(f"{rendered}\n")
        self.stream.flush()
