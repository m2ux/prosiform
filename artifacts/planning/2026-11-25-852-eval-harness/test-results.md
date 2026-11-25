# Test Results

Validation observed at `852-eval-harness` head e298a4604b00c4dbcfe620666139ac5c11d39979, based on `main` at 6f103e34d.

## Eval Harness

`make eval-harness`: 858 passed. On `main` at 6f103e34d it reports 819 passed and 39 failed.

## Failing Clusters

Each cluster's tests were run at the parent of the merge that introduced its cause, where they pass, and at that merge, where they fail.

| Cluster | Tests | Started failing at | Cause |
| --- | --- | --- | --- |
| Deferred-line walks | 34 | [#819](https://github.com/m2ux/prosiform/pull/819), F27, merge c6afa79e9 | A bundle names each deferred line's target from the folder it is in. The walk ran `pf` from the form's root on those destinations and found no target, and several tests compared them with names written from the root. |
| Guide opening | 2 | [#810](https://github.com/m2ux/prosiform/pull/810), F24, merge c7629a739 | The guide opens on following a bundle. The tests held a bare `pf` run's output to the guide's earlier first words. |
| Brief sections | 3 | [#841](https://github.com/m2ux/prosiform/pull/841), F34, merge e2dde5e56 | A named brief's sub-section is headed by the dispatch's plain text, and only the dispatch line inside it carries the mark. The tests looked for a heading carrying the mark. |

## Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lint, format, types, 2,323 build tests, 1,155 harness tests and 708 corpus fixtures.

## Main After Merge

#854 merged as f890d8522, directly after #849. `make eval-harness` on `main` at f890d8522: 843 passed, 15 failed. Each failure looks for a bundle file under the full SHA256 preset qualifier the eval's `entry_bundle` derived, which #849 replaced with the preset names.

## Bundle Names

At `852-bundle-names` head d546772c2, based on f890d8522, `entry_bundle` takes `prosiform.cli.selection_name`. `make eval-harness`: 858 passed. `make check` exits 0.

## Live Layout

The tests now resolve each deferred line, but a workspace laid out as the runner lays one out still cannot. In the `deferred-dispatch` workflow's `bundle-set` workspace, the entry bundle's deferred line names its target from the temporary folder the runner bundled in, and `pf` on it fails with `E_TARGET_NOT_FOUND` from both the workspace and the bundle's folder. [F40, issue #853](https://github.com/m2ux/prosiform/issues/853) holds that defect.
