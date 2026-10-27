# W03 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| The session limits its tools with `--tools Read,Write,Edit,Glob,Grep` and carries no `--allowedTools`. | `--allowedTools` pre-approves tools without removing any, so Bash would still exist, and a bare `Read` approval would let a session read outside its workspace. `--tools` leaves no Bash tool; under `acceptEdits` a read or edit outside the workspace is not approved, and a non-interactive session cannot grant it. |
| The prompt goes on standard input. | `--tools` takes a variadic list, which would swallow a prompt given as the last argument. |
| Every form's entry in the workspace is `workflow.md`. | The instruction names one entry, so the forms differ only in their material. |
| `--budget-usd` is required, and a run without `ANTHROPIC_API_KEY` fails before starting a session. | The work item's review: a run with no credential fails before spending. `--bare` reads no other credential. |
| A session waits while the caps in flight leave no room, and the run stops only when none is in flight. | Parallel sessions stopping at the first refusal would leave budget unused once those in flight settle below their caps. |
| A session reporting no cost settles at its cap. | A crashed or silent session's spend is unknown; charging the cap keeps the run within its budget. |
| `--agent-command` is a command line; `--results` and `--run-id` are options. | The tests start the stub as `python stub_agent.py` and write records under a temporary directory with a known name. |
| `checks.md`, `src/README.md` and the Makefile's harness comment name the runner. | In scope: they describe what `make harness` holds. |

## Held

| Change | Reason |
| --- | --- |
| The live `claude-haiku-5-5` session is not run. Options: provide an `ANTHROPIC_API_KEY` for the one session (recommended — the session command stays as planned); pass an `apiKeyHelper` through `--settings`; or drop `--bare` and isolate with `--setting-sources`, `--strict-mcp-config` and an explicit system prompt on the claude.ai login, which changes the session command and draws on the team subscription. | `--bare` authenticates by `ANTHROPIC_API_KEY` alone and the host holds only a claude.ai login. W05's cost estimate and the `result` field names wait on it; W05 needs the same credential. |
