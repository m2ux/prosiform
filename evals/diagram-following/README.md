# Diagram-Following Eval

How well an agent, given a workflow drawn as a Mermaid diagram whose nodes link the sections saying what to do in each state, follows that workflow to completion. The eval gives each workflow to headless agent sessions, scores the path each session took, and compares the pass rates with a committed baseline.

## Forms

Each workflow in [`workflows/`](workflows) is written twice, as [`workflow.py`](workflow.py) describes: once as a diagram and once as prose whose transitions are sentences. A session receives one of three forms, always entered at `workflow.md`:

| Form | Material | What it isolates |
| --- | --- | --- |
| `bundle` | The diagram form bundled by `pf` into one file. | The product under test. |
| `tree` | The diagram form's source tree, unbundled. | Against `bundle`, what bundling adds. |
| `prose` | The prose form bundled by `pf` into one file. | Against `bundle`, what the diagram adds. |

Every session is given the same [instruction](instruction.md), naming only the entry document. Each scenario in a workflow's `scenarios.toml` names the inputs a session finds under `inputs/` and the path a correct session walks.

## Scoring

A session records each state it enters as a line of `trace.log` and does each state's action by writing a file under `actions/`. The [scorer](score.py) passes a session whose trace is its scenario's path with every state's action done. A failing session takes the first of seven classes that fits where its trace departs from the path:

| Class | The session |
| --- | --- |
| `missing_action` | walked the path and left a state's action undone or wrong. |
| `unfinished` | stopped partway along the path. |
| `invented_state` | entered a state the diagram does not hold. |
| `loop_miscount` | left or repeated a loop at the wrong count. |
| `wrong_branch` | took the other branch of a decision on an input. |
| `skipped_state` | jumped ahead, omitting states between. |
| `invalid_transition` | entered a state no edge leads to: a step back, a state after the end, or the same state again. |

## Login

Sessions run on the eval's own Claude login, kept apart from yours in `<eval-root>/config`, where the eval root defaults to `~/projects/eval/prosiform`. Log in once:

```bash
CLAUDE_CONFIG_DIR=~/projects/eval/prosiform/config claude
```

then `/login`. A run whose configuration directory holds no login fails before it starts a session. Each session runs `claude -p` in a fresh workspace under the eval root with that configuration directory, no MCP server, no slash commands, file tools only and an environment holding no other Claude or Anthropic variable.

## Running

| Command | Runs |
| --- | --- |
| `make eval-diagrams` | The [runner](run.py) over the default matrix, then the report. A default run costs about USD 4 and takes about 10 minutes; its budget is USD 75. `ARGS='...'` passes the runner's options through. |

The command starts paid agent sessions, so no other target depends on it and `make check` never runs it; `make harness` holds the runner, scorer and report against a stub agent and recorded results instead. The runner's options, each passed through `ARGS`:

| Option | Default | Meaning |
| --- | --- | --- |
| `--budget-usd` | 75 under `make eval-diagrams`; required otherwise | The run's spending cap, at least the sessions times `--session-budget-usd`. A later value in `ARGS` overrides the default. |
| `--session-budget-usd` | 0.50 | Each session's spending cap. |
| `--session-timeout-seconds` | 600 | How long a session runs before it is ended and scored as it stands. |
| `--models` | `claude-haiku-5-5,claude-sonnet-5-5` | The models, comma-separated. |
| `--workflows` | every workflow | The workflows, comma-separated. |
| `--forms` | `bundle,tree,prose` | The forms, comma-separated. |
| `--repetitions` | 5 | Sessions per model, form and scenario. |
| `--parallel` | 4 | Sessions running at once. |
| `--eval-root` | `~/projects/eval/prosiform` | The directory holding the login and the workspaces. |
| `--agent-command` | `claude` | The agent's command line. |
| `--results` | `results/` beside this file | Where runs are recorded. |
| `--run-id` | the start time, as `YYYYMMDDTHHMMSSZ` | The run's directory name. |

For example, one model over one workflow:

```bash
make eval-diagrams ARGS='--models claude-haiku-5-5 --workflows linear --repetitions 1 --budget-usd 2'
```

### Default matrix and cost

The default matrix is two models, `claude-haiku-5-5` and `claude-sonnet-5-5`; the five scenarios of the three workflows; the three forms; and five repetitions: 150 sessions. A default run costs about USD 4.01, the `cost_usd` the committed baseline records for its run, and takes about 10 minutes at four sessions at once. By model:

| Model | Sessions | Mean cost per session (USD) | Run cost (USD) | Mean session duration |
| --- | --- | --- | --- | --- |
| `claude-haiku-5-5` | 75 | 0.0038 | 0.29 | 15 s |
| `claude-sonnet-5-5` | 75 | 0.0496 | 3.72 | 18 s |

The costliest session recorded USD 0.088. `make eval-diagrams` passes a budget of USD 75, the 150 sessions at the USD 0.50 session cap, so it starts every session of the default matrix.

A run whose budget is less than its sessions times the session cap is refused before it starts a session, naming the budget, the sessions, the cap and the budget they need. A smaller matrix lowers the budget it needs by its sessions, and a lower `--session-budget-usd` by the cap: a Haiku session over one workflow records about USD 0.003, so `--session-budget-usd 0.05` covers it with room to spare. The agent checks its session cap between calls, so a session can record more than its cap; a run stops starting sessions before its recorded cost, with the caps of the sessions in flight reserved, would pass the budget, and lists those it did not start.

## Reading the report

A run writes its records under `results/<run-id>/`, which git ignores: per session, `<model>/<workflow>/<scenario>/<form>/<repetition>/` with its transcript, trace, actions and `session.json`; and `run.json`, the run's options, cost and sessions not started. The runner then writes `report.md` and `report.json` beside `run.json`. To write them again, against another baseline:

```bash
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --baseline <file>
```

The [report](report.py) gives three tables: per model, per model and form across scenarios, and per model, form and scenario. Each row gives its sessions and passes, the pass rate, each failure class's count, the sessions ended at their timeout, the mean tokens (input, output, cache write and cache read) and the mean cost over the sessions recording them. The report opens with the run's cost and the count of sessions not started, and closes with those sessions listed.

`baseline.json` beside this file is the baseline, a reviewed default run's cells: each one's sessions, passes, pass rate and failure counts, with that run's id, date, models, repetitions and cost. [`report.md`](report.md) beside it is that run's report. With a baseline present, each row's Change is its pass rate less the baseline row's, in percentage points, and each failure count is followed by its change in brackets when it moved. A row the baseline lacks reads `new`, and the rows the baseline holds that the run lacks are listed under Baseline Only. With no baseline, Change reads `—`.

## Refreshing the baseline

Run the default matrix, review its report, then write its cells as the baseline and commit `baseline.json` with the run's `report.md` beside it:

```bash
make eval-diagrams
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --write-baseline
cp evals/diagram-following/results/<run-id>/report.md evals/diagram-following/report.md
```

The report written alongside is compared with the baseline being replaced, so it shows what the new baseline moves.
