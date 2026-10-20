## Overview

What the delivery of `I00:E07:W02` was measured to do at `95a7923`, the checks it was held to, and the review the dispatcher ran over it independently of the delivering session's report.

## The Wrapper

Sixteen cases in `src/tests/test_delivery.py`: thirteen over the decision itself and three driving the installed `prosiform` console script end to end through the wrapper, resolved by name rather than by path.

The decision is a pure function of a completed run's status, its buffered bytes and the transport's limit, so each outcome is measured against stated inputs rather than against a process that happened to behave that way.

| Case | Measured |
| --- | --- |
| A run that failed, with Markdown on standard output | Reported as a failed run; the output is not read as evidence of success |
| A bundle within the limit | Delivered, carrying the document |
| A bundle over the limit | Reported as over the transport limit, carrying no document |
| A limit of zero | Refused, because nothing carries no bundle and does not mean unlimited |
| No limit supplied | There is no default; the transport names its own |

One corpus fixture, `fixtures/delivery/a-failing-run-publishes-no-bundle`, states the command-side half of the exit-status clause: a failing run exits nonzero, publishes nothing on standard output, and reports `E_TARGET_NOT_FOUND`. It is the first fixture in the corpus to cite an `Agent delivery contract` clause.

## The Gate

Measured by the dispatcher in a separate worktree at the delivered head, not taken from the delivering session's report.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages, no dependency added |
| `make lint` | All checks passed |
| `make format-check` | 40 files already formatted |
| `make typecheck` | Success: no issues found in 39 source files |
| `make test` | 495 passed |
| `make harness` | 305 passed |
| `make corpus` | 157 fixture(s), 152 pass, 0 fail, 5 awaited, 0 unexpected pass |
| `make smoke` | prosiform installs into an environment and bundles a reference from a source root |
| `make layout` | 3 tree(s) present |
| `make tables` | 13 command(s) and 7 declaration(s) |
| `make links` | Every reference in 6 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |

Nothing regressed and no fixture's `awaiting` marker was lifted or added.

## The Review

The dispatcher reproduced every figure above and checked the substance against the repository rather than against the report.

- **The order the contract names is the order the code takes.** `received()` reads the status before it counts any bytes, so a failed run is a failure however much Markdown it left behind, and only a count within the limit yields a document. Confirmed by reading the function, not by running it.
- **Nothing is substituted for an undeliverable bundle.** The over-limit outcome carries `document` as nothing at all, so there is no partial, no summary and no reference for a caller to follow.
- **The catalogue did not move.** `fixtures/manifest.schema.json` is untouched, so the two-branch window between the schema and the contract stayed shut.
- **The `AC6` blocker is as reported.** The schema's `severity` is a closed enum of `error` and `warning`, and a harness test asserts that the severities the schema admits are exactly the catalogues that exist. An entry-destination record therefore needs a catalogue entry on both branches before it can be emitted or declared.

The dispatcher's own measurement of that blocker's reach: **103 fixtures declare `exit_status = 0`, and 99 of those declare no diagnostics at all**. An emission unconditional on success changes what every one of them states.

## Limitations

Three of the five fixtures the row's Test part named cannot exist, and the row says so rather than approximating them, following [D47](../2026-10-17-prosiform-v1/decisions.md).

- *An output exceeding the transport budget* is the wrapper's limit, and the corpus runner drives the command rather than the wrapper. The build's own output budget is already covered by `fixtures/limits/an-output-byte-budget-crossed`.
- *A broken output pipe* cannot arise in a fixture run: the runner buffers both streams and never closes a pipe early.
- *A successful whole delivery* is a property of the buffer and the limit, invisible from inside a run of the command. A fixture here would appear to exercise the wrapper while exercising the command.

`AC6` is not delivered by this row at all. It is `W05`.
