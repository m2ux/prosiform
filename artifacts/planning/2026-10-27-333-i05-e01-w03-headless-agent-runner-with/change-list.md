# W03 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| The session limits its tools with `--tools Read,Write,Edit,Glob,Grep` and carries no `--allowedTools`. | `--allowedTools` pre-approves tools without removing any, so Bash would still exist, and a bare `Read` approval would let a session read outside its workspace. `--tools` leaves no Bash tool; under `acceptEdits` a read or edit outside the workspace is not approved, and a non-interactive session cannot grant it. |
| The prompt goes on standard input. | `--tools` takes a variadic list, which would swallow a prompt given as the last argument. |
| Every form's entry in the workspace is `workflow.md`. | The instruction names one entry, so the forms differ only in their material. |
| `--budget-usd` is required. | A paid run never starts without a cap of its own. |
| A session waits while the caps in flight leave no room, and the run stops only when none is in flight. | Parallel sessions stopping at the first refusal would leave budget unused once those in flight settle below their caps. |
| A session reporting no cost settles at its cap. | A crashed or silent session's spend is unknown; charging the cap keeps the run within its budget. |
| `--agent-command` is a command line; `--results` and `--run-id` are options. | The tests start the stub as `python stub_agent.py` and write records under a temporary directory with a known name. |
| `checks.md`, `src/README.md` and the Makefile's harness comment name the runner. | In scope: they describe what `make harness` holds. |
| `--session-timeout-seconds` (600): on expiry the session's process group is killed, `exit_status` is `timeout`, its `trace.log` and `actions/` are kept and scored, and it settles at its cap when it reported no cost, so the run continues. | Planner decision on PR #337: a hung session held its worker and its reservation. |
| Sessions run on the claude.ai team login under an eval root, without `--bare`. `--eval-root` (default `~/projects/eval/prosiform`) holds `config/`, passed as `CLAUDE_CONFIG_DIR`, and `workspaces/<run-id>/<cell>/`. The command adds `--strict-mcp-config` and `--disable-slash-commands`. The session's environment drops every `CLAUDE*` and `ANTHROPIC_*` variable — a superset of the directed `CLAUDECODE`, `CLAUDE_CODE_*`, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL`, so variables such as `CLAUDE_EFFORT` cannot reach it either — and keeps the rest. A run whose `config/` holds no `.credentials.json` (the file the CLI writes in its config directory, checked by presence only) fails before starting a session and names the login command. | User decision on the held credential question: `--bare` authenticates by `ANTHROPIC_API_KEY` alone, and the host holds only a claude.ai team login. |

## Held

| Change | Reason |
| --- | --- |
| The live `claude-haiku-5-5` session runs once the eval login exists. | Resolved credential question; the login is the user's step, and the planner runs the session. |
| Ancestors of the eval root are not shielded: without `--bare`, a `CLAUDE.md` in `~/projects/eval/`, `~/projects/` or `~` would reach every session. None exists today. | Arising hazard of dropping `--bare`; `--setting-sources` and an explicit system prompt are the levers if one appears. |
