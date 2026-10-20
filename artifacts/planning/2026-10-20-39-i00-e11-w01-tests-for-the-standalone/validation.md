# Validation — I00:E11:W01

> Validation record · Created 2026-10-20

The checks under test are the five standalone ones — `smoke.py`, `layout.py`, `links.py`, `tables.py` and `vocabulary.py` — and `documents.py`, the reading three of them share. Every run below is on the task branch `i00/e11/w01-tests-for-the-standalone` at the revision its section names, in the worktree `.worktrees/i00-e11-w01`.

A passing suite says a test ran, not that it observes anything, so each test module is also run against the check it holds with the reading removed. Those runs are recorded under [T3](#t3-the-parsing-each-test-module-observes), and each one is reverted before the next.

## Procedure

| Step | Command |
| --- | --- |
| The harness suite, which the new modules join | `make harness` |
| The repository's whole suite, checks and corpus included | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen prosiform' make check` |
| The anchor capture | `gh api --method POST markdown -f mode=markdown -F text=@headings.md` |

## T1 The slug rule against GitHub's anchors

**Observes AC1.** The link check's heading-slug rule generates the anchors GitHub generates, and the comparison is a command the suite runs.

The oracle is one call to GitHub's Markdown API over a document of nineteen headings. `checks/tests/anchors.json` holds the bytes GitHub was given and the `id` attributes of the response in order, the `user-content-` prefix removed. The headings are the ones a rule parts company with GitHub over: an emoji, a variation selector (U+FE0F), an accent, a code span, a link, emphasis in both spellings, an ampersand between two spaces, an underscore inside a word, a trailing run of hash marks, and a heading written twice, whose second occurrence GitHub numbers `-1`.

`checks/tests/test_slug.py` feeds the captured document to `links.fragments_of` and compares the fragments it generates with the anchor set, and each heading to `links.slug` against the anchor GitHub generated for it.

```text
make harness
443 passed in 6.74s
```

**A heading the rule gets wrong.** The capture named one at once. GitHub's rendering consumes the underscores of `_underlined_` as emphasis and keeps the one inside `Snake_case`; the rule kept both. Running the suite with the emphasis reduction removed from `links.slug` reports it:

```text
E       AssertionError: the rule and GitHub disagree, each heading to (rule, github):
E       {'**Bold** and _underlined_ words': ('bold-and-_underlined_-words', 'bold-and-underlined-words')}
FAILED checks/tests/test_slug.py::test_each_heading_generates_the_anchor_github_generated_for_it
FAILED checks/tests/test_slug.py::test_every_fragment_the_document_generates_is_one_github_generates
2 failed, 441 passed
```

The rule now reduces a run of emphasis to its text, as it already reduced a code span and a link, and the comparison passes. `test_a_heading_the_rule_would_get_wrong_is_reported` holds the second case standing: a rule written in terms of word characters drops the variation selector GitHub keeps, and the test fails if that narrowing ever stops differing from the rule in force.

**What it establishes and what it does not.** It establishes that the rule generates GitHub's anchors for the captured document, as a command rather than as an observation in a record. The capture is recorded, not fetched on every run, so a change GitHub makes to its anchor generation is caught on the next refresh rather than on the next run. A check that reached a third party every run would redden a branch over an outage, which is the verdict `checks/README.md` already takes for a reference.

## T2 Each standalone check's parsing

**Observes AC2.** Each standalone check has tests of its own, running with the others under `make harness`.

| Module | The reading it holds |
| --- | --- |
| `checks/tests/test_slug.py` | The link check's heading-slug rule, against the capture |
| `checks/tests/test_links.py` | The references and heading fragments the link check resolves, beside its reachability cases |
| `checks/tests/test_tables.py` | The Makefile's targets, the project's declarations, and the table rows read against both |
| `checks/tests/test_vocabulary.py` | The design's marked terms, the glossary's definitions and avoided terms, and the design link |
| `checks/tests/test_layout.py` | The tree listings git prints |
| `checks/tests/test_smoke.py` | The status, the two streams and the command path an installed run gives back |

Each case supplies input the parser reads wrongly if its rule drifts, rather than the repository's own documents, where every parse happens to be correct.

```text
make harness
443 passed in 6.74s
```

## T3 The parsing each test module observes

**Observes AC2.** A test module fails when the reading it holds is removed, so the module observes the parsing rather than accompanying it.

Each mutation was applied alone and reverted before the next.

| Mutation | What failed |
| --- | --- |
| `documents.strip_code_fences` returns its text unchanged | `test_links.py::test_every_reference_a_document_carries_is_read`, `test_links.py::test_a_fenced_reference_is_an_example_rather_than_a_reference`, `test_tables.py::test_a_document_carries_the_tables_outside_its_fences`, `test_tables.py::test_a_fenced_table_is_an_example_rather_than_a_row` — 4 failed, 439 passed |
| `tables.RULE` admits a dot-prefixed name and a `:=` assignment | `test_tables.py::test_an_assignment_is_not_a_target`, `test_tables.py::test_makes_own_directive_is_not_a_target`, `test_tables.py::test_a_recipe_line_and_a_comment_are_not_targets` — 3 failed, 440 passed |
| `vocabulary.strip_code` returns its text unchanged | `test_vocabulary.py::test_a_mark_inside_a_code_span_or_a_fence_is_an_example` — 1 failed, 442 passed |
| `layout.tracked_files` splits on newlines without dropping the blank line | `test_layout.py::test_a_listing_names_one_file_for_each_line`, `test_layout.py::test_a_blank_line_names_no_file`, `test_layout.py::test_a_tree_git_tracks_nothing_under_holds_no_file`, `test_layout.py::test_a_tree_lists_the_files_under_it_and_no_others` — 4 failed, 439 passed |
| `smoke.reported` accepts a run that wrote to standard error | `test_smoke.py::test_a_run_writing_to_standard_error_is_refused` — 1 failed, 442 passed |
| `links.slug` keeps the underscores of a run of emphasis | the two reported under [T1](#t1-the-slug-rule-against-githubs-anchors) |

The suite returns to 443 passed after each revert.

## T4 The repository's own suites and checks

**Observes no criterion of this unit.** It holds the change to the repository's standing bar.

```text
PROSIFORM_BUILD='uv run --project <worktree>/src --frozen prosiform' make check
exit 0

ruff check          All checks passed!
ruff format --check 50 files already formatted
mypy                Success: no issues found in 49 source files
pytest (src)        603 passed in 0.59s
pytest (harness)    443 passed in 6.22s
corpus              203 fixture(s), 201 pass, 0 fail, 2 awaited, 0 unexpected pass
smoke               prosiform installs into an environment and bundles a reference from a source root
layout              3 tree(s) present
tables              14 command(s) and 7 declaration(s)
links               every reference in 12 document(s) resolved
vocabulary          34 contract term(s) marked, every one defined
invocation          27 statement(s) of the documented invocation
```

The link check's run is online and resolves the new `checks/README.md` reference to `tests/anchors.json`.

## Observations

- **The capture found a live defect in the slug rule.** The underscore case was not written as a prediction; GitHub answered differently from the rule on the first comparison, and the rule was corrected to the answer. No document in this repository carries a heading with a run of underscore emphasis, so the defect was unreachable by the link check's own run and reachable by the oracle.
- **GitHub's duplicate numbering is the rule's own.** The repeated heading in the capture takes `why-1`, which is what `fragments_of` generates for a second occurrence, so the numbering is held by the same comparison rather than by an expectation of its own.
- **`smoke.py` parses responses rather than documents.** Its reading is the status and the two streams of an installed run, so its tests supply runs rather than text, and the installation steps themselves stay with the check's own command.
