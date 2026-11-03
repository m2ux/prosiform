# Change List — I10:E06 W07

The plan changes this delivery session made under its allowance, and those it held.

## Applied

- **Folded work: bootstrap joins the Claude matrix.** The Claude harness now carries a shell limited to `pf`, so the `bootstrap` form is no longer withheld from it. The default matrix is 26 scenarios, 60 cells and 600 sessions, and `EVAL_BUDGET_TOKENS` is 36 000 000.
- **Folded work: edge-run runbook.** `RUNBOOK.md`'s edge run names `compiled` where it named `staged`.

## Held

- **Overlap with `i10/e04/main` W18.** E04's staged form, its per-start command reading and its Claude `Bash(pf:*)` allowlist are not ported; this branch carries one compiled form with its own `PF_SETS` and `argv(..., pf)`. E04 W19 reconciles E04's scenarios and the two harness changes when E06 reaches `main`.
- **Overlap with `i10/e00/w04-shake-down-the-baseline` (#632, #637).** Its harness fixes sit on a base this branch predates, so `harness.py`, `run.py` and `test_run.py` may conflict when both reach `main`; the later one resolves.
- **Cursor and opencode shells are not confined to `pf`.** Neither CLI offers a command allowlist this harness uses, so `pf` changes nothing on their command lines.
- **Scoring of a compiled session that never runs `pf`.** `unbootstrapped` still applies to `bootstrap` alone; holding a `compiled` session to the run-pf line is E04 W19's.

Initiative creation was not needed.
