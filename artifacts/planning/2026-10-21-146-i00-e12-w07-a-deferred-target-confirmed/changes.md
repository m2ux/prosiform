# Change List

Every plan change this session applied, and every one it held for the user.

## Applied

- **Task creation — [#147](https://github.com/m2ux/prosiform/issues/147), placed as row `W23` of the deferred-debt epic [#39](https://github.com/m2ux/prosiform/issues/39).** `checks/links.py` applies its inline-link pattern to a document's whole text, so a link form written inside a code span or a fenced block is resolved as a reference. `example/README.md` showed the deferral syntax that way and the check refused it. The issue is raised in the task shape, titled `[I00:E11:W23]`, and the epic's table carries the row. See [validation.md](validation.md).

- **Folded work — epic [#39](https://github.com/m2ux/prosiform/issues/39), `AC24`.** The new row delivers a criterion the epic did not carry: a link form inside literal content passed over by the link check while a link beside it is resolved. Every row of that epic covers at least one criterion, so the row and the criterion are one change.

- **Folded work — [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md), *Adversarial acceptance fixtures*.** The Deferral bullet names the two refusals and the rebased destination this row declares, so the corpus the design calls for and the corpus the repository carries say the same thing.

## Held

- **Folded work — epic [#136](https://github.com/m2ux/prosiform/issues/136), row `W08`.** Recommended: let `W08` state in the published documentation that a deferred link's destination names its target from the allowed source root, alongside what position decides and what the mark defers. `AC9` already names the documentation and the glossary as `W08`'s, and the rebase is a third thing a reader of the mark needs. This row leaves `W08`'s cell and `AC9` as they stand rather than widening either from the row that made the rebase true.

## Not a plan change

- **The example tree carries a deferral.** `I00:E12:W01` left the decision to `W02` and `W02` left it here, because a deferral written before this row would publish a destination relative to its source document, which this row rebases. The tree is where the design's usage examples run, and position's three answers now sit in one place: `modes/plan-mode.md` links the artifact documents it reads, defers the routing document it was reached through, and the tree's README cites the design outside the root. The two `usage-example/` bundles were regenerated once.

- **The output budget is unchanged.** `docs/output-budget.md` measures the `work-planner` closure at `acac858`, a tree carrying no deferral, so no rebased destination enters that figure and the recorded bytes stand.

- **The rewrite is given its destination whole.** `rewrite.edits()` prefixed a number sign to whatever the bundle assigned, which made a bundle fragment the only destination the rewrite could publish. Where a link points is the bundle's question, so the answer is composed where it is decided and the rewrite writes it. The constant that spelled the prefix has no subject left.

- **A loop variable is renamed.** `cli.selected_format()` counted with a local named `index`, which the module now imports from `source` for the heading index a confirmation reads. The local takes the `at` the rest of the module counts with.
