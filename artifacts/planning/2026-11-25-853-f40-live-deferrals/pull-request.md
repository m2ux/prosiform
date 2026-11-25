## Overview

A live session of the diagram-following eval in the `bundle-set` and `briefed` forms bundles the deferred lines its bundles carry. The runner bundles each set in a copy of the form's sources, so a line names its target from its bundle's folder in the workspace. The instruction runs that line from the bundle's folder, as the guide does, and the harnesses admit the run. A stub run of `deferred-dispatch` now makes the run, so the harness fails where a live session would.

## Changes

A bundle names each deferred line's target from the folder it is in, and the eval's runner, instruction and sandbox did not account for it.

### Workspace Layout

- **Bundle in a copy of the sources.**
  `bundles_of` in `run.py` bundles each form into a copy of its sources, so each line resolves from its bundle's folder in a workspace.

### Session Contract

- **Run a line from its bundle's folder.**
  `instruction-bundle-set.md` runs a link in a bundle from the folder that bundle is in, as the guide `pf` prints states.
- **Admit the change of folder.**
  `claude` admits `Bash(cd *)` beside `Bash(pf *)` and `opencode` admits `cd *` beside `pf *`; `codex`'s `pf` tool takes the folder as its `cwd`.

### Harness Tests

- **The stub makes the run.**
  `stub_agent.py` runs a session's line as `cd <folder> && pf '<line>'`, refuses a command the harness's rules do not admit, and answers the call with the build's output and exit.
- **The live layout is held.**
  `test_run.py` holds a prepared workspace's deferred lines to documents it holds, a `deferred-dispatch` session to a passing run of its line, and the instruction, guide and harnesses to one folder.

## Test Plan

| Test | Description | Coverage | Pass |
| --- | --- | --- | --- |
| T1 | `test_a_deferred_line_in_a_prepared_workspace_names_a_document_there` | AC1 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-853-f40-live-deferrals/test-results.md#live-layout) |
| T2 | `test_a_stub_session_bundles_a_deferred_line_from_its_bundles_folder` | AC2 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-853-f40-live-deferrals/test-results.md#live-layout) |
| T3 | `test_the_instruction_guide_and_harnesses_agree_where_a_line_runs` and the harness permission tests | AC3 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-853-f40-live-deferrals/test-results.md#live-layout) |
| T4 | `make eval-harness` and `make check` | AC4 | [✓](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-853-f40-live-deferrals/test-results.md#suites) |

## References

- **R1.** [#819](https://github.com/m2ux/prosiform/pull/819) — Publishes deferrals from the folder each bundle is in.
- **R2.** [Invocation](https://github.com/m2ux/prosiform/blob/main/invocation.md) — Run a link in a bundle as written, from the folder that bundle is in.
- **R3.** [Planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-853-f40-live-deferrals/README.md) — The decision on where a session runs a line, and the validation.
- **R4.** [Agent review](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-853-f40-live-deferrals/agent-review.json) — The review of head fe3bb30ef against `main`, with no finding.
