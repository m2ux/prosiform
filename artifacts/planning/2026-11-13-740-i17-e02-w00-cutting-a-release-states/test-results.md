# Test Results

Results for W00 at `41b144bce` on `i17/e02/w00-cutting-a-release-states`, run on 2026-11-13 with `PROSIFORM_BUILD` naming the worktree's `src/.venv/bin/pf`.

## T1 Cutting a Release

A read of [Cutting a release](https://github.com/m2ux/prosiform/blob/41b144bce187644f1340a014153d95edb1b0e598/docs/versioning.md#cutting-a-release): a release is one merge on `main` carrying both tags; step 4 merges the release branch into `main` through the release pull request; step 5 has the annotated `contract/vX.Y.Z` and `python/vX.Y.Z` tags name that release merge. `git show contract/v0.24.0` and `git show python/v0.24.0` each name `6fc54bbf7`, the merge of #705 from `release/v0.24.0`. Held.

## T2 Links

`make links` passes: every reference in 427 documents resolved. Held.

## T3 Full Check

`make check` passes: lint, `make test` (2137 passed), harness (1054 passed), corpus (615 fixtures, 615 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
