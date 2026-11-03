# Glossary

Every term the contract uses, defined once. A term defined here means this and nothing else in the design, the acceptance criteria, the fixture corpus and the tool's own diagnostics. The design italicises a term where it first uses it, and the vocabulary check holds this file to defining each one.

The tool is `prosiform`. It bundles; what it produces is a bundle.

## The act and the artifact

| Term | Definition |
| --- | --- |
| **bundle** (v.) | To resolve a reference closure into one self-contained Markdown document. |
| **bundle** (n.) | One validated document a run produces: the entry's, or one dispatched target's. |
| **candidate** | A bundle before it has passed validation. Nothing is published while a check fails. |
| **profile** | The named, versioned Markdown grammar and option set a run declares. |
| **guide** | What `pf` run with no arguments prints to standard output: the compile step, `pf -o <folder> <destination>` from the skill's directory; the rule that a link whose text opens with `↳` names an inline target, compiled, read whole and followed; that a `⇉` link names a file given to a sub-agent and an `In parallel` section lists several given to their own sub-agents at once; and that a sub-agent returns each question unanswered, in an answer whose first line reads `Question:`. It is the build's own text, so a skill's bootstrap is one instruction: run `pf` and follow it. |

## Sources

| Term | Definition |
| --- | --- |
| **boundary** | The deepest directory holding every local Markdown path a document's own links name, normalised from that document's directory; a document naming none has its own directory. It is derived from the links, so it admits every authored link. |
| **source document** | One captured local Markdown file, recognized by its `.md` or `.markdown` suffix. |
| **section** | A document-level heading and its subsections, ending before the next heading of equal or higher level. The smallest unit a reference can select. |
| **region** | A contiguous span of a source document selected for inclusion: a whole document, or a section. |
| **preamble** | Content above a source document's first heading. It belongs to no section, so only a whole-document selection carries it. |
| **frontmatter** | A leading delimited YAML block, validated and retained as source metadata, excluded from Markdown content and dependency discovery. |
| **preset** | A named mapping of conversion settings a document declares in `prosiform` to govern its own content: `default` is always in force, and each other preset is in force where its name is a word of the title of the section holding the link that reaches the document. An entry reference, which no section holds, selects by the title of the section or document it names, and so does a dispatched target, which compiles as an entry. Distinct from the profile, the grammar a run implements. |

## References

| Term | Definition |
| --- | --- |
| **reference** | An authored Markdown link to a local document or section, or a destination naming one that a `mermaid` diagram link writes: a `click` line, a class diagram's `link` line, or a sequence diagram's `link` or `links` participant menu, its keywords in any letter case. |
| **entry reference** | A reference supplied as an argument. Traversal starts at each one. |
| **target** | The document or section a reference resolves to, after path and fragment normalization. |
| **dependency** | A target a reference resolves to whose document declares `prosiform` in its leading frontmatter, where its author has not withheld it with a deferral, a dispatch operator or a parallel dispatch mark. It is resolved, bundled and rewritten wherever the document sits; a reference naming a document that declares nothing, or none, cites what it names and creates none. |
| **deferral** | An author's statement that a reference is compiled in a run of its own rather than this one, written as a `¬` followed by a space opening the link's text, or written against the composition mark as `¬↳`; a mark followed directly by other text is link text like any other. The target is required to exist and is carried nowhere; the bundle emits the link's text with the mark and the blanks following it removed, and its destination is the target's URI-escaped path from the invocation working directory. The mark is authoring syntax rather than content, because the destination already states the deferral. A deferral naming anything but a Markdown document or section that declares `prosiform` is refused. |
| **dispatch operator** | An author's statement that a sub-agent follows a link's material, written as a `⇉` followed by a space opening the link's text; a mark followed directly by other text is link text like any other, and one written against the composition mark, as in `⇉↳`, is refused, because a dispatch places nothing inline. The target is required to exist and contributes no content, dependency or group membership to the bundle carrying the link; the run compiles it as a bundle of its own instead. The link is published where it is written, with its mark and the one blank after it, pointing at the target's bundle file. A deferral mark written before it, as in `¬⇉`, is refused, because a dispatch is compiled up front into a bundle of its own; text opening with two dispatch marks is refused, and a dispatch naming anything but a Markdown document or section that declares `prosiform` is refused. A dispatch naming the document that writes it warns where it closes no cycle. |
| **dispatched bundle** | The bundle a run compiles for one target its dispatches reach, transitively: each distinct document or section once, as its own entry and under its own budgets, in the run's folder under its own selection's name. A chain of them returning to one already on it is a cycle, and the run publishes nothing. |
| **parallel dispatch mark** | An author's statement that a sub-agent follows a link's material together with the other parallel dispatches of its section, written as a `⫽` followed by a space opening the link's text; a mark followed directly by other text is link text like any other, and one written against the composition mark, as in `⫽↳`, is refused, because a dispatch places nothing inline. It is a dispatch: the target is required to exist, contributes nothing to the bundle carrying the link and compiles to a bundle of its own. The link is published without its mark, pointing at its section's `In parallel` sub-section, or as a `⇉` link to the target's bundle file where its set holds one target. A deferral mark written before it, as in `¬⫽`, is refused, because a dispatch is compiled up front into a bundle of its own; text opening with it and a dispatch operator is refused, and a parallel dispatch mark naming anything but a Markdown document or section that declares `prosiform` is refused. |
| **set** | The `⫽` links in one section's own content, wherever its prose writes them; a child section's `⫽` links form that child section's set. A set of two or more distinct targets points at its section's one `In parallel` sub-section, whose bundles are dispatched together; a set of one is a single dispatch. A set states no order. |
| **parallel dispatch sub-section** | The section a bundle generates for a set of two or more distinct targets: a heading `In parallel` one level below the section holding the set's links, after its own content and before its child sections, listing each target as a `⇉` link to its bundle file under one instruction. A set states no order, and an authored heading equal to it is refused. |
| **arrow** | A scalar whose being a link's whole label states no operation, composition having one mark, so the run refuses the link: an assigned scalar of the Arrows, Supplemental Arrows-A, -B or -C block, or a Dingbats or Miscellaneous Symbols and Arrows scalar whose Unicode character name holds the word `ARROW` or `ARROWS`. |
| **composition directive** | A link whose text opens with the composition mark `↳` followed by a space, alone or after the deferral mark as `¬↳`. A `↳` followed directly by other text is link text like any other. It places the section it names beneath the section writing it: targets sharing a title in that section share one destination section, and each directive contributes the target's content beneath a heading naming the target's parent. The mark requests placement alone and the link's text carries no other meaning; the link is published with its text and the mark removed, pointing at its contribution. A deferred directive keeps its destination section and contribution, whose content a later run compiles under the presets the target's own heading selects, so one whose section's title selects other presets of the target is refused, and so is a section both composed and deferred by one section. A dispatch mark written against the mark is refused, because a dispatch places nothing inline, and so is a link labelled with an arrow. One naming a section of the document that writes it warns, and one composing a section holding it is refused as a cycle. |
| **dispatch depth** | The number of dispatch hops along one chain of bundles, counted from the run's entry: a dispatch the entry carries is the first hop, and a dispatch a dispatched bundle carries is one hop further. A chain deeper than three warns. |
| **closure** | The transitive closure of the reference relation over the entry references: every declaring target reachable by following the references selected content carries. |
| **expansion depth** | Link hops from the nearest entry reference to a target, along its shortest path. |
| **substitution mapping** | The `subst` pairs a document's presets in force state for every reference reaching it in one bundle, each naming a different document or section for one reference that document writes: a key is the identity a reference normalizes to, a key carrying a fragment redirects that section alone and states precedence over a key naming the whole document, and both sides resolve from the declaring document's directory. It is read before classification, closure and rewriting and is applied to the identity a reference normalized to, so every reference the document writes is redirected — a compiled, deferred, dispatched or parallel-dispatched target alike, a reference naming a document that declares and one the run would carry as a citation. A key naming a document that does not exist is redirected like any other. A document's links are written once, so two presets in force for it that map one key to two alternatives are refused. |
| **substitute** | The target a substitution mapping names, which is the target outright rather than an overlay of its bytes: its title, its group and depth, its own declaration and its own links are the ones the run uses, and a bundle reads as if the author had written the substitute's path in the link. |
| **resource** | A reference the bundle carries as text rather than opening: an image whatever file it names, a remote address, any other link naming no local Markdown document. It is emitted as authored and never opened, rebased or resolved. |

## Selection and arrangement

| Term | Definition |
| --- | --- |
| **selection** | The set of regions chosen for inclusion. |
| **consolidation** | Replacing overlapping selections with their union, so each region appears exactly once however many references reach it. |
| **structural ancestor** | A heading emitted with no body, to preserve the outline of a partial selection. Not a dependency, and not a substitute for selecting the section it names. |
| **group** | A division of the bundle: one source document, or contributing documents declaring the same group identity and depth in their metadata. |
| **placement order** | The order the bundle arranges its sources in: each is placed at the first reference that names it, reading the entry references in invocation order and then each placed source's selected content in turn. Groups and the members within a group follow it, so the order an author writes links in sets the arrangement. |
| **grouping rule** | The `group` pair of a source document's preset, pairing a group identity with its grouping depth. |
| **member** | A contributing source document whose metadata declares a named group. |
| **variant** | One of several same-named sections a merged group draws from different documents. Emitted once as a shared heading, with one subheading per source document. |
| **overview** | The section a merged group gathers its member subheadings beneath, where it also emits merged sections. A titled entry member opens its group with its own title and preamble, its sections lead, and the other members' subheadings follow in the overview. |
| **scope** | The section holding a composition directive, at the heading the bundle emits for it. A directive in a preamble, or in a heading the bundle emits as text alone, has none and is refused. |
| **destination section** | The section a scope gains, one level below it, for each heading title its directives' targets carry, headed by that title; directives in one scope naming same-titled targets share one. |
| **contribution** | What one composition directive places in its destination section: a heading naming the target's immediate parent, one level further down, then the target's body and subsections at their relative depth. The directive's link points at that heading. |
| **title case** | The spelling every heading the bundle generates carries: each word of the name capitalized, every separator the name carries kept. It changes letters and not structure, and it reaches what the compiler writes and nothing else. |

## Addressing

| Term | Definition |
| --- | --- |
| **destination** | The fragment naming a place in the bundle: the slug a renderer generates for the emitted heading, with its ordinal where one is needed. |
| **slug** | The identifier a renderer derives from heading text under the declared profile. |
| **ordinal** | The counter a renderer appends when two emitted headings produce one slug. |
| **rewriting** | Repointing a reference at the destination of the target it resolved to. |

## Checking and delivery

| Term | Definition |
| --- | --- |
| **validation** | Checking a candidate against the provenance recorded while building it. Mandatory, and prior to any output. |
| **provenance** | The record of which source region produced which span of the candidate, kept separately from generated structure. |
| **invariant** | A property validation establishes, such as exactly-once coverage or one intended destination per rewritten reference. |
| **diagnostic** | One message a run emits to standard error, carrying a severity, a stable code, the reference or location it concerns, the identity that reference resolved to and the chain of references that reached it where it has them, and a remedy where one is accurate. |
| **publication** | Writing every bundle a run produces — the entry's and each dispatched bundle, its bundle set — once every one has validated, into a folder of the run's own, named for its entry with the `.bundles` suffix, under the output folder, built beside it and swapped in whole. |
| **run folder** | The folder a run publishes its bundles into: the joined name of its entry selections with the `.bundles` suffix, under the output folder `-o` names, which the run makes where absent. |
| **delivery** | Transporting a published bundle to the caller. A successful build does not establish a successful delivery. |

## Terms deliberately not used

| Avoided | Why |
| --- | --- |
| **compositor** | A compositor sets type. It arranges; it resolves nothing. |
| **scaffold** | Scaffolding is removed when building finishes. A structural ancestor is permanent in the bundle. |
| **cohort** | Imported from demography, and earns nothing group membership does not already say. |
| **branch** | Collides with the version-control sense. A same-named section from another document is a variant. |
| **anchor** | The bundle emits no anchor elements. A destination names a heading; it is not an element. |
| **include** | Suggests textual substitution at a point. Selection, consolidation and grouping decide what appears and where. |
