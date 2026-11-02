# Validation

The checks [W11](w11.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `26d58ce9`. It carries `aa97db93` and adds the deferral's preset rule to *Presets and `subst`*, the paired-directive rule to *Deferred composition*, and both to the Composition fixture list. |
| Branch head | `749f1e76` on `i09/e04/w11-contradicting-composition-plans-refused` |

## T1 to T3 Deferral Presets

`fetch.md` declares an `offline` preset with the pair `net.md: cache.md`, and the headings `Implementation` and `Implementation offline`.

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-deferral-whose-step-and-target-select-no-preset-is-kept` | Step `Fetch the page`, `[¬→](fetch.md#implementation)`: both select none. Exit 0, the generated `[↳ Implementation](fetch.md#implementation)` line. | AC20 |
| `a-deferral-whose-step-and-target-select-one-preset-is-kept` | Step `Fetch the page offline`, target `Implementation offline`: both select `offline`. Exit 0. | AC20 |
| `an-immediate-directive-is-held-to-no-target-heading` | `[→](fetch.md#implementation)` under `Fetch the page offline`: composed, its nested directive redirected to `cache.md#open` (`W_SUBST_USED`). Exit 0. | AC20 |
| `a-deferral-whose-step-selects-a-preset-its-target-does-not-is-refused` | Step `Fetch the page offline`, target `Implementation`: `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8`, naming `fetch.md#implementation`, `'offline'` and `no preset`. | AC20 |
| `a-deferral-whose-target-selects-a-preset-its-step-does-not-is-refused` | Step `Fetch the page`, target `Implementation offline`: refused alike, naming `no preset` and `'offline'`. | AC20 |

Result: pass.

## T4 Composed and Deferred in One Scope

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-section-composed-and-deferred-in-one-step-is-refused` | `[→](fetch.md#implementation)` and `[¬→](fetch.md#implementation)` in one step: `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8`, naming `'→' at guide.md:8` and `'¬→' at guide.md:8`. | AC21 |

Result: pass.

## T5 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `749f1e76`. Results:

- Unit tests: 1643 passed. The harness ran 1154.
- Corpus: 493 fixtures, all pass.
- Conformance: 354 clauses. *Section composition — Presets and subst* has 8 fixtures and *Deferred composition* 9.
- Independence: every term is one the contract names.

Result: pass.
