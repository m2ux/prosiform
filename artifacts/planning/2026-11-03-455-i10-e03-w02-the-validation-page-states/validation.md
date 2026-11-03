# Validation

Evidence for the validation page's invariant row, observed at branch head `118c674f` of `i10/e03/w02-the-validation-page-states`.

## The page lists the invariant

Covers `AC3`. Inspection of `docs/validation.md` shows the invariant table carrying a "One member per destination" row beside Target integrity, stating that each destination answers one member of a group. The row agrees with the design's "One destination answers one member" clause and with the check in `src/prosiform/candidate.py`. Result: pass.

## The page's vocabulary and tables hold

`make vocabulary`, `make tables` and `make links` accept the page with the row. Result: pass.

## The repository checks

`make check`, run with the build under test named by `PROSIFORM_BUILD`, covers lint, types, the unit tests, the 504-fixture corpus, invocation, conformance and independence. Result: pass, exit 0.
