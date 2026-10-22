# Section Composition: Unicode Links Compose Content Within the Containing Section

## Overview

Add an ontology-independent “inline here” link form to Prosiform. A supported Markdown link whose plain-text label is exactly one non-ASCII Unicode scalar value composes the selected target section beneath the section containing that occurrence. Authors can assign glyphs meanings such as input, output or invariant; the compiler recognizes only the expansion syntax. Deferral composes with inline expansion: a deferred inline link retains its destination section for later composition.

## Problem

- **Bundling does not express call-site placement.**
  The [current inclusion and grouping contract](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L54-L108) carries linked sections into document groups. A caller cannot compose referenced sections beneath its own containing section, merging matching section titles while retaining source-parent contributions.
- **A compact interface needs independently placed fragments.**
  A protocol step can collect input and output contracts from several calls while their implementations remain deferred. Contracts need a shared title within that step and separate contributions identified by source parent.
- **Ontology meanings must remain author-owned.**
  Recognizing inputs, outputs, activities or artifacts would couple the compiler to one document model. The [existing deferred-reference handling](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L1137-L1157) already separates a syntactic marker from later agent execution.

## Proposal

- **Reserve a lexical form for inline expansion.**
  After Markdown parsing and character-reference decoding, recognize an optional existing deferral prefix first. A link qualifies for inline expansion when its remaining label is plain text containing exactly one non-ASCII Unicode scalar value. Reserve that form; it is not an ordinary short-label link.
  - ASCII labels such as `A` or `1` keep existing behavior. One supplementary-plane scalar qualifies; combining sequences, variation-selector sequences and multi-scalar emoji do not.
  - Apart from consuming the deferral prefix and its defined separator, do not trim whitespace, normalize Unicode or flatten formatting to make a label qualify. An entity spelling that decodes to the same scalar has the same meaning.
  - Deferral and inline placement are independent properties. The label `¬ ↑` requests deferred inline expansion; `↑` requests immediate inline expansion. A lone deferral marker retains its existing meaning and does not become an inline glyph.
- **Keep meaning outside the compiler.**
  Treat every qualifying glyph identically. Do not maintain an input/output glyph registry or infer execution, typing, authorization or workflow relationships from it.
  - `[↓↑](contract.md#io)` is a two-scalar label and does not invoke this syntax. Two section contributions use two links; there is no implicit label splitting.
  - Apply the rule to link forms already admitted by the Markdown profile, including resolved reference-style forms where supported. Code examples, images and unresolved plain text are not inline-expansion links.
- **Compose sections within the containing section.** The nearest enclosing heading defines the destination scope:
  - A referenced section becomes a child section of that scope. References with the same section title in that scope share one destination section.
  - Each contribution sits below that destination section under a heading named after the immediate parent of the referenced source section. Preserve the contribution's prose, lists, tables and nested sections with relative heading depth.
  - Apply the rule to any authored section title. Inputs and Outputs have no special compiler meaning. Do not merge across sibling destination sections.
  - A procedure authored with numbered step headings therefore receives a separate composed contract beneath each step. Recognizing or converting procedure lists is outside the compiler feature.
  - Place generated child sections at the end of their containing section's own content, before its existing child sections, in first-reference order. Contributions follow reference order. Marker links are composition directives, not sentence-level replacement slots.
  - Match section titles exactly after Markdown text decoding, without case folding or Unicode normalization. Distinct source parents with the same title retain distinct contributions; source identity must not be lost.
  - Diagnose a missing containing heading, missing source section or parent heading, an incompatible existing child-heading collision, or unrepresentable heading depth. Do not invent parent names or silently flatten source structure.
- **Retain the inserted content's source context.**
  Resolve relative links and reference definitions in the fragment against the fragment's source, not the caller. Carry its dependencies through the normal validation and destination-rewriting process.
  - Preserve source attribution for diagnostics inside expanded content. Resolve colliding reference-definition names without changing which destination an occurrence denotes.
  - A reserved inline link must resolve to an eligible Markdown target inside the allowed root. An external URL, resource or escaping target is an inline-target error, not an unexpanded marker silently carried into output.
- **Expand each occurrence and bound recursion.**
  Repeated marked references each contribute within their containing section, including repeated references to the same source. Deduplicating source reads or validation must not remove a requested occurrence.
  - Follow nested inline links. Reject a cycle on the active inline-expansion path with the source chain; repeated independent occurrences are valid.
  - Inline-only targets do not also appear as separately grouped copies merely because they were inlined. A target also reached by an ordinary dependency retains the ordinary inclusion semantics.
  - Count materialized occurrences against explicit expansion/output budgets so repeated inclusion cannot evade limits. Preserve ordinary dependency-cycle behavior where it does not recurse through inline expansion.
- **Compose deferral with either inclusion form.**
  A call can inline its contract now and retain a deferred implementation link, or defer an inline contract itself. Deferral controls when content is expanded; inline syntax controls where it is placed.
  - A deferred inline occurrence retains its target, source context and destination-section identity without materializing the target body. Apply existing deferred destination checks; full structural, dependency and recursion validation occurs when that occurrence is activated.
  - When activated through the deferred-bundling mechanism, compose the selected section into its retained destination scope, merging with that scope's matching title. Nested deferred inline occurrences remain deferred until selected. Do not treat a valid deferred destination as proof its body compiles.
- **Publish the grammar and conformance behavior together.**
  Update the authoring/profile specification, compiler behavior and conformance fixtures for this reserved form. Preserve complete-output publication: any inline-expansion error publishes no partial bundle.

Example composed outline; the author chooses the contract names and numbered step headings:

    Procedure
    ├── 1. Gather Evidence
    │   ├── Inputs
    │   │   ├── Query Repository Graph
    │   │   └── Read Contract Registry
    │   └── Outputs
    │       ├── Query Repository Graph
    │       └── Read Contract Registry
    └── 2. Assess Finding
        ├── Inputs
        │   └── Apply Rubric
        └── Outputs
            └── Apply Rubric

The first step references Inputs and Outputs beneath two source parents. Each title is merged only within that step. A deferred inline link such as `[¬ ↑](collection.md#outputs)`, contributes only when selected; its destination remains the original containing section.

This issue defines structural document composition, not sentence-level prose substitution, IO-contract inference, schema checking, workflow execution or ontology-specific notation.

## Acceptance Criteria

- [ ] **AC1.** Inline recognition is exactly the declared plain-text, decoded, single non-ASCII Unicode-scalar predicate, as lexical fixtures covering ASCII, entities, whitespace, formatting, supplementary scalars and multi-scalar sequences demonstrate.
- [ ] **AC2.** Deferral and inline placement compose independently, as fixtures for immediate glyphs, deferred glyphs such as `¬ ↑`, ordinary deferred labels and the lone deferral marker demonstrate.
- [ ] **AC3.** Matching referenced section titles compose into one child section per containing section, as multi-source and sibling-step output fixtures demonstrate.
- [ ] **AC4.** Each contribution is nested under its source-parent name with its original block structure preserved, as multi-paragraph, nested-heading, list and table fixtures demonstrate.
- [ ] **AC5.** Links and reference definitions within inserted content retain their original source meaning, as cross-directory and colliding-definition fixtures demonstrate.
- [ ] **AC6.** Each independent marked occurrence contributes its own structurally nested content, as repeated-reference and mixed ordinary/inline fixtures demonstrate.
- [ ] **AC7.** Recursive inline inclusion reports the active source chain rather than looping or silently omitting content, as direct and indirect cycle fixtures demonstrate.
- [ ] **AC8.** Materialized inline content is accounted for by the declared expansion/output budgets, as multiplicative-expansion limit fixtures demonstrate.
- [ ] **AC9.** A reserved inline link cannot silently retain an ineligible target, as external-resource and source-root-boundary fixtures demonstrate.
- [ ] **AC10.** Composing contract sections leaves an accompanying deferred implementation body absent from that bundle, as combined-selection fixtures demonstrate.
- [ ] **AC11.** Deferred inline occurrences retain their destination-section identity and source context without eager body expansion, as deferred-bundle fixtures demonstrate.
- [ ] **AC12.** Activating a deferred inline occurrence composes it into its retained destination section and validates its content while preserving nested deferrals, as staged-compilation and deferred-invalid-body fixtures demonstrate.
- [ ] **AC13.** Any inline-expansion failure publishes no partial bundle, as stdout and named-output failure fixtures demonstrate.
- [ ] **AC14.** The published grammar describes the reserved syntax without assigning ontology meanings to glyphs, as specification review and matching conformance fixtures demonstrate.

- [ ] **AC15.** Composition ordering and exact title matching are deterministic, as reordered-reference, Unicode-title and same-name-parent fixtures demonstrate.
- [ ] **AC16.** Missing structural context, conflicting child headings and unsupported heading depth produce source-located diagnostics, as structural failure fixtures demonstrate.

## References

- **R1.** [Pinned compiler contract](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L34-L150) — Selection, closure, grouping, source rechecks and complete publication.
- **R2.** [Pinned deferred-reference handling](https://github.com/m2ux/prosiform/blob/cd3d8e635b8db500ceb7230b26209bdd37f637da/src/prosiform/cli.py#L1137-L1157) — A deferred reference retains its marker for a later compilation.
