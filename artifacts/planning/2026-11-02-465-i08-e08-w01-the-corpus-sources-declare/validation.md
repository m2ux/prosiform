# W01 Validation

Each check the [work item](w01.md) names, run in the task worktree on branch `i08/e08/w01-the-corpus-sources-declare` with `PROSIFORM_BUILD` naming the worktree's build.

## Revision

- Tested head: `86723dc4bb7634a338d8e0fb73e2b6a81f6438a7`, on epic base `033e9b88` with `origin/i08/e06/main` (`6143af507`) merged in as `e89d808f9`.
- Commits: `940d6352` fails a fixture whose sources declare a setting outside a preset; `86a480cf` states that reading in `checks/README.md` and `checks.md`; `86723dc4` pins the README's design link to `cf3824687`, the engineering revision removing the design's Usage examples clause.
- Design pin: `cf3824687` carries, past the earlier pin `187478e44`, the Usage examples removal and I09:E04 W02's directive recognition wording (`ee8df5019`), a clause this base already stated at the earlier pin. Conformance passes at the new pin.

## T1 Make Corpus

`make corpus` reports `424 fixture(s), 424 pass, 0 fail, 0 awaited, 0 unexpected pass`, with each fixture's sources read for a setting outside a preset.

- A frontmatter scan of every fixture source finds 737 declaring `prosiform`; every key names a preset holding a mapping, except `root` in `inclusion/a-declared-root-is-refused` and the scalar `Target` in `inclusion/a-preset-key-holding-a-scalar-is-refused`, each a fixture expecting `E_INVALID_CONVERSION_METADATA`.
- `git diff --stat e89d808f9 86723dc4 -- fixtures` is empty: no expected bundle or source changed in this task.

Result: ✓

## T2 Make Harness

`make harness` passes 1081 tests. The new cases in `checks/tests/test_corpus_run.py` hold that presets are read as declared, that `group`, `subst`, `root` and a scalar-valued key are each named by source and key, that a fixture expecting the refusal is not read, and that a fixture meeting its manifest still fails and fails the run when its source declares outside a preset.

Result: ✓

## T3 Make Check

`make check` exits 0: lock, lint, format, type checks, 1563 build tests, 1081 harness tests, the corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass. Conformance reports 354 clauses, none of them Usage examples.

Result: ✓
