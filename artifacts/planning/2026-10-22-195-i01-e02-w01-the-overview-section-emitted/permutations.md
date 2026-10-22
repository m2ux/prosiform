# Member permutations

The six shapes a member takes, read against the build on `main` at `7ba5fe9`. The sources are kept at [../2026-10-17-prosiform-v1/i01-e02/permutations](../2026-10-17-prosiform-v1/i01-e02/permutations) and the run is `--group rules:2` with `guide.md` as the entry.

The merged arrangement itself is not in question: documents under one folder contribute their sections to a shared outline, the grouping depth selects those sections, and variant headings distinguish their contributors. What these permutations settle is the structure the arrangement emits around that outline.

## Sources

| Member | Shape |
| --- | --- |
| `rules/common.md` | Preamble, then `## Style` and `## Links` |
| `rules/agents.md` | `## Style` and `## Tools`, no preamble; shares `Style` with Common |
| `rules/limits.md` | `## Budgets` alone; shares nothing |
| `rules/notes.md` | A bare list; no heading at all |
| `rules/titled.md` | `# Titled`, then `## Detail` |
| `rules/nested/deep.md` | `## Deep`, one folder down |

## What the build emits now

```markdown
# guide
# Rules
## Overview
### Common        Read this first.
### Notes         - Jot it down. / - Move on.
## Style
### Agents        Name the harness.
### Common        Keep paragraphs short.
## Tools          List what it may call.
## Links          Check every link.
## Budgets        Stay inside the budget.
## Deep           Far down the tree.
## Detail         The detail.
```

Entry line: `[Common](#common), [Agents](#style), [Limits](#budgets), [Notes](#notes), [Titled](#detail), [Deep](#deep)`

## What each permutation shows

| Member shape | Observation | Settled by |
| --- | --- | --- |
| Preamble only — `notes.md` | Its content has a heading of its own, `### Notes`, yet sits inside a wrapper that names nothing further | W01 |
| Sections, shares a name — `agents.md` | Resolves to `#style`, the shared heading, although `### Agents` names it | W02 |
| Preamble and sections — `common.md` | Correctly resolves to `#common`; two headings slug `#common`, the second silently suffixed by a renderer | W01, W02 |
| Sections, shares nothing — `limits.md` | Resolves to `#budgets`, its own unshared section. Sound as it stands | — |
| Its own H1 — `titled.md` | The H1 is absorbed into a generated heading that is then discarded, so **nothing in the bundle names this document** | W01 |
| A nested path — `nested/deep.md` | `## Deep` sits as a sibling of top-level members' sections, with its path nowhere | W01 |

## The two cases W01 separates

The wrapper exists to catch content that would otherwise sit directly beneath the group heading with no heading of its own.

- **Nothing pools at the grouping depth** — every member is preamble, as in `example/my-skill`. The member subsections are the group's entire structure, so the wrapper adds a level for nothing and is excluded. `--group rules:1` then emits `# Rules`, `## Agents`, `## Common`.
- **Sections pool at the grouping depth** — a member's preamble has no heading of its own and would be lost among the pooled sections, so the wrapper is emitted and carries it.

`rules:1` and `rules:2` emit identical output on the first case today, which is why no choice of depth reaches the shorter arrangement.

## Out of scope

The merged sections, the grouping depth that selects them, the variant headings that distinguish contributors, and the `--group` argument are unchanged by this epic. An arrangement that emits one section per member instead of pooling by heading was considered and rejected: it removes the capability the merged group exists to provide.
