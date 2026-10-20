# prosiform: revised v1 design

prosiform is intended for agent skills and other instruction sets authored as collections of linked Markdown documents. Authors can keep procedures, shared rules, prerequisites, and reference material in separate, reusable sections rather than duplicating them in every operation. An agent typically enters through a document such as `SKILL.md` and selects a linked procedure to carry out.

The problem addressed here is the gap between that modular authoring structure and the complete context needed to perform an operation. A document or section link identifies a *destination*, but does not itself establish which content is retrieved, whether its dependencies are followed, or whether the resulting context is complete. Leaving those decisions to the agent makes retrieval part of the reasoning task, with opportunities for missed prerequisites, unnecessarily broad reads, and inconsistent handling of repeated or recursive references.

prosiform moves this retrieval and assembly work into a deterministic compilation step. Given one or more local document or section references, it recursively resolves supported Markdown dependencies, consolidates repeated and overlapping *selections*, and produces one continuous Markdown document organized under a top-level filename heading for each source. Source headings move down one level beneath that heading, except in a file whose own title it already carries, and heading-only ancestors preserve the outline of partial selections; links to included documents are rewritten to the fragments a renderer generates for the headings they now name. It validates the complete *candidate* before *publication*, either returning the *bundle* or failing with *diagnostics* the calling agent can explain to the user. Authors retain modular source files, while the agent receives the selected material and its explicitly linked dependencies without needing further local Markdown retrieval.

The intended guarantee is complete, validated bundling of the explicitly linked content under a declared Markdown *profile*, not control over agent execution. prosiform does not infer unlinked prerequisites, execute procedures, enforce workflow transitions, or guarantee that an agent obeys the resulting instructions; web references and non-Markdown *resources* are also outside its recursive bundling scope. This separation lets the tool make retrieval predictable without becoming a workflow engine or requiring authors to abandon their linked-document structure.

A term italicised on first use is a contract term. It means one thing and nothing else here, in the acceptance criteria, in the fixture corpus and in the tool's diagnostics, and the glossary published with the build defines it. The vocabulary check reads those marks and holds the glossary to them.

## Design status

This document specifies the approved behaviour and initial defaults. Two builds implement it: a Python prototype that establishes the contract and the fixture corpus and stays in use as a differential oracle, and a production build in Rust with `pulldown-cmark` as the first parser candidate, subject to the verification gates below. The Rust sections state the production build's obligations; the behavioural contract binds both.

## Input and output contract

- **Entry references:** Accept one or more local document or document-plus-fragment *references* and an explicit allowed source *root*. An *entry reference* names the procedure to be carried out, not the routing document the caller read to find it; a routing document reaches the bundle only if something selected links to it.
- **Whole documents:** A reference without a fragment, or with an empty fragment, selects the full document body, including its *preamble*, subject to *frontmatter* stripping and the documented syntax transformations below.
- **Sections:** A nonempty fragment selects an eligible document-level heading and its subsections, ending before the next document-level heading of equal or higher level. A source heading is the only thing that names a *section*.
- **Recursive bundling:** Traverse supported Markdown links within selected content until every reachable local Markdown *target* has been resolved and included.
- **Continuous Markdown:** Emit one bundle Markdown document with one generated H1 per *group* and rewritten links resolving to internal destinations. Do not add per-section metadata envelopes or an enclosing code fence.
- **Groups:** A group is one top-level division of the bundle. By default it is one *source document*, headed by its normalized root-relative path with the Markdown extension removed; under a *grouping rule* it is one merged directory, headed by that directory's *slug* in title case. Emit each selected *region* once. Keep source order among selected content and required heading-only ancestors within a document's group, and within each contribution a document makes to a merged one.
- **Dependency order:** Order groups by root-relative path, a merged group taking its directory's. Discovery order and argument order never decide the arrangement, so one selection always bundles to the same bytes. The grouping rules in force are the only thing that changes where a section sits.
- **Entry line:** Open the bundle with a generated preamble naming each entry reference and linking to the destination it resolved to.
- **Entry identity:** Keep selected entry targets identifiable even when their content is subsumed by a larger included region.

## Parser and source-preserving edits

Use `pulldown-cmark` as the first semantic-parser candidate, behind a version-pinned source-range adapter. Retain original source bytes and apply edits to identified spans instead of regenerating the whole document.

Its `into_offset_iter()` exposes Markdown events paired with source ranges, and `reference_definitions()` exposes the reference-definition map ([pulldown-cmark parser API](https://docs.rs/pulldown-cmark/latest/pulldown_cmark/struct.Parser.html)). These APIs are a starting point, not a guarantee that every destination, definition, or nested edit already has the exact span required by this specification.

- **Parsing authority:** Let the parser identify headings, links, images, definitions, code examples, and HTML nodes, the last so they can be refused.
- **Source positions:** Build the source-range adapter around offset events and reference-definition data. Verify and retain the original spans needed for headings, link/image uses, and definitions; do not equate an enclosing event range with a precise destination span without *validation*.
- **Source model:** Derive block ancestry, eligible section boundaries, and link ownership from the event stream while retaining canonical source identities and *provenance* ranges.
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

Use a versioned `skill-markdown-v1` profile based on CommonMark, with pipe tables and double-tilde strikethrough enabled and source task-list markers preserved. Configure parser options explicitly rather than enabling every available extension; `pulldown-cmark` supports option-controlled event parsing ([parser API](https://docs.rs/pulldown-cmark/latest/pulldown_cmark/struct.Parser.html)).

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

Expose one command, with bundled Markdown on stdout and diagnostics on stderr. Do not add subcommands, remote fetching, watch mode, or persistent caching to the initial interface.

```text
prosiform --root DIR [OPTIONS] REF [REF ...]
```

| Option | Behavior |
| --- | --- |
| `--root DIR` | Required allowed source root; resolve relative configuration paths from the process working directory. |
| `--from DOC` | Root-relative referring document for fragment-only positional references. Positional references naming a file remain root-relative. |
| `-o, --output FILE` | Atomically publish validated output to a file, resolved from the process working directory; default or `-` means stdout. A path naming an input source is refused. |
| `--group SLUG:DEPTH` | Merge every document under a directory named `SLUG` at source heading level `DEPTH`, which is 1 through 6; repeatable, once per slug. Documents no group names keep their own group. |
| `--check` | Discover, bundle, and validate without emitting or publishing the bundle. |
| `--diagnostics text\|json` | Default human-readable diagnostics, or JSON Lines on stderr. |
| `--version` | Report tool version and profile identifier. |
| `--help` | Show usage, defaults, and exit-status meanings. |

Each resource budget adds one option of its own, declared with its default and its counting rule at Resource limits.

`--check` accepts `--output FILE`, validating the run without writing that file. Optional manifests and dependency explanations can be added later without changing the core invocation.

A command line the grammar above does not admit is refused with `E_INVALID_USAGE`. A missing `--root`, no entry reference, an option the contract does not declare, an option value outside the set its row names, a fragment-only reference with no `--from`, and an output path naming an input source are all one defect — the command line's own form — and they lead a caller to one remedy, so they take one code and the message says which fault it was. A grouping rule keeps `E_INVALID_GROUP_RULE`, which names a defect in the rule's value rather than in the grammar that admits the option. A `--root` naming no directory is well formed and names a root that is not there: it fails with `E_ROOT_NOT_FOUND` as the input failure it is.

### Usage examples

```bash
# A procedure and everything it reaches. The routing document the caller
# read to find it, SKILL.md, is not an entry reference and is not bundled.
prosiform --root example/work-tracker modes/plan-mode.md

# Grouped: every document under a named directory merged at a heading level.
prosiform --root example/work-tracker \
  --group artifacts:2 --group modes:2 \
  modes/plan-mode.md

# Multiple selected targets.
prosiform --root example/work-tracker \
  'artifacts/epic-issue-body.md#record-epic-delivery' \
  'artifacts/epic.md#delivery-findings'

# A referring document supplies context for a bare fragment only.
prosiform --root example/work-tracker \
  --from artifacts/epic-issue-body.md \
  '#record-epic-delivery'

# Full compilation and validation, without publication.
prosiform --root example/work-tracker --check \
  'artifacts/epic-issue-body.md#record-epic-delivery'
```

Each example runs against `example/work-tracker`, a tree this repository carries, and the corpus executes it under `fixtures/usage-example/`, so an example that stops being a valid invocation fails a run. Missing references produce the specified diagnostics.

## Explicitly linked source structure

Common rules, file-level prerequisites, and shared SKILL.md instructions will be refactored into addressable sections. Operations must link to the sections that govern them, so the tool can obtain the required context through explicit links.

- **Generic bundling:** Do not infer prerequisite semantics from file names or section names. Do not automatically import all of SKILL.md or ancestor body content; a heading-only *structural ancestor* supplies structure, not additional governing instructions.
- **Explicit dependencies:** A section's author is responsible for marking any required shared rules or context, and a marked reference is part of the recursive dependency graph. Linking cites material; marking requires it. A document therefore cites shared material that sits outside the allowed root without putting the bundling outside that root, and a skill stays bundleable with its own directory as the root however widely its prose refers.
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

Emit exactly one document-level H1 for each contributing source file, using its normalized root-relative path with the Markdown extension removed. Escape the path as literal heading text so punctuation in it cannot create links, images, or inline HTML.

All content from that source belongs beneath its file heading. The output has no additional master heading above these file groups; source documents with the same basename in different directories remain distinguishable by their root-relative paths. Two documents whose paths differ only by Markdown extension produce two file headings a reader cannot tell apart, and fail with `E_AMBIGUOUS_FILE_GROUP`.

- **Absorbed title:** The file heading absorbs a source's first heading when that heading is the document's only H1 and its slug equals the slug of the final segment of the file heading's path. Both sides are slugged, so the capitalization and spacing a filesystem carries decide nothing: a document named `My Note.md` whose title is `My Note` is absorbed, as one named `my-note.md` is. An absorbed title is not emitted and contributes no destination segment, because the file heading already names it. A reference to it resolves to the file heading's own destination, so a document's self-reference to its title reaches the heading a reader sees carrying that text.
- **Group shift:** Every emitted source heading in a file group moves down exactly one level: H1 becomes H2, H2 becomes H3, and so on. A group whose title was absorbed keeps its source levels, the file heading having taken the level the shift makes room for. Preserve visible heading text and relative depth; do not renormalize selected roots independently.
- **Heading syntax:** Shift ATX headings by editing their heading syntax. Convert Setext headings to equivalent ATX headings when required, preserving their visible text and inline semantics, including multiline source forms.
- **Containers:** Apply the same level shift to real headings within retained containers without removing or changing the container structure. Heading-like text inside code remains untouched.
- **Preamble:** A selected document's preamble appears after its filename H1 and before its first retained source heading.
- **Source order:** Within each file group, emit selected regions and structural ancestors in their original source order.
- **Depth overflow:** Fail with `E_HEADING_DEPTH_OVERFLOW` before publication if any emitted source heading or structural ancestor would require a level beyond H6. Do not flatten it, clamp its level, or emit H7-like text as if it were a heading.

The hierarchy guarantee is the original selected source outline beneath one additional file level. File headings isolate source documents, while destinations are assigned over the bundle as a whole, so two files contributing a section of the same name stay distinguishable.

### Grouping

A group is the unit the bundle is organized into. By default a group is one source document, headed by its path. A group changes that for part of the tree: `--group SLUG:DEPTH`, repeatable, names a directory slug and a source heading level, and every document under any directory of that slug is merged at that level.

```text
--group artifacts:2 --group references:2
```

A grouping rule is refused with `E_INVALID_GROUP_RULE` when its depth is outside 1 through 6, when its slug names no directory under the allowed source root, or when a slug is given twice. A depth outside the range and a slug given twice are faults in the command line's own form and exit 2; a slug naming no such directory is a fault in the tree the rule points at and exits 1, as a reference naming no document does. A code names a defect and an exit status names a category of outcome, so one code decides either status according to the fault it names. A rule whose directories contribute no document to the *closure* is not an error: it arranges nothing, and the run reports it as `W_EMPTY_GROUP_RULE` on stderr.

- **Group membership:** A document belongs to the group whose slug matches the deepest directory segment of its path. A document no group matches keeps its own group, so one bundle can carry both arrangements.
- **Group structure:** A group emits one H1 carrying its slug, then one H2 for each distinct source heading text at its depth, each holding every *member* document's contribution. A source heading at the grouping depth becomes that H2; the level below becomes H3, and so on.
- **Verbatim names:** A merged heading keeps its source text. Nothing is prefixed, qualified or renamed where the text occurs once in its group.
- **Document-keyed sections:** A merged section carrying body text above its first subheading, from more than one document, is the document's section rather than a container of named items, and splits into *variants*: one variant heading per contributing document, with that document's text and subheadings beneath it. Every mode's `Procedure` merges this way, since a procedure is the mode's own. A section carrying only named items, such as `Operations`, does not. This test is applied first, and a section it splits is arranged by document throughout; the rule below applies to the names inside a section it leaves alone.
- **Variants by document:** Where two or more documents contribute one heading text to one merged section, that text is emitted once as a heading of its own and each document's content hangs beneath it under a variant heading naming the document. The variants of a name then sit together, so a reader comparing them reads one place rather than several. A variant heading is the shortest run of that document's root-relative path which distinguishes it from the others, in title case, measured after dropping the leading segments they all share, since those are the context the group heading already states. Each document's own heading is replaced by the shared one, and its content shifts one level to sit under its variant heading.
- **Residual ambiguity:** Qualification separates documents, not headings within one. Two headings of one document colliding in one group is the source ambiguity the heading rules already refuse. Anything still coinciding, such as a generated group heading matching a section name elsewhere, takes the renderer's ordinal as any repeat does.
- **Group naming:** A group's heading is its directory slug in title case, so `artifacts` is emitted as `Artifacts`.
- **Document content above the grouping depth:** A group carries an `Overview` section holding each member's selected content above the grouping depth: its preamble, and the body of any section shallower than that depth with its outline beneath. Each member contributes one subsection, named by that document's stem in title case, less a trailing word the section already states: `artifacts/epic-issue-body.md` contributes `Epic Issue Body` under `Artifacts` / `Overview`. A member's own H1 is absorbed by that subsection heading when its slug equals the stem, as a file heading absorbs the title it carries. That heading is where a whole-document reference to the member resolves. A member with nothing above the grouping depth gets no heading, and a whole-document reference to it resolves to its first contribution. A preamble reaches the bundle only through a whole-document selection, since it belongs to no section.
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
- **Internal links:** Rewrite each marked link to the destination of the target it resolved to, using the same map that produced it, whether the link names another file or a fragment of its own. A reference the run resolved is a reference the bundle carries, so every one of them has a destination; an unmarked local Markdown link resolved to nothing and is emitted as the author wrote it, under the link classification rules.
- **Visible headings:** Preserve selected source heading text while shifting levels by the group's shift. Nothing is inserted at a destination; the heading and its position in the outline are what the destination names.
- **Uniqueness:** Each destination occurs once in the bundle and each rewritten link resolves to exactly one of them. The ordinal makes this true by construction and validation establishes it, rather than leaving it to the chance that no two headings coincide.

### Resolvable where the bundle is read

A destination is the fragment the renderer itself would generate, so every internal link resolves: in a Markdown renderer, in an editor preview, and for an agent reading the document whole. The bundle needs no anchor elements and no identifiers to achieve this, because the headings it already emits are what the renderer indexes.

An ordinal is safe here in a way it is not in a source document. In a source, an edit elsewhere changes how many similar headings precede a target, so a stored link silently repoints. A bundle is generated whole in one pass and validated against the map that produced it, so every ordinal it carries is assigned and checked in the same run. A bundle is not a source: it is not hand-edited, and no link into one outlives the run that wrote it.

### Entry line

The bundle opens with a preamble of its own: one generated line naming each entry reference and linking to the destination it resolved to, followed by a statement that the remainder is material those entries reference.

```markdown
This bundle was built for [Plan Mode](#plan-mode); everything else is material it references.

# Artifacts
```

- **Link text:** The visible text of the heading the destination names, so what the line says and what the reader finds agree. Under a grouping rule that is the member's *overview* subsection, which is a name the caller cannot derive from the reference it supplied.
- **Order:** Several entries are named in bundle order — the groups in root-relative path order, and inside one group the headings in source order — followed by the closing statement. Each name is separated from the next by a comma and the last from the one before it by `and`. The order is the bundle's rather than the command line's, so one selection opens on one line however its entry references were written, and a reader meets the names in the order the document that follows carries them.
- **No execution verb:** The line states what the bundle was built for. It does not instruct the agent to carry anything out, because the tool does not know whether an entry names a procedure, and execution verbs belong to the authored instructions.
- **Generated structure:** The line is recorded with the group, file and variant headings as generated structure, not as selected content, so it counts toward no source's coverage. Its links are ordinary internal references and are validated as such.
- **Reading scope at the point of use:** A bundle can hold several documents' procedures. The line is where the bundle says which one it was built for, so the distinction between the material to act on and the material it references survives into the document the agent actually reads.

The line is not a detection signal. An authored document may legitimately open with links into its own sections, so generated-input detection continues to rest on the file heading alone.

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

1. Resolve entry references and allowed source paths.
2. Read and parse each distinct source file once during discovery, capturing its identity and content hash and excluding leading frontmatter from bundled content.
3. Index source headings, links, definitions, ownership, and eligible section boundaries.
4. Discover the recursive dependency graph and expand included source coverage to a fixed point.
5. Consolidate selections, group them by source file, and derive required heading-only ancestors. Check shifted heading depths and assign each emitted heading its destination in bundle order, without treating structural ancestors as new dependencies.
6. Apply source-local reference conversions, rewrite destinations and heading syntax, and construct the candidate with one filename H1 per source.
7. Reparse in candidate-validation mode and compare with selected source constructs, including target integrity, unintended new references, coverage, namespaces, and block boundaries. Do not reload the candidate through source-input validation.
8. Recheck every source against its captured content hash and canonical path identity; fail if a source has changed, disappeared, or resolved elsewhere.
9. Publish the validated document; otherwise fail with actionable diagnostics.

**Expanding coverage:** If a later reference includes an ancestor section or whole document, replace narrower duplicate selections with the larger region. Traverse dependencies in newly included content before declaring compilation complete.

Keep parsed-file caching separate from included-region tracking. Reach a fixed point before final emission, and retain mappings from all selected targets to their consolidated destinations.

## Self-reference and ancestor-reference behavior

Direct self-reference is invalid, while a nested reference back to an ancestor resolves to the existing ancestor destination. This distinction is confirmed and is evaluated using source-section identity, not merely file identity or the scope of the entry argument.

- **Direct self-reference:** A marked link from section A to the same canonical section A fails with `E_SELF_REFERENCE`. A mark asks the bundle to carry the node the link is written in, which is the node already carrying it; an unmarked link naming its own section is a mention, and the bundle emits it as authored.
- **Ancestor reference:** During traversal A → B → A, B's reference to A becomes an internal link to the existing A destination. Do not expand or duplicate A.
- **Shared dependency:** A → C and B → C include C once; both links resolve to its destination.
- **Different section in the same file:** A link to a distinct section is not a direct self-reference solely because the file is the same.
- **Equivalent references:** Determine identity after canonical path and fragment resolution, rather than comparing the literal link strings.
- **Link ownership:** Assign each link to the innermost eligible source section containing its position, including inline content in that heading. Links in nested containers belong to that enclosing eligible section. Ownership does not change when a whole document or ancestor section is selected.
- **Whole-document selection:** Selecting `guide.md` does not make its links to `guide.md#section` self-references. A document node and its heading-section nodes are distinct identities.
- **Preamble ownership:** Content before the first eligible heading belongs to the document node. A link from that preamble to the same whole-document node is a direct self-reference; a heading-section link back to its whole document is an ancestor inclusion, not a direct section-to-itself link.

Store link ownership separately from selected inclusion ranges. Consolidating a child section into a larger region must not change whether one of its links is a direct self-reference.

## Frontmatter policy

Strip leading source frontmatter from every included document, including whole-document entries. Use deterministic delimiter scanning, without parsing or executing YAML.

1. Accept and remove one optional leading UTF-8 BOM.
2. If the first physical line after the BOM is exactly `---`, excluding its LF or CRLF terminator, treat it as the frontmatter opener.
3. Close at the next physical line exactly equal to `---` or `...`, excluding its terminator.
4. Strip the opening line, metadata content, closing line, and the closing line's terminator when present.
5. Preserve subsequent body content, including following blank lines.
6. Fail with `E_UNTERMINATED_FRONTMATTER` when a recognized opener lacks a closing delimiter.

Do not recognize indented delimiters, trailing spaces on delimiters, TOML `+++`, or JSON metadata as v1 frontmatter. A document intended to begin with a literal horizontal rule must use another spelling, such as `***`, rather than the reserved leading `---`.

A BOM is allowed before the opener, but an actual leading blank line means the following `---` is body content. Keep original source coordinates for diagnostics, and do not strip YAML examples in code blocks or non-leading thematic breaks.

Discard metadata without validating YAML values. Count it toward input-size limits, but never discover dependencies in it or emit or execute it.

## Link classification and resource handling

A reference is a dependency when its author marked it as one, it carries no scheme and no authority, and it resolves to a Markdown file under the allowed root. Everything else is text the bundle carries unchanged, an unmarked local Markdown link among it. The tool guarantees internal resolution for the first kind and claims nothing about the second.

A mention is not a dependency. An author naming a document without marking the link has recorded that the document exists, not that the bundle must carry it, and only the author can tell those apart: no shape a reference takes distinguishes them, which is why the shape is not what decides.

- **The mark:** A dependency's link text opens with `¬`, as in `[¬ Record Epic Delivery](epic-issue-body.md#record-epic-delivery)`. The character is ordinary text to the profile, so marking adds no construct the grammar must recognize and a renderer that knows nothing of this tool displays the link. The mark is authoring syntax rather than content: a rewritten link carries the text that followed the mark and not the mark itself, and the spaces or tabs separating the two go with it, so `[¬ the rules]` and `[¬the rules]` both carry `the rules`. A line break is content the author wrote rather than that separator, and survives where one follows the mark.
- **Marked local Markdown document links:** Resolve, recursively bundle, and rewrite to bundle destinations. Resolve relative paths from the originating source document, never from whichever document happened to discover it.
- **Unmarked local Markdown links:** Emit as authored. The reference is not resolved, the document it names is not opened, and the link is not rewritten even where the bundle carries that document because another reference marked it. What one author marked cannot change what another author's reference says.
- **Fragment-only links:** A marked fragment-only link resolves against the original source document's heading index, then follows the same bundling and rewriting rules. An unmarked one is emitted as authored.
- **Everything else:** A reference carrying a scheme or an authority is not a local document reference. Emit it as authored and never open, fetch or interpret it. No scheme is permitted or refused, because which scheme it carries decides nothing: carrying one at all is what puts the reference outside the tool's interest. Images and other non-Markdown references are text by the same rule.
- **A marked resource:** Marking a resource fails with `E_MARKED_RESOURCE`. A resource is a reference that is not a local Markdown document, and an image whatever it points at: image syntax embeds rather than links, so a document named that way is no more bundleable than a picture. A mark means bundle this and a resource is never bundled, so the request cannot be met. Emitting it as authored cannot meet it either: the mark is dropped by the rewrite and a resource is never rewritten, so the bundle would carry a mark, which the mark's own rule forbids.
- **Unsupported local-document syntax:** Fail with an actionable diagnostic rather than silently excluding a local Markdown dependency. In v1, raw HTML links to local Markdown are rejected unless explicitly supported by the parser and resolver.
- **Examples:** Do not follow apparent links inside code spans, fenced code blocks, or other literal example content.

## Reference normalization and path identity

Require an explicit allowed source root and canonicalize that root once. Command-line document paths are relative to the root; links inside sources are relative to their originating document's directory.

The root is the caller's confinement boundary, not a claim about how the sources are organized. It must contain every document the entry references reach: a collection that shares material with a sibling collection is rooted above both, since a reference leaving the root fails whether or not its author meant it. A refused reference therefore says the root is too narrow at least as often as it says the link is wrong, and the diagnostic names the resolved path so the caller can tell which.

A fragment-only command-line reference requires `--from DOC`; otherwise it fails. File-naming positional references remain root-relative even when `--from` is present. A fragment-only source link uses its source document automatically.

### Resolution sequence

1. For authored Markdown links, obtain the destination from the parser with Markdown escapes and entities interpreted once. CLI reference arguments enter directly as URI-reference strings.
2. Split URI components before percent-decoding so encoded `#` and `?` remain filename characters rather than becoming delimiters.
3. Emit any reference carrying a scheme or an authority as authored, and resolve no further.
4. Reject any query component on local Markdown document references, including an explicitly empty query.
5. Strictly validate percent escapes and decode path and fragment exactly once as UTF-8. Look up the decoded source fragment exactly; do not lowercase or re-slug it.
6. Reject NULs, control characters, decoded path separators originating from escapes, and remaining backslash separators. Local paths use forward slashes in v1.
7. Normalize `.` and `..` relative to the proper reference base. Permit normalized internal `..`, but reject paths outside the allowed root.
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
| `sub/../guide.md#run` | Normalize to `guide.md#run` when confined to the root. |
| A normalized path outside the root | Fail with `E_SOURCE_OUTSIDE_ROOT`. |

A schemeless reference that is not a relative path confined to the root fails explicitly: a root-relative path beginning with `/`, a filesystem absolute path, and a platform-specific drive path each name a local document the root cannot contain, and refusing them keeps an intended dependency from being dropped in silence. This restriction applies to document references, not to the configuration path naming the allowed source root.

### No-symlink source policy

Reject Markdown source paths containing symlinks below the canonical source root with `E_SOURCE_SYMLINK`. Do not let dependency bases vary according to which logical alias was discovered first.

Use rooted, no-follow access or equivalent safeguards, not merely a pre-open string check. Platforms unable to enforce the policy must fail or declare a narrower supported environment rather than silently weakening root confinement.

Non-Markdown resource links are not opened as source dependencies. They remain governed by the resource policy.

## Resources are text

A relative image or other non-Markdown reference is text. It is emitted byte-identical to its source and never opened, rebased or resolved, so a bundle read from somewhere other than its source directory may not find it.

A bundle carrying at least one resource reference warns on stderr with `W_RESOURCE_PORTABILITY` that resource portability is not guaranteed. A successful Markdown bundling establishes nothing about the resources its text mentions, and the warning does not turn a successful run into a failure. A bundle whose text mentions no resource carries nothing to warn about and emits the warning not at all.

Rebasing a resource path means deciding where the bundle will be read from, which is the caller's question rather than the tool's. Nothing here maps a resource to a URL, so the tool holds no notion of a web address at all.

## Resource limits

Use deterministic configurable limits and fail rather than truncate. These are approved initial engineering defaults, not benchmark-derived limits or guarantees about an agent's context capacity.

| Option | Default | Counting rule |
| --- | --- | --- |
| `--max-files` | `256` | Distinct normalized source-document identities opened. |
| `--max-file-bytes` | `1,048,576` | Raw bytes in one source, including frontmatter and any BOM. |
| `--max-input-bytes` | `16,777,216` | Sum of raw source bytes, once per source identity. |
| `--max-output-bytes` | `262,144` | Complete UTF-8 bundle, including filename headings, structural ancestors, and separators. |
| `--max-targets` | `4,096` | Distinct canonical document/section targets discovered, even if later subsumed. |
| `--max-links` | `32,768` | Authored link/image occurrences examined in selected content, once per source occurrence. |
| `--max-nesting` | `64` | Supported syntactic container nesting; exceeding the limit is an error. |
| `--max-expansion-depth` | `8` | Link hops from the nearest entry reference to a reached target, counted along its shortest path. |

Crossing any of these fails the compilation with `E_RESOURCE_LIMIT`, and the diagnostic names the budget crossed and the figure that crossed it. One code covers all eight because one remedy does: the sources are restructured or the number is raised, and the figure the run reports is what says which.

Accept positive decimal integer overrides; zero must not mean unlimited. Traverse iteratively; the expansion-depth budget is a declared constraint on how far a chain of references may reach, not a recursive-call-depth cap, and a cyclic graph within the budget bundles normally.

*Expansion depth* constrains the shape of a reference graph rather than its size, which the file, byte and target budgets bound. It exists so a document reaches what governs it directly, and a chain that outgrows the budget is a prompt to restructure the sources rather than to raise the number.

Enforce `--max-nesting` as an explicit failure, not merely a parser option that could silently reinterpret over-deep syntax. Apply necessary parsing-safety limits to the complete opened source being indexed, even when the requested section is narrower, and include that enforcement in the parser fixture gate.

The wrapper must enforce any smaller transport limit; 256 KiB is not universally safe for agent delivery. Do not estimate tokens by dividing bytes by a constant; future token budgets must name and pin the tokenizer.

## Source consistency

Read each distinct source once during discovery and keep its parsed content, canonical identity, and content hash for the entire compile. Before publication, recheck all sources and fail with `E_SOURCE_CHANGED` and a retry message if any content or identity has changed. One code covers a source that changed, disappeared or resolved elsewhere: each is the same fact, that the bytes discovery captured are no longer the bytes the path names.

This is change detection, not a transactional filesystem snapshot: files can change again after a check. When strict reproducibility is required, bundle from an immutable source snapshot; do not claim that hashing alone supplies cross-file atomicity.

## Generated input policy

Rebundling of prosiform output is unsupported in v1. Reject an input document whose first heading is a document-level H1 whose text, with a supported Markdown extension appended, names a document under the allowed source root **other than the document being read**, with `E_GENERATED_INPUT`.

A bundle's first file heading names its first contributing source, which is never the bundle itself, so ordinary unmodified output identifies itself without a metadata wrapper. An authored document titled with its own name points at itself and is not detected: a document at `My Note.md` headed `# My Note` is the absorbed title's worked example and bundles. A heading-like example in code is not a heading and does not trigger detection.

The destinations themselves can no longer carry this signal, since a bundle's links are ordinary fragments indistinguishable from an authored one. Detection rests on the file heading alone, which is weaker: it is not proof of origin or a security signature, rewriting that heading defeats it, and no detection of arbitrary modified derivatives is claimed. A merged group is headed by a directory slug rather than a path, so a bundle whose every group is merged carries no file heading and is not detected. Rebundling it is unsupported on the same terms, and v1 claims no detection of it.

## Agent delivery contract

Successful compilation establishes that the complete candidate passed validation. It does not establish that a downstream tool transport delivered every byte to the calling agent.

- **Exit status:** The agent-facing wrapper must check process success rather than interpreting the mere presence of Markdown as a successful read.
- **Response limit:** The wrapper must buffer or otherwise verify complete output and enforce a response-size limit compatible with its transport. If it cannot deliver the whole document, return a *delivery* failure rather than a truncated apparent success.
- **Entry destinations:** On success, report each entry reference and the destination it resolved to on the diagnostic stream, in the declared format, so a caller can act on it as data. The report carries `W_ENTRY_DESTINATION`, a warning because it accompanies a run that succeeded. The bundle states the same thing in its entry line, which is what reaches the agent.
- **Clean Markdown:** Keep success stdout limited to the bundle document. Beyond the entry line, the bundle carries no generated commentary: completion metadata, byte counts, warnings, and diagnostics belong in the wrapper's structured result or a sidecar, never in per-section Markdown envelopes.
- **Broken pipes:** Report transport/write failure through a nonzero exit when detectable. Do not claim that stdout can be atomically delivered to every consumer.
- **No silent fallback:** Do not replace oversized output with a summary, a partial document, or references that the agent must follow separately.

## Validation scope

Validate link resolution, self-reference, supported selected syntax, and resource rules within the selected dependency closure. Parsing a complete file for indexing does not make its unselected sibling sections dependencies; ancestor-only headings undergo structural, depth, and namespace checks but not dependency traversal.

Whole-file checks are limited to facts needed for safe access or correct interpretation: source identity and encoding, raw-byte and required parsing-resource limits, frontmatter, source-change detection, original heading enumeration, definitions needed by selected uses, ambiguity of requested fragments, and generated-input detection.

An unrelated broken link or self-link in an unselected sibling must not fail bundling. If closure expands to include that sibling, its links become subject to validation.

An opened file can nevertheless fail because an unselected construct exceeds a declared file-wide parsing-safety limit. Diagnose this as inability to safely index the containing source, not as an inferred dependency on that sibling.

Keep `--max-links` scoped to authored occurrences in the selected closure. If full-file indexing needs another work budget or instrumentation, specify it separately rather than silently changing that option's meaning.

### Source and candidate validation modes

Use the same declared Markdown grammar where applicable, but separate the policy context for source validation from candidate validation.

- **Source mode:** Enforce source-root and generated-input rules, source-fragment resolution, and source-owned self-reference checks. A source fragment names one heading and carries no ordinal.
- **Candidate mode:** Accept generated filename headings, shifted headings, and structural ancestors. Validate destinations, coverage, reconstructed outlines, block structure, and reference invariants against source provenance.
- **Ownership:** Retain original source ownership independently of output heading levels. Validate the reconstructed outline against that model rather than assigning synthetic file/structural ancestor headings executable ownership.
- **Preprocessing:** Do not pass the candidate back through source frontmatter stripping, dependency discovery, or generated-input rejection.
- **Reuse:** The producer's candidate may pass candidate validation, while that same document supplied to a later invocation remains invalid under the generated-input policy.

## Validation and failure contract

Validation is mandatory. Failures must give the calling agent enough information to explain the problem to the user or halt safely.

- **Resolution:** Every supported local Markdown reference resolves to a known document or section.
- **Target integrity:** Every rewritten link points to the intended source-derived destination, not merely a section whose slug happens to coincide.
- **Uniqueness:** Each bundle destination occurs once, and resolves in the renderer that reads the bundle.
- **Boundaries:** Combining sections must not make later material part of an earlier code fence, HTML block, or unintended container.
- **Preservation:** Preserve selected instruction wording and code under the declared transformations: leading BOM removal, frontmatter stripping, reference-use conversion, definition removal, destination rewriting, title absorption, heading shifts and necessary Setext conversion, the generated entry line, generated group, variant and overview headings, heading-only ancestors, Markdown escaping, and boundary whitespace. Untouched non-heading bytes and code examples are not reformatted or repaired.
- **Completeness:** No content is silently dropped to satisfy resource limits, and no failed dependency is silently omitted.
- **Safety:** Enforce the allowed source root and configured resource limits. Never execute included commands, and never open a reference the tool did not resolve as a local Markdown dependency.
- **Publication:** Compile failures return nonzero status and no bundle on stdout. Diagnostics go to stderr. File output should be published atomically only after successful validation. An output destination that refuses the write, a detected broken pipe among them, fails with `E_PUBLICATION_FAILED`.

### Post-compilation invariants

Validate the completed document against the source-to-output mapping, not only its surface syntax.

- **One intended destination:** Each rewritten link resolves to exactly one destination corresponding to its intended original document or section, and that destination is the fragment the declared renderer generates for the heading it names.
- **Reference preservation:** Each link/image use in selected source content retains its visible content and title and reaches its intended destination under the resource policy. Structural ancestor-only titles intentionally contain no live source links or images.
- **No new links:** Source text parsed as literal bracketed text must not become a new link or image through bundling.
- **No definition leakage:** No original link-reference definition nodes survive emission; literal examples of definitions remain unchanged.
- **Exactly-once coverage:** Each selected source region's content is represented once after unioning overlaps, excluding a removed leading BOM, stripped frontmatter, and removed reference definitions. Parent inclusion satisfies child inclusion without another copy.
- **No accidental omissions:** Selected-content coverage equals the resolved dependency closure under the documented transformations. Track generated structure separately so it cannot conceal a missing selected region.
- **No accidental expansion:** The only unselected source-derived content emitted is required heading-only ancestry. Never include an unselected ancestor's body or siblings merely to supply structure.
- **Ownership stability:** Link ownership and direct-self-reference classification remain the same before and after overlap consolidation.
- **Block-syntax preservation:** Generated headings and region boundaries must not absorb content into unintended non-heading containers.
- **Entry line integrity:** The bundle's entry line names every entry reference and no other, and each of its links resolves to the destination that reference's target was assigned.
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

An unexpected internal error carries `E_UNEXPECTED_INTERNAL_ERROR`. It names the run rather than any document the run read, so a caller reading it is not sent to look at its sources.

Every failing outcome this contract names carries a code, so a diagnostic without one reports a defect the contract does not define.

With `--diagnostics json`, emit one JSON object per stderr line, including `severity`, `code`, `message`, location, original reference, resolved identity when available, inclusion chain, and remedy when accurate. The resolved identity is named `resolved`: a bundle destination where the reference reached one, and a canonical source path where it reached a document. Do not mix JSON diagnostics with progress prose.

## Adversarial acceptance fixtures

Before broad implementation, create small fixtures with exact expected bundles or expected failures.

- **Identity:** Whole-file bundling with internal section links; direct self-links through heading names; ancestor back-references; preamble-to-document self-links; same-file cross-section links.
- **Coverage:** Child-first then parent inclusion; whole-document inclusion discovered late; shared dependencies; multi-file cycles; different entry argument orders.
- **Destinations:** A unique bundled heading taking a bare slug, repeated bundled headings taking ordinals in bundle order, a source fragment ambiguous within one document refused, two documents whose paths differ only by Markdown extension refused, same-basename paths in different directories, and a file group whose filename heading does not imply whole-document inclusion.
- **References:** Definitions outside a selected section, conflicting labels, unused definition removal, unresolved bracketed text remaining literal, reference-style images and titles, fragment-only links, and unsupported raw HTML document links.
- **Extraction:** ATX and Setext roots, rejection of nested-heading targets, nested headings not terminating outer selections, and original duplicate numbering including ineligible headings.
- **Boundaries:** Unclosed fences, HTML blocks, adjacent lists, nested containers, file-group separation, leading frontmatter, and YAML examples that must remain intact.
- **File hierarchy:** Same-basename sources in different directories; the Markdown extension absent from the filename heading; paths needing Markdown escaping; a group whose title the file heading absorbs and one whose H1 it does not; a document carrying more than one H1; H1–H5 shifts; H6 overflow; Setext and multiline-heading conversion; and unchanged heading-like code examples.
- **Grouping:** One entry bundled with and without a group, selecting the same content; a merged section drawn from several documents; a name occurring once left bare; a name several documents carry emitted once with a variant heading each, distinguished at one path segment and at more than one; a merged section carrying body text from more than one document split by document; a document no group matches keeping its own group; a whole-document reference to a member resolving to its overview subsection, and one to a member with no preamble resolving to its first contribution; a reference to a grouping-depth heading resolving to the variant carrying the document it named; a member's shallower section carried under its overview subsection; a section split by document taking precedence over the names inside it; and a rule refused for its depth, its unknown slug or its repetition.
- **Partial outlines:** Disjoint selections such as Alpha and Beta/Detail; deduplicated ancestor structural ancestors; original skipped heading levels; ancestor promotion after dependency expansion; and no ancestor-body or structural ancestor-link dependency leakage.
- **Entry line:** One entry and several; an entry whose destination is a file heading and one whose destination is an overview subsection under a grouping rule; the link text matching the heading it names; and the line counting toward no source's coverage.
- **Wrapper identity:** A partial file group's document destination does not satisfy a whole-document dependency without expanding its selected content.
- **Normalization:** Empty fragments, query rejection, percent-encoded delimiters, double-encoded percent sequences, invalid escapes, root escapes, internal `..`, symlinked files/directories, and unsupported path forms.
- **Resources:** An image, a script link and a relative path inside a command example each emitted byte-identical, with the portability warning on stderr.
- **Consistency:** Source modification, deletion, or changed canonical identity during compilation.
- **Validation scope:** Unselected broken/self-referential siblings do not fail a narrow run but do fail when later included.
- **Generated inputs:** Reject a source opening on a file heading, while ignoring a heading-like example in code and an authored title that merely contains a slash.
- **Delivery:** Nonzero process exit, output-budget failure, broken output pipe, wrapper rejection of transport-oversized output, and a successful run reporting each entry reference's destination, with and without a grouping rule.
- **Parser fidelity:** Exact ranges for multiline references, reference-style images, nested image/link edits, tables, tabs, Unicode, escapes, CRLF, and original diagnostic coordinates.
- **Definition inventory:** Remove every selected definition occurrence, including duplicates, unused labels, case-fold-equivalent labels, multiline definitions, and supported containers, without changing original winner selection.
- **Parser exhaustion:** Trigger reference-expansion suppression below the tool's public input/output limits and require an explicit failure. Include a case that consumes the budget on its last valid reference with no later lookup, which must not falsely claim omitted references.
- **Validation modes:** Candidate validation accepts generated filename headings and structural ancestors, confirms each destination against the renderer's own slugging, and preserves saved source ownership; a subsequent source invocation rejects the generated document.
- **File-wide safety:** Excessive parsing depth in an unselected sibling can fail with a file-indexing resource diagnostic, while an ordinary unselected broken link does not.
- **Profile:** Task markers protected from definitions, disabled typographic rewriting, Markdown suffix classification, and explicit rejection of unsupported selected dependency constructs.
- **Frontmatter:** Optional BOM, exact opening/closing delimiters, `...` termination, leading-blank-line distinction, malformed delimiters, and missing closers.
- **CLI:** Root versus `--from` resolution, `--check` with an output file and no publication, clean JSON diagnostics, and documented exit statuses.
- **Limits:** Every limit fails at the first exceeded boundary without truncation; zero/negative overrides fail; parser nesting cannot silently fall back to different syntax.

## Implementation verification and residual policy detail

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
