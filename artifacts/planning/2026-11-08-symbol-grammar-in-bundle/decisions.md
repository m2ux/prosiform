# Decisions

## Confirmed

- Only the guide's Symbol grammar moves into the bundle. Usage, compiling a link and exit status stay in the text bare `pf` prints (user, 2026-11-08).
- The bundle no longer tells its reader to run `pf` (user, 2026-11-08).
- Bare `pf` no longer prints the Symbol grammar (user, 2026-11-08).

## Implementation Details

### Source (`src/prosiform/`)

- `cli.py` — `GUIDE` loses its `Symbol grammar:` block. The parser description (`Run with no arguments, pf prints the guide…`) and the `execute` docstring that names the run-pf line are reworded.
- `bundle.py` — `RUN_PF` is replaced by a `SYMBOL_GRAMMAR` constant holding the three entries as a Markdown bullet list, `pf` in code spans. `instruction_group` emits `# § Instructions`, the list, then `Follow [<first heading>](#<slug>) next.` as its own paragraph. The module docstring, `INSTRUCTIONS` and `opened` docstrings describe the section as holding the symbol grammar.
- `provenance.py` — the `Instruction` docstring names the symbol list in place of the run-pf line. The list is recorded as `Instruction(..., listed=True)`, the form dispatch-set lines already use, so candidate validation reads it as generated content.
- `dispatch.py` — the `TOGETHER` docstring points at the `§ Instructions` section, which now holds what a `⫽` link means.
- `__init__.py` — the package docstring names the fixed symbol grammar in place of the run-pf wording.

### Corpus and tests

- 432 expected bundles under `fixtures/` regenerate: only their `§ Instructions` section changes. A diff check confirms no other byte moves.
- `tests/test_cli.py` — the guide tests assert the guide carries no symbol entries; the "each rule an agent follows" test moves to the bundle constant.
- `tests/test_dispatch_publication.py` — the `⫽ Dispatch Set` heading assertion reads the bundle constant.
- `checks/smoke.py` — `BUNDLE` takes the new opening.
- `evals/diagram-following/` — `workflow.py`, `test_workflow.py` and `harness.py` match the new opening; the two bootstrap skills depend on open question 1.

### Documentation

- `invocation.md` — the guide paragraph drops the symbol rules and the "bootstrap is one instruction" claim.
- `README.md` — "Run `pf` with no arguments for the agent guide" is reworded.
- `docs/dispatch.md` — `## The guide` and `## The run-pf line` become one section stating the `§ Instructions` symbol grammar; inbound links (`#the-guide`, `#the-run-pf-line`, `invocation.md#guide`) are repointed.
- `docs/composition.md`, `docs/glossary.md` (`guide`, `dispatch-set sub-section` rows) — state that the bundle carries the symbol grammar.
- A final grep for `run-pf`, `RUN_PF`, ``Run `pf` ``, `the guidance it prints` returns nothing outside fixtures of unrelated meaning.

### Release

- Every bundle's bytes change, so the previous corpus fails: below `1.0.0` that moves the minor. `src/pyproject.toml` declares `0.21.0`; `contract/v0.21.0` and `python/v0.21.0` are cut after merge.
- One pull request into `main`, opened as a draft and marked ready once review clears.

## Open Questions

1. Skills that bootstrap with "Run `pf`." followed by a hand-written `↳` line (the eval bootstrap skills, and skills in m2ux/workflow-server) get the meaning of `↳` from bare `pf`. Without the Symbol grammar there, those skills lose it.
2. The `↳` entry says "compile its destination with `pf`". How to build that command (path resolution, `--presets`) stays in bare `pf`, so an agent meeting a tagged `↳` still needs one bare call.
3. Whether every bundle carries all three entries, or only the entries for marks it holds.
