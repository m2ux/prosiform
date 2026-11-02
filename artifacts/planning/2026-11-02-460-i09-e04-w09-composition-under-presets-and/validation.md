# Validation

The checks [W09](w09.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `cf382468`, which carries every clause in `main` (I08:E06 and I08:E08 included) and I09:E04's own, the invisible-label amendment `ee8df501` among them; its *Section composition* states *Presets and subst* and *The eligible target* |
| Branch head | `bcf4792a` on `i09/e04/w09-composition-under-presets-and`, with `main` merged at `ef9a884c` (I08:E06 and I08:E08) and `i09/e04/main` at `1c5a6987` (W05 included) |

## T1 Presets Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-selected-preset-governs-the-contribution` | The guide's `Checks` section composes `read.md#inputs`, selecting `read.md`'s `checks` preset; its pair `format.md: stub.md` redirects the link the contribution writes, so the bundle carries the stub's `Paths`, and `W_SUBST_USED` names `read.md:10`. | AC18 |
| `a-selected-group-pair-places-no-contribution` | The `Calls` section composes `read.md#inputs` and links `read.md` whole, selecting a preset whose pair joins `Reading`. The contribution stays beneath `Calls`; the ordinary reference alone places `read.md` in `Reading`. | AC18 |

Result: pass.

## T2 Substitution Fixture

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `the-writers-subst-redirects-a-directive` | The guide's `default` maps `read.md` to `stub.md`, so its directive composes the stub's `Inputs` under a contribution heading naming the stub, the directive points at it, and `W_SUBST_USED` names `guide.md:10`. | AC19 |

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `bcf4792a`. Results:

- Unit tests: 1626 passed. The harness ran 1134.
- Corpus: 473 fixtures, all pass.
- Conformance: 354 clauses read, and no declaration names a missing clause. *Section composition — Presets and subst* is covered by three fixtures.
- Independence: every shaped term is one the contract names, after W08's dispatch fixture stopped naming its `Prepare` section, a term the design no longer states once its usage examples retired.

Result: pass.
