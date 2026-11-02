# Validation

Checks run in the unit worktree on branch `i08/e04/w00-design-clause-the-variable` at `b47ee607`, with the README pinning design revision `5511a5a8b10192e978f8b1319f9eb254e3f550f4` and `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## make conformance

Observes AC7.

- The design at the pin carries the section and its three rules: the report lists `Conformance faults`, `Conformance faults — Values`, `Conformance faults — Absent` and `Conformance faults — Unknown value` among the clauses it states.
- The report closes with `0 declaration(s) naming no clause`, so every clause the epic's fault fixtures name — `Source consistency`, `Exit status and JSON diagnostics — 4`, `Validation and failure contract — Publication` among them — is one the pinned design carries.
- No section of the design names `-x` or a fault option: the CLI contract's option table and its invalid-usage list carry none.
- The four new clauses are reported as covered by no fixture; the epic's later rows add the fixtures that name them.

Result: pass.

## make check

The full set of repository checks, `make conformance` among them, exits `0`.

Result: pass.
