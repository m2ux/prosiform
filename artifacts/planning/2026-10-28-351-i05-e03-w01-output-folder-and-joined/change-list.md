# I05:E03:W01 Change List

The plan changes this delivery session made under the deliver-mode allowance, and those it held.

## Applied

- **Folded work, I05:E03 W01.** The diagram renderer (`scripts/render-diagram.py`, `docs/diagram-renderer.md`) read its bundle from standard output, so W01 moves it to the folder and names its saved bundle `.bundle.md`; the epic's component map did not list it.
- **Folded work, I05:E03 W01.** `.gitignore` ignores `*.bundle.md`, so W01 tracks `fixtures/**/expected/*.bundle.md` for the renamed expected bundles to be committed.
- **Folded work, I05:E03 W01.** The README diagrams (`docs/images/compilation.*`, `docs/images/agent-rules.*`) named bundles `skill-bundle.md`, `codex-bundle.md` and `claude-bundle.md`, which no run derives; W01 relabels them with derived names, and `example/README.md` cites the one diagram the README shows.
- **Folded work, I05:E03 W01.** `fixtures/cli/output-naming-an-input-source` is removed: a derived bundle name never names its own entry, so the case cannot be stated; `output-naming-a-dependency-source` carries the refusal.
- **Folded work, I05:E03 W01.** `expected.absent` is retired with `expected.stdout`: the runner compares every file a run creates, which subsumes a declared-absent path.

## Held

None.

## Deferred debt and arising issues

None. Each item the validation found was fixed in the unit.
