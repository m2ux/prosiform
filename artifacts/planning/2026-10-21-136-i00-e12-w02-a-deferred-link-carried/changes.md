# Change List

Every plan change this session applied, and every one it held for the user.

## Applied

- **Folded work — [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md), *Adversarial acceptance fixtures*.** The list of fixture families names the deferral family this row declares, so the corpus the design calls for and the corpus the repository carries say the same thing.

## Held

- **Folded work — epic [#136](https://github.com/m2ux/prosiform/issues/136), row `W07`.** Recommended: give `W07` the confirmation of a deferred reference's target. `AC5` states that a reference under the root naming no document, or no heading, fails whether it is compiled or deferred. `W03` delivered that against a base on which a marked reference was compiled, so the deferred half had no subject until this row withheld the compilation, and it is now unobserved. `W07` resolves a deferred reference anyway to rebase its destination to the target's root-relative path, so the confirmation is work it already does. Adding it here would deliver `AC5` from a row scoped to `AC3`, and the epic's rows are being written by four sessions at once, so this row leaves `W07`'s cell alone. The work is raised as [#146](https://github.com/m2ux/prosiform/issues/146), which states what a confirmation covers, and is left unplaced for the decision. See [validation.md](validation.md).

- **Folded work — epic [#136](https://github.com/m2ux/prosiform/issues/136), row `W07`.** Recommended: let `W07` put a deferral in the example tree. `I00:E12:W01` left this row to decide whether `example/work-tracker/modes/plan-mode.md` cites its routing document in prose or defers it with a link. A deferral there would be published with the destination its author wrote, which is relative to the document carrying it; `W07` rebases that destination to the target's root-relative path, which is the spelling the design says a deferred link carries. Writing the deferral now would publish a destination `W07` must change, and regenerate the `usage-example/` bundles and the output budget twice, so the tree is left as `W01` wrote it.

## Not a plan change

- **The mark-stripping paths are removed rather than guarded.** `rewrite.unmarked()`, `rewrite.mark_span()` and the mark span's own edit published a compiled link without its mark, and `bundle.compiled()` and `bundle.emitted_visible()` carried that removal into the text a heading shows. A link the bundle compiles carries no mark, so none of them has a subject, and the two heading maps are now the visible text and its slug. [D59](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) names the stripping among the delivered work its rule leaves without one.

- **The refusals keyed to the old mark are gone from the base, not from this row.** `W04` and `W05` merged into `i00/e12/main` while this row was in flight, retiring `E_MARKED_RESOURCE` and `E_SELF_REFERENCE`. The row was rebased onto that base and keeps neither refusal; the catalogue check, which `I00:E12:W01` recorded red, passes on the rebased revision.

- **The marks the build's own tests wrote are removed where position is the subject.** A test writing the mark to select a dependency now writes the reference unmarked, because a marked reference is one this run withholds. The tests whose subject is the mark — a mark on a reference above the root, and the deferral this row delivers — keep it.
