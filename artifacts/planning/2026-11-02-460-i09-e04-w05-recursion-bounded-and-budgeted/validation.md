# Validation

The checks [W05](w05.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `99bec9f7`, whose *Section composition* states *Nested directives*, *Composition cycles* and *Budgets*, and *Resource limits* the `output-bytes` and `depth` rules |
| Branch head | `981a56bc` on `i09/e04/w05-recursion-bounded-and-budgeted`, cut from `i09/e04/main` at `25d95297` |

## T1 Nested Composition and Cycle Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-directive-inside-a-contribution-composes-beneath-it` | A directive in a contribution's body composes beneath the contribution heading, ahead of the carried subsection; one in that subsection composes beneath it. Each nested link points at its own contribution heading. | AC9 |
| `a-directive-composing-its-own-section-is-refused` | Direct cycle: `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8`, chain `guide.md → guide.md#prepare` | AC9 |
| `a-contribution-composing-its-own-section-is-refused` | Direct cycle inside a contribution: closing directive at `read.md:8`, chain `guide.md → read.md#inputs → read.md#inputs` | AC9 |
| `a-cycle-of-directives-is-refused` | Indirect cycle: closing directive at `review.md:8`, chain `guide.md → plan.md#steps → review.md#checks → plan.md#steps` | AC9 |
| `test_a_cycle_of_directives_names_each_earlier_directive_as_related` | The closing directive is `location`, and `guide.md:8` and `plan.md:8` are `related` | AC9 |

Result: pass.

## T2 Budget Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-multiplying-composition-crossing-the-output-budget` | Nine copies composed from under 400 bytes of sources cross `output-bytes=1000`; `E_RESOURCE_LIMIT`, nothing published | AC10 |
| `test_a_multiplying_composition_fails_before_it_is_whole` | The figure the crossing reports lies between the budget and the whole bundle's bytes: the run stopped at the first crossing emission | AC10 |
| `a-directive-is-a-hop-toward-the-expansion-depth` | A section a contribution's directive reaches is two hops from the entry and crosses `depth=1` | AC10 |

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `981a56bc`. Results:

- Unit tests: 1655 passed. The harness ran 1208.
- Corpus: 478 fixtures, all pass.
- Conformance: 356 clauses read, and no declaration names a missing clause. *Nested directives* is covered by 4 fixtures, *Composition cycles* by 3, *Budgets* by 2.

Result: pass.
