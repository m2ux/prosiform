# Validation — W04 and W05 Group and Member Names, Title Case and Destinations

> Evidence · 2026-11-01

Every case below ran in the worktree `.worktrees/i07/e00/w04-refuse-group-and-member`, on branch `i07/e00/w04-refuse-group-and-member`, cut from `i07/e00/main` at `5bffb717`. The build under test is `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The base build is the same `src` and `docs` exported from `5bffb717` into a scratch folder.

## Baseline

One tree reproduced findings 37, 38 and 39 against the base build: a group `my-rules` with members `rules/a-b.md`, `rules/x_y.md` and `rules/-.md`, each with a preamble and a `## Procedure`, beside an entry linking all three.

```
# Entry

Reads [one](#a-b), [two](#x-y) and [dash](#).

# My Rules

## Overview

### A B
...
### 

Preamble dash.
```

The group heading drops its hyphen where a file heading keeps it, the member `rules/-.md` is named by an empty heading, and the reference to it is rewritten to the empty fragment `#`. A group named `-` headed its group with an empty H1, as did a group named `_`.

## T1

**Wordless group names refused, unit.** `src/tests/test_metadata.py::test_a_group_name_whose_title_case_is_empty_is_refused` parses `-`, `_`, `--`, `- _` and `_-_` and asserts `E_INVALID_CONVERSION_METADATA` with the message `prosiform.group must carry a word`. `test_a_group_name_carrying_a_word_is_admitted` admits `a`, `-a-`, `x_1` and `!`. Both pass on the branch.

## T2

**Wordless group name refused, corpus.** `fixtures/grouping/a-group-name-carrying-no-word-fails` declares group `_ -`. Against the base build the run exited 0 and published a bundle; against the branch it exits 1 and publishes nothing:

```
E_INVALID_CONVERSION_METADATA: prosiform.group must carry a word, since its title case is the group's heading; name the group with a character other than a hyphen, an underscore or whitespace
  reference: rules/common.md
  location: rules/common.md:3:10
```

## T3

**Wordless member named by its path text, unit.** `src/tests/test_grouping.py::test_a_member_whose_name_carries_no_word_takes_its_path_text` names `rules/-.md`, `rules/_.md`, `rules/- _.md` and `rules/--.md` beside `rules/kept.md`: each takes `Rules/<stem>.md`, and `kept.md` keeps `Kept`.

## T4

**Wordless member named by its path text, corpus.** `fixtures/grouping/a-member-whose-name-carries-no-word-takes-its-path-text` publishes `### Rules/-.md` as the member's subsection and variant heading, and the entry's reference to the member is rewritten to `#rules-md`. The base build emitted `### ` and `#`.

## T5

**One title case in one bundle.** `fixtures/grouping/one-spelling-for-every-generated-heading` holds an untitled file heading, a group and two members whose names carry hyphens. The branch publishes `# Guides/Field-Notes`, `# Harness-Rules`, and `### Agent-Harness` as both subsection and variant; the base build published `# Harness Rules` and `### Agent Harness` beside `# Guides/Field-Notes`. `test_grouping.py::test_a_group_is_headed_by_its_name_in_title_case` holds `epic-issue-body` to `Epic-Issue-Body` and `plan_mode` to `Plan_Mode`, and the member-name tests hold `Epic-Issue-Body`, `Alpha/Notes`, `A/Plan` and `C/One`.

Six existing fixtures moved with the convention, each by generated headings and their destinations alone: `a-pooled-subset-keeps-group-member-names`, `a-whole-document-reference-to-a-member`, `member-names-distinguished-after-formatting`, `members-of-one-stem-in-different-directories`, `variant-headings-distinguished-at-more-than-one-segment` and `mock/a-substitute-declaring-a-group-joins-it`.

## T6

**Titled parent reaches its title, unit.** `test_grouping.py::test_a_titled_parent_s_whole_document_reference_reaches_its_title` merges a titled parent `rules/guide.md` with `rules/other.md` at depths 1, 2 and 3 and asserts the heading answering the parent's whole-document target is `Guide` at each.

## T7

**Titled parent reaches its title, corpus.** `fixtures/grouping/a-titled-parent-reached-as-a-whole-at-depth-one` and `-two` carry a member linking back to the parent. Against the base build both rewrote the link to `#steps`, the parent's first H2; against the branch both rewrite it to `#guide`, the heading carrying the parent's title — the merged section at depth 1 and the group's H1 at depth 2.

## T8

**The overview wraps content only.** `test_grouping.py::test_members_holding_only_a_first_heading_take_no_overview` merges two members holding only an absorbed title and a merged section: no `Overview` is emitted and `Bare` and `Kept` stand at H2 beneath the group. `test_a_member_carrying_content_above_the_depth_takes_the_overview` keeps the wrapper where one member carries a preamble. `fixtures/grouping/a-member-named-by-the-title-it-absorbs` publishes `## Titled` directly beneath `# Notes`; the base build published `## Overview` then `### Titled`.

## T9

**make check.** `PROSIFORM_BUILD=... make check` exits 0 on the branch: lint, format, types, steps, authoring, the unit tests, harness, 378 corpus fixtures, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and mock scenarios.
