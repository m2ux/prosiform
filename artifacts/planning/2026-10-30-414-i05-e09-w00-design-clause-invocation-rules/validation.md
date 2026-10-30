# Validation — W00 Design Clause, Invocation Rules and Pin

> Evidence record · Created 2026-10-30

Every check below ran in the worktree `.worktrees/i05/e09/w00-design-clause-invocation-rules` on branch `i05/e09/w00-design-clause-invocation-rules`, at the revision each section names. The build under test was named by `PROSIFORM_BUILD` as `uv run --project <worktree>/src --frozen pf`, the same form the continuous-integration job supplies.

The design amendment is `578093687a55c7ed2dc1110b7347fa80a4f6f0ce` on `engineering`, stating `Link classification and resource handling — The substitution mapping`. The pin in `README.md` names it.

## T1 — A declaration naming the clause fails at the previous pin

**Ran:** `make conformance`, with the pin still at `4c72d818`, and a probe fixture under `fixtures/zz-probe` declaring `Link classification and resource handling — The substitution mapping`.

**Observed:** exit `1`. The report counted `303 clause(s) the design states`, `1 declaration(s) naming no clause`, and failed with:

```text
FAIL Link classification and resource handling — The substitution mapping is declared by zz-probe and names no clause the design states
```

This is the fact the row exists for: a fixture written before the clause lands cannot merge, because conformance reads the design at the pinned revision rather than at the branch the clause was written on.

## T2 — The same declaration resolves at the new pin

**Ran:** `make conformance` at the same worktree with `README.md` pinned to `57809368`, the probe fixture unchanged.

**Observed:** exit `0`. The clause's mapping line changed from `0 fixture(s)` to `1 fixture(s)`, the uncovered count fell from `56` to `55`, and `0 declaration(s) naming no clause` was reported. The probe fixture was removed afterwards; it is not part of this branch.

Every later row's mock fixture resolves against this pin for the same reason.

## T3 — The clause is reported uncovered, not failing, with no declaration naming it

**Ran:** `make conformance` at branch head `ef194933`, the corpus unchanged and no fixture naming the clause.

**Observed:** exit `0`:

```text
Link classification and resource handling — The substitution mapping: 0 fixture(s)
conformance report: 304 clause(s) the design states, 56 covered by no fixture, 0 declaration(s) naming no clause; ...
```

An uncovered clause is the report's measurement rather than its verdict, so the clause states the behaviour without failing the check until W01 lands the first fixture. The clause count rose from `303` to `304` and the uncovered count from `55` to `56`, which is the one clause the amendment adds.

## T4 — `make independence` reports no term this work introduces

**Ran:** `make independence` before the change (`3284 term(s)`) and at branch head (`3309 term(s)`).

**Observed:** exit `0` in both runs:

```text
ok   vocabulary  3309 term(s) from artifacts/planning/2026-10-17-prosiform-v1/design.md, docs/glossary.md and 54 declared name(s)
ok   corpus      348 fixture(s) and their identities
ok   report      the conformance report as it renders
independence check: every shaped term of every fixture declaration and every report entry is one the contract names
```

The check reads its vocabulary from the design at the pin, the glossary, `invocation.md`'s declared names and the example tree's headings. The clause's prose is read from `engineering` at the pinned commit, so the words it uses — `substitution mapping`, `substitute`, `stand-in` — are admitted by the design itself; the two glossary rows keep `make vocabulary` satisfied, which is the half of the rule the design cannot.

## T5 — `make invocation` still agrees with the option tables

**Ran:** `make invocation` before the change and at branch head.

**Observed:** exit `0`, `29 statement(s)` in both runs, unchanged. No option row was added, which is correct: the check compares the table with the build's `-h` output in both directions, so a `-m` row now would fail as an option the command does not offer. The row lands with W01, where the option exists.

## T6 — The bundling rule states what a mapping entry does

Inspected `invocation.md`'s `## Bundling` section, which now carries the rule after its first paragraph: a mapping entry redirects what a reference names; a key is matched against the identity a reference normalizes to; a fragment key redirects that section alone and takes precedence over a document key; both sides resolve from the working directory, so a substitute may lie outside the writing source's root; the substitute is the target outright, its title, group and own links being the ones the bundle carries; every reference is redirected — an entry reference, a referring document, and a compiled, deferred, dispatched or parallel-dispatched target; and a run states each redirected target and each key no reference named, publishing either way.

The design states the same rules with their refusals and their field names, at `Link classification and resource handling — The substitution mapping`. The guide states them in fewer words and names no option row, which is why T5 is unchanged.

## T7 — `make check`

**Ran:** `make check` at branch head `ef194933`, with `PROSIFORM_BUILD` naming the locked build.

**Observed:** exit `0`. The targets that touch this change reported:

- `lock-check`, `lint`, `format-check`, `typecheck` — no Python file changed, and each passed.
- `test` and `harness` — passed.
- `authoring` — passed.
- `corpus` — `348 fixture(s)`, unchanged and green.
- `smoke`, `layout`, `tables`, `links --online`, `vocabulary`, `invocation`, `conformance`, `independence`, `steps` — each passed. `vocabulary` reported `46 contract term(s) ... every one defined in docs/glossary.md`, two more than before the change.

## T8 — No surviving sentence describes resolution as reading only the authored path

**Ran:** a read of every passage in `design.md` and `invocation.md` that states what a reference resolves to, at the pinned revision.

**Observed:** the passages that say a reference resolves from its author's directory within its author's root remain true and are unchanged by the mapping — a mapping entry is applied to the reference a caller authored, and an entry bounded to a root would refuse the case the parameter exists for. The one place resolution is described as deciding what a reference names now carries the mapping beside it, so the clause's own introduction states that the mapping is read before the root and the operator rather than after either. No sentence was found that claims resolution reads only the authored path.
