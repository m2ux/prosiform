# Validation

Evidence for each check the [work item](w08.md) names, run in the unit's worktree at fd58c2e0 with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Inspection

A `grep -i -w 'root\|roots'` over `README.md`, `invocation.md`, `checks.md` and `docs/*.md` finds the repository root four times, the refused `root` key in `docs/sources.md` and `invocation.md`, and the example rule in `checks.md` that a declaration names no root. Nothing else. Each page AC13 names was read through after the rewrite:

- **Sources.** *The root* is now *The declaration* and *The boundary*. A link resolves from its own file and is compiled when its target declares `prosiform`, wherever the target sits, above the working directory included. A target declaring nothing, or a missing one, is text. The working directory bounds entry references and diagnostic paths. The key table lists `group` and `group-depth`, and `root` is named as refused.
- **References.** A dependency names a declaring document. The text table carries "declares nothing" and "does not exist" rows. The mapping and operator prose, and both figures, ask the target's declaration.
- **Architecture.** Figures 2 and 3 ask whether the target declares `prosiform`.
- **Glossary.** **root** is gone. **dependency**, the three operators, **closure**, **substitution mapping** and **substitute** state declaration.
- **Others.** The hierarchy, destinations, validation, selection and bundles pages, the docs index, the invocation, the readme and the `make smoke` row in `checks.md` each state the declaration where they stated a root (AC13).

## T2 Examples

`make examples`: every case exits with its declared status: eight publish, and `refused` exits 1 with `E_TARGET_NOT_FOUND` for `rules/quality.md#reviews`. Every file in `scripts/examples.json` declares `prosiform` and none names a root. No `docs/images/*.svg` carries `root:`. The `references` drawing shows `library/guide.md`, which declares nothing, beside the bundle carrying its link as written (AC14).

The output-budget page states the derived boundary of `skills/work-planner/guidelines.md` where it named a root. Its figures were re-taken from its recipe with every document declaring. The bundle is 307,209 bytes, 45,065 over the default. Left undeclared, `skills/guidelines.md` is text and the bundle is 291,227 bytes (AC14).

## T3 Held Sentences

`make harness`: 1070 passed. `checks/tests/test_authoring.py` finds the three sentences it now holds `docs/sources.md` to.

## T4 Links, Vocabulary and Invocation

`make links`, `make vocabulary` (46 terms, every one defined), `make invocation`, `make tables`, `make layout` and `make steps` each exit 0.

## T5 Full Check

`make check` exits 0 at fd58c2e0 before opening.
