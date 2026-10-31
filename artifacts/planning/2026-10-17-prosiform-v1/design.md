# prosiform: revised v1 design

prosiform is intended for agent skills and other instruction sets authored as collections of linked Markdown documents. Authors can keep procedures, shared rules, prerequisites, and reference material in separate, reusable sections rather than duplicating them in every operation. An agent typically enters through a document such as `SKILL.md` and selects a linked procedure to carry out.

The problem addressed here is the gap between that modular authoring structure and the complete context needed to perform an operation. A document or section link identifies a *destination*, but does not itself establish which content is retrieved, whether its dependencies are followed, or whether the resulting context is complete. Leaving those decisions to the agent makes retrieval part of the reasoning task, with opportunities for missed prerequisites, unnecessarily broad reads, and inconsistent handling of repeated or recursive references.

prosiform moves this retrieval and assembly work into a deterministic compilation step. Given one or more local document or section references, it recursively resolves supported Markdown dependencies, consolidates repeated and overlapping *selections*, and produces one continuous Markdown document organized under a top-level file heading for each source, carrying its title or, where it has none, its path. Source headings move down one level beneath that heading, except in a file whose own title it carries, and heading-only ancestors preserve the outline of partial selections; links to included documents are rewritten to the fragments a renderer generates for the headings they now name. It validates the complete *candidate* before *publication*, either returning the *bundle* or failing with *diagnostics* the calling agent can explain to the user. Authors retain modular source files, while the agent receives the selected material and its explicitly linked dependencies without needing further local Markdown retrieval.

The intended guarantee is complete, validated bundling of the explicitly linked content under a declared Markdown *profile*, not control over agent execution. prosiform does not infer unlinked prerequisites, execute procedures, enforce workflow transitions, or guarantee that an agent obeys the resulting instructions; web references and non-Markdown *resources* are also outside its recursive bundling scope. This separation lets the tool make retrieval predictable without becoming a workflow engine or requiring authors to abandon their linked-document structure.

A term italicised on first use is a contract term. It means one thing and nothing else here, in the acceptance criteria, in the fixture corpus and in the tool's diagnostics, and the glossary published with the build defines it. The vocabulary check reads those marks and holds the glossary to them.

## Design status

This document specifies the approved behaviour and initial defaults. Two builds implement it: a Python prototype that establishes the contract and the fixture corpus and stays in use as a differential oracle, and a production build in Rust with `pulldown-cmark` as the first parser candidate, subject to the verification gates below. The Rust sections state the production build's obligations; the behavioural contract binds both.

## Input and output contract

- **Entry references:** Accept one or more local document or document-plus-fragment *references*, resolved from the invocation working directory. An entry reference names a document whose frontmatter declares `prosiform`, and one naming a document that declares nothing fails with `E_TARGET_NOT_FOUND` before any source is read. An *entry reference* names the procedure to be carried out, not the routing document the caller read to find it; a routing document reaches the bundle only if something selected links to it.
- **Whole documents:** A reference without a fragment, or with an empty fragment, selects the full document body, including its *preamble*, subject to *frontmatter* stripping and the documented syntax transformations below.
- **Sections:** A nonempty fragment selects an eligible document-level heading and its subsections, ending before the next document-level heading of equal or higher level. A source heading is the only thing that names a *section*.
- **Recursive bundling:** Traverse supported Markdown links within selected content until every reachable local Markdown *target* has been resolved and included.
- **Continuous Markdown:** Emit each bundle as one Markdown document with one generated H1 per *group* and rewritten links resolving to internal destinations. Do not add per-section metadata envelopes or an enclosing code fence.
- **Generated headings:** A heading the bundle generates — a file heading, a merged group's heading, a member subsection heading and a variant heading alike — is emitted in *title case*: each word of the name is capitalized and the name's own structure is kept. The convention changes letters and not structure, so a file heading named by a path keeps its slashes and its hyphens and capitalizes each part of a hyphenated word, while a name a group derives from a declared group slug or a document stem is those words joined by spaces and is capitalized as it is derived. The convention covers what the compiler writes and nothing else: a heading an author wrote, a document title carried by a file heading included, is emitted as they spelled it, as is the link text a dispatch sub-section's heading carries, and a filesystem path a run names — a diagnostic's reference, a deferred link's destination — carries the spelling the filesystem holds.
- **Groups:** A group is one top-level division of the bundle. By default it is one *source document*, headed by its title, or by its normalized path relative to the invocation working directory with the Markdown extension removed where it carries none; a *grouping rule* declared in per-file metadata joins contributing documents under their declared *slug*. Emit each selected *region* once. Keep source order among selected content and required heading-only ancestors within a document's group, and within each contribution a document makes to a merged one.
- **Dependency order:** Arrange sources in *placement order*: each source is placed at the first reference that names it, reading the entry references in the order the invocation gives them and then the selected content of each placed source, in the order the sources were placed, each in source order. A group stands where its first source is placed, so the group carrying the parent leads, and the members within a group follow placement order. A merged group's sections follow the parent's own sections, then first appearance across its members; the variants within a section follow member order, the parent's first. An author sets the arrangement by the order links are written in: a preamble linking Rules and then Conventions places them, in that order, directly after the entry document's own sections. Placement reads the selected content the closure settles on, so the order the traversal discovers sources in decides nothing. Declaration conflicts are read in path order: each source's normalized path relative to the invocation working directory, compared lexically with forward-slash separators. Equal displayed member names and coinciding file headings take ordinals as any repeated heading does, and the run warns of them. A declaration admits what a source's links reach and decides no order, heading or name. Per-file grouping declarations determine where a section sits.
- **Entry identity:** Keep selected entry targets identifiable even when their content is subsumed by a larger included region.

## Parser and source-preserving edits

Use `pulldown-cmark` as the first semantic-parser candidate, behind a version-pinned source-range adapter. Retain original source bytes and apply edits to identified spans instead of regenerating the whole document.

Its `into_offset_iter()` exposes Markdown events paired with source ranges, and `reference_definitions()` exposes the reference-definition map ([pulldown-cmark parser API](https://docs.rs/pulldown-cmark/latest/pulldown_cmark/struct.Parser.html)). These APIs are a starting point, not a guarantee that every destination, definition, or nested edit already has the exact span required by this specification.

- **Parsing authority:** Let the parser identify headings, links, images, definitions, code examples, and HTML nodes, the last so they can be refused.
- **Source positions:** Build the source-range adapter around offset events and reference-definition data. Verify and retain the original spans needed for headings, link/image uses, and definitions; do not equate an enclosing event range with a precise destination span without *validation*.
- **Source model:** Derive block ancestry, eligible section boundaries, and link positions from the event stream while retaining canonical source identities and *provenance* ranges.
- **Coordinate mapping:** Map ranges in the parser's input view back to original UTF-8 bytes, including any BOM/frontmatter preprocessing, CRLF, tabs, escapes, and Unicode. Preserve original diagnostic coordinates.
- **Edits:** Apply validated non-overlapping edits. Handle constructs such as an image inside a link through a defined parent-edit strategy rather than overlapping replacements.
- **Untouched content:** Preserve original bytes and newline spelling, including code examples. Generated headings and separators may use LF; do not globally reformat sources.
- **Validation:** Reparse the candidate with the same explicit profile and check the declared source-to-output *invariants*.

The source-range adapter is an unproven implementation dependency, not an existing capability claim. It must pass fixtures for multiline references, reference-style images, tables, nested containers, escaped destinations, Unicode, and CRLF before this approach is considered validated; definition removal must cover unused as well as referenced definitions.

### Mandatory parser viability gates

Two additional acceptance gates apply before selecting a production parser version or publishing any bundle.

- **Complete definition occurrences:** Collect every reference-definition occurrence and its source range, separately from the winning-definition map used for resolution. Cover unused definitions, later duplicate definitions, case-fold-equivalent labels, multiline definitions, and supported container contexts. Preserve original first-definition resolution while removing all selected definition occurrences.
- **Observable reference-resolution suppression:** Detect when an internal parser resource limit prevents a reference lookup and fail with `E_PARSER_REFERENCE_LIMIT`, including the first affected source span when available. A successfully exhausted budget with no later suppressed lookup is not itself evidence that a reference was omitted.

A retained definition's span does not prove that duplicate occurrences can be enumerated. Similarly, an event stream that omits a suppressed reference cannot establish completeness merely by agreeing with a second parse.

If the public API is insufficient, require parser-aware occurrence collection, narrowly scoped parser instrumentation, an upstream change, or a different candidate. Any preflight used instead of a suppression signal must prove the relevant bound conservatively without confusing legitimate literal bracketed text with failed links.

Do not disable the parser's resource protections to satisfy these gates. A general broken-reference callback is not an adequate exhaustion signal unless the pinned implementation demonstrably invokes it for every limit-suppressed lookup.

Do not fall back to regex-only *rewriting* when an edit span is unavailable. Fail the unsupported case or explicitly revisit the parser/editing approach; do not silently switch to whole-document formatting or another authoritative parser.

Pin exact Rust dependency versions after the fixtures pass. Do not regenerate the whole document through an HTML or Markdown formatter; if the first parser candidate cannot satisfy the fixture gate, revisit the parser choice without weakening the behavioural contract.

## Markdown and source-heading profile

Use a versioned `skill-markdown-v4` profile based on CommonMark, with pipe tables and double-tilde strikethrough enabled and source task-list markers preserved. Configure parser options explicitly rather than enabling every available extension; `pulldown-cmark` supports option-controlled event parsing ([parser API](https://docs.rs/pulldown-cmark/latest/pulldown_cmark/struct.Parser.html)).

- **Core syntax:** Support ATX/Setext headings, paragraphs, lists, blockquotes, code spans and blocks, inline/reference links and images, thematic breaks, and ordinary CommonMark autolinks.
- **Task lists:** Preserve `[ ]`, `[x]`, and `[X]` markers without generating checkbox HTML. Recognize marker positions so reference definitions cannot turn them into links.
- **HTML:** Recognize HTML so it can be refused. Raw HTML in selected content fails with `E_RAW_HTML`; the bundle carries Markdown only.
- **Typography:** Disable smart quotes, typographic substitutions, and formatting cleanup.
- **Bare text:** Do not infer dependencies from ordinary paths in prose. Bare URLs may remain text; browser-specific rendering is outside the guaranteed profile.
- **Unsupported extensions:** Footnotes, wiki links, heading-attribute syntax, and include/transclusion directives are not v1 bundling features. Reject recognized unsupported dependency or section-naming constructs in selected content with `E_UNSUPPORTED_CONSTRUCT`, but do not guess every possible extension from ordinary prose.
- **File suffixes:** Recognize `.md` and `.markdown` case-insensitively for classification while preserving filesystem spelling and case semantics. An explicit entry with another suffix fails with `E_UNSUPPORTED_ENTRY_SUFFIX`.
- **Encoding:** Require valid UTF-8, and fail a source that is not with `E_INVALID_ENCODING` rather than decoding it with replacement characters. Tolerate and remove one leading UTF-8 BOM as source transport metadata.

Pin the parser configuration and definition-handling rules as part of the profile. Later extension changes must not silently change the interpretation of existing source.

### Source-heading resolution

Use a fixture-validated Rust adapter for GitHub-compatible source-heading slugs and duplicate tracking, with fresh state per complete source document. Select or implement the Rust slugging component against the compatibility fixtures; no specific slugger crate is selected yet.

Derive visible heading text from parser events: text/code content, link labels and decoded entities, excluding formatting delimiters, image alternative text and line breaks. An image contributes nothing but the space on either side of it, and a line break inside a Setext heading joins its lines with no separator. Enumerate headings in original source order, container-nested headings included. A heading's fragment is the slug its own visible text produces, and nothing numbers two headings of one source apart, so a fragment names a heading by what its author wrote rather than by how many similar headings precede it.

Test punctuation, repeated spaces, markup, Unicode, and headings whose slugs coincide. Two headings in one source producing the same slug are not numbered apart: a fragment requiring one of them fails with `E_AMBIGUOUS_SOURCE_HEADING`, and the author disambiguates by retitling. A source fragment must therefore identify one heading on its own, while a bundle destination is free to carry the renderer's *ordinal*, because the tool assigns it over a document it generated. Source-fragment lookup produces the slug a bundle destination is built from; GitHub documents formatting removal and duplicate numbering for its source heading links ([GitHub section-link rules](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)).

The pinned adapter and compatibility fixtures define the supported profile. Do not promise perfect parity with every future renderer change.

## CLI contract

Expose `pf` as the sole executable, with case-sensitive short operational flags and diagnostics on stderr. A run writes its bundles into a folder of its own, named for its entry with the `.bundles` suffix, under the folder `-o` names, the invocation working directory by default. Standard output carries no bundle: the guide and the help, version and code-listing responses use it. The package and product are named Prosiform. Do not add subcommands, remote fetching, watch mode, or persistent caching to the initial interface.

```text
pf [OPTIONS] REF [REF ...]
pf
```

| Option | Behavior |
| --- | --- |
| `-o DIR` | The folder the run's own folder is written into, under its automatic name with the `.bundles` suffix, relative to the invocation working directory; the invocation working directory when absent. The folder must exist. `-` names standard output, which carries no bundle, and is refused. A run folder holding any captured source is refused. |
| `-c` | Discover, bundle, and validate without emitting or publishing the bundle. |
| `-d text\|json` | Default human-readable diagnostics, or JSON Lines on stderr. |
| `-v` | Report tool version and profile identifier. |
| `-h` | Show usage, defaults, and exit-status meanings. |

One `--budget NAME=VALUE`, repeatable, names each resource ceiling, declared with its default and its counting rule at Resource limits.

`-c` accepts `-o DIR`, validating every bundle of the run without writing into that folder. Optional manifests and dependency explanations can be added later without changing the core invocation.

A command line the grammar above does not admit is refused with `E_INVALID_USAGE`: arguments naming no entry reference, an undeclared option (including `-r`, `-g`, `-f`, `-m` and `-x`), an invalid option value, a fragment-only entry, `-o -`, or a run folder holding any captured source. These failures exit 2. Declarations are source input and follow the diagnostics below. Check mode applies the same invocation and destination validation and publishes nothing.

### Conformance faults

Some clauses state behaviour no source tree can produce: a source changing between capture and publication, an internal error, a publication the run refuses after publication began. A fixture describing one has no tree to write, so a run reads `PROSIFORM_FAULT` from its environment and performs the fault it names. Its values are `source-changed`, `internal` and `cleanup-refused`. A run without the variable performs no fault, and a value outside the three is invalid usage rather than a silent pass. The mechanism is an environment variable rather than an option because a caller must not be able to ask for a fault, and a conformance setting that reached the option surface would state a capability the tool does not offer.

### Usage examples

```bash
# Each source declares `prosiform`, which is what admits it to a bundle.
pf work-planner/modes/align-mode.md
pf 'work-planner/modes/align-mode.md#prerequisites'

# Distinct selections share one bundle, in a folder of their joined name under -o.
pf -o build work-planner/SKILL.md \
  'work-planner/modes/align-mode.md#prerequisites'

# A referring document supplies context for a bare fragment only.
pf -f work-planner/modes/align-mode.md '#prerequisites'

# Full compilation and validation, without publication.
pf -c 'work-planner/modes/align-mode.md#prerequisites'
```

For these examples, `work-planner/modes/align-mode.md` declares the following frontmatter and contains an eligible `prerequisites` heading. `work-planner/SKILL.md` declares `prosiform` alone. The examples specify the file-owned invocation contract; runtime conformance must execute them against an identified candidate and specimen tree.

```yaml
---
prosiform:
  group: modes
  group-depth: 2
---
```

### Guide

`pf` with no arguments prints the *guide* to standard output and exits `0`: what an agent needs before it compiles anything. It states the compile step, `pf -o <folder> <destination>` run from the skill's directory, which holds `SKILL.md`, with a non-zero exit stopping the run and reporting its diagnostics; that a link whose text opens with `↳` names an inline target, which is compiled, read whole and followed; and that a bundle opening with a Prosiform section is followed from there. The guide is the build's own text, so a skill's bootstrap is one instruction: run `pf` and follow it. No option prints it, and `-h` states that a bare `pf` does.

### Automatic output names

Count distinct explicit selections after canonical file and fragment resolution. Repeated equivalent references count once; absent and empty fragments share whole-document identity. Distinct sections of one file, or a whole document and one of its sections, remain distinct entries even when coverage consolidates them. A *preset* may hold an `exclude` naming sections its declaring file withholds, and what it removes is settled before consolidation, so no other selection restores it.

For each selection, take its path relative to the invocation working directory, remove the recognized Markdown extension, preserve spelling and replace each path separator with `_`. For a section, append `__` and its resolved source fragment identifier. Join the selections' names with `+` in the order the command line first names each: the joined name with `.bundles` appended names the run's folder under the output folder, and with `.bundle.md` appended names the entry's bundle in it. The suffix keeps the run's folder apart from an author's folder named like the entry, which a run neither writes into nor replaces. Each dispatched target's bundle in that folder is named by its own selection the same way. A fragment-only entry derives its filename from the file supplied by `-f`. Roots and group names never rename an entry's output.

| Entry, from the working directory | Automatic filename |
| --- | --- |
| `work-planner/modes/align-mode.md`, declaring `prosiform` | `work-planner_modes_align-mode.bundle.md` |
| Same file, fragment `prerequisites` | `work-planner_modes_align-mode__prerequisites.bundle.md` |
| `work-planner/SKILL.md`, declaring `prosiform` | `work-planner_SKILL.bundle.md` |
| `work-planner/artifacts/epic.markdown` | `work-planner_artifacts_epic.bundle.md` |
| `../library/guide.md` | `.._library_guide.bundle.md` |
| Equivalent references `guide.md` and `./guide.md#`, both declaring | `guide.bundle.md` |
| `guide.md#one` and `guide.md#two` | `guide__one+guide__two.bundle.md` |
| `rules.md`, then `guide.md#run` | `rules+guide__run.bundle.md` |

Retain parent segments when an entry lies above the working directory, then flatten their separators: they become filename text, never output traversal. Literal underscores remain literal. Recommend hyphens in authored file and directory names to reduce ambiguity; this does not guarantee collision freedom for arbitrary paths or case-insensitive filesystems. No encoding, hashing, shortening or collision registry is applied to automatic names. Two bundles of one run deriving one name — `a/b.md` and `a_b.md`, or a dispatched target named like the joined entry — are refused with `E_PUBLICATION_FAILED`, naming both selections, before any bundle is written, `-c` included. So is a run folder or bundle name longer than the output folder's filesystem allows, naming the selection it is derived for. Filesystem name or length failures use `E_PUBLICATION_FAILED`. Every run folder takes the captured-source check, and every bundle candidate validation and the folder's atomic replacement, whichever output folder holds it.

## Explicitly linked source structure

Common rules, file-level prerequisites, and shared SKILL.md instructions will be refactored into addressable sections. Operations must link to the sections that govern them, so the tool can obtain the required context through explicit links.

- **Generic bundling:** Do not infer prerequisite semantics from file names or section names. Do not automatically import all of SKILL.md or ancestor body content; a heading-only *structural ancestor* supplies structure, not additional governing instructions.
- **Explicit dependencies:** A path-bearing reference naming a local Markdown document whose frontmatter declares `prosiform` is part of the recursive dependency graph unless its author defers it, and one naming a document that declares nothing is text the bundle carries. The declaration is what the target states about itself: a document a bundle must carry declares, and one it only names does not. Fragment-only links identify the source itself. A *deferral* states that the material is reached in a run of its own rather than in this one.
- **Reading versus execution:** Inclusion makes material available; it does not authorize executing every included procedure. Execution verbs and call boundaries remain part of the authored instructions.

## Section extraction and output hierarchy

Only headings that are direct children of the document are selectable section roots in v1. Both ATX and Setext headings are eligible when recognized by the configured parser; heading-like text in code is not.

- **Boundary:** Include subsequent document-level blocks until the next document-level heading of equal or higher level.
- **Subsections:** Include deeper document-level headings and their content.
- **Containers:** Headings inside lists, blockquotes, or other containers do not terminate a document-level section.
- **Nested target:** A fragment targeting a container-nested heading fails with `E_NESTED_SECTION_TARGET`.
- **Enclosing inclusion:** Container-nested headings may be retained when their whole document or enclosing eligible section is selected. Shift their heading levels along with other emitted source headings, while preserving the containing list/quote and other non-heading content.
- **Source heading index:** Index every source heading the profile recognizes, container-nested ones included. Extraction eligibility must not change another heading's original fragment.

### File-scoped hierarchy

Emit exactly one document-level H1 for each contributing source file. Its text is the document's title: the source's first heading, where that heading is the document's only H1 and sits at the document level. A document carrying no title is headed by its normalized path relative to the invocation working directory with the Markdown extension removed, in *title case*. Escape the heading as literal text so punctuation in a title or a path cannot create links, images, or inline HTML.

All content from that source belongs beneath its file heading. The output has no additional master heading above these file groups, and a boundary names nothing in it. Distinct documents whose file headings coincide — two sharing a title, or untitled documents whose paths differ only by Markdown extension or capitalization — keep both headings, which take distinct destinations as any repeated bundled heading does: the later carries the renderer's *ordinal*. A reader tells such headings apart only by where each stands, so the run publishes the bundle and warns with `W_COINCIDENT_HEADING`. The parent's title is its file heading where the bundle opens on it.

- **Absorbed title:** The file heading absorbs the document's title. An absorbed title is not emitted and contributes no destination segment, because the file heading carries its text. A reference to it resolves to the file heading's own destination, so a document's self-reference to its title reaches the heading a reader sees carrying that text. A title is absorbed only where the group emits its section; where it does not, the file heading still carries the title's text and the group shifts.
- **Group shift:** Every emitted source heading in a file group moves down exactly one level: H1 becomes H2, H2 becomes H3, and so on. A group whose title was absorbed keeps its source levels, the file heading having taken the level the shift makes room for. Preserve visible heading text and relative depth; do not renormalize selected roots independently.
- **Heading syntax:** Shift ATX headings by editing their heading syntax. Convert Setext headings to equivalent ATX headings when required, preserving their visible text and inline semantics, including multiline source forms.
- **Containers:** Apply the same level shift to real headings within retained containers without removing or changing the container structure. Heading-like text inside code remains untouched.
- **Preamble:** A selected document's preamble appears after its file heading and before its first retained source heading.
- **Source order:** Within each file group, emit selected regions and structural ancestors in their original source order.
- **Depth overflow:** Fail with `E_HEADING_DEPTH_OVERFLOW` before publication if any emitted source heading or structural ancestor would require a level beyond H6. Do not flatten it, clamp its level, or emit H7-like text as if it were a heading.

The hierarchy guarantee is the original selected source outline beneath one additional file level. File headings isolate source documents, while destinations are assigned over the bundle as a whole, so two files contributing a section of the same name stay distinguishable.

### Grouping

A group is the unit the bundle is organized into. A source without conversion fields keeps its individual file group. A source declaring the paired fields in [Conversion metadata](#conversion-metadata) joins the named group at its declared source heading depth.

- **Group membership:** Membership is explicit and independent of directories. Only documents contributing selected content or its required generated identity to the *closure* join a group. A declaration discovers no files; unannotated siblings keep individual groups. Group identity is the exact declared string, with no trimming or case folding, and is distinct from an individual file group's identity even when their displayed headings coincide.
- **Consistent depth:** All contributing members of one group declare the same depth. Sort declarations by path order; compare the first member with the first later member whose depth differs. Fail with `E_GROUP_DEPTH_CONFLICT`, identifying the group and both declarations at their depth values. Deferred-only targets participate in local metadata validation, but contribute no membership or cross-file conflict.
- **Group structure:** A group emits one H1 carrying its slug, or the parent's title under the parent arrangement, then one H2 for each distinct source heading text at its depth, each holding every *member* document's contribution. A source heading at the grouping depth becomes that H2; the level below becomes H3, and so on.
- **Verbatim names:** A merged heading keeps its source text. Nothing is prefixed, qualified or renamed where the text occurs once in its group.
- **Document-keyed sections:** A merged section contributed by more than one document splits into *variants*: one variant heading per contributor, with that document's text, list items and subheadings beneath it. Each item stays with its document throughout the section. Contributions may contain body text, subheadings or the section heading alone. A section with one contributing document retains that document's arrangement.
- **Variants by document:** Where two or more documents contribute one heading text at the grouping depth, that text is emitted once and each document's content hangs beneath its variant heading. Each member's name is measured once against every member of the group: the shortest distinguishing run of its path, in title case, after dropping shared leading segments and a trailing word the group's heading already states. Qualification compares the final displayed names after title casing, separator normalization and removal of the group word, retaining further path segments until those names distinguish the members. If every available segment is present and removing the group word still joins names, the complete names retain that word. The same name serves its overview subsection and every variant, including sections contributed by only a subset of the group. Each document's grouping-depth heading is replaced by the shared one, and its content shifts one level to sit under its variant heading.
- **Residual ambiguity:** If complete member paths still yield indistinguishable displayed names — names one text but for capitalization, such as members whose paths differ only by Markdown extension — the members keep those names, each takes a distinct destination by the renderer's ordinal, and the run publishes the bundle and warns with `W_COINCIDENT_HEADING`, locating each member at its group declaration. Qualification separates documents, not headings within one. Two headings of one document colliding in one group is the source ambiguity the heading rules already refuse. Other repeated headings, such as a generated group heading matching a section name elsewhere, take the renderer's ordinal as any repeat does.
- **Group naming:** A group's heading is its declared slug in title case, so `artifacts` is emitted as `Artifacts`. Heading escaping, anchor allocation and member-name qualification apply even when that slug names no directory.
- **Document content above the grouping depth:** A group carries each member's selected content above the grouping depth — its preamble, and the body of any section shallower than that depth with its outline beneath — under one subsection naming that document. That subsection's heading is the shortest run of the member's path which distinguishes it from the group's other members, in title case, measured after dropping the leading segments they all share, less a trailing word the group's own heading already states: `artifacts/epic-issue-body.md` contributes `Epic Issue Body` under `Artifacts`, and `guides/alpha/notes.md` beside `guides/beta/notes.md` contributes `Alpha Notes`. That is the run a variant heading is shortened to, so one bundle states a member's name one way wherever a reader meets it. A member's own H1 is absorbed by that subsection heading when its slug equals the stem, as a file heading absorbs the title it carries. That heading is where a whole-document reference to the member resolves, and where a reference to the title it absorbed resolves with it. A preamble reaches the bundle only through a whole-document selection, since it belongs to no section.
- **A heading for every member:** A member takes that subsection where it carries selected content above the grouping depth, where the heading absorbs its own H1, and where the arrangement emits nothing else from it at all — the last two cases emitting the heading alone — so every member the group merges is named by a heading the bundle carries and a title is absorbed only into a heading the bundle emits. A member whose selected content all sits at the grouping depth takes no subsection: the merged sections it contributes to name it, and a whole-document reference to it resolves to the first heading the group emits from it that no other member shares — the variant heading naming that document where its contribution is pooled with another member's, and the merged heading itself where the text it contributes occurs once in the group. No two members of one group therefore reach one destination, and a reference the run resolves into a merged group names a destination the bundle has, whatever the member contributes.
- **The overview section:** The member subsections sit beneath an `Overview` section of the group where the group also emits merged sections, so a member's preamble is read as that member's rather than as one more of the group's own sections. Where the group emits no merged section the subsections are its whole structure and sit directly beneath the group's heading, which is the arrangement a caller asking for a folder as a section with its documents beneath reaches. The *overview* section is the group's, not a member's: it carries no content of its own and holds the subsections in member order.
- **The parent arrangement:** Where the parent is a member of a merged group, the sections it carries at the grouping depth lead the group's merged sections in the parent's order, its own contribution first where several members share one, and a section only another member contributes follows them. Where the parent's selection carries its title above the grouping depth, that title opens the group as its H1 in place of the group's slug, and the parent's preamble and any other content it carries above that depth follow at the levels the author wrote; the parent takes no subsection, and the other members' subsections follow the merged sections, beneath `Overview` where the group emits merged sections and otherwise directly beneath the title. Where the selection carries no such title — an untitled document, a section selected, or a title at the grouping depth — the group opens on its own heading and the overview precedes the merged sections.
- **Merged section references:** A reference to a source heading at the grouping depth resolves to that document's variant heading where the name carries variants, and to the merged heading itself where the name occurs once. A reference reaches the document it named under every arrangement.

Grouping changes how a bundle is arranged, not what it contains. The closure, the *consolidation* and the selected content are the same whichever grouping is asked for, and so are the validation invariants, which are stated over groups rather than over source files so that they hold under every arrangement.

### Heading-only structural ancestors

For each selected section, retain the chain of eligible ancestor headings needed to preserve its original outline. Emit only those ancestors' headings, not their body text, unselected siblings, or other descendants.

Structural ancestry is generated structural content, not dependency inclusion:

- **Heading text:** Render a structural ancestor's original visible title as escaped text, without live source links, images, or HTML. Do not traverse references from an ancestor-only heading or import its body.
- **Provenance:** Record structural ancestor headings separately from selected content, retaining their canonical source-heading identities and original levels for validation.
- **Deduplication:** Emit each structural ancestor once. If dependency discovery later selects that ancestor as content, replace its structural ancestor with the normally transformed source heading and selected body rather than adding a second copy.
- **Named titles:** A source heading the generated file heading already names is not emitted as a structural ancestor, whether or not its section was selected. The file heading stands in its place in the outline, so emitting both publishes two headings a reader cannot tell apart.
- **Targets:** A structural ancestor is not a substitute for selecting the corresponding source section. A real link to that ancestor expands closure to include the section normally, replacing the structural ancestor with the transformed heading and its selected body; a displayed title does not satisfy a reference.
- **Depth:** Shift structural ancestor levels by their group's shift. Do not compress skipped levels or invent missing headings that did not exist in the source.

For example, selecting `Alpha` and `Detail` from a source whose original outline is `## Alpha`, `## Beta`, `### Detail` requires a heading-only `Beta` in the bundle:

```markdown
# guide

### Alpha

Selected Alpha content.

### Beta

#### Detail

Selected Detail content.
```

`Beta`'s body is not included unless it is independently selected or reached as a dependency. Structural ancestry preserves the parent-child relationship without importing unlinked prerequisites.

### Block boundaries

Insert blank-line separation between maximal emitted regions and reparse the candidate. Reject boundaries that merge or absorb content into unintended code fences, lists, quotes, HTML blocks, or other non-heading containers.

Do not silently close fences or repair code examples. Report unsafe boundaries with `E_UNSAFE_BUNDLE_BOUNDARY`, identifying the source regions and conflicting output boundary.

## Bundle destinations

Resolve fragments against the original complete source document before mapping them, so a destination follows from source identity rather than from traversal position or discovery order. A destination is then the fragment a renderer generates for the bundled heading it names: that heading's slug under the profile's slugging rules, carrying the ordinal the renderer appends when two bundled headings share a slug.

```text
#{heading-slug}        a bundled heading whose slug is unique in the bundle
#{heading-slug}-{n}    the heading that is the (n+1)th to carry that slug
```

- **One document:** The bundle is one document, so a destination is scoped to the whole bundle rather than to a file group. A section whose slug is unique in the bundle needs no qualification, and a reference from one file group to another is spelled the same way as a reference within one.
- **Ordinal assignment:** Walk the emitted headings in bundle order — file headings, structural ancestors, selected source headings and the headings a retained container carries alike, because a renderer indexes every heading the bundle emits and numbers the rest from a count that holds them all. The first heading to carry a slug takes that slug; each later one takes the slug and its ordinal, counting from one and passing over an ordinal something already carries, so a heading whose own text ends in one does not collide with it. This is the renderer's own rule, reproduced so the two agree.
- **Document destinations:** A whole-document reference resolves to the destination of that file's heading. The presence of a file heading does not mean the whole document was included, and a whole-document reference still requires full-body inclusion under the established transformation rules.
- **Internal links:** Rewrite each compiled link to the destination of the target it resolved to, using the same map that produced it, whether the link names another file or a fragment of its own. A reference this run compiled is a reference the bundle carries, so every one of them has a destination; a reference naming a document that declares nothing is emitted as the author wrote it, a deferred one carries an invocation-working-directory-relative destination and a dispatched one its dispatch sub-section's destination, under the link classification rules, each without its mark.
- **Visible headings:** Preserve selected source heading text while shifting levels by the group's shift. Nothing is inserted at a destination; the heading and its position in the outline are what the destination names.
- **Uniqueness:** Each destination occurs once in the bundle and each rewritten link resolves to exactly one of them. The ordinal makes this true by construction and validation establishes it, rather than leaving it to the chance that no two headings coincide.

### Resolvable where the bundle is read

A destination is the fragment the renderer itself would generate, so every internal link resolves: in a Markdown renderer, in an editor preview, and for an agent reading the document whole. The bundle needs no anchor elements and no identifiers to achieve this, because the headings it already emits are what the renderer indexes.

An ordinal is safe here in a way it is not in a source document. In a source, an edit elsewhere changes how many similar headings precede a target, so a stored link silently repoints. A bundle is generated whole in one pass and validated against the map that produced it, so every ordinal it carries is assigned and checked in the same run. A bundle is not a source: it is not hand-edited, and no link into one outlives the run that wrote it.

### Markdown-only output

The bundle contains Markdown and nothing else. No anchor elements, no identifiers and no other markup are emitted at a destination, so a destination is a name for a place in the document rather than an element in it.

A source heading is the only thing that names a section. There is no supported syntax for attaching a second name to one, so both a source fragment and a bundle destination resolve against heading slugs alone, the first against one document's headings and the second against the bundle's.

### Source markup policy

Raw HTML is outside the profile. A source carrying it in selected content fails rather than copying it into the bundle, which keeps the output free of identifiers and elements the tool neither created nor tracks.

A source heading is the only thing that names a section. There is no supported syntax for attaching a second name to one, so a fragment resolves against the source-heading slugs alone.

## Source-local reference interpretation

Parse each source independently after frontmatter recognition and before selecting output regions. Resolve reference-style links and images using only that source's definition environment, including definitions outside the selected region.

1. Convert resolved reference-style uses in selected content to inline links or images.
2. Preserve visible link text, image alternative content, and optional titles with the necessary Markdown escaping.
3. Rewrite local Markdown destinations to bundle destinations; emit every other destination as authored.
4. Remove all original link-reference definition nodes from emitted content, including unused definitions.
5. Preserve unresolved bracketed text as literal text; do not infer a *dependency* from text the source parser did not recognize as a link.
6. Leave examples inside code spans and code blocks unchanged.

For example, a literal `[runner]` in one source must remain literal even if another source defines `[runner]: tools.md#run`. Convert the latter source's resolved use to an inline link and omit its definition from the bundle.

Definition removal is an allowed non-rendered-syntax transformation. Fail if the parser/editing strategy cannot preserve these distinctions; footnotes and other document-global definition systems require separately declared support.

## Compile before publishing

Bundling is a compile-and-validate process rather than streaming concatenation. No success output is published until the complete candidate has been constructed and validated.

1. Capture the invocation working directory and normalize explicit entry references for bounded bootstrap access.
2. Capture each distinct canonical source once under byte and parsing limits, retain its identity, content hash and immutable per-source settings, derive its boundary, and exclude leading frontmatter from bundled content.
3. Index source headings, links, definitions, and eligible section boundaries.
4. Discover the recursive dependency graph and expand included source coverage to a fixed point.
5. Remove each document's excluded sections, then consolidate selections, group them by source file, and derive required heading-only ancestors. Check shifted heading depths and assign each emitted heading its destination in bundle order, without treating structural ancestors as new dependencies.
6. Apply source-local reference conversions, rewrite destinations and heading syntax, and construct the candidate with one file heading per source.
7. Reparse in candidate-validation mode and compare with selected source constructs, including target integrity, unintended new references, coverage, namespaces, and block boundaries. Do not reload the candidate through source-input validation.
8. Recheck every source against its captured content hash and canonical path identity; fail if a source has changed, disappeared, or resolved elsewhere.
9. Publish the validated document; otherwise fail with actionable diagnostics.

**Expanding coverage:** If a later reference includes an ancestor section or whole document, replace narrower duplicate selections with the larger region. Traverse dependencies in newly included content before declaring compilation complete.

Keep parsed-file caching separate from included-region tracking. Reach a fixed point before final emission, and retain mappings from all selected targets to their consolidated destinations.

## Self-reference and ancestor-reference behavior

A reference back to content the bundle already carries resolves to that content's destination, whether it names an ancestor of the node it sits in or that node itself. Identity is evaluated using source-section identity, not merely file identity or the scope of the entry argument.

- **Direct self-reference:** A link from section A to the same canonical section A resolves to A's own destination, like any other reference the bundle carries. The content is in the bundle either way, so the link names a place that exists and nothing is expanded twice.
- **Ancestor reference:** During traversal A → B → A, B's reference to A becomes an internal link to the existing A destination. Do not expand or duplicate A.
- **Shared dependency:** A → C and B → C include C once; both links resolve to its destination.
- **Different section in the same file:** A link to a distinct section is not a direct self-reference solely because the file is the same.
- **Equivalent references:** Determine identity after canonical path and fragment resolution, rather than comparing the literal link strings.
- **Link position:** A reference resolves by its target alone, wherever in the source it sits. A link in a heading's inline content, in a nested container, or in the content above the first eligible heading names the same destination as the same link written anywhere else in that document.
- **Whole-document selection:** Selecting `guide.md` does not make its links to `guide.md#section` self-references. A document node and its heading-section nodes are distinct identities.
- **Preamble content:** Content before the first eligible heading is the document node's own, so a whole-document selection carries it and a reference naming that document resolves to the document's destination.

A destination belongs to the target a reference resolves to rather than to the region the reference sits in, so consolidating a child section into a larger region leaves every destination the bundle carries as it was.

## Frontmatter policy

Read leading source frontmatter from every normally opened source, including whole-document entries and deferred targets opened for destination validation. Recognize its boundaries by deterministic delimiter scanning, parse its YAML safely, and exclude it from the Markdown body.

1. Accept and remove one optional leading UTF-8 BOM.
2. If the first physical line after the BOM is exactly `---`, excluding its LF or CRLF terminator, treat it as the frontmatter opener.
3. Close at the next physical line exactly equal to `---` or `...`, excluding its terminator.
4. Strip the opening line, metadata content, closing line, and the closing line's terminator when present.
5. Preserve subsequent body content, including following blank lines.
6. Fail with `E_UNTERMINATED_FRONTMATTER` when a recognized opener lacks a closing delimiter.

Do not recognize indented delimiters, trailing spaces on delimiters, TOML `+++`, or JSON metadata as v1 frontmatter. A document intended to begin with a literal horizontal rule must use another spelling, such as `***`, rather than the reserved leading `---`.

A BOM is allowed before the opener, but an actual leading blank line means the following `---` is body content. Keep original source coordinates for diagnostics, and do not strip YAML examples in code blocks or non-leading thematic breaks.

Parse the recognized block from the same captured bytes used for source identity and hashing. Count its complete bytes toward input-size limits. Frontmatter supplies no Markdown headings, links, reference definitions or rendered content and is never executed. Preserve the body's mapping to original physical source coordinates.

### Conversion metadata

The top-level `prosiform` mapping carries source-owned settings. This is a Prosiform frontmatter extension; strict Agent Skills schema compatibility is not required:

```yaml
---
name: artifact-rules
description: Rules for authoring artifacts.
prosiform:
  group: artifacts
  group-depth: 2
---
```

Ordinary Markdown needs neither `name`, `description`, nor a `SKILL.md` filename. Other top-level skill fields have no conversion meaning and impose no additional schema beyond the safe YAML rules below.

| Field | Accepted value | Meaning |
| --- | --- | --- |
| `prosiform.group` | A single-line printable string with at least one non-whitespace character, containing neither `:` nor `/`. | Exact identity of the group this source joins. |
| `prosiform.group-depth` | YAML Core integer from 1 through 6, excluding booleans, floats and strings. | Source heading depth for this member's merged sections. |

Group and group-depth are present together or absent together. Absent grouping fields leave the source in its individual file group. Absent frontmatter, an empty block or an absent or empty `prosiform` mapping declares nothing, so the document is text wherever a link names it. A present `prosiform` must be a mapping with string keys; null, scalar and sequence values fail. Its only keys are `group`, `group-depth` and a *preset* name; unknown keys fail. Unrelated frontmatter fields, including `metadata`, have no conversion meaning. No schema version, inherited profile or command argument string is interpreted.

- **The admitted keys:** `group`, `group-depth` and a *preset* name are the keys the `prosiform` mapping admits, and a key outside them fails with `E_INVALID_CONVERSION_METADATA` wherever it sits in the mapping. A preset's value is a mapping; a key whose value is anything else is refused. There is no top-level parameter form, so a file-wide setting cannot vary with what a caller selected.
- **A bundle compilation is the unit a preset governs:** One entry reference and the closure it reaches. A preset is the whole setting of the compilation that selects it and covers every document that compilation reaches, so a document reached as a dependency is compiled under the entry's preset rather than its own.
- **`profile` and `preset` are two terms:** `skill-markdown-v4` is the profile, the grammar a run implements and reports with `-v`. A preset is the per-compilation setting above, named by the section a compilation's entry reference selects.
- **A preset is selected by heading text:** A preset applies where the section the compilation's entry reference names has a heading whose text equals the preset's name. The resolved text is matched rather than the authored fragment because the two live in different documents and a fragment may be percent-escaped.
- **Exclusion:** A preset may hold an `exclude` of sections, each removed from the contribution of the file that declares the preset. The scope is the declaring file, so no entry names a document, and there is no top-level form: a list is a preset's shape. An exclusion names what a fragment names — a document-level heading and everything beneath it — and an optional level tells two headings of one name apart. A link written inside an excluded section is no dependency, so its target is never read. An exclusion holding content another reference selected fails with `E_EXCLUDED_CONTENT`, and one withholding every region its file holds fails with `E_EXCLUDED_ENTRY`. An exclusion naming a heading the file does not carry is silent, because a preset is shared across documents that vary, and a deferral is not carried across.
- **The preset warnings:** `W_PRESET_UNUSED` names a preset no compilation selected. A preset reached only through a deferral is not unused, and a document's own preset is inert where that document was reached as a dependency.
- **`root` is refused:** `prosiform.root` stated a confinement boundary for a source's outgoing links. A document's boundary is derived from the links it writes, so the field states nothing a run reads; a declaration carrying it fails with `E_INVALID_CONVERSION_METADATA` naming the field and the remedy, because a declaration that silently does nothing is read as a declaration that took effect.
- **An empty block declares:** Presence is a fact of its own. An empty `prosiform` mapping qualifies its document and carries no conversion settings; a document with no mapping at all is text.
- **Unrelated fields have no conversion meaning:** A top-level field the conversion contract does not name, `metadata` among them, states nothing about a run and is neither read nor published, whatever it holds.

- **YAML grammar:** Accept one YAML 1.2 document using the Core schema. An empty or comments-only block is absent metadata; an explicit null document root fails. A nonempty document root must be a mapping. Reject duplicate keys in every mapping, custom tags, aliases and merge keys (`<<`), including in unrelated fields. Document-root and `prosiform` mapping keys must be strings. Elsewhere, safe Core keys and nested collections remain valid; duplicate keys use YAML node equality (tag and canonical value), so boolean and integer keys remain distinct. Printable group characters follow YAML printable characters except line breaks and control characters; spaces within and around a nonblank name are significant. Malformed YAML fails even without conversion keys.
- **Bounded parsing:** Use a pinned established safe YAML parser, with documented scalar typing, duplicate detection, source marks and resource behavior verified by fixtures. Enforce raw source-byte limits before decoding and YAML collection nesting before constructing nested values. For `nesting`, a root mapping or sequence has depth 1, each contained mapping or sequence adds 1, and scalars add 0. YAML depth and Markdown container depth are measured independently against the same limit; exceeding either fails with `E_RESOURCE_LIMIT`. Do not expand aliases or construct custom tagged objects.
- **Source ownership:** Decode one immutable conversion value, including the declaration its boundary is derived from, per captured canonical source. Direct entries, fragment-only entries, ordinary links and transitive links all use that source's own settings for its content and outgoing references. A fragment retains that value even when its frontmatter lies outside the selected region. A shared source reached through different parents has the same declaration and the same derived boundary. Repeated reachability, overlapping fragments and ordinary cycles retain one capture and the existing selection union.
- **Selection boundary:** Validate syntax and local fields whenever the normal reader opens a source. Aggregate group declarations only after closure selection. Deferred-only targets contribute no content or membership; later activation uses their own settings. External and non-Markdown references retain their classification without being opened. A local Markdown document that declares nothing is text, so it is probed for its frontmatter and no further byte of it is read. Candidate validation uses the same per-source grouping decisions as rendering.
- **Operational interface:** Entries, output destination, diagnostics, check mode and resource budgets are invocation parameters. Structural settings come only from source metadata. The unsupported `-r` and `-g` options receive invalid CLI usage, exit 2.

### Metadata failures

Metadata input failures exit 1, fail check mode, publish no bundle, and preserve an existing output file. Text and JSON diagnostics identify the failing field and original physical source location. A YAML syntax error points to the parser's marked token; an invalid key points to that key; a value type or value error points to that value; a missing paired field points to the present field; an unknown reserved field points to its key. Duplicate keys identify both occurrences. Collection-depth errors point to the collection that exceeds the limit.

| Diagnostic | Defect |
| --- | --- |
| `E_INVALID_FRONTMATTER` | Invalid YAML, nonmapping or explicit-null root, duplicate keys, non-string root keys, custom tags, aliases or merge keys. |
| `E_INVALID_CONVERSION_METADATA` | Invalid `prosiform` mapping, non-string keys, an absent paired grouping field, unknown setting, the refused `root`, invalid group slug, or invalid integer depth. |
| `E_GROUP_DEPTH_CONFLICT` | Contributing sources declare different depths for the same exact group identity. |
| `E_SOURCE_SYMLINK` | A bootstrap source or dependency access traverses a symlink forbidden by the no-follow policy. |
| `E_SOURCE_OUTSIDE_ROOT` | A path form no grammar admits: a drive path, an absolute path, or one normalising above the invocation working directory. |
| `E_TARGET_NOT_FOUND` | A permitted Markdown target is missing or is not a regular source file, or its requested heading is missing. |
| `E_SOURCE_ACCESS` | A source cannot be opened or read due to an access or filesystem error other than the specific missing, symlink or confinement defects above. |
| `E_SOURCE_CHANGED` | Captured source bytes, identity or derived boundary change or disappear before publication. |

`E_ROOT_NOT_FOUND` is retired with the `root` field it reported. Conformance compares the codes the contract declares against the codes a build reports for itself, so the retirement is stated here rather than left as a gap between the two lists.

Unterminated recognized blocks use `E_UNTERMINATED_FRONTMATTER`; byte and nesting limits use `E_RESOURCE_LIMIT`. Metadata diagnostics carry a JSON `location` object with `file`, `line` and `column`: `file` is the canonical source path relative to the invocation working directory, retaining parent segments when needed. Inclusion chains use the same unambiguous coordinate system. Lines are one-based physical lines, and columns are one-based Unicode code-point positions, counting a tab and a leading BOM as one position each. CRLF is one line ending. For a group conflict, the primary location is the first declaration in path order and `related` is an array with the other declaration's `file`, `line`, `column` and `message`. Each message names the field, group and declared depth. Duplicate-key diagnostics likewise carry the first occurrence as a related location and the duplicate as primary. Omit `related` when there is no related location. Text diagnostics render the same coordinates and both locations where present. A bootstrap access failure identifies its positional reference when no physical location is available. Ordering and messages are independent of discovery order.

## Link classification and resource handling

A reference is a dependency when its author has not withheld it and it either names a fragment in its captured source or carries no scheme and no authority and resolves to a local Markdown document whose leading frontmatter declares `prosiform`. Fragment-only references retain their source identity. Other references are text the bundle carries under the rules below. What a document contributes is a property of that document rather than of whichever source linked it, so one document reached by two sources is one answer and needs no agreement between them. An operator states how material is compiled: a *deferral* states that it is compiled by a later run, a *dispatch operator* that a sub-agent compiles it, and a *parallel dispatch mark* that a sub-agent compiles it together with the other parallel dispatches of its section.

The tool guarantees internal resolution for a dependency and claims nothing about anything else.

A declaration states what a document is worth to a bundle, and an operator states how its material is compiled. A document's *boundary* is the deepest directory holding every local Markdown path its own links name, normalised from that document's directory; a document naming none has its own directory. The boundary admits every authored link, because it is derived from them: what still confines a run is the invocation working directory, from which an entry reference and every path a diagnostic names are resolved. A *substitution mapping* states what a reference names instead: it is read before classification, closure and rewriting, and it is applied to the identity a reference normalized to. Classification, closure and rewriting take the one answer it gives, so no stage resolves an identity the mapping redirected.

- **The substitution mapping:** A *preset* maps one reference to another, so a run builds against stand-in material without the tree under test being edited. It is stated once per pairing in the preset's `mock` entry, each side a reference read from the declaring file's directory by the grammar every other reference is read by: percent decoding, control-character refusal, `..` normalization and the Markdown-suffix test are unchanged. A key is the identity a reference normalizes to, so two spellings of one path name one key, and a key carrying a fragment redirects that section alone and takes precedence over a key naming the whole document, which covers the document and every fragment of it. Both sides resolve from the directory of the file declaring the preset, so a stand-in kept beside it is reachable. A compilation selecting no preset substitutes nothing. Every reference a compilation reaches is redirected — a positional entry and a compiled, deferred, dispatched or parallel-dispatched target alike. The *substitute* is the target outright: its title, its group and depth, its own declaration and its own links are the ones the run uses, and the bundle reads as if the author had written the substitute's path in the link. A substitute is a source in every respect, so its own links are matched against the mapping as any document's are, and a substitute that is also a key is read from disk rather than followed again. Two entries whose keys normalize to one identity, an entry whose key and value normalize to one identity, a key carrying no document and a value naming no Markdown document are invalid usage. A key naming a document that does not exist is not refused: the reference is redirected before any source is read, which is what makes an artifact under authoring testable before it lands. The mapping is read wherever a reference is resolved, so a check run applies it and reports each substitution as a publishing run does. A successful run states each redirected target, naming the identity the reference would have resolved to and the substitute, and states each key no reference named; an unmatched key warns and publishes rather than failing.
- **Local Markdown document links:** Resolve, recursively bundle, and rewrite to bundle destinations. Resolve each path-bearing reference from the directory of the originating source, independent of the source that discovered it, and compile it when its target's frontmatter declares `prosiform`. The substitution mapping decides the identity first, so a substitute is compiled whether or not the path it was named for sits beside the writing source.
- **The deferral mark:** A link whose text opens with `¬` followed by at least one space, as in `[¬ Record Epic Delivery](epic-issue-body.md#record-epic-delivery)`, is not compiled by this run. A `¬` with no space after it opens no operator: `[¬Record](record.md)` is an ordinary link, compiled like any other, its mark kept as text. The character is ordinary text to the profile, so deferring adds no construct the grammar must recognize and a renderer that knows nothing of this tool displays the link. The mark is authoring syntax rather than content: the bundle carries the link's text with the mark and the blanks following it removed, because the destination the link publishes already states that the material is a run of its own.
- **The dispatch operator:** A link whose text opens with `⇉` followed by at least one space, as in `[⇉ the shared rules](rules.md)`, states that a sub-agent follows its material. It withholds what a deferral withholds from the bundle carrying the link — the target contributes no content, adds no dependency through the link and no group membership — and its target is required to exist and to name the heading it names, because a dispatch an agent performs is one that can succeed. The run compiles the target as a bundle of its own instead. The link is published without its mark and the blanks following it, and points at the dispatch sub-section its section carries for the target, which states the dispatch. A `⇉` with no space after it opens no operator: `[⇉Sync](sync.md)` is an ordinary link, compiled like any other, its mark kept as text and no diagnostic raised. The space is what tells an operator from link text that happens to start with an arrow.
- **The parallel dispatch mark:** A link whose text opens with `⫽` (U+2AFD) followed by at least one space, as in `[⫽ Code Review](review.md#code)`, is a dispatch whose sub-agent runs together with those of the other `⫽` links in its section. It withholds what the dispatch operator withholds, its target is required to exist as a dispatch's is, and the run compiles the target as a bundle of its own. The link is published without its mark and the blanks following it, and points at the `Dispatch in parallel` sub-section its section carries. A `⫽` with no space after it opens no operator: `[⫽Reviews](plan.md#reviews)` is an ordinary link, its mark kept as text and no diagnostic raised.
- **Operators that combine:** A deferral states when the material is compiled and a dispatch states who compiles it, so `¬⇉` or `¬⫽`, the marks written together, states one compilation on two counts and is admitted: the material is deferred, and the run that later compiles it finds the dispatch. A blank between the two marks states two operators rather than one, so `[¬ ⇉ target]` is refused: the marks of the combined operator are written together. The deferral dominates what this bundle publishes — the rebased path, the marks removed, and no sub-section, since the dispatch belongs to that later run. Text opening with two dispatch marks, as in `[⇉ ⫽ the reviews](plan.md#reviews)`, states two ways for one sub-agent to run and is refused with a diagnostic naming the link, under `E_UNSUPPORTED_CONSTRUCT`, because the run says so rather than choosing. The defect is in the source the run read rather than in its metadata, which is why it is not a metadata code. Operators are read in order and the first mark with no space after it ends them, so `[¬⇉ the rules](rules.md)` opens no operator and is an ordinary link.
- **An operator's target:** An operator states how a Markdown document or section is compiled, so a link or an image whose text opens with `¬`, `⇉` or `⫽` and names anything else — a remote address, a resource, an image whatever it points at — states a compilation no run performs. The run refuses it under `E_UNSUPPORTED_CONSTRUCT`, naming the reference and the source location it is written at, rather than publishing a mark that states nothing.
- **Dispatched bundles:** A run follows its dispatches — its `⇉` and `⫽` links — transitively and compiles each distinct target — a document, or a document and fragment — once, as its own entry, into a bundle of its own in the run's folder, named by that selection as an entry is. Every dispatch naming the target names that one bundle, and a dispatch naming the run's own single selection names the entry's bundle. Each bundle is compiled under every rule an entry's is, so a link resolves from the file that writes it and is compiled when its target declares, a deferred link contributes nothing and a dispatched link is a further dispatch; a target whose compilation is refused ends the run with that refusal and publishes nothing. A target's shape is the corpus's convention, so a target carrying no numbered step publishes with no diagnostic, and so does a `⫽` target holding a paragraph, a numbered list or an item linking no document.
- **Dispatch sub-sections:** Each section of a bundle whose `⇉` links dispatch a target carries one *dispatch sub-section* for it: a heading `Dispatch <link text>`, the link's visible text without its mark, one level below the section holding the link, after that section's own content and before its child sections, whose body is one line naming the target's bundle file and linking the protocol it follows: ``[Dispatch](#dispatch) `<bundle file>` to a sub-agent.`` The heading's link text is written with each run of whitespace, a line break among them, as one space, so a link wrapped across lines names a one-line heading; the published link keeps the text its source wrote. A dispatched link with no text after its mark leaves its sub-section nothing to be named by, so the run publishes nothing and fails with `E_UNSUPPORTED_CONSTRUCT`, naming the link, its source location and the route that reached it, as the operator refusals do. Links in one section naming one target share its sub-section, the first link's text naming it; each section dispatching the target carries its own, and all name the one bundle. A dispatch in content above a group's first heading takes a sub-section at that heading's level. The sub-section is generated structure, emitted in bundle order like every other heading, so its destination is the renderer's fragment for it and a repeated one takes its ordinal. A dispatch in a level-6 section leaves no level for its sub-section, so the run publishes nothing and fails with `E_HEADING_DEPTH_OVERFLOW`, naming the link.
- **Parallel dispatch sub-sections:** The `⫽` links in a section's own content, wherever its prose writes them, are one *set*; a child section's `⫽` links form that child section's set. Each section carrying a set carries one sub-section for it, headed `Dispatch in parallel`, one level below the section, after the section's own content and its dispatch sub-sections and before its child sections. Its body is the line ``Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):``, linking the protocol it follows, and a bulleted list holding one item for each distinct target the set names, in the order its first link is written: ``- `<bundle file>` (<link text>)``, the first link's visible text without its mark, each run of whitespace written as one space. A target named twice in one set is listed once. A set states no order. Every `⫽` link in the section points at the sub-section, and a target the section names with both `⇉` and `⫽` takes a dispatch sub-section and a place in the set. The sub-section is generated structure placed as a dispatch sub-section is: a set above a group's first heading takes that heading's level, a repeated one takes its ordinal, and a set in a level-6 section fails with `E_HEADING_DEPTH_OVERFLOW`, naming its first link.
- **The Prosiform section:** A bundle carrying a dispatch sub-section or a parallel dispatch sub-section opens with a *Prosiform section*, which states the protocols those sub-sections follow: a heading `# Prosiform`, then `## Dispatch` whenever the bundle dispatches, and `## Parallel dispatch` when it carries a set. A parallel dispatch is dispatch done together and its protocol links Dispatch, so a bundle carrying only sets carries both. A bundle dispatching nothing carries no Prosiform section. The section is the bundle's first heading: it precedes a file heading, and in an entry opening on content above its title it follows that content and precedes the dispatch sub-section the content takes. Its levels are fixed, so each protocol sub-section is the same bytes in every bundle carrying it, and its destinations are `#dispatch` and `#parallel-dispatch`. Each protocol is one paragraph whose wording the profile fixes:
  - **Dispatch:** Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.
  - **Parallel dispatch:** Dispatch every listed bundle at once, each to a sub-agent of its own per [dispatch](#dispatch); an item the invoking step applies "for each" of several values is dispatched once per value, together. Continue when every item has returned; a failed item cancels nothing, and every failure returns together as blockers. Questions return together once all items have, and only the items that asked are dispatched again.
- **Generated heading collisions:** A heading an author wrote, or a file heading, whose text equals one pf emits in the same bundle — `Prosiform`, `Dispatch in parallel`, a protocol heading of the bundle's Prosiform section, or the heading of a dispatch sub-section the bundle carries — would give two sections one name, so the run publishes nothing and fails with `E_HEADING_COLLISION`, naming the authored heading and the text pf emits. A heading pf does not emit in a bundle is the author's there: a bundle dispatching nothing may carry `Prosiform`, and a bundle carrying no set `Dispatch in parallel`.
- **Dispatching its own document:** A dispatched link naming the document that writes it — a section of it by fragment alone or through its own path, or the whole of it — hands a sub-agent material the dispatching session's own document carries. Where that closes no cycle, the run publishes and warns with `W_DISPATCH_SELF`, naming the link and the target, so its author moves the procedure to a document of its own or links it without the operator. A dispatch of the whole document from a section of it, or of the section that writes the link, returns to its own bundle and is a cycle.
- **Dispatch depth:** Dispatch nests: a sub-agent follows its target's bundle, and the dispatched links that bundle carries are dispatched again. The *dispatch depth* of a chain is the number of dispatch hops along it, `⇉` and `⫽` alike, counted from the run's entry. A chain reaching a fourth hop is deeper than a chain is held to: the run publishes and warns with `W_DISPATCH_DEPTH`, because flattening the chain is the author's optimisation rather than a defect. The limit is fixed.
- **Dispatch cycles:** A chain of bundles returning to one already on it — the entry's among them — would have its sub-agents dispatch one another without end, so the run publishes nothing and fails with `E_DISPATCH_CYCLE`, naming the chain. A dispatch naming its own bundle is the shortest cycle. Neither search follows a target already on the chain, so the analysis terminates on any graph of dispatches.
- **A deferred link's destination:** Rebase it to the target's path relative to the captured invocation working directory, preserving filesystem spelling and URI-escaping path characters such as literal `%`, `#`, `?` and spaces. Retain the resolved fragment when present. This spelling can be passed directly to `pf` from that same working directory, including for a fragment-only withheld link. A later invocation from another directory must adjust the path. A deferred link is never rewritten to a bundle destination, even where another reference carried its target into the bundle: what one author withheld cannot be changed by another author's reference. A dispatched link points at its dispatch sub-section on the same ground, never at its target's heading where another reference carried that into the bundle.
- **A withheld link's target:** Required to exist. The normal source reader confirms the document and any requested heading, validating its local metadata and file-wide safety properties. This reference selects no content, discovers no outgoing dependencies and contributes no group membership. A compilation an agent will follow, and one a sub-agent will follow, is one that can succeed.
- **A link naming a document that declares nothing:** Emit as authored. The target is probed rather than captured — its frontmatter span is delimited and decoded within the existing byte budget and the read stops there — so it contributes no content, no group and no destination, and it is counted against no source budget. A link naming a document that does not exist is text on the same ground, because nothing states the bundle is answerable for it; one whose text opens with an operator is refused, as an operator's target requires. A reference the substitution mapping redirects is no text: the mapping is consulted on the identity the reference normalized to before the target is probed, so a mapped reference is compiled whatever its authored path resolves to.
- **Fragment-only links:** Resolve against the original source document's heading index, then follow the same bundling and rewriting rules, every operator included. A fragment names content in its captured source. The substitution mapping is consulted on the identity the fragment resolved to, so a fragment-only reference is redirected like any other.
- **A target that resolves to nothing:** A reference the substitution mapping did not redirect, whose text opens with an operator and which names no document, or a fragment naming no heading in the document it resolves to, fails with `E_TARGET_NOT_FOUND`, whether it is compiled or withheld. An operator states that a run, or an agent, compiles the target, so one that cannot be read is a defect rather than text.
- **Everything else:** A reference carrying a scheme or an authority is not a local document reference. Emit it as authored and never open, fetch or interpret it. No scheme is permitted or refused, because which scheme it carries decides nothing: carrying one at all is what puts the reference outside the tool's interest.
- **Resources:** A resource is a reference that is not a local Markdown document, and an image whatever it points at: image syntax embeds rather than links, so a document named that way is no more bundleable than a picture. Emit every resource as authored wherever it resolves, and warn once that the bundle names one. A resource whose text opens with an operator is refused, as an operator's target requires.
- **Unsupported local-document syntax:** Fail with an actionable diagnostic rather than silently excluding a local Markdown dependency. In v1, raw HTML links to local Markdown are rejected unless explicitly supported by the parser and resolver. A Mermaid Kanban ticket's link and an HTML anchor in a diagram's node label naming local Markdown are rejected the same way, under `E_UNSUPPORTED_CONSTRUCT` naming the line.
- **Examples:** Do not follow apparent links inside code spans, fenced code blocks, or other literal example content, except a Mermaid diagram's link destinations. In a fenced code block whose info string opens with `mermaid`, each destination a diagram link line names is a use on the line it is written, counted against the link budget, and is followed and rewritten as a link is: a destination naming a local Markdown document or section is bundled, and its characters become the anchor of the group it names, every other byte of the fence carried as written. A Gantt task's `click` is the one link Mermaid draws as no anchor: it binds a handler that opens the destination when the task is clicked in the running page, so the rewritten anchor is what that click opens. A sequence diagram's `link` and `links` destinations spell that anchor `#35;<slug>`, the entity Mermaid renders as `#`, because its sequence lexer reads a bare `#` as opening a comment. The lines are `click <node> href "<destination>"` and `click <node> "<destination>"` in any diagram; `link <class> "<destination>"` in a class diagram; and, in a sequence diagram, `link <actor>: <label> @ <destination>`, whose destination is the trimmed text after the first `@`, and `links <actor>: {…}`, each string value of whose JSON object is one destination. A diagram's type is the word its text opens on once a leading front matter block, its `%%{…}%%` directives and its `%%` comments are set aside, as Mermaid detects it, so a line beginning `link` in any other diagram is carried as written. Their keywords match in any letter case. A sequence line's text ends at its first `;` or `#` that opens no entity, as Mermaid's sequence lexer ends it, so a `link` destination or a `links` object ends there and the bytes after it are carried as written; a `#35;` a sequence destination holds names the `#` it renders as, so `<doc>.md#35;<fragment>` names the section `<fragment>`. A `links` object is read as `JSON.parse` reads it: a key written twice names its last value alone, and a value that is not a string is refused with a diagnostic naming the line, under `E_UNSUPPORTED_CONSTRUCT`, because Mermaid renders it as a broken link. A click naming a callback, a destination naming no local Markdown document, a `links` value holding a JSON escape and a `links` line holding no JSON object are carried as written and open nothing, as is a C4 diagram's `$link`. A Kanban ticket's link, which Mermaid builds by putting the ticket in place of `#TICKET#` in the `ticketBaseUrl` the diagram's front matter or `%%{init}%%` directive sets, and an HTML anchor in a node label are links Mermaid renders and the reader does not follow: one naming a local Markdown document is refused with a diagnostic naming its line, under `E_UNSUPPORTED_CONSTRUCT`, as raw HTML naming one is, so the author writes it as a `click`, and one naming a remote address is carried as written. A diagram link carries no operator, because a diagram gives it no link text to open with one.

## Reference normalization and path identity

Capture the canonical invocation working directory once. Resolve positional file references from it, allowing relative parent segments. A positional reference is `document` or `document#fragment`; a fragment alone names no document on the command line, because `[Check](#section)` inside a document already resolves against that document and needs no spelling.

A path-bearing local Markdown reference authored in a source, a deferred link included, resolves from that source's own directory, which is the path a reader of the file follows in an editor or on GitHub; a preset's mapping entry is the exception, naming both sides from the directory of the file declaring it. Whether the resolved target enters the bundle is decided by that target's own declaration and by nothing about either file's position, so documents in different directories need no agreement and one document reached by two sources is one answer. A document's derived boundary is the deepest directory holding every local Markdown path its own links name, and it admits every authored link because it is derived from them. What confines a run is the invocation working directory, which bounds positional entries and the paths diagnostics name. Fragment-only references identify the captured source itself.

A document may link a sibling library that does not contain it, and nothing about that position decides the answer: the link is compiled when the target declares and is text when it does not. Selecting an entry authorizes bounded capture of that file without requiring it to lie beneath any directory its bytes declare.

### Bounded bootstrap capture

Normalize each explicit file reference before opening it. Bind access to the canonical invocation directory for descendants, or a verified no-follow parent directory for a relative entry using parent segments. Verify traversed components before canonicalization can hide symlinks. This bootstrap grant opens only the named regular Markdown source, not its dependencies. Declarations are read from these captured bytes under the same raw per-file and aggregate byte limits, UTF-8 rules, YAML collection-depth limit and physical coordinate mapping used for ordinary sources. Do not perform an unbounded preliminary read to discover a declaration.

Retain canonical source identity, bytes, content hash, immutable settings and the declaration its boundary is derived from together. Bind every dependency access to the invocation working directory captured at start. Reaching the same canonical source through another parent retains the capture, because a document's settings are its own and neither first-discovery parent nor an incoming link supplies them. Canonical normalized paths identify sources; distinct hard-linked paths remain distinct source identities.

Retain the bound access context for every capture and recheck full-file content and identities before publication. Mutation, deletion or replacement of a source fails with `E_SOURCE_CHANGED`; no successful bundle or partial file is published. Bootstrap capture counts toward all source limits and output-overlap checks, including deferred-only targets. Safe access and capture are required in check mode too.

### Resolution sequence

1. For authored Markdown links, obtain the destination from the parser with Markdown escapes and entities interpreted once. CLI reference arguments enter directly as URI-reference strings.
2. Split URI components before percent-decoding so encoded `#` and `?` remain filename characters rather than becoming delimiters.
3. Emit source-authored references carrying a scheme or an authority as authored, and resolve no further. A positional reference of either shape fails with `E_SOURCE_OUTSIDE_ROOT`.
4. Reject any query component on local Markdown document references, including an explicitly empty query.
5. Strictly validate percent escapes and decode path and fragment exactly once as UTF-8. Look up the decoded source fragment exactly; do not lowercase or re-slug it.
6. Reject NULs, control characters, decoded path separators originating from escapes, and remaining backslash separators. Local paths use forward slashes in v1.
7. Normalize `.` and `..` relative to the proper reference base: the invocation working directory for positional files, the authoring source's own directory for path-bearing source links. A relative positional parent path uses bounded bootstrap capture. Fragment-only source links use their captured document directly.
8. Enforce no-symlink source access and require a supported regular Markdown file.
9. Treat absent and empty fragments as whole-document references; otherwise resolve to the canonical eligible section identity.

Do not apply additional Unicode normalization to filesystem names beyond what the operating system requires. Distinct normalized source paths remain distinct source documents even if their contents or inode happen to be shared.

| Reference | Required interpretation |
| --- | --- |
| `guide.md` | Whole document with the documented transformations. |
| `guide.md#` | Same whole-document target. |
| `#run` within `guide.md` | Original section `run` in that document. |
| `guide.md?view=raw#run` | Fail: unsupported local Markdown query. |
| `notes%23draft.md#run` | Section `run` in literal filename `notes#draft.md`. |
| `notes%2523draft.md#run` | Section `run` in literal filename `notes%23draft.md`; no second decoding. |
| `sub/../guide.md#run` | Normalize to `guide.md#run` against the reference's own base. |
| `../guide.md` positionally | Capture the file relative to invocation working directory with bounded no-follow access. |
| A source link whose target declares nothing | Emit as authored without capturing the target, deferred mark included. |

A path beginning with `/`, a filesystem absolute path, a platform-specific drive path, a scheme or an authority is unsupported as an entry and fails with `E_SOURCE_OUTSIDE_ROOT`. Inside a source those references are emitted as authored without opening a dependency.

### No-symlink source policy

Reject symlinks in every traversed component of bootstrap source and dependency access with `E_SOURCE_SYMLINK`. The invocation working directory is canonicalized once; every subsequent walk is bound to its captured directory or a verified directory derived from it. A dependency base does not vary according to which logical alias was discovered first.

Use rooted, no-follow access or equivalent safeguards, not merely a pre-open string check. Platforms unable to enforce the policy must fail or declare a narrower supported environment rather than silently weakening confinement to the invocation working directory.

Non-Markdown resource links are not opened as source dependencies. They remain governed by the resource policy.

## Resources are text

A relative image or other non-Markdown reference is text. It is emitted byte-identical to its source and never opened, rebased or resolved, so a bundle read from somewhere other than its source directory may not find it.

A bundle carrying at least one resource reference warns on stderr with `W_RESOURCE_PORTABILITY` that resource portability is not guaranteed. A successful Markdown bundling establishes nothing about the resources its text mentions, and the warning does not turn a successful run into a failure. A bundle whose text mentions no resource carries nothing to warn about and emits the warning not at all.

Rebasing a resource path means deciding where the bundle will be read from, which is the caller's question rather than the tool's. Nothing here maps a resource to a URL, so the tool holds no notion of a web address at all.

## Resource limits

Use deterministic configurable limits and fail rather than truncate. These are approved initial engineering defaults, not benchmark-derived limits or guarantees about an agent's context capacity.

| Budget name | Default | Counting rule |
| --- | --- | --- |
| `files` | `256` | Distinct normalized source-document identities opened. |
| `file-bytes` | `1,048,576` | Raw bytes in one source, including frontmatter and any BOM. |
| `input-bytes` | `16,777,216` | Sum of raw source bytes, once per source identity. |
| `output-bytes` | `262,144` | Complete UTF-8 bundle, including file headings, structural ancestors, and separators. |
| `targets` | `4,096` | Distinct canonical document/section targets discovered, even if later subsumed. |
| `links` | `32,768` | Authored link/image occurrences examined in selected content, once per source occurrence. |
| `nesting` | `64` | Markdown syntactic container depth and, independently, YAML collection depth as defined in Conversion metadata; exceeding either limit is an error. |
| `depth` | `8` | Link hops from the nearest entry reference to a reached target, counted along its shortest path. |

Every budget holds per bundle. Each bundle a run publishes is read by one agent and compiled from its own entry, so `depth` counts hops from that entry and every other budget counts what that bundle alone opens, reaches and publishes; a dispatched target crossing one fails the run while the entry's own closure stays within it.

Crossing any of these fails the compilation with `E_RESOURCE_LIMIT`, and the diagnostic names the budget crossed and the figure that crossed it. One code covers all eight because one remedy does: the sources are restructured or the number is raised, and the figure the run reports is what says which.

Accept a name from the eight and a positive decimal integer; a name outside them, an entry carrying no `=`, a name given twice and a value that is no positive integer are each invalid usage. Zero must not mean unlimited. Traverse iteratively; the expansion-depth budget is a declared constraint on how far a chain of references may reach, not a recursive-call-depth cap, and a cyclic graph within the budget bundles normally.

*Expansion depth* constrains the shape of a reference graph rather than its size, which the file, byte and target budgets bound. It exists so a document reaches what governs it directly, and a chain that outgrows the budget is a prompt to restructure the sources rather than to raise the number.

Enforce the `nesting` ceiling as an explicit failure, not merely a parser option that could silently reinterpret over-deep syntax. Apply necessary parsing-safety limits to the complete opened source being indexed, even when the requested section is narrower, and include that enforcement in the parser fixture gate.

The wrapper must enforce any smaller transport limit; 256 KiB is not universally safe for agent delivery. Do not estimate tokens by dividing bytes by a constant; future token budgets must name and pin the tokenizer.

## Source consistency

Read each distinct source once during discovery and keep its parsed content, canonical identity, and content hash for the entire compile. Before publication, recheck all sources and fail with `E_SOURCE_CHANGED` and a retry message if any content or identity has changed. One code covers a source that changed, disappeared or resolved elsewhere: each is the same fact, that the bytes discovery captured are no longer the bytes the path names.

This is change detection, not a transactional filesystem snapshot: files can change again after a check. When strict reproducibility is required, bundle from an immutable source snapshot; do not claim that hashing alone supplies cross-file atomicity.

## Agent delivery contract

Successful compilation establishes that the complete candidate passed validation. It does not establish that a downstream tool transport delivered every byte to the calling agent.

- **Exit status:** The agent-facing wrapper must check process success rather than interpreting the mere presence of Markdown as a successful read.
- **Response limit:** The wrapper must buffer or otherwise verify complete output and enforce a response-size limit compatible with its transport. If it cannot deliver the whole document, return a *delivery* failure rather than a truncated apparent success.
- **Clean Markdown:** Keep the bundle file limited to the bundle document. The bundle opens on its Prosiform section where it dispatches, and otherwise on its first group's content, and carries no generated commentary: completion metadata, byte counts, warnings, and diagnostics belong in the wrapper's structured result or a sidecar, never in per-section Markdown envelopes.
- **Broken pipes:** Report transport/write failure through a nonzero exit when detectable. Do not claim that stdout can be atomically delivered to every consumer.
- **No silent fallback:** Do not replace oversized output with a summary, a partial document, or references that the agent must follow separately.

## Validation scope

Validate link resolution, supported selected syntax, and resource rules within the selected dependency closure. Parsing a complete file for indexing does not make its unselected sibling sections dependencies; ancestor-only headings undergo structural, depth, and namespace checks but not dependency traversal.

Whole-file checks are limited to facts needed for safe access or correct interpretation: source identity and encoding, raw-byte and required parsing-resource limits, frontmatter, source-change detection, original heading enumeration, definitions needed by selected uses, and ambiguity of requested fragments.

An unrelated broken link in an unselected sibling must not fail bundling. If closure expands to include that sibling, its links become subject to validation.

An opened file can nevertheless fail because an unselected construct exceeds a declared file-wide parsing-safety limit. Diagnose this as inability to safely index the containing source, not as an inferred dependency on that sibling.

Keep `-L` scoped to authored occurrences in the selected closure. If full-file indexing needs another work budget or instrumentation, specify it separately rather than silently changing that option's meaning.

### Source and candidate validation modes

Use the same declared Markdown grammar where applicable, but separate the policy context for source validation from candidate validation.

- **Source mode:** Enforce declaration rules, source-fragment resolution, and source-owned self-reference checks. A source fragment names one heading and carries no ordinal.
- **Candidate mode:** Accept generated file headings, shifted headings, and structural ancestors. Validate destinations, coverage, reconstructed outlines, block structure, and reference invariants against source provenance.
- **Ownership:** Retain original source ownership independently of output heading levels. Validate the reconstructed outline against that model rather than assigning synthetic file/structural ancestor headings executable ownership.
- **Preprocessing:** Do not pass the candidate back through source frontmatter stripping or dependency discovery.

## Validation and failure contract

Validation is mandatory. Failures must give the calling agent enough information to explain the problem to the user or halt safely.

- **Resolution:** Every supported local Markdown reference resolves to a known document or section.
- **Target integrity:** Every rewritten link points to the intended source-derived destination, not merely a section whose slug happens to coincide.
- **Uniqueness:** Each bundle destination occurs once, and resolves in the renderer that reads the bundle.
- **Boundaries:** Combining sections must not make later material part of an earlier code fence, HTML block, or unintended container.
- **Preservation:** Preserve selected instruction wording and code under the declared transformations: leading BOM removal, frontmatter stripping, reference-use conversion, definition removal, destination rewriting, title absorption, heading shifts and necessary Setext conversion, generated group, variant and member headings, heading-only ancestors, Markdown escaping, and boundary whitespace. Untouched non-heading bytes and code examples are not reformatted or repaired.
- **Completeness:** No content is silently dropped to satisfy resource limits, and no failed dependency is silently omitted.
- **Safety:** Enforce bounded bootstrap access, the invocation working directory and configured resource limits. Never execute included commands, and never open a reference the tool did not resolve as a local Markdown dependency.
- **Publication:** Compile failures return nonzero status and write no bundle. Diagnostics go to stderr, and standard output carries no bundle. A run validates every bundle it publishes before it writes any, so a failure in any one writes none, and `-c` validates the same set and writes none. Before any bundle is written the run holds every bundle to the output budget, every derived name to one bundle, the output folder to existing and every derived name to the length its filesystem allows, under `-c` as without it, so a set publication would refuse ends a check run as it ends the run. A source the run's bundles read with different bytes or identities between two of their reads fails with `E_SOURCE_CHANGED`. The run's bundles are written into a fresh hidden folder beside the run's folder, whose name is fixed in length whatever the run folder's, which is then renamed onto it; whatever already stands at the run folder's path — only ever an entry carrying the run's `.bundles` name — is renamed aside first and removed once the new one stands, so a reader sees the whole set one run produced or the whole set before it, never a mixture, and for a moment no folder at all. The run folder's path is never followed: the output folder is resolved and the run's name joined to it, so a symbolic link standing at that path is renamed and removed as the link it is, and whatever it names is left as it was. A failure before the new folder stands removes it and leaves the output folder as it was; where the earlier set cannot be renamed back, the failure names the path it was moved aside to. An earlier set that cannot be removed once the new folder stands leaves the run published, and warns with `W_EARLIER_SET_RETAINED`, naming the path that holds it. Nothing else in the output folder is removed or rewritten. An output path that refuses the write, a detected broken pipe among them, fails with `E_PUBLICATION_FAILED` naming that path.

### Post-compilation invariants

Validate the completed document against the source-to-output mapping, not only its surface syntax.

- **One intended destination:** Each rewritten link resolves to exactly one destination corresponding to its intended original document or section, and that destination is the fragment the declared renderer generates for the heading it names.
- **Reference preservation:** Each link/image use in selected source content retains its visible content and title and reaches its intended destination under the resource policy. Structural ancestor-only titles intentionally contain no live source links or images.
- **No new links:** Source text parsed as literal bracketed text must not become a new link or image through bundling.
- **No definition leakage:** No original link-reference definition nodes survive emission; literal examples of definitions remain unchanged.
- **Exactly-once coverage:** Each selected source region's content is represented once after unioning overlaps, excluding a removed leading BOM, stripped frontmatter, and removed reference definitions. Parent inclusion satisfies child inclusion without another copy.
- **No accidental omissions:** Selected-content coverage equals the resolved dependency closure under the documented transformations. Track generated structure separately so it cannot conceal a missing selected region.
- **No accidental expansion:** The only unselected source-derived content emitted is required heading-only ancestry. Never include an unselected ancestor's body or siblings merely to supply structure.
- **Destination stability:** A reference's destination is the one its target was assigned, before and after overlap consolidation.
- **Block-syntax preservation:** Generated headings and region boundaries must not absorb content into unintended non-heading containers.
- **Group isolation:** Each group has exactly one H1, each contributing source belongs to exactly one group, and a source's emitted headings sit beneath that group's H1 rather than entering another group's outline.
- **Outline preservation:** Each selected eligible heading retains its original ancestor chain and relative level gaps under its group's shift, using structural ancestors where needed. In a merged group the grouping rules supply the chain above the grouping depth, and the heading the rules place there is where the preserved chain begins. Validate against the original source outline and the grouping rules together.
- **Depth safety:** No emitted heading exceeds H6; overflow produces a failure, not a success with altered depth.

Use provenance ranges and distinct generated-structure records to check these properties. Repeated identical prose in different source regions is not duplication by itself, and string counting is not a sufficient exactly-once test; neither filename wrappers nor structural ancestors may count as selected body content.

These checks establish named syntax, reference, and coverage invariants. They do not prove natural-language instruction equivalence or successful agent execution.

Illustrative diagnostic, not an existing command result:

```text
E_TARGET_NOT_FOUND: cannot resolve local Markdown target
  source: artifacts/epic-issue-body.md:42
  link: epic.md#delivery-findings
  resolved file: artifacts/epic.md
  missing fragment: delivery-findings
  inclusion chain:
    modes/sync-mode.md
    → artifacts/epic-issue-body.md#record-epic-delivery
    → artifacts/epic.md#delivery-findings
  action: correct the link or restore the target heading
  result: compilation failed; no bundle emitted
```

Diagnostics should include a stable error code, referring source location, original reference, relevant resolved identity, inclusion chain, and a practical remedy when one can be stated accurately.

### Exit status and JSON diagnostics

Use stable error codes for individual defects and the following exit-status categories. Warnings may accompany success, and each carries a stable code of its own, prefixed `W_` where an error code is prefixed `E_`.

| Exit | Meaning |
| --- | --- |
| `0` | Successful compilation, validation, or informational CLI response. |
| `1` | Input, dependency, policy, safety, or resource-limit failure. |
| `2` | Invalid CLI usage or option combination. |
| `3` | Output publication or delivery failure, including a detected broken pipe. |
| `4` | Unexpected internal error; do not misreport it as a source-document defect. |

`W_COINCIDENT_HEADING` reports generated headings that coincide: two file headings, or two member headings of one merged group, whose texts are one text but for capitalization. One warning names each coinciding set, carrying the shared text, the first heading's source as `location` and every other as `related`, in bundle order. A heading an author repeats raises none.

`W_DISPATCH_DEPTH` reports a chain of dispatches reaching a fourth hop, and `E_DISPATCH_CYCLE` refuses a chain returning to a bundle already on it. Each distinct target the entry dispatches raises at most one depth warning, at the first link dispatching it, and the run refuses the first cycle it finds: each carries that link as `location`, each later hop's link as `related` with the target it dispatches, and the entry followed by every hop's target as `chain`, each chain in the order the bundles write their dispatches. `W_DISPATCH_SELF` reports a dispatched link naming the document that writes it, naming the link as `location`, the reference, and the target as `resolved`.

`E_HEADING_COLLISION` refuses an authored heading or a file heading whose text equals one pf emits in the same bundle, naming the authored heading as `location`, its document as `source` and the text in its message.

`W_EARLIER_SET_RETAINED` reports a published run whose earlier set, moved aside, could not be removed, naming that path in its message and remedy.

`W_MOCK_SUBSTITUTED` reports the substitution mapping's work: one warning for each key a reference named, emitted at the first reference that named it, however many references named that key. It names that link as `location`, the destination the author wrote as `source`, and the substitute's identity as `resolved`, and its message states the identity the reference would have resolved to. `W_MOCK_UNUSED` reports each mapping key no reference named, carrying the key's authored spelling as `source` and no `location`, because it states a fact about the invocation rather than about a source. Both accompany a successful run and leave it at `0`, and a run given no mapping raises neither.

An unexpected internal error carries `E_UNEXPECTED_INTERNAL_ERROR`. It names the run rather than any document the run read, so a caller reading it is not sent to look at its sources.

Every failing outcome this contract names carries a code, so a diagnostic without one reports a defect the contract does not define.

With `-d json`, emit one JSON object per stderr line, including `severity`, `code`, `message`, location, original reference, resolved identity when available, inclusion chain, and remedy when accurate. The resolved identity is named `resolved`: a bundle destination where the reference reached one, and a canonical source path where it reached a document. Do not mix JSON diagnostics with progress prose.

## Adversarial acceptance fixtures

Before broad implementation, create small fixtures with exact expected bundles or expected failures.

- **Identity:** Whole-file bundling with internal section links; direct self-links through heading names; ancestor back-references; preamble-to-document self-links; same-file cross-section links.
- **Coverage:** Child-first then parent inclusion; whole-document inclusion discovered late; shared dependencies; multi-file cycles; different entry argument orders.
- **Destinations:** A unique bundled heading taking a bare slug, repeated bundled headings taking ordinals in bundle order, a source fragment ambiguous within one document refused, two documents whose file headings coincide taking ordinals and a warning, same-basename paths in different directories, and a file group whose file heading does not imply whole-document inclusion.
- **References:** Definitions outside a selected section, conflicting labels, unused definition removal, unresolved bracketed text remaining literal, reference-style images and titles, fragment-only links, and unsupported raw HTML document links.
- **Deferral:** A marked reference contributing nothing to the bundle, the mark and the blanks following it removed from the published link because its destination states the deferral, a mark with no space after it compiled as an ordinary link, a fragment-only reference deferred the same way, a deferred link standing unrewritten where another reference carried its target, a deferred reference naming no document and one naming no heading each refused, a deferred link naming a remote address, a resource or a document that declares nothing and a deferred image each refused, and a deferred link published with its target's URI-escaped path from the invocation working directory.
- **Dispatch:** A dispatched reference contributing nothing to the bundle carrying it and compiled to a bundle of its own, its link published without its mark and pointing at a dispatch sub-section naming that bundle, a dispatched target named by its working-directory path and fragment, a sub-section placed after its section's own content and before its child sections, a link opening with the deferral mark and the dispatch operator refused with the link named, a mark with no space after it compiled as an ordinary link with no warning, a dispatched link naming a remote address, a resource or a document that declares nothing and a dispatched image each refused, a chain of exactly three dispatches publishing four bundles with no warning, a fourth hop warning, a cycle of dispatches refused, a dispatch of its own whole document from a section refused as a cycle, a dispatched section of the entry's own document counted as a hop, a dispatched section carrying numbered steps, a dispatched section of headings and bullets and a dispatched document whose only numbered list is code each publishing with no diagnostic, a dispatch naming a section of its own document by fragment or by path warning once, a dispatched target crossing `-F` while the entry stays within it failing, a dispatch in a level-6 section refused, a link wrapped across lines, broken by a hard line break or ending in a space naming a one-line sub-section heading, a link with no text after its mark refused, an authored heading equal to a dispatch sub-section's or to `Prosiform` refused, and an authored `Prosiform` or `Dispatch in parallel` heading publishing where the bundle emits none.
- **Parallel dispatch:** The `⫽` links of one section pointing, without their marks, at one `Dispatch in parallel` sub-section listing each target's bundle; a target named twice in one set listed once; a section carrying `⇉` and `⫽` links with a sub-section for each `⇉` target and one for its set; a `⫽` target holding a paragraph, a numbered list or an item linking no document publishing with no diagnostic; a link opening with the parallel dispatch mark and the dispatch operator refused; a `⫽` link naming a remote address refused; and a mark with no space after it compiled as an ordinary link.
- **Prosiform section:** A bundle using the dispatch operator opening with the Dispatch protocol alone; a bundle using the parallel dispatch mark opening with the Dispatch and Parallel dispatch protocols; a bundle using both stating each once; a bundle using neither carrying no Prosiform section; the section following an entry's preamble and preceding a file heading; each sub-section's instruction linking its protocol; and an authored heading equal to a protocol heading pf emits refused.
- **Extraction:** ATX and Setext roots, rejection of nested-heading targets, nested headings not terminating outer selections, and original duplicate numbering including ineligible headings.
- **Boundaries:** Unclosed fences, HTML blocks, adjacent lists, nested containers, file-group separation, leading frontmatter, and YAML examples that must remain intact.
- **File hierarchy:** Same-basename sources in different directories; a document's title heading its file group; the Markdown extension absent from a path-named file heading; a nested path and a hyphenated name emitted in title case beside a merged group's heading; a heading an author wrote and a deferred link's path keeping the spelling their source gave them; paths needing Markdown escaping; a group whose title the file heading absorbs and one whose H1 it does not; a document carrying more than one H1; H1–H5 shifts; H6 overflow; Setext and multiline-heading conversion; and unchanged heading-like code examples.
- **Grouping:** One entry bundled with and without a group, selecting the same content; a merged section drawn from several documents; a name occurring once left bare; a name several documents carry emitted once with a variant heading each, distinguished at one path segment and at more than one; two members of one stem in different directories taking the subsection headings that tell them apart; a merged section carrying body text from more than one document split by document; an unannotated document keeping its own group; a whole-document reference to a member resolving to the subsection naming it, one to a member carrying nothing above the grouping depth and contributing a heading text no other member carries resolving to that merged heading, and one to such a member whose contribution is pooled with another's resolving to the variant heading naming it; a member named by the heading its own title is absorbed into; a group emitting no merged section carrying its member subsections directly beneath its heading; a reference to a grouping-depth heading resolving to the variant carrying the document it named; a member's shallower section carried under the subsection naming it; a section split by document taking precedence over the names inside it; and explicit members in unrelated directories using the same group identity.
- **Partial outlines:** Disjoint selections such as Alpha and Beta/Detail; deduplicated ancestor structural ancestors; original skipped heading levels; ancestor promotion after dependency expansion; and no ancestor-body or structural ancestor-link dependency leakage.
- **Wrapper identity:** A partial file group's document destination does not satisfy a whole-document dependency without expanding its selected content.
- **Normalization:** Empty fragments, query rejection, percent-encoded delimiters, double-encoded percent sequences, invalid escapes, paths normalising above the invocation working directory, internal `..`, symlinked files/directories, and unsupported path forms.
- **Resources:** An image, a script link and a relative path inside a command example each emitted byte-identical, with the portability warning on stderr.
- **Consistency:** Source modification, deletion, or changed canonical identity during compilation.
- **Validation scope:** Unselected broken/self-referential siblings do not fail a narrow run but do fail when later included.
- **Delivery:** Nonzero process exit, output-budget failure, broken output pipe, wrapper rejection of transport-oversized output, and a successful run reporting each entry reference's destination, with and without a grouping rule.
- **Parser fidelity:** Exact ranges for multiline references, reference-style images, nested image/link edits, tables, tabs, Unicode, escapes, CRLF, and original diagnostic coordinates.
- **Definition inventory:** Remove every selected definition occurrence, including duplicates, unused labels, case-fold-equivalent labels, multiline definitions, and supported containers, without changing original winner selection.
- **Parser exhaustion:** Trigger reference-expansion suppression below the tool's public input/output limits and require an explicit failure. Include a case that consumes the budget on its last valid reference with no later lookup, which must not falsely claim omitted references.
- **Validation modes:** Candidate validation accepts generated file headings and structural ancestors, confirms each destination against the renderer's own slugging, and preserves saved source ownership; a subsequent source invocation rejects the generated document.
- **File-wide safety:** Excessive parsing depth in an unselected sibling can fail with a file-indexing resource diagnostic, while an ordinary unselected broken link does not.
- **Profile:** Task markers protected from definitions, disabled typographic rewriting, Markdown suffix classification, and explicit rejection of unsupported selected dependency constructs.
- **Frontmatter:** Optional BOM, exact opening/closing delimiters, `...` termination, leading-blank-line distinction, malformed delimiters, and missing closers.
- **CLI:** Rejection of `-r` and `-g` with `E_INVALID_USAGE` and exit 2; retained operational flags; working-directory resolution for positional files and `-f`, `-c` with an output file and no publication, clean JSON diagnostics, and documented exit statuses.
- **Limits:** Every limit fails at the first exceeded boundary without truncation; zero/negative overrides fail; parser nesting cannot silently fall back to different syntax.

### Metadata conformance cases

| Outcome | Required fixtures |
| --- | --- |
| Per-file ownership | Direct entry, ordinary link, transitive dependency, fragment-only entry with referrer, and section fragment of one annotated source; entry settings do not affect a linked source. |
| Explicit grouping | Unannotated sibling; same group across unrelated directories; duplicate basenames; group/section heading collision; matching depths; conflicting depths with deterministic locations under reversed discovery and entry order. |
| Stable selection | Diamond dependency, overlapping fragments and ordinary cycle; deferred-only target, later activation, and a target reached through both deferred and ordinary links. |
| Accepted YAML | Absent, empty and comments-only block; empty document-root or `prosiform` mapping; unrelated skill fields; integer depth; BOM and CRLF; both closing delimiters. |
| Rejected metadata | Malformed YAML; scalar, sequence or explicit-null root; invalid `prosiform` mapping and values; missing paired field; unknown key; blank/control-containing or colon/slash group; string, float, boolean and out-of-range depths; empty, non-string or unsupported root paths. |
| Safe YAML | Duplicate keys at root and nested levels with both coordinates; custom tags, aliases, merge keys; collection depth at and beyond the limit; raw source-byte boundary and source-change capture. |
| Body separation | Apparent Markdown headings, links and definitions in metadata produce no dependencies or rendered bytes; body YAML fences remain literal; physical diagnostic coordinates include metadata and BOM. |
| Preserved assembly | Overview and variant arrangements, shortest distinguishing member names, heading overflow, ambiguous source slugs, anchor collisions and document/section rewrites retain their defined outcomes. |
| Atomic failure | Invalid metadata and conflicting groups under file output and check mode, with an existing output file preserved; text and JSON carry both conflict locations. |
| Public interface | Help and invocation table agree on operational options; structural option rejection; representative metadata corpus and installed-wheel smoke against the identified candidate. |

### File-owned invocation conformance cases

| Outcome | Required fixtures |
| --- | --- |
| Declaration defaults | An entry declaring nothing failing, and a linked file declaring nothing emitted as text, with the invocation working directory different from both containing directories; each resolves its outgoing paths from its own directory, and the invocation directory bounds them. |
| Target declarations | A target above the writing document's directory compiled where a retired root would have carried it as a citation; a sibling library outside its linker; a target declaring nothing emitted as authored; a document declaring an empty block compiled. |
| Shared identity | Diamond dependencies and cycles across different directories; reversed entry and discovery order; one capture per canonical source; distinct paths sharing an inode remain distinct. |
| Declaration safety | A `root` refused as an unknown key; an empty block declaring; a document declaring nothing; unreadable sources; source symlinks; confined internal parent traversal. |
| Bootstrap limits | Positional entry capture enforces raw per-file, aggregate and YAML nesting limits before following links; entry mutation during capture; source identity changes before publication. |
| Self references | Fragment-only links and deferred fragments; deferred target validated but its outgoing dependencies unopened. |
| Shared paths | Two physical sources sharing a path relative to their own directories, named by their working-directory paths; stable source sorting and conflict locations; unambiguous diagnostics and inclusion chains; ambiguous displayed member names published with a warning. |
| Derived filenames | Whole-file, `.markdown`, mixed-case suffix, section and empty fragment, and equivalent duplicate references; literal underscores, spaces, Unicode and parent segments; a linked target's group does not rename the entry. |
| Combined selection | Multiple files, distinct sections of one file, and whole-file plus section selections produce one bundle, in a run folder of the same name, whose name joins each selection's name in command-line order, including in check mode. |
| Publication | A run folder carrying the `.bundles` suffix in the invocation working directory and in the `-o` folder; an author folder named like the entry left untouched; `-o -` refused; an existing run folder preserved on failure and replaced whole on success; a run folder holding any captured source, including deferred-only targets, refused; filename/length failure; check mode and clean stdout/stderr; a set of bundles validated whole before any is written, and a swap refused part-way restoring the earlier folder. |
| Deferred handoff | URI-escaped cwd-relative destination, including parent segments and literal delimiters, can be invoked from the same working directory with `pf`; a document that declares nothing and an unopened resource retain authored bytes. |

Runtime delivery updates each consumer in the layer that changes its behavior: settings schema consumers with the decoder, entry fixtures and CLI consumers with the resolver, and stdout-dependent consumers with automatic output publication. This includes installed-wheel smoke commands and diagram renderer invocations. Compare compiled content independently of invocation and output location against baseline `93fe6b354a85e244f64e33af700a55aab4f26044`; entry-root annotations preserve body bytes and deliberately update physical-location expectations. Authoring guidance teaches the declaration, full setting names and hyphen-preferred paths. These are required conformance checks, not claims that the current runtime has passed them.

## Implementation verification and residual policy detail

- **Source-language handoff:** The tagged contract includes YAML 1.2 Core frontmatter, per-source declaration and conversion ownership, metadata and source-access diagnostics, normalized output naming and the operational CLI surface. Freeze evidence records the Python baseline revision, explicit contributing-member annotations and resulting fixture bytes; the Rust build consumes that same tagged contract and corpus. Contract review alone establishes no compiler conformance.
- **Source-range adapter:** Rust and the first parser candidate are selected, but range fidelity, complete occurrence coverage, observable reference-resolution suppression, and nested-edit handling must be proven after implementation is authorized.
- **Dependency pins:** Choose an appropriate Rust slugging component and exact tested dependency versions; compatibility fixtures, not assumptions about upstream behavior, establish the supported profile.
- **Calibration:** Revisit numerical defaults only with measured fixture and real-skill data. The approved initial limits are not performance claims.
- **Upstream route:** Keep the possible contribution recorded in the note below. No issue or PR drafting, implementation, or publication is authorized.

The implementation should remain a deterministic local Markdown compiler. Workflow state, authorization, semantic instruction rewriting, and remote document ingestion are separate concerns, not implicit parts of bundling.

### Upstream follow-up reference

If parser verification demonstrates a need, consider two narrowly scoped pulldown-cmark contributions: observable reference-resolution suppression and opt-in access to every reference-definition occurrence. Preserve default rendering, first-definition resolution, and existing resource protections.

- **Definition access:** Review the earlier source-tooling discussion and definition-tracker work in [issue #423](https://github.com/pulldown-cmark/pulldown-cmark/issues/423), which was closed through PR #512.
- **Expansion protection:** Preserve the quadratic-growth mitigation introduced in [PR #845](https://github.com/pulldown-cmark/pulldown-cmark/pull/845); propose observability rather than disabling the limit.
- **Offset-iterator regression:** Track the existing report and fix/backport discussion in [issue #1129](https://github.com/pulldown-cmark/pulldown-cmark/issues/1129) rather than opening a duplicate.
- **Contribution process:** Consult the project's [contribution guidance](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/main/CONTRIBUTING.md), which requests advance discussion for larger changes.

This is a deferred design reference only. Do not draft an upstream issue or PR, or take external action, unless the user later requests it.
