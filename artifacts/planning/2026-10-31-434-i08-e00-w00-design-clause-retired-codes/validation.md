# Validation — W00 Design Clause, Retired Codes and Pin

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i08/e00/w00-design-clause-retired-codes` on branch `i08/e00/w00-design-clause-retired-codes`, cut from `i08/e00/main` at `23882b7d`. The build under test was named by `PROSIFORM_BUILD` as `uv run --project <worktree>/src --frozen pf`, the same form the continuous-integration job supplies.

The design amendment is `5306e0f3` on `engineering`: inclusion stated as a property of the target document, `root` refused as an unknown key, `E_ROOT_NOT_FOUND` retired, and the selection, capture, resolution and safety clauses stated against the declaration. The pin in `README.md` names it.

## T1 — The clause set the epic's fixtures cite is absent at the previous pin

**Ran:** `make conformance` at the previous pin `4c72d818`, the corpus unchanged.

**Observed:** exit `0`, `303 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause`. No clause of the `fixtures/inclusion/` family exists, so no fixture could name one.

## T2 — The amendment lands and the pin names it

**Ran:** `git push origin engineering` from the engineering worktree, then `make conformance` at the new pin `5306e0f3`.

**Observed:** exit `0` once the fixtures are repointed, `306 clause(s) the design states` against `303` before, `0 declaration(s) naming no clause`.

## T3 — The corpus is unchanged by the amendment

**Ran:** `make corpus` at the new pin, the build unchanged.

**Observed:** exit `0`, `349 fixture(s), 349 pass, 0 fail, 0 awaited, 0 unexpected pass`. No source tree, invocation or expected bundle in the corpus changes, which is the property the clause states: the bundles the example published before this epic are the ones it publishes after it.

## T4 — The two renamed clauses are the only failing declarations

**Ran:** `make conformance` at the new pin, then again after the 17 manifests naming the two renamed clauses were repointed.

**Observed:** before, `2 declaration(s) naming no clause`; after, `0`. The two are `Local Markdown document links under the root`, now `Local Markdown document links`, and `Local Markdown links resolving outside the root`, now `A link naming a document that declares nothing`. Seventeen fixtures across ten families named them; no fixture tree, invocation or expected bundle changes.

## T5 — The checks other than the harness

**Ran:** `make conformance`, `make invocation`, `make authoring`, `make corpus` at the branch head.

**Observed:** conformance `306 clause(s) the design states, 58 covered by no fixture, 0 declaration(s) naming no clause`; invocation `29 statement(s)`; authoring `0 finding(s)`; corpus `349 fixture(s), 349 pass, 0 fail`.

## Findings

- **Blocking, and outside this row.** `make check` fails `test_a_catalogue_is_the_codes_the_design_declares[warning-W_]`, and CI reproduces it: the design at `engineering` declares `W_MOCK_SUBSTITUTED` and `W_MOCK_UNUSED`, and the build's catalogue in `fixtures/manifest.schema.json` declares neither.
- **The cause is a pin join, not this amendment.** The schema change landed at `12803a9e` on `i05/e09/main`, which has never merged to `main`; the design statements landed at `5d9a3567` on `engineering`. Moving the pin to any `engineering` revision carrying those statements exposes the gap.
- **The row's own amendment is inert against it.** `make conformance`, `make invocation` and `make authoring` all pass, and `make corpus` runs 349 fixtures with none failing.
- **The consequence.** CI cannot go green until `i05/e09/main`'s schema reaches `main`, which is `I08:E07`'s base and not this row's to merge.

The design amendment is committed to `engineering` at `5306e0f3`; the branch carries the pin move and the 17 manifest declarations that follow the two renamed clauses.

## T6 — The review found the amendment self-contradictory, and the fix

**Ran:** a read of the amended design against the code table it states, and a run of the build on a document declaring `root`.

**Observed:** the catalogue still carried `E_ROOT_NOT_FOUND` as a live row and `E_INVALID_CONVERSION_METADATA` still described a malformed root value, three lines below the clause refusing `root`. Six further clauses named a root the document no longer has. The rows are removed, the retirement is stated once where the catalogue ends, and the remaining clauses are restated. `make conformance` reports `305 clause(s)`, `0 declaration(s) naming no clause`, `0 declared code(s) the build reports nowhere`.

**Also observed:** the build accepts a document declaring `root`, because the refusal is W01's work. The design states it ahead of the build, which is what a design clause does; no fixture names it yet, so the corpus is unaffected.
