# Implementation Evidence — W01

> Delivery · Created 2026-10-24

## Executive Summary

The dispatch operator is reserved and `prosiform.dispatch` is admitted. A link whose text opens with `»` withholds its compilation exactly as a deferral does, publishes its mark, and carries the target's URI-escaped working-directory-relative destination with its fragment retained. The entry document's declared text is emitted after the entry sentence in the bundle's opening line. Two disagreeing declarations fail with `E_INVALID_CONVERSION_METADATA` naming both locations, and a link opening with both operators is refused with `E_UNSUPPORTED_CONSTRUCT` naming the link.

The work is on `i01/e09/w01-a-second-operator-and`, based on `i01/e09/main`, with the contract text on `i01/e09/w01-a-second-operator-and-engineering`, based on `i01/e09/engineering`.

## Diagnostic Code Chosen

The design's diagnostic table names `E_INVALID_CONVERSION_METADATA` for metadata faults. A link written with two operators is a fault in the source the run read rather than in its metadata, so the refusal takes `E_UNSUPPORTED_CONSTRUCT`, the code the profile already declares for a construct in selected content the profile does not admit. The design copy states this beside the rule, and the corpus manifest for [`dispatch/a-link-carrying-both-operators`](../../../../fixtures/dispatch/a-link-carrying-both-operators/manifest.toml) declares it.

## Where Each Criterion Is Shown

| Criterion | Fixture |
| --- | --- |
| AC1 — a dispatched link contributes no content and reaches the bundle carrying its mark | [`dispatch/a-dispatched-reference-is-not-compiled`](../../../../fixtures/dispatch/a-dispatched-reference-is-not-compiled/manifest.toml) |
| AC2 — its destination is the URI-escaped cwd-relative path with the fragment retained | [`dispatch/a-dispatched-destination-named-from-the-root`](../../../../fixtures/dispatch/a-dispatched-destination-named-from-the-root/manifest.toml) |
| AC3 — a bundle whose entry document declares the key opens with that text after the entry sentence | [`dispatch/a-declared-dispatch-text-opens-the-bundle`](../../../../fixtures/dispatch/a-declared-dispatch-text-opens-the-bundle/manifest.toml) |
| AC4 — no declaration leaves the entry line the corpus already records | every `usage-example/` fixture passes unchanged, and [`dispatch/a-metadata-field-carries-no-dispatch`](../../../../fixtures/dispatch/a-metadata-field-carries-no-dispatch/manifest.toml) states it for a `metadata` field |
| AC5 — two declarations carrying different values fail naming both locations and write no output | [`dispatch/two-dispatch-declarations-disagree`](../../../../fixtures/dispatch/two-dispatch-declarations-disagree/manifest.toml) |
| AC6 — a link opening with both operators is refused naming the link | [`dispatch/a-link-carrying-both-operators`](../../../../fixtures/dispatch/a-link-carrying-both-operators/manifest.toml) |
| AC7 — an unknown `prosiform` key still fails and `metadata` has no conversion meaning | [`dispatch/an-unknown-prosiform-key-still-fails`](../../../../fixtures/dispatch/an-unknown-prosiform-key-still-fails/manifest.toml) and [`dispatch/a-metadata-field-carries-no-dispatch`](../../../../fixtures/dispatch/a-metadata-field-carries-no-dispatch/manifest.toml) |
| AC8 — a `¬` link still withholds its target and still requires it | the six `deferral/` fixtures pass unchanged |
| AC9 — the glossary defines the dispatch operator as a contract term | `make vocabulary` reports 38 marked terms on the pinned design, every one defined |
| AC10 — the conformance report maps each clause to its fixture and lists no new uncovered clause | `make conformance` reports 305 clauses, 0 declarations naming no clause |

## AC2 In Detail

The fixture's source writes `../shared/my rules.md#run`, a path relative to the document that carries the link. The bundle publishes `shared/my%20rules.md#run`: the path from the invocation working directory, with the space URI-escaped and the fragment retained. That is the same rule `rebased` already applies to a deferral, so the operator adds no destination rule of its own.

## The Entry Line and the Parallel Fix

The baseline on `i01/e09/main` was red when this work started: 186 corpus fixtures and 41 unit tests failed because the entry line's wording and position drifted from the recorded expectations. That work landed on this branch as `fix/main-red` (pull request #244) while this unit was in progress, so the failure count is measured against it.

The emission was written to compose with that fix rather than to decide it. `entry_line` appends the declared text to the sentence it already emits, at the one call site that emits it, and hard-codes neither the closing phrase nor a position. Moving the entry line therefore moves the dispatch text with it, and the corpus's recorded expectations hold for both.

## Verification

| Check | Result |
| --- | --- |
| `make corpus` | 260 fixtures, 260 pass, 0 fail, 0 awaited |
| `make check` | exit 0 — lock, lint, format, typecheck, unit tests, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance, independence |
| `make harness` | 626 passed |
| `make vocabulary` | 38 contract terms marked, every one defined, every definition carried |
| `make conformance` | 305 clauses, 55 covered by no fixture, 0 declarations naming no clause, 0 codes undeclared |
| `make independence` | every word of every fixture declaration and report entry is one the contract states |
| `make links` | every reference in 51 documents resolved |

The unit suite is green: 0 failures, against 41 at the baseline before `fix/main-red`.

## Plan Changes

None. The epic, the task and the row already stated this work; the reserved planning folder was in place and the row on #242 links it. No row was created, folded, migrated or re-prioritised, and no initiative was needed.
