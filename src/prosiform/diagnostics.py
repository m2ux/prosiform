"""The diagnostic stream and the two formats it is written in.

A diagnostic is one message a run emits to standard error. It carries a
severity, the stable code of the defect it reports, a message, and the
further fields the contract names where they are known: the reference it
concerns, the destination that reference resolved to, the source location
it was found at, and a remedy where one can be stated accurately. The code
is required because the contract names one for every failing outcome it
declares, so a diagnostic without one would report a defect the contract
does not name.

Text renders a diagnostic for a reader. JSON renders it as data, one object
per line and nothing else on the stream, so a caller parses standard error
without separating records from prose. The format is chosen once, for the
whole run, and every diagnostic the run emits is written in it.
"""

import json
from dataclasses import asdict, dataclass
from typing import IO

TEXT = "text"
JSON = "json"
FORMATS = (TEXT, JSON)

ERROR = "error"
WARNING = "warning"

INDENT = "  "


@dataclass(frozen=True)
class Diagnostic:
    """One message a run emits to standard error."""

    severity: str
    message: str
    code: str
    reference: str | None = None
    destination: str | None = None
    source: str | None = None
    remedy: str | None = None

    def fields(self) -> dict[str, str]:
        """The fields this diagnostic carries, in declaration order."""
        return {
            name: value for name, value in asdict(self).items() if value is not None
        }

    def as_text(self) -> str:
        """The diagnostic as a reader reads it: a heading, then its detail."""
        carried = self.fields()
        heading = carried.pop("code")
        message = carried.pop("message")
        carried.pop("severity")
        lines = [f"{heading}: {message}"]
        lines += [f"{INDENT}{name}: {value}" for name, value in carried.items()]
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
