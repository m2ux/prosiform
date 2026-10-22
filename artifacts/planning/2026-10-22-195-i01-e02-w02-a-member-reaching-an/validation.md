# Validation

The checks this unit ran, the revision they ran against and what each observed.

**Revision:** `i01/e02/w02-a-member-reaching-an` at `6ff7d37`, cut from `origin/i01/e02/main` at `a56a738`, and again at `62c2a3d` with `origin/i01/e02/main` merged in at `9037a91`.
**Build under test:** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`.

## Repository checks

`make check` runs the repository's whole set — lock, lint, format, typecheck, unit tests, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence — and stops at the first failure.

At `6ff7d37`:

```text
728 passed in 0.69s
598 passed in 8.42s
corpus check: 242 fixture(s), 242 pass, 0 fail, 0 awaited, 0 unexpected pass
link check: every reference in 23 document(s) resolved
vocabulary check: 35 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md
  on origin/engineering, every one defined in docs/glossary.md
conformance report: 244 clause(s) the design states, 0 covered by no fixture,
  0 declaration(s) naming no clause
independence check: every word of every fixture declaration and every report entry
  is one the contract states
```

Exit status 0.

At `62c2a3d`, with W05's member heading merged in, every target holds and the vocabulary check reports the contract term `title case` that W03 marks on the engineering branch and whose glossary entry is not yet in the repository:

```text
726 passed in 0.68s
599 passed in 8.92s
corpus check: 243 fixture(s), 243 pass, 0 fail, 0 awaited, 0 unexpected pass
FAIL title case — the design marks it as a contract term, and docs/glossary.md does not define it
vocabulary check: 1 term(s) the glossary and the contract disagree on
```

Exit status 2. The epic base `i01/e02/main` at `9037a91` reports the same failure, which no revision of this branch carries or can answer: the checks read the design from the contract branch as it currently stands, so a term marked there before its glossary entry reaches the repository fails every branch at once. [#204](https://github.com/m2ux/prosiform/issues/204) carries that reading.

## A group whose members' first contributions carry one heading text

`grouping/two-members-contributing-one-heading-text` declares two members carrying nothing above `--group rules:2`, each contributing `## Style`, with one of them also linking to the other. Both are named as entry references.

```markdown
This bundle was built for [Agents](#agents) and [Common](#common); everything else is material it references.

# Rules

## Style

### Agents

Name the harness.

### Common

Keep paragraphs short.

## Tools

List what it may call, then read [Common](#common).

## Links

Check every link.
```

The entry line names each member at the variant heading naming it, and the internal link from one member to the other reaches `#common` rather than the `## Style` both documents write. `src/tests/test_grouping.py::test_two_members_contributing_one_heading_text_reach_two_destinations` reads the same case through the headings the group records.

Observed: AC3.

## A member whose first contribution is unshared

`grouping/a-whole-document-reference-to-a-member` declares a member carrying nothing above the grouping depth and contributing `## Outcomes`, a heading text no other member carries. Its destination is that merged heading, and the fixture passes on the bytes it already declared. `src/tests/test_grouping.py::test_a_heading_text_one_member_carries_is_that_member_s_destination` reads the same case beside a member sharing nothing.

Observed: AC3.

## No two members of one group sharing a destination

`src/tests/test_grouping.py::test_no_two_members_of_one_group_reach_one_destination` reads a group of four members — one carrying a preamble, two contributing one heading text, one contributing a text no other carries — and holds that each is answered by a heading of its own and no heading answers two.

Observed: AC3.

## The merged arrangement held to what it was

Every fixture declaring a pooled section, a variant heading or a grouping depth passes on the bytes it already declared: `grouping/one-entry-under-a-group`, `grouping/a-reference-to-a-grouping-depth-heading`, `grouping/variant-headings-distinguished-at-more-than-one-segment`, `grouping/structural-ancestors-inside-a-merged-group`, `grouping/a-section-shallower-than-the-grouping-depth`, `grouping/a-document-no-group-matches` and `usage-example/every-document-under-a-directory-merged`. No expectation of a merged section or a variant heading changed in this unit.

Two declarations stating the destination a grouped entry reference reaches were restated to the destinations their own bytes show — `delivery/an-entry-destination-under-a-grouping-rule` and `grouping/a-whole-document-reference-to-a-member` — and both pass on those bytes unchanged.

## The reproduction tree

The tree at [../2026-10-17-prosiform-v1/i01-e02/permutations](../2026-10-17-prosiform-v1/i01-e02/permutations), run as `--group rules:2` with `guide.md` as the entry, emits the arrangement W01 left and the entry line:

```text
[Common](#common), [Agents](#agents), [Limits](#budgets), [Notes](#notes), [Titled](#titled), [Deep](#deep)
```

`agents.md`, whose every region sits at the grouping depth and whose `## Style` `common.md` also writes, is reached at the variant heading naming it. `limits.md` and `nested/deep.md`, which share their heading text with no other member, are reached at their own merged sections as before.
