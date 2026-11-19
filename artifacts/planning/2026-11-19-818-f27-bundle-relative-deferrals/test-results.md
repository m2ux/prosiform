# Test Results

Results for F27 at `24cd20729` on `f27-link-from-bundle`, run on 2026-11-19 in the unit checkout.

## T1 Deferral Paths

`test_closure.test_a_deferral_publishes_its_target_from_the_bundle_folder` covers bundle folders inside, beside and outside the working directory. The fixture `deferral/a-deferred-destination-resolves-from-an-output-folder-elsewhere`, run from `source/src` with `-o ../out`, publishes `../../src/rules.md#counting`, and `deferral/a-deferred-link-compiles-from-the-folder-its-bundle-is-in` compiles that link from the bundle's folder with exit 0. The 31 expected bundles carrying deferrals differ from `main` only by the `../` steps before each destination. Held.

## T2 Guide Text

`fixtures/cli/informational-guide-response`: `pf` with no arguments prints that a link is run "from the folder that bundle is in". Held.

## T3 Specimen

The deferred-composition specimen, `tally.md` reading "Count as [¬↳ Counting](rules.md#counting) states.", compiled from `src/` into `out3/` by the branch build, which publishes `[↳ Counting](../../src/rules.md#counting)`; each run one agent given the bundle and a folder holding `source.md`, run with the branch build installed:

| Build | Runs | Reached the rules without searching | Answered 3 lines, 18 words |
| --- | --- | --- | --- |
| 0.28.2 | 5 | 0 | 3 |
| This branch | 5 | 5 | 5 |

All runs are Haiku 5.5. Under this branch, 1 run compiled the link and 4 read the source document directly. Held: every run reached the rules without a file-system search.

## T4 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2282 passed), harness (1124 passed), corpus (685 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
