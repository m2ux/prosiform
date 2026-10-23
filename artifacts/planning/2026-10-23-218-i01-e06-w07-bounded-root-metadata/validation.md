# Bounded Root Metadata Validation

## Revision

Runtime branch: `i01/e06/w07-bounded-root-metadata`, commit `31ba28e4e23343caf242172396f7021f8b28b8d9`. Base: `i01/e06/main`. The working tree is clean.

## Schema And Capture

`uv run --project src --frozen pytest src/tests/test_metadata.py src/tests/test_source_metadata.py src/tests/test_conversion_compilation.py` passes as part of the full source suite. AC19 is observed by root declaration location/type/path tests and captured-byte mutation tests. AC23 is observed by exact reserved-key, Core integer, pairing, unrelated-field and obsolete-field tests.

The root value preserves raw spelling and absence. It is independent of grouping and immutable with its physical source location. Bounds remain enforced before decoding/construction. Core integer forms are accepted by value, while booleans, floats and quoted depths fail. Unrelated `metadata` has no conversion meaning; obsolete keys inside `prosiform` fail.

## Full Checks

`PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i01/e06/w07-bounded-root-metadata/src --frozen pf' make check` passes. See [full-check.log](full-check.log).

- Source tests: 975 passed.
- Check-harness tests: 611 passed.
- Corpus: 252 passed, zero failures or awaited fixtures.
- Installed-wheel smoke, lint, formatting, strict typing, lock, layout, tables, online links, vocabulary, invocation, conformance and independence checks pass.
- `git diff --check` passes.

The conformance report retains 22 clauses without fixtures, 16 clauses with no run and three installation claims not observed by a run. These are existing report limitations; this decoder task verifies AC19 and AC23, not per-file root resolution or automatic output publication. The full-check vocabulary/corpus contract remains the project's configured prior runtime snapshot.

## Review

All active schema consumers, example declarations, diagnostics and affected coordinates use the top-level mapping. Fixture body bytes and expected compiled output are preserved. The optional root is captured but runtime root resolution belongs to the following task. Parent review confirmed unrelated metadata semantics, YAML Core integer forms and preservation of root spelling.

## Plan Changes

None. No blocking, trivial or non-trivial debt was discovered beyond the planned runtime work.

## Delivery

[Task PR #228](https://github.com/m2ux/prosiform/pull/228) merged into `i01/e06/main` at `a4769c285df83190c93fcf8fcd18ee707c331c2d`. GitHub Checks passed for exact task head `31ba28e4e23343caf242172396f7021f8b28b8d9`; the target has no branch protection or active rules, and there are no commit-status contexts. The repository auto-close setting is confirmed disabled by the user in this session.

The merged epic-base checkout ran the schema/capture/compilation test command: 196 passed. See [merged-tests.log](merged-tests.log). This verifies AC19 and AC23 against the delivered revision; both are ticked and W07 is Done. Runtime review #222 includes #228 and remains draft. No Development link is required for this task row because it has no task issue. Actual Development-link reads covered both repository PR pages and all nested issue pages; the existing runtime review relation to epic #218 remains present.

The synchronization report also notes a pre-existing contract-review reference discrepancy: #227 cites #226 while the contract base includes #219 and #226. W07 changes the runtime base only and preserves that separate contract review.
