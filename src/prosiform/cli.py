"""Coordinate an invocation from argument parsing through bundle publication.

`traverse` discovers the selected sources, `compose` constructs a
validated bundle, and `publication` publishes the run. Their supporting
units own reference, source, layout and diagnostic rules.
"""

import argparse
import errno
import json
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
from urllib.parse import quote

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
    carries_title,
    document_title,
    file_heading,
    group,
    opened,
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
    DRIVE,
    SEPARATOR,
    UNSUBSTITUTED,
    WORKING_FOLDER,
    Briefs,
    BundleFolder,
    BundleSelection,
    Declarations,
    Levels,
    Malformed,
    OutsideRoot,
    Probed,
    Reference,
    Substitution,
    Unmapped,
    Unresolvable,
    alternatives_of,
    arrowed,
    briefing,
    bundle_selection,
    bundled_pick,
    components,
    conflicting,
    contradicting,
    deferred,
    deferring_dispatch,
    directive,
    gapped,
    identity,
    inside,
    level_map,
    level_of,
    matching_presets,
    model_of,
    named,
    operators,
    resolve,
    withholding,
    withholding_target,
)
from prosiform.composition import (
    Colliding,
    Composed,
    Composing,
    Cycling,
    Held,
    Overflowing,
    Parentless,
    Within,
    compositions,
    contributions,
    owned,
)
from prosiform.diagnostics import (
    ERROR,
    FORMATS,
    INDENT,
    TEXT,
    WARNING,
    Diagnostic,
    Location,
    RelatedLocation,
    Reporter,
)
from prosiform.dispatch import CODES as DISPATCH_CODES
from prosiform.dispatch import (
    DISPATCH_CYCLE,
    HEADING_COLLISION,
    Anchors,
    Hop,
    Refused,
    analysed,
    anchors,
    collisions,
    cycle,
    region_of,
    selfward,
    subsections,
    written_in,
)
from prosiform.entry import NotOneLink, published
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
from prosiform.marks import (
    DEFERRAL_MARK,
    DISPATCH_MARK,
    INLINE_MARK,
    PARALLEL_MARK,
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
from prosiform.preamble import grouped as preamble_group
from prosiform.preamble import selected as preamble_selection
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
    marked_tag,
    parse,
    refusals,
)
from prosiform.provenance import Contributing, Range
from prosiform.pruning import Removed, prune
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
    Use,
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
    uses,
    within,
)
from prosiform.source import (
    CODES as SOURCE_CODES,
)
from prosiform.tags import PICK, picks
from prosiform.tags import read as read_tags

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

ALTERNATIVE_UNRESOLVED = "E_ALTERNATIVE_UNRESOLVED"
INVALID_ENCODING = "E_INVALID_ENCODING"
GROUP_CONFLICT = "E_GROUP_CONFLICT"
INVALID_USAGE = "E_INVALID_USAGE"
LEVEL_ON_ENTRY = "E_LEVEL_ON_ENTRY"
LEVEL_UNMAPPED = "E_LEVEL_UNMAPPED"
PUBLICATION_FAILED = "E_PUBLICATION_FAILED"
SOURCE_CHANGED = "E_SOURCE_CHANGED"
SOURCE_ACCESS = "E_SOURCE_ACCESS"
SOURCE_OUTSIDE_ROOT = "E_SOURCE_OUTSIDE_ROOT"
SOURCE_SYMLINK = "E_SOURCE_SYMLINK"
STUB_OFF_ENTRY = "E_STUB_OFF_ENTRY"
TARGET_NOT_FOUND = "E_TARGET_NOT_FOUND"
UNEXPECTED_INTERNAL_ERROR = "E_UNEXPECTED_INTERNAL_ERROR"
UNSUPPORTED_ENTRY_SUFFIX = "E_UNSUPPORTED_ENTRY_SUFFIX"

RESOURCE_PORTABILITY = "W_RESOURCE_PORTABILITY"
COINCIDENT_HEADING = "W_COINCIDENT_HEADING"
EMPTY_SECTION = "W_EMPTY_SECTION"
EARLIER_SET_RETAINED = "W_EARLIER_SET_RETAINED"
SUBST_USED = "W_SUBST_USED"
SUBST_UNUSED = "W_SUBST_UNUSED"
PRESET_UNUSED = "W_PRESET_UNUSED"
COMPOSE_SELF = "W_COMPOSE_SELF"

OPERATOR_NAMES = {
    DEFERRAL_MARK: "the deferral mark",
    DISPATCH_MARK: "the dispatch mark",
    PARALLEL_MARK: "the parallel dispatch mark",
    INLINE_MARK: "the composition mark",
}

CODES = tuple(
    sorted(
        {
            ALTERNATIVE_UNRESOLVED,
            INVALID_ENCODING,
            GROUP_CONFLICT,
            INVALID_USAGE,
            LEVEL_ON_ENTRY,
            LEVEL_UNMAPPED,
            PUBLICATION_FAILED,
            SOURCE_CHANGED,
            SOURCE_ACCESS,
            SOURCE_OUTSIDE_ROOT,
            SOURCE_SYMLINK,
            STUB_OFF_ENTRY,
            TARGET_NOT_FOUND,
            UNEXPECTED_INTERNAL_ERROR,
            UNSUPPORTED_ENTRY_SUFFIX,
            RESOURCE_PORTABILITY,
            COINCIDENT_HEADING,
            EMPTY_SECTION,
            EARLIER_SET_RETAINED,
            SUBST_USED,
            SUBST_UNUSED,
            PRESET_UNUSED,
            COMPOSE_SELF,
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
  0  successful bundling, validation, or informational response
  1  input, dependency, policy, safety, or resource-limit failure
  2  invalid usage or option combination
  3  output publication or delivery failure, a broken pipe among them
  4  unexpected internal error
"""

GUIDE = """\
Following a bundle:

  Read the bundle you were given and follow every instruction in it as
  written, taking each link by the symbol grammar below. A sub-agent
  handed a bundle follows it the same way, handing on each ⇉ and ⫽ link
  it meets.

Symbol grammar:

  ↳  names a section to inline: bundle its destination with pf, read that
     bundle whole, keep it in context, and follow it where the link stands.
     Do not open its source yourself: read the bundle pf writes.
  ⇉  names a bundle to hand on: give a sub-agent the path of its file,
     which it reads there, with the inputs the dispatching step states as
     given, and continue with its answer. Do not open the bundle
     yourself: hand on its link. Do not check or redo its work: take
     its answer as given. Hand over the path and those inputs alone:
     add no instruction, framing or reply form.
     Where on <model> follows a ⇉ link, or a diagram's %% <node> on
     <model> comment stands beneath its node's link, start its sub-agent
     on that model; where neither does, start it as your harness does
     by default.
     Where a ⇉ link points at a sub-section rather than at a bundle
     file, the text above its ⇉ line there, and the sections beneath
     that line, are the bundle's brief: do what it asks of you before
     you hand the bundle on. What it states the bundle takes is what
     you hand over; what it states the bundle leaves or answers is the
     sub-agent's work
  ⫽  marks a dispatch set: its section holds one set of bundles, listed as
     ⇉ lines.
     Give each bundle's file path to its own sub-agent at once, with the
     inputs the dispatching step states as given, one per value where
     that step applies to several.
     A failure cancels nothing; all failures return together.
  ?  among a link's title tags leaves the pick to you, made with --pick.
     On a ⇉ link it points at a sub-section listing one ⇉ line for each
     alternative beside its choice line: hand on the one bundle whose
     choice line fits your work

Usage:

  pf bundles a Markdown document that declares prosiform into one or
  more bundles.

  pf -o <folder> '<link>' [--pick <alternative>]
  pf -o <folder> <document>[#<section>]

  -o <folder>            folder the run's bundles are written into, made if
                         absent; default: the working directory
  <link>                 a link as a bundle publishes it: a Markdown link,
                         or a Mermaid click or class diagram link line
  <document>             one document, or document#section, named from the
                         working directory
  --pick <alternative>   the alternative a link whose title carries ?
                         leaves to you

Bundling a link:

  Run pf on a link in a bundle as written, quoted as one argument, from
  the folder that bundle is in, never on a ⇉ or ⫽ link. When its title
  carries ?, add --pick naming the alternative that fits your task if
  you know it, or when pf lists the alternatives:

    pf -o out '[¬ Review](modes/review.md#review "checks, final draft")'
    pf -o out 'click Intake "activities/intake.md" "?"' --pick Epic

  Title tags layer the target's presets above default.

Exit status:

  0  the bundles were written
  1  a failure stopped the run: report its diagnostics and go no further
  2  invalid usage or option combination
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
    """An input refusal carrying the diagnostic evidence supplied by its caller.

    An empty chain or remedy is represented as None;
    `diagnostics.Diagnostic.fields` owns omission from rendered data.
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
    """A crossed budget as an input failure with the resource-limit code.

    `limits.Crossed` supplies the message and remedy.
    """
    return input_failure(str(crossed), code=RESOURCE_LIMIT, remedy=crossed.remedy)


def unindexable(crossed: Crossed, path: str, chain: Sequence[str]) -> Failure:
    """A budget crossing reported against the source being indexed.

    The source path occupies both reference and source fields; `chain`
    locates the route to it. `limits.Crossed` supplies the remedy.
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
    """A parser lookup refusal reported against its source and route.

    `profile.Suppressed` supplies the reference, position and remedy.
    An absent reference uses the source path; `source.Source.line`
    converts the parser position to the file coordinate.
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
    """One budget and override from a NAME=VALUE entry.

    The first equals sign separates a declared budget name from the
    value `override` validates. A missing separator, unknown name or
    figure below the budget's `least` value is invalid argument syntax.
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
    """An argument action collecting budget entries in the parser namespace."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,
        option_string: str | None = None,
    ) -> None:
        """Record one parsed budget entry, refusing a repeated budget name."""
        budget, limit = values
        entries = dict(getattr(namespace, self.dest))
        if budget in entries:
            raise argparse.ArgumentError(
                self, f"the {budget.name} budget is named twice; name it once"
            )
        entries[budget] = limit
        setattr(namespace, self.dest, entries)


def budgets(options: argparse.Namespace) -> Limits:
    """The command-line budget settings, completed by `limits.in_force`."""
    return in_force(options.budgets)


def substs(conversion: Conversion) -> None:
    """Validate the reference syntax of every substitution side.

    `closure.resolve` owns reference parsing. A malformed or external
    side, or a path ending in a separator, is invalid conversion
    metadata located at its entry. The trailing separator is checked
    before normalization can discard it.
    """
    for preset in conversion.presets:
        for at, pair in enumerate(preset.substs):
            for side in (pair.original, pair.substitute):
                try:
                    refusal = (
                        "carries a scheme or an authority, so it names no local "
                        "document"
                        if resolve(side).external
                        else "ends in a path separator, so it names a folder, and a "
                        "pair names one document or one section"
                        if components(side).path.endswith(SEPARATOR)
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
    """The document and section one `subst` key names, read from its document.

    A key resolves from the declaring document's directory, as every
    reference the document writes does, so one declaration reads the
    same wherever the run starts.
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
    mapping a key to a substitute of its own identity, or writing a key
    naming a section alone states a rule the run cannot apply as written,
    so each is invalid usage at the entry. A key names the document whose
    references it redirects, which a section alone does not. A
    substitute naming no Markdown document is refused the same way,
    because the reference it redirects could only be published as text.
    Identities are read as `subst_identity` and `subst_reference` read
    them, the reference that opened the declaring document being `found`.
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
            substitute = subst_reference(pair, found.path)
            if not is_markdown(substitute.path):
                raise preset_refusal(
                    f"{entry} maps {pair.original!r} to {pair.substitute!r}, which "
                    f"names no Markdown document, so the reference it redirects "
                    f"could only be published as text",
                    "name a Markdown document or section as the substitute",
                    found,
                    pair.location,
                )
            if key == (substitute.path, substitute.fragment):
                raise preset_refusal(
                    f"{entry} maps {pair.original!r} to {pair.substitute!r}, which "
                    f"name one identity, so the substitute stands in for itself",
                    "name a substitute other than the reference it replaces",
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
    conversion: Conversion, tags: frozenset[str], reference: Reference, document: str
) -> None:
    """Hold the selected presets to agreeing about every shared setting.

    For the presets `closure.matching_presets` selects, different group
    pairs or substitutes for one key are invalid usage naming both
    declarations. `subst_identity` and `subst_reference` own identity
    resolution; `document` names the declaring document.
    """
    stated: Membership | None = None
    substitutes: dict[tuple[str, str | None], tuple[str, Subst]] = {}
    selected = f"selected by tags {sorted(tags)!r}"
    for preset in matching_presets(conversion, tags):
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
                "state one group pair in the presets one tag selection selects",
                reference,
                stated.group_location,
                (
                    one.group_location,
                    f"prosiform.{one.preset}.{GROUP} is {{{one.group}: {one.depth}}}",
                ),
            )
        for pair in preset.substs:
            key = subst_identity(pair.original, document)
            named_first, first_pair = substitutes.setdefault(key, (preset.name, pair))
            if identity(subst_reference(first_pair, document)) != identity(
                subst_reference(pair, document)
            ):
                raise preset_refusal(
                    f"prosiform.{named_first}.{SUBST} and "
                    f"prosiform.{preset.name}.{SUBST}, both {selected}, map "
                    f"{pair.original!r} to {first_pair.substitute!r} and "
                    f"{pair.substitute!r}",
                    "map the reference to one substitute in the selected presets",
                    reference,
                    first_pair.location,
                    (
                        pair.location,
                        f"prosiform.{preset.name}.{SUBST} maps {pair.original!r} "
                        f"to {pair.substitute!r}",
                    ),
                )


@dataclass(frozen=True)
class Governed:
    """One substitution pair in force.

    `preset` names its declaration, `pair` holds the authored entry and
    `substitute` its resolved reference. `routing` distinguishes an
    authored route from a trial stand-in.
    """

    preset: str
    pair: Subst
    substitute: Reference
    routing: bool = False


def subst_reference(pair: Subst, document: str) -> Reference:
    """One `subst` substitute as the reference the run reads.

    It resolves as a link written in its key's document resolves: from
    that document's directory, a section alone naming a section of that
    document, and opened through the walk from that directory. The key
    resolves from the declaring document, `document`, as
    `subst_identity` states, and its walk is the one the declaring
    document's link to it takes.
    """
    key = resolve(pair.original, posixpath.dirname(document))
    walk = posixpath.join(posixpath.dirname(document), key.walk or key.path)
    found = resolve(pair.substitute, posixpath.dirname(key.path))
    if not components(pair.substitute).path:
        return replace(found, path=key.path, walk=walk)
    return replace(
        found, walk=posixpath.join(posixpath.dirname(walk), found.walk or found.path)
    )


def picked(
    conversion: Conversion, references: Iterable[Reference]
) -> tuple[Preset, ...]:
    """The selected alternatives in declaration order.

    `closure.matching_presets` owns tag matching, and
    `metadata.Conversion.alternatives` identifies alternatives.
    """
    names = {
        preset.name
        for reference in references
        for preset in matching_presets(conversion, reference.tags)
    }
    return tuple(one for one in conversion.alternatives if one.name in names)


def unresolved(
    path: str,
    conversion: Conversion,
    rerun: bool = False,
    placing: Reference | None = None,
    carried: bool = False,
    varying: bool = False,
) -> Failure:
    """The diagnostic for the alternative refusal `resolved` identifies.

    `placing` locates a composing reference or dispatch; an absent value
    names the document alone. `rerun`, `carried` and `varying` choose
    the remedy for an entry pick, a carried brief or an alternative
    brief, respectively. Alternatives and their choice lines are listed
    in declaration order.
    """
    width = max(len(one.name) for one in conversion.alternatives)
    rows = "".join(
        f"\n{INDENT}{one.name.ljust(width)}  {one.choice}"
        for one in conversion.alternatives
    )
    return Failure(
        USAGE_FAILURE,
        Diagnostic(
            ERROR,
            f"{path} needs one alternative in force:{rows}",
            code=ALTERNATIVE_UNRESOLVED,
            source=path,
            remedy=(
                "rerun with --pick naming the alternative that fits your task"
                if rerun
                else "name the alternative that fits your task in the title or "
                "tooltip of each link reaching it, a link entry's among them"
                if placing is None
                else f"write the brief {placing.original!r} so it bundles with no "
                "alternative in force, since the picking dispatch carrying it "
                "leaves the pick to its agent"
                if carried
                else "declare the brief in default or an ordinary preset, so it "
                "does not vary by alternative, since the picking dispatch "
                "carrying it leaves the pick to its agent"
                if varying
                else "name the alternative that fits your task in the title of "
                "the directive or dispatch placing this copy"
            ),
            reference=None if placing is None else placing.original,
            chain=None if placing is None else placing.chain,
            location=(
                None
                if placing is None or placing.origin is None
                else located(placing.origin)
            ),
        ),
    )


def preambled(
    path: str,
    tokens: Sequence[Token],
    references: Sequence[Reference],
    paired: bool,
    entries: Collection[Reference],
) -> bool:
    """Whether a document's title and introduction stand in its folder's preamble group.

    A document in a subfolder that every including reference reaches by
    a section, and that a `group` pair joins to a merged group, carries
    them there, unless it is the parent opening the bundle on its own
    title.
    """
    return (
        all(one.fragment is not None for one in references)
        and paired
        and bool(posixpath.dirname(path))
        and not (path == parent_document(entries) and carries_title(tokens))
    )


def routed(
    path: str,
    conversion: Conversion,
    tokens: Sequence[Token],
    references: Sequence[Reference],
    entries: Collection[Reference],
    grouped: bool = True,
) -> bool:
    """Whether alternatives affect the selected content of one document.

    A group pair matters where `grouped` is true; a substitution matters
    where a selected link names its key. `selection` owns the selected
    regions and `preambled` decides whether to add the introduction.
    `linked`, `names` and `subst_identity` own link-key matching.
    """
    if grouped and any(one.membership is not None for one in conversion.alternatives):
        return True
    chosen = selection(path, tokens, references, entries)
    read_regions = tuple(regions(tokens)) if chosen is None else chosen.regions
    including = [one for one in references if not one.composes]
    introduction = preamble_selection(tokens)
    if introduction is not None and preambled(
        path,
        tokens,
        including,
        any(pair(conversion, one.tags) is not None for one in including),
        entries,
    ):
        read_regions += introduction.regions
    written = linked(path, tokens, read_regions)
    return any(
        names(written, subst_identity(pair.original, path))
        for one in conversion.alternatives
        for pair in one.substs
    )


def resolved(
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    selected: Mapping[str, Sequence[Reference]],
    entries: Collection[Reference],
    hops: Iterable[Hop],
) -> None:
    """Hold each carried group or composed copy to its required alternative count.

    Each inclusion set `included` keeps and each composing tag selection
    is checked separately. Several selected alternatives fail; none
    fails where `routed` finds an effect. `picked` supplies the count,
    `briefed` identifies carried briefs, and `unresolved` renders the
    failure. A picking dispatch takes precedence when locating its
    carried brief; an entry carrying the pick token permits the rerun
    remedy `entry` supports.
    """
    carried: dict[tuple[str, str | None, frozenset[str]], Reference] = {}
    for hop in hops:
        if picks(hop.target.tags):
            brief = briefed(hop, read[hop.target.path].conversion)
            if brief is not None:
                carried.setdefault((brief.path, brief.fragment, brief.tags), brief)
    for path, references in selected.items():
        conversion = read[path].conversion
        if not conversion.alternatives:
            continue
        including = included(references, parsed, read)
        held = [
            *([(including, True)] if including else []),
            *(
                (
                    [one for one in references if one.composes and one.tags == tags],
                    False,
                )
                for tags in dict.fromkeys(
                    one.tags for one in references if one.composes
                )
            ),
        ]
        for reaching, grouped in held:
            placing = None if grouped else reaching[0]
            count = len(picked(conversion, reaching))
            if count > 1:
                raise unresolved(path, conversion, placing=placing)
            if count == 0 and routed(
                path, conversion, parsed[path], reaching, entries, grouped
            ):
                brief = None
                if not grouped:
                    needing = [
                        one
                        for one in reaching
                        if routed(path, conversion, parsed[path], [one], entries, False)
                    ]
                    brief = next(
                        (
                            carried[key]
                            for one in needing
                            if (key := (one.path, one.fragment, one.tags)) in carried
                        ),
                        None,
                    )
                    placing = needing[0] if brief is None else brief
                raise unresolved(
                    path,
                    conversion,
                    rerun=any(one in entries and picks(one.tags) for one in reaching),
                    placing=placing,
                    carried=brief is not None,
                )


def governing(
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    selected: Mapping[str, Sequence[Reference]],
    entries: Collection[Reference],
) -> dict[str, dict[tuple[str, str | None], Governed]]:
    """The substitution pairs governing each carried document's group.

    `included` supplies the group's references. `defaults` supplies its
    base pairs and `layer` combines the selected presets above them;
    conflicts produce `disagreeing`. `agreed` checks each reference's
    selection, and the alternative cardinality rule `resolved` owns
    is checked before comparing those selections. Only documents with
    pairs in force appear in the result.
    """
    table: dict[str, dict[tuple[str, str | None], Governed]] = {}
    for path, references in selected.items():
        conversion = read[path].conversion
        including = included(references, parsed, read)
        if len(picked(conversion, including)) > 1:
            raise unresolved(path, conversion)
        for reference in references:
            if len(picked(conversion, [reference])) > 1:
                raise unresolved(
                    path,
                    conversion,
                    placing=reference if reference.composes else None,
                )
            agreed(conversion, reference.tags, reference, path)
        standing = defaults(conversion, path)
        above: dict[tuple[str, str | None], Governed] = {}
        for reference in including:
            for preset in matching_presets(conversion, reference.tags):
                clash = layer(above, preset, path)
                if clash is not None:
                    raise disagreeing(*clash, path, reference)
        in_force = {**standing, **above}
        if in_force:
            table[path] = in_force
    return table


def defaults(
    conversion: Conversion, path: str
) -> dict[tuple[str, str | None], Governed]:
    """The `subst` pairs a document's `default` puts in force wherever it bundles."""
    return {
        subst_identity(pair.original, path): Governed(
            DEFAULT, pair, subst_reference(pair, path), routing=True
        )
        for pair in conversion.default.substs
    }


def layer(
    above: dict[tuple[str, str | None], Governed],
    preset: Preset,
    path: str,
) -> tuple[Governed, Governed] | None:
    """Layer one selected preset's substitution pairs into `above`.

    A stub's pair is marked as a stand-in and other pairs as routes.
    A stand-in takes precedence over an agreeing route. A different
    substitute for an existing key is returned with the earlier pair
    and left out of the mapping. `subst_identity` and `subst_reference`
    own reference resolution.
    """
    for pair in preset.substs:
        one = Governed(
            preset.name,
            pair,
            subst_reference(pair, path),
            preset.stub is None,
        )
        key = subst_identity(pair.original, path)
        first = above.setdefault(key, one)
        if identity(first.substitute) != identity(one.substitute):
            return first, one
        if first.routing and not one.routing:
            above[key] = one
    return None


def disagreeing(
    first: Governed, later: Governed, document: str, reference: Reference
) -> Failure:
    """Two presets selected for one document mapping one key to two substitutes."""
    return preset_refusal(
        f"prosiform.{first.preset}.{SUBST} and prosiform.{later.preset}.{SUBST}, "
        f"both selected for {document!r}, map {later.pair.original!r} to "
        f"{first.pair.substitute!r} and {later.pair.substitute!r}",
        "map the reference to one substitute in the presets selected for one document",
        reference,
        first.pair.location,
        (
            later.pair.location,
            f"prosiform.{later.preset}.{SUBST} maps {later.pair.original!r} to "
            f"{later.pair.substitute!r}",
        ),
    )


def copies(
    read: Mapping[str, Source],
    selected: Mapping[str, Sequence[Reference]],
) -> dict[tuple[str, frozenset[str]], dict[tuple[str, str | None], Governed]]:
    """The substitution pairs governing each composed tag selection.

    The layering rule `governing` owns is applied separately to every
    composing reference's tags, using `defaults` and `layer`. Results
    are keyed by document and tag selection; an empty result is absent.
    `governing` checks agreement before these pairs are read.
    """
    table: dict[tuple[str, frozenset[str]], dict[tuple[str, str | None], Governed]] = {}
    for path, references in selected.items():
        conversion = read[path].conversion
        for reference in references:
            copy = (path, reference.tags)
            if not reference.composes or copy in table:
                continue
            standing = defaults(conversion, path)
            above: dict[tuple[str, str | None], Governed] = {}
            for preset in matching_presets(conversion, reference.tags):
                layer(above, preset, path)
            pairs = {**standing, **above}
            if pairs:
                table[copy] = pairs
    return table


def governed(
    mapping: Substitution,
    table: Mapping[str, Mapping[tuple[str, str | None], Governed]],
    composed: Mapping[
        tuple[str, frozenset[str]], Mapping[tuple[str, str | None], Governed]
    ],
) -> Substitution:
    """The run's mapping with the pairs each group's and each copy's links take."""
    return mapping.governed(
        {
            path: {key: one.substitute for key, one in pairs.items()}
            for path, pairs in table.items()
        },
        {
            copy: {key: one.substitute for key, one in pairs.items()}
            for copy, pairs in composed.items()
        },
    )


class Once(argparse.Action):
    """An argument action storing one option value in the parser namespace."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        """Store the option value, refusing a second supplied value."""
        if getattr(namespace, self.dest, None) is not None:
            raise usage_failure(f"{option_string} is supplied more than once")
        setattr(namespace, self.dest, values)


def parser() -> Parser:
    """The command's grammar: every option the contract declares, and no other."""
    grammar = Parser(
        prog=NAME,
        add_help=False,
        allow_abbrev=False,
        usage=f"{NAME} [OPTIONS] REF [--pick ALTERNATIVE]",
        description=(
            "Bundle the local Markdown closure of one entry reference, "
            "and of each target they dispatch, into validated bundles. Run with "
            "no arguments, pf prints the guide to following a bundle."
        ),
        epilog=f"{BUDGET_TABLE}\n{EXIT_STATUSES}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
        "entry",
        metavar="REF",
        nargs="?",
        help="a link as a bundle publishes it, or document[#fragment]; paths from cwd",
    )
    grammar.add_argument(
        "--pick",
        metavar="ALTERNATIVE",
        action=Once,
        help="the alternative for an entry whose title carries ?",
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
            if option in "od":
                value = token[at + 1 :].removeprefix("=") or next(tokens, "")
                if option == "d" and value in FORMATS:
                    selected = value
            break
    return selected


def entry(text: str, pick: str | None) -> Reference:
    """Normalize one invocation entry and apply its optional pick.

    `entry.published` reads an authored link, `tags.read` reads its
    title and `closure.resolve` owns destination normalization. A tag
    `profile.marked_tag` rejects is invalid usage. `pick` is admitted
    only beside the pick token and joins the entry's tags; the token
    is retained. An external entry is refused as outside the source
    root. `execute` owns selection of the invocation root.
    """
    try:
        link = published(text)
    except NotOneLink as refused:
        raise usage_failure(
            f"the entry {text!r} {refused}", reference=text
        ) from refused
    tags = frozenset() if link is None else link.tags
    stating = marked_tag(tags)
    if stating is not None:
        raise usage_failure(
            f"the entry {text!r} carries the title tag {stating!r}, which "
            f"states operator marks, and a title names presets alone",
            reference=text,
        )
    if pick is not None:
        if not picks(tags):
            raise usage_failure(
                f"--pick names the alternative for an entry whose title carries "
                f"{PICK!r}, and the entry {text!r} carries none",
                reference=text,
            )
        tags = tags | read_tags(pick)
    if link is not None:
        text = link.destination
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
    return replace(found, tags=tags)


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
    """One captured read: `source` content, raw byte `size` and `capture` identity."""

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
    reference = found.original
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
            f"the reference {reference!r} names no document",
            code=TARGET_NOT_FOUND,
            remedy="name a document that exists",
            reference=reference,
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
    """Capture one source and its settings within the supplied budgets.

    `profile.is_markdown` owns suffix classification, `access.read_source`
    owns bounded access, and `source.content` owns content extraction.
    The capture records the bytes and identities from that read.
    `limits.Limits.hold` enforces file and cumulative input sizes before
    decoding; `substs` and `stated_once` validate the decoded settings.
    `reading` and `delimiting` own refusal translation.
    """
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
    """Answer whether a target exists and declares, without retaining a capture.

    `access.read_head` reads up to `source.closes_head` within the file
    byte budget; `source.declaration` owns decoding. Probe bytes do not
    consume the cumulative input budget. An absent ordinary target
    returns `closure.Probed.ABSENT`; an absent redirected target is
    reported through `reading`. `delimiting` translates metadata faults.
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
    """Require Markdown entry targets to declare prosiform.

    `closure.Declarations.answer` supplies the declaration state. An
    absent or silent target fails as not found; `read_document` owns
    entry suffix refusal.
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


def refused(
    name: str, source: Source, refusal: Refusal, chain: Sequence[str]
) -> Failure:
    """A profile refusal located in its original source with the supplied route.

    `profile.Refusal` supplies the construct and related position;
    `source.Source.line` owns coordinate conversion.
    """
    message = refusal.message
    if refusal.earlier is not None:
        earlier = location(name, source.line(refusal.earlier))
        message += f"; the earlier link is at {earlier}"
    return input_failure(
        message,
        code=refusal.code,
        remedy=refusal.remedy,
        reference=refusal.reference,
        source=location(name, source.line(refusal.line)),
        chain=chain,
    )


def changed(path: str, what: str, chain: Sequence[str]) -> Failure:
    """Report a captured source that differs from the read used by the run."""
    return input_failure(
        f"the source {path!r} {what}, so the bundle would carry bytes the run "
        f"no longer reads",
        code=SOURCE_CHANGED,
        remedy="bundle again, over sources nothing is writing",
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

    A source that changes during bundling is a fact about the run
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
    """References grouped by document path, in path order.

    `closure.resolve` owns normalized identities; `placement` owns the
    order in which these groups appear in a bundle.
    """
    selected: dict[str, list[Reference]] = {}
    for one in requested:
        selected.setdefault(one.path, []).append(one)
    return dict(sorted(selected.items()))


def reaching(selected: dict[str, list[Reference]]) -> dict[str, tuple[str, ...]]:
    """The first recorded reference chain for each selected document.

    `traverse` owns discovery and chain selection.
    """
    return {
        path: selecting[0].chain for path, selecting in selected.items() if selecting
    }


def included(
    found: Sequence[Reference],
    parsed: Mapping[str, Sequence[Token]],
    read: Mapping[str, Source],
) -> list[Reference]:
    """Every reference that includes what it names: each one composing nothing.

    A document only composition directives reach contributes its content
    to their contributions alone: it stands in no file group, joins no
    merged group and is carried nowhere else. A document an inclusion
    also reaches keeps that inclusion, carrying what the inclusions
    select, beside its contributions.

    A link a composed section writes to one of its own subsections names
    a heading each copy of that section carries, where it points as
    `composition.Composing.copy` and `composition.owned` assign it, so it
    includes nothing, unless an inclusion
    carries the region writing it too: that group's copy of the link
    names the subsection as any link does. The same section linked from
    anywhere else is included as any is.
    """

    def spanned(path: str, chosen: Sequence[Token]) -> tuple[int, int]:
        source = read[path]
        start = (chosen[0].map or (0, 0))[0]
        end = max((token.map or (0, 0))[1] for token in chosen)
        return source.line(start + 1) or 1, source.line(end) or 1

    composed: dict[str, list[tuple[int, int, set[int]]]] = {}
    for one in found:
        if not one.composes or one.fragment is None:
            continue
        try:
            chosen = section(parsed[one.path], one.fragment) or ()
        except (Ambiguous, Nested):
            # `selection` refuses this reference with its own diagnostic.
            continue
        if not chosen:
            continue
        low, high = spanned(one.path, chosen)
        composed.setdefault(one.path, []).append(
            (low, high, {id(token) for token in chosen[1:]})
        )

    def written(one: Reference) -> tuple[str, int] | None:
        if one.origin is None:
            return None
        path, _, line = one.origin.rpartition(":")
        return (path, int(line)) if line.isdigit() else None

    def carries(one: Reference, at: tuple[str, int]) -> bool:
        if one.path != at[0]:
            return False
        if one.fragment is None:
            return True
        try:
            chosen = section(parsed[one.path], one.fragment) or ()
        except (Ambiguous, Nested):
            return False
        if not chosen:
            return False
        low, high = spanned(one.path, chosen)
        return low <= at[1] <= high

    def within(one: Reference) -> bool:
        if one.origin is None or one.fragment is None or one.path not in composed:
            return False
        path, _, line = one.origin.rpartition(":")
        if path != one.path or not line.isdigit():
            return False
        try:
            named = section(parsed[one.path], one.fragment) or ()
        except (Ambiguous, Nested):
            return False
        return bool(named) and any(
            low <= int(line) <= high and id(named[0]) in held
            for low, high, held in composed[one.path]
        )

    including = [one for one in found if not one.composes]
    dropped = {id(one) for one in including if within(one)}
    # A kept link can carry the region another dropped link is written
    # in, so the set shrinks to its fixed point.
    while True:
        kept = [one for one in including if id(one) not in dropped]
        restored = {
            id(one)
            for one in including
            if id(one) in dropped
            and (at := written(one)) is not None
            and any(carries(each, at) for each in kept)
        }
        if not restored:
            return kept
        dropped -= restored


def rooted(
    tokens: Sequence[Token], one: Reference, fragment: str
) -> tuple[Token, ...] | None:
    """Resolve a fragment through `source.section`, translating its refusals.

    An ambiguous or nested heading is reported as an input failure with
    the reference's resolved document and inclusion chain. An unmatched
    fragment remains None for `selection` to refuse.
    """
    try:
        return section(tokens, fragment)
    except Ambiguous as shared:
        raise input_failure(
            f"the reference {one.original!r} names {len(shared.lines)} headings "
            f"of the document it selects from, which it cannot tell apart",
            code=AMBIGUOUS_SOURCE_HEADING,
            remedy="retitle one of the headings so each takes a slug of its own",
            reference=one.original,
            resolved=one.path,
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
            resolved=one.path,
            source=one.origin,
            chain=one.chain,
        ) from nested


def selection(
    path: str,
    tokens: Sequence[Token],
    references: Sequence[Reference],
    entries: Collection[Reference],
) -> Selection | None:
    """The union of regions the references select from one document.

    `rooted` owns fragment lookup. Every fragment is checked even when
    a whole-document reference also selects the source; an unmatched
    one fails with its reference and inclusion chain. Whole-document
    entry selection returns None. Other selections return
    `source.Selection` with regions in document order.
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
        found = rooted(tokens, one, spelled)
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
    """Dependencies carried by the selected regions of one source.

    `source.uses` supplies occurrences, including diagram occurrences
    under `source.Click`. Dependency eligibility follows `closure.bundled`,
    using `closure.withholding` and `closure.Declarations.declares`.
    `closure.directive` supplies composition classification. A malformed
    Markdown destination fails with its source position and route.
    Each yielded reference extends the supplied chain by its identity.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        at = location(path, source.line(use.line))
        route = (*chain, use.destination)
        if use.resource:
            continue
        try:
            found = inside(path, use.destination, substitution, at, tags=use.tags)
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
            composes=found.fragment is not None and directive(use.opening),
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
    """Report operator combinations or targets that cannot be bundled.

    `closure.operators`, `closure.gapped`, `closure.arrowed`,
    `closure.deferring_dispatch`, `closure.contradicting` and
    `closure.conflicting` own operator recognition and contradictions.
    `closure.Declarations.answer` supplies the target state. The refusal
    names the authored use and its route; an operated absent target
    fails as not found, and an operated nondeclaring or non-Markdown
    target fails as an unsupported construct.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        at = location(path, source.line(use.line))
        if gapped(use.opening):
            raise input_failure(
                f"the link {use.name!r} writes a blank between "
                + " and ".join(
                    f"{OPERATOR_NAMES[mark]} {mark!r}"
                    for mark in operators(use.opening)
                )
                + " and the symbol after it, which state one operation only "
                "when written together",
                code=UNSUPPORTED_CONSTRUCT,
                remedy="write the symbols with no space between them, and one "
                "space between the last of them and the link's text",
                reference=use.name,
                source=at,
                chain=(*chain, use.destination),
            )
        if use.label is not None and arrowed(use.label):
            raise input_failure(
                f"the link {use.label!r} is labelled with an arrow, which states "
                f"no operation",
                code=UNSUPPORTED_CONSTRUCT,
                remedy=f"write the composition mark {INLINE_MARK!r}, a space and "
                "the link's text to compose the section",
                reference=use.label,
                source=at,
                chain=(*chain, use.destination),
            )
        if deferring_dispatch(use.opening):
            raise input_failure(
                f"the link {use.name!r} writes the deferral mark against a "
                "dispatch mark, which states a dispatch no bundle publishes",
                code=UNSUPPORTED_CONSTRUCT,
                remedy="write the dispatch mark, a space and the link's text, "
                "which bundles the target up front",
                reference=use.name,
                source=at,
                chain=(*chain, use.destination),
            )
        if contradicting(use.opening):
            raise input_failure(
                f"the link {use.name!r} writes a dispatch mark against the "
                "composition mark, so it sends its material to a sub-agent and "
                "places it inline at once",
                code=UNSUPPORTED_CONSTRUCT,
                remedy=f"write the composition mark {INLINE_MARK!r} alone to "
                "compose the section, or the dispatch mark to dispatch it",
                reference=use.name,
                source=at,
                chain=(*chain, use.destination),
            )
        if conflicting(use.opening):
            raise input_failure(
                f"the link {use.name!r} opens with "
                + "".join(
                    f"{OPERATOR_NAMES[mark]} {mark!r}"
                    for mark in operators(use.opening)
                )
                + ", which state two ways for one sub-agent to run",
                code=UNSUPPORTED_CONSTRUCT,
                remedy="open the link's text with the one operator that states how "
                "the material is bundled",
                reference=use.name,
                source=at,
                chain=(*chain, use.destination),
            )
        if not operators(use.opening):
            continue
        target = (
            None
            if use.resource
            else named(path, use.destination, substitution, at, chain, tags=use.tags)
        )
        answer = None if target is None else declarations.answer(target)
        if answer is Probed.DECLARING:
            continue
        if answer is Probed.ABSENT:
            raise input_failure(
                f"the link {use.name!r} opens with an operator and names "
                f"{use.destination!r}, which names no document, so the operator "
                f"states a bundling no run can read",
                code=TARGET_NOT_FOUND,
                remedy="name a Markdown document that exists, or remove the operator",
                reference=use.destination,
                source=at,
                chain=(*chain, use.destination),
            )
        if answer is Probed.SILENT:
            raise input_failure(
                f"the link {use.name!r} opens with an operator and names "
                f"{use.destination!r}, a document whose frontmatter declares no "
                f"prosiform, so the operator states no bundling the run can "
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
            f"the {kind} {use.name!r} opens with an operator and names "
            f"{use.destination!r}, which is no Markdown document or section, so "
            f"the operator states no bundling the run can carry out",
            code=UNSUPPORTED_CONSTRUCT,
            remedy="name a Markdown document or section, or remove the operator",
            reference=use.destination,
            source=at,
            chain=(*chain, use.destination),
        )


def refusals_of_picks(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> None:
    """Report the pick placements `closure.compiled_pick` refuses.

    Only a declaring target is checked. The diagnostic locates the
    use, extends its chain and suggests a permitted placement.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        if use.resource or not bundled_pick(use.opening, use.tags):
            continue
        at = location(path, source.line(use.line))
        target = named(path, use.destination, substitution, at, chain, tags=use.tags)
        if target is None or not declarations.declares(target):
            continue
        raise input_failure(
            f"the link {use.name!r} carries the pick token {PICK!r} and names "
            f"{use.destination!r}, which this run bundles, so no agent is left "
            f"to pick",
            code=UNSUPPORTED_CONSTRUCT,
            remedy=f"write the deferral mark {DEFERRAL_MARK!r} to leave the pick "
            f"to a later run, the dispatch mark {DISPATCH_MARK!r} to leave it to "
            "the dispatching agent, or name the alternative in the link's title",
            reference=use.name,
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
    """Require a composition directive to have a scope and a section target.

    `closure.directive` identifies directives and `closure.deferred`
    identifies their timing. A document-level directive or one naming
    a whole document is unsupported. In one scope, immediate and
    deferred directives naming one identity conflict, reported through
    `placed_twice`. `refusals_of_operators` owns target-kind refusals.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    placed: dict[tuple[int | None, str, str | None, bool], tuple[str, str]] = {}
    for use in uses(tokens, selected):
        if not directive(use.opening):
            continue
        at = location(path, source.line(use.line))
        if use.title is not None:
            target = named(
                path, use.destination, substitution, at, chain, tags=use.tags
            )
            if target is None or declarations.answer(target) is not Probed.DECLARING:
                continue
            if target.fragment is None:
                raise input_failure(
                    f"the directive {use.name!r} names {use.destination!r}, a "
                    f"whole document rather than a section of it, so no section "
                    f"answers its composition",
                    code=UNSUPPORTED_CONSTRUCT,
                    remedy="name a section of the document",
                    reference=use.destination,
                    source=at,
                    chain=(*chain, use.destination),
                )
            later = deferred(use.opening)
            section = (use.heading, target.path, target.fragment)
            other = placed.get((*section, not later))
            if other is not None:
                raise placed_twice(use, at, other, later, chain)
            placed.setdefault((*section, later), (use.name, at))
            continue
        raise input_failure(
            f"the link {use.name!r} is a composition directive in the preamble, "
            f"which no section holds, so the run has no scope to place "
            f"{use.destination!r} beneath",
            code=UNSUPPORTED_CONSTRUCT,
            remedy="write the directive inside the section its target belongs "
            "beneath, or write the link without the composition mark",
            reference=use.destination,
            source=at,
            chain=(*chain, use.destination),
        )


def placed_twice(
    use: Use,
    at: str,
    other: tuple[str, str],
    later: bool,
    chain: Sequence[str],
) -> Failure:
    """One scope composing a section and deferring it, naming both directives."""
    this = (use.name, at)
    immediate, deferring = (other, this) if later else (this, other)
    return input_failure(
        f"the directive {immediate[0]!r} at {immediate[1]} composes "
        f"{use.destination!r} in its scope and the deferred directive "
        f"{deferring[0]!r} at {deferring[1]} defers it from the same scope, so "
        f"the section would be placed now and left to a later run at once",
        code=UNSUPPORTED_CONSTRUCT,
        remedy="keep one of the two directives: compose the section, or defer it",
        reference=use.destination,
        source=at,
        chain=(*chain, use.destination),
    )


def composing_itself(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
    substitution: Substitution = UNSUBSTITUTED,
) -> Iterator[Diagnostic]:
    """Warnings for directives composing a section of their own document.

    `closure.directive` identifies composition and `closure.deferred`
    identifies deferral. Deferred directives and a directive selecting
    its own heading are excluded; `composition.Composing.cycle` owns cycle
    refusal. Each warning locates the directive and its route.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        if use.title is None or not directive(use.opening) or deferred(use.opening):
            continue
        at = location(path, source.line(use.line))
        target = named(path, use.destination, substitution, at, chain, tags=use.tags)
        if target is None or target.fragment is None or target.path != path:
            continue
        yield Diagnostic(
            WARNING,
            f"the directive {use.name!r} composes {identity(target)!r} in the "
            f"document that writes it, so it places material that document "
            f"already carries",
            code=COMPOSE_SELF,
            reference=use.destination,
            resolved=identity(target),
            chain=target.chain,
            remedy="move the section to a document of its own, or link it "
            "without the composition mark",
            location=Location(path, source.line(use.line) or 1, 1),
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
    """Targets withheld by the selected regions, with occurrence context.

    `closure.withholding_target` owns target classification. Each result
    retains its tags and extends the source chain, with composition and
    deferral flags supplied by `closure.directive` and `closure.deferred`.
    These results are targets to confirm, separate from the dependencies
    `required` yields.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for use in uses(tokens, selected):
        if use.resource:
            continue
        at = location(path, source.line(use.line))
        found = withholding_target(
            path,
            use.destination,
            use.opening,
            declarations,
            substitution,
            at,
            chain,
            tags=use.tags,
        )
        if found is None:
            continue
        yield replace(
            found,
            origin=at,
            chain=(*chain, identity(found)),
            title=use.title,
            composes=directive(use.opening),
            defers=deferred(use.opening),
        )


def dispatches(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    chosen: Selection | None,
    chain: Sequence[str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
) -> Iterator[Hop]:
    """Dispatch hops in the selected regions, with source locations and routes.

    `dispatch.written_in` supplies recognized dispatch occurrences. A
    recognized dispatch with empty text is refused at its occurrence.
    `source.Click` owns diagram-link text and title interpretation.
    """
    selected = tuple(regions(tokens)) if chosen is None else chosen.regions
    for region in selected:
        for link in written_in(
            path, source, tokens, region, declarations, substitution
        ):
            if not link.text:
                raise input_failure(
                    f"the link {link.opening!r} dispatches {link.written!r} with "
                    f"no text after its mark, so it names nothing for its "
                    f"reader",
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


def briefed(hop: Hop, conversion: Conversion) -> Reference | None:
    """The composing brief of one dispatch, or None where it has none.

    `closure.brief_of` owns brief selection and `closure.briefing` constructs
    its reference; conflicts and malformed references become located
    invocation failures. A picking dispatch
    whose alternative declares a brief produces `unresolved` with the
    varying-brief remedy. A returned brief inherits the dispatch's
    origin and replaces its final chain hop with the brief identity.
    """
    target = hop.target
    try:
        found = briefing(target, conversion)
    except Briefs as two:
        raise Failure(
            USAGE_FAILURE,
            Diagnostic(
                ERROR,
                f"{two}, both selected by the dispatch {target.original!r}, so "
                f"nothing says which section the dispatch carries",
                code=INVALID_USAGE,
                reference=target.original,
                chain=target.chain or None,
                remedy="select one preset naming a brief",
                location=hop.location,
            ),
        ) from two
    except Unresolvable as malformed:
        raise input_failure(
            f"the brief of {target.path!r}, carried by the dispatch "
            f"{target.original!r}, {malformed}",
            code=INVALID_CONVERSION_METADATA,
            remedy="name the brief by a fragment of a heading the document carries",
            reference=target.original,
            resolved=target.path,
            chain=target.chain,
        ) from malformed
    if picks(target.tags) and any(
        one.brief is not None for one in conversion.alternatives
    ):
        raise unresolved(target.path, conversion, placing=target, varying=True)
    if found is None:
        return None
    return replace(
        found,
        origin=target.origin,
        chain=(*target.chain[:-1], identity(found)),
        title=None,
    )


def verify_cached(root: Path, one: Reference, captured: Mapping[str, Capture]) -> None:
    """Check one cached target's referring route and filesystem identity.

    `access.opened` owns no-follow access. A refused route becomes an
    input failure; an identity differing from the capture becomes
    `changed`. A target without a capture needs no cache check.
    """
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


def stubbed(source: Source, run: frozenset[str]) -> Source:
    """One source as a run reads it: its settings holding the run's names."""
    return replace(source, conversion=replace(source.conversion, run=run))


def levelled(
    read: Mapping[str, Source], models: tuple[tuple[str, str], ...]
) -> dict[str, Source]:
    """Each source as a run reads it: its settings holding the run's level map."""
    return {
        path: replace(source, conversion=replace(source.conversion, models=models))
        for path, source in read.items()
    }


def presets_disagreeing(two: Levels, reference: Reference, what: str) -> Failure:
    """Two presets one reference selects stating different levels or models."""
    return Failure(
        USAGE_FAILURE,
        Diagnostic(
            ERROR,
            f"{two}, both selected by {what} {reference.original!r}, so nothing "
            f"says which holds",
            code=INVALID_USAGE,
            reference=reference.original,
            chain=reference.chain or None,
            remedy="select one preset stating the value",
        ),
    )


def entry_models(
    entry: Reference, conversion: Conversion
) -> tuple[tuple[str, str], ...]:
    """The run's level map, read from the presets its entry puts in force.

    The operator's own session follows the entry's bundle, so no model is
    applied there, and a level in the entry's selection is refused.
    """
    try:
        level = level_of(entry.tags, conversion)
        models = level_map(entry.tags, conversion)
    except Levels as two:
        raise presets_disagreeing(two, entry, "the entry") from two
    if level is not None:
        raise input_failure(
            f"the entry {entry.original!r} puts the level {level!r} in force, "
            f"and the operator's own session follows the entry's bundle, so no "
            f"model is applied to it",
            code=LEVEL_ON_ENTRY,
            remedy="state the level in a document the entry dispatches, or "
            "select no preset stating one",
            reference=entry.original,
            resolved=entry.path,
        )
    return models


def checked_models(hops: Sequence[Hop], read: Mapping[str, Source]) -> None:
    """Refuse a dispatch whose level the run's level map names no model for.

    A dispatch carrying the pick token is checked for each alternative
    its target declares, since each is a bundle of its own.
    """
    for hop in hops:
        conversion = read[hop.target.path].conversion
        targets = (
            [one for one, _alternative in alternatives_of(hop.target, conversion)]
            if picks(hop.target.tags)
            else [hop.target]
        )
        for target in targets:
            try:
                model_of(target, conversion)
            except Levels as two:
                raise presets_disagreeing(two, target, "the dispatch") from two
            except Unmapped as unmapped:
                raise Failure(
                    INPUT_FAILURE,
                    Diagnostic(
                        ERROR,
                        f"the dispatch {target.original!r} starts {target.path!r} "
                        f"at the level {unmapped.level!r}, which the run's level "
                        f"map names no model for",
                        code=LEVEL_UNMAPPED,
                        reference=target.original,
                        resolved=target.path,
                        chain=target.chain or None,
                        remedy=f"map {unmapped.level!r} to a model in the levels "
                        f"of the entry's presets",
                        location=hop.location,
                    ),
                ) from unmapped


def run_names(entry: Reference) -> frozenset[str]:
    """The names a run selects stubs by: those its entry's title gives.

    The pick token names no preset and `default` selects no named one,
    so neither is among them.
    """
    return frozenset(name for name in entry.tags if name not in (PICK, DEFAULT))


def entry_stubs(
    entry: Reference, conversion: Conversion
) -> dict[tuple[str, str | None], Governed]:
    """The entry's selected stub pairs, layered by `layer`.

    `run_names` owns selectable names; `subst_identity` and
    `subst_reference` own reference resolution. A conflict returned by
    `layer` produces `disagreeing`.
    """
    pairs: dict[tuple[str, str | None], Governed] = {}
    for preset in conversion.presets:
        if preset.stub is not None and preset.name.casefold() in run_names(entry):
            clash = layer(pairs, preset, entry.path)
            if clash is not None:
                raise disagreeing(*clash, entry.path, entry)
    return pairs


def staked(
    substitution: Substitution, entry: Reference, read: Mapping[str, Source]
) -> Substitution:
    """The mapping with its run entry and selected stub pairs.

    A mapping with an entry is retained. Otherwise `entry_stubs`
    supplies the pairs and `closure.Substitution.stubbed` binds them.
    """
    if substitution.entry is not None:
        return substitution
    pairs = entry_stubs(entry, read[entry.path].conversion)
    return substitution.stubbed(
        entry.path, {key: one.substitute for key, one in pairs.items()}
    )


def stub_off_entry(one: Reference, conversion: Conversion) -> None:
    """Refuse a stub declared by a document other than the run's entry.

    A stub binds trial material, and the run's entry is its one channel:
    its pairs reach every document the run bundles, so a document under
    test carries none.
    """
    stub = next((preset for preset in conversion.presets if preset.stub), None)
    if stub is not None:
        raise input_failure(
            f"{one.path!r} declares the stub {stub.name!r}, and a stub is "
            f"declared by the run's entry alone, whose pairs reach every "
            f"document the run bundles",
            code=STUB_OFF_ENTRY,
            remedy="declare the stub in the run's entry",
            reference=one.original,
            resolved=one.path,
            chain=one.chain,
        )


def traverse(
    root: Path,
    requested: Sequence[Reference],
    limits: Limits,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    run: frozenset[str] = frozenset(),
    picking: bool = True,
) -> tuple[
    dict[str, Source],
    dict[str, list[Token]],
    dict[str, dict[str, Definition]],
    dict[str, Capture],
    list[Reference],
    list[Hop],
    list[Diagnostic],
]:
    """Captured sources and discovered occurrences at the dependency fixed point.

    Entry references start the frontier. Each round loads new source
    paths, unions selecting occurrences and rechecks every growing
    selection. A new document/fragment or selecting occurrence enters
    the next frontier; no such addition ends traversal. Captures are
    shared by source path, while occurrences retain heading, tags and
    composition context. `verify_cached` checks every referring route.

    All selections are resolved before preset checks and selected-region
    refusals, so an invalid fragment reports first. `selection`,
    `governing`, `copies` and the operator refusal functions own those
    checks. `read_document`, `profile.parse`, `source.nesting` and
    `source.occurrences` supply the figures held by `limits.Limits.hold`.
    Expansion depth counts reference-chain links independently of
    fixed-point rounds; a shorter newly active route retains that depth.

    Each round uses an unrecorded mapping: later selecting occurrences
    can change routing, so substitutions are recorded during `compose`.
    Withheld targets, dispatches and self-composition warnings reflect
    the final round's mapping. `briefed` supplies dispatch briefs as
    dependencies of the discovering round.

    `staked` binds the run mapping, `stubbed` attaches its names and
    `stub_off_entry` checks declarations. `confirm` checks withheld
    targets after closure. When `picking` is true, `stated_pick` checks
    their picks, using `later_needs_pick` for a later run's requirement.
    """
    read: dict[str, Source] = {}
    parsed: dict[str, list[Token]] = {}
    defined: dict[str, dict[str, Definition]] = {}
    captured: dict[str, Capture] = {}
    found = list(requested)
    seen = {(one.path, one.fragment) for one in found}
    titled: set[tuple[str, str | None, str | None, bool, frozenset[str]]] = set()
    limits.hold(TARGETS, len(seen))
    counted: dict[str, int] = {}
    postponed: dict[
        tuple[str, str | None, str | None, bool, frozenset[str], bool], Reference
    ] = {}
    dispatching: dict[tuple[str, frozenset[str]], Hop] = {}
    composed_itself: dict[tuple[Location | None, str | None], Diagnostic] = {}
    total = 0
    entry = substitution.entry or requested[0].path

    def load(one: Reference) -> None:
        nonlocal total
        verify_cached(root, one, captured)
        if one.path in read:
            return
        limits.hold(FILES, len(read) + 1)
        opened = read_document(root, one, limits, total)
        if one.path != entry:
            stub_off_entry(one, opened.source.conversion)
        source = stubbed(opened.source, run)
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

    frontier = list(requested)
    while frontier:
        for one in frontier:
            load(one)
        substitution = staked(substitution, requested[0], read)
        discovered: list[Reference] = []
        reselecting: list[Reference] = []
        carried = contributing(found)
        chosen_of = {
            path: selection(path, parsed[path], selecting, requested)
            for path, selecting in carried.items()
        }
        mapping = governed(
            substitution,
            governing(read, parsed, carried, requested),
            copies(read, carried),
        ).unrecorded()
        # A later preset can invalidate answers from the preceding mapping.
        postponed.clear()
        dispatching.clear()
        composed_itself.clear()
        for path, selecting in carried.items():
            chosen = chosen_of[path]
            regions_read = (
                tuple(regions(parsed[path])) if chosen is None else chosen.regions
            )
            counted[path] = occurrences(parsed[path], regions_read)
            limits.hold(LINKS, sum(counted.values()))
            reached = min((one.chain for one in selecting), key=len)
            refusal = next(refusals(within(parsed[path], regions_read)), None)
            if refusal is not None:
                raise refused(path, read[path], refusal, reached)
            kept = {id(one) for one in included(selecting, parsed, read)}
            readings = [
                ([one for one in selecting if id(one) in kept], mapping),
                *(
                    (
                        [one for one in selecting if one.composes and one.tags == tags],
                        mapping.composed(path, tags),
                    )
                    for tags in dict.fromkeys(
                        one.tags for one in selecting if one.composes
                    )
                ),
            ]
            for references, reading in readings:
                part = selection(path, parsed[path], references, requested)
                refusals_of_operators(
                    path,
                    read[path],
                    parsed[path],
                    part,
                    reached,
                    declarations,
                    reading,
                )
                refusals_of_picks(
                    path,
                    read[path],
                    parsed[path],
                    part,
                    reached,
                    declarations,
                    reading,
                )
                refusals_of_directives(
                    path,
                    read[path],
                    parsed[path],
                    part,
                    reached,
                    declarations,
                    substitution,
                )
                for warning in composing_itself(
                    path, read[path], parsed[path], part, reached, reading
                ):
                    composed_itself.setdefault(
                        (warning.location, warning.reference), warning
                    )
                for one in withheld(
                    path,
                    read[path],
                    parsed[path],
                    part,
                    reached,
                    declarations,
                    reading,
                ):
                    verify_cached(root, one, captured)
                    postponed.setdefault(
                        (
                            one.path,
                            one.fragment,
                            one.title,
                            one.composes,
                            one.tags,
                            one.defers,
                        ),
                        one,
                    )
                briefs: list[Reference] = []
                for link in dispatches(
                    path,
                    read[path],
                    parsed[path],
                    part,
                    reached,
                    declarations,
                    reading,
                ):
                    dispatching.setdefault((link.name, link.target.tags), link)
                    load(link.target)
                    brief = briefed(link, read[link.target.path].conversion)
                    if brief is not None:
                        briefs.append(brief)
                for one in [
                    *required(
                        path,
                        read[path],
                        parsed[path],
                        part,
                        reached,
                        declarations,
                        reading,
                    ),
                    *briefs,
                ]:
                    verify_cached(root, one, captured)
                    occurrence = (
                        one.path,
                        one.fragment,
                        one.title,
                        one.composes,
                        one.tags,
                    )
                    if occurrence in titled:
                        continue
                    titled.add(occurrence)
                    if (one.path, one.fragment) in seen:
                        reselecting.append(one)
                        continue
                    limits.hold(EXPANSION_DEPTH, len(one.chain) - 1)
                    seen.add((one.path, one.fragment))
                    limits.hold(TARGETS, len(seen))
                    discovered.append(one)
        found.extend(discovered)
        found.extend(reselecting)
        frontier = [*discovered, *reselecting]
    later: dict[tuple[str, str | None, frozenset[str]], bool] = {}

    def needs_pick(deferral: Reference) -> bool:
        key = (deferral.path, deferral.fragment, deferral.tags)
        if key not in later:
            later[key] = later_needs_pick(
                root, deferral, read[deferral.path].conversion, declarations
            )
        return later[key]

    for one in postponed.values():
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
            read[one.path] = stubbed(opened.source, run)
            captured[one.path] = opened.capture
            parsed[one.path] = tokens
        confirm(parsed[one.path], one)
        if picking and (one.defers or picks(one.tags)):
            stated_pick(read[one.path].conversion, one, needs_pick)
    return (
        read,
        parsed,
        defined,
        captured,
        found,
        list(dispatching.values()),
        list(composed_itself.values()),
    )


def confirm(
    tokens: Sequence[Token],
    one: Reference,
) -> None:
    """Confirm the existence of a withheld target's heading.

    `source.index` supplies all headings. An unmatched fragment is an input
    failure with the target's route; a missing fragment needs no check.
    A deferred directive also needs the selectable section `rooted`
    validates. The caller supplies the captured source's token stream.
    """
    if one.fragment is None:
        return
    if one.composes:
        if rooted(tokens, one, one.fragment) is not None:
            return
    elif any(heading.fragment == one.fragment for heading in index(tokens)):
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


def later_needs_pick(
    root: Path,
    one: Reference,
    target: Conversion,
    declarations: Declarations,
) -> bool:
    """Whether a deferral's later run requires a pick.

    Simulate that target as an entry through `traverse`, using default
    `limits.in_force` budgets and `metadata.Conversion.carried` names.
    `included`, `picked` and `routed` supply the alternative test
    `resolved` owns. A successful unpicked traversal needs a pick
    where that test finds one missing. A failed unpicked traversal
    needs a pick only where an alternative traversal succeeds.
    """
    entry = replace(
        one,
        composes=False,
        defers=False,
        origin=None,
        chain=(identity(one),),
        tags=one.tags | target.carried(),
    )

    def traversed(
        tags: frozenset[str],
    ) -> tuple[dict[str, Source], dict[str, list[Token]], list[Reference]] | None:
        chosen = replace(entry, tags=tags)
        try:
            read, parsed, _, _, found, _, _ = traverse(
                root,
                [chosen],
                in_force({}),
                declarations,
                Substitution(),
                run_names(chosen),
                picking=False,
            )
        except (Failure, Crossed):
            return None
        return read, parsed, found

    unpicked = traversed(entry.tags)
    if unpicked is None:
        return any(
            traversed(entry.tags | {alternative.name.casefold()}) is not None
            for alternative in target.alternatives
        )
    read, parsed, found = unpicked
    conversion = read[one.path].conversion
    references = included(contributing(found)[one.path], parsed, read)
    return not picked(conversion, references) and routed(
        one.path, conversion, parsed[one.path], references, [entry]
    )


def stated_pick(
    conversion: Conversion,
    one: Reference,
    needs_pick: Callable[[Reference], bool],
) -> None:
    """Require a deferral or picking dispatch to state a usable pick.

    `picked` supplies selected alternatives, `tags.picks` identifies the
    pick token, and `needs_pick` supplies later-run need. A deferral
    may name at most one alternative, and must name one or carry the
    token where needed. A picking dispatch names no alternative beside
    its token. The token is refused for a target with no alternatives.
    A defect is located at the source link with its inclusion chain.
    """
    alternatives = conversion.alternatives
    pick = picks(one.tags)
    kind = "deferred link" if one.defers else "dispatch"
    if not alternatives:
        if not pick:
            return
        message = (
            f"the {kind} {one.original!r} carries the pick token "
            f"{PICK!r}, but {one.path} declares no alternative to pick"
        )
        remedy = f"remove {PICK!r} from the link's title"
    else:
        names = [preset.name for preset in picked(conversion, (one,))]
        if (len(names) == 1 and not pick) or (not names and pick):
            return
        if not names and not needs_pick(one):
            return
        listed = ", ".join(repr(preset.name) for preset in alternatives)
        if pick:
            stated = (
                f"names {', '.join(repr(name) for name in names)} beside the pick "
                f"token {PICK!r}"
            )
        elif names:
            stated = f"names {', '.join(repr(name) for name in names)}"
        else:
            stated = "names no alternative"
        message = (
            f"the {kind} {one.original!r} {stated}; {one.path} declares "
            f"the alternatives {listed}, and the link must name exactly one of "
            f"them or carry {PICK!r} alone"
        )
        remedy = f"title the link with one alternative, or with {PICK!r} alone"
    raise input_failure(
        message,
        code=UNSUPPORTED_CONSTRUCT,
        remedy=remedy,
        reference=one.original,
        resolved=one.path,
        source=one.origin,
        chain=one.chain,
    )


def pair(conversion: Conversion, tags: frozenset[str]) -> Membership | None:
    """The group pair for one tag selection.

    The first membership `closure.matching_presets` selects takes
    precedence over `metadata.Conversion.default`'s membership; None
    means neither supplies one. `agreed` checks selection agreement
    before the caller reads the pair.
    """
    return next(
        (
            preset.membership
            for preset in matching_presets(conversion, tags)
            if preset.membership is not None
        ),
        conversion.default.membership,
    )


def unselected(
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    selected: Mapping[str, Sequence[Reference]],
    entries: Collection[Reference],
) -> dict[str, tuple[str, ...]]:
    """Ordinary named presets absent from the references' selections.

    `closure.matching_presets` owns matching. Default, alternative and
    stub presets are excluded, and names retain declaration order.
    Only documents with references appear.
    """
    left: dict[str, tuple[str, ...]] = {}
    for path, references in selected.items():
        conversion = read[path].conversion
        chosen = {
            preset.name
            for reference in references
            for preset in matching_presets(conversion, reference.tags)
        }
        left[path] = tuple(
            preset.name
            for preset in conversion.presets
            if preset.name != DEFAULT
            and preset.choice is None
            and preset.stub is None
            and preset.name not in chosen
        )
    return left


def joined(
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    selected: Mapping[str, Sequence[Reference]],
    entries: Collection[Reference],
) -> dict[str, tuple[Membership, ...]]:
    """Distinct group memberships selected by each document's inclusion references.

    `agreed` validates each reference and `pair` reads its membership.
    Memberships retain reference order, with duplicate values omitted.
    """
    joins: dict[str, tuple[Membership, ...]] = {}
    for path, references in selected.items():
        conversion = read[path].conversion
        held: dict[Membership, None] = {}
        for reference in references:
            agreed(conversion, reference.tags, reference, path)
            one = pair(conversion, reference.tags)
            if one is not None:
                held[one] = None
        joins[path] = tuple(held)
    return joins


def group_depths(joins: Mapping[str, Sequence[Membership]]) -> dict[str, int]:
    """One consistent depth for every named group.

    Memberships are checked in source-path order. A group with
    different depths fails with the first declaration and the
    conflicting declaration's coordinate. `joined` supplies memberships.
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
    """A generated heading's `text` and its source `location`."""

    text: str
    location: Location


def file_named(
    path: str,
    source: Source,
    tokens: Sequence[Token],
    wrapped: bool,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    *,
    conversions: Mapping[str, Conversion],
) -> Named | None:
    """A document's emitted file heading with its source coordinate.

    `bundle.file_heading` owns heading text and `bundle.document_title`
    owns title recognition. A title locates the heading at its source
    line; a path heading uses the document's first coordinate. A parent
    with neither a single title nor a file heading returns None.
    """
    title = document_title(tokens)
    if title is None and not wrapped:
        return None
    at = None if title is None or title.map is None else title.map[0] + 1
    line = source.line(at)
    return Named(
        file_heading(path, tokens, declarations, substitution, conversions=conversions),
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
    """Warnings for case-insensitive collisions among generated source headings.

    `file_named` supplies file headings and `grouping.member_headings`
    supplies member text. Each file-heading set and each merged group's
    member set is compared separately; authored headings are excluded.
    Warnings and their member coordinates follow emitted order and are
    rendered by `coincidence`.
    """
    files: dict[str, tuple[int, list[Named]]] = {}
    found: list[tuple[int, Diagnostic]] = []
    conversions = {path: source.conversion for path, source in read.items()}
    for at, one in enumerate(groups):
        named = one.record.path
        if one.record.preamble:
            continue
        if one.record.merged is None:
            if named not in read:
                # Generated groups have no source coordinate to report.
                continue
            heading = file_named(
                named,
                read[named],
                parsed[named],
                one.filed,
                declarations,
                substitution,
                conversions=conversions,
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
    """The first document of a nonempty entry sequence, or None."""
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
) -> tuple[dict[str, list[Reference]], dict[tuple[str, str], str]]:
    """Included documents and their placing documents, in first-reference order.

    Entry order leads, followed by links read from placed selections.
    A document is placed on its first visit. `required` supplies
    dependencies and `included` identifies inclusions; composed
    selections are walked at their directive, under
    `closure.Substitution.composed`. `briefed` supplies dispatch briefs
    after their source's own links.

    `pair` owns membership selection. The second result records the
    placing document for each document/group pair; invocation-placed
    members have no placing document.
    """
    selected = contributing(included(found, parsed, read))
    order = list(dict.fromkeys(one.path for one in entries if one.path in selected))
    placers: dict[tuple[str, str], str] = {}
    entered: set[tuple[str, str]] = set()
    for one in entries:
        if one.path not in selected:
            continue
        held = pair(read[one.path].conversion, one.tags)
        if held is not None:
            entered.add((one.path, held.group))
    composed: set[tuple[str, str | None, frozenset[str]]] = set()

    def place(
        path: str, chosen: Selection | None, holder: str, reading: Substitution
    ) -> None:
        briefs = (
            briefed(hop, read[hop.target.path].conversion)
            for hop in dispatches(
                path, read[path], parsed[path], chosen, (), declarations, reading
            )
        )
        for one in [
            *required(
                path, read[path], parsed[path], chosen, (), declarations, reading
            ),
            *(brief for brief in briefs if brief is not None),
        ]:
            if one.composes:
                if (one.path, one.fragment, one.tags) not in composed:
                    composed.add((one.path, one.fragment, one.tags))
                    section_of = selection(one.path, parsed[one.path], [one], entries)
                    place(
                        one.path,
                        section_of,
                        holder,
                        substitution.composed(one.path, one.tags),
                    )
                continue
            if one.path not in selected:
                continue
            if one.path not in order:
                order.append(one.path)
            held = pair(read[one.path].conversion, one.tags)
            if held is not None and (one.path, held.group) not in entered:
                placers.setdefault((one.path, held.group), holder)

    at = 0
    while at < len(order):
        path = order[at]
        at += 1
        place(
            path,
            selection(path, parsed[path], selected[path], entries),
            path,
            substitution,
        )
    return {path: selected[path] for path in order}, placers


Division = tuple[str, bool]


def divisions(
    selected: Mapping[str, Sequence[Reference]],
    joins: Mapping[str, Sequence[Membership]],
) -> list[Division]:
    """File and merged divisions in first-member placement order.

    `joins` supplies the memberships `joined` owns. A document with
    none becomes a file division; a merged division is recorded once
    at its first membership. The flag distinguishes the two kinds.
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
    placers: Mapping[tuple[str, str], str],
    joins: Mapping[str, Sequence[Membership]],
) -> dict[Division, Division]:
    """The division each nested group stands inside.

    A merged group stands inside the division holding the document whose
    link placed its first member in that group: that document's file
    group, or the merged group it joins, the first of them the bundle
    places where it joins several. A group whose first member an entry
    placed in it is held by no division and stands at the top level, as
    every file group does.

    A document can place a group's first member while standing in that
    group, directly or through the groups holding its own: a later
    member's link placing the first member under a second pair. Such a
    group would hold itself, so it is held by no division and stands at
    the top level. Groups are weighed in placement order, so of two
    groups that would hold each other, the later one stands at the top
    level and holds the earlier.
    """
    rank = {one: at for at, one in enumerate(order)}
    held: dict[Division, Division] = {}
    for division in order:
        name, grouped = division
        if not grouped:
            continue
        placer = placers.get((merging[name][0], name))
        if placer is None:
            continue
        holder = (
            (placer, False)
            if not joins[placer]
            else min(
                (
                    one
                    for one in order
                    if one[0] in {join.group for join in joins[placer]}
                ),
                key=rank.__getitem__,
            )
        )
        enclosing: Division | None = holder
        while enclosing is not None and enclosing != division:
            enclosing = held.get(enclosing)
        if enclosing is None:
            held[division] = holder
    return held


def level(division: Division, held: Mapping[Division, Division]) -> int:
    """The heading level a division opens at: one below each division enclosing it."""
    holder = held.get(division)
    return 1 if holder is None else level(holder, held) + 1


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
    placers: Mapping[tuple[str, str], str],
    chains: Mapping[str, Sequence[str]],
    limits: Limits,
    dispatching: Anchors | None = None,
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    composing: Contributing | None = None,
    copies: Held | None = None,
    within: Within | None = None,
    folder: BundleFolder = WORKING_FOLDER,
) -> tuple[list[Group], Composed]:
    """Construct placed divisions and their composition destinations.

    `divisions` owns division order, `holders` owns nesting and `level`
    owns heading depth. `composed` builds each tree from its leaves;
    `grouping.prepared` and `grouping.merged` own merged-group layout,
    and `bundle.group` owns file-group construction.

    `preambled` selects introductions for `preamble.grouped`. Once all
    groups exist, `composition.compositions` places contributions and
    returns their destinations. `folder` supplies the publication
    context used by the builders.
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
    nested: dict[Division, list[Division]] = {}
    for division, holder in held.items():
        nested.setdefault(holder, []).append(division)
    built: dict[Division, Group] = {}
    authored = None if composing is None else composing.get((), {})
    conversions = {path: source.conversion for path, source in read.items()}
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
                conversions=conversions,
                folder=folder,
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
                        conversions=conversions,
                        folder=folder,
                    )
                    for path in paths
                ],
                parent,
                level((named, True), held),
            )
        folders: dict[str, list[str]] = {}
        for path in selected:
            if preambled(
                path, parsed[path], selected[path], bool(joins[path]), entries
            ):
                folders.setdefault(posixpath.dirname(path), []).append(path)
        preamble_divisions = []
        for paths in folders.values():
            built_preamble = preamble_group(
                paths,
                parsed,
                read,
                defined,
                {
                    path: selection(path, parsed[path], selected[path], entries)
                    for path in paths
                },
                assigned,
                declarations,
                substitution,
                conversions=conversions,
            )
            if built_preamble is not None:
                preamble_divisions.append(built_preamble)
        return compositions(
            [
                one
                for division in order
                if division not in held
                for one in composed(division, built, nested)
            ]
            + preamble_divisions,
            parsed,
            read,
            defined,
            limits,
            assigned,
            dispatching,
            declarations,
            substitution,
            composing,
            copies,
            within,
            folder,
        )


@contextmanager
def assembling(chains: Mapping[str, Sequence[str]]) -> Iterator[None]:
    """Translate construction refusals into located input failures.

    `bundle.Overflow` and `bundle.Unplaced` identify file-group faults;
    `composition`'s exception types identify contribution faults.
    `chains` supplies each source's inclusion route. A composition
    fault names its directive and extends that route; a cycle carries
    earlier directives as related locations. `crossing` renders output
    budget crossings.
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
            "or write the link without the composition mark",
            reference=parentless.destination,
            source=location(parentless.path, parentless.line),
            chain=(*chains.get(parentless.path, ()), parentless.destination),
        ) from parentless
    except Overflowing as beyond:
        raise input_failure(
            f"the {beyond.kind} {beyond.destination!r} in {beyond.path!r} "
            f"composes the heading {beyond.heading!r} at level {beyond.level}, "
            f"which is beyond H{MAX_LEVEL}",
            code=HEADING_DEPTH_OVERFLOW,
            remedy="write the dispatch in a shallower section"
            if beyond.kind == "dispatch"
            else "write the directive in a shallower section, or name a "
            "shallower section of its target",
            reference=beyond.destination,
            source=location(beyond.path, beyond.line),
            chain=(*chains.get(beyond.path, ()), beyond.destination),
        ) from beyond
    except Cycling as cycling:
        first, closing = cycling.chain[0], cycling.chain[-1]
        sections = tuple(identity(each.target) for each in cycling.chain)
        briefing = first.kind == "dispatch"
        raise Failure(
            INPUT_FAILURE,
            Diagnostic(
                ERROR,
                f"the directive {closing.written!r} in {closing.at[0]!r} composes "
                f"{sections[-1]!r}, which holds a directive on the chain of "
                f"compositions that placed it, so the composition would not end"
                if not briefing
                else f"the brief the dispatch {first.written!r} in {first.at[0]!r} "
                f"carries composes {sections[-1]!r}, which holds that dispatch, so "
                f"the brief would be lifted inside itself without end",
                code=DISPATCH_CYCLE if briefing else UNSUPPORTED_CONSTRUCT,
                reference=closing.written,
                source=location(closing.at[0], closing.line),
                chain=(*chains.get(first.at[0], ()), *sections),
                remedy="remove the directive from the brief, or dispatch its target "
                "without a brief"
                if briefing
                else "remove a directive from the chain, or write one without the "
                "composition mark",
                location=Location(closing.at[0], closing.line or 1, 1),
                related=tuple(
                    RelatedLocation(
                        each.at[0],
                        each.line or 1,
                        1,
                        f"{each.kind} carrying {identity(each.target)!r}"
                        if each.kind == "dispatch"
                        else f"composes {identity(each.target)!r}",
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
        why = (
            "is no section a destination section can stand beneath"
            if unplaced.composing
            else "is emitted as text alone, so the bundle has no link to publish"
        )
        raise input_failure(
            f"the {kind} {unplaced.opening!r} in {unplaced.path!r} names "
            f"{unplaced.destination!r}, and the heading that carries it {why}",
            code=UNSUPPORTED_CONSTRUCT,
            remedy=f"write the {kind} in the body beneath the heading",
            reference=unplaced.destination,
            source=location(unplaced.path, unplaced.line),
            chain=chains.get(unplaced.path, ()),
        ) from unplaced


def destination_map(
    groups: Sequence[Group], assigned: Sequence[str]
) -> dict[tuple[str, str | None], str]:
    """The first destination assigned to each emitted target identity.

    Each group's recorded heading targets are paired with their
    `assigned` fragments. `source.fragments` owns fragment allocation;
    the group's builders own the targets their headings answer.
    """
    found: dict[tuple[str, str | None], str] = {}
    at = 0
    for one in groups:
        for offset, targets in enumerate(one.targets):
            for target in targets:
                found.setdefault(target, assigned[at + offset])
        at += len(one.headings)
    return found


def emitted_regions(
    groups: Sequence[Group], parsed: Mapping[str, Sequence[Token]]
) -> Iterator[tuple[Range, Token]]:
    """Each source region the published groups carry, in first-emitted order.

    A region is yielded once for each selection its links are read under:
    a group's, and each tag selection of the composed copies carrying it.
    """
    seen: set[tuple[str, tuple[int, int], frozenset[str] | None]] = set()
    for one in groups:
        for part in one.record.ranges:
            key = (part.path, part.lines, part.selecting)
            if key not in seen:
                seen.add(key)
                yield part, region_of(parsed[part.path], part)


def protected_headings(
    groups: Sequence[Group],
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    entries: Collection[Reference],
    chains: Mapping[str, Sequence[str]],
    declarations: Declarations,
    substitution: Substitution,
) -> set[int]:
    """The first destination headings used by entries and included references.

    A source target resolves to its first recorded destination, as
    `destination_map` states. A composition addresses its own contribution
    rather than a source group's heading. Its contribution and the
    dispatch headings are retained by `pruning.prune` independently.
    """
    requested = {(entry.path, entry.fragment) for entry in entries}
    for part, region in emitted_regions(groups, parsed):
        requested.update(
            (found.path, found.fragment)
            for found in required(
                part.path,
                read[part.path],
                parsed[part.path],
                Selection((region,)),
                chains.get(part.path, ()),
                declarations,
                substitution.composed(part.path, part.selecting),
            )
            if not found.composes
        )
    owners: dict[tuple[str, str | None], int] = {}
    for grouped in groups:
        for heading in grouped.record.headings:
            for target in heading.answers:
                owners.setdefault(target, id(heading))
    return {owners[target] for target in requested if target in owners}


def empty_sections(
    removed: Sequence[Removed],
    read: Mapping[str, Source],
    parsed: Mapping[str, Sequence[Token]],
    chains: Mapping[str, Sequence[str]],
) -> list[Diagnostic]:
    """Warn for `pruning.prune` removals in their original bundle order.

    A generated heading locates the title of the first source it answers
    or its group carries.
    Where the generated structure supplies no source, its heading and
    group name still identify what the bundle omitted.
    """
    warnings = []
    for one in removed:
        heading = one.heading
        candidates = [
            *(path for path, _fragment in heading.answers),
            one.record.path,
            *(path for each in one.record.headings for path, _fragment in each.answers),
            *one.record.paths(),
        ]
        path = next((path for path in candidates if path in read), None)
        at = None
        if path is not None:
            title = document_title(parsed[path])
            line = None if title is None or title.map is None else title.map[0] + 1
            at = Location(path, read[path].line(line) or 1, 1)
        warnings.append(
            Diagnostic(
                WARNING,
                f"the empty {heading.kind} {heading.text!r} in {one.record.path!r} "
                "was pruned from the bundle",
                code=EMPTY_SECTION,
                source=path,
                chain=None if path is None else tuple(chains.get(path, ())) or None,
                location=at,
            )
        )
    return warnings


def compose(
    read: dict[str, Source],
    parsed: dict[str, list[Token]],
    defined: dict[str, dict[str, Definition]],
    entries: Collection[Reference],
    found: Sequence[Reference],
    limits: Limits,
    bundle_file: Callable[[Reference], str],
    declarations: Declarations = DECLARING,
    substitution: Substitution = UNSUBSTITUTED,
    folder: BundleFolder = WORKING_FOLDER,
) -> tuple[str, list[Diagnostic], list[Hop], list[Diagnostic]]:
    """The validated bundle, heading warnings and published dispatch hops.

    `placement` orders sources and `assembled` builds their groups.
    Construction runs twice: the first pass discovers emitted headings,
    then `source.fragments` and `destination_map` provide the map used
    for the final rewrite. `dispatch.subsections` and `bundle.opened`
    run in both passes so the map includes generated headings, and
    `pruning.prune` follows `dispatch.subsections` in each pass, with
    `protected_headings` naming the headings it keeps.

    `composition.contributions` and `composition.owned` provide the
    contribution maps; `dispatch.anchors` supplies dispatch destinations.
    `candidate.validate` checks the final result, with `unsafe`
    translating boundary refusals to input failures. Dispatch placement
    and heading collisions use `dispatch`'s located refusals.

    Published hops and self-composition warnings are read from
    `emitted_regions`, using `dispatches` and `composing_itself`.
    `empty_sections` and `coincident` supply heading warnings. `folder`
    is the publication context passed to the builders.
    """
    chains = reaching(contributing(found))
    selected, placers = placement(
        read, parsed, found, entries, declarations, substitution
    )
    joins = joined(read, parsed, selected, entries)
    copies: Held = {}
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
            copies=copies,
            folder=folder,
        )
        briefs = Composing(
            parsed,
            read,
            defined,
            limits,
            declarations=declarations,
            substitution=substitution,
            held=copies,
            folder=folder,
        )
        with assembling(chains):
            headed, placed = subsections(
                built,
                parsed,
                read,
                bundle_file,
                briefs.brief,
                declarations,
                substitution,
            )
        contributed.update(briefs.placed)
        protected = protected_headings(
            headed, read, parsed, entries, chains, declarations, substitution
        )
        headed, removed, positions = prune(headed, parsed, protected)
        collisions(headed, read)
    except Refused as refusal:
        raise Failure(INPUT_FAILURE, refusal.diagnostic) from refusal
    # `bundle.opened` adds a heading after dispatch positions are recorded.
    placed = {
        key: {
            link: positions[at] + 1 if isinstance(at, int) else at
            for link, at in served.items()
        }
        for key, served in placed.items()
    }
    headed = opened(headed)
    assigned = fragments([heading for one in headed for heading in one.headings])
    targets = destination_map(headed, assigned)
    dispatching = anchors(placed, assigned)
    composing = contributions(contributed, headed, assigned)
    within = owned(copies, headed, assigned)
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
        within=within,
        folder=folder,
    )
    briefs = Composing(
        parsed,
        read,
        defined,
        limits,
        targets,
        dispatching,
        declarations,
        substitution,
        composing,
        within=within,
        folder=folder,
    )
    with assembling(chains):
        groups, _ = subsections(
            built,
            parsed,
            read,
            bundle_file,
            briefs.brief,
            declarations,
            substitution,
        )
    protected = protected_headings(
        groups, read, parsed, entries, chains, declarations, substitution
    )
    groups, _removed, _positions = prune(groups, parsed, protected)
    groups = opened(groups)
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
            bundle_file=bundle_file,
            within=within,
            folder=folder,
        )
    except Unsafe as boundary:
        reached = chains.get(boundary.path or "", ())
        raise unsafe(boundary, reached) from boundary
    hops: dict[tuple[str, frozenset[str]], Hop] = {}
    itself: dict[tuple[Location | None, str | None], Diagnostic] = {}
    for part, region in emitted_regions(groups, parsed):
        path = part.path
        chosen = Selection((region,))
        chain = chains.get(path, ())
        reading = substitution.composed(path, part.selecting)
        for hop in dispatches(
            path, read[path], parsed[path], chosen, chain, declarations, reading
        ):
            hops.setdefault((hop.name, hop.target.tags), hop)
        for warning in composing_itself(
            path, read[path], parsed[path], chosen, chain, reading
        ):
            itself.setdefault((warning.location, warning.reference), warning)
    return (
        bundled,
        empty_sections(removed, read, parsed, chains)
        + coincident(groups, selected, joins, read, parsed, declarations, substitution),
        list(hops.values()),
        list(itself.values()),
    )


def resource(destination: str, embedded: bool) -> bool:
    """Whether a destination requires the resource-portability warning.

    An absent path, scheme, authority or drive letter excludes a use.
    Other uses qualify when embedded or when `profile.is_markdown`
    rejects their suffix. `closure.components` owns splitting and
    `source.external` owns scheme and authority detection.
    """
    written = components(destination).path
    if not written or external(written) or DRIVE.match(written) is not None:
        return False
    return embedded or not is_markdown(written)


def resourced(bundled: str, budget: int) -> bool:
    """Whether the emitted bundle contains a resource use.

    `profile.parse` and `source.uses` read the emitted text; `resource`
    owns classification. Diagram occurrences follow `source.Click`.
    """
    tokens = parse(bundled, budget)
    return any(
        resource(use.destination, use.resource)
        for use in uses(tokens, tuple(regions(tokens)))
    )


def substituted(
    mapping: Substitution,
    quiet: Collection[tuple[str, tuple[str, str | None], str]],
) -> list[Diagnostic]:
    """One warning for each stub's `subst` pair a reference named.

    `closure.Redirects.record` owns occurrence recording and deduplication.
    The warning names the recorded link as
    `location` where the reference stands in a source, the destination
    the author wrote as `source`, and the substitute's identity as
    `resolved`; its message states the identity the reference would have
    resolved to, which is what tells two keys naming one stand-in apart.
    A quiet pair, as `routes` names one, is the route its author
    declared, so a reference using it raises nothing.
    """
    return [
        Diagnostic(
            WARNING,
            f"the reference {one.source!r} is redirected to the substitute "
            f"{one.resolved!r}, where it would have resolved to {one.would!r}",
            code=SUBST_USED,
            source=one.source,
            resolved=one.resolved,
            location=None if one.origin is None else located(one.origin),
        )
        for one in mapping.redirects.targets()
        if (*one.pair, one.declared) not in quiet
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
    """A publication unit's `text`, file `name`, `warnings` and source `selection`."""

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
    """Validate the publication set, emit its warnings and optionally write it.

    Output byte limits, distinct bundle names and filesystem name
    lengths are checked before warnings or bundle writes. The parent
    folder is created where absent. `occupied` owns the run-path
    check, and `publish_folder` owns replacement of the set.

    Bundle warnings are emitted in bundle order, followed by `notices`.
    When `check` is true, validation and warnings complete without
    writing bundle files; otherwise the set and `retained` request are
    passed to `publish_folder`.
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
            raise colliding(one.name, earlier.selection, one.selection)
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


def colliding(name: str, earlier: str, later: str) -> Failure:
    """Two bundles of one run whose selections derive one file name."""
    return Failure(
        PUBLICATION_FAILURE,
        Diagnostic(
            ERROR,
            f"the bundles of {earlier!r} and {later!r} both "
            f"derive the name {name!r}, so one would overwrite the other",
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
    """Publish a staged bundle folder, preserving the earlier set on failure.

    Bundles are written into a fresh sibling folder. The existing run
    path is renamed aside, then the staged folder is renamed into
    place; a reader sees a complete set or, between renames, no path.
    Symbolic links are renamed and removed without following them.

    A failure before placement restores the earlier path and removes
    staging. An unrestorable earlier set remains where `unrestored`
    reports it. Failure to remove an earlier set after publication
    leaves the new set published and reports its location. `retained`
    keeps the earlier set, creating an empty one first where absent.
    `sibling` owns staging names; `run_folder` owns the run path.
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


def selection_name(selection: BundleSelection) -> str:
    """Path and fragment with sorted, individually URL-escaped preset names.

    A nonempty selection adds a hyphen and joins declaration spellings with
    plus signs. Escaping each name keeps separators and path characters literal.
    """
    name = str(Path(selection.path).with_suffix("")).replace(os.sep, "_")
    if selection.fragment is not None:
        name += "__" + selection.fragment
    if selection.presets:
        name += "-" + "+".join(
            quote(preset, safe="") for preset in sorted(selection.presets)
        )
    return name


def bundle_file(selection: BundleSelection) -> str:
    """The `selection_name` of one effective selection with the bundle suffix."""
    return selection_name(selection) + BUNDLE_SUFFIX


def run_folder(output: Path, entry: BundleSelection) -> Path:
    """The run's output path, using its entry's `selection_name` and bundle suffix."""
    return output / (selection_name(entry) + RUN_FOLDER_SUFFIX)


@dataclass(frozen=True)
class Bundled:
    """One bundle and its run evidence.

    `text`, `name` and `selection` identify the bundle. `hops` maps
    effective selections to dispatch occurrences. `leading` and
    `trailing` hold warnings around the run's depth warning. `captured`
    holds source captures and `unselected` unused preset names. `pairs`
    and `copied` hold group and copy substitution pairs; `linked` holds
    authored target identities by source. `models` is the run's level
    map and `substitution` its reference mapping.
    """

    text: str
    name: str
    selection: BundleSelection
    hops: Mapping[BundleSelection, Hop]
    leading: Sequence[Diagnostic]
    trailing: Sequence[Diagnostic]
    captured: Mapping[str, Capture]
    unselected: Mapping[str, tuple[str, ...]]
    pairs: Mapping[str, Mapping[tuple[str, str | None], Governed]]
    copied: Mapping[
        tuple[str, frozenset[str]], Mapping[tuple[str, str | None], Governed]
    ]
    linked: Mapping[str, frozenset[tuple[str, str | None]]]
    models: tuple[tuple[str, str], ...] = ()
    substitution: Substitution = UNSUBSTITUTED

    def in_force(self) -> Iterator[tuple[str, tuple[str, str | None], Governed]]:
        """Each pair in force for a document, its group's then its copies', by path."""
        held = [
            *(((path, 0, ()), pairs) for path, pairs in self.pairs.items()),
            *(
                ((path, 1, tuple(sorted(tags))), pairs)
                for (path, tags), pairs in self.copied.items()
            ),
        ]
        for (path, _kind, _tags), pairs in sorted(held, key=lambda one: one[0]):
            for key, pair in pairs.items():
                yield path, key, pair


def bundle_one(
    root: Path,
    requested: Sequence[Reference],
    options: argparse.Namespace,
    substitution: Substitution = UNSUBSTITUTED,
    run: frozenset[str] = frozenset(),
    entry: BundleSelection | None = None,
    models: tuple[tuple[str, str], ...] | None = None,
) -> Bundled:
    """Bundle one effective entry selection and collect its evidence.

    `budgets` creates this bundle's counters. `traverse` discovers its
    sources, `resolved` checks alternative selections, and `compose`
    constructs its output. `staked` binds the supplied run mapping.
    `run` supplies run names, `entry` the selection naming the run
    folder, and `models` its level map. An absent entry uses this
    bundle's own selection for `run_folder`. An absent model map
    is read by `entry_models` from this bundle's own entry.

    `closure.bundle_selection` identifies dispatched selections;
    `closure.alternatives_of` expands a picking dispatch. `unselected`,
    `governing`, `copies` and `linked` supply evidence for run warnings.
    """
    limits = budgets(options)
    declarations = Declarations(lambda found: probe(root, found, limits))
    declared_entries(requested, declarations)
    try:
        read, parsed, defined, captured, found, hops, _ = traverse(
            root, requested, limits, declarations, substitution, run
        )
    except Crossed as crossed:
        raise crossing(crossed) from crossed
    substitution = staked(substitution, requested[0], read)
    if models is None:
        models = entry_models(requested[0], read[requested[0].path].conversion)
    read = levelled(read, models)
    checked_models(hops, read)
    resolved(read, parsed, contributing(found), requested, hops)
    selected = bundle_selection(requested[0], read[requested[0].path].conversion)
    name = bundle_file(selected)
    named = {name: selected}
    written = run_folder(
        Path(options.output).resolve(), selected if entry is None else entry
    )
    folder = BundleFolder(root.as_posix(), written.as_posix())

    def dispatched_file(reference: Reference) -> str:
        effective = bundle_selection(reference, read[reference.path].conversion)
        file = bundle_file(effective)
        earlier = named.setdefault(file, effective)
        if earlier != effective:
            raise colliding(file, selection_text(earlier), selection_text(effective))
        return file

    pairs = governing(read, parsed, contributing(found), requested)
    copied = copies(read, contributing(found))
    bundled, coinciding, hops, itself = compose(
        read,
        parsed,
        defined,
        requested,
        found,
        limits,
        dispatched_file,
        declarations,
        governed(substitution, pairs, copied),
        folder,
    )
    dispatching: dict[BundleSelection, Hop] = {}
    own: list[Hop] = []
    for hop in hops:
        conversion = read[hop.target.path].conversion
        targets = (
            [one for one, _alternative in alternatives_of(hop.target, conversion)]
            if picks(hop.target.tags)
            else [hop.target]
        )
        for target in targets:
            selection = bundle_selection(target, conversion)
            if selection in dispatching:
                continue
            dispatching[selection] = replace(hop, target=target)
            if hop.own and (not own or own[-1] is not hop):
                own.append(hop)
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
    return Bundled(
        bundled,
        name,
        selected,
        dispatching,
        [
            *coinciding,
            *(selfward(hop) for hop in own),
            *itself,
        ],
        trailing,
        captured,
        unselected(read, parsed, contributing(found), requested),
        pairs,
        copied,
        {
            path: linked(path, parsed[path], tuple(regions(parsed[path])))
            for path in {
                *(
                    path
                    for path, held in pairs.items()
                    if any(one.routing for one in held.values())
                ),
                *(
                    path
                    for (path, _tags), held in copied.items()
                    if any(one.routing for one in held.values())
                ),
            }
        },
        models,
        substitution,
    )


def linked(
    document: str, tokens: Sequence[Token], selected: Sequence[Token]
) -> frozenset[tuple[str, str | None]]:
    """The document and section each link in the selected regions of one document names.

    An identity is the one the link was written to name, before any
    `subst` pair redirects it, and a link naming no local Markdown
    document names none.
    """
    return frozenset(
        (found.path, found.fragment)
        for use in uses(tokens, selected)
        if not use.resource and (found := named(document, use.destination)) is not None
    )


def names(
    identities: Collection[tuple[str, str | None]], key: tuple[str, str | None]
) -> bool:
    """Whether a link naming one of these identities names a `subst` key.

    A key carrying a section is named by a link to that section, and a
    key naming a whole document by a link to the document or any of
    its sections.
    """
    path, fragment = key
    return key in identities or (
        fragment is None and any(one == path for one, _ in identities)
    )


def unused_presets(bundles: Iterable[Bundled]) -> list[Diagnostic]:
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
            f"bundled, so it governs nothing",
            code=PRESET_UNUSED,
            source=path,
            remedy="name the preset in the reaching link's title, or drop the preset",
        )
        for path in sorted(left)
        for name in left[path]
    ]


def routes(
    bundles: Iterable[Bundled],
) -> set[tuple[str, tuple[str, str | None], str]]:
    """The routing pairs the run put in force, by document, key and substitute.

    A pair a stub holds for one document, key and substitute in any
    bundle of the run is no route there. It stands in only for the
    substitute it names, so a routing pair naming another substitute for
    the same key stays a route.
    """
    routing: set[tuple[str, tuple[str, str | None], str]] = set()
    standing: set[tuple[str, tuple[str, str | None], str]] = set()
    for one in bundles:
        for path, key, pair in one.in_force():
            named = (path, key, identity(pair.substitute))
            (routing if pair.routing else standing).add(named)
    return routing - standing


def unused_pairs(bundles: Iterable[Bundled], mapping: Substitution) -> list[Diagnostic]:
    """One warning for each `subst` pair in force that no reference used.

    A pair is in force for the links its declaring document writes, so
    one no reference of the run named substitutes nothing. A routing
    pair routes whatever the document is bundled for, so it is unused
    only where no link of its document names its key, a link outside
    the selection naming it as one inside does. The warning
    carries the key as its author wrote it as `source`, names the
    declaring document and preset in its message, and carries no
    location: bundle by bundle, each bundle's documents by path, and each
    document's pairs in the order its presets are read.
    """
    held: dict[tuple[str, str, tuple[str, str | None]], Governed] = {}
    written: dict[str, frozenset[tuple[str, str | None]]] = {}
    for one in bundles:
        written.update(one.linked)
        for path, key, pair in one.in_force():
            held.setdefault((path, pair.preset, key), pair)
    return [
        Diagnostic(
            WARNING,
            f"the subst key {one.pair.original!r} of prosiform.{one.preset} in "
            f"{path!r} names "
            + (
                "no link its document writes"
                if one.routing
                else "no reference the run resolved where it is in force"
            )
            + ", so it substitutes nothing",
            code=SUBST_UNUSED,
            source=one.pair.original,
            remedy="name an identity the declaring document links, or drop the pair",
        )
        for (path, _preset, key), one in held.items()
        if not (
            names(written[path], key)
            if one.routing
            else mapping.redirects.served((path, key), one.substitute)
        )
    ]


def dispatched_set(
    root: Path,
    entry: Bundled,
    single: Collection[BundleSelection],
    options: argparse.Namespace,
    run: frozenset[str] = frozenset(),
) -> dict[BundleSelection, Bundled]:
    """Bundle each distinct dispatched selection once, transitively.

    Selections are visited in occurrence order. A selection equal to
    the run's entry reuses its bundle; other selections are passed to
    `bundle_one` under the entry's mapping, names and model map.
    """
    built: dict[BundleSelection, Bundled] = {}
    pending = list(entry.hops.items())
    while pending:
        selected, hop = pending.pop(0)
        if selected in built or selected in single:
            continue
        target = replace(hop.target, origin=None, chain=(hop.name,))
        one = bundle_one(
            root,
            [target],
            options,
            entry.substitution,
            run,
            entry.selection,
            entry.models,
        )
        built[selected] = one
        pending.extend(one.hops.items())
    return built


def selection_text(selected: BundleSelection) -> str:
    """One bundle selection as its destination and matched declared preset names."""
    destination = selected.path
    if selected.fragment is not None:
        destination += f"#{selected.fragment}"
    if selected.presets:
        names = json.dumps(sorted(selected.presets), ensure_ascii=False)
        destination += f" with presets {names}"
    return destination


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
    if options.entry is None:
        raise usage_failure("one entry reference is required")
    if options.output == STANDARD_OUTPUT:
        raise usage_failure(
            "-o - names standard output, which carries no bundle; -o names the "
            "folder the run's bundles are written under"
        )
    mapping = Substitution()
    requested = [entry(options.entry, options.pick)]
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

    output = Path(options.output).resolve()
    run = run_names(requested[0])
    first = bundle_one(root, requested, options, mapping, run)
    folder = run_folder(output, first.selection)
    single = {first.selection}
    built = dispatched_set(root, first, single, options, run)

    def onward(target: BundleSelection) -> Mapping[BundleSelection, Hop]:
        return first.hops if target in single else built[target].hops

    try:
        cycle(first.hops, single, onward)
    except Refused as refused:
        raise Failure(INPUT_FAILURE, refused.diagnostic) from refused
    captured = captured_once(one.captured for one in (first, *built.values()))
    for held in sources(root, captured):
        if held == folder or folder in held.parents:
            raise usage_failure(
                f"the output folder {str(folder)!r} holds the input source "
                f"{str(held)!r}"
            )
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
            selection_text(first.selection),
        ),
        *(
            Bundle(
                one.text,
                one.name,
                [*one.leading, *one.trailing],
                selection_text(selected),
            )
            for selected, one in built.items()
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
            *substituted(mapping, routes((first, *built.values()))),
            *unused_pairs((first, *built.values()), mapping),
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
