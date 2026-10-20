## Overview

What was run over `I00:E11:W14` at `3bbdd54`, what each check observed, and the defect the work found in the arrangement it reports on.

## The Warning

`execute` reads the rules in force against the closure once the bundle is published: `idle()` takes each slug no contributing document belongs to, in declaration order, and one warning carrying `W_EMPTY_GROUP_RULE` is emitted for each, naming the slug. Membership is the arrangement's own rule, so the test asks what the group would carry rather than what the directory holds.

The warning sits between the bundle's publication and the entry destinations, which is where the run's other successful-run diagnostics are.

## The Unit Tests

Three cases in `src/tests/test_cli.py`, each reading standard error as JSON.

| Check | Observed |
| --- | --- |
| `test_a_grouping_rule_the_closure_leaves_idle_is_reported_as_arranging_nothing` | A rule naming a directory the closure reaches no document under: status 0, the diagnostics `W_EMPTY_GROUP_RULE` then `W_ENTRY_DESTINATION`, the warning naming `'docs'` |
| `test_a_grouping_rule_the_closure_carries_a_document_under_arranges_it` | A rule the entry document belongs to: status 0, no `W_EMPTY_GROUP_RULE` on the stream |
| `test_each_idle_grouping_rule_is_reported_and_an_arranging_one_is_not` | Three rules in force, one of them arranging: two warnings, naming `'docs'` and `'other'` in declaration order, the arranging slug absent |

All three pass. The run of the whole build suite is 606 passed, up from 603 by these three.

## The Corpus Fixture

`fixtures/grouping/a-rule-matching-no-document-in-the-closure` declares the clause: a rule for `other:2` with `docs/guide.md` as the entry, exit status 0, the published bundle, and `W_EMPTY_GROUP_RULE` ahead of `W_ENTRY_DESTINATION` on standard error. It carried `awaiting = "I00:E11:W14"`, which this row removes, and `fixtures/README.md` now names the one fixture still carrying a marker, `reference/a-marked-link-inside-image-alternative-content`.

The fixture reports `pass` rather than `awaited`, and the corpus count moves from 201 pass and 2 awaited to 202 pass and 1 awaited over 203 fixtures.

## The Gate

Every target the repository declares, run in this row's worktree at the delivered head. The corpus and invocation targets were given this checkout's build as `PROSIFORM_BUILD`.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 606 passed |
| `make harness` | 379 passed |
| `make corpus` | 203 fixture(s), 202 pass, 0 fail, 1 awaited, 0 unexpected pass |
| `make smoke` | prosiform installs into an environment and bundles a reference from a source root |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) held to the build |

## The Review

- **The change is confined to the stated surface.** Four files: `src/prosiform/cli.py`, `src/tests/test_cli.py`, the fixture's `manifest.toml` and `fixtures/README.md`. No other diagnostic moved, and the help text the invocation check reads is untouched.
- **A rule that arranges something stays silent.** Held by a test of its own and by every other grouping fixture, each of which declares its diagnostics exhaustively and none of which gained a warning.
- **The warning carries the code and the slug and nothing else.** No `reference` field: the contract's field names a reference a source wrote, and a directory slug is not one.

## What It Found

A merged group whose members emit no heading that answers the entry reference crashes the run with `E_UNEXPECTED_INTERNAL_ERROR`. `entry_line` indexes the last of the destinations and the list is empty, so a source of a single H1 under a grouped directory, named as the entry, returns status 4 and publishes nothing.

The defect is present on the epic base, at `9ffb716`, independently of this row: the same invocation fails from an untouched worktree at that commit. It blocks none of this row's criteria — the fixture's idle rule arranges no member at all — so it is deferred rather than fixed here, and the row's own tests give their grouped documents a section so they exercise the arrangement rather than the crash.
