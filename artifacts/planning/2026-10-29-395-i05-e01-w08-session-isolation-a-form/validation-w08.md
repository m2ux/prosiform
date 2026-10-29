# Validation — I05:E01 W08

> Task delivery · Created 2026-10-29

## Delivery Checkpoint

- Epic: [I05:E01] Diagram Following — https://github.com/m2ux/prosiform/issues/333
- Task issue: [#395](https://github.com/m2ux/prosiform/issues/395)
- Branch: `i05/e01/w08-session-isolation-a-form`, cut from `origin/i05/e01/main`
- Worktree: `/home/mike1/projects/dev/md-composer/.worktrees/i05/e01/w08-session-isolation-a-form`
- Tested revision: `57f7f2985f29ff53f8d5179417ce16d7b35c8d36`
- Environment: `UV_CACHE_DIR=/tmp/w08-eval-uv`, `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"`

## Checks

### AC1 — A plugin in the config directory is refused before the first session

**Where:** `evals/diagram-following/test_run.py::test_a_run_whose_config_installs_a_plugin_hook_starts_no_session`

The test plants `plugins/installed_plugins.json` holding one plugin in a temporary config directory, runs the eval against the stub agent, and asserts `CorpusError` matching `installs a plugin.*remove .*installed`. It also asserts the stub's log is empty and `results/` was never created, so no session started. A second test, `test_a_run_whose_remote_settings_enable_a_plugin_starts_no_session`, covers the other file the preflight reads: `remote-settings.json` with an entry true in `enabledPlugins` is refused matching `enables a plugin.*remove .*remote-settings`, and likewise starts no session. `test_a_config_with_no_plugin_starts_every_session` shows the refusal does not over-reach: an installed-plugins file holding no plugin and an empty enable map both start their session.

**Result:** ✓ Pass.

### AC2 — A session carrying context the run did not supply fails the run, naming it

**Where:** `evals/diagram-following/test_run.py::test_a_session_carrying_injected_context_fails_the_run`

`STUB_AGENT_INJECT` makes the stub print a `SessionStart:startup` `hook_response` carrying `additionalContext` before its first turn, as the plugin did in run `20261029T143428Z`. The run raises `CorpusError` matching `1 session(s) carried context this run did not supply.*carried a hook response carrying .*apply its rules skill`. `test_a_run_naming_every_carrying_session_starts_its_sessions` runs two workflows and asserts the message reports `3 session(s)` and names `stub-model/linear/straight-through/bundle/1` once, so every carrying session is named and each once. The run raises before writing `run.json`, so a refused run is not recorded as a completed one. `test_the_context_read_finds_each_form_of_injected_context` holds the read to each form it recognises — a hook response, an appended system prompt and a memory file — and to silence on an init, assistant and result message and on an absent transcript.

**Result:** ✓ Pass.

### AC3 — The README states each mechanism and what the preflight refuses

**Where:** `evals/diagram-following/README.md`, section **Isolation**.

Inspected. The section carries one table row per mechanism, each naming what it keeps out: `CLAUDE_CONFIG_DIR` with the scrubbed `CLAUDE*`/`ANTHROPIC_*` environment, `--strict-mcp-config`, `--disable-slash-commands`, `--tools Read,Write,Edit,Glob,Grep`, `--permission-mode acceptEdits`, `--no-session-persistence`, and the injected-context read. It then states the two files the preflight refuses — `plugins/installed_plugins.json` and `remote-settings.json` — why no flag suppresses a plugin's hooks, and that a run carrying context fails after its sessions finish, naming each one. Each named flag was read back from `agent_argv` and `environment` in `run.py` and matches.

**Result:** ✓ Pass.

## Mutation Checks

Each new behaviour was removed in turn and the suite rerun, so each test is shown to observe what it claims.

| Mutation | Observed |
| --- | --- |
| `preflight` skips the installed-plugin refusal | `test_a_run_whose_config_installs_a_plugin_hook_starts_no_session` fails: `DID NOT RAISE CorpusError` |
| `preflight` skips the remote-settings refusal | `test_a_run_whose_remote_settings_enable_a_plugin_starts_no_session` fails: `DID NOT RAISE CorpusError` |
| the run skips the injected-context read | `test_a_session_carrying_injected_context_fails_the_run` and `test_a_run_naming_every_carrying_session_starts_its_sessions` both fail: `DID NOT RAISE CorpusError` |

An earlier pass of the first mutation was masked: the test ran the full default matrix, whose budget gate raised first. Both new preflight tests now run one workflow in one form, so the refusal is the first thing reached.

## Test Runs

| Run | Command | Result |
| --- | --- | --- |
| Eval tests | `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/` | ✓ 88 passed |
| Full suite | `make check` | ✓ exit 0 — lint, format-check, typecheck, `make test` 1302 passed, `make harness` 831 passed, and every document check |

No paid session ran. Every test drives the stub agent beside the suite.

## Limitations

- The preflight reads the two files the observed plugin and remote settings wrote. A plugin installed by another path the eval's directory might hold — a marketplace cache reached by a settings file the preflight does not read — is not refused; the injected-context read is what catches a session it reaches.
- The injected-context read recognises the three shapes a transcript states it in. An agent adding context under a key none of these names is not read.
- The read runs after the sessions finish and before `run.json` is written, so a refused run spends what its sessions spent. The stub costs nothing; a paid run that carried context would have paid for sessions that measure nothing.

## Merge

- Target `i05/e01/main`: no branch protection, no active rules.
- Auto-close of issues on merge: confirmed disabled for `m2ux/prosiform`.
