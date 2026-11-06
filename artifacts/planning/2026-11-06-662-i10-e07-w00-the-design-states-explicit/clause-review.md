# W00 Clause-to-Fixture Review

Candidate: [the immutable W00 design](https://github.com/m2ux/prosiform/blob/d6f95677d6dfa6d6b7b37f9106cb7e2a4fafabfd/artifacts/planning/2026-10-17-prosiform-v1/design.md), at `d6f95677d6dfa6d6b7b37f9106cb7e2a4fafabfd`.

| Contract area | Candidate clause | Concrete observing fixture or scenario |
| --- | --- | --- |
| Entry grammar | CLI contract; File-owned invocation conformance cases — Single entry | Planned: one `--entry` and optional `--tags` succeeds; positional input, repeated entries, repeated tags and tags without an entry fail at usage. Migrate existing multi-entry fixtures to an authored wrapper document. |
| Shared tag grammar | Presets — Selection by tags | Planned: inline link and CLI entry select identical `checks,draft` settings; whitespace, case, repetition, empty tokens and unknown tokens resolve to the same effective selection. Existing heading-selection fixtures migrate to title tags. |
| Occurrence scope | Presets — Selection belongs to the link | Planned: two links under one heading select different presets; preamble and reference-style links select identically; changing heading and visible label changes no selection. Image and Mermaid tooltip titles select none. |
| Target ownership | Presets — What a selection governs | Migrate `inclusion/a-dependencys-preset-comes-from-itself`; add a substituted target whose own declared preset answers the preserved occurrence tags, and an outgoing link whose own title differs from its parent's incoming tags. |
| Default and conflict rules | Presets — default always applies; Selected presets union | Migrate `inclusion/default-applies-in-every-section`, `inclusion/a-section-matching-no-preset-selects-default`, and existing preset-union/conflict fixtures to explicit title tags. Unknown tags are silent while declared unused-preset warnings remain observable. |
| Effective selection identity | Presets — Bundle selection identity | Planned: dispatch one section twice with different effective preset sets and substitutions; inspect distinct output files and contents. Repeat with reordered/case-varied/unknown tags and assert one effective variant. |
| Deterministic filenames | Automatic output names | Planned: compare the canonical UTF-8 compact JSON hash with fixed expected names; test Unicode and escaped names, default-only names, traversal-order independence, and a collision that publishes no partial set. `checks,draft` has the exact digest recorded in the contract. |
| Dispatch and parallel sets | Dispatched bundles; Dispatch links; Parallel dispatch sub-sections | Migrate `dispatch/a-dispatched-target-is-a-bundle-of-its-own`; add two effective selections of one destination in a parallel set and verify two items, while equivalent selections deduplicate. Candidate validation rejects a swapped variant filename. |
| Graph analysis | Dispatch cycles; Resource limits | Planned: a chain switching variants returns only when it repeats the complete canonical selection; depth analysis uses the same identities as scheduling, and one variant exceeding its own budget refuses the complete publication. |
| Deferred parity | A deferred link's destination; Section composition — Presets and subst; Deferred composition | Replace the heading-mismatch refusal scenarios with a tagged deferred link whose scope and target headings differ. Compile its preserved destination and title through the guide's `--entry`/`--tags` command and compare its selection with immediate composition. |
| Agent command specification | Guide; Reference normalization and path identity | Migrate `cli/informational-guide-response`; observe the exact command specification for an authored relative link, a same-file fragment qualified with its document, and a tag list containing spaces passed as one shell-quoted argument. |

The scenarios are contract obligations for the implementation units; W00 defines and reviews them but does not implement their source, fixtures or runtime behavior. Main's current immutable README design pin stays at `6deca17d6b56c61f477c815da6eeecc3949d8ca1` until its joined CLI/caller/fixture unit adopts W00's revision.

## Bounded Validation

- `git diff --check`: pass.
- Existing link checker against the candidate: all 11 distinct internal destinations resolve. Its full offline result reports six pre-existing remote references because `--online` was not supplied; those URLs were not changed or fetched.
- Existing vocabulary reader against the candidate: 47 marked terms, none undefined by the shipped glossary. `references` is expressed in singular `reference`; it has the same existing glossary definition.
- Explicit obsolete-rule scan: zero surviving operative keyword-selector, heading-mismatch, multi-entry grammar or joined-entry naming claims.
- Exact digest calculation: compact JSON `["checks","draft"]` hashes to `13c9f40cda0225cb29b9fa2332a291e8950291238a73b75fed0cd1521986f6e8`; the candidate's filename example carries that value.
- Existing pinned conformance check: pass, 361 clauses, 64 uncovered, zero missing clause declarations, zero code mismatches. This checks the current immutable pin, not candidate runtime support.
- Candidate parsed through `checks/conformance.py`'s `report`: 365 clauses, 69 uncovered, zero code mismatches. One removed clause identifier (`Presets — Selection by keyword`) is still named by 15 existing fixtures and needs migration with the CLI/caller/fixture unit. The candidate is not reported as passing the current corpus.

Raw evidence: [validation output](validation-output.txt), [candidate inventory](candidate-conformance.txt), [current-pin conformance](pinned-conformance.txt), and the published task commit.
