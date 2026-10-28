"""Compile captured Markdown sources with file-owned dependency roots.

Positional files resolve from the invocation working directory. Each source
uses its explicit file-relative root, or the invocation directory when absent.
Bounded no-follow capture retains bytes, metadata and filesystem identities;
publication rechecks every captured source and bound directory. Discovery,
rewriting and candidate validation use the same per-source resolution context."""

import argparse
import os
import re
import shutil
import sys
import uuid
from collections.abc import Callable, Collection, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, replace
from importlib.metadata import version
from pathlib import Path
from typing import IO, Any, NoReturn

from markdown_it.token import Token

from prosiform import PROFILE
from prosiform.access import (
    Absent,
    Symlinked,
    Unreadable,
    directory,
    read_source,
)
from prosiform.access import (
    opened as open_source,
)
from prosiform.bundle import (
    CODES as BUNDLE_CODES,
)
from prosiform.bundle import (
    HEADING_DEPTH_OVERFLOW,
    MAX_LEVEL,
    Group,
    Overflow,
    assemble,
    document_title,
    file_heading,
    group,
)
from prosiform.candidate import (
    CODES as CANDIDATE_CODES,
)
from prosiform.candidate import (
    UNSAFE_BUNDLE_BOUNDARY,
    Unsafe,
    validate,
)
from prosiform.closure import (
    DEFERRAL_MARK,
    DISPATCH_MARK,
    DRIVE,
    RUN_SET_MARK,
    Malformed,
    OutsideRoot,
    Reference,
    components,
    conflicting,
    dispatched,
    identity,
    inside,
    operators,
    resolvable,
    resolve,
    run_set,
    withholding,
    withholding_target,
)
from prosiform.diagnostics import (
    ERROR,
    FORMATS,
    TEXT,
    WARNING,
    Diagnostic,
    Location,
    RelatedLocation,
    Reporter,
)
from prosiform.dispatch import CODES as DISPATCH_CODES
from prosiform.dispatch import (
    Anchors,
    Hop,
    Refused,
    analysed,
    anchors,
    collisions,
    cycle,
    selfward,
    subsections,
)
from prosiform.grouping import member_headings, merged, prepared
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
from prosiform.limits import (
    CODES as LIMITS_CODES,
)
from prosiform.metadata import InvalidMetadata
from prosiform.profile import (
    CODES as PROFILE_CODES,
)
from prosiform.profile import (
    PARSER_REFERENCE_LIMIT,
    REFERENCES,
    SUFFIXES,
    UNSUPPORTED_CONSTRUCT,
    Refusal,
    Suppressed,
    is_markdown,
    parse,
    refusals,
)
from prosiform.provenance import Target
from prosiform.rewrite import Definition, definitions
from prosiform.run_set import CODES as RUN_SET_CODES
from prosiform.run_set import RunSet, misshapen, stray
from prosiform.source import (
    AMBIGUOUS_SOURCE_HEADING,
    CLOSERS,
    ENCODING,
    NESTED_SECTION_TARGET,
    UNTERMINATED_FRONTMATTER,
    Ambiguous,
    Capture,
    Nested,
    Selection,
    Source,
    Unterminated,
    content,
    decode,
    external,
    fragments,
    hashed,
    index,
    lines,
    nesting,
    occurrences,
    regions,
    section,
    uses,
    within,
)
from prosiform.source import (
    CODES as SOURCE_CODES,
)

NAME = "pf"

SUCCESS = 0
INPUT_FAILURE = 1
USAGE_FAILURE = 2
PUBLICATION_FAILURE = 3
INTERNAL_ERROR = 4

STANDARD_OUTPUT = "-"
BUNDLE_SUFFIX = ".bundle.md"
CURRENT_FOLDER = "."

INVALID_ENCODING = "E_INVALID_ENCODING"
GROUP_DEPTH_CONFLICT = "E_GROUP_DEPTH_CONFLICT"
INVALID_USAGE = "E_INVALID_USAGE"
PUBLICATION_FAILED = "E_PUBLICATION_FAILED"
ROOT_NOT_FOUND = "E_ROOT_NOT_FOUND"
SOURCE_CHANGED = "E_SOURCE_CHANGED"
SOURCE_ACCESS = "E_SOURCE_ACCESS"
SOURCE_OUTSIDE_ROOT = "E_SOURCE_OUTSIDE_ROOT"
SOURCE_SYMLINK = "E_SOURCE_SYMLINK"
TARGET_NOT_FOUND = "E_TARGET_NOT_FOUND"
UNEXPECTED_INTERNAL_ERROR = "E_UNEXPECTED_INTERNAL_ERROR"
UNSUPPORTED_ENTRY_SUFFIX = "E_UNSUPPORTED_ENTRY_SUFFIX"

RESOURCE_PORTABILITY = "W_RESOURCE_PORTABILITY"
COINCIDENT_HEADING = "W_COINCIDENT_HEADING"

OPERATOR_NAMES = {
    DEFERRAL_MARK: "the deferral mark",
    DISPATCH_MARK: "the dispatch mark",
    RUN_SET_MARK: "the run-set mark",
}

CODES = tuple(
    sorted(
        {
            INVALID_ENCODING,
            GROUP_DEPTH_CONFLICT,
            INVALID_USAGE,
            PUBLICATION_FAILED,
            ROOT_NOT_FOUND,
            SOURCE_CHANGED,
            SOURCE_ACCESS,
            SOURCE_OUTSIDE_ROOT,
            SOURCE_SYMLINK,
            TARGET_NOT_FOUND,
            UNEXPECTED_INTERNAL_ERROR,
            UNSUPPORTED_ENTRY_SUFFIX,
            RESOURCE_PORTABILITY,
            COINCIDENT_HEADING,
            *BUNDLE_CODES,
            *CANDIDATE_CODES,
            *DISPATCH_CODES,
            *LIMITS_CODES,
            *PROFILE_CODES,
            *RUN_SET_CODES,
            *SOURCE_CODES,
        }
    )
)

SOURCE_CHANGED_FAULT = "source-changed"
INTERNAL_FAULT = "internal"
FAULTS = (SOURCE_CHANGED_FAULT, INTERNAL_FAULT)

DECIMAL = re.compile(r"^[0-9]+$")

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

    Every such fault leads a caller to one remedy, so they share one code.
    """
    return Failure(
        USAGE_FAILURE,
        Diagnostic(
            ERROR,
            message,
            code=code,
            reference=reference,
            remedy=f"run {NAME} -h for usage",
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


def declined(
    suppressed: Suppressed, path: str, source: Source, chain: Sequence[str]
) -> Failure:
    """One reference lookup the parser declined, as the failure to index its source.

    The diagnostic names the reference the declined lookup would have
    made, together with the first span the parser was reading when it
    declined, which is where an author finds the nesting to write the
    reference out of. A span whose construct spells no destination
    leaves the reference unnamed, and the diagnostic names the source
    it could not index; a span the parser records no line for is
    reported against the source alone.
    """
    return input_failure(
        f"the source {path!r} cannot be safely indexed: {suppressed}",
        code=PARSER_REFERENCE_LIMIT,
        remedy=suppressed.remedy,
        reference=suppressed.reference or path,
        source=location(path, source.line(suppressed.line)),
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
        allow_abbrev=False,
        usage=f"{NAME} [OPTIONS] REF [REF ...]",
        description=(
            "Bundle the local Markdown closure of one or more entry references, "
            "and of each target they dispatch, into validated bundles."
        ),
        epilog=EXIT_STATUSES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    grammar.add_argument(
        "-f",
        dest="referrer",
        metavar="DOC",
        help="working-directory-relative document for fragment-only references",
    )
    grammar.add_argument(
        "-o",
        dest="output",
        metavar="DIR",
        default=CURRENT_FOLDER,
        help="existing folder the run's own folder of bundles is written into, "
        "swapped in whole; default: the working directory",
    )
    grammar.add_argument(
        "-c",
        dest="check",
        action="store_true",
        help="discover, bundle, validate; publish nothing; accepts -o",
    )
    grammar.add_argument(
        "-d",
        dest="diagnostics",
        choices=FORMATS,
        default=TEXT,
        help=f"stderr diagnostics; default {TEXT}",
    )
    grammar.add_argument(
        "-x",
        dest="fault",
        choices=FAULTS,
        help="inject a conformance run fault no source tree expresses; default none",
    )
    for budget in BUDGETS:
        grammar.add_argument(
            budget.option,
            dest=budget.dest,
            metavar="N",
            type=override,
            default=budget.default,
            help=f"{budget.counted}; positive decimal integer, "
            f"default {budget.default}",
        )
    grammar.add_argument(
        "-C",
        "--codes",
        dest="codes",
        action="store_true",
        help="list this build's error and warning codes",
    )
    grammar.add_argument(
        "-v",
        "--version",
        dest="version",
        action="store_true",
        help="tool version and profile identifier",
    )
    grammar.add_argument(
        "-h",
        "--help",
        dest="help",
        action="store_true",
        help="usage, defaults and exit statuses",
    )
    grammar.add_argument(
        "references",
        metavar="REF",
        nargs="*",
        help="document, document#fragment, or #fragment with -f; paths from cwd",
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
    tokens = iter(arguments)
    for token in tokens:
        if token == "--":
            break
        if not token.startswith("-") or token.startswith("--"):
            continue
        for at, option in enumerate(token[1:], start=1):
            if option in "cCvh":
                continue
            if option in "rfogdxFBIOTLNE":
                value = token[at + 1 :].removeprefix("=") or next(tokens, "")
                if option == "d" and value in FORMATS:
                    selected = value
            break
    return selected


def entry(text: str) -> Reference:
    """Normalize a positional reference with bounded relative-parent bootstrap."""
    try:
        found = resolve(text, allow_parent=True)
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
    """Canonical paths of every captured source, including deferred targets."""
    return {Path(os.path.normpath(root / path)) for path in read}


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


def read_document(
    root: Path, found: Reference, limits: Limits, total: int = 0
) -> Opened:
    """Capture bounded bytes, typed settings and no-follow source/root identities.

    Metadata resolves only after the source has been captured within the byte
    and nesting limits. An explicit root is walked from its declaring directory;
    absence binds the invocation working directory. Diagnostics retain physical
    coordinates and the referring chain."""
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
        observed: list[tuple[str, int, int]] = []
        data = read_source(
            root,
            found.walk or name,
            limit=min(limits.of(FILE_BYTES), limits.of(INPUT_BYTES) - total),
            observed=observed,
        )
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
    except OSError as error:
        raise input_failure(
            str(error),
            code=SOURCE_ACCESS,
            remedy="check source permissions",
            reference=reference,
            source=found.origin,
            chain=chain,
        ) from error
    try:
        limits.hold(FILE_BYTES, len(data))
        limits.hold(INPUT_BYTES, total + len(data))
    except Crossed as crossed:
        raise unindexable(crossed, name, chain) from crossed
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
    captured = Capture(
        observed[-1][0],
        hashed(data),
        chain,
        found.walk or name,
        tuple(observed[:-1]),
        (observed[-1][1], observed[-1][2]),
        len(data),
    )
    try:
        source = content(
            text,
            file=name,
            max_bytes=limits.of(FILE_BYTES),
            max_depth=limits.of(NESTING),
        )
        declared = source.conversion.root
        root_walk = str(Path(name).parent / declared) if declared is not None else "."
        try:
            rooted = directory(root, root_walk)
        except (Unreadable, OSError) as error:
            code = (
                SOURCE_SYMLINK
                if isinstance(error, Symlinked)
                else ROOT_NOT_FOUND
                if isinstance(error, Absent)
                else SOURCE_ACCESS
            )
            raise Failure(
                INPUT_FAILURE,
                Diagnostic(
                    ERROR,
                    str(error),
                    code,
                    location=source.conversion.root_location,
                    reference=reference,
                    chain=chain,
                ),
            ) from error
        effective = os.path.relpath(rooted[-1][0], root)
        source = replace(source, root="" if effective == "." else effective)
        captured = replace(captured, directories=(*captured.directories, *rooted))
        return Opened(source, len(data), captured)
    except InvalidMetadata as invalid:
        raise Failure(
            INPUT_FAILURE, replace(invalid.diagnostic, reference=reference, chain=chain)
        ) from invalid
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


def recheck(root: Path, captured: dict[str, Capture]) -> None:
    """Verify captured bytes and filesystem identities before publication."""
    for path in sorted(captured):
        was = captured[path]
        try:
            for name, device, inode in was.directories:
                checked = directory(root, os.path.relpath(name, root))[-1]
                if checked[1:] != (device, inode):
                    raise changed(path, "bound directory identity changed", was.chain)
            observed: list[tuple[str, int, int]] = []
            data = read_source(
                root, was.walk or path, limit=was.size, observed=observed
            )
        except (Unreadable, OSError) as error:
            raise changed(path, str(error), was.chain) from error
        if observed[-1][1:] != was.file_identity:
            raise changed(path, "source identity changed", was.chain)
        if hashed(data) != was.digest:
            raise changed(path, "source bytes changed", was.chain)


class Faulted(Exception):
    """A fault the run was asked to perform on itself, and performed."""


def rewrite_sources(root: Path, captured: dict[str, Capture]) -> None:
    """Write other bytes to each source the run read.

    A source that changes during compilation is a fact about the run
    rather than about any document it reads, so a source tree and an
    invocation state nothing about it and a run asked for the fault is
    what reaches it. The write happens where a concurrent writer's
    would: after discovery captured the bytes and before the recheck
    reads them again.
    """
    for path in sorted(captured):
        with (root / path).open("ab") as handle:
            handle.write(b"\n")


def contributing(
    referrer: Reference | None, requested: Sequence[Reference]
) -> dict[str, list[Reference]]:
    """Each file group the bundle carries, by the path that names it.

    A reference naming a document selects from that document, and a
    fragment alone selects from the document `-f` names. The path
    is the identity the reference normalized to, so two references
    spelling one document name one group, which carries what each of
    them selected. The documents are in path order, which is the order
    each round of the traversal reads them in; `placement` decides the
    order the bundle carries them in.
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

    A whole document an entry reference selected is the selection
    `None`, which is what lets the parent, the first entry document,
    open the bundle on its own title. A whole document only a
    dependency selected is every region it holds.

    A fragment the document does not yield is a reference that reached
    a document and no section of it, so its diagnostic names that
    document as the identity it resolved to and the chain that reached
    the reference.
    """
    wanted: set[int] = set()
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
        wanted.update(id(token) for token in found)
    if whole:
        return None if entered else Selection(tuple(regions(tokens)))
    return Selection(tuple(token for token in regions(tokens) if id(token) in wanted))


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

    A withheld reference is not compiled: the run yields no dependency
    for it, so nothing it names is bundled through that reference, and
    the link reaches the bundle with its mark for the run that compiles
    it. Its target is what `withheld` yields, because a reference under
    the root is one the run stays responsible for whether or not it
    carries what the reference names.

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
            found = inside(path, use.destination, source.root)
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
        if withholding(use.opening):
            continue
        yield replace(found, origin=at, chain=(*chain, identity(found)))


def refusals_of_operators(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
) -> None:
    """Refuse a link whose operator states nothing the run can carry out.

    Each operator states how one compilation is carried out — by a later
    run, by a sub-agent, or by this run as a run-set — so a link stating
    two states two contradictory things. An operator names the
    compilation of a Markdown document or section under the source root,
    so one opening a link or an image naming anything else — a remote
    address, a resource, a document outside the root — states a
    compilation no run performs. Each is a source fault rather than a
    metadata fault: what the author wrote states no compilation the run
    can carry out, and the run reports the link rather than reading it
    one way.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        at = location(path, source.line(use.line))
        if conflicting(use.opening):
            stated = list(dict.fromkeys(operators(use.opening)))
            raise input_failure(
                f"the link {use.opening!r} opens with "
                + " and ".join(f"{OPERATOR_NAMES[mark]} {mark!r}" for mark in stated)
                + ", which state different things for one compilation",
                code=UNSUPPORTED_CONSTRUCT,
                remedy="open the link's text with the one operator that states how "
                "the material is compiled",
                reference=use.opening,
                source=at,
                chain=(*chain, use.destination),
            )
        if not operators(use.opening):
            continue
        target = resolvable(path, use.destination, source.root)
        if not use.resource and target is not None:
            continue
        kind = "image" if use.resource else "link"
        raise input_failure(
            f"the {kind} {use.opening!r} opens with an operator and names "
            f"{use.destination!r}, which is no Markdown document or section under "
            f"the source root, so the operator states no compilation the run "
            f"can carry out",
            code=UNSUPPORTED_CONSTRUCT,
            remedy="name a Markdown document or section the source root carries, "
            "or remove the operator",
            reference=use.destination,
            source=at,
            chain=(*chain, use.destination),
        )


def withheld(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
) -> Iterator[Reference]:
    """Every target the selected content of one source withholds.

    A withheld reference under the allowed source root naming a
    Markdown document is one this run does not carry and stays
    responsible for, so its target is yielded here to be confirmed. An
    operator on a reference leaving the root, or on one naming no
    Markdown document, withholds nothing, and the run refuses it before
    reading the withheld targets.

    What is yielded is a target and not a dependency. It joins no
    frontier, so the document is not bundled through this reference,
    contributes no content and no destination of its own, and heads no
    file group.

    The chain is the one a compiled reference in the same place would
    carry, because a refusal reports the route the run followed to the
    link whichever half of the rule the link falls under.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        if use.resource:
            continue
        found = withholding_target(path, use.destination, use.opening, source.root)
        if found is None:
            continue
        at = location(path, source.line(use.line))
        yield replace(found, origin=at, chain=(*chain, identity(found)))


def dispatches(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
) -> Iterator[Hop]:
    """Every dispatched link the selected content of one source carries.

    A dispatch is a withheld link whose target the run compiles as a
    bundle of its own, so what is yielded is the target `withheld`
    yields for it, with the place the link is written: the hop a chain
    of dispatches takes from here.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        if use.resource or not dispatched(use.opening):
            continue
        found = withholding_target(path, use.destination, use.opening, source.root)
        if found is None:
            continue
        line = source.line(use.line)
        yield Hop(
            replace(
                found,
                origin=location(path, line),
                chain=(*chain, identity(found)),
            ),
            Location(path, 1 if line is None else line, 1),
        )


def run_sets(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
) -> Iterator[RunSet]:
    """Every run-set link the selected content of one source carries.

    A run-set's target is compiled like any link's, so what is yielded is
    the target the link resolves to, with the text the link opens with
    and the place it is written, for the check of the target's shape.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        if use.resource or not run_set(use.opening):
            continue
        found = resolvable(path, use.destination, source.root)
        if found is None:
            continue
        line = source.line(use.line)
        yield RunSet(
            replace(
                found,
                origin=location(path, line),
                chain=(*chain, identity(found)),
            ),
            use.opening,
            Location(path, 1 if line is None else line, 1),
        )


def verify_cached(root: Path, one: Reference, captured: Mapping[str, Capture]) -> None:
    """Every referring route must retain no-follow access to a cached identity."""
    if one.path not in captured:
        return
    observed: list[tuple[str, int, int]] = []
    try:
        os.close(open_source(root, one.walk or one.path, observed))
    except (Unreadable, OSError) as error:
        code = SOURCE_SYMLINK if isinstance(error, Symlinked) else SOURCE_ACCESS
        raise input_failure(
            str(error),
            code=code,
            remedy="check the referring path",
            reference=one.original,
            chain=one.chain,
        ) from error
    if observed[-1][1:] != captured[one.path].file_identity:
        raise changed(one.path, "source identity changed", one.chain)


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
    list[Hop],
    list[RunSet],
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

    The dispatched links the selected content carries are returned as
    well, each target once at the first link the rounds read naming it,
    for the bundles the run compiles from them, and so are the
    run-set links, each target once in the same way, for the check of
    its shape.
    """
    read: dict[str, Source] = {}
    parsed: dict[str, list[Token]] = {}
    defined: dict[str, dict[str, Definition]] = {}
    captured: dict[str, Capture] = {}
    found = list(requested)
    seen = {(one.path, one.fragment) for one in found}
    limits.hold(TARGETS, len(seen))
    counted: dict[str, int] = {}
    deferred: dict[tuple[str, str | None], Reference] = {}
    dispatching: dict[str, Hop] = {}
    running: dict[str, RunSet] = {}
    total = 0
    hop = 0
    frontier = ([referrer] if referrer is not None else []) + list(requested)
    while frontier:
        hop += 1
        for one in frontier:
            verify_cached(root, one, captured)
            if not one.path or one.path in read:
                continue
            limits.hold(FILES, len(read) + 1)
            opened = read_document(root, one, limits, total)
            source = opened.source
            environment: dict[str, Any] = {}
            try:
                tokens = parse(source.text, limits.of(NESTING), environment)
                limits.hold(NESTING, nesting(tokens))
            except Crossed as crossed:
                raise unindexable(crossed, one.path, one.chain) from crossed
            except Suppressed as suppressed:
                raise declined(suppressed, one.path, source, one.chain) from suppressed
            total += opened.size
            read[one.path] = source
            captured[one.path] = opened.capture
            parsed[one.path] = tokens
            defined[one.path] = definitions(
                environment.get(REFERENCES, {}), lines(source.text)
            )
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
            refusals_of_operators(path, read[path], parsed[path], chosen, reached)
            for one in withheld(path, read[path], parsed[path], chosen, reached):
                verify_cached(root, one, captured)
                deferred.setdefault((one.path, one.fragment), one)
            for link in dispatches(path, read[path], parsed[path], chosen, reached):
                dispatching.setdefault(link.name, link)
            for named in run_sets(path, read[path], parsed[path], chosen, reached):
                running.setdefault(named.name, named)
            for one in required(path, read[path], parsed[path], chosen, reached):
                verify_cached(root, one, captured)
                if (one.path, one.fragment) in seen:
                    continue
                limits.hold(EXPANSION_DEPTH, hop)
                seen.add((one.path, one.fragment))
                limits.hold(TARGETS, len(seen))
                discovered.append(one)
        found.extend(discovered)
        frontier = discovered
    for one in deferred.values():
        if one.path not in read:
            limits.hold(FILES, len(read) + 1)
            opened = read_document(root, one, limits, total)
            try:
                tokens = parse(opened.source.text, limits.of(NESTING), {})
                limits.hold(NESTING, nesting(tokens))
            except Crossed as crossed:
                raise unindexable(crossed, one.path, one.chain) from crossed
            except Suppressed as suppressed:
                raise declined(
                    suppressed, one.path, opened.source, one.chain
                ) from suppressed
            total += opened.size
            read[one.path] = opened.source
            captured[one.path] = opened.capture
            parsed[one.path] = tokens
        confirm(parsed[one.path], one)
    return (
        read,
        parsed,
        defined,
        captured,
        found,
        list(dispatching.values()),
        list(running.values()),
    )


def confirm(
    tokens: Sequence[Token],
    one: Reference,
) -> None:
    """Hold one deferred reference to naming a document and a heading that exist.

    A deferral says that the material is reached in a run of its own,
    not that nobody is answerable for it, so the document is read and
    the fragment is looked up. A reference the root does not carry is
    refused by the read, and one naming no heading of the document it
    resolves to is refused here, each with the code and the route a
    compiled reference naming nothing reports.

    The question is whether the document carries the heading, asked of
    the index of every heading the profile recognizes. Which section a
    fragment roots, and whether two headings make it ambiguous, is what
    the run compiling the link decides; this run says only that the
    target is there to be found.

    The caller supplies the cached index from the source's captured read.
    A deferred-only source contributes no content to a group.
    """
    if one.fragment is None:
        return
    if any(heading.fragment == one.fragment for heading in index(tokens)):
        return
    raise input_failure(
        f"the reference {one.original!r} names no heading of the document it defers",
        code=TARGET_NOT_FOUND,
        remedy="name a heading the document carries",
        reference=one.original,
        resolved=one.path,
        source=one.origin,
        chain=one.chain,
    )


def group_depths(
    read: Mapping[str, Source], selected: Mapping[str, Sequence[Reference]]
) -> dict[str, int]:
    """Consistent depths for named groups, ordered by source path."""
    members: dict[str, list[str]] = {}
    for path in sorted(selected):
        name = read[path].conversion.group
        if name is not None:
            members.setdefault(name, []).append(path)
    depths: dict[str, int] = {}
    for name in sorted(members):
        first = read[members[name][0]].conversion
        assert first.depth is not None and first.depth_location is not None
        depths[name] = first.depth
        for path in members[name][1:]:
            current = read[path].conversion
            if current.depth != first.depth:
                location = current.depth_location
                assert location is not None
                raise Failure(
                    INPUT_FAILURE,
                    Diagnostic(
                        ERROR,
                        f"prosiform.group-depth for group {name!r} "
                        f"is {first.depth}; "
                        f"another member declares {current.depth}",
                        code=GROUP_DEPTH_CONFLICT,
                        location=first.depth_location,
                        related=(
                            RelatedLocation(
                                location.file,
                                location.line,
                                location.column,
                                "prosiform.group-depth for group "
                                f"{name!r} is {current.depth}",
                            ),
                        ),
                        remedy="use one depth for every contributing group member",
                    ),
                )
    return depths


@dataclass(frozen=True)
class Named:
    """One generated heading, and where the source it names is located."""

    text: str
    location: Location


def file_named(
    path: str, source: Source, tokens: Sequence[Token], wrapped: bool
) -> Named | None:
    """One document's file heading, located at the title it carries or at the document.

    A titled document is headed by its title, so the heading is located
    on the line that title stands on. The parent opens the bundle on
    that title rather than on a heading the bundle writes, and is headed
    by it all the same. An untitled document is headed by its path,
    which names the document as a whole, so the heading is located at
    the document's first position; a parent the bundle opens without a
    file heading and without a single title is headed by nothing.
    """
    title = document_title(tokens)
    if title is None and not wrapped:
        return None
    at = None if title is None or title.map is None else title.map[0] + 1
    line = source.line(at)
    return Named(
        file_heading(path, tokens, source.root),
        Location(path, 1 if line is None else line, 1),
    )


def coincidence(
    kind: str, named: Sequence[Named], remedy: str, within: str = ""
) -> Diagnostic:
    """One warning naming a set of generated headings that read alike.

    The first heading is the primary location and every other is a
    related one, each carrying the text it reads, so a caller finds each
    source the coinciding headings stand for. A set held within one
    merged group names that group.
    """
    first, *others = named
    return Diagnostic(
        WARNING,
        f"{len(named)} {kind}s{within} read {first.text!r}, which a reader tells apart "
        f"only by where each stands",
        code=COINCIDENT_HEADING,
        remedy=remedy,
        location=first.location,
        related=tuple(
            RelatedLocation(
                one.location.file,
                one.location.line,
                one.location.column,
                f"{kind} {one.text!r}",
            )
            for one in others
        ),
    )


def coincident(
    groups: Sequence[Group],
    selected: Mapping[str, Sequence[Reference]],
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
) -> list[Diagnostic]:
    """One warning for each set of generated headings that coincide.

    The headings that name a source are its file headings, the parent's
    own title among them where the bundle opens on it, and, within one
    merged group, its member headings. Two of either
    coincide where their texts are one text but for capitalization,
    because a reader reads them as one name and the renderer slugs them
    alike, so the bundle tells them apart by an ordinal alone. A member
    is named by the shortest run of its path that distinguishes it from
    the group's other members, so members whose paths differ only by
    Markdown extension or capitalization take one name. The bundle is
    published either way; the warning is what sends a reader to check
    it. A heading an author wrote is the author's to repeat and warns of
    nothing.

    The warnings follow the bundle order of the first heading each set
    holds, and each set's headings follow it too.
    """
    files: dict[str, tuple[int, list[Named]]] = {}
    found: list[tuple[int, Diagnostic]] = []
    for at, one in enumerate(groups):
        named = one.record.path
        if one.record.merged is None:
            heading = file_named(named, read[named], parsed[named], one.wrapped)
            if heading is not None:
                files.setdefault(heading.text.casefold(), (at, []))[1].append(heading)
            continue
        paths = [path for path in selected if read[path].conversion.group == named]
        names = member_headings(paths, named)
        members: dict[str, list[Named]] = {}
        for path in paths:
            declared = read[path].conversion.group_location
            assert declared is not None
            members.setdefault(names[path].casefold(), []).append(
                Named(names[path], declared)
            )
        found.extend(
            (
                at,
                coincidence(
                    "member heading",
                    same,
                    "rename a member so its path distinguishes it in the group",
                    f" of group {named!r}",
                ),
            )
            for same in members.values()
            if len(same) > 1
        )
    found.extend(
        (
            at,
            coincidence(
                "file heading",
                same,
                "retitle or rename a document so its file heading reads apart",
            ),
        )
        for at, same in files.values()
        if len(same) > 1
    )
    return [diagnostic for _at, diagnostic in sorted(found, key=lambda one: one[0])]


def parent_document(entries: Collection[Reference]) -> str | None:
    """The first entry document, which opens the bundle on its own title."""
    if not isinstance(entries, Sequence) or not entries:
        return None
    return entries[0].path or None


def placement(
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    selected: Mapping[str, list[Reference]],
    referrer: Reference | None,
    entries: Collection[Reference],
) -> dict[str, list[Reference]]:
    """Each document the bundle carries, in the order a reference first names it.

    The entry references are read first, in the order the invocation
    gives them, and then the selected content of each placed document,
    in the order the documents were placed, each in source order. A
    document is placed at the first reference that names it, so the
    parent leads and an author orders what follows by the order the
    links are written in. Every document the bundle carries is reached
    from an entry reference by a chain of the links read here, so the
    order covers them all.
    """
    base = referrer.path if referrer is not None else ""
    placed = [one.path or base for one in entries]
    order = list(dict.fromkeys(path for path in placed if path in selected))
    at = 0
    while at < len(order):
        path = order[at]
        at += 1
        chosen = selection(path, parsed[path], selected[path], entries)
        for one in required(path, read[path], parsed[path], chosen, ()):
            if one.path in selected and one.path not in order:
                order.append(one.path)
    return {path: selected[path] for path in order}


def assembled(
    read: dict[str, Source],
    parsed: dict[str, list[Token]],
    defined: dict[str, dict[str, Definition]],
    selected: dict[str, list[Reference]],
    entries: Collection[Reference],
    assigned: dict[tuple[str, str | None], str] | None,
    inforce: Mapping[str, int],
    dispatching: Anchors | None = None,
) -> list[Group]:
    """Each group the bundle carries, its links rewritten where a map says so.

    The documents arrive in placement order, which `placement` decides.
    A document without conversion settings is its own file group. Every
    other document joins the merged group its slug names, which carries
    its members in placement order. A group stands where its first
    document is placed, so the group carrying the parent leads and one
    selection always bundles to the same bytes.
    """
    parent = parent_document(entries)
    groups: list[Group] = []
    merging: dict[str, list[str]] = {}
    for path in selected:
        selecting = selected[path]
        named = read[path].conversion.group
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
                    read[path].root,
                    path == parent,
                    dispatching,
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
                            read[path].root,
                            path == parent,
                            dispatching,
                        )
                        for path in paths
                    ],
                    parent,
                )
            )
    rank = {path: at for at, path in enumerate(selected)}
    return sorted(groups, key=lambda one: rank[one.order])


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
    contributed it, and a variant heading or the subsection
    naming a member to the document it names. A destination is scoped to the
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


def compose(
    read: dict[str, Source],
    parsed: dict[str, list[Token]],
    defined: dict[str, dict[str, Definition]],
    referrer: Reference | None,
    entries: Collection[Reference],
    found: Sequence[Reference],
    limits: Limits,
    bundle_file: Callable[[Target], str],
) -> tuple[str, list[Diagnostic]]:
    """The complete bundle candidate, and the warnings its headings raise.

    The candidate is one group per source, and it opens on the first
    group's first part. The warnings name the generated headings that
    coincide, which accompany the bundle rather than refuse it.

    A destination belongs to the bundle rather than to a group, so it
    is known only once every group exists. The groups are therefore
    built twice: once to learn the headings the bundle emits, and once
    more with the map those headings produce, which is what each
    compiled link is rewritten through. Each build carries the dispatch
    sub-sections its sections need, inserted once the group exists, so
    the headings the map is built from are every heading the bundle
    emits. The second pass emits the same headings as the first,
    because a rewrite edits a link's destination and its mark and
    nothing a heading is slugged from.

    Candidate validation closes the pass. Every invariant it holds is
    a property of the construction, which an author cannot reach, so a
    disagreement is a fault in the tool. The boundary between two
    emitted regions is the exception: it follows from the documents the
    run was asked to bundle together, and an author closing a code
    example or selecting other content resolves it, so it is reported
    as the input failure it is. A dispatch the bundle cannot place, and
    an authored heading equal to one pf emits, are refused as input
    failures too.
    """
    selected = contributing(referrer, found)
    inforce = group_depths(read, selected)
    selected = placement(read, parsed, selected, referrer, entries)
    try:
        headed, placed = subsections(
            assembled(read, parsed, defined, selected, entries, None, inforce),
            parsed,
            read,
            bundle_file,
        )
        collisions(headed)
    except Refused as refusal:
        raise Failure(INPUT_FAILURE, refusal.diagnostic) from refusal
    assigned = fragments([heading for one in headed for heading in one.headings])
    targets = destination_map(headed, assigned)
    dispatching = anchors(placed, assigned)
    groups, _ = subsections(
        assembled(
            read, parsed, defined, selected, entries, targets, inforce, dispatching
        ),
        parsed,
        read,
        bundle_file,
    )
    bundled = assemble(groups)
    try:
        validate(
            bundled,
            groups,
            assigned,
            targets,
            read,
            parsed,
            limits.of(NESTING),
            dispatching,
        )
    except Unsafe as boundary:
        reached = reaching(selected).get(boundary.path or "", ())
        raise unsafe(boundary, reached) from boundary
    return bundled, coincident(groups, selected, read, parsed)


def resource(destination: str, embedded: bool) -> bool:
    """Whether one reference use names a resource rather than a document or a section.

    A resource is what the bundle carries as text, which the use states
    along with where it points. An image embeds rather than links, so it
    names a resource whatever its destination spells, and a link names
    one when its destination names no Markdown document. A fragment
    names a place in the bundle itself, and a reference carrying a
    scheme, an authority or a drive letter names something no directory
    the bundle is read from decides, so neither is one under either use.
    """
    written = components(destination).path
    if not written or external(written) or DRIVE.match(written) is not None:
        return False
    return embedded or not is_markdown(written)


def resourced(bundled: str, budget: int) -> bool:
    """Whether the published bundle's text names at least one resource.

    The bundle is read as a renderer reads it, so a resource a source
    wrote as a reference-style use is counted at the inline form the
    bundle publishes it as. The uses are the ones discovery reads, so an
    image's alternative content is descended into where it sits and the
    warning classifies a reference as emission classifies it. A bundle
    whose text names none carries nothing to warn about.
    """
    tokens = parse(bundled, budget)
    return any(
        resource(use.destination, use.resource)
        for use in uses(tokens, tuple(regions(tokens)))
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


@dataclass(frozen=True)
class Bundle:
    """One composed bundle, the file name it is published under and its warnings."""

    text: str
    name: str
    warnings: Sequence[Diagnostic]


def publication(
    bundles: Sequence[Bundle],
    folder: Path,
    limits: Limits,
    reporter: Reporter,
    check: bool,
) -> None:
    """Validate every bundle a run publishes, then publish the set whole or not at all.

    Each bundle is held to the output budget before any is written, so a
    bundle the budget refuses ends the run with its diagnostic and
    nothing written. Every bundle's warnings follow, in turn, and then
    the set is published into the run's folder, unless the run only
    validates, which writes nothing.
    """
    for one in bundles:
        try:
            limits.hold(OUTPUT_BYTES, len(one.text.encode(ENCODING)))
        except Crossed as crossed:
            raise crossing(crossed) from crossed
    for one in bundles:
        for warning in one.warnings:
            reporter.emit(warning)
    if not check:
        publish_folder(bundles, folder)


def sibling(folder: Path, role: str) -> Path:
    """A hidden path beside the run's folder that nothing else names."""
    return folder.with_name(f".{folder.name}.{role}.{uuid.uuid4().hex}")


def publish_folder(bundles: Sequence[Bundle], folder: Path) -> None:
    """Write a run's set of bundles as one folder, swapped in whole.

    Every bundle is written into a fresh folder beside the run's
    folder, which is then renamed onto it, so a reader sees the whole
    set the run produced or the whole set that was there before it,
    never a mixture. A folder already standing there is renamed aside
    first and removed once the new one is in place, so for a moment no
    folder stands at that path. A failure before the new folder is in
    place removes it and leaves everything else as it was, the earlier
    folder restored where it was moved aside. Nothing else in the output
    folder is touched. Each file is created fresh, so two bundles of one
    run deriving one name refuse the second rather than overwrite the
    first.
    """
    staged = sibling(folder, "new")
    try:
        staged.mkdir()
    except OSError as refused:
        raise refusal(folder, refused) from refused
    try:
        for one in bundles:
            with (staged / one.name).open("x", encoding=ENCODING, newline="") as file:
                file.write(one.text)
    except OSError as refused:
        shutil.rmtree(staged, ignore_errors=True)
        raise refusal(staged / one.name, refused) from refused
    aside = None
    if folder.exists() or folder.is_symlink():
        aside = sibling(folder, "old")
        try:
            os.rename(folder, aside)
        except OSError as refused:
            shutil.rmtree(staged, ignore_errors=True)
            raise refusal(folder, refused) from refused
    try:
        os.rename(staged, folder)
    except OSError as refused:
        shutil.rmtree(staged, ignore_errors=True)
        if aside is not None:
            os.rename(aside, folder)
        raise refusal(folder, refused) from refused
    if aside is None:
        return
    try:
        if aside.is_dir() and not aside.is_symlink():
            shutil.rmtree(aside)
        else:
            aside.unlink()
    except OSError as refused:
        raise refusal(aside, refused) from refused


def refusal(destination: Path, refused: OSError) -> Failure:
    """One output path that refused the run's bundles, as a publication failure."""
    return Failure(
        PUBLICATION_FAILURE,
        Diagnostic(
            ERROR,
            f"the output path {str(destination)!r} refused the bundle: {refused}",
            code=PUBLICATION_FAILED,
            remedy="name an existing folder the run can write",
        ),
    )


def selections(
    referrer: Reference | None, requested: Sequence[Reference]
) -> tuple[Target, ...]:
    """Each distinct selection the command line names, in first-named order."""
    return tuple(
        dict.fromkeys(
            (one.path or (referrer.path if referrer else ""), one.fragment)
            for one in requested
        )
    )


def run_name(selected: Sequence[Target]) -> str:
    """The name the selections give a run: each selection's name, joined.

    A selection is named by its working-directory path, its Markdown
    extension removed and each separator written as an underscore, and a
    section adds two underscores and its fragment. The names are joined
    with a plus sign in the order given.
    """
    names = []
    for path, fragment in selected:
        name = str(Path(path).with_suffix("")).replace(os.sep, "_")
        if fragment is not None:
            name += f"__{fragment}"
        names.append(name)
    return "+".join(names)


def bundle_file(target: Target) -> str:
    """The file one selection's bundle is published under."""
    return f"{run_name((target,))}{BUNDLE_SUFFIX}"


def derived_name(referrer: Reference | None, requested: Sequence[Reference]) -> str:
    """The entry bundle's file name, joined from each distinct selection's name."""
    return f"{run_name(selections(referrer, requested))}{BUNDLE_SUFFIX}"


def misshaped(
    links: Sequence[RunSet],
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
) -> list[Diagnostic]:
    """One warning for each target a run-set link names that is no run-set.

    The target is compiled into the bundle, so its selected content is
    the whole document, or the section a fragment names with its
    subsections, read from the source the run parsed. Each link in it
    resolves from the target's own document within that document's root.
    """
    found: list[Diagnostic] = []
    for link in links:
        tokens = parsed[link.target.path]
        source = read[link.target.path]
        if link.target.fragment is None:
            chosen: Sequence[Token] = tuple(regions(tokens))
        else:
            try:
                rooted = section(tokens, link.target.fragment)
            except (Ambiguous, Nested):
                continue
            if rooted is None:
                continue
            chosen = rooted

        def calls(
            destination: str, document: str = link.target.path, root: str = source.root
        ) -> bool:
            return resolvable(document, destination, root) is not None

        held = stray(tokens, chosen, calls)
        if held is not None:
            found.append(misshapen(link, held, source.line(held.line)))
    return found


@dataclass(frozen=True)
class Compiled:
    """One bundle of a run, compiled from its own entry under its own budgets.

    The dispatches are each distinct target the bundle dispatches, at the
    first link naming it. The warnings are held in two runs so a depth
    warning, which only the run's entry raises and only once every
    bundle is compiled, takes its place between them.
    """

    text: str
    name: str
    hops: Sequence[Hop]
    leading: Sequence[Diagnostic]
    trailing: Sequence[Diagnostic]
    captured: Mapping[str, Capture]


def compiled(
    root: Path,
    referrer: Reference | None,
    requested: Sequence[Reference],
    options: argparse.Namespace,
    folder: Path,
) -> Compiled:
    """One bundle compiled as its own entry, every budget counted from it alone.

    Each bundle is read by one agent, so each starts from a fresh count
    of what it opens, reaches and publishes, and its expansion depth is
    counted from its own entry.
    """
    limits = budgets(options)
    try:
        read, parsed, defined, captured, found, hops, running = traverse(
            root, referrer, requested, limits
        )
    except Crossed as crossed:
        raise crossing(crossed) from crossed
    for held in sources(root, read):
        if held == folder or folder in held.parents:
            raise usage_failure(
                f"the output folder {str(folder)!r} holds the input source "
                f"{str(held)!r}"
            )
    bundled, coinciding = compose(
        read, parsed, defined, referrer, requested, found, limits, bundle_file
    )
    trailing = misshaped(running, read, parsed)
    if resourced(bundled, limits.of(NESTING)):
        trailing.append(
            Diagnostic(
                WARNING,
                "the bundle names at least one resource, which it carries as the "
                "text its source wrote, so a reader opening the bundle from "
                "another directory may not find it",
                code=RESOURCE_PORTABILITY,
            )
        )
    return Compiled(
        bundled,
        derived_name(referrer, requested),
        hops,
        [*coinciding, *(selfward(hop) for hop in hops if hop.own)],
        trailing,
        captured,
    )


def dispatched_set(
    root: Path,
    entry: Compiled,
    single: Collection[str],
    options: argparse.Namespace,
    folder: Path,
) -> dict[str, Compiled]:
    """Every bundle the entry's dispatches reach, transitively, by target.

    Each distinct target is compiled once, as its own entry, in the
    order the dispatches reaching it were read. A target naming the
    run's own single selection is the entry's bundle.
    """
    built: dict[str, Compiled] = {}
    pending = list(entry.hops)
    while pending:
        hop = pending.pop(0)
        if hop.name in built or hop.name in single:
            continue
        target = replace(hop.target, origin=None, chain=(hop.name,))
        one = compiled(root, None, [target], options, folder)
        built[hop.name] = one
        pending.extend(one.hops)
    return built


def execute(arguments: Sequence[str], stdout: IO[str], reporter: Reporter) -> int:
    """One invocation, from its command line to the status its outcome returns."""
    grammar = parser()
    options = grammar.parse_args(list(arguments))

    if options.help:
        publish(grammar.format_help(), stdout)
        return SUCCESS
    if options.version:
        publish(f"{NAME} {version('prosiform')} ({PROFILE})\n", stdout)
        return SUCCESS
    if options.codes:
        publish("".join(f"{code}\n" for code in CODES), stdout)
        return SUCCESS

    if not options.references:
        raise usage_failure("at least one entry reference is required")
    if options.output == STANDARD_OUTPUT:
        raise usage_failure(
            "-o - names standard output, which carries no bundle; -o names the "
            "folder the run's bundles are written under"
        )
    requested = [entry(reference) for reference in options.references]
    if not options.referrer:
        for one in requested:
            if not one.path:
                raise usage_failure(
                    f"the fragment-only reference {one.original!r} needs -f to "
                    f"name the document it resolves against"
                )

    root = Path.cwd().resolve()
    referring = entry(options.referrer) if options.referrer else None
    if referring is not None:
        referring = replace(referring, chain=(identity(referring),))
    requested = entered(referring, requested)

    selected = selections(referring, requested)
    folder = Path(options.output, run_name(selected)).resolve()
    first = compiled(root, referring, requested, options, folder)
    single = {requested[0].chain[0]} if len(selected) == 1 else set()
    built = dispatched_set(root, first, single, options, folder)

    def onward(target: Reference) -> Sequence[Hop]:
        name = identity(target)
        return first.hops if name in single else built[name].hops

    try:
        cycle(first.hops, single, onward)
    except Refused as refused:
        raise Failure(INPUT_FAILURE, refused.diagnostic) from refused
    captured = {
        path: held
        for one in (first, *built.values())
        for path, held in one.captured.items()
    }
    if options.fault == SOURCE_CHANGED_FAULT:
        rewrite_sources(root, captured)
    recheck(root, captured)
    if options.fault == INTERNAL_FAULT:
        raise Faulted("the run was asked to fail in itself")
    deep = analysed(first.hops, single, onward)
    bundles = [
        Bundle(first.text, first.name, [*first.leading, *deep, *first.trailing]),
        *(
            Bundle(one.text, one.name, [*one.leading, *one.trailing])
            for one in built.values()
        ),
    ]
    publication(bundles, folder, budgets(options), reporter, options.check)
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
