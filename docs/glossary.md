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
| **root** | The directory confining all source access. A path resolving outside it fails. |
| **source document** | One local Markdown file under the root, recognized by its `.md` or `.markdown` suffix. |
| **section** | A document-level heading and its subsections, ending before the next heading of equal or higher level. The smallest unit a reference can select. |
| **region** | A contiguous span of a source document selected for inclusion: a whole document, or a section. |
| **preamble** | Content above a source document's first heading. It belongs to no section, so only a whole-document selection carries it. |
| **frontmatter** | A leading delimited metadata block, stripped from every included document and never traversed. |

## References

| Term | Definition |
| --- | --- |
| **reference** | An authored Markdown link to a local document or section. |
| **entry reference** | A reference supplied as an argument. Traversal starts at each one. |
| **entry point** | The routing document a caller reads to choose an entry reference. It is not an argument, so it is never bundled. |
| **target** | The document or section a reference resolves to, after path and fragment normalization. |
| **dependency** | A target its author marked as required, by opening the reference's link text with `¬`. It is resolved, bundled and rewritten; a reference left unmarked cites the document it names and creates none. |
| **closure** | The transitive closure of the reference relation over the entry references: every target reachable by following marked references from selected content. |
| **expansion depth** | Link hops from the nearest entry reference to a target, along its shortest path. |
| **resource** | A reference target that is not a local Markdown document: an image, a remote address, any other non-Markdown link. It is emitted as authored and never opened, rebased or resolved. |

## Selection and arrangement

| Term | Definition |
| --- | --- |
| **selection** | The set of regions chosen for inclusion. |
| **consolidation** | Replacing overlapping selections with their union, so each region appears exactly once however many references reach it. |
| **structural ancestor** | A heading emitted with no body, to preserve the outline of a partial selection. Not a dependency, and not a substitute for selecting the section it names. |
| **group** | A top-level division of the bundle. By default one source document; a grouping rule makes it one merged directory. |
| **grouping rule** | `SLUG:DEPTH`. Every document under a directory named `SLUG` is merged at source heading level `DEPTH`, beneath one heading carrying the slug in title case. Repeatable, once per slug. |
| **member** | A source document a grouping rule claims. |
| **variant** | One of several same-named sections a merged group draws from different documents. Emitted once as a shared heading, with one subheading per source document. |
| **overview** | The section of a merged group holding each member's content above the grouping depth, one subheading each. |

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
| **cohort** | Imported from demography, and earns nothing a grouping rule and a group do not already say. |
| **branch** | Collides with the version-control sense. A same-named section from another document is a variant. |
| **anchor** | The bundle emits no anchor elements. A destination names a heading; it is not an element. |
| **include** | Suggests textual substitution at a point. Selection, consolidation and grouping decide what appears and where. |
