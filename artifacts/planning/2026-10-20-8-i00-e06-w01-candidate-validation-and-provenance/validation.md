## Overview

What the delivery of `I00:E06:W01` was measured to do at `fc0fd61`, the checks it was held to, and the review the dispatcher ran over it independently of the delivering session's report.

## The Invariants

Twenty-eight build tests in `src/tests/test_candidate.py` give each check a candidate or a record that disagrees with the other and assert the invariant named. Among them: a missing selected region, a region no range accounts for, a destination reaching another heading, a destination reaching no heading, an emitted heading the provenance does not record, a surviving definition, literal bracketed text becoming a link, a rewritten link showing other text, reformatted untouched bytes, a repaired code example, a blank line removed from inside a fence, a heading at another level, a recorded level beyond the sixth, a region recorded twice, and an entry line naming another destination. The positive cases include repeated identical prose in two regions validating, which is the case the contract names as not duplication by itself.

Six corpus fixtures under `fixtures/candidate-validation/` exercise the same invariants end to end on sources that validate: repeated identical prose in two regions; a destination a coinciding slug would reach elsewhere; a definition removed beside its literal example; a selected region between two unselected ones; a code example carried byte for byte; and untouched bytes beside a rewritten link.

## Candidate Validation Publishes Nothing on a Disagreement

`validate()` is the last call in `compose()` before it returns the bundle, so no publication path runs ahead of it. `test_a_candidate_disagreeing_with_its_provenance_publishes_nothing` replaces `assemble` with one that drops a region and asserts the published outcome: exit status 4, nothing on standard output, the named output file absent, and one diagnostic carrying `E_UNEXPECTED_INTERNAL_ERROR` whose message names the invariant.

No new error code was added. The contract names no source-document code for a post-compilation invariant violation, and the internal-error outcome names the run rather than any document the run read, which is what a compiler disagreeing with its own record is.

## The Gate

Measured by the dispatcher in a separate worktree at the delivered head, not taken from the delivering session's report.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages, no dependency added |
| `make lint` | All checks passed |
| `make format-check` | 37 files already formatted |
| `make typecheck` | Success: no issues found in 36 source files |
| `make test` | 479 passed |
| `make harness` | 304 passed |
| `make corpus` | 156 fixture(s), 151 pass, 0 fail, 5 awaited, 0 unexpected pass |
| `make layout` | 3 tree(s) present |
| `make tables` | 12 command(s) and 7 declaration(s) |
| `make links` | Every reference in 6 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |

Against the baseline of 451 unit tests, 298 harness tests and 150 fixtures, nothing regressed and no fixture's `awaiting` marker was lifted or added. The fixture diff against `main` is 221 insertions and no deletions, so no existing fixture was modified and none was weakened.

## The Review

The dispatcher reproduced every figure above and checked four claims against the repository rather than against the report.

- **Nothing published ahead of validation.** Confirmed by reading `compose()` rather than by running it.
- **No catalogue movement.** `fixtures/manifest.schema.json` is untouched, so the two-branch window between the schema and the contract stayed shut.
- **Ownership stability is satisfied by construction.** `source.owner()` takes a token stream and a position and states in its own documentation that a selection does not enter the answer. The absence of a check is correct, and the module says so where a reader would otherwise assume coverage.
- **Region accounting named the wrong invariant.** The region count comparison is an equality, so it already failed a candidate carrying more regions than the provenance accounts for, but reported that as `no accidental omissions`. The contract names omission and expansion as two invariants, and a diagnostic reporting the first for either sends a reader looking for a missing region when content was added. Three tests encoded the wrong name.

The last of these was corrected at `fc0fd61` on the delivery branch, which splits the two and leaves both exercised: one test asserts omission and three assert expansion. The behaviour was already right; the change is which invariant a failure names.

## Limitations

A corpus fixture cannot show a candidate disagreeing with its own provenance. A fixture declares a source tree, an invocation and the bytes published, and a build that works produces no disagreement from any source tree. The disagreement cases are therefore build tests that mutate the candidate or the record, and the published outcome the criterion asserts is covered end to end in `test_cli.py`. The corpus fixtures stand as the positive exercises.

Two invariants are not checked here and are absent rather than weakened: ownership stability, for the reason above, and block-syntax preservation, which is `I00:E08:AC1`. The structural-ancestor half of outline preservation waits on `I00:E09:W02`, which is what emits a structural ancestor; with none emitted, a chain check would run over an empty set and pass whatever the outline did.
