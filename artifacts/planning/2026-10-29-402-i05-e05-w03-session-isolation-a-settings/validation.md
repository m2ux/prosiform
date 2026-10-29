# Validation — I05:E05 W03

> Task delivery · Created 2026-10-29

## Delivery Checkpoint

- Epic: [I05:E05] Deferred Debt — https://github.com/m2ux/prosiform/issues/374
- Task issue: [#402](https://github.com/m2ux/prosiform/issues/402)
- Branch: `i05/e05/w03-session-isolation-a-settings`, cut from `origin/i05/e05/main`
- Worktree: `/home/mike1/projects/dev/md-composer/.worktrees/i05/e05/w03-session-isolation-a-settings`
- Tested revision: `c56b1d99b23a23c8aa633fa669e9be3b6f994a3d`
- Environment: Python 3.13.16, `UV_CACHE_DIR=/tmp/wb18-uv`, `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"`

## Test Plan

Every row was executed at the head of this branch. Instrument: the eval's own tests under `evals/diagram-following/`, `make check`, and the mutation pass below.

| Test | Description | Coverage | Result |
| --- | --- | --- | --- |
| T1 | A settings file declaring hooks is refused before the first session, naming the file and every declared event | AC1 | ✓ Pass |
| T2 | The stub's log holds no started session and no `results/` directory is written | AC1 | ✓ Pass |
| T3 | A settings file holding only preferences starts its sessions, so the refusal does not over-reach | AC2 | ✓ Pass |
| T4 | A settings file that is not JSON is refused naming the file and the decode error | — | ✓ Pass |
| T5 | The README names the settings file among what the preflight refuses | AC3 | ✓ Pass |
| T6 | `make check` over the whole repository | — | ✓ Pass |

## Checks

### AC1 A settings file declaring a hook is refused before the first session, naming the file and its events

**Where:** `evals/diagram-following/test_run.py::test_a_run_whose_settings_file_declares_a_hook_starts_no_session` (T1, T2)

The test plants `settings.json` in a temporary config directory holding `{"theme": "dark"}` and a `hooks` block declaring `SessionStart` and `PreToolUse`, each with a command. It runs the eval against the stub agent over one workflow in one form, and asserts `CorpusError` matching:

    settings\.json declares a hook for PreToolUse, SessionStart.*remove .*settings\.json before this run

so the refusal names the file and both events, in the order the events are sorted. It then asserts the stub's log is empty and `results/` was never created, so no session started and the run left no record.

`hooking` returns the file and the events whose command list is non-empty, so an event declared with an empty list is not counted as a hook. The refusal is raised from `preflight`, which `run()` calls before it reads the corpus, creates `run_directory` or starts a session, so the refusal costs nothing.

**Result:** ✓ Pass.

### AC2 A settings file holding only preferences starts its sessions

**Where:** `evals/diagram-following/test_run.py::test_a_run_whose_settings_file_holds_only_preferences_starts_its_session` (T3)

The test writes `{"theme": "dark", "model": "claude-haiku-5-5"}` and asserts the run reports one started session and the stub's log holds one entry. A directory may keep the preferences the eval's own configuration needs; only a `hooks` block is a refusal.

T4, `test_a_settings_file_that_is_not_json_is_refused`, holds the reuse of `record_of`: `{not json` is refused matching `settings\.json is not JSON`, and no session starts, as the two existing files are refused.

**Result:** ✓ Pass.

### AC3 The README names the settings file among what the preflight refuses

**Where:** `evals/diagram-following/README.md`, section **Isolation** (T5)

Inspected. The preflight's list now carries three entries; the third reads:

> `settings.json` declaring a hook for any event in its `hooks` block, which delivers that command to a session with no plugin installed at all. The refusal names each event the block declares, and a settings file holding only preferences is no refusal, so the directory keeps its theme and model.

Each statement was read back from `preflight` and `hooking` in `run.py`. The list's opening sentence, "Neither flag suppresses a plugin's hooks, so the preflight refuses a run whose config directory would let one reach a session", still holds: a settings-file hook arrives by the same route. `run.py`'s module docstring states the third refusal beside the other two, naming the events.

**Result:** ✓ Pass.

## Mutation Checks

Each new behaviour was removed or altered in turn and the suite rerun, so each test is shown to observe what it claims. `run.py` was restored from a copy before and after every mutation.

| Mutation | Observed |
| --- | --- |
| `preflight` skips the settings-file refusal | `test_a_run_whose_settings_file_declares_a_hook_starts_no_session` and `test_a_settings_file_that_is_not_json_is_refused` both fail: `DID NOT RAISE CorpusError` |
| the refusal omits the events it found | `test_a_run_whose_settings_file_declares_a_hook_starts_no_session` fails: the message reads `declares a hook, which reaches`, so the events are absent |
| any settings file is refused | `test_a_run_whose_settings_file_holds_only_preferences_starts_its_session` fails, the message naming `SessionStart` for a file declaring none, so the boundary against preferences is observed |
| `preflight` runs after `run_directory` is created | T2 fails on `results/` existing, beside the two plugin tests and the login test, so "before the first session and before any record" is observed |
| `preflight` runs after the sessions settle | `test_a_run_whose_settings_file_declares_a_hook_starts_no_session` fails on the stub log holding an entry, so the refusal is observed to precede the session rather than the record |

## Test Runs

| Run | Command | Result |
| --- | --- | --- |
| Eval tests | `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/` | ✓ 96 passed |
| Harness suite | `make harness` | ✓ 869 passed |
| Full suite | `make check` | ✓ exit 0 — `uv lock --check`, `ruff check`, `ruff format --check`, `mypy` (78 files), `make test` 1302 passed, `make harness` 869 passed, authoring 0 findings, corpus 342 fixtures 0 fail, smoke, layout, tables, links, vocabulary, invocation, conformance, independence 303 clauses, steps |

No paid session ran. Every test drives the stub agent beside the suite, and `make check` never starts `make eval-diagrams`.

## Limitations

- `hooking` counts an event as declared when its value is a non-empty mapping, list or other truthy value. An event declared as a hook map holding only disabled entries is refused although it delivers nothing, since the preflight reads the file's shape rather than each command's enablement.
- The refusal is the config directory's `settings.json` alone. A settings file named elsewhere and applied with `--settings`, or one under a project `.claude/` directory inside a session's workspace, is not read; the injected-context read remains what catches a hook that reaches a session by another path.
- The refusal reads one file. A `hooks` block in a settings file the config directory reaches through an `include` or a profile is not followed.
