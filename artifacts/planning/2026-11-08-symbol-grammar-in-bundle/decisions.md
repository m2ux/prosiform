# Decisions

## Confirmed

- The bundle's `§ Instructions` section carries the Symbol grammar (user, 2026-11-08).
- The bundle no longer tells its reader to run `pf` (user, 2026-11-08).
- Bare `pf` prints the guide as it does today, Symbol grammar included (user, 2026-11-08).
- The Symbol grammar is one object in the code, rendered by both the guide and the bundle (user, 2026-11-08).
- Every bundle carries all three entries, whatever marks it holds (user, 2026-11-08).

## Implementation Details

### Source (`src/prosiform/`)

- `symbols.py` (new) — `SYMBOLS`, a tuple of `(mark, meaning)` entries holding the three rules in the guide's current wording, plain text with no Markdown syntax. It is the only home of that wording. `docs/architecture.md` lists the module.
- `cli.py` — `GUIDE` builds its `Symbol grammar:` block from `SYMBOLS`, keeping today's layout (two-space indent, wrapped continuation lines), so bare `pf` prints identical bytes. The `execute` docstring that names the run-pf line is reworded.
- `bundle.py` — `RUN_PF` goes. `instruction_group` emits `# § Instructions`, `SYMBOLS` rendered as a Markdown bullet list (`- ↳ names …`), then `Follow [<first heading>](#<slug>) next.` as its own paragraph. The module docstring, `INSTRUCTIONS` and `opened` docstrings describe the section as holding the symbol grammar.
- `provenance.py` — the `Instruction` docstring names the symbol list in place of the run-pf line. The list is recorded as `Instruction(..., listed=True)`, the form dispatch-set lines already use, so candidate validation reads it as generated content.
- `dispatch.py` — the `TOGETHER` docstring points at the `§ Instructions` section, which now holds what a `⫽` link means.
- `__init__.py` — the package docstring names the fixed symbol grammar in place of the run-pf wording.

### Corpus and tests

- 432 expected bundles under `fixtures/` regenerate: only their `§ Instructions` section changes. A diff check confirms no other byte moves.
- `tests/test_cli.py` — the bare-command test still asserts `GUIDE` byte for byte. A new test asserts the guide and a bundle's `§ Instructions` section each carry every `SYMBOLS` entry.
- `tests/test_dispatch_publication.py` — the `⫽ Dispatch Set` heading assertion reads `SYMBOLS`.
- `checks/smoke.py` — `BUNDLE` takes the new opening.
- `evals/diagram-following/` — `workflow.py`, `test_workflow.py` and `harness.py` match the new opening. The bootstrap skills ("Run `pf`." then a `↳` line) are unchanged, because bare `pf` still states `↳`.

### Documentation

- `invocation.md` — the guide paragraph is unchanged. The sentence "Every bundle opens with the run-pf line…" states that every bundle opens with the symbol grammar.
- `docs/dispatch.md` — `## The run-pf line` becomes `## The instructions section`: the bundle states the symbol grammar the guide states, from one source. `## The guide` drops "and in no bundle". Inbound `#the-run-pf-line` links are repointed.
- `docs/composition.md`, `docs/glossary.md` (`guide`, `dispatch-set sub-section` rows) — state that the bundle carries the symbol grammar and that a sub-agent needs no `pf` call to read it.
- A final grep for `run-pf`, `RUN_PF`, ``Run `pf` ``, `the guidance it prints` returns nothing outside fixtures of unrelated meaning.

### Release

- Every bundle's bytes change, so the previous corpus fails: below `1.0.0` that moves the minor. `src/pyproject.toml` declares `0.21.0`; `contract/v0.21.0` and `python/v0.21.0` are cut after merge.
- One pull request into `main`, opened as a draft and marked ready once review clears.

## Open Questions

1. The `↳` entry says "compile its destination with pf". How to build that command (path resolution, `--presets`) stays in bare `pf`, so an agent meeting a tagged `↳` still needs one bare call. Whether the bundle says so.
