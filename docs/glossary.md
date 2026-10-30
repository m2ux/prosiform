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
| **guide** | What `pf` run with no arguments prints to standard output: the compile step, `pf -o <folder> <destination>` from the skill's directory; the rule that a link whose text opens with `↳` names an inline target, compiled, read whole and followed; and that a bundle opening with a Prosiform section is followed from there. It is the build's own text, so a skill's bootstrap is one instruction: run `pf` and follow it. |

## Sources

| Term | Definition |
| --- | --- |
| **root** | A source's confinement directory. A reference the source carries resolves from the source's own directory, and names a dependency only where it lands inside the root. An explicit declaration resolves from that source's directory; absence uses the invocation working directory. It bounds what the source may include and names no heading, order or output. |
| **source document** | One captured local Markdown file, recognized by its `.md` or `.markdown` suffix. |
| **section** | A document-level heading and its subsections, ending before the next heading of equal or higher level. The smallest unit a reference can select. |
| **region** | A contiguous span of a source document selected for inclusion: a whole document, or a section. |
| **preamble** | Content above a source document's first heading. It belongs to no section, so only a whole-document selection carries it. |
| **frontmatter** | A leading delimited YAML block, validated and retained as source metadata, excluded from Markdown content and dependency discovery. |

## References

| Term | Definition |
| --- | --- |
| **reference** | An authored Markdown link to a local document or section, or a destination naming one that a `mermaid` diagram link writes: a `click` line, a class diagram's `link` line, or a sequence diagram's `link` or `links` participant menu, its keywords in any letter case. |
| **entry reference** | A reference supplied as an argument. Traversal starts at each one. |
| **target** | The document or section a reference resolves to, after path and fragment normalization. |
| **dependency** | A target a reference resolves to under the allowed source root, where its author has not withheld it with a deferral, a dispatch operator or a parallel dispatch mark. It is resolved, bundled and rewritten; a reference resolving outside the root cites the document it names and creates none. |
| **deferral** | An author's statement that a reference is compiled in a run of its own rather than this one, written as a `¬` followed by a space opening the link's text; a mark with no space after it is link text like any other. The target is required to exist and is carried nowhere; the bundle emits the link's text with the mark and the blanks following it removed, and its destination is the target's URI-escaped path from the invocation working directory. The mark is authoring syntax rather than content, because the destination already states the deferral. A deferral naming anything but a Markdown document or section under the root is refused. |
| **dispatch operator** | An author's statement that a sub-agent follows a link's material, written as a `⇉` followed by a space opening the link's text; a mark with no space after it is link text like any other. The target is required to exist and contributes no content, dependency or group membership to the bundle carrying the link; the run compiles it as a bundle of its own instead. The link is published without its mark, pointing at the dispatch sub-section its section carries for the target. A link states one operator, so text opening with two is refused, and a dispatch naming anything but a Markdown document or section under the root is refused. A dispatch naming the document that writes it warns where it closes no cycle. |
| **dispatched bundle** | The bundle a run compiles for one target its dispatches reach, transitively: each distinct document or section once, as its own entry and under its own budgets, in the run's folder under its own selection's name. A chain of them returning to one already on it is a cycle, and the run publishes nothing. |
| **dispatch sub-section** | The section a bundle generates for each target a section of it dispatches: a heading `Dispatch <link text>` one level below that section, after its own content and before its child sections, whose one line names the target's bundle file. A dispatch in a level-6 section leaves no level for one and is refused, and an authored heading equal to one is refused. |
| **parallel dispatch mark** | An author's statement that a sub-agent follows a link's material together with the other parallel dispatches of its section, written as a `⫽` followed by a space opening the link's text; a mark with no space after it is link text like any other. It is a dispatch: the target is required to exist, contributes nothing to the bundle carrying the link and compiles to a bundle of its own. The link is published without its mark, pointing at its section's parallel dispatch sub-section. A link states one operator, so text opening with it and a deferral or a dispatch operator is refused, and a parallel dispatch mark naming anything but a Markdown document or section under the root is refused. |
| **set** | The `⫽` links in one section's own content, wherever its prose writes them; a child section's `⫽` links form that child section's set. Every link of a set points at its section's one parallel dispatch sub-section, whose bundles are dispatched together. A set states no order. |
| **parallel dispatch sub-section** | The section a bundle generates for the set of `⫽` links in one section's own content: a heading `Dispatch in parallel` one level below that section, after its own content and its dispatch sub-sections and before its child sections, listing each target's bundle file once with its link text. A set states no order. |
| **Prosiform section** | The section a bundle that dispatches opens with, stating the protocols its dispatch and parallel dispatch sub-sections follow: `# Prosiform`, then `## Dispatch` whenever the bundle dispatches and `## Parallel dispatch` when it carries a set, in wording the profile fixes, so each protocol is the same bytes in every bundle. It is the bundle's first heading, and a bundle dispatching nothing carries none. An authored heading equal to one of its headings is refused. |
| **dispatch depth** | The number of dispatch hops along one chain of bundles, counted from the run's entry: a dispatch the entry carries is the first hop, and a dispatch a dispatched bundle carries is one hop further. A chain deeper than three warns. |
| **closure** | The transitive closure of the reference relation over the entry references: every target reachable by following the references selected content carries under the root. |
| **expansion depth** | Link hops from the nearest entry reference to a target, along its shortest path. |
| **substitution mapping** | An invocation parameter naming a different document or section for one reference, given once per entry as `-m ORIGINAL=ALTERNATIVE`: a key is the identity a reference normalizes to, a key carrying a fragment redirects that section alone and states precedence over a key naming the whole document, and both sides resolve from the invocation working directory rather than the writing source's root. |
| **substitute** | The target a substitution mapping names, which is the target outright rather than an overlay of its bytes: its title, its group and depth, its own root and its own links are the ones the run uses, and a bundle reads as if the author had written the substitute's path in the link. |
| **resource** | A reference the bundle carries as text rather than opening: an image whatever file it names, a remote address, any other link naming no local Markdown document. It is emitted as authored and never opened, rebased or resolved. |

## Selection and arrangement

| Term | Definition |
| --- | --- |
| **selection** | The set of regions chosen for inclusion. |
| **consolidation** | Replacing overlapping selections with their union, so each region appears exactly once however many references reach it. |
| **structural ancestor** | A heading emitted with no body, to preserve the outline of a partial selection. Not a dependency, and not a substitute for selecting the section it names. |
| **group** | A top-level division of the bundle: one source document, or contributing documents declaring the same group identity and depth in their metadata. |
| **placement order** | The order the bundle arranges its sources in: each is placed at the first reference that names it, reading the entry references in invocation order and then each placed source's selected content in turn. Groups and the members within a group follow it, so the order an author writes links in sets the arrangement. |
| **grouping rule** | A source document's paired metadata fields declaring its group identity and grouping depth. |
| **member** | A contributing source document whose metadata declares a named group. |
| **variant** | One of several same-named sections a merged group draws from different documents. Emitted once as a shared heading, with one subheading per source document. |
| **overview** | The section a merged group gathers its member subheadings beneath, where it also emits merged sections. A titled entry member opens its group with its own title and preamble, its sections lead, and the other members' subheadings follow in the overview. |
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
