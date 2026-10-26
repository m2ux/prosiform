# Glossary

Every term the contract uses, defined once. A term defined here means this and nothing else in the design, the acceptance criteria, the fixture corpus and the tool's own diagnostics. The design italicises a term where it first uses it, and the vocabulary check holds this file to defining each one.

The tool is `prosiform`. It bundles; what it produces is a bundle.

## The act and the artifact

| Term | Definition |
| --- | --- |
| **bundle** (v.) | To resolve a reference closure into one self-contained Markdown document. |
| **bundle** (n.) | The single validated document produced by one run. |
| **candidate** | A bundle before it has passed validation. Nothing reaches standard output while a check fails. |
| **profile** | The named, versioned Markdown grammar and option set a run declares. |

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
| **reference** | An authored Markdown link to a local document or section. |
| **entry reference** | A reference supplied as an argument. Traversal starts at each one. |
| **target** | The document or section a reference resolves to, after path and fragment normalization. |
| **dependency** | A target a reference resolves to under the allowed source root, where its author has not withheld it with either operator. It is resolved, bundled and rewritten; a reference resolving outside the root cites the document it names and creates none. |
| **deferral** | An author's statement that a reference is compiled in a run of its own rather than this one, written as a `¬` opening the link's text. The target is required to exist and is carried nowhere; the bundle emits the link's text with the mark and the spaces following it removed, and its destination is the target's URI-escaped path from the invocation working directory. The mark is authoring syntax rather than content, because the destination already states the deferral. |
| **dispatch operator** | An author's statement that a link's material is compiled by a sub-agent rather than by this run, written as a `⇉` opening the link's text. It withholds the compilation a deferral withholds: the target is required to exist, contributes no content, adds no dependency and no group membership, and its destination is the target's URI-escaped path from the invocation working directory. Unlike a deferral, the mark is published, because it is what states that the material belongs to another agent. A link states one operator, so text opening with both is refused. Dispatch nests: the sub-agent compiles the target as its own entry, and the dispatches that closure carries are dispatched again. |
| **dispatch depth** | The number of dispatch hops along one chain, counted from the bundle being compiled: a dispatch the bundle carries is the first hop, and a dispatch the closure of a dispatched target would carry, compiled as its own entry, is one hop further. A chain deeper than three warns. |
| **closure** | The transitive closure of the reference relation over the entry references: every target reachable by following the references selected content carries under the root. |
| **expansion depth** | Link hops from the nearest entry reference to a target, along its shortest path. |
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
| **overview** | The section a merged group gathers its member subheadings beneath, where it also emits merged sections. |
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
| **publication** | Emitting a validated bundle to standard output or to a file, atomically. |
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
