"""Compile captured Markdown sources, each link classified by its target's declaration.

Positional files resolve from the invocation working directory, and every
link resolves from the file carrying it. A link naming a Markdown document is
a dependency when that document's frontmatter declares `prosiform`, which a
frontmatter-only probe answers once per path. Bounded no-follow capture
retains bytes, metadata and filesystem identities; publication rechecks every
captured source and bound directory. Discovery, rewriting and candidate
validation read one record of declarations."""

import argparse
import errno
import os
import posixpath
import re
import shutil
import sys
import uuid
from collections.abc import Callable, Collection, Iterable, Iterator, Mapping, Sequence
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
    read_head,
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
    Unplaced,
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
    DECLARING,
    DEFERRAL_MARK,
    DISPATCH_MARK,
    DRIVE,
    PARALLEL_MARK,
    SEPARATOR,
    UNSUBSTITUTED,
    Declarations,
    Malformed,
    OutsideRoot,
    Pairing,
    Probed,
    Reference,
    Substitution,
    components,
    conflicting,
    directive,
    gapped,
    identity,
    inside,
    named,
    operators,
    resolve,
    withholding,
    withholding_target,
)
from prosiform.composition import (
    Colliding,
    Composed,
    Cycling,
    Overflowing,
    Parentless,
    compositions,
    contributions,
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
    HEADING_COLLISION,
    Anchors,
    Hop,
    Refused,
    analysed,
    anchors,
    collisions,
    cycle,
    selfward,
    subsections,
    written_in,
)
from prosiform.grouping import member_headings, merged, prepared
from prosiform.limits import (
    BUDGETS,
    EXPANSION_DEPTH,
    FILE_BYTES,
    FILES,
    INPUT_BYTES,
    LINKS,
    NAMED,
    NESTING,
    OUTPUT_BYTES,
    RESOURCE_LIMIT,
    TARGETS,
    Budget,
    Crossed,
    Limits,
    in_force,
)
from prosiform.limits import (
    CODES as LIMITS_CODES,
)
from prosiform.metadata import (
    DEFAULT,
    GROUP,
    INVALID_CONVERSION_METADATA,
    SUBST,
    Conversion,
    InvalidMetadata,
    Membership,
    Preset,
    Subst,
)
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
from prosiform.provenance import Contributing, Target
from prosiform.rewrite import Definition, definitions
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
    closes_head,
    content,
    declaration,
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
    sections,
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
RUN_FOLDER_SUFFIX = ".bundles"
CURRENT_FOLDER = "."
SUBSTITUTION = "="
"""What separates an `-m` pair's original from its alternative."""

INVALID_ENCODING = "E_INVALID_ENCODING"
GROUP_CONFLICT = "E_GROUP_CONFLICT"
INVALID_USAGE = "E_INVALID_USAGE"
PUBLICATION_FAILED = "E_PUBLICATION_FAILED"
SOURCE_CHANGED = "E_SOURCE_CHANGED"
SOURCE_ACCESS = "E_SOURCE_ACCESS"
SOURCE_OUTSIDE_ROOT = "E_SOURCE_OUTSIDE_ROOT"
SOURCE_SYMLINK = "E_SOURCE_SYMLINK"
TARGET_NOT_FOUND = "E_TARGET_NOT_FOUND"
UNEXPECTED_INTERNAL_ERROR = "E_UNEXPECTED_INTERNAL_ERROR"
UNSUPPORTED_ENTRY_SUFFIX = "E_UNSUPPORTED_ENTRY_SUFFIX"

RESOURCE_PORTABILITY = "W_RESOURCE_PORTABILITY"
COINCIDENT_HEADING = "W_COINCIDENT_HEADING"
EARLIER_SET_RETAINED = "W_EARLIER_SET_RETAINED"
MOCK_SUBSTITUTED = "W_MOCK_SUBSTITUTED"
MOCK_UNUSED = "W_MOCK_UNUSED"
PRESET_UNUSED = "W_PRESET_UNUSED"

OPERATOR_NAMES = {
    DEFERRAL_MARK: "the deferral mark",
    DISPATCH_MARK: "the dispatch mark",
    PARALLEL_MARK: "the parallel dispatch mark",
}

CODES = tuple(
    sorted(
        {
            INVALID_ENCODING,
            GROUP_CONFLICT,
            INVALID_USAGE,
            PUBLICATION_FAILED,
            SOURCE_CHANGED,
            SOURCE_ACCESS,
            SOURCE_OUTSIDE_ROOT,
            SOURCE_SYMLINK,
            TARGET_NOT_FOUND,
            UNEXPECTED_INTERNAL_ERROR,
            UNSUPPORTED_ENTRY_SUFFIX,
            RESOURCE_PORTABILITY,
            COINCIDENT_HEADING,
            EARLIER_SET_RETAINED,
            MOCK_SUBSTITUTED,
            MOCK_UNUSED,
            PRESET_UNUSED,
            *BUNDLE_CODES,
            *CANDIDATE_CODES,
            *DISPATCH_CODES,
            *LIMITS_CODES,
            *PROFILE_CODES,
            *SOURCE_CODES,
        }
    )
)

SOURCE_CHANGED_FAULT = "source-changed"
INTERNAL_FAULT = "internal"
CLEANUP_FAULT = "cleanup-refused"
FAULTS = (SOURCE_CHANGED_FAULT, INTERNAL_FAULT, CLEANUP_FAULT)
FAULT_VARIABLE = "PROSIFORM_FAULT"

DECIMAL = re.compile(r"^[0-9]+$")


def budget_line(budget: Budget) -> str:
    """One budget's line of the help: its default, what it counts, and its floor."""
    floor = f"; at least {budget.least}" if budget.least > 1 else ""
    return f"default {budget.default}; {budget.counted}{floor}"


BUDGET_TABLE = "budgets:\n" + "".join(
    f"  {budget.name:<14}{budget_line(budget)}\n" for budget in BUDGETS
)

EXIT_STATUSES = """exit statuses:
  0  successful compilation, validation, or informational response
  1  input, dependency, policy, safety, or resource-limit failure
  2  invalid usage or option combination
  3  output publication or delivery failure, a broken pipe among them
  4  unexpected internal error
"""

GUIDE = """# Following a Skill with pf

A skill's links name the documents to read. pf compiles a linked document, \
and everything it reaches, into a bundle that is read whole.

## Compile

From the skill's directory, which holds `SKILL.md`, run:

```bash
pf -o <folder> <destination>
```

- `<destination>`  The link's destination as written.
- `<folder>`  A working directory outside the repository. The run makes it \
if it is not there.

The run writes its bundles into `<folder>/<name>.bundles/`, where `<name>` is \
the destination's path without its Markdown suffix, each `/` written as `_` \
and a fragment added after `__`: `modes/plan-mode.md` compiles to \
`modes_plan-mode.bundles/modes_plan-mode.bundle.md`, beside a bundle for each \
target it dispatches.

A non-zero exit stops the run and reports pf's diagnostics.

## Inline Targets

A link whose text opens with `↳` names an inline target: compile it, read the \
whole bundle and follow it.

## Following a Bundle

A bundle that opens with a Prosiform section is followed from there: the \
section states how each dispatched bundle in the run's folder is handed to a \
sub-agent, and the steps after it name the bundles they dispatch.
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


def budget_entry(value: str) -> tuple[Budget, int]:
    """One `NAME=VALUE` budget entry: the budget it names and the figure it sets.

    The entry splits at its first `=`. An entry carrying none, a name
    outside the declared budgets and a figure below the budget's floor
    are each a command line the grammar does not admit, refused before
    any source is read.
    """
    name, separator, figure = value.partition("=")
    if not separator:
        raise argparse.ArgumentTypeError(
            f"the budget entry {value!r} carries no '='; write NAME=VALUE"
        )
    if not name:
        raise argparse.ArgumentTypeError(
            f"the budget entry {value!r} names no budget; write NAME=VALUE"
        )
    if name not in NAMED:
        raise argparse.ArgumentTypeError(
            f"the budget name {name!r} is none of the budgets declared: "
            f"{', '.join(NAMED)}"
        )
    budget = NAMED[name]
    limit = override(figure)
    if limit < budget.least:
        raise argparse.ArgumentTypeError(
            f"the {name} budget of {limit} is below {budget.least}, the least "
            f"under which a declaring document can be read"
        )
    return budget, limit


class BudgetEntries(argparse.Action):
    """Each budget entry of the command line, one entry per budget.

    A second entry naming a budget an earlier entry named is refused:
    the two state one budget twice, and only one of the two orders
    would make a run reproducible.
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,
        option_string: str | None = None,
    ) -> None:
        budget, limit = values
        entries = dict(getattr(namespace, self.dest))
        if budget in entries:
            raise argparse.ArgumentError(
                self, f"the {budget.name} budget is named twice; name it once"
            )
        entries[budget] = limit
        setattr(namespace, self.dest, entries)


def budgets(options: argparse.Namespace) -> Limits:
    """Every budget in force: each the command line names, the rest at default."""
    return in_force(options.budgets)


def mock(value: str) -> Pairing:
    """One `ORIGINAL=ALTERNATIVE` pair, each side read from the working directory.

    Both sides are read by the grammar every other reference is read
    by, so a substitute kept above the working directory is named as a
    command-line reference names one. Neither side is matched against
    the mapping: a substitute is material rather than another
    indirection, and a value that is also a key is read from disk.

    A side ending in a separator names a folder rather than a document,
    and that separator is read here, before the reference grammar
    normalizes the path. `closure.normalized` drops an empty path
    segment, so `rules/` and `rules` normalise to one path and the
    separator that states the difference is gone before anything else
    can read it. Both sides of one pair state one kind, because a folder
    and a document answer different questions and one entry cannot ask
    both. A folder side carries no section, because a folder names no
    heading for one to select.
    """
    original, given, alternative = value.partition(SUBSTITUTION)
    if not given or not original or not alternative:
        raise argparse.ArgumentTypeError(f"{value!r} is no ORIGINAL=ALTERNATIVE pair")
    if marked(original) != marked(alternative):
        raise argparse.ArgumentTypeError(
            f"{value!r} names a folder on one side and a document on the other, so "
            f"the entry states two different questions"
        )
    if marked(original) and (
        components(original).fragment or components(alternative).fragment
    ):
        raise argparse.ArgumentTypeError(
            f"{value!r} gives a folder side a section, and a folder names no heading"
        )
    return Pairing(entry(original), entry(alternative), marked(original))


def substs(conversion: Conversion) -> None:
    """Hold each `subst` side a document's presets state to the reference grammar.

    A side is read as every other reference is, so a side the grammar
    refuses, or one carrying a scheme or an authority and naming no
    local document, fails as invalid conversion metadata at its entry.
    The grammar's refusals hold whatever directory a side resolves
    from, so no base is needed to decide them.
    """
    for preset in conversion.presets:
        for at, pair in enumerate(preset.substs):
            for side in (pair.original, pair.alternative):
                try:
                    refusal = (
                        "carries a scheme or an authority, so it names no local "
                        "document"
                        if resolve(side).external
                        else None
                    )
                except (Malformed, OutsideRoot) as unresolvable:
                    refusal = str(unresolvable)
                if refusal is not None:
                    raise InvalidMetadata(
                        Diagnostic(
                            ERROR,
                            f"prosiform.{preset.name}.{SUBST}[{at}] side "
                            f"{side!r} {refusal}",
                            INVALID_CONVERSION_METADATA,
                            location=pair.location,
                        )
                    )


def subst_identity(text: str, document: str) -> tuple[str, str | None]:
    """The document and section one `subst` side names, read from its document.

    A side resolves from the declaring document's directory, as every
    reference the document writes does, and a side naming a section
    alone names a section of the declaring document.
    """
    found = resolve(text, posixpath.dirname(document))
    return (found.path or document, found.fragment)


def preset_refusal(
    message: str,
    remedy: str,
    reference: Reference,
    location: Location,
    related: tuple[Location, str] | None = None,
) -> Failure:
    """One preset rule stated twice or against itself, as the invalid usage it is.

    The location is the entry the refusal names, and a rule stated twice
    carries its other statement as the related location.
    """
    return Failure(
        USAGE_FAILURE,
        Diagnostic(
            ERROR,
            message,
            code=INVALID_USAGE,
            reference=reference.original,
            chain=reference.chain or None,
            remedy=remedy,
            location=location,
            related=None
            if related is None
            else (
                RelatedLocation(
                    related[0].file, related[0].line, related[0].column, related[1]
                ),
            ),
        ),
    )


def stated_once(conversion: Conversion, found: Reference) -> None:
    """Hold each preset a document declares to stating each of its rules once.

    A preset mapping two `subst` keys that normalise to one identity,
    mapping a key to an alternative of its own identity, or writing a key
    naming a section alone states a rule the run cannot apply as written,
    so each is invalid usage at the entry. A key names the document whose
    references it redirects, which a section alone does not. Identities
    are read from the declaring document, the reference that opened it
    being `found`.
    """
    for preset in conversion.presets:
        keys: dict[tuple[str, str | None], int] = {}
        for at, pair in enumerate(preset.substs):
            entry = f"prosiform.{preset.name}.{SUBST}[{at}]"
            if not components(pair.original).path:
                raise preset_refusal(
                    f"{entry} key {pair.original!r} names a section alone, and a "
                    f"key names the document whose references it redirects",
                    "name the document the section belongs to, as rules.md#Checks",
                    found,
                    pair.location,
                )
            key = subst_identity(pair.original, found.path)
            if key == subst_identity(pair.alternative, found.path):
                raise preset_refusal(
                    f"{entry} maps {pair.original!r} to {pair.alternative!r}, which "
                    f"name one identity, so the alternative stands in for itself",
                    "name an alternative other than the reference it replaces",
                    found,
                    pair.location,
                )
            if key in keys:
                earlier = f"prosiform.{preset.name}.{SUBST}[{keys[key]}]"
                raise preset_refusal(
                    f"{entry} key {pair.original!r} names the identity the key of "
                    f"{earlier} names, so the preset maps one reference twice",
                    "map each reference once in a preset",
                    found,
                    pair.location,
                    (
                        preset.substs[keys[key]].location,
                        f"{earlier} maps {preset.substs[keys[key]].original!r}",
                    ),
                )
            keys[key] = at


def agreed(
    conversion: Conversion, title: str | None, reference: Reference, document: str
) -> None:
    """Hold the presets one title selects to agreeing about every setting they share.

    Selected presets union, so two stating one `group` pair, or mapping
    one `subst` key to one alternative, state one setting. Two stating
    different `group` pairs, or mapping one key to two alternatives,
    leave nothing saying which would take effect, so the reference
    selecting them is invalid usage naming both presets and the setting.
    `default` lies beneath every selection rather than beside it, so it
    disagrees with none. The declaring document is `document`.
    """
    stated: Membership | None = None
    alternatives: dict[tuple[str, str | None], tuple[str, Subst]] = {}
    selected = f"selected by the title {title!r}"
    for preset in keywords(conversion, title):
        one = preset.membership
        stated = stated or one
        if (
            one is not None
            and stated is not None
            and ((stated.group, stated.depth) != (one.group, one.depth))
        ):
            raise preset_refusal(
                f"prosiform.{stated.preset}.{GROUP} and "
                f"prosiform.{one.preset}.{GROUP}, both {selected}, state "
                f"{{{stated.group}: {stated.depth}}} and "
                f"{{{one.group}: {one.depth}}}",
                "state one group pair in the presets one title selects",
                reference,
                stated.group_location,
                (
                    one.group_location,
                    f"prosiform.{one.preset}.{GROUP} is {{{one.group}: {one.depth}}}",
                ),
            )
        for pair in preset.substs:
            key = subst_identity(pair.original, document)
            named_first, first_pair = alternatives.setdefault(key, (preset.name, pair))
            if subst_identity(first_pair.alternative, document) != subst_identity(
                pair.alternative, document
            ):
                raise preset_refusal(
                    f"prosiform.{named_first}.{SUBST} and "
                    f"prosiform.{preset.name}.{SUBST}, both {selected}, map "
                    f"{pair.original!r} to {first_pair.alternative!r} and "
                    f"{pair.alternative!r}",
                    "map the reference to one alternative in the presets one title "
                    "selects",
                    reference,
                    first_pair.location,
                    (
                        pair.location,
                        f"prosiform.{preset.name}.{SUBST} maps {pair.original!r} "
                        f"to {pair.alternative!r}",
                    ),
                )


def marked(text: str) -> bool:
    """Whether one mapping side names a folder, stated by a trailing separator.

    The marker is read from the path component alone, so a side carrying
    a section states its folder marker before the delimiter rather than
    at the end of its text; `rules/#Checks` is then a folder side
    carrying a section, which its own refusal names.

    The marker belongs to the side rather than to its path. The
    reference grammar drops an empty path segment, so `rules/` and
    `rules` normalize to one path, and the separator is read here before
    that normalization runs.
    """
    return components(text).path.endswith(SEPARATOR)


def substitution(options: argparse.Namespace) -> Substitution:
    """The mapping the command line names, by the identity each key normalized to.

    Every key stands for one identity, so two spellings of one path name
    one key and the section a key carries is part of what it names. The
    sides were resolved while the grammar was read, before any source
    was opened. Each key keeps the spelling the caller wrote, because a
    key no reference named is reported as the caller wrote it.

    A folder pairing states a folder on both sides, so its key is a path
    and its substitute a folder: the remainder a reference carries past
    the key is what the substitute folder takes. The Markdown-suffix test
    is applied to the path each reference resolves to under the
    substitute folder rather than to the folder, because a folder
    legitimately names no document while the documents it holds are
    read. A reference landing on something the profile does not read is
    text, by the rule every destination is classified by.

    A mapping shape that states nothing is refused here, because here is
    where the whole mapping is known: a key carrying no document, a
    substitute naming no Markdown document, a key and a substitute naming
    one identity, and a second key naming an identity the first already
    names. The four are decided from one set of identities, so no run
    reaches a shape that would otherwise win silently by being read last.

    The two tests of a pair's own sides answer before the two that
    compare them, so a pair naming no document reports the side that
    names none rather than a coincidence between two empty identities.
    """
    keys: dict[tuple[str, str | None], Reference] = {}
    folders: dict[str, Reference] = {}
    spelled: dict[tuple[str, str | None], str] = {}
    for pairing in options.mock or ():
        named = (pairing.original.path, pairing.original.fragment)
        if pairing.folder:
            if not (pairing.original.path and pairing.alternative.path):
                raise folderless(pairing.original, pairing.alternative)
        elif not pairing.original.path:
            raise documentless(pairing.original)
        elif not is_markdown(pairing.alternative.path):
            raise unbundleable(pairing.original, pairing.alternative)
        if identity(pairing.original) == identity(pairing.alternative):
            raise self_mocked(pairing.original, pairing.alternative)
        if named in spelled:
            raise duplicated(spelled[named], pairing.original)
        spelled[named] = pairing.original.original
        if pairing.folder:
            folders[pairing.original.path] = pairing.alternative
        else:
            keys[named] = pairing.alternative
    return Substitution(keys, spelled, folders)


def duplicated(earlier: str, later: Reference) -> Failure:
    """Two mapping keys naming one identity, as the spellings their author wrote."""
    return usage_failure(
        f"the mapping keys {earlier!r} and {later.original!r} name one identity, "
        f"so only one of them can redirect it",
        reference=later.original,
    )


def self_mocked(original: Reference, alternative: Reference) -> Failure:
    """One mapping entry whose substitute names the identity its key names.

    A folder pair reaching this compares two paths, so its separator is
    not part of what it states: `rules/=rules/` names one folder on both
    sides exactly as `rules.md=rules.md` names one document.
    """
    return usage_failure(
        f"the mapping entry {original.original!r}={alternative.original!r} names "
        f"one identity on both sides, so the substitute stands in for itself",
        reference=original.original,
    )


def folderless(original: Reference, alternative: Reference) -> Failure:
    """One folder pair whose key or substitute names no folder.

    The reference is the side that names none, as each of the other
    refusals names the side the fault sits on: either side of the entry
    can be edited, and the message names the pair whole.
    """
    unsided = original if not original.path else alternative
    return usage_failure(
        f"the mapping entry {original.original!r}={alternative.original!r} names a "
        f"folder by a separator alone, so no folder is named to redirect",
        reference=unsided.original,
    )


def documentless(original: Reference) -> Failure:
    """One mapping key carrying no document, as a section alone does."""
    return usage_failure(
        f"the mapping key {original.original!r} names no document to redirect, so "
        f"no reference can name it",
        reference=original.original,
    )


def unbundleable(original: Reference, alternative: Reference) -> Failure:
    """One mapping entry whose substitute names no Markdown document.

    The substitute is the target outright, so a reference redirected to
    one the profile classifies as a resource is a reference the run
    publishes as text rather than bundles.
    """
    return usage_failure(
        f"the mapping entry {original.original!r}={alternative.original!r} gives a "
        f"substitute naming no Markdown document, so the reference it redirects "
        f"could only be published as text",
        reference=alternative.original,
    )


def parser() -> Parser:
    """The command's grammar: every option the contract declares, and no other."""
    grammar = Parser(
        prog=NAME,
        add_help=False,
        allow_abbrev=False,
        usage=f"{NAME} [OPTIONS] REF [REF ...]",
        description=(
            "Bundle the local Markdown closure of one or more entry references, "
            "and of each target they dispatch, into validated bundles. Run with "
            "no arguments, pf prints the guide to compiling and following them."
        ),
        epilog=f"{BUDGET_TABLE}\n{EXIT_STATUSES}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    grammar.add_argument(
        "-m",
        "--mock",
        dest="mock",
        metavar="ORIGINAL=ALTERNATIVE",
        action="append",
        type=mock,
        help="redirect one reference to the document or section the run reads "
        "instead, given once per pairing; both sides read from the working "
        "directory; repeatable; default none",
    )
    grammar.add_argument(
        "-o",
        dest="output",
        metavar="DIR",
        default=CURRENT_FOLDER,
        help="folder the run's own folder of bundles is written into, made if absent, "
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
        "--budget",
        dest="budgets",
        metavar="NAME=VALUE",
        action=BudgetEntries,
        type=budget_entry,
        default={},
        help="set the budget NAME to VALUE, a positive decimal integer, given once "
        "per budget; repeatable; the budgets, their defaults and what each "
        "counts are listed below",
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
        help="document or document#fragment; paths from cwd",
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
            if option in "odm":
                value = token[at + 1 :].removeprefix("=") or next(tokens, "")
                if option == "d" and value in FORMATS:
                    selected = value
            break
    return selected


def entry(text: str, substitution: Substitution = UNSUBSTITUTED) -> Reference:
    """Normalize a positional reference, keeping the leading parents of a path above.

    The mapping names what the reference resolves to instead, and is
    read after the normalization: an entry reference is written in no
    source, so the mapping applies to the identity the reference
    normalized to rather than to anything a source decides.
    An entry reference stands in no source, so a redirect of one is
    recorded with no source position.
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
            remedy="name a document under the invocation working directory",
            reference=text,
        ) from outside
    if found.external:
        raise input_failure(
            f"the entry reference {text!r} carries a scheme or an authority, so it "
            f"names no local document",
            code=SOURCE_OUTSIDE_ROOT,
            remedy="name a document under the invocation working directory",
            reference=text,
        )
    return substitution.redirect(found)


def entered(requested: Sequence[Reference]) -> list[Reference]:
    """Each entry reference standing at the head of the chain it opens.

    An entry reference is reached by nothing, so the chain a
    diagnostic about it carries is the one identity it names.
    """
    return [replace(one, chain=(identity(one),)) for one in requested]


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


@contextmanager
def reading(found: Reference) -> Iterator[None]:
    """One read of the document a reference names, its refusals as diagnostics.

    A capture and a probe walk the same path, so the refusal a walk
    meets — a symbolic link, a path naming no document, an access fault
    — is reported alike whichever read met it.
    """
    reference, name = found.original, found.path
    written = "the entry reference" if found.origin is None else "the reference"
    try:
        yield
    except Symlinked as linked:
        raise input_failure(
            f"{written} {reference!r} reaches its source through {linked}, "
            f"a symbolic link",
            code=SOURCE_SYMLINK,
            remedy="name the document the symbolic link points at",
            reference=reference,
            source=found.origin,
            chain=found.chain,
        ) from linked
    except Absent as absent:
        raise input_failure(
            missing(found),
            code=TARGET_NOT_FOUND,
            remedy=(
                "name a folder whose documents the key's remainder reaches"
                if found.folder is not None
                else "name a document that exists"
            ),
            reference=reference,
            resolved=name if found.folder is not None else None,
            source=found.origin,
            chain=found.chain,
        ) from absent
    except OSError as error:
        raise input_failure(
            str(error),
            code=SOURCE_ACCESS,
            remedy="check source permissions",
            reference=reference,
            source=found.origin,
            chain=found.chain,
        ) from error


def decoded_text(found: Reference, data: bytes) -> str:
    """The bytes a read returned as text, or the failure their encoding is."""
    written = "the entry reference" if found.origin is None else "the reference"
    try:
        return decode(data)
    except UnicodeDecodeError as undecodable:
        raise input_failure(
            f"{written} {found.original!r} names a document that is not valid "
            f"{ENCODING.upper()}: byte {undecodable.start}, "
            f"{undecodable.reason}",
            code=INVALID_ENCODING,
            remedy=f"save the document as {ENCODING.upper()}",
            reference=found.original,
            source=found.path,
            chain=found.chain,
        ) from undecodable


@contextmanager
def delimiting(found: Reference) -> Iterator[None]:
    """One frontmatter decode, its refusals reported against the reference."""
    written = "the entry reference" if found.origin is None else "the reference"
    try:
        yield
    except InvalidMetadata as invalid:
        raise Failure(
            INPUT_FAILURE,
            replace(invalid.diagnostic, reference=found.original, chain=found.chain),
        ) from invalid
    except Unterminated as unclosed:
        raise input_failure(
            f"{written} {found.original!r} names a document whose frontmatter "
            f"opener is closed by no later line of exactly "
            f"{' or '.join(CLOSERS)}",
            code=UNTERMINATED_FRONTMATTER,
            remedy=f"close the block with a line of exactly {' or '.join(CLOSERS)}",
            reference=found.original,
            source=location(found.path, unclosed.line),
            chain=found.chain,
        ) from unclosed


def read_document(
    root: Path, found: Reference, limits: Limits, total: int = 0
) -> Opened:
    """Capture bounded bytes, typed settings and no-follow source identities.

    Metadata resolves only after the source has been captured within the byte
    and nesting limits. Every source is bounded by the invocation working
    directory. Diagnostics retain physical coordinates and the referring
    chain."""
    name, chain = found.path, found.chain
    if not is_markdown(name):
        raise input_failure(
            f"the entry reference {found.original!r} names a document whose "
            f"suffix is outside the {PROFILE} profile",
            code=UNSUPPORTED_ENTRY_SUFFIX,
            remedy=f"name a document ending {' or '.join(SUFFIXES)}",
            reference=found.original,
            chain=chain,
        )
    observed: list[tuple[str, int, int]] = []
    with reading(found):
        data = read_source(
            root,
            found.walk or name,
            limit=min(limits.of(FILE_BYTES), limits.of(INPUT_BYTES) - total),
            observed=observed,
        )
    try:
        limits.hold(FILE_BYTES, len(data))
        limits.hold(INPUT_BYTES, total + len(data))
    except Crossed as crossed:
        raise unindexable(crossed, name, chain) from crossed
    text = decoded_text(found, data)
    captured = Capture(
        observed[-1][0],
        hashed(data),
        chain,
        found.walk or name,
        tuple(observed[:-1]),
        (observed[-1][1], observed[-1][2]),
        len(data),
    )
    with delimiting(found):
        source = content(
            text,
            file=name,
            max_bytes=limits.of(FILE_BYTES),
            max_depth=limits.of(NESTING),
        )
        substs(source.conversion)
    stated_once(source.conversion, found)
    return Opened(source, len(data), captured)


def probe(root: Path, found: Reference, limits: Limits) -> Probed:
    """Whether the document a reference names exists and declares, its body unread.

    The probe reads the document's head through the walk a capture
    takes, within `file-bytes`, and decodes it as a capture would, so an invalid
    declaration fails the probe with the diagnostic it fails a capture
    with. Nothing it reads is counted against `input-bytes` or kept: answering
    whether a document declares carries nothing into the bundle.

    A head holding no opener declares nothing whatever the file's size,
    so a document larger than `file-bytes` that declares nothing is answered
    without crossing it. A head crossing `file-bytes` before its block closes
    fails the run, since its declaration cannot be read within the
    budget; a declaring document is captured afterwards, and the capture
    holds `file-bytes` over the whole file.

    A path naming no document is answered as absent, and the caller
    reading the link decides what that is. A substitute naming no
    document is refused here: the caller who named it stated the run is
    answerable for it.
    """
    with reading(found):
        try:
            head = read_head(
                root,
                found.walk or found.path,
                limit=limits.of(FILE_BYTES),
                ended=closes_head,
            )
        except Absent:
            if found.redirected:
                raise
            return Probed.ABSENT
    try:
        limits.hold(FILE_BYTES, len(head))
    except Crossed as crossed:
        raise unindexable(crossed, found.path, found.chain) from crossed
    with delimiting(found):
        settings = declaration(
            decoded_text(found, head),
            file=found.path,
            max_bytes=limits.of(FILE_BYTES),
            max_depth=limits.of(NESTING),
        )
    return Probed.DECLARING if settings.declared else Probed.SILENT


def declared_entries(
    requested: Sequence[Reference], declarations: Declarations
) -> None:
    """Hold every entry reference to naming a document that declares `prosiform`.

    An entry reference names the procedure the bundle carries out, so a
    document declaring nothing is no procedure and one naming nothing
    is nothing to carry out: each fails with the code a reference
    naming nothing fails with, before any source is read. An entry
    naming no Markdown document is refused by its suffix when it is
    read, and is not asked.
    """
    for asked in requested:
        if not is_markdown(asked.path):
            continue
        answer = declarations.answer(asked)
        if answer is Probed.DECLARING:
            continue
        stated = (
            "names no document"
            if answer is Probed.ABSENT
            else "names a document whose frontmatter declares no prosiform"
        )
        raise input_failure(
            f"the entry reference {asked.original!r} {stated}, so it names no "
            f"procedure the bundle can carry",
            code=TARGET_NOT_FOUND,
            remedy=(
                "name a document that exists"
                if answer is Probed.ABSENT
                else "declare prosiform in the document's frontmatter"
            ),
            reference=asked.original,
            chain=asked.chain,
        )


def missing(found: Reference) -> str:
    """One reference naming no document, as the reader who must fix it reads it.

    A reference an author wrote names the document that author meant,
    so the reader is told the document is absent. A reference a folder
    key derived names a path nobody wrote, so the message states the
    whole route: the reference as authored, the key that answered it,
    and the path the redirect resolved to.
    """
    if found.folder is None:
        return f"the reference {found.original!r} names no document"
    return (
        f"the reference {found.original!r} is redirected by the mapping key "
        f"{found.folder!r} to {found.path!r}, which names no document"
    )


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


def conformance_fault(environment: Mapping[str, str]) -> str | None:
    """The fault the run's environment asks it to perform on itself, if any.

    Some outcomes the contract declares are facts about the run rather than
    about any document it reads, so a conformance run names one in
    `PROSIFORM_FAULT` and the run performs it. An environment carrying no
    such variable asks for no fault. A value outside the three is refused
    as invalid usage, so a mistyped setting fails rather than passing as a
    run meeting no fault.
    """
    fault = environment.get(FAULT_VARIABLE)
    if fault is None or fault in FAULTS:
        return fault
    raise usage_failure(
        f"{FAULT_VARIABLE} holds {fault!r}, which names no fault; it admits "
        f"{', '.join(FAULTS)}"
    )


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


def contributing(requested: Sequence[Reference]) -> dict[str, list[Reference]]:
    """Each file group the bundle carries, by the path that names it.

    A reference selects from the document it names. The path
    is the identity the reference normalized to, so two references
    spelling one document name one group, which carries what each of
    them selected. The documents are in path order, which is the order
    each round of the traversal reads them in; `placement` decides the
    order the bundle carries them in.
    """
    selected: dict[str, list[Reference]] = {}
    for one in requested:
        selected.setdefault(one.path, []).append(one)
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


def included(found: Sequence[Reference]) -> list[Reference]:
    """Every reference that includes what it names: each one composing nothing.

    A document only composition directives reach contributes its content
    to their contributions alone: it stands in no file group, joins no
    merged group and is carried nowhere else. A document an inclusion
    also reaches keeps that inclusion, carrying what the inclusions
    select, beside its contributions.
    """
    return [one for one in found if not one.composes]


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
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> Iterator[Reference]:
    """Every dependency the selected content of one source carries.

    A use naming a Markdown document whose frontmatter declares
    `prosiform` is a reference the bundle carries, and every other use
    is text: a document declaring nothing is probed and never captured,
    a path naming no document states nothing the bundle answers for,
    and the link reaches the bundle as its author wrote it. The target's declaration
    is the whole of the question, so a document states that it travels
    and every link reaching it agrees.

    A withheld reference is not compiled: the run yields no dependency
    for it, so nothing it names is bundled through that reference, and
    the link reaches the bundle with its mark for the run that compiles
    it. Its target is what `withheld` yields, because a reference naming
    a declaring document is one the run stays responsible for whether
    or not it carries what the reference names.

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

    A composition directive naming a section is a dependency like any
    other, since the run reads what it composes, and it states that it
    composes, so the bundle places its section beneath the directive's
    scope rather than in a group of its own.

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
            found = inside(path, use.destination, substitution, at)
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
        occurrence = replace(
            found,
            origin=at,
            chain=(*chain, identity(found)),
            title=use.title,
            composes=found.fragment is not None and directive(use.label),
        )
        if not declarations.declares(occurrence):
            continue
        yield occurrence


def refusals_of_operators(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> None:
    """Refuse a link whose operators state no one compilation the run can carry out.

    A deferral says when the material is compiled and a dispatch says who
    compiles it, so the two are carried out together, their marks written
    together: a blank between two symbols — two marks, or a mark and a
    composition directive's label — states no one operation. Two dispatch marks
    say who, differently — one sub-agent, or one beside its section's
    others — so a link stating both states two ways for one sub-agent to
    run, and the run says so rather than choosing. An operator names the
    compilation of a declaring Markdown document or section, so one
    opening a link or an image naming anything else — a remote address,
    a resource, a document declaring nothing — states a
    compilation no run performs. Each is a source fault rather than a
    metadata fault: what the author wrote states no compilation the run
    can carry out, and the run reports the link rather than reading it
    one way.

    An operator states that a run or an agent compiles its target, so
    one naming a Markdown path that holds no document names a target
    that cannot be read, and fails as a reference naming nothing does.
    The same link without its operator is text.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        at = location(path, source.line(use.line))
        if gapped(use.opening, use.label):
            raise input_failure(
                f"the link {use.opening!r} writes a blank between "
                + " and ".join(
                    f"{OPERATOR_NAMES[mark]} {mark!r}"
                    for mark in operators(use.opening)
                )
                + " and the symbol after it, which state one operation only "
                "when written together",
                code=UNSUPPORTED_CONSTRUCT,
                remedy="write the symbols with no space between them, and one "
                "space between the last of them and the link's text",
                reference=use.opening,
                source=at,
                chain=(*chain, use.destination),
            )
        if conflicting(use.opening):
            raise input_failure(
                f"the link {use.opening!r} opens with "
                + "".join(
                    f"{OPERATOR_NAMES[mark]} {mark!r}"
                    for mark in operators(use.opening)
                )
                + ", which state two ways for one sub-agent to run",
                code=UNSUPPORTED_CONSTRUCT,
                remedy="open the link's text with the one operator that states how "
                "the material is compiled",
                reference=use.opening,
                source=at,
                chain=(*chain, use.destination),
            )
        if not operators(use.opening):
            continue
        target = (
            None
            if use.resource
            else named(path, use.destination, substitution, at, chain)
        )
        answer = None if target is None else declarations.answer(target)
        if answer is Probed.DECLARING:
            continue
        if answer is Probed.ABSENT:
            raise input_failure(
                f"the link {use.opening!r} opens with an operator and names "
                f"{use.destination!r}, which names no document, so the operator "
                f"states a compilation no run can read",
                code=TARGET_NOT_FOUND,
                remedy="name a Markdown document that exists, or remove the operator",
                reference=use.destination,
                source=at,
                chain=(*chain, use.destination),
            )
        if answer is Probed.SILENT:
            raise input_failure(
                f"the link {use.opening!r} opens with an operator and names "
                f"{use.destination!r}, a document whose frontmatter declares no "
                f"prosiform, so the operator states no compilation the run can "
                f"carry out",
                code=UNSUPPORTED_CONSTRUCT,
                remedy="declare prosiform in the target's frontmatter, or remove "
                "the operator",
                reference=use.destination,
                source=at,
                chain=(*chain, use.destination),
            )
        kind = "image" if use.resource else "link"
        raise input_failure(
            f"the {kind} {use.opening!r} opens with an operator and names "
            f"{use.destination!r}, which is no Markdown document or section, so "
            f"the operator states no compilation the run can carry out",
            code=UNSUPPORTED_CONSTRUCT,
            remedy="name a Markdown document or section, or remove the operator",
            reference=use.destination,
            source=at,
            chain=(*chain, use.destination),
        )


def refusals_of_directives(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> None:
    """Refuse a composition directive no section holds or no document answers.

    A directive places its target beneath the section containing it, so
    one written in the preamble has no scope to place it in. One naming a
    Markdown path that holds no document names a target that cannot be
    read, and fails as a reference naming nothing does. Either label asks
    for a placement the run cannot make, which is a source fault: the run
    reports the link rather than reading it as an ordinary one.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        if not directive(use.label):
            continue
        at = location(path, source.line(use.line))
        if use.title is not None:
            target = (
                None
                if use.resource
                else named(path, use.destination, substitution, at, chain)
            )
            if target is None or declarations.answer(target) is not Probed.ABSENT:
                continue
            raise input_failure(
                f"the directive {use.label!r} names {use.destination!r}, which "
                f"names no document, so its composition has no section to place",
                code=TARGET_NOT_FOUND,
                remedy="name a section of a Markdown document that exists",
                reference=use.destination,
                source=at,
                chain=(*chain, use.destination),
            )
        raise input_failure(
            f"the link {use.label!r} is a composition directive in the preamble, "
            f"which no section holds, so the run has no scope to place "
            f"{use.destination!r} beneath",
            code=UNSUPPORTED_CONSTRUCT,
            remedy="write the directive inside the section its target belongs "
            "beneath, or give the link a label that requests no placement",
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
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> Iterator[Reference]:
    """Every target the selected content of one source withholds.

    A withheld reference naming a declaring Markdown document is one
    this run does not carry and stays responsible for, so its target is
    yielded here to be confirmed. An operator on a reference naming a
    document that declares nothing, or on one naming no Markdown
    document, withholds nothing, and the run refuses it before
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
        at = location(path, source.line(use.line))
        found = withholding_target(
            path, use.destination, use.opening, declarations, substitution, at, chain
        )
        if found is None:
            continue
        yield replace(found, origin=at, chain=(*chain, identity(found)))


def dispatches(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> Iterator[Hop]:
    """Every dispatched link the selected content of one source carries.

    A dispatch is a withheld link whose target the run compiles as a
    bundle of its own, so what is yielded is the target the link names,
    with the place the link is written: the hop a chain of dispatches
    takes from here. The links are those the bundle's dispatch
    sub-sections are placed for, read by the one reader that places
    them, so every hop the run follows has its sub-section. A link with
    no text after its mark leaves that sub-section nothing to be named
    by, so it is refused as the operator refusals are, naming the route.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for region in selected:
        for link in written_in(
            path, source, tokens, region, declarations, substitution
        ):
            if not link.text:
                raise input_failure(
                    f"the link {link.opening!r} dispatches {link.written!r} with "
                    f"no text after its mark, so no sub-section heading can "
                    f"name it",
                    code=UNSUPPORTED_CONSTRUCT,
                    remedy="write the link's text after its mark",
                    reference=link.opening,
                    source=location(path, link.location.line),
                    chain=(*chain, link.written),
                )
            yield Hop(
                replace(
                    link.reference,
                    origin=location(path, link.location.line),
                    chain=(*chain, identity(link.reference)),
                ),
                link.location,
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
    requested: Sequence[Reference],
    limits: Limits,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> tuple[
    dict[str, Source],
    dict[str, list[Token]],
    dict[str, dict[str, Definition]],
    dict[str, Capture],
    list[Reference],
    list[Hop],
]:
    """Every source the run reads and every reference it carries, at the fixed point.

    The entry references are the first frontier. Each round reads the
    sources its frontier names, then reads every group's selected
    content for the dependencies it marks; a dependency naming a
    document and section the run already carries adds no target, and the
    round that discovers no new one is the fixed point. A reference
    graph with a cycle therefore terminates on the identity each
    reference normalized to rather than on a depth the traversal
    refuses at.

    A dependency reaching a carried document and section from a section
    title no earlier dependency reached it from is carried all the same,
    because the title selects that document's presets and each reference
    bundles the document under the selection it made. So is one reaching
    it by the other kind, a directive where an inclusion reached it or
    an inclusion where a directive did, because the bundle places a
    document's content by the references of each kind. It joins the
    references the run carries and not the frontier, since the content
    it selects is content the run already reads.

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
    for the bundles the run compiles from them.
    """
    read: dict[str, Source] = {}
    parsed: dict[str, list[Token]] = {}
    defined: dict[str, dict[str, Definition]] = {}
    captured: dict[str, Capture] = {}
    found = list(requested)
    seen = {(one.path, one.fragment) for one in found}
    titled: set[tuple[str, str | None, str | None, bool]] = set()
    limits.hold(TARGETS, len(seen))
    counted: dict[str, int] = {}
    deferred: dict[tuple[str, str | None], Reference] = {}
    dispatching: dict[str, Hop] = {}
    total = 0
    hop = 0
    frontier = list(requested)
    while frontier:
        hop += 1
        for one in frontier:
            verify_cached(root, one, captured)
            if one.path in read:
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
        reselecting: list[Reference] = []
        for path, selecting in contributing(found).items():
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
            refusals_of_operators(
                path,
                read[path],
                parsed[path],
                chosen,
                reached,
                declarations,
                substitution,
            )
            refusals_of_directives(
                path,
                read[path],
                parsed[path],
                chosen,
                reached,
                declarations,
                substitution,
            )
            for one in withheld(
                path,
                read[path],
                parsed[path],
                chosen,
                reached,
                declarations,
                substitution,
            ):
                verify_cached(root, one, captured)
                deferred.setdefault((one.path, one.fragment), one)
            for link in dispatches(
                path,
                read[path],
                parsed[path],
                chosen,
                reached,
                declarations,
                substitution,
            ):
                dispatching.setdefault(link.name, link)
            for one in required(
                path,
                read[path],
                parsed[path],
                chosen,
                reached,
                declarations,
                substitution,
            ):
                verify_cached(root, one, captured)
                if (one.path, one.fragment, one.title, one.composes) in titled:
                    continue
                titled.add((one.path, one.fragment, one.title, one.composes))
                if (one.path, one.fragment) in seen:
                    reselecting.append(one)
                    continue
                limits.hold(EXPANSION_DEPTH, hop)
                seen.add((one.path, one.fragment))
                limits.hold(TARGETS, len(seen))
                discovered.append(one)
        found.extend(discovered)
        found.extend(reselecting)
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
    )


def confirm(
    tokens: Sequence[Token],
    one: Reference,
) -> None:
    """Hold one withheld reference to naming a document and a heading that exist.

    A deferral says that the material is reached in a run of its own,
    and a dispatch that a sub-agent reaches it, not that nobody is
    answerable for it, so the document is read and
    the fragment is looked up. A withheld target naming no document is
    refused with the operator that withholds it, and one naming no
    heading of the document it resolves to is refused here, each with
    the code and the route a compiled reference naming nothing reports.

    The question is whether the document carries the heading, asked of
    the index of every heading the profile recognizes. Which section a
    fragment roots, and whether two headings make it ambiguous, is what
    the run compiling the link decides; this run says only that the
    target is there to be found.

    The caller supplies the cached index from the source's captured read.
    A withheld-only source contributes no content to a group.
    """
    if one.fragment is None:
        return
    if any(heading.fragment == one.fragment for heading in index(tokens)):
        return
    raise input_failure(
        f"the reference {one.original!r} names no heading of the document it withholds",
        code=TARGET_NOT_FOUND,
        remedy="name a heading the document carries",
        reference=one.original,
        resolved=one.path,
        source=one.origin,
        chain=one.chain,
    )


def keyworded(name: str, title: str) -> bool:
    """Whether a preset name appears as words in one section title.

    The comparison ignores case, and each end of the name meets the
    start or end of the title or a character that is neither a letter
    nor a digit, so `checks` appears in `Checks and Draft` and not in
    `Checklist`. A name carrying no character appears nowhere.
    """
    word = name.casefold()
    folded = title.casefold()
    start = folded.find(word) if word else -1
    while start >= 0:
        end = start + len(word)
        before = folded[start - 1] if start else ""
        after = folded[end] if end < len(folded) else ""
        if not before.isalnum() and not after.isalnum():
            return True
        start = folded.find(word, start + 1)
    return False


def keywords(conversion: Conversion, title: str | None) -> tuple[Preset, ...]:
    """The presets one section title selects, in the order they are declared.

    `default` is in force beneath every selection, so it is selected by
    no spelling; a title absent, as a preamble's is, selects nothing.
    """
    if title is None:
        return ()
    return tuple(
        preset
        for preset in conversion.presets
        if preset.name != DEFAULT and keyworded(preset.name, title)
    )


def pair(conversion: Conversion, title: str | None) -> Membership | None:
    """The `group` pair in force for content one section title selects.

    A selected preset's pair holds over the one `default` states, and the
    selected presets are held to agreeing before it is read; `default`'s
    pair is in force where no selected preset states one. None means no
    pair is in force, and the content keeps its individual file group.
    """
    return next(
        (
            preset.membership
            for preset in keywords(conversion, title)
            if preset.membership is not None
        ),
        conversion.default.membership,
    )


def entry_title(tokens: Sequence[Token], one: Reference) -> str | None:
    """The title an entry reference selects its document's presets by.

    An entry is written in no section, so the document it names supplies
    the title: the heading of the section a section entry names, or the
    document's own title for a whole-document entry, absent where the
    document carries none.
    """
    if one.fragment is not None:
        return next(
            (
                heading.text
                for heading in index(tokens)
                if heading.fragment == one.fragment
            ),
            None,
        )
    title = document_title(tokens)
    if title is None or title.map is None:
        return None
    line = title.map[0] + 1
    return next((text for at, text in sections(tokens) if at == line), None)


def selecting_title(
    tokens: Sequence[Token], reference: Reference, entries: Collection[Reference]
) -> str | None:
    """The title one reference selects its document's presets by.

    An entry is written in no section, so `entry_title` reads the title
    its own document supplies; any other reference selects by the title
    of the section holding it.
    """
    return entry_title(tokens, reference) if reference in entries else reference.title


def unselected(
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    selected: Mapping[str, Sequence[Reference]],
    entries: Collection[Reference],
) -> dict[str, tuple[str, ...]]:
    """The presets of each carried document that no reference reaching it selected.

    `default` is in force wherever its document is compiled, so it is
    never among them. The names keep the order the document declares
    them in. A document reached only through a deferral is carried by
    no bundle, so its presets are weighed by none.
    """
    left: dict[str, tuple[str, ...]] = {}
    for path, references in selected.items():
        conversion = read[path].conversion
        chosen = {
            preset.name
            for reference in references
            for preset in keywords(
                conversion, selecting_title(parsed[path], reference, entries)
            )
        }
        left[path] = tuple(
            preset.name
            for preset in conversion.presets
            if preset.name != DEFAULT and preset.name not in chosen
        )
    return left


def joined(
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    selected: Mapping[str, Sequence[Reference]],
    entries: Collection[Reference],
) -> dict[str, tuple[Membership, ...]]:
    """The `group` pairs in force for each document the bundle carries.

    Each reference reaching a document selects that document's presets
    by its own title, the title of the section it is written in or, for
    an entry, the title `entry_title` reads, so a document's presets
    govern its content and no other document's. The presets one
    reference selects are held to agreeing before their pair is read,
    so one reference places the document under one pair at most. A
    document carries the pair each reference reaching it put in force,
    each once.
    """
    joins: dict[str, tuple[Membership, ...]] = {}
    for path, references in selected.items():
        conversion = read[path].conversion
        held: dict[Membership, None] = {}
        for reference in references:
            title = selecting_title(parsed[path], reference, entries)
            agreed(conversion, title, reference, path)
            one = pair(conversion, title)
            if one is not None:
                held[one] = None
        joins[path] = tuple(held)
    return joins


def group_depths(joins: Mapping[str, Sequence[Membership]]) -> dict[str, int]:
    """Consistent depths for named groups, ordered by source path.

    A document is a member of each group the pairs its references put in
    force name, so one document two references place differently may
    hold one depth in one group and another in a second; within one
    group every membership must agree.
    """
    members: dict[str, list[tuple[str, Membership]]] = {}
    for path in sorted(joins):
        for one in joins[path]:
            members.setdefault(one.group, []).append((path, one))
    depths: dict[str, int] = {}
    for name in sorted(members):
        _, first = members[name][0]
        depths[name] = first.depth
        for _, current in members[name][1:]:
            if current.depth != first.depth:
                location = current.depth_location
                raise Failure(
                    INPUT_FAILURE,
                    Diagnostic(
                        ERROR,
                        f"prosiform.{first.preset}.{GROUP} for group "
                        f"{name!r} is {first.depth}; "
                        f"another member declares {current.depth}",
                        code=GROUP_CONFLICT,
                        location=first.depth_location,
                        related=(
                            RelatedLocation(
                                location.file,
                                location.line,
                                location.column,
                                f"prosiform.{current.preset}.{GROUP} for group "
                                f"{name!r} is {current.depth}",
                            ),
                        ),
                        remedy="use one depth for every contributing group member",
                    ),
                )
    return depths


def membership(joins: Sequence[Membership], named: str) -> Membership | None:
    """The membership joining one document to the named group, where it joins it."""
    return next((one for one in joins if one.group == named), None)


@dataclass(frozen=True)
class Named:
    """One generated heading, and where the source it names is located."""

    text: str
    location: Location


def file_named(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    wrapped: bool,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> Named | None:
    """One document's file heading, located at the title it carries or at the document.

    A titled document is headed by its title, so the heading is located
    on the line that title stands on. The parent opens the bundle on
    that title rather than on a heading the bundle writes, and is headed
    by it all the same. An untitled document is headed by its path,
    which names the document as a whole, so the heading is located at
    the document's first position; a parent the bundle opens without a
    file heading and without a single title is headed by nothing.

    The text is the one the group emits, so it is read under the same
    mapping: a title carrying a withheld link whose target the mapping
    redirected publishes without its mark, and the heading this warning
    compares is the heading a reader meets.
    """
    title = document_title(tokens)
    if title is None and not wrapped:
        return None
    at = None if title is None or title.map is None else title.map[0] + 1
    line = source.line(at)
    return Named(
        file_heading(path, tokens, declarations, substitution),
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
    joins: Mapping[str, Sequence[Membership]],
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
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
            heading = file_named(
                named, read[named], parsed[named], one.filed, declarations, substitution
            )
            if heading is not None:
                files.setdefault(heading.text.casefold(), (at, []))[1].append(heading)
            continue
        joining = {
            path: pair
            for path in selected
            if (pair := membership(joins[path], named)) is not None
        }
        names = member_headings(list(joining), named)
        members: dict[str, list[Named]] = {}
        for path, pair in joining.items():
            members.setdefault(names[path].casefold(), []).append(
                Named(names[path], pair.group_location)
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
    found: Sequence[Reference],
    entries: Collection[Reference],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> tuple[dict[str, list[Reference]], dict[str, str]]:
    """Each document the bundle includes, in the order a reference first names it.

    The entry references are read first, in the order the invocation
    gives them, and then the selected content of each placed document,
    in the order the documents were placed, each in source order. A
    document is placed at the first reference that names it, so the
    parent leads and an author orders what follows by the order the
    links are written in. Every document the bundle carries is reached
    from an entry reference by a chain of the links read here, so the
    order covers them all.

    A composition directive places nothing: the section it names is
    content of the document whose group carries the directive, so that
    section is read where the directive is written, once, and a link
    it carries places a document as one its scope's document writes,
    a directive it carries reading its own section the same way.

    The first mapping holds the references including each document,
    as `included` keeps them. The second names, for each document a
    link placed, the document whose group carries that link. An entry
    is placed by the invocation rather than by a document, so it is
    absent there.
    """
    selected = contributing(included(found))
    order = list(dict.fromkeys(one.path for one in entries if one.path in selected))
    placers: dict[str, str] = {}
    composed: set[tuple[str, str | None]] = set()

    def place(path: str, chosen: Selection | None, holder: str) -> None:
        for one in required(
            path, read[path], parsed[path], chosen, (), declarations, substitution
        ):
            if one.composes:
                if (one.path, one.fragment) not in composed:
                    composed.add((one.path, one.fragment))
                    section_of = selection(one.path, parsed[one.path], [one], entries)
                    place(one.path, section_of, holder)
                continue
            if one.path in selected and one.path not in order:
                order.append(one.path)
                placers[one.path] = holder

    at = 0
    while at < len(order):
        path = order[at]
        at += 1
        place(path, selection(path, parsed[path], selected[path], entries), path)
    return {path: selected[path] for path in order}, placers


Division = tuple[str, bool]


def divisions(
    selected: Mapping[str, Sequence[Reference]],
    joins: Mapping[str, Sequence[Membership]],
) -> list[Division]:
    """Each division of the bundle, in the order its first document is placed.

    A division is a file group, named by its document's path, or a
    merged group, named by the group it is; the flag says which. A
    document the pairs in force for it pair with no group is its own
    file group, and every other document joins each merged group a
    membership names. Merged groups sharing their first document stand
    in the order its memberships name them.
    """
    found: dict[Division, None] = {}
    for path in selected:
        if not joins[path]:
            found[(path, False)] = None
        for one in joins[path]:
            found.setdefault((one.group, True), None)
    return list(found)


def holders(
    order: Sequence[Division],
    merging: Mapping[str, Sequence[str]],
    placers: Mapping[str, str],
    joins: Mapping[str, Sequence[Membership]],
) -> dict[Division, Division]:
    """The division each nested group stands inside.

    A merged group stands inside the division holding the document whose
    link placed its first member: that document's file group, or the
    merged group it joins, the first of them the bundle places where it
    joins several. A group whose first member is an entry is held by no
    division and stands at the top level, as every file group does.

    The holding division carries a document placed before the group's
    first member, so it precedes the group in placement order and no
    group holds itself, directly or through another.
    """
    rank = {one: at for at, one in enumerate(order)}
    held: dict[Division, Division] = {}
    for division in order:
        name, grouped = division
        if not grouped:
            continue
        placer = placers.get(merging[name][0])
        if placer is None:
            continue
        held[division] = (
            (placer, False)
            if not joins[placer]
            else min(((one.group, True) for one in joins[placer]), key=rank.__getitem__)
        )
    return held


def composed(
    division: Division,
    built: Mapping[Division, Group],
    nested: Mapping[Division, Sequence[Division]],
) -> list[Group]:
    """One division's result: its own group, then each group nested in it, composed.

    Each nested group is composed with everything it holds before the
    division holding it merges that result, so a group arrives in its
    holder's result with what it placed already inside it.
    """
    return [
        built[division],
        *(
            one
            for inner in nested.get(division, ())
            for one in composed(inner, built, nested)
        ),
    ]


def assembled(
    read: dict[str, Source],
    parsed: dict[str, list[Token]],
    defined: dict[str, dict[str, Definition]],
    selected: dict[str, list[Reference]],
    entries: Collection[Reference],
    assigned: dict[tuple[str, str | None], str] | None,
    joins: Mapping[str, Sequence[Membership]],
    placers: Mapping[str, str],
    chains: Mapping[str, Sequence[str]],
    limits: Limits,
    dispatching: Anchors | None = None,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Contributing | None = None,
) -> tuple[list[Group], Composed]:
    """Each group the bundle carries, its links rewritten where a map says so.

    The documents arrive in placement order, which `placement` decides,
    with the document whose link placed each. A document the pairs in
    force for it pair with no group is its own file group. Every other
    document joins each merged group a membership names, once however
    often it is named, and each group carries its members in placement
    order, so the pairs in force for a document place its own sections
    and no other document's.

    Composition runs from the leaves up. A merged group whose first
    member a document's link placed nests inside that document's
    division, after everything the division carries of its own, its
    headings one level deeper for each division enclosing it; `composed`
    finishes each nested group before its holder merges it. A file
    group, and a merged group whose first member is an entry, stands at
    the top level where its first document is placed, so the group
    carrying the parent leads and one selection always bundles to the
    same bytes.

    The sections the bundle's directives compose are placed once every
    group stands where it is emitted, and the contribution heading each
    composing link points at is returned beside the groups. The
    composing map holds each composing link's destination by the placing
    of the region writing it: the authored links' under none, which the
    groups are rewritten through, and every contribution's own beside
    them.
    """
    parent = parent_document(entries)
    inforce = group_depths(joins)
    merging: dict[str, list[str]] = {}
    for path in selected:
        for one in joins[path]:
            members = merging.setdefault(one.group, [])
            if path not in members:
                members.append(path)
    order = divisions(selected, joins)
    held = holders(order, merging, placers, joins)
    levels: dict[Division, int] = {}
    nested: dict[Division, list[Division]] = {}
    for division in order:
        holder = held.get(division)
        levels[division] = 1 if holder is None else levels[holder] + 1
        if holder is not None:
            nested.setdefault(holder, []).append(division)
    built: dict[Division, Group] = {}
    authored = None if composing is None else composing.get((), {})
    with assembling(chains):
        for division in order:
            path, grouped = division
            if grouped:
                continue
            tokens = parsed[path]
            built[division] = group(
                path,
                tokens,
                lines(read[path].text),
                defined[path],
                selection(path, tokens, selected[path], entries),
                assigned,
                declarations,
                path == parent,
                dispatching,
                read[path].first_line,
                substitution,
                authored,
            )
        for named, paths in merging.items():
            depth = inforce[named]
            built[(named, True)] = merged(
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
                        declarations,
                        path == parent,
                        dispatching,
                        read[path].first_line,
                        substitution,
                        authored,
                    )
                    for path in paths
                ],
                parent,
                levels[(named, True)],
            )
        return compositions(
            [
                one
                for division in order
                if division not in held
                for one in composed(division, built, nested)
            ],
            parsed,
            read,
            defined,
            limits,
            assigned,
            dispatching,
            declarations,
            substitution,
            composing,
        )


@contextmanager
def assembling(chains: Mapping[str, Sequence[str]]) -> Iterator[None]:
    """One assembly, a source fault it meets reported as the input it is.

    A heading beyond the sixth level is a hierarchy the bundle cannot
    emit, a dispatched link the bundle places no sub-section for is a
    handoff it cannot state, and a directive whose composition has no
    section, parent or level to take, or a name its scope already
    holds, is a placement it cannot make, and a composition reaching a
    section that holds a directive on its own chain is one that would
    not end. Each is a property of the sources the run was asked to
    bundle rather than a fault in the tool, so each is reported with
    the code the contract declares for it, and with the chain that
    reached the document the fault was found in,
    whichever member of a merged group that is. A composition fault
    names the directive, where it is written, and the chain extended by
    it; a cycle names each earlier directive on its chain as related. A
    contribution crossing the output budget is the crossing it is.
    """
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
            chain=chains.get(beyond.path, ()),
        ) from beyond
    except Parentless as parentless:
        raise input_failure(
            f"the directive {parentless.destination!r} in {parentless.path!r} "
            f"names a section no heading stands above, so its contribution "
            f"has no parent to name",
            code=UNSUPPORTED_CONSTRUCT,
            remedy="name a section that stands beneath a heading of its document, "
            "or give the link a label that requests no placement",
            reference=parentless.destination,
            source=location(parentless.path, parentless.line),
            chain=(*chains.get(parentless.path, ()), parentless.destination),
        ) from parentless
    except Overflowing as beyond:
        raise input_failure(
            f"the directive {beyond.destination!r} in {beyond.path!r} composes "
            f"the heading {beyond.heading!r} at level {beyond.level}, which is "
            f"beyond H{MAX_LEVEL}",
            code=HEADING_DEPTH_OVERFLOW,
            remedy="write the directive in a shallower section, or name a "
            "shallower section of its target",
            reference=beyond.destination,
            source=location(beyond.path, beyond.line),
            chain=(*chains.get(beyond.path, ()), beyond.destination),
        ) from beyond
    except Cycling as cycling:
        first, closing = cycling.chain[0], cycling.chain[-1]
        sections = tuple(identity(each.target) for each in cycling.chain)
        raise Failure(
            INPUT_FAILURE,
            Diagnostic(
                ERROR,
                f"the directive {closing.written!r} in {closing.at[0]!r} composes "
                f"{sections[-1]!r}, which holds a directive on the chain of "
                f"compositions that placed it, so the composition would not end",
                code=UNSUPPORTED_CONSTRUCT,
                reference=closing.written,
                source=location(closing.at[0], closing.line),
                chain=(*chains.get(first.at[0], ()), *sections),
                remedy="remove a directive from the chain, or give one a label "
                "that requests no placement",
                location=Location(closing.at[0], closing.line or 1, 1),
                related=tuple(
                    RelatedLocation(
                        each.at[0],
                        each.line or 1,
                        1,
                        f"composes {identity(each.target)!r}",
                    )
                    for each in cycling.chain[:-1]
                )
                or None,
            ),
        ) from cycling
    except Crossed as crossed:
        raise crossing(crossed) from crossed
    except Colliding as colliding:
        raise input_failure(
            f"the directive {colliding.destination!r} in {colliding.path!r} "
            f"places the section {colliding.title!r} beneath its scope, whose "
            f"authored heading {colliding.title!r} at {colliding.authored} names it "
            f"already",
            code=HEADING_COLLISION,
            remedy="retitle the authored heading, or write the directive in "
            "another section",
            reference=colliding.destination,
            source=location(colliding.path, colliding.line),
            chain=(*chains.get(colliding.path, ()), colliding.destination),
        ) from colliding
    except Unplaced as unplaced:
        kind = "directive" if unplaced.composing else "dispatch"
        placed = "destination section" if unplaced.composing else "dispatch sub-section"
        raise input_failure(
            f"the {kind} {unplaced.opening!r} in {unplaced.path!r} names "
            f"{unplaced.destination!r}, and the heading that carries it is no "
            f"section a {placed} can stand beneath",
            code=UNSUPPORTED_CONSTRUCT,
            remedy=f"write the {kind} in the body beneath the heading, where a "
            f"{placed} has a section to follow",
            reference=unplaced.destination,
            source=location(unplaced.path, unplaced.line),
            chain=chains.get(unplaced.path, ()),
        ) from unplaced


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
    entries: Collection[Reference],
    found: Sequence[Reference],
    limits: Limits,
    bundle_file: Callable[[Target], str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> tuple[str, list[Diagnostic]]:
    """The complete bundle candidate, and the warnings its headings raise.

    The candidate holds the groups each included source takes, and it
    opens on the first group's first part. A source only composition
    directives reach takes none: its content stands in their
    contributions. A diagnostic names the route the run followed to a
    source, whichever kind of reference reached it. The warnings name
    the generated headings that coincide, which accompany the bundle
    rather than refuse it.

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
    chains = reaching(contributing(found))
    selected, placers = placement(
        read, parsed, found, entries, declarations, substitution
    )
    joins = joined(read, parsed, selected, entries)
    try:
        built, contributed = assembled(
            read,
            parsed,
            defined,
            selected,
            entries,
            None,
            joins,
            placers,
            chains,
            limits,
            None,
            declarations,
            substitution,
        )
        headed, placed = subsections(
            built,
            parsed,
            read,
            bundle_file,
            declarations,
            substitution,
        )
        collisions(headed, read)
    except Refused as refusal:
        raise Failure(INPUT_FAILURE, refusal.diagnostic) from refusal
    assigned = fragments([heading for one in headed for heading in one.headings])
    targets = destination_map(headed, assigned)
    dispatching = anchors(placed, assigned)
    composing = contributions(contributed, headed, assigned)
    built, _ = assembled(
        read,
        parsed,
        defined,
        selected,
        entries,
        targets,
        joins,
        placers,
        chains,
        limits,
        dispatching,
        declarations,
        substitution,
        composing,
    )
    groups, _ = subsections(
        built,
        parsed,
        read,
        bundle_file,
        declarations,
        substitution,
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
            declarations,
            substitution,
            composing,
        )
    except Unsafe as boundary:
        reached = chains.get(boundary.path or "", ())
        raise unsafe(boundary, reached) from boundary
    return bundled, coincident(
        groups, selected, joins, read, parsed, declarations, substitution
    )


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


def substituted(mapping: Substitution) -> list[Diagnostic]:
    """One warning for each mapping key a reference named.

    A key names one substitution, so the references it served state one
    warning at the first of them. The warning names that link as
    `location` where the reference stands in a source, the destination
    the author wrote as `source`, and the substitute's identity as
    `resolved`; its message states the identity the reference would have
    resolved to, which is what tells two keys naming one stand-in apart.
    """
    return [
        Diagnostic(
            WARNING,
            f"the reference {one.source!r} is redirected to the substitute "
            f"{one.resolved!r}, where it would have resolved to {one.would!r}",
            code=MOCK_SUBSTITUTED,
            source=one.source,
            resolved=one.resolved,
            location=None if one.origin is None else located(one.origin),
        )
        for one in mapping.redirects.targets()
    ]


def unused(mapping: Substitution) -> list[Diagnostic]:
    """One warning for each mapping key no reference named.

    A key that matched nothing mocks nothing, so whatever the run asserts
    of its bundle holds of material the caller did not mean to test. The
    key states a fact about the invocation rather than about any source,
    so the warning carries the key's authored spelling and no location.

    A folder key answers many references and is named once, at the first
    of them, so a key reaching no compiled reference warns once however
    many references its folder holds. A folder holding only documents
    its references classify as text is such a key: the folder was never
    consulted, and the warning is the fact that states it.
    """
    return [
        Diagnostic(
            WARNING,
            f"the mapping key {spelling!r} names no reference the run resolved, "
            f"so it substitutes nothing",
            code=MOCK_UNUSED,
            source=spelling,
            remedy="name an identity a source of the run links, or drop the pairing",
        )
        for spelling in mapping.unserved()
    ]


def located(origin: str) -> Location:
    """One diagnostic location from the source position a reference carries.

    A position is written as its document and the line it stands on, and
    a reference reached by a link is always on one; the document alone
    is the whole of the position where no line is known.
    """
    document, marked, line = origin.rpartition(":")
    if not marked or not DECIMAL.match(line):
        return Location(origin, 1, 1)
    return Location(document, int(line), 1)


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
    """One composed bundle, the file name it is published under and its warnings.

    The selection names what the bundle was compiled from, so a
    diagnostic about the bundle can name its source.
    """

    text: str
    name: str
    warnings: Sequence[Diagnostic]
    selection: str


def publication(
    bundles: Sequence[Bundle],
    folder: Path,
    limits: Limits,
    reporter: Reporter,
    check: bool,
    retained: bool = False,
    notices: Sequence[Diagnostic] = (),
) -> None:
    """Validate every bundle a run publishes, then publish the set whole or not at all.

    Each bundle is held to the output budget, every name is held to one
    bundle, the output folder is made where absent, the path standing at
    the run folder's own to being a folder or a link, and the run folder's
    name and each bundle's are held to the length its filesystem allows,
    before any is written, so a set publication would refuse ends the run with its
    diagnostic and nothing written, whether or not the run only
    validates. Every bundle's warnings follow, in turn, then the
    warnings that are facts about the run rather than about one of its
    bundles, and then the set is published into the run's folder, unless
    the run only validates, which writes nothing. A run asked to retain
    the earlier set stands an empty one at its folder where nothing
    stands there, once every check has passed, and is refused its removal
    once the new set stands.

    A run's own warnings follow the bundle checks for the same reason
    they hold under `-c`: what a run states of itself is stated by a run
    that would otherwise have published, so a substituted check reports
    its substitutions exactly as a substituted publication does.
    """
    for one in bundles:
        try:
            limits.hold(OUTPUT_BYTES, len(one.text.encode(ENCODING)))
        except Crossed as crossed:
            raise crossing(crossed) from crossed
    named: dict[str, Bundle] = {}
    for one in bundles:
        earlier = named.setdefault(one.name, one)
        if earlier is not one:
            raise colliding(earlier, one)
    if not folder.parent.is_dir():
        try:
            folder.parent.mkdir(parents=True)
        except OSError as error:
            raise Failure(
                PUBLICATION_FAILURE,
                Diagnostic(
                    ERROR,
                    f"the output folder {str(folder.parent)!r} cannot be made, so "
                    f"the run's bundles cannot be written under it",
                    code=PUBLICATION_FAILED,
                    remedy="name a folder the run can create, or one already there",
                ),
            ) from error
    longest = os.pathconf(folder.parent, "PC_NAME_MAX")
    for one, name in [(bundles[0], folder.name), *((one, one.name) for one in bundles)]:
        if len(os.fsencode(name)) > longest:
            raise overlong(one, name, longest)
    held = occupied(folder)
    if held is not None:
        raise occupied_failure(folder, held)
    for one in bundles:
        for warning in one.warnings:
            reporter.emit(warning)
    for notice in notices:
        reporter.emit(notice)
    if not check:
        publish_folder(bundles, folder, reporter, retained)


def occupied(folder: Path) -> str | None:
    """What stands at the run folder's path, where a run folder cannot be placed.

    A run folder is a folder or the link a run once placed there, so a
    symbolic link is replaced as the link it is and a folder is the
    earlier set. Anything else — a regular file, a device, a socket or a
    named pipe under the run's own `.bundles` name — is material the run
    never wrote and cannot replace without destroying bytes it never
    read, so it is refused rather than renamed aside.
    """
    if not (folder.exists() or folder.is_symlink()):
        return None
    if folder.is_symlink() or folder.is_dir():
        return None
    return "a file" if folder.is_file() else "neither a folder nor a link"


def occupied_failure(folder: Path, held: str) -> Failure:
    """One path standing where the run's folder belongs, as a refusal."""
    return Failure(
        PUBLICATION_FAILURE,
        Diagnostic(
            ERROR,
            f"the output path {str(folder)!r} holds {held}, which is neither the "
            f"run folder a run writes nor a link to one, so the bundles cannot "
            f"be published without removing it",
            code=PUBLICATION_FAILED,
            remedy="remove or rename what stands there, or name another output folder",
        ),
    )


def overlong(one: Bundle, name: str, longest: int) -> Failure:
    """A name the run derives for one selection that its filesystem refuses."""
    return Failure(
        PUBLICATION_FAILURE,
        Diagnostic(
            ERROR,
            f"the run derives the name {name!r} for {one.selection!r}, "
            f"{len(os.fsencode(name))} bytes, longer than the {longest} the "
            f"output folder's filesystem allows",
            code=PUBLICATION_FAILED,
            remedy="shorten the source's path so its derived name fits",
        ),
    )


def colliding(earlier: Bundle, later: Bundle) -> Failure:
    """Two bundles of one run whose selections derive one file name."""
    return Failure(
        PUBLICATION_FAILURE,
        Diagnostic(
            ERROR,
            f"the bundles of {earlier.selection!r} and {later.selection!r} both "
            f"derive the name {later.name!r}, so one would overwrite the other",
            code=PUBLICATION_FAILED,
            remedy="rename one of the two sources so their derived names differ",
        ),
    )


def sibling(folder: Path, role: str) -> Path:
    """A hidden path beside the run's folder that nothing else names.

    Its length is fixed, whatever the run folder's name, so any run
    folder the filesystem accepts can be staged beside.
    """
    return folder.with_name(f".pf.{role}.{uuid.uuid4().hex}")


def publish_folder(
    bundles: Sequence[Bundle], folder: Path, reporter: Reporter, retained: bool
) -> None:
    """Write a run's set of bundles as one folder, swapped in whole.

    Every bundle is written into a fresh folder beside the run's
    folder, which is then renamed onto it, so a reader sees the whole
    set the run produced or the whole set that was there before it,
    never a mixture. Whatever already stands at the run folder's path
    is renamed aside first and removed once the new folder is in place,
    so for a moment nothing stands at that path. The path is never
    followed: a symbolic link standing there is renamed and removed as
    the link it is, and whatever it names is left as it was.

    A failure before the new folder is in place removes it and leaves
    everything else as it was, the earlier set restored where it was
    moved aside; one that cannot be restored is reported where it lies.
    An earlier set that cannot be removed once the new folder stands
    leaves the run published, and is reported where it lies. Nothing
    else in the output folder is touched.

    The run's folder is the entry's derived name with the `.bundles`
    suffix, so the folder a run replaces is only ever one a run names,
    never an author's folder named like the entry.
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
    if retained and not (folder.exists() or folder.is_symlink()):
        folder.mkdir()
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
            try:
                os.rename(aside, folder)
            except OSError as stranded:
                raise unrestored(folder, aside, stranded) from refused
        raise refusal(folder, refused) from refused
    if aside is None:
        return
    try:
        if retained:
            raise PermissionError(errno.EACCES, "the run was asked to refuse it")
        if aside.is_dir() and not aside.is_symlink():
            shutil.rmtree(aside)
        else:
            aside.unlink()
    except OSError as refused:
        reporter.emit(
            Diagnostic(
                WARNING,
                f"the run's bundles are published, and the earlier set moved "
                f"aside to {str(aside)!r} could not be removed: {refused}",
                code=EARLIER_SET_RETAINED,
                remedy=f"remove {str(aside)!r}",
            )
        )


def refusal(destination: Path, refused: OSError) -> Failure:
    """One output path that refused the run's bundles, as a publication failure."""
    return Failure(
        PUBLICATION_FAILURE,
        Diagnostic(
            ERROR,
            f"the output path {str(destination)!r} refused the bundle: {refused}",
            code=PUBLICATION_FAILED,
            remedy="name a folder the run can write",
        ),
    )


def unrestored(folder: Path, aside: Path, refused: OSError) -> Failure:
    """A refused swap whose earlier set could not be put back where it stood."""
    return Failure(
        PUBLICATION_FAILURE,
        Diagnostic(
            ERROR,
            f"the output path {str(folder)!r} refused the bundle, and the earlier "
            f"set moved aside to {str(aside)!r} could not be restored: {refused}",
            code=PUBLICATION_FAILED,
            remedy=f"rename {str(aside)!r} to {str(folder)!r}",
        ),
    )


def selections(requested: Sequence[Reference]) -> tuple[Target, ...]:
    """Each distinct selection the command line names, in first-named order."""
    return tuple(dict.fromkeys((one.path, one.fragment) for one in requested))


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


def derived_name(requested: Sequence[Reference]) -> str:
    """The entry bundle's file name, joined from each distinct selection's name."""
    return f"{run_name(selections(requested))}{BUNDLE_SUFFIX}"


@dataclass(frozen=True)
class Compiled:
    """One bundle of a run, compiled from its own entry under its own budgets.

    The dispatches are each distinct target the bundle dispatches, at the
    first link naming it. The warnings are held in two runs so a depth
    warning, which only the run's entry raises and only once every
    bundle is compiled, takes its place between them. The unselected
    presets are those `unselected` returns for the documents the bundle
    carries, which the run weighs against its other bundles'.
    """

    text: str
    name: str
    hops: Sequence[Hop]
    leading: Sequence[Diagnostic]
    trailing: Sequence[Diagnostic]
    captured: Mapping[str, Capture]
    unselected: Mapping[str, tuple[str, ...]]


def compiled(
    root: Path,
    requested: Sequence[Reference],
    options: argparse.Namespace,
    folder: Path,
    substitution: Substitution = UNSUBSTITUTED,
) -> Compiled:
    """One bundle compiled as its own entry, every budget counted from it alone.

    Each bundle is read by one agent, so each starts from a fresh count
    of what it opens, reaches and publishes, and its expansion depth is
    counted from its own entry.

    The mapping is the command line's and not the bundle's: a dispatched
    target's own bundle is compiled under every rule an entry's is, and
    the mapping is one of them, so a link inside a dispatched document
    resolves the substitute the caller named.
    """
    limits = budgets(options)
    declarations = Declarations(lambda found: probe(root, found, limits))
    declared_entries(requested, declarations)
    try:
        read, parsed, defined, captured, found, hops = traverse(
            root, requested, limits, declarations, substitution
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
        read,
        parsed,
        defined,
        requested,
        found,
        limits,
        bundle_file,
        declarations,
        substitution,
    )
    trailing: list[Diagnostic] = []
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
        derived_name(requested),
        hops,
        [*coinciding, *(selfward(hop) for hop in hops if hop.own)],
        trailing,
        captured,
        unselected(read, parsed, contributing(found), requested),
    )


def unused_presets(bundles: Iterable[Compiled]) -> list[Diagnostic]:
    """One warning for each preset no reference of the run selected.

    A preset one bundle leaves unselected and another selects governed
    content the run published, so a preset is unused only where every
    bundle carrying its document left it unselected. The warning states
    a fact about the document rather than about one reference, so it
    carries the document as `source` and no location, in path order and
    then in the order the document declares its presets.
    """
    left: dict[str, tuple[str, ...]] = {}
    for one in bundles:
        for path, names in one.unselected.items():
            earlier = left.get(path, names)
            left[path] = tuple(name for name in earlier if name in names)
    return [
        Diagnostic(
            WARNING,
            f"the preset {name!r} of {path!r} is selected by no reference the run "
            f"compiled, so it governs nothing",
            code=PRESET_UNUSED,
            source=path,
            remedy=(
                "name the preset as a word in the title of a section reaching the "
                "document, or drop the preset"
            ),
        )
        for path in sorted(left)
        for name in left[path]
    ]


def dispatched_set(
    root: Path,
    entry: Compiled,
    single: Collection[str],
    options: argparse.Namespace,
    folder: Path,
    substitution: Substitution = UNSUBSTITUTED,
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
        one = compiled(root, [target], options, folder, substitution)
        built[hop.name] = one
        pending.extend(one.hops)
    return built


def target_name(target: Target) -> str:
    """One selection as the document and the section it names."""
    path, fragment = target
    return path if fragment is None else f"{path}#{fragment}"


def captured_once(captures: Iterator[Mapping[str, Capture]]) -> dict[str, Capture]:
    """Every source the run's bundles read, each as one read of it.

    Each bundle captures the sources it reads, so a source two bundles
    read is captured twice. Two captures holding different bytes or
    identities record a source written between the two reads, and the
    run's bundles would carry two versions of it, so the run is refused
    as one whose source changed.
    """
    found: dict[str, Capture] = {}
    for one in captures:
        for path, held in one.items():
            earlier = found.setdefault(path, held)
            if (earlier.digest, earlier.file_identity) != (
                held.digest,
                held.file_identity,
            ):
                raise changed(
                    path, "changed between two of the run's reads", held.chain
                )
    return found


def execute(arguments: Sequence[str], stdout: IO[str], reporter: Reporter) -> int:
    """One invocation, from its command line to the status its outcome returns."""
    if not arguments:
        publish(GUIDE, stdout)
        return SUCCESS
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

    fault = conformance_fault(os.environ)
    if not options.references:
        raise usage_failure("at least one entry reference is required")
    if options.output == STANDARD_OUTPUT:
        raise usage_failure(
            "-o - names standard output, which carries no bundle; -o names the "
            "folder the run's bundles are written under"
        )
    mapping = substitution(options)
    requested = [entry(reference, mapping) for reference in options.references]
    for one in requested:
        if not one.path:
            raise usage_failure(
                f"the entry reference {one.original!r} names a fragment alone, and "
                f"a fragment alone names no document; name the section as "
                f"document#fragment",
                reference=one.original,
            )

    root = Path.cwd().resolve()
    requested = entered(requested)

    selected = selections(requested)
    folder = Path(options.output).resolve() / f"{run_name(selected)}{RUN_FOLDER_SUFFIX}"
    first = compiled(root, requested, options, folder, mapping)
    single = {requested[0].chain[0]} if len(selected) == 1 else set()
    built = dispatched_set(root, first, single, options, folder, mapping)

    def onward(target: Reference) -> Sequence[Hop]:
        name = identity(target)
        return first.hops if name in single else built[name].hops

    try:
        cycle(first.hops, single, onward)
    except Refused as refused:
        raise Failure(INPUT_FAILURE, refused.diagnostic) from refused
    captured = captured_once(one.captured for one in (first, *built.values()))
    if fault == SOURCE_CHANGED_FAULT:
        rewrite_sources(root, captured)
    recheck(root, captured)
    if fault == INTERNAL_FAULT:
        raise Faulted("the run was asked to fail in itself")
    deep = analysed(first.hops, single, onward)
    bundles = [
        Bundle(
            first.text,
            first.name,
            [*first.leading, *deep, *first.trailing],
            " ".join(target_name(one) for one in selected),
        ),
        *(
            Bundle(one.text, one.name, [*one.leading, *one.trailing], name)
            for name, one in built.items()
        ),
    ]
    publication(
        bundles,
        folder,
        budgets(options),
        reporter,
        options.check,
        fault == CLEANUP_FAULT,
        [
            *substituted(mapping),
            *unused(mapping),
            *unused_presets((first, *built.values())),
        ],
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
