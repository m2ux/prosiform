# Validation

The checks [W10](w10.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `4958ad38`, *Section composition* unchanged by this row. |
| Branch head | `ba89dc28` on `i09/e04/w10-the-grammar-published-beside` |

## T1 Page Against the Fixtures

| Check | Shows | Criterion |
| --- | --- | --- |
| Worked examples | Each of the page's four `markdown` blocks is a substring of a fixture's bytes: the step and bundle of `titles-from-several-sources-share-one-destination-section`, and the step and bundle of `a-composed-contract-leaves-its-deferred-implementation-absent`. | AC16 |
| Fixture coverage | Every one of the 70 `composition` fixtures is linked under the design rule its manifest names, with `dispatch/a-deferred-directive-in-a-dispatched-bundle-opens-with-a-first-run` for the first run. | AC16 |
| Specification review | The page states the label requests placement and nothing else, reads no meaning into a label or a placed section's title, and describes `[¬ text]` as withholding only. It names no input, output or invariant semantics. | AC16 |

Result: pass.

## T2 Documentation Checks

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `ba89dc28`. Results:

- `make links`: every reference in 143 documents resolved, `docs/composition.md` and its fixture links among them.
- `make vocabulary`: 49 contract terms, each defined in the glossary.
- `make tables`: 19 commands and 8 declarations, each named by a table.
- Unit tests: 1663 passed. The harness ran 1161. Corpus: 498 fixtures, all pass. Conformance and independence pass.

Result: pass.
