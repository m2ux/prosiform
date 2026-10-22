# Validation

The checks this unit ran, the revision they ran against and what each observed.

**Revision:** `i01/e02/w05-a-member-heading-that` at `333fbb3`, cut from `origin/i01/e02/main` at `a56a738`.
**Build under test:** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`.

## Repository checks

`make check` runs the repository's whole set — lock, lint, format, typecheck, unit tests, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence — and stops at the first failure.

```text
723 passed in 0.68s
598 passed in 7.40s
corpus check: 242 fixture(s), 242 pass, 0 fail, 0 awaited, 0 unexpected pass
vocabulary check: 35 contract term(s) marked in
  artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering,
  every one defined in docs/glossary.md
conformance report: 244 clause(s) the design states, 0 covered by no fixture,
  0 declaration(s) naming no clause
independence check: every word of every fixture declaration and every report entry
  is one the contract states
```

Exit status 0.

## Two members of one stem in different directories

`grouping/members-of-one-stem-in-different-directories` declares `guides/alpha/notes.md` and `guides/beta/notes.md` under `--group guides:2`, each carrying a preamble and a section at the grouping depth. The two stems agree, so each subsection carries the segment that tells it apart:

```markdown
# Guides

## Overview

### Alpha Notes

What the first run recorded before its sections.

### Beta Notes

What the second run recorded before its sections.

## Findings

### Summary

The first run held throughout.

### Detail

The second run held until the last step.
```

The entry document reaches both members as whole documents, and each reference resolves to the subsection naming its member: `Both runs are recorded: [Alpha](#alpha-notes) and [Beta](#beta-notes).`

Observed: AC7.

## A stem that distinguishes its member on its own

`grouping/a-whole-document-reference-to-a-member` declares `notes/with-preamble.md` beside `notes/bare.md`. One segment tells them apart, so each subsection is headed by its stem and the fixture's bytes are unchanged: `### With Preamble`.

`grouping/a-group-emitting-no-merged-section`, `grouping/an-entry-naming-a-member-carrying-one-heading`, `grouping/a-reference-to-a-member-carrying-one-heading`, `grouping/a-member-named-by-the-title-it-absorbs`, `grouping/a-section-shallower-than-the-grouping-depth` and `usage-example/every-document-under-a-directory-merged` each declare members a stem distinguishes, and each passes on the bytes it already declared.

`src/tests/test_grouping.py::test_a_member_is_named_by_its_stem_less_what_the_group_states` and `::test_a_member_a_stem_distinguishes_is_named_by_that_stem_alone` read the same rule over the names alone, including the trailing word a group's own heading states, which `modes/plan-mode.md` contributes as `Plan`.

Observed: AC7.

## One bundle naming a member one way

`grouping/variant-headings-distinguished-at-more-than-one-segment` carries `guides/alpha/notes.md` and `guides/beta/notes.md` contributing one heading text to one merged section. Its variant headings are `Alpha Notes` and `Beta Notes`, and the subsection naming the second member, which absorbs that member's title, carries the same run:

```markdown
# Guides

## Overview

### Beta Notes

## Findings

### Summary

#### Alpha Notes

The first run held throughout.

#### Beta Notes

The second run held until the last step.
```

`src/tests/test_grouping.py::test_members_of_one_stem_take_the_segments_that_tell_them_apart` holds the subsection headings to the run, and `::test_a_shared_stem_takes_the_segments_that_tell_the_paths_apart` holds the variant headings to the same one.

Observed: AC7.

## Links resolving under the heading text

| Fixture | Reference | Where it resolves |
| --- | --- | --- |
| `grouping/members-of-one-stem-in-different-directories` | Each entry document's whole-document reference to a member | The subsection carrying that member's distinguishing run |
| `grouping/variant-headings-distinguished-at-more-than-one-segment` | An internal link from one member to the other as a whole document | `#beta-notes`, the subsection naming it |
| `grouping/variant-headings-distinguished-at-more-than-one-segment` | The entry line's reference to the selected section | `#findings`, the merged section |

Observed: AC7.

## The merged arrangement held to what it was

`grouping/one-entry-under-a-group`, `grouping/a-reference-to-a-grouping-depth-heading`, `grouping/variant-headings-distinguished-at-more-than-one-segment`, `grouping/structural-ancestors-inside-a-merged-group`, `grouping/a-document-no-group-matches` and `grouping/a-section-shallower-than-the-grouping-depth` declare the pooled sections, the grouping depth that selects them and the variant headings that distinguish contributors. Every pooled section and every variant heading they declare is emitted as it was declared; the one byte-level change across the corpus is the subsection heading naming a member whose stem the group repeats.
