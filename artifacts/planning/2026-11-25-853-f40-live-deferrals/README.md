# Live Deferrals

## Executive Summary

A live session in the eval's `bundle-set` and `briefed` forms bundles the deferred lines its bundles carry. The runner bundles each set in a copy of the form's sources, the instruction runs a line from its bundle's folder as the guide does, and the `claude` and `opencode` harnesses admit `cd` beside `pf`. The stub agent makes the run, so `make eval-harness` fails where a live session would.

[Issue #853](https://github.com/m2ux/prosiform/issues/853) holds the work. It is delivered on `f40-live-deferrals`, cut from `main` at 6a6b78410. [test-results.md](test-results.md) records the validation.

## Commits

| Commit | Layer | Holds |
| --- | --- | --- |
| 149b9bc51 | Workspace layout | `bundles_of` in `run.py` bundles each form into a copy of its sources, so each deferred line names its target from its bundle's folder in a workspace. |
| 359144328 | Session contract | `instruction-bundle-set.md` runs a link from its bundle's folder; `harness.py` admits `cd` beside `pf` for `claude` and `opencode`; the eval `README.md` states both. |
| fe3bb30ef | Harness tests | `stub_agent.py` makes a session's run on a line from its bundle's folder under the harness's rules; `test_run.py` holds AC1 to AC3. |

## Decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Where a live session runs `pf` on a deferred line | From the folder of the bundle that carries it, as the guide states. | The guide and `invocation.md` already prescribe it, so the instruction follows the contract rather than restating another rule. |
| How the sandbox admits that run | `claude` admits `Bash(cd *)` and `opencode` admits `cd *` beside `pf`; `codex` uses its `pf` tool's `cwd`. | `cd` writes nothing; `acceptEdits` and `external_directory` still confine writes and paths to the workspace. |
| Where the runner bundles | Into a copy of the form's sources, for every bundled form. | The layout a session sees is then the layout `pf` wrote, with no path rewriting. |

## Tasks

- [x] Reproduce the line failing from both the workspace and the bundle's folder.
- [x] Bundle in a copy of the sources.
- [x] Align the instruction and the harness permissions with the guide.
- [x] Make the stub run the line, and hold AC1 to AC3 in tests that fail on the old layout.
- [x] Run `make eval-harness` and `make check`.
- [x] Open, review and merge the draft pull request to `main`, and close #853. [#856](https://github.com/m2ux/prosiform/pull/856) merged as e2d7d7e2f; #853 closed with AC1 to AC4 ticked.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [issue.md](issue.md) | Body of issue #853, with its acceptance criteria. |
| [pull-request.md](pull-request.md) | Body of the delivering pull request. |
| [test-results.md](test-results.md) | The validation at the head. |
| [agent-review.json](agent-review.json) | The agent review of the delivering pull request. |
