# Change List

Every plan change this session applied, and every one it held for the user.

## Applied

- **None.** The row delivered the scope its work item declares. The corpus gained the two reference fixtures the criterion is read from, the catalogue row gained the clause that declares its code, and the command's suite gained a run for each shape. Nothing was folded in from another row and nothing was carried out of this one.

## Held

- **Criterion coverage — epic [#136](https://github.com/m2ux/prosiform/issues/136), `AC5`.** Recommended: add `AC5` to `W08`'s Coverage. `AC5` reads *whether it is compiled or deferred*, and the deferred half cannot be observed until `W02` gives the mark its deferring meaning. `W03` is the only row whose Coverage names `AC5`, and its row is now delivered, so no row is scheduled to verify the criterion whole and tick it. `W08` already depends on `W03` and integrates the epic's statements, which makes it the row that can read the criterion whole. The change was held rather than applied because it rewrites another row's cell while three sibling sessions are writing this epic body, and the wave's sync pass is where a cell that is not this row's is safely touched.

- **Folded work — epic [#136](https://github.com/m2ux/prosiform/issues/136), rows `W02`, `W04`, `W05` and `W08`.** Recommended: leave the mark-writing unit tests to the rows that retire their subject. `src/tests/test_cli.py`, `test_source.py` and `test_rewrite.py` still write `¬` on references that position alone now classifies, so the mark is inert in most of them and the test reads as though it still selected something. Rewriting them here would be a sweep across three test modules for no change in what any of them observes, and `W02` must revisit most of them in any case: once a marked link is withheld from the compilation, a test writing one no longer describes a dependency. The tests that assert the mark is stripped on rewrite are `W02`'s directly, and those that assert a marked resource or a marked self-reference is refused are `W04`'s and `W05`'s. What survives those three rows is `W08`'s to find.

## Known conditions this row did not change

- **The catalogue check is red on the epic base.** `checks/tests/test_catalogue.py` fails because [D59](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) withdrew `E_MARKED_RESOURCE` and `E_SELF_REFERENCE` from the design while the build still raises them. [`W01`'s record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-21-136-i00-e12-w01-classification-by-where-a/changes.md) held this for the user and named `W04` and `W05` as the rows that clear it. This row changes neither code and adds no diagnostic, so the condition stands exactly as that record left it.

- **The base moved while this row ran.** `W06` merged [#140](https://github.com/m2ux/prosiform/pull/140) into `i00/e12/main` after this branch was pushed. The branch was rebased onto it, both commits applied with no conflict, and every suite re-run against the rebased revision. `W02` had not merged at that point, which is what leaves the deferred half of `AC5` to it.
