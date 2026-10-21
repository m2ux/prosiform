# Change List

Every plan change this session applied, and every one it held for the user.

## Applied

- **Folded work — epic [#136](https://github.com/m2ux/prosiform/issues/136), rows W04 and W05.** The published documentation and the example tree were corrected to state classification by position, which `W08` would otherwise have carried alongside the deferral. The deferral half of `W08` stands.

## Held

- **Folded work — epic [#136](https://github.com/m2ux/prosiform/issues/136), rows W04 and W05.** Recommended: leave the catalogue check red until those rows land. `checks/tests/test_catalogue.py` fails on the epic base because D59 withdrew `E_MARKED_RESOURCE` and `E_SELF_REFERENCE` from the design while the build still raises them. Adding a note to either row's Description would say what the rows already imply, and removing a code here would deliver the rule that replaces it, which this row is scoped out of.
- **Folded work — epic [#136](https://github.com/m2ux/prosiform/issues/136), row W02.** Recommended: let `W02` decide whether the example tree carries a deferral. `example/work-tracker/modes/plan-mode.md` now names its routing document in prose, because a link under the root is one the bundle carries; once a marked link is withheld from the compilation, that citation could be a deferred link instead. Nothing is wrong with the tree as it stands, and `W02` is the row that can make the change observable.

## Not a plan change

- **The fixture `usage-example/an-unmarked-reference-as-authored` is retired.** Its subject was a citation of a document the bundle already carried, which classification by position cannot produce, and its invocation was not one of the design's published usage examples. The two criteria it touched are observed by `reference/a-document-under-the-root-is-a-dependency` and `reference/a-document-outside-the-root-is-text`.
