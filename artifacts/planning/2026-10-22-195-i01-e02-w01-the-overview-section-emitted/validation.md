# Validation

The checks this unit ran, the revision they ran against and what each observed.

**Revision:** `i01/e02/w01-the-overview-section-emitted` at `bb7be45`, cut from `origin/i01/e02/main` at `7ba5fe9`.
**Build under test:** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`.

## Repository checks

`make check` runs the repository's whole set — lock, lint, format, typecheck, unit tests, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence — and stops at the first failure.

```text
corpus check: 241 fixture(s), 241 pass, 0 fail, 0 awaited, 0 unexpected pass
vocabulary check: 35 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md
  on origin/engineering, every one defined in docs/glossary.md
conformance report: 244 clause(s) the design states, 0 covered by no fixture,
  0 declaration(s) naming no clause
independence check: every word of every fixture declaration and every report entry
  is one the contract states
```

Exit status 0.

## Grouping fixtures for members with and without above-depth content

`grouping/a-group-emitting-no-merged-section` declares two members carrying nothing at the grouping depth under `--group rules:1`. The group emits no merged section, so the subsection naming each member is the group's whole structure:

```markdown
# Rules

## Agents

Name the harness.

## Common

Keep paragraphs short.
```

`grouping/one-entry-under-a-group`, `grouping/a-whole-document-reference-to-a-member`, `grouping/a-section-shallower-than-the-grouping-depth` and `usage-example/every-document-under-a-directory-merged` declare groups that pool sections at the grouping depth. Each keeps the overview section carrying the member subsections, and each passes on the bytes it already declared.

Observed: AC1.

## A member whose own H1 is its only identity

`grouping/a-member-named-by-the-title-it-absorbs` declares a member whose every other region sits at the grouping depth. Its title is absorbed into the subsection heading, which the bundle emits:

```markdown
# entry

The member [Titled](#titled) is named by the heading its own title is absorbed into.

# Notes

## Overview

### Titled

## Findings

The run held throughout.
```

`src/tests/test_grouping.py::test_a_member_whose_title_the_subsection_absorbs_takes_one` reads the same case through the parts a group emits.

Observed: AC2.

## A member the arrangement emits nothing else from

`grouping/an-entry-naming-a-member-carrying-one-heading` and `grouping/a-reference-to-a-member-carrying-one-heading` declare a member whose whole content is the one heading its subsection absorbs, under a group that pools and one that does not. `src/tests/test_grouping.py::test_a_member_the_group_emits_nothing_else_from_takes_a_subsection` reads the parts.

Observed: AC2.

## Entry and internal links under both arrangements

| Fixture | Arrangement | What resolves |
| --- | --- | --- |
| `grouping/a-group-emitting-no-merged-section` | No merged section | Each entry reference to the subsection naming its member |
| `grouping/an-entry-naming-a-member-carrying-one-heading` | Overview section | Each entry reference to the subsection naming its member |
| `grouping/a-reference-to-a-member-carrying-one-heading` | No merged section | A compiled reference to the subsection naming the member |
| `grouping/a-member-named-by-the-title-it-absorbs` | Overview section | A compiled reference to the heading the member's title is absorbed into |
| `grouping/a-whole-document-reference-to-a-member` | Overview section | A member carrying nothing above the grouping depth to its first contribution |

Observed: AC1, AC2.

## The merged arrangement held to what it was

`grouping/one-entry-under-a-group`, `grouping/a-reference-to-a-grouping-depth-heading`, `grouping/variant-headings-distinguished-at-more-than-one-segment`, `grouping/a-document-no-group-matches` and `grouping/structural-ancestors-inside-a-merged-group` declare the pooled sections, the names inside them and the variant headings that distinguish contributors. Every pooled section and every variant heading they declare is emitted as it was declared.

One of them, `variant-headings-distinguished-at-more-than-one-segment`, gained a member subsection: its second document is reached as a whole, so the subsection naming it absorbs its title and is where that reference resolves. Its merged section, its names and both variant headings are unchanged.

## The reproduction tree

The tree at [../2026-10-17-prosiform-v1/i01-e02/permutations](../2026-10-17-prosiform-v1/i01-e02/permutations), run as `--group rules:2` with `guide.md` as the entry:

```markdown
# Rules

## Overview

### Common        Read this first.
### Notes         - Jot it down. / - Move on.
### Titled
## Style
### Agents        Name the harness.
### Common        Keep paragraphs short.
## Tools          List what it may call.
## Links          Check every link.
## Budgets        Stay inside the budget.
## Deep           Far down the tree.
## Detail         The detail.
```

Entry line: `[Common](#common), [Agents](#style), [Limits](#budgets), [Notes](#notes), [Titled](#titled), [Deep](#deep)`.

`titled.md` is named by `### Titled`, and the entry reference naming it resolves there rather than to the shared outline. The same tree at `--group rules:1` keeps its overview section, because `titled.md` writes its H1 at that depth and so pools a merged section.

`example/my-skill`, whose members under `rules/` are preamble alone, reaches the shorter arrangement the permutations record calls for:

```bash
prosiform --root my-skill --group rules:1 procedure.md rules/common.md
```

```markdown
# Rules

## Agents

Select rules for your harness:

- If you are Codex, compile [¬ Codex](rules/codex.md).
- If you are Claude, compile [¬ Claude](rules/claude.md).

## Common

- Check every link.
- Use clear headings.

Follow [Agents](#agents).
```
