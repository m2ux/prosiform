"""The prosiform command: its options, its two streams and its exit statuses.

One invocation names an allowed source root and one or more entry
references, and returns a status naming the category of its outcome.
Standard output carries exactly one thing per run: the bundle a compiling
run publishes, or the response an informational run returns, or nothing at
all. Diagnostics go to standard error in the format the run asked for, so
a caller reads a result from the status and an explanation from a stream
that never carries the bundle.

The command checks the form of every option before it looks for anything
an option names, so an invalid command line is reported as invalid usage
rather than as a fault in a tree it may not even have described correctly.

Every entry reference normalizes to a path identity before anything is
opened: its components split before any escape is decoded, each escape is
validated and decoded exactly once, and `.` and `..` normalize against
the allowed source root. A reference the root cannot contain — one
walking above it, a root-relative or absolute path, a drive path, or a
scheme or authority naming no local document — fails rather than being
opened, and a query, an invalid escape, a control character or a
backslash separator is a command line the grammar does not admit.

The allowed source root is canonicalized once, and every source is read by
descending its normalized path from that directory without following a
link, so the root confines what a run opens rather than what a run spells.
A path reaching a source through a symbolic link below the root fails,
whatever that link points at.

Every entry document the run names is read as bytes, required to be valid
UTF-8, stripped of the transport metadata it carries ahead of its content
and parsed under the declared profile, and selected content carrying a
construct that profile refuses fails as the refusal it is. Every location
a diagnostic reports is the location in the file the author holds,
whatever the strip removed ahead of it.

Validation follows the selection rather than the file. A whole document is
parsed to index it, because heading enumeration, the definitions selected
uses resolve against, the ambiguity of a requested fragment and what a
document opens on are facts about the file; but link resolution,
the profile's refusals and the authored-occurrence budget
are held over the regions the run selected, so a defect in a section
nobody asked for decides no outcome. A section closure later reaches is
selected content like any other, and its defects are then its run's.

A parsing-safety budget is the exception the contract draws: it is held
over the complete opened source, because a parser indexes a whole file
however narrow the requested section is. Crossing one is reported as an
inability to index that source rather than as a dependency on whatever
construct crossed it, since the run reached for no such dependency.

A dependency is a reference that resolves to a Markdown document under
the allowed source root, and the run resolves one against the document
carrying it, reads it and bundles it. Every other reference is text the
bundle carries as its author wrote it: a local Markdown link resolving
outside the root is not resolved further, the document it names is not
opened, and it stays as authored. A reference carrying a scheme or an
authority and one naming a file outside the profile's suffixes are text
by the same rule, and an apparent link inside a code span or a code
block is an example rather than a reference. Position is therefore what
the run follows, and the content a run reads for references is the
content it selected. Traversal repeats over what each round adds until
no round adds anything, so a reference graph with a cycle reaches a
fixed point carrying each reachable region once.

The only thing the run bundles is a local Markdown document, so a
resource is carried as the author wrote it wherever it resolves, the
allowed source root included. An image names a resource whatever file
it points at.

A reference is classified by the identity it resolves to rather than by
the text it was written as. Each link belongs to the innermost eligible
section containing it, and to the document itself where no section
does. A link whose target is the very node that owns it, an including
ancestor of it, or the whole document a section sits in, resolves to
the destination already present and expands nothing; one naming another
section of the same document names a second identity and carries it.
Ownership is read from the document's structure rather than from what a
run selected, so consolidating a section into a larger region leaves
every classification as it was.

Each reference the run compiled is rewritten to the destination the
bundle gave the target it resolved to, and a mark goes with the
rewrite; a reference the run did not compile keeps every byte its
author wrote, a mark included. A
destination belongs to the bundle rather than to a group, so the map
holding one is known only once every group exists: the groups are
built to learn the headings the bundle emits, and built again through
the map those headings produce. The candidate is then read back and
its headings compared with that map, so a bundle is published only
where each destination it carries resolves to exactly one heading in
it.

Each budget the profile declares is counted as the design states and
fails the compilation at the first boundary it crosses, with nothing
truncated and no bundle published. One code reports every crossing and
the message names the budget and the figure that crossed it.

A reference with no fragment, or with an empty one, selects the whole
document. A reference carrying a nonempty fragment selects the section
that fragment names, which runs to the next document-level heading of
equal or higher level; a fragment alone selects from the document
`--from` names. Each document a run selects from carries every region
the run's references selected from it into one group of the bundle: its
own file group, or the merged group a grouping rule puts it in with the
other documents under a directory of that slug. The groups are ordered
by root-relative path, a merged group taking the first of its members'.
A fragment naming
a heading a container carries names no section and fails as an
unsupported target; one naming no heading of its document names
nothing, and fails as the reference to a missing target it is.

A source opening on a document-level H1 whose text, with a supported
Markdown suffix appended, names another document under the allowed
source root is refused as output offered as input. The document being
read is not that other document, so a title a document's own path
spells points at itself and bundles, and a heading-like line inside
code is no heading at all. Detection is read from the complete source,
because what a document opens on is a fact about the file rather than
about the regions a run selected.

Every source is captured at discovery as the canonical path its read
arrived at and a hash of the bytes it held, and the whole set is
rechecked once the candidate is built and before anything publishes. A
source that changed, disappeared or resolved elsewhere fails the run,
which publishes nothing and asks for a retry. The recheck is change
detection between the two reads: a source can be written again after
it, and a hash taken over one file at a time supplies no atomicity
across the set, so a run needing strict reproducibility bundles from a
snapshot made immutable outside this tool.

The bundle is published once the whole candidate is built. A
validation-only run publishes nothing, to either stream or to a named
file; a run naming an output file writes it atomically, through a
neighbouring temporary file renamed into place, so a reader of that path
sees the previous bytes or the whole bundle and never a partial one.

An output path naming a source the run read is refused. The comparison
is made over the completed closure, which is where the full set of
paths a run read is known, so a document the run reached as a
dependency is a document the run will not write over. Each source is
located at its root-relative path under the canonicalized root and
never through a symbolic link, because the read follows no link and a
resolution would name a file the run never opened.
"""

import argparse
import os
import re
import sys
import tempfile
from collections.abc import Collection, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, replace
from importlib.metadata import version
from pathlib import Path, PurePosixPath
from typing import IO, Any, NoReturn

from markdown_it.token import Token

from prosiform import PROFILE
from prosiform.access import (
    Absent,
    Symlinked,
    Unreadable,
    present,
    read_source,
)
from prosiform.bundle import (
    AMBIGUOUS_FILE_GROUP,
    HEADING_DEPTH_OVERFLOW,
    MAX_LEVEL,
    Group,
    Overflow,
    assemble,
    entry_line,
    group,
    heading_text,
)
from prosiform.candidate import UNSAFE_BUNDLE_BOUNDARY, Unsafe, validate
from prosiform.closure import (
    DRIVE,
    Malformed,
    OutsideRoot,
    Reference,
    components,
    external,
    identity,
    inside,
    resolve,
)
from prosiform.diagnostics import (
    ERROR,
    FORMATS,
    TEXT,
    WARNING,
    Diagnostic,
    Reporter,
)
from prosiform.grouping import merged, prepared
from prosiform.limits import (
    BUDGETS,
    EXPANSION_DEPTH,
    FILE_BYTES,
    FILES,
    INPUT_BYTES,
    LINKS,
    NESTING,
    OUTPUT_BYTES,
    RESOURCE_LIMIT,
    TARGETS,
    Crossed,
    Limits,
)
from prosiform.profile import (
    REFERENCES,
    SUFFIXES,
    Refusal,
    is_markdown,
    parse,
    refusals,
)
from prosiform.rewrite import Definition, definitions
from prosiform.source import (
    AMBIGUOUS_SOURCE_HEADING,
    CLOSERS,
    ENCODING,
    HREF,
    INLINE,
    NESTED_SECTION_TARGET,
    REFERENCE_USES,
    SRC,
    UNTERMINATED_FRONTMATTER,
    Ambiguous,
    Capture,
    Nested,
    Selection,
    Source,
    Unterminated,
    content,
    decode,
    fragments,
    hashed,
    lines,
    nesting,
    occurrences,
    opening_heading,
    regions,
    section,
    uses,
    within,
)

NAME = "prosiform"

SUCCESS = 0
INPUT_FAILURE = 1
USAGE_FAILURE = 2
PUBLICATION_FAILURE = 3
INTERNAL_ERROR = 4

STANDARD_OUTPUT = "-"

MIN_DEPTH = 1
MAX_DEPTH = 6

GENERATED_INPUT = "E_GENERATED_INPUT"
INVALID_ENCODING = "E_INVALID_ENCODING"
INVALID_GROUP_RULE = "E_INVALID_GROUP_RULE"
INVALID_USAGE = "E_INVALID_USAGE"
PUBLICATION_FAILED = "E_PUBLICATION_FAILED"
ROOT_NOT_FOUND = "E_ROOT_NOT_FOUND"
SOURCE_CHANGED = "E_SOURCE_CHANGED"
SOURCE_OUTSIDE_ROOT = "E_SOURCE_OUTSIDE_ROOT"
SOURCE_SYMLINK = "E_SOURCE_SYMLINK"
TARGET_NOT_FOUND = "E_TARGET_NOT_FOUND"
UNEXPECTED_INTERNAL_ERROR = "E_UNEXPECTED_INTERNAL_ERROR"
UNSUPPORTED_ENTRY_SUFFIX = "E_UNSUPPORTED_ENTRY_SUFFIX"

ENTRY_DESTINATION = "W_ENTRY_DESTINATION"
RESOURCE_PORTABILITY = "W_RESOURCE_PORTABILITY"

GROUP_RULE = re.compile(r"^([^:/]+):([0-9]+)$")
DECIMAL = re.compile(r"^[0-9]+$")
DIAGNOSTICS_OPTION = "--diagnostics"

EXIT_STATUSES = """exit statuses:
  0  successful compilation, validation, or informational response
  1  input, dependency, policy, safety, or resource-limit failure
  2  invalid usage or option combination
  3  output publication or delivery failure, a broken pipe among them
  4  unexpected internal error
"""


class Failure(Exception):
    """One outcome the contract names, and the status that outcome returns."""

    def __init__(self, status: int, diagnostic: Diagnostic) -> None:
        super().__init__(diagnostic.message)
        self.status = status
        self.diagnostic = diagnostic


def usage_failure(
    message: str, code: str = INVALID_USAGE, reference: str | None = None
) -> Failure:
    """A command line the contract's grammar does not admit.

    Every such fault leads a caller to one remedy, so they share one
    code. A grouping rule is the exception the contract itself draws: its
    code names a defect in the rule's value, which the same code reports
    as an input failure when the slug names no directory.
    """
    return Failure(
        USAGE_FAILURE,
        Diagnostic(
            ERROR,
            message,
            code=code,
            reference=reference,
            remedy=f"run {NAME} --help for usage",
        ),
    )


def input_failure(
    message: str,
    code: str,
    remedy: str = "",
    reference: str | None = None,
    resolved: str | None = None,
    source: str | None = None,
    chain: Sequence[str] = (),
) -> Failure:
    """A command line that is well formed and names something the run refuses.

    The evidence a failure carries is the evidence it has: a reference
    the run resolved far enough to name a document carries that
    identity, and one the traversal reached through other references
    carries the chain of them.
    """
    return Failure(
        INPUT_FAILURE,
        Diagnostic(
            ERROR,
            message,
            code=code,
            reference=reference,
            resolved=resolved,
            source=source,
            chain=tuple(chain) or None,
            remedy=remedy or None,
        ),
    )


def crossing(crossed: Crossed) -> Failure:
    """One crossed budget, as the input failure the contract declares it.

    Every budget takes one code, because whichever was crossed the
    remedy is the same shape, and the message names the boundary and
    the figure that crossed it so a caller knows which to act on.
    """
    return input_failure(str(crossed), code=RESOURCE_LIMIT, remedy=crossed.remedy)


def unindexable(crossed: Crossed, path: str, chain: Sequence[str]) -> Failure:
    """One budget crossed while indexing a source, as the failure to index it.

    A parsing-safety budget is held over the complete opened source, so
    the construct that crosses one sits wherever the author wrote it and
    the run selected nothing by reading it. Reporting a dependency would
    name a reference the run never followed and send an author to look
    for one, so the diagnostic names the source that cannot be indexed
    and the route the run took to open it.
    """
    return input_failure(
        f"the source {path!r} cannot be safely indexed: {crossed}",
        code=RESOURCE_LIMIT,
        remedy=crossed.remedy,
        reference=path,
        source=path,
        chain=chain,
    )


class Parser(argparse.ArgumentParser):
    """An argument parser whose grammar failures are the command's own."""

    def error(self, message: str) -> NoReturn:
        raise usage_failure(message)


def override(value: str) -> int:
    """One budget override, which is a positive decimal integer and nothing else.

    Zero is refused rather than read as unlimited: a budget exists to
    be crossed, and a caller wanting a larger one names the number. A
    value written in any other notation is a command line the grammar
    does not admit.
    """
    if DECIMAL.match(value) is None or int(value) < 1:
        raise argparse.ArgumentTypeError(
            f"{value!r} is no positive decimal integer; zero is not unlimited"
        )
    return int(value)


def budgets(options: argparse.Namespace) -> Limits:
    """Every budget in force, as the command line left it."""
    return Limits({budget: getattr(options, budget.dest) for budget in BUDGETS})


def parser() -> Parser:
    """The command's grammar: every option the contract declares, and no other."""
    grammar = Parser(
        prog=NAME,
        add_help=False,
        usage=f"{NAME} --root DIR [OPTIONS] REF [REF ...]",
        description=(
            "Bundle the local Markdown closure of one or more entry references "
            "into one validated document."
        ),
        epilog=EXIT_STATUSES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    grammar.add_argument(
        "--root",
        metavar="DIR",
        help="the allowed source root; required, and resolved from the "
        "working directory",
    )
    grammar.add_argument(
        "--from",
        dest="referrer",
        metavar="DOC",
        help="the root-relative referring document a fragment-only reference "
        "resolves against",
    )
    grammar.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        default=STANDARD_OUTPUT,
        help="publish the validated bundle to FILE, atomically; "
        "default or - is standard output",
    )
    grammar.add_argument(
        "--group",
        metavar="SLUG:DEPTH",
        action="append",
        default=[],
        help="merge every document under a directory named SLUG at source "
        "heading level DEPTH, 1 through 6; repeatable, once per slug",
    )
    grammar.add_argument(
        "--check",
        action="store_true",
        help="discover, bundle and validate without emitting or publishing "
        "the bundle; accepted with --output",
    )
    grammar.add_argument(
        "--diagnostics",
        choices=FORMATS,
        default=TEXT,
        help=f"the diagnostic format on standard error; default {TEXT}",
    )
    for budget in BUDGETS:
        grammar.add_argument(
            budget.option,
            metavar="N",
            type=override,
            default=budget.default,
            help=f"the budget of {budget.counted}; "
            f"a positive decimal integer, default {budget.default}",
        )
    grammar.add_argument(
        "--version",
        action="store_true",
        help="report the tool version and the profile identifier",
    )
    grammar.add_argument(
        "--help",
        action="store_true",
        help="show this usage, the defaults, and the exit-status meanings",
    )
    grammar.add_argument(
        "references",
        metavar="REF",
        nargs="*",
        help="an entry reference: a root-relative document, a document and a "
        "fragment, or a fragment alone with --from",
    )
    return grammar


def diagnostic_format(arguments: Sequence[str]) -> str:
    """The format the command line asks for, read before the grammar is checked.

    A usage failure is written in the format the run asked for, so the
    format is known before the grammar decides whether the run is valid. A
    value the contract does not declare leaves the default standing; the
    grammar then reports it as the usage failure it is.
    """
    selected = TEXT
    for index, token in enumerate(arguments):
        if token == DIAGNOSTICS_OPTION and index + 1 < len(arguments):
            value = arguments[index + 1]
        elif token.startswith(f"{DIAGNOSTICS_OPTION}="):
            value = token.partition("=")[2]
        else:
            continue
        if value in FORMATS:
            selected = value
    return selected


def rule(declaration: str) -> tuple[str, int]:
    """One grouping rule, as the slug and depth it declares."""
    written = GROUP_RULE.match(declaration)
    if written is None:
        raise usage_failure(
            f"the grouping rule {declaration!r} is not a directory slug and a "
            f"depth separated by a colon",
            code=INVALID_GROUP_RULE,
        )
    slug, depth = written.group(1), int(written.group(2))
    if not MIN_DEPTH <= depth <= MAX_DEPTH:
        raise usage_failure(
            f"the grouping rule {declaration!r} names depth {depth}, which is "
            f"outside {MIN_DEPTH} through {MAX_DEPTH}",
            code=INVALID_GROUP_RULE,
        )
    return slug, depth


def rules(declarations: Sequence[str]) -> dict[str, int]:
    """Every grouping rule in force, each slug named once."""
    inforce: dict[str, int] = {}
    for declaration in declarations:
        slug, depth = rule(declaration)
        if slug in inforce:
            raise usage_failure(
                f"the grouping rule {declaration!r} names {slug!r}, which "
                f"another rule already names",
                code=INVALID_GROUP_RULE,
            )
        inforce[slug] = depth
    return inforce


def entry(text: str) -> Reference:
    """One entry reference, normalized to the document identity it names.

    An entry names a document under the allowed source root, so a
    reference the root cannot contain fails here rather than being
    opened. A scheme and an authority name no local document at all,
    which is the one form the resolution sequence classifies rather than
    refuses: inside a source such a reference is text the bundle
    carries, and on the command line it names nothing to bundle.

    This is the one place the root's confinement is a refusal. The root
    binds what the caller asks the run to carry out, and a reference an
    author wrote inside a source is that author citing material the
    bundle does not carry, so discovery leaves it as text and nothing
    downstream of here raises the code again.
    """
    try:
        found = resolve(text)
    except Malformed as malformed:
        raise usage_failure(
            f"the entry reference {text!r} {malformed}", reference=text
        ) from malformed
    except OutsideRoot as outside:
        raise input_failure(
            f"the entry reference {text!r} {outside}",
            code=SOURCE_OUTSIDE_ROOT,
            remedy="name a document the source root carries",
            reference=text,
        ) from outside
    if found.external:
        raise input_failure(
            f"the entry reference {text!r} carries a scheme or an authority, so it "
            f"names no document the allowed source root can contain",
            code=SOURCE_OUTSIDE_ROOT,
            remedy="name a document the source root carries",
            reference=text,
        )
    return found


def entered(
    referrer: Reference | None, requested: Sequence[Reference]
) -> list[Reference]:
    """Each entry reference standing at the head of the chain it opens.

    An entry reference is reached by nothing, so the chain a
    diagnostic about it carries is the one identity it names. A
    fragment alone names a section of the referring document, which is
    the base its identity is written against.
    """
    base = referrer.path if referrer is not None else ""
    return [replace(one, chain=(identity(one, base),)) for one in requested]


def sources(root: Path, read: Collection[str]) -> set[Path]:
    """Where every source the run read sits, under the allowed source root.

    A source is located by joining its root-relative path to the
    canonicalized root and by nothing further. The read descends that
    path one segment at a time and follows no link, so each segment
    names the directory entry the walk opened and the join is already
    the file the bytes came from. A resolution through a symbolic link
    would instead name a file the run never read, and a comparison
    against that file answers a question about the link rather than
    about the source.
    """
    return {root / path for path in read}


def location(name: str, at: int | None) -> str:
    """One source location: the document, and the line where the parser knows one."""
    return name if at is None else f"{name}:{at}"


@dataclass(frozen=True)
class Opened:
    """One source as the run opened it: its content, its size and what it was.

    A byte budget is declared over what the file holds, frontmatter and
    any byte-order mark included, so the figure is taken at the read
    and not from the content the strip returned. The capture is taken
    there too, over the same bytes and the path they came from, so the
    recheck before publication compares a later read against the read
    the bundle was built from.
    """

    source: Source
    size: int
    capture: Capture


def canonical(root: Path, path: str) -> str:
    """Where one root-relative source path resolves on the filesystem.

    The allowed source root is canonicalized once and the read follows
    no link, so the path a discovery resolves is the file whose bytes
    the run holds. A later resolution naming somewhere else says the
    source now resolves elsewhere.
    """
    return os.path.realpath(root / path)


def read_document(root: Path, found: Reference) -> Opened:
    """One document's content, read under the allowed source root.

    A refusal is worded for the reference that asked for the document
    and located where that reference is written, so a run says which
    link it could not follow and which document carries it.

    The read descends the normalized path from the canonicalized root one
    segment at a time and follows no link, so a reference reaching a
    source through a symbolic link below the root fails rather than
    arriving at whatever that link points at.

    What arrives here is a path a normalization produced, which the root
    can hold: one that walks above its base raises before a path is
    returned, and the entry reference carrying it is refused where
    entries are read. The refusals below are therefore the faults a read
    meets. A walk declining a segment of such a path is this tool's own
    invariant breaking, which the declared internal-error status reports.

    The bytes are read without newline translation, so a CRLF source
    reaches the scan spelled as the file spells it, and they are decoded
    strictly, so a source that is not valid UTF-8 fails here as the source
    defect it is rather than reaching the command's generic handler.
    """
    reference, name = found.original, found.path
    written = "the entry reference" if found.origin is None else "the reference"
    chain = found.chain
    if not is_markdown(name):
        raise input_failure(
            f"the entry reference {reference!r} names a document whose suffix is "
            f"outside the {PROFILE} profile",
            code=UNSUPPORTED_ENTRY_SUFFIX,
            remedy=f"name a document ending {' or '.join(SUFFIXES)}",
            reference=reference,
            chain=chain,
        )
    try:
        data = read_source(root, name)
    except Symlinked as linked:
        raise input_failure(
            f"{written} {reference!r} reaches its source through {linked}, "
            f"a symbolic link below the allowed source root",
            code=SOURCE_SYMLINK,
            remedy="name the document the link points at, under the source root",
            reference=reference,
            source=found.origin,
            chain=chain,
        ) from linked
    except Absent as absent:
        raise input_failure(
            f"{written} {reference!r} names no document under the allowed source root",
            code=TARGET_NOT_FOUND,
            remedy="name a document the source root carries",
            reference=reference,
            source=found.origin,
            chain=chain,
        ) from absent
    try:
        text = decode(data)
    except UnicodeDecodeError as undecodable:
        raise input_failure(
            f"{written} {reference!r} names a document that is not valid "
            f"{ENCODING.upper()}: byte {undecodable.start}, "
            f"{undecodable.reason}",
            code=INVALID_ENCODING,
            remedy=f"save the document as {ENCODING.upper()}",
            reference=reference,
            source=name,
            chain=chain,
        ) from undecodable
    captured = Capture(canonical(root, name), hashed(data))
    try:
        return Opened(content(text), len(data), captured)
    except Unterminated as unclosed:
        raise input_failure(
            f"{written} {reference!r} names a document whose frontmatter "
            f"opener is closed by no later line of exactly "
            f"{' or '.join(CLOSERS)}",
            code=UNTERMINATED_FRONTMATTER,
            remedy=f"close the block with a line of exactly {' or '.join(CLOSERS)}",
            reference=reference,
            source=location(name, unclosed.line),
            chain=chain,
        ) from unclosed


def refused(
    name: str, source: Source, refusal: Refusal, chain: Sequence[str]
) -> Failure:
    """One construct the profile refuses, reported against the source carrying it.

    The line the parser reports is a line of the content the strip
    returned, and the line the diagnostic carries is the line that content
    occupies in the file. The chain is the one that reached the source,
    because the construct is where the run arrived rather than something
    a further reference named.
    """
    return input_failure(
        refusal.message,
        code=refusal.code,
        remedy=refusal.remedy,
        reference=refusal.reference,
        source=location(name, source.line(refusal.line)),
        chain=chain,
    )


def named_document(root: Path, read: str, title: str) -> str | None:
    """The document one file heading's text names, other than the one carrying it.

    A file heading is a root-relative path with its Markdown suffix
    removed, so its text names a document when a supported suffix
    appended to it reaches one under the allowed source root. The
    document being read is not that document: a title a document's own
    path spells points at itself, which is the absorbed title's worked
    example and names no other source.
    """
    for suffix in SUFFIXES:
        named = f"{title}{suffix}"
        if named != read and present(root, named):
            return named
    return None


def generated(
    root: Path,
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chain: Sequence[str],
) -> None:
    """Refuse one source that opens on another document's file heading.

    A published bundle carries generated file headings and rewritten
    links, so bundling it again would rewrite generated structure as if
    an author had written it. The file heading is the signal, and the
    whole of it: it is no proof of origin, rewriting it defeats the
    detection, and a bundle whose every group is merged is headed by a
    directory slug and carries no file heading to read. What the
    heading does establish is that this document opens by naming
    another document under the root, which is what output read back as
    input does.

    The reading is of the complete source, because what a document
    opens on is a fact about the file rather than about the regions a
    run selected.
    """
    first = opening_heading(tokens)
    if first is None:
        return
    named = named_document(root, path, first.text)
    if named is None:
        return
    raise input_failure(
        f"{path!r} opens on the file heading {first.text!r}, which names the "
        f"document {named!r} under the allowed source root, so it is output "
        f"offered as input",
        code=GENERATED_INPUT,
        remedy="bundle the sources the document was built from",
        reference=first.text,
        source=location(path, source.line(first.line)),
        chain=chain,
    )


def changed(path: str, what: str, chain: Sequence[str]) -> Failure:
    """One source that is no longer the source the run read."""
    return input_failure(
        f"the source {path!r} {what}, so the bundle would carry bytes the run "
        f"no longer reads",
        code=SOURCE_CHANGED,
        remedy="run the compilation again, over sources nothing is writing",
        reference=path,
        source=path,
        chain=chain,
    )


def unsafe(boundary: Unsafe, chain: Sequence[str]) -> Failure:
    """One bundle boundary that would place content inside an unintended container.

    The defect is in the documents the run was asked to bundle
    together rather than in the tool, so it is reported as the input
    failure it is: the boundary names the source regions either side
    of it and the container that absorbed one into the other, and the
    reference is the source whose region opens that container, which
    is the document to change.
    """
    return input_failure(
        str(boundary),
        code=UNSAFE_BUNDLE_BOUNDARY,
        remedy=boundary.remedy,
        reference=boundary.path,
        source=boundary.path,
        chain=chain,
    )


def recheck(
    root: Path, captured: dict[str, Capture], chains: dict[str, tuple[str, ...]]
) -> None:
    """Hold every source the run read to still being the source it read.

    Each source is read again and compared against the canonical path
    it resolved to and the hash of the bytes it held. A source that
    changed, disappeared or resolved elsewhere fails the run, and the
    remedy is to run it again.

    This is change detection. It establishes that a source differs from
    what discovery read, between that read and this one, and nothing
    beyond: a source can be written again after the comparison, and a
    hash taken over one file at a time states nothing about the set of
    them together. A run needing strict reproducibility bundles from a
    source snapshot made immutable outside this tool.
    """
    for path in sorted(captured):
        was = captured[path]
        try:
            data = read_source(root, path)
        except Unreadable as unreadable:
            raise changed(
                path,
                f"is no longer a document the allowed source root yields: {unreadable}",
                chains.get(path, ()),
            ) from unreadable
        now = canonical(root, path)
        if now != was.identity:
            raise changed(
                path,
                f"resolves to {now!r} rather than {was.identity!r}",
                chains.get(path, ()),
            )
        if hashed(data) != was.digest:
            raise changed(
                path,
                "holds content other than the bytes the run read",
                chains.get(path, ()),
            )


def directories(root: Path) -> set[str]:
    """The name of every directory under the allowed source root."""
    found: set[str] = set()
    for _, below, _ in os.walk(root):
        found.update(below)
    return found


def contributing(
    referrer: Reference | None, requested: Sequence[Reference]
) -> dict[str, list[Reference]]:
    """Each file group the bundle carries, by the path that names it.

    A reference naming a document selects from that document, and a
    fragment alone selects from the document `--from` names. The path
    is the identity the reference normalized to, so two references
    spelling one document name one group, which carries what each of
    them selected, and the groups are ordered by root-relative path so
    one selection always bundles to the same bytes.
    """
    selected: dict[str, list[Reference]] = {}
    for one in requested:
        name = one.path or (referrer.path if referrer is not None else "")
        selected.setdefault(name, []).append(one)
    return dict(sorted(selected.items()))


def reaching(selected: dict[str, list[Reference]]) -> dict[str, tuple[str, ...]]:
    """The inclusion chain that reached each document the bundle carries.

    A document several references select is reached by each of them,
    and the one the chain names is the first the traversal discovered,
    which is the shortest route to it. A diagnostic about the document
    rather than about one reference into it — a construct the profile
    refuses, a boundary two regions make unsafe — names that route.
    """
    return {
        path: selecting[0].chain for path, selecting in selected.items() if selecting
    }


def selection(
    path: str,
    tokens: Sequence[Token],
    references: Sequence[Reference],
    entries: Collection[Reference],
) -> Selection | None:
    """What one source contributes, as the references naming it select it.

    A reference with no fragment selects every region the document
    holds. A fragment is the section name the normalization decoded, so
    the heading it is looked up against is the text the author wrote
    however the reference spelled it. Every fragment is resolved
    whatever else the run selected, because a fragment naming no
    heading names nothing however much of its document reaches the
    bundle.

    An entry reference is one the caller named, and the entry line
    links what the caller asked for, so only the heading an entry
    resolved to stays identifiable. A whole document an entry selected
    and nothing else named is the selection `None`, whose entry is the
    file heading; a whole document only a dependency selected enters
    the entry line not at all.

    A fragment the document does not yield is a reference that reached
    a document and no section of it, so its diagnostic names that
    document as the identity it resolved to and the chain that reached
    the reference.
    """
    wanted: set[int] = set()
    named: list[Token] = []
    whole = False
    entered = False
    for one in references:
        spelled = one.fragment
        if spelled is None:
            whole = True
            entered = entered or one in entries
            continue
        try:
            found = section(tokens, spelled)
        except Ambiguous as shared:
            raise input_failure(
                f"the reference {one.original!r} names {len(shared.lines)} headings "
                f"of the document it selects from, which it cannot tell apart",
                code=AMBIGUOUS_SOURCE_HEADING,
                remedy="retitle one of the headings so each takes a slug of its own",
                reference=one.original,
                resolved=path,
                source=one.origin,
                chain=one.chain,
            ) from shared
        except Nested as nested:
            raise input_failure(
                f"the reference {one.original!r} names a heading a container "
                f"carries, which is no selectable section root",
                code=NESTED_SECTION_TARGET,
                remedy="name a heading the document carries at its own level",
                reference=one.original,
                resolved=path,
                source=one.origin,
                chain=one.chain,
            ) from nested
        if found is None:
            raise input_failure(
                f"the reference {one.original!r} names no heading of the document "
                f"it selects from",
                code=TARGET_NOT_FOUND,
                remedy="name a heading the document carries",
                reference=one.original,
                resolved=path,
                source=one.origin,
                chain=one.chain,
            )
        if one in entries:
            named.append(found[0])
        wanted.update(id(token) for token in found)
    if whole:
        if not named and entered:
            return None
        return Selection(tuple(regions(tokens)), tuple(named))
    return Selection(
        tuple(token for token in regions(tokens) if id(token) in wanted), tuple(named)
    )


def required(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
) -> Iterator[Reference]:
    """Every dependency the selected content of one source carries.

    A use resolving to a Markdown document under the allowed source
    root is a reference the bundle carries, and every other use is
    text: a mention leaving the root is not resolved further, the
    document it names is not opened, and the link reaches the bundle as
    its author wrote it. Where the reference resolves is the whole of
    the question, so an author states what the bundle must carry by
    where the target sits.

    A resource is no local Markdown document and an image is a
    resource whatever it points at, so neither is a dependency and both
    reach the bundle as their author wrote them, wherever they resolve.
    Only a Markdown document is bundleable, so nothing a resource
    reference carries asks for one.

    A reference whose form the grammar does not admit, and which names
    a Markdown document, is a defect rather than a mention: an author
    spelled a dependency the profile cannot resolve.

    A reference naming the node that owns it, an including ancestor of
    it, or the whole document a section sits in, names a destination the
    bundle already carries, and the traversal reaches it as it reaches
    any identity it has seen. Identity is what the frontier closes over,
    so a reference pointing back adds nothing to it and expands nothing
    twice.

    The chain passed in is the one that reached this source, and every
    reference the source carries stands one hop beyond it. A reference
    refused here therefore reports the route the run followed to the
    link, which is what an author needs to find the document that wrote
    it.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        at = location(path, source.line(use.line))
        route = (*chain, use.destination)
        if use.resource:
            continue
        try:
            found = inside(path, use.destination)
        except OutsideRoot:
            continue
        except Malformed as malformed:
            if not is_markdown(components(use.destination).path):
                continue
            raise input_failure(
                f"the reference {use.destination!r} {malformed}",
                code=TARGET_NOT_FOUND,
                remedy="write the dependency as a reference the profile resolves",
                reference=use.destination,
                source=at,
                chain=route,
            ) from malformed
        if found.external or not is_markdown(found.path):
            continue
        yield replace(found, origin=at, chain=(*chain, identity(found)))


def traverse(
    root: Path,
    referrer: Reference | None,
    requested: Sequence[Reference],
    limits: Limits,
) -> tuple[
    dict[str, Source],
    dict[str, list[Token]],
    dict[str, dict[str, Definition]],
    dict[str, Capture],
    list[Reference],
]:
    """Every source the run reads and every reference it carries, at the fixed point.

    The entry references are the first frontier. Each round reads the
    sources its frontier names, then reads every group's selected
    content for the dependencies it marks; a dependency naming a
    document and section the run already carries adds nothing, and the
    round that discovers no new one is the fixed point. A reference
    graph with a cycle therefore terminates on the identity each
    reference normalized to rather than on a depth the traversal
    refuses at.

    The selection of a group grows as later content marks more of its
    document, so every group is read again each round. What the
    traversal returns is what the bundle is composed from, so the
    bundle follows from the closure rather than from the order its
    documents were discovered in.

    Each reference carries the chain that reached it, which is the
    chain of the first reference naming the document the link was
    written in and the reference's own identity after it. That first
    reference is the one the shortest route arrived by, because the
    rounds discover a document at the hop its nearest entry reference
    reaches it in.

    Reading a document and validating what it contributes are two
    stages, and the selection divides them. Opening a source holds the
    facts the whole file decides — its bytes, its nesting, what it
    opens on, the definitions it declares — and a parsing-safety
    budget crossed there is the source failing to index rather than a
    dependency. The round then reads each group's selected regions for
    the dependencies they mark and the constructs the profile refuses
    there, so an unselected section is content the run parsed and
    never asked for. A selection only grows, so a region a later round
    adds is held to the same checks in the round that adds it.

    A round is one link hop: an entry reference stands at no hops, and
    a reference a round discovers stands at that round's number. A
    selection only grows, so the round a reference is first discovered
    in is the shortest path from the nearest entry reference to it,
    which is what the expansion-depth budget is declared over. The
    budgets over what the run opens, counts and reaches are held here
    as each figure is reached, so a run crosses a boundary at the point
    it crosses it rather than after building what it could not keep.
    """
    read: dict[str, Source] = {}
    parsed: dict[str, list[Token]] = {}
    defined: dict[str, dict[str, Definition]] = {}
    captured: dict[str, Capture] = {}
    found = list(requested)
    seen = {(one.path, one.fragment) for one in found}
    limits.hold(TARGETS, len(seen))
    counted: dict[str, int] = {}
    total = 0
    hop = 0
    frontier = ([referrer] if referrer is not None else []) + list(requested)
    while frontier:
        hop += 1
        for one in frontier:
            if not one.path or one.path in read:
                continue
            opened = read_document(root, one)
            source = opened.source
            environment: dict[str, Any] = {}
            try:
                limits.hold(FILE_BYTES, opened.size)
                tokens = parse(source.text, limits.of(NESTING), environment)
                limits.hold(NESTING, nesting(tokens))
            except Crossed as crossed:
                raise unindexable(crossed, one.path, one.chain) from crossed
            total += opened.size
            limits.hold(INPUT_BYTES, total)
            generated(root, one.path, source, tokens, one.chain)
            read[one.path] = source
            captured[one.path] = opened.capture
            parsed[one.path] = tokens
            defined[one.path] = definitions(
                environment.get(REFERENCES, {}), lines(source.text)
            )
            limits.hold(FILES, len(read))
        discovered: list[Reference] = []
        for path, selecting in contributing(referrer, found).items():
            chosen = selection(path, parsed[path], selecting, requested)
            regions_read = (
                tuple(regions(parsed[path])) if chosen is None else chosen.regions
            )
            counted[path] = occurrences(parsed[path], regions_read)
            limits.hold(LINKS, sum(counted.values()))
            reached = selecting[0].chain
            refusal = next(refusals(within(parsed[path], regions_read)), None)
            if refusal is not None:
                raise refused(path, read[path], refusal, reached)
            for one in required(path, read[path], parsed[path], chosen, reached):
                if (one.path, one.fragment) in seen:
                    continue
                limits.hold(EXPANSION_DEPTH, hop)
                seen.add((one.path, one.fragment))
                limits.hold(TARGETS, len(seen))
                discovered.append(one)
        found.extend(discovered)
        frontier = discovered
    return read, parsed, defined, captured, found


def membership(path: str, inforce: Mapping[str, int]) -> str | None:
    """The slug of the group one document belongs to, where a rule names one.

    A document belongs to the group whose slug matches the deepest
    directory segment of its path, so a rule naming an inner directory
    takes precedence over one naming a directory above it. A document
    no rule matches keeps its own file group.
    """
    return next(
        (
            segment
            for segment in reversed(PurePosixPath(path).parts[:-1])
            if segment in inforce
        ),
        None,
    )


def unambiguous(
    selected: dict[str, list[Reference]], inforce: Mapping[str, int]
) -> None:
    """Hold each file heading to naming one source, as a reader must read it.

    A merged group is headed by its directory slug rather than by a
    path, so a member of one heads no file group and two members
    sharing a title are told apart by the names the arrangement gives
    them.
    """
    headed: dict[str, str] = {}
    for path, selecting in selected.items():
        if membership(path, inforce) is not None:
            continue
        title = heading_text(path)
        if title in headed:
            raise input_failure(
                f"{path!r} and {headed[title]!r} both head a file group {title!r}, "
                f"which a reader cannot tell apart",
                code=AMBIGUOUS_FILE_GROUP,
                remedy="bundle one of the two, or rename one of the documents",
                reference=path,
                chain=selecting[0].chain,
            )
        headed[title] = path


def assembled(
    read: dict[str, Source],
    parsed: dict[str, list[Token]],
    defined: dict[str, dict[str, Definition]],
    selected: dict[str, list[Reference]],
    entries: Collection[Reference],
    assigned: dict[tuple[str, str | None], str] | None,
    inforce: Mapping[str, int],
) -> list[Group]:
    """Each group the bundle carries, its links rewritten where a map says so.

    A document no grouping rule names is its own file group. Every
    other document joins the merged group its slug names, which carries
    its members in root-relative path order. The groups are ordered by
    root-relative path, a merged group taking the first of its
    members', so one selection always bundles to the same bytes.
    """
    groups: list[Group] = []
    merging: dict[str, list[str]] = {}
    for path, selecting in selected.items():
        named = membership(path, inforce)
        if named is not None:
            merging.setdefault(named, []).append(path)
            continue
        tokens = parsed[path]
        with overflowing(path, selecting):
            groups.append(
                group(
                    path,
                    tokens,
                    lines(read[path].text),
                    defined[path],
                    selection(path, tokens, selecting, entries),
                    assigned,
                )
            )
    for named, paths in merging.items():
        depth = inforce[named]
        with overflowing(paths[0], selected[paths[0]]):
            groups.append(
                merged(
                    named,
                    depth,
                    [
                        prepared(
                            path,
                            parsed[path],
                            lines(read[path].text),
                            defined[path],
                            selection(path, parsed[path], selected[path], entries),
                            assigned,
                            depth,
                        )
                        for path in paths
                    ],
                )
            )
    return sorted(groups, key=lambda one: one.order)


@contextmanager
def overflowing(path: str, selecting: Sequence[Reference]) -> Iterator[None]:
    """One assembly, a heading beyond the sixth level reported as the input it is."""
    try:
        yield
    except Overflow as beyond:
        raise input_failure(
            f"{beyond.path!r} emits the heading {beyond.heading!r} at level "
            f"{beyond.level}, which is beyond H{MAX_LEVEL}",
            code=HEADING_DEPTH_OVERFLOW,
            remedy="raise the heading in the source, or select a section of it",
            reference=beyond.path,
            source=beyond.path,
            chain=selecting[0].chain if selecting else (),
        ) from beyond


def destination_map(
    groups: Sequence[Group], assigned: Sequence[str]
) -> dict[tuple[str, str | None], str]:
    """The destination each resolved target was given, by the identity naming it.

    Each emitted heading records the targets it is where they resolve:
    a file heading answers to its whole document and to the title it
    absorbed, a carried heading to the fragment its author's text
    produced, a merged heading to that fragment in every document that
    contributed it, and a variant heading or a member's overview
    subsection to the document it names. A destination is scoped to the
    bundle, so the map is one map over every group rather than one map
    for each.
    """
    found: dict[tuple[str, str | None], str] = {}
    at = 0
    for one in groups:
        for offset, targets in enumerate(one.targets):
            for target in targets:
                found.setdefault(target, assigned[at + offset])
        at += len(one.headings)
    return found


def entries_named(
    groups: Sequence[Group], assigned: Sequence[str]
) -> list[tuple[str, str]]:
    """Each entry reference the bundle opens on, as its text and its destination.

    The order is the bundle's own: the groups in root-relative path
    order, and inside one group the headings in source order. One
    selection therefore opens on one line however the entry references
    were written on the command line.
    """
    named = []
    at = 0
    for one in groups:
        for entry in one.entries:
            named.append((one.headings[entry], assigned[at + entry]))
        at += len(one.headings)
    return named


def compose(
    read: dict[str, Source],
    parsed: dict[str, list[Token]],
    defined: dict[str, dict[str, Definition]],
    referrer: Reference | None,
    entries: Collection[Reference],
    found: Sequence[Reference],
    limits: Limits,
    inforce: Mapping[str, int],
) -> tuple[str, list[tuple[str, str]]]:
    """The complete bundle candidate, and the entry destinations it opens on.

    The candidate is its entry line and one group per source. The pairs
    returned are the ones that entry line is written from, so what a
    caller reads on the diagnostic stream and what the bundle states in
    its opening line are one computation rather than two.

    A destination belongs to the bundle rather than to a group, so it
    is known only once every group exists. The groups are therefore
    built twice: once to learn the headings the bundle emits, and once
    more with the map those headings produce, which is what each
    compiled link is rewritten through. The second pass emits the same headings
    as the first, because a rewrite edits a link's destination and its
    mark and nothing a heading is slugged from.

    Candidate validation closes the pass. Every invariant it holds is
    a property of the construction, which an author cannot reach, so a
    disagreement is a fault in the tool. The boundary between two
    emitted regions is the exception: it follows from the documents the
    run was asked to bundle together, and an author closing a code
    example or selecting other content resolves it, so it is reported
    as the input failure it is.
    """
    selected = contributing(referrer, found)
    unambiguous(selected, inforce)
    headed = assembled(read, parsed, defined, selected, entries, None, inforce)
    assigned = fragments([heading for one in headed for heading in one.headings])
    targets = destination_map(headed, assigned)
    groups = assembled(read, parsed, defined, selected, entries, targets, inforce)
    named = entries_named(groups, assigned)
    bundled = assemble(entry_line(named), groups)
    try:
        validate(
            bundled,
            groups,
            assigned,
            targets,
            referrer,
            entries,
            read,
            parsed,
            limits.of(NESTING),
        )
    except Unsafe as boundary:
        reached = reaching(selected).get(boundary.path or "", ())
        raise unsafe(boundary, reached) from boundary
    return bundled, named


def resource(destination: str) -> bool:
    """Whether one destination names a resource rather than a document or a section.

    A resource is what the bundle carries as text: a reference naming
    no Markdown document under the allowed root. A fragment names a
    place in the bundle itself, and a reference carrying a scheme, an
    authority or a drive letter names something no directory the bundle
    is read from decides, so neither is one.
    """
    written = components(destination).path
    if not written or external(written) or DRIVE.match(written) is not None:
        return False
    return not is_markdown(written)


def resourced(bundled: str, budget: int) -> bool:
    """Whether the published bundle's text names at least one resource.

    The bundle is read as a renderer reads it, so a resource a source
    wrote as a reference-style use is counted at the inline form the
    bundle publishes it as. A bundle whose text names none carries
    nothing to warn about.
    """
    return any(
        resource(str(child.attrGet(HREF) or child.attrGet(SRC) or ""))
        for token in parse(bundled, budget)
        if token.type == INLINE
        for child in token.children or []
        if child.type in REFERENCE_USES
    )


def publish(text: str, stream: IO[str]) -> None:
    """Write one response to standard output, or report that it was refused."""
    try:
        stream.write(text)
        stream.flush()
    except OSError as refused:
        if stream is sys.stdout:
            sys.stdout = open(os.devnull, "w")
        raise Failure(
            PUBLICATION_FAILURE,
            Diagnostic(
                ERROR,
                f"standard output refused the response: {refused}",
                code=PUBLICATION_FAILED,
            ),
        ) from refused


def publish_file(text: str, destination: Path) -> None:
    """Write one validated bundle to a named file, atomically.

    The bytes go to a temporary file beside the destination and that file
    is renamed onto it, which is one filesystem operation, so a reader of
    the destination sees the bytes that were there before or the whole
    bundle and never a partial one. A write the destination refuses
    leaves the temporary file behind no longer than the attempt.
    """
    written = None
    try:
        handle = tempfile.NamedTemporaryFile(
            "w",
            encoding=ENCODING,
            newline="",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            delete=False,
        )
        written = Path(handle.name)
        with handle:
            handle.write(text)
        os.replace(written, destination)
    except OSError as refused:
        if written is not None:
            written.unlink(missing_ok=True)
        raise Failure(
            PUBLICATION_FAILURE,
            Diagnostic(
                ERROR,
                f"the output path {str(destination)!r} refused the bundle: {refused}",
                code=PUBLICATION_FAILED,
                remedy="name a path the run can write",
            ),
        ) from refused


def execute(arguments: Sequence[str], stdout: IO[str], reporter: Reporter) -> int:
    """One invocation, from its command line to the status its outcome returns."""
    grammar = parser()
    options = grammar.parse_args(list(arguments))

    if options.help:
        publish(grammar.format_help(), stdout)
        return SUCCESS
    if options.version:
        publish(f"{NAME} {version(NAME)} ({PROFILE})\n", stdout)
        return SUCCESS

    if options.root is None:
        raise usage_failure("--root is required and names the allowed source root")
    if not options.references:
        raise usage_failure("at least one entry reference is required")
    requested = [entry(reference) for reference in options.references]
    if not options.referrer:
        for one in requested:
            if not one.path:
                raise usage_failure(
                    f"the fragment-only reference {one.original!r} needs --from to "
                    f"name the document it resolves against"
                )
    inforce = rules(options.group)

    root = Path(options.root).resolve()
    referring = entry(options.referrer) if options.referrer else None
    if referring is not None:
        referring = replace(referring, chain=(identity(referring),))
    requested = entered(referring, requested)

    if not root.is_dir():
        raise input_failure(
            f"the allowed source root {options.root!r} names no directory",
            code=ROOT_NOT_FOUND,
            remedy="name a directory that exists",
        )
    present = directories(root)
    for slug in inforce:
        if slug not in present:
            raise input_failure(
                f"the grouping rule for {slug!r} names no directory under the "
                f"allowed source root",
                code=INVALID_GROUP_RULE,
                remedy="name a directory the source root carries",
            )

    limits = budgets(options)
    try:
        read, parsed, defined, captured, found = traverse(
            root, referring, requested, limits
        )
    except Crossed as crossed:
        raise crossing(crossed) from crossed
    if options.output != STANDARD_OUTPUT:
        destination = Path(options.output).resolve()
        if destination in sources(root, read):
            raise usage_failure(
                f"the output path {options.output!r} names an input source"
            )
    bundled, named = compose(
        read, parsed, defined, referring, requested, found, limits, inforce
    )
    recheck(root, captured, reaching(contributing(referring, found)))
    try:
        limits.hold(OUTPUT_BYTES, len(bundled.encode(ENCODING)))
    except Crossed as crossed:
        raise crossing(crossed) from crossed
    if resourced(bundled, limits.of(NESTING)):
        reporter.emit(
            Diagnostic(
                WARNING,
                "the bundle names at least one resource, which it carries as the "
                "text its source wrote, so a reader opening the bundle from "
                "another directory may not find it",
                code=RESOURCE_PORTABILITY,
            )
        )
    if not options.check:
        if options.output == STANDARD_OUTPUT:
            publish(bundled, stdout)
        else:
            publish_file(bundled, Path(options.output).resolve())
    for reference, target in named:
        reporter.emit(
            Diagnostic(
                WARNING,
                f"the entry reference {reference!r} resolves to the destination "
                f"{target!r}, which the bundle's entry line links it to",
                code=ENTRY_DESTINATION,
                reference=reference,
                resolved=target,
            )
        )
    return SUCCESS


def main(
    argv: Sequence[str] | None = None,
    stdout: IO[str] | None = None,
    stderr: IO[str] | None = None,
) -> int:
    """The command, returning the status its outcome declares."""
    out = sys.stdout if stdout is None else stdout
    err = sys.stderr if stderr is None else stderr
    arguments = list(sys.argv[1:] if argv is None else argv)
    reporter = Reporter(err, diagnostic_format(arguments))
    try:
        return execute(arguments, out, reporter)
    except Failure as outcome:
        reporter.emit(outcome.diagnostic)
        return outcome.status
    except Exception as unexpected:  # noqa: BLE001 - the declared status 4
        reporter.emit(
            Diagnostic(
                ERROR,
                f"unexpected internal error: {unexpected!r}",
                code=UNEXPECTED_INTERNAL_ERROR,
            )
        )
        return INTERNAL_ERROR
