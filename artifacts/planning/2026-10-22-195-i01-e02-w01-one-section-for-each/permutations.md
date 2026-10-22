# Member permutations

The six shapes a member takes, read against the build on `main` at `7ba5fe9`. The sources are kept at [../2026-10-17-prosiform-v1/i01-e02/permutations](../2026-10-17-prosiform-v1/i01-e02/permutations) and the run is `--group rules:2` with `guide.md` as the entry.

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

## Permutation by permutation

| Member shape | Now | Specified |
| --- | --- | --- |
| Preamble only | `### Notes` inside the wrapper | `## Notes` |
| Sections, shares a name | Torn apart: `### Agents` under `## Style`, `## Tools` loose; resolves to the shared `#style` | `## Agents` with `### Style`, `### Tools`; resolves to `#agents` |
| Preamble and sections | Split three ways, with two headings slugging `#common` | `## Common` carrying its preamble, `### Style`, `### Links` |
| Sections, shares nothing | `## Budgets` loose; nothing names the member | `## Limits` with `### Budgets` |
| Its own H1 | H1 absorbed and discarded; the member is named nowhere | `## Titled` is that H1, with `### Detail` beneath |
| A nested path | `## Deep` loose, indistinguishable from a top-level member | `## Deep` with `### Deep` absorbed into it |

## Specified output

```markdown
# Rules
## Agents         ### Style / ### Tools
## Common         Read this first. / ### Style / ### Links
## Deep           Far down the tree.
## Limits         ### Budgets
## Notes          - Jot it down. / - Move on.
## Titled         ### Detail
```

## What the permutations settled

- **The wrapper has nothing left to carry.** Every member has a heading of its own, so no contribution sits directly beneath the group heading.
- **Absorption reaches any level.** `titled.md` is named by its own `# Titled`; `deep.md` would otherwise emit `Deep` inside `Deep`, so its leading `## Deep` is absorbed the same way.
- **A stem is not always unique.** `nested/deep.md` and a `rules/deep.md` would both be `Deep`, so a member takes the shortest run of its root-relative path that distinguishes it, which is the rule variant headings followed.
- **The grouping rule loses its heading level.** No input produces different output for a different level once the arrangement is by member, so the rule is the folder slug alone. That is row W03.
