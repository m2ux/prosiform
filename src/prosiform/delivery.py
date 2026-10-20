"""The delivery wrapper: what it takes for a bundle to count as delivered.

A successful compilation establishes that the complete candidate passed
validation. It does not establish that a transport carried every byte of
it to the calling agent. This module is the wrapper that owns the
difference: it invokes the entry point as a process, buffers the whole of
standard output, reads the outcome from the process status, and holds the
buffered bundle against the response limit the transport declares.

Three outcomes exhaust a completed run. A nonzero status is a build
failure, whatever standard output happened to carry; a bundle larger than
the transport's limit is a delivery failure; and a run that succeeded and
fits is a delivery, which is the one outcome that carries the document.
Neither failure carries a document, a part of one, a summary of one, or a
reference the caller must follow to reach one: substituting any of those
returns a truncated apparent success under another name, and a caller
acting on it acts on a bundle it never received.

The status decides the outcome, and the bytes on standard output are
never read as evidence that a run succeeded. A failing run whose
diagnostics went to the other stream can leave Markdown behind, and a
caller reading that Markdown as success accepts the failure.

The transport names its own response limit, so the wrapper takes one and
declares no default. 256 KiB is the build's own output budget and is not
universally safe for agent delivery, and a limit the wrapper invented
would be enforced in the transport's name without being the transport's.
The limit counts the bytes of the bundle as encoded, because bytes are
what a transport carries; a token figure divided out of a byte count
estimates the budget of a tokenizer nobody named.

Buffering is what makes the whole bundle available to count, and it is
also why the wrapper never breaks the entry point's output pipe. A write
the entry point's own output destination refuses, a broken pipe among
them, is reported by that process as a nonzero status, which reaches the
caller here as the build failure it is.

Completion metadata, byte counts and the run's diagnostics are carried in
the structured result, so the document a caller receives is the bundle the
build published and nothing beside it.
"""

import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

ENCODING = "utf-8"


class Outcome(Enum):
    """What one completed run amounts to for the caller waiting on a bundle."""

    DELIVERED = "delivered"
    BUILD_FAILED = "build failed"
    OVER_TRANSPORT_LIMIT = "over the transport limit"


@dataclass(frozen=True)
class Delivery:
    """One run's structured result: its outcome, its figures and its stream."""

    outcome: Outcome
    status: int
    counted: int
    limit: int
    document: str | None
    diagnostics: str

    @property
    def delivered(self) -> bool:
        """Whether the whole bundle reached the caller."""
        return self.outcome is Outcome.DELIVERED

    def explain(self) -> str:
        """Why the caller has no bundle, or that it has one."""
        if self.outcome is Outcome.DELIVERED:
            return f"delivered {self.counted} bytes within a limit of {self.limit}"
        if self.outcome is Outcome.BUILD_FAILED:
            return f"the run exited {self.status} and published no bundle"
        return (
            f"the bundle is {self.counted} bytes, which the transport's limit of "
            f"{self.limit} cannot carry whole; it is withheld rather than cut"
        )


def received(status: int, output: bytes, diagnostics: str, limit: int) -> Delivery:
    """The delivery one completed run amounts to, from its status and its bytes.

    The order is the contract's. The status is read first, so a run that
    failed is a failure however much Markdown it left on standard
    output. The buffered bytes are then counted against the transport's
    limit, and only a count within it yields a document.
    """
    if limit < 1:
        raise ValueError(
            f"the transport's response limit is {limit}; a limit of nothing "
            f"carries no bundle and does not mean unlimited"
        )
    counted = len(output)
    if status != 0:
        outcome, document = Outcome.BUILD_FAILED, None
    elif counted > limit:
        outcome, document = Outcome.OVER_TRANSPORT_LIMIT, None
    else:
        outcome, document = Outcome.DELIVERED, output.decode(ENCODING)
    return Delivery(outcome, status, counted, limit, document, diagnostics)


def deliver(argv: Sequence[str], limit: int) -> Delivery:
    """Run the entry point to completion and decide what it delivered.

    The process is given no standard input and both of its streams are
    buffered, so the whole bundle is in hand before the limit is held
    against it, and the diagnostic stream is in hand whatever the outcome.
    """
    completed = subprocess.run(
        list(argv),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
    )
    return received(
        completed.returncode,
        completed.stdout,
        completed.stderr.decode(ENCODING, errors="replace"),
        limit,
    )
