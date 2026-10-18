# Worked Example

Two compositions produced from a real source tree under the v1 rules, so the contract can be reviewed as output rather than as prose.

## What was composed

| | |
| --- | --- |
| Source root | `.claude/skills/work-planner` at commit `6888ebf` |
| Entry reference | `modes/plan-mode.md`, whole document |
| Expansion-depth budget | 8 |
| Prerequisites sections | Excluded from every source, as [D11](decisions.md#d11--prerequisite-sections-go-as-composition-replaces-them) retires them |
| Cohorts | none, and `--group artifacts:2 --group modes:2` |
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
| Entry group position | last, after the 26 documents it reaches |

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

## Grouped by cohort

The same closure composed with `--group artifacts:2 --group modes:2`, which merges every document under those directories at its second heading level. `references/requirement-characteristics` is claimed by no cohort and keeps its own group, as does `modes/plan-mode`, which is the entry reference and is never claimed.

| Measure | No cohort | `artifacts:2` |
| --- | --- | --- |
| Top-level groups | 27, one per document | 4 |
| Destinations | 353 | 253 |
| Branched names | 0 | 13 |
| Carrying an ordinal | 81 | 18 |
| Bytes | 187,488 | 187,097 |

Twenty-one artifact documents merge into `# Artifacts`, holding `## Operations`, `## Fields` and `## Commands`, and five modes into `# Modes`. All twenty-four merged operations keep their bare names, because no two documents offer the same one:

```markdown
# Artifacts

## Operations

### Populate Architecture Overview
### Plan Board Changes
### Select Project Board
```

The thirteen branched names are all in `## Fields`. A name several documents contribute is emitted once, with each document's content under a branch heading naming it, so the eight `Template` fields sit together:

```markdown
## Fields

### Template
#### Architecture Overview
#### Epic Issue Body
#### Initiative Issue Body
#### Planning Record
#### Proposal Body
#### Pull Request Body
#### Task Body
#### Work Item

### Sections
#### Architecture Overview
#### Proposal Body
```

Seventeen destinations take the renderer's ordinal, most of them branch headings: a document contributing to several branched names supplies its title to each, so `Epic Issue Body` recurs.

A merged section is not always a container of named items. Every mode's `Procedure` carries the mode's own numbered steps, so merging five of them by item would run five procedures together with nothing to tell them apart. A section carrying body text from more than one document therefore branches whole:

```markdown
## Procedure

### Align Mode
#### Repair Issue Format
#### Plan Gap Task

### Deliver Mode
#### Integrate Epic Delivery
#### Fetch Merge Readiness
```

`modes/plan-mode` is absent from that cohort: an entry reference is never claimed, so it keeps its own group at the end. `SKILL.md` is absent from the composite entirely, since nothing in the closure links to it.

Published and rendered by GitHub, with none broken.

**This is also where the merge earns its keep as a review tool.** Reading the eight `Template` fields together shows that `Template` does not belong under `Fields` at all — a template is the artifact's shape, not one of its fields — which is a structural defect in the source that document-by-document reading had not surfaced in this workspace. The same question applies to `Sections`, carried by four documents under the same heading.

A cohort is headed by its directory slug in title case and carries a `Body` section holding each member's preamble, named by the document's stem less a trailing word the section already states:

```markdown
# Artifacts

## Body

### Epic Issue

Populates one epic body. The body states one slice of the design and lists the tasks that deliver it.

## Operations
```

That trimming is the rule the branch headings already follow, drop what the containing heading states, applied to a name rather than a path: `epic-issue-body.md` reads `Epic Issue` under `Body`. A preamble belongs to no section, so only a whole-document selection carries one; the artifacts cohort has one such member and the modes cohort three.

Only `work-planner` is broadly representative in this workspace, so the case the parameter is built for — one slug under two libraries, qualified at one segment — is implemented but not exercised against real sources here.

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

- **Nothing.**
  The questions this example raised — the qualifier's length, the generated group name and the group order — are settled in D21 to D25.
