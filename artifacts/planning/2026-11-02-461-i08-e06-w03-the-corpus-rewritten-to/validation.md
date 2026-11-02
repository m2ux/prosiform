# Validation

Evidence for each check the work items [w03.md](w03.md), [w04.md](w04.md), [w05.md](w05.md), [w09.md](w09.md) and [w11.md](w11.md) name, on branch `i08/e06/w03-the-corpus-rewritten-to` at `46fa24034`, after merging `origin/i08/e06/main` at `cb6ee8d13` (W07+W10, #566). Every run sets `PROSIFORM_BUILD` to the worktree's build.

## Corpus

`make corpus`: 431 fixtures, 431 pass.

- Thirteen `fixtures/mock/` fixtures state their pair in `guide.md`'s `default` preset as a flow mapping on the line that held `prosiform: {}`, so every expected bundle and every `W_SUBST_USED` location is unchanged; `a-substitute-declaring-a-group-joins-it` keeps its line count by writing `default` as one flow mapping (AC4).
- `a-value-naming-no-markdown-document-is-refused` moves to its preset form; its expected status, code and message terms are unchanged, and its `reference` names the entry reference, `guide.md`, as every preset refusal does (AC4).
- Withdrawn: `a-duplicate-key-is-refused`, `a-self-mock-is-refused` and `a-fragment-only-key-is-refused`, whose preset forms are `fixtures/inclusion/a-duplicate-subst-entry-is-refused`, `a-subst-key-naming-its-value-is-refused` and `a-section-only-subst-key-is-refused`; and `a-redirected-entry-derives-its-name-from-the-substitute`, retired with the entry redirect (W07) (AC4).
- `fixtures/inclusion/no-preset-substitutes-nothing` passes: a link under a `default` stating no `subst` compiles `rules.md` beside a `stand-in.md`, with no diagnostic (AC7).

## Invocation

`make invocation`: 28 statements, each held to the build. The option table has no `-m` row and the build's help names none, compared in both directions (AC1, AC5, AC6).

## Vocabulary

`make vocabulary`: 48 contract terms, each defined in `docs/glossary.md`; the *substitution mapping* entry states the `subst` pairs of a document's presets (AC6).

## Repository Search

A search of the worktree for `"-m"`, `--mock`, `` `-m ``, `mock_scenarios` and `mock-scenarios` finds no file. `checks/mock_scenarios.py`, `checks/tests/test_mock_scenarios.py` and the `mock-scenarios` target are removed, and `make check` names none (AC1, AC5, AC12).

## Unit Tests

`make test`: 1569 pass. `src/tests/test_mock.py` states every run case through a `default` preset pair, and its lookup cases through `Substitution().governed(...)`; the command-line pair-shape, long-form and entry-redirect cases are removed with the option (AC1).

## Make Check

`make check`: exit `0`, including `make conformance` (no declaration naming no clause) and `make harness` (1129 pass) (AC12).
