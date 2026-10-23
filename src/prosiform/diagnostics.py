"""The diagnostic stream and the two formats it is written in.

A diagnostic is one message a run emits to standard error. It carries a
severity, the stable code of the defect it reports, a message, and the
further fields the contract names where they are known: the reference it
concerns, the identity that reference resolved to, the source location it
was found at, the inclusion chain that reached it, and a remedy where one
can be stated accurately. A resolved identity is a bundle destination
where the reference reached one and a canonical source path where it
reached a document. The inclusion chain is the references followed from
an entry reference to the one the diagnostic concerns, each named by the
identity it resolved to, so a caller reading a failure deep in a closure
sees the route the run took to reach it. The code is required because the
contract names one for every failing outcome it declares, so a diagnostic
without one would report a defect the contract does not name.

A field a diagnostic does not carry is a field its defect has no value
for: a command line the grammar refuses names no source, and a run that
failed before resolving anything stands at the end of no chain.

Text renders a diagnostic for a reader. JSON renders it as data, one object
per line and nothing else on the stream, so a caller parses standard error
without separating records from prose. A chain is a sequence, so JSON
carries it as one and text writes its hops in order along a single line.
The format is chosen once, for the whole run, and every diagnostic the run
emits is written in it.
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
    """An original physical source coordinate."""

    file: str
    line: int
    column: int


@dataclass(frozen=True)
class RelatedLocation(Location):
    """A further coordinate explaining the primary diagnostic."""

    message: str


@dataclass(frozen=True)
class Diagnostic:
    """One message a run emits to standard error."""

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
        """The fields this diagnostic carries, in declaration order.

        A chain is a sequence of hops rather than one value, and it is
        carried as the list it is, so a caller reads the route rather
        than parsing a rendering of it.
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
        """The diagnostic as a reader reads it: a heading, then its detail."""
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
        """The diagnostic as data: one JSON object on one line."""
        return json.dumps(self.fields())


class Reporter:
    """Standard error, written in the format the run asked for."""

    def __init__(self, stream: IO[str], diagnostic_format: str = TEXT) -> None:
        self.stream = stream
        self.format = diagnostic_format

    def emit(self, diagnostic: Diagnostic) -> None:
        """Write one diagnostic, terminated by a newline of its own."""
        rendered = diagnostic.as_json() if self.format == JSON else diagnostic.as_text()
        self.stream.write(f"{rendered}\n")
        self.stream.flush()
