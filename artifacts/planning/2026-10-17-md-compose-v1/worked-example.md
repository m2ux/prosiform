# Worked Example

One composite produced from a real source tree under the v1 rules, so the contract can be reviewed as output rather than as prose.

## What was composed

| | |
| --- | --- |
| Source root | `.claude/skills/work-planner` at commit `6888ebf` |
| Entry reference | `modes/plan-mode.md`, whole document |
| Expansion-depth budget | 8 |
| Prerequisites sections | Excluded from every source, as [D11](decisions.md#d11--prerequisite-sections-go-as-composition-replaces-them) retires them |
| Output | [Composite](worked-example-composite.md) |

The Prerequisites exclusion is the one departure from composing the tree as it stands today. Those sections name whole documents coarsely, and D11 removes them during the refinement stage once composition supplies what they named. Composing with them in place would measure the tool against a structure that is going away, so this example composes the tree D11 leaves behind.

## Result

| Measure | Value |
| --- | --- |
| Contributing files | 27 |
| Of those, whole documents | 6 |
| Sections selected in the other 21 | 204 |
| Headings emitted | 380 |
| Deepest emitted heading | H5 |
| Internal links rewritten | 421 |
| Composite size | 206,896 bytes |
| Expansion depth reached | 4 hops |

Validation reparsed the composite and checked it against the invariants it can establish from the output alone: every one of the 421 internal links resolves to one of 380 destinations, no two destinations coincide, no original reference definition survives, and no heading exceeds H6.

## What it shows

- **A destination is a path, and nothing is emitted at it.**
  `[Outcomes](modes/plan-mode.md/plan-mode/outcomes)` names the file, the ancestor chain and the section. The target is an ordinary shifted source heading carrying no identifier, and the reader locates it by the document's structure.

- **Heading-only scaffolding carries no body.**
  `artifacts/board-queue.md` contributes one section. Its group emits the filename heading, then `Board Queue` and `Fields` as titles alone, then `Task Eligibility` with its content. No sibling section and no ancestor body reaches the composite.

- **Heading-like text in code is untouched.**
  The template fences in `artifacts/architecture-overview.md` hold `# Architecture Overview — {{Change Name}}` and a `---` pair inside a Mermaid block. Neither is shifted, parsed as a heading, or read as frontmatter.

- **Whole-document and section references produce different destinations.**
  `[Propose Mode](modes/propose-mode.md)` keeps the bare file segment; `[Populate Planning Record](artifacts/planning-record.md/planning-record/operations/populate-planning-record)` carries the full chain.

## Measurements against reading the sources whole

| Reading | Files | Bytes |
| --- | --- | --- |
| Closure with Prerequisites sections present, read whole | 39 | 318,018 |
| Closure with Prerequisites sections removed, read whole | 27 | 239,331 |
| Composed | 27 | 206,896 |
| The whole skill, read whole | 38 | 302,445 |

Most of the reduction is D11's, not composition's. Removing the prerequisite lists drops twelve files no procedure linked, worth 78,687 bytes; selecting sections within what remains saves a further 32,435, or 13.5%. At this skill's granularity, composition's case rests on the completeness signal, the single document and the resolved links rather than on size.

That is also the first thing [D12](decisions.md#d12--each-run-is-measured-against-reading-the-sources-whole)'s run records will measure at scale, and this example is the shape those records take.

## What it does not establish

The composite was produced by a direct reading of the design, not by the prototype, which does not exist yet. It demonstrates what the rules produce and where they are ambiguous. It is not a conformance result, carries no fixture, and proves nothing about byte-level preservation, diagnostics, exit statuses or any failure path.

## Open

- **Group order.**
  File groups are emitted in root-relative path order, which satisfies the design's requirement for a deterministic order derived from source identity. It places the entry document, `modes/plan-mode.md`, three quarters of the way through the composite. Whether the entry reference should lead its composite is unsettled.
