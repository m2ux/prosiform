# Test Results

Results for F28 at `122f0fe05` on `f28-read-the-compiled`, run on 2026-11-19 in the unit checkout.

## T1 Guide Text

`fixtures/cli/informational-guide-response`: `pf` with no arguments exits 0 and prints, among its lines, "Do not open its source yourself: read the bundle pf writes.". `test_cli.py` holds the sentence among the guide's rules. Held.

## T2 Specimen Reading

The deferred-composition specimen compiled by 0.29.0, its link published as `[↳ Counting](../../src/rules.md#counting)`, run with this branch's build installed; each run one agent given the bundle and a folder holding `source.md`:

| Guide | Runs | Read the bundle pf wrote | Read the source document |
| --- | --- | --- | --- |
| 0.29.0 | 5 | 1 | 4 |
| This branch | 5 | 5 | 1, before reading the bundle |

All runs are Haiku 5.5, and every run answered 3 lines and 18 words. Held: each run read the bundle pf wrote.

## T3 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2282 passed), harness (1124 passed), corpus (685 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
