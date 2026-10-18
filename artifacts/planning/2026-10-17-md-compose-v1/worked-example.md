# Worked Example

Two compositions produced from a real source tree under the v1 rules, so the contract can be reviewed as output rather than as prose.

## What was composed

| | |
| --- | --- |
| Source root | `.claude/skills/work-planner` at commit `6888ebf` |
| Entry reference | `modes/plan-mode.md`, whole document |
| Expansion-depth budget | 8 |
| Prerequisites sections | Excluded from every source, as [D11](decisions.md#d11--prerequisite-sections-go-as-composition-replaces-them) retires them |
| Grouping level | `1` (by document) and `2` (by section level) |
| Output | [Composite](worked-example-composite.md), [grouped composite](worked-example-grouped.md) |

The Prerequisites exclusion is the one departure from composing the tree as it stands today. Those sections name whole documents coarsely, and D11 removes them during the refinement stage once composition supplies what they named. Composing with them in place would measure the tool against a structure that is going away, so this example composes the tree D11 leaves behind.

A second composition, entered at `SKILL.md`, was run to exercise the failure paths. Its output is not kept; what it found is recorded below.

## Result

| Measure | Value |
| --- | --- |
| Contributing files | 27 |
| Of those, whole documents | 6 |
| Sections selected in the other 21 | 204 |
| Headings emitted | 353 |
| Deepest emitted heading | H4 |
| Internal links rewritten | 421 |
| Composite size | 187,488 bytes |
| Expansion depth reached | 4 hops |

Validation reparsed the composite and checked it against the invariants the output alone can establish: every one of the 421 internal links resolves to one of 353 destinations, no two destinations coincide, no original reference definition survives, and no heading exceeds H6.

The composite was then published and rendered by GitHub, which is the independent check. GitHub generates 353 anchors for its 353 headings, 272 bare and 81 carrying an ordinal, and the page's 774 fragment links -- the 421 rewritten ones and GitHub's own 353 heading self-links -- all resolve. None are broken.

## What it shows

- **A destination is the renderer's own fragment, and nothing is emitted at it.**
  `[Template](#template)` is the fragment GitHub generates for the heading `### Template`, so the link resolves where the composite is read. Where two composed headings share a slug the destination carries the renderer's ordinal, as `[Fields](#fields-7)` does. The target is an ordinary shifted source heading carrying no identifier, and the reader locates it by the document's structure.

- **A file heading absorbs a title it already carries.**
  `artifacts/architecture-overview.md` opens with `# Architecture Overview`, which slugifies to its own filename stem, so the file heading replaces it and that group keeps its source levels. Thirty-seven of the skill's thirty-eight documents are this shape. `SKILL.md`, whose H1 is `Work Planner`, is the one that is not: it keeps its H1 and shifts.

- **Heading-only scaffolding carries no body.**
  `artifacts/board-queue` contributes one section. Its group emits the filename heading, then `Fields` as a title alone, then `Task Eligibility` with its content. No sibling section and no ancestor body reaches the composite.

- **Heading-like text in code is untouched.**
  The template fences in `artifacts/architecture-overview.md` hold `# Architecture Overview — {{Change Name}}` and a `---` pair inside a Mermaid block. Neither is shifted, parsed as a heading, or read as frontmatter.

- **Whole-document and section references produce different destinations.**
  `[Propose Mode](#modespropose-mode)` resolves to that file's heading, whose slug drops the slash as the renderer does; `[Populate Planning Record](#populate-planning-record)` resolves to the section.

## Grouped at section level

The same closure composed at `--group-level 2`, where a group is one source heading text merged across every document carrying it rather than one document.

| Measure | Level 1 | Level 2 |
| --- | --- | --- |
| Groups | 27, one per document | 9 |
| Destinations | 353 | 276 |
| Carrying an ordinal | 81 | 26 |
| Bytes | 187,488 | 185,915 |

Eight distinct headings exist at level 2 across those 27 documents: `Operations` in 20 of them, `Fields` in 18, `Commands` in 13, `Procedure` in 6, `Outcomes` in 4. Grouping by that level puts every operation in the skill in one place.

**The work-planner skill does not compose at this level.** Twenty-six names collide inside the merged `Fields` group, so the run refuses and publishes nothing:

| Colliding name | Documents |
| --- | --- |
| `Template` | architecture-overview, epic-issue-body, initiative-issue-body, planning-record, proposal-body, pull-request-body, task-body, work-item |
| `Titles` | epic-issue-body, initiative-issue-body, issue-body, proposal-body, pull-request-body, task-body |
| `Sections` | architecture-overview, proposal-body, task-body, work-item |
| `Problem`, `Proposal`, `Non-Goals`, `References`, `Work Breakdown`, `Acceptance Criteria`, `Open Questions`, `Breakdown Prose`, `Delivery Findings`, `Delivery State` | two documents each |

That is the rule working rather than failing. Grouping merges separate documents into one namespace, and the author guarantees uniqueness among what they merged. The published grouped composite above is the refused candidate, kept so the arrangement can be reviewed; a conforming one needs those names made distinct first.

One collision is the compositor's own: the generated `Sources` group clashes with a `Sources` heading in `initiative-issue-body.md`, which is worth knowing before the name is settled.

## Measurements against reading the sources whole

| Reading | Files | Bytes |
| --- | --- | --- |
| Closure with Prerequisites sections present, read whole | 39 | 318,018 |
| Closure with Prerequisites sections removed, read whole | 27 | 239,331 |
| Composed | 27 | 187,488 |
| The whole skill, read whole | 38 | 302,445 |

Most of the reduction is D11's, not composition's. Removing the prerequisite lists drops twelve files no procedure linked, worth 78,687 bytes; selecting sections within what remains saves a further 51,843, or 21.7%. At this skill's granularity, composition's case rests on the completeness signal, the single document and the resolved links rather than on size.

That is also the first thing [D12](decisions.md#d12--each-run-is-measured-against-reading-the-sources-whole)'s run records will measure at scale, and this example is the shape those records take.

## What the failure paths found

The Plan Mode closure composes clean. The `SKILL.md` closure, which reaches `guidelines.md` and `modes/revise-mode.md`, does not: it fails on ten defects in the source, every one of them a real link fault that reading the files would not surface.

| Defect | Where | Count |
| --- | --- | --- |
| `SKILL.md#command-conventions`, where the heading is `Conventions` | `guidelines.md:189` | 1 |
| `../guidelines.md…`, from `guidelines.md`, which is already at the root | `guidelines.md:3, 193, 206` | 4 |
| `../../guidelines.md…`, from `modes/`, which leaves the root | `modes/revise-mode.md:17, 30, 36, 42` | 4 |
| `guidelines.md#disclosure-verification`, where no such heading exists | `guidelines.md:193`, `modes/revise-mode.md:42` | 1 |

Each `..` fault is one level too many, so each link resolves above the allowed source root and fails confinement. The skill is maintained upstream, so these are reported rather than corrected here.

This is the completeness signal doing the thing the proposal claimed for it, on the first real tree it was pointed at.

## What it does not establish

The composites were produced by a direct reading of the design, not by the prototype, which does not exist yet. They demonstrate what the rules produce and where they are ambiguous. This is not a conformance result, carries no fixture, and proves nothing about byte-level preservation, diagnostic wording, exit statuses or atomic publication.

## Open

- **Group order.**
  File groups are emitted in root-relative path order, which satisfies the design's requirement for a deterministic order derived from source identity. It places the entry document, `modes/plan-mode`, three quarters of the way through the composite. Whether the entry reference should lead its composite is unsettled.
