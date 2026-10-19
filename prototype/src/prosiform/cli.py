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

Every entry document the run names is read as bytes, required to be valid
UTF-8, stripped of the transport metadata it carries ahead of its content
and parsed under the declared profile, and a source carrying a construct
that profile refuses fails as the refusal it is. Every location a
diagnostic reports is the location in the file the author holds, whatever
the strip removed ahead of it.

A reference with no fragment, or with an empty one, selects the whole
document, and each document so selected becomes one file group of the
bundle, the groups ordered by root-relative path. A reference carrying a
nonempty fragment names a section, and section selection is not part of
this build: such a run publishes nothing and returns the
unexpected-internal-error status, which says that the build cannot carry
the request out rather than that anything is wrong with the source it
names.

The bundle is published once the whole candidate is built. A
validation-only run publishes nothing, to either stream or to a named
file; a run naming an output file writes it atomically, through a
neighbouring temporary file renamed into place, so a reader of that path
sees the previous bytes or the whole bundle and never a partial one.
"""

import argparse
import os
import re
import sys
import tempfile
from collections.abc import Sequence
from importlib.metadata import version
from pathlib import Path
from typing import IO, NoReturn

from prosiform import PROFILE
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
from prosiform.diagnostics import ERROR, FORMATS, TEXT, Diagnostic, Reporter
from prosiform.profile import SUFFIXES, Refusal, is_markdown, parse, refusals
from prosiform.source import (
    CLOSERS,
    ENCODING,
    UNTERMINATED_FRONTMATTER,
    Source,
    Unterminated,
    content,
    decode,
    fragments,
    lines,
)

NAME = "prosiform"

SUCCESS = 0
INPUT_FAILURE = 1
USAGE_FAILURE = 2
PUBLICATION_FAILURE = 3
INTERNAL_ERROR = 4

STANDARD_OUTPUT = "-"
FRAGMENT = "#"

MIN_DEPTH = 1
MAX_DEPTH = 6

INVALID_ENCODING = "E_INVALID_ENCODING"
INVALID_GROUP_RULE = "E_INVALID_GROUP_RULE"
INVALID_USAGE = "E_INVALID_USAGE"
PUBLICATION_FAILED = "E_PUBLICATION_FAILED"
ROOT_NOT_FOUND = "E_ROOT_NOT_FOUND"
SOURCE_OUTSIDE_ROOT = "E_SOURCE_OUTSIDE_ROOT"
TARGET_NOT_FOUND = "E_TARGET_NOT_FOUND"
UNEXPECTED_INTERNAL_ERROR = "E_UNEXPECTED_INTERNAL_ERROR"
UNSUPPORTED_ENTRY_SUFFIX = "E_UNSUPPORTED_ENTRY_SUFFIX"

GROUP_RULE = re.compile(r"^([^:/]+):([0-9]+)$")
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


def usage_failure(message: str, code: str = INVALID_USAGE) -> Failure:
    """A command line the contract's grammar does not admit.

    Every such fault leads a caller to one remedy, so they share one
    code. A grouping rule is the exception the contract itself draws: its
    code names a defect in the rule's value, which the same code reports
    as an input failure when the slug names no directory.
    """
    return Failure(
        USAGE_FAILURE,
        Diagnostic(ERROR, message, code=code, remedy=f"run {NAME} --help for usage"),
    )


def input_failure(
    message: str,
    code: str,
    remedy: str = "",
    reference: str | None = None,
    source: str | None = None,
) -> Failure:
    """A command line that is well formed and names something the run refuses."""
    return Failure(
        INPUT_FAILURE,
        Diagnostic(
            ERROR,
            message,
            code=code,
            reference=reference,
            source=source,
            remedy=remedy or None,
        ),
    )


class Parser(argparse.ArgumentParser):
    """An argument parser whose grammar failures are the command's own."""

    def error(self, message: str) -> NoReturn:
        raise usage_failure(message)


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


def document(reference: str) -> str:
    """The document part of one entry reference, empty for a fragment alone."""
    return reference.partition(FRAGMENT)[0]


def fragment(reference: str) -> str:
    """The fragment one entry reference carries, empty where it names none.

    An absent fragment and an empty one are the same whole-document
    reference, so both read as no fragment here.
    """
    return reference.partition(FRAGMENT)[2]


def relative(root: Path, name: str) -> str:
    """One source's normalized root-relative path, which names its file group."""
    return (root / name).resolve().relative_to(root).as_posix()


def entries(referrer: str | None, references: Sequence[str]) -> list[tuple[str, str]]:
    """Each distinct document this run reads, and the reference that names it.

    A referring document is a source of the run like any other, and two
    references naming one document name one source.
    """
    named: list[tuple[str, str]] = []
    seen: set[str] = set()
    for reference in ([referrer] if referrer else []) + list(references):
        name = document(reference)
        if name and name not in seen:
            seen.add(name)
            named.append((reference, name))
    return named


def sources(root: Path, named: Sequence[tuple[str, str]]) -> set[Path]:
    """Every path this run reads from, resolved against the allowed source root."""
    return {(root / name).resolve() for _, name in named}


def location(name: str, at: int | None) -> str:
    """One source location: the document, and the line where the parser knows one."""
    return name if at is None else f"{name}:{at}"


def read_entry(root: Path, reference: str, name: str) -> Source:
    """One entry document's content, read under the allowed source root.

    The bytes are read without newline translation, so a CRLF source
    reaches the scan spelled as the file spells it, and they are decoded
    strictly, so a source that is not valid UTF-8 fails here as the source
    defect it is rather than reaching the command's generic handler.
    """
    if not is_markdown(name):
        raise input_failure(
            f"the entry reference {reference!r} names a document whose suffix is "
            f"outside the {PROFILE} profile",
            code=UNSUPPORTED_ENTRY_SUFFIX,
            remedy=f"name a document ending {' or '.join(SUFFIXES)}",
            reference=reference,
        )
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise input_failure(
            f"the entry reference {reference!r} normalizes to {str(path)!r}, which "
            f"is outside the allowed source root",
            code=SOURCE_OUTSIDE_ROOT,
            remedy="name a document the source root carries",
            reference=reference,
        )
    if not path.is_file():
        raise input_failure(
            f"the entry reference {reference!r} names no document under the "
            f"allowed source root",
            code=TARGET_NOT_FOUND,
            remedy="name a document the source root carries",
            reference=reference,
        )
    try:
        text = decode(path.read_bytes())
    except UnicodeDecodeError as undecodable:
        raise input_failure(
            f"the entry reference {reference!r} names a document that is not valid "
            f"{ENCODING.upper()}: byte {undecodable.start}, "
            f"{undecodable.reason}",
            code=INVALID_ENCODING,
            remedy=f"save the document as {ENCODING.upper()}",
            reference=reference,
            source=name,
        ) from undecodable
    try:
        return content(text)
    except Unterminated as unclosed:
        raise input_failure(
            f"the entry reference {reference!r} names a document whose frontmatter "
            f"opener is closed by no later line of exactly "
            f"{' or '.join(CLOSERS)}",
            code=UNTERMINATED_FRONTMATTER,
            remedy=f"close the block with a line of exactly {' or '.join(CLOSERS)}",
            reference=reference,
            source=location(name, unclosed.line),
        ) from unclosed


def refused(name: str, source: Source, refusal: Refusal) -> Failure:
    """One construct the profile refuses, reported against the source carrying it.

    The line the parser reports is a line of the content the strip
    returned, and the line the diagnostic carries is the line that content
    occupies in the file.
    """
    return input_failure(
        refusal.message,
        code=refusal.code,
        remedy=refusal.remedy,
        reference=refusal.reference,
        source=location(name, source.line(refusal.line)),
    )


def directories(root: Path) -> set[str]:
    """The name of every directory under the allowed source root."""
    found: set[str] = set()
    for _, below, _ in os.walk(root):
        found.update(below)
    return found


def contributing(root: Path, references: Sequence[str]) -> dict[str, str]:
    """Each file group the bundle carries, by the path that names it.

    A reference with no fragment selects a whole document, which is the
    group. Two references naming one document name one group, and the
    groups are ordered by root-relative path so one selection always
    bundles to the same bytes.
    """
    selected: dict[str, str] = {}
    for reference in references:
        if fragment(reference):
            continue
        name = document(reference)
        selected.setdefault(relative(root, name), name)
    return dict(sorted(selected.items()))


def unambiguous(paths: Sequence[str]) -> None:
    """Hold each file heading to naming one source, as a reader must read it."""
    headed: dict[str, str] = {}
    for path in paths:
        title = heading_text(path)
        if title in headed:
            raise input_failure(
                f"{path!r} and {headed[title]!r} both head a file group {title!r}, "
                f"which a reader cannot tell apart",
                code=AMBIGUOUS_FILE_GROUP,
                remedy="bundle one of the two, or rename one of the documents",
                reference=path,
            )
        headed[title] = path


def compose(root: Path, read: dict[str, Source], references: Sequence[str]) -> str:
    """The complete bundle candidate: its entry line and one group per source."""
    selected = contributing(root, references)
    unambiguous(list(selected))
    groups: list[Group] = []
    for path, name in selected.items():
        source = read[name]
        try:
            groups.append(group(path, parse(source.text), lines(source.text)))
        except Overflow as beyond:
            raise input_failure(
                f"{path!r} emits the heading {beyond.heading!r} at level "
                f"{beyond.level}, which is beyond H{MAX_LEVEL}",
                code=HEADING_DEPTH_OVERFLOW,
                remedy="raise the heading in the source, or select a section of it",
                reference=path,
                source=path,
            ) from beyond
    assigned = fragments([heading for one in groups for heading in one.headings])
    named = []
    at = 0
    for one in groups:
        named.append((one.headings[0], assigned[at]))
        at += len(one.headings)
    return assemble(entry_line(named), groups)


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


def execute(arguments: Sequence[str], stdout: IO[str]) -> int:
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
    if not options.referrer:
        for reference in options.references:
            if not document(reference):
                raise usage_failure(
                    f"the fragment-only reference {reference!r} needs --from to "
                    f"name the document it resolves against"
                )
    inforce = rules(options.group)

    root = Path(options.root).resolve()
    named = entries(options.referrer, options.references)
    reading = sources(root, named)
    if options.output != STANDARD_OUTPUT:
        destination = Path(options.output).resolve()
        if destination in reading:
            raise usage_failure(
                f"the output path {options.output!r} names an input source"
            )

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

    read: dict[str, Source] = {}
    for reference, name in named:
        source = read_entry(root, reference, name)
        refusal = next(refusals(parse(source.text)), None)
        if refusal is not None:
            raise refused(name, source, refusal)
        read[name] = source

    selecting = [reference for reference in options.references if fragment(reference)]
    if selecting:
        raise Failure(
            INTERNAL_ERROR,
            Diagnostic(
                ERROR,
                f"this build bundles whole documents and carries no section "
                f"selection, so {selecting[0]!r} names content it cannot select",
                code=UNEXPECTED_INTERNAL_ERROR,
                remedy="use a build that carries one, or name the whole document",
            ),
        )

    bundled = compose(root, read, options.references)
    if options.check:
        return SUCCESS
    if options.output == STANDARD_OUTPUT:
        publish(bundled, stdout)
    else:
        publish_file(bundled, Path(options.output).resolve())
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
        return execute(arguments, out)
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
