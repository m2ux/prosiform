# Change List — I10:E04 W19

The plan changes this delivery session made under its allowance, and those it held.

## Applied

- **Folded work** — the staged-to-compiled move of the edge workflows' trees landed in the merge of `main` into `i10/e04/main` (`7ab77824`) rather than on the task branch: the epic base's corpus loader reads no `staged` form once the code folds it, so the merge could not load the corpus without the move. The task branch carries the mark rewrites and the corpus test.
- **Folded work** — the corpus reader matches a source heading by its slug, which a `¬↳` naming `#read-mirror` needs.

## Held

- **Design decision, epic base merge** — a compiled session's workspace holds the compiled sources beside the bundle set in the folder `pf` writes it to, the entry named at its bundle path, and takes the compiled instruction (`instruction-compiled.md`, formerly the staged one). A `↳` line names its target from the sources, so a bundle set alone cannot compile one. Recommended: keep it; it is the one layout that lets the settled model's compiled session compile `↳` lines. The alternative, the bundle set alone, leaves every deferred scenario uncompilable. Consequence: the four dispatch workflows' compiled sessions now see their sources too.
- **Design decision, epic base merge** — the default `--forms` is every form, so the edge workflows join the default matrix and the baseline (E00 W02): 78 cells, 780 sessions, `EVAL_BUDGET_TOKENS` 46 800 000. Recommended: keep it, since one compiled form leaves no form to hold them apart; the baseline runbook can name its workflows if the edge workflows should stay out of it.
- **Runbook, E04 W16** — the Edge Run names `cursor` and `opencode` alone, while the nested scenarios (`dispatch-depth`, `subagent-first-run`) reach Claude alone, so the edge run as written measures them on no harness. W16's shakedown owns the runbook; recommended: add Claude to the Edge Run's harnesses there.
- **Plan correction** — the work item named `¬⫽` cases in `dispatch-depth` and `subagent-first-run`; the epic base's sources hold none, so nothing changed there.
- **Merge, held** — the merge of #651 into `i10/e04/main` was refused by the session's permission classifier; the pull request stands open, CI green, mergeable. On merge, the W19 row's Done and AC27 are ticked and #622's Changes and References take W19.
