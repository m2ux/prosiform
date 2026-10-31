# Diagram-Following Eval

How well an agent, given a workflow drawn as a Mermaid diagram whose nodes link the sections saying what to do in each state, follows that workflow to completion. The eval gives each workflow to headless agent sessions, scores the path each session took, and compares the pass rates with a committed baseline.

## Forms

Each workflow in [`workflows/`](workflows) is written in the forms [`workflow.py`](workflow.py) describes: a diagram, a prose form whose transitions are sentences, a linked form whose decisions name a document stating the branch's label, and the two dispatch forms a workflow dispatching a target is written in. A session receives one of six forms, always entered at `workflow.md`:

| Form | Material | What it isolates |
| --- | --- | --- |
| `bundle` | The diagram form bundled by `pf` into one file. | The product under test. |
| `tree` | The diagram form's source tree, unbundled. | Against `bundle`, what bundling adds. |
| `prose` | The prose form bundled by `pf` into one file. | Against `bundle`, what the diagram adds. |
| `linked` | The linked form's source tree, unbundled. | Whether a decision is resolved by following its link. |
| `compiled` | The compiled form's bundle set: the entry's bundle, every dispatched target's beside it, and the Prosiform section `pf` emits around each. | Whether an agent follows the dispatch protocol `pf` compiles. |
| `authored` | The authored-protocol form's one bundle, whose state documents write the same protocol as prose. | Against `compiled`, what compilation adds. |

A workflow gives a session only the forms it is written in: the three workflows walking a decision to a terminal state take `bundle`, `tree`, `prose` and `linked`, and the four dispatch scenarios take `compiled` and `authored`.

The linked form's decisions carry no label of their own. Each names a rule document that states one label, so the edge a branch takes is recoverable only by opening the document the section links, and the label it states is held to the edges the diagram draws. Its rule document's destination resolves from the section that writes it, under `states/`.

Every session is given the same [instruction](instruction.md), naming only the entry document. Each scenario in a workflow's `scenarios.toml` names the inputs a session finds under `inputs/` and the path a correct session walks.

A diagram form's `click` lines carry destinations relative to the document that writes them, so a node opens its section for a reader of the source tree and for a session in its workspace. GitHub draws a Mermaid fence in a frame of its own and resolves such a destination against that frame, so a diagram form's clicks open nothing in the blob view; the state documents sit beside the entry document all the same.

### Dispatch scenarios

The four dispatch scenarios say what a bundled workflow's dispatch protocol is for: whether an agent hands a dispatched section to a sub-agent at all, starts a set's targets together, and puts a sub-agent's question to the user rather than answering it.

| Workflow | Scenario | What it dispatches |
| --- | --- | --- |
| `dispatch-chain` | `chain` | A section whose own step dispatches a second, so a run starts two sub-agents in order. |
| `dispatch-set` | `parallel-set` | Two sections at once, so a run starts two sub-agents together. |
| `dispatch-beside` | `set-beside-a-dispatch` | One section, then two more as a set of their own. |
| `dispatch-question` | `returned-question` | A section returning a question, put to the user, then dispatched again with the answers. |

A dispatch scenario's `scenarios.toml` names the trace a correct run produces beside the path it walks: one `[[scenario.trace]]` table per sub-agent start, in the order the walk dispatches it.

| Field | Meaning |
| --- | --- |
| `dispatch` | The section the sub-agent follows, as `<document>#<heading>`. Both forms name a section, so one trace is the trace of both. |
| `returned` | What the sub-agent gave back: `done`, or `question` for one it returned unanswered. |
| `together` | Whether it started beside the entry above it, which marks every member of a set but the one opening it. |

The trace is held to the source: [`dispatch_walk()`](workflow.py) walks each state's steps in path order, following a dispatched section's own steps, and the test asserts the corpus states that walk and no other. The compiled form writes a step's targets with `⇉`, and a set's with `⫽`, so `pf` compiles each target into a bundle of its own, and its step is its marks alone: the operator states the dispatch and the `Dispatch` protocol `pf` publishes from it states what to do, so a sentence beside the marks would state the dispatch a second time and is a fault. The authored form writes the same steps as ordinary links to the same sections and the protocol as prose, so it publishes the entry's bundle alone and its prose is its only statement of the dispatch. The two forms therefore hold one statement of the dispatch each, and a pass rate's difference between them is what compilation adds.

## Scoring

A session records each state it enters as a line of `trace.log` and does each state's action by writing a file under `actions/`. The [scorer](score.py) passes a session whose trace is its scenario's path with every state's action done. A failing session takes the first of seven classes that fits where its trace departs from the path:

| Class | The session |
| --- | --- |
| `missing_action` | walked the path and left a state's action undone or wrong. |
| `unfinished` | stopped partway along the path. |
| `invented_state` | entered a state the diagram does not hold. |
| `loop_miscount` | repeated a loop more times than its input requires. |
| `wrong_branch` | took the other branch of a decision on an input. |
| `skipped_state` | jumped ahead, omitting states between. |
| `invalid_transition` | entered a state no edge leads to: a step back, a state after the end, or the same state again. |

A session whose agent reports an error, or prints no `result` message, takes `errored` instead of any of these. It entered no state, so its trace says nothing about how it followed the workflow: a refusal, an expired quota or a crashed command fails `errored` rather than as an `unfinished` run.

### Dispatch checks

A dispatch scenario states the sub-agents a correct run starts, so a run whose trace is the path and whose actions are done is held to its sub-agent record before it passes. The record is [`subagents.json`](score.py), written from the session's transcript as it settles and sitting beside the trace and the session's cost, so the scorer reads it rather than the transcript. Each entry names the section a sub-agent followed, what it returned and whether it started beside the entry above it.

| Class | The session |
| --- | --- |
| `undispatched` | left a bundle the scenario dispatches without a sub-agent, or started them in another order. |
| `sequential_set` | started a set's bundles one after another rather than together. |
| `unrelayed_question` | answered a sub-agent's returned question in its own place, returning `done` where the scenario states `question`. |

The three are read in that order, after the run is held to its path and its actions, so a trace that stopped short is `unfinished` however few sub-agents it started, and a record failing two checks takes the earlier. A scenario that dispatches nothing passes all three.

A run in which every session took `errored` is **refused**. No session entered a state, so the matrix is no result, and its pass rates would read a spent login as a matrix of failing agents. `run.json` records `"state": "refused"` and a `reason`, and its report names both instead of giving tables or comparing pass rates. The reason is one session's own `result` text, so a reader sees the limit the agent reported. Only a run that started its whole matrix and errored in every session is refused: a run its budget stopped part way is unfinished, and one where some sessions errored on a genuine fault beside sessions that entered a state is a completed run whose failures are its result. The boundary is decided once the sessions settle, before `run.json` is written.

## Login

Sessions run on an agent CLI the run names, `--harness claude` or `--harness cursor`, and each harness states what confines its sessions. The Claude harness runs on the eval's own login, kept apart from yours in `<eval-root>/config`, where the eval root defaults to `~/projects/eval/prosiform`. Log in once:

```bash
CLAUDE_CONFIG_DIR=~/projects/eval/prosiform/config claude
```

then `/login`.

## Isolation

A session receives one form of one workflow and the instruction, so a pass measures the agent reading that form. Each mechanism below holds one part of that boundary; the first two are refused before a session starts, and the last is read back from each session's own transcript.

| Mechanism | What it keeps out |
| --- | --- |
| `CLAUDE_CONFIG_DIR` names the eval's config directory | The caller's own configuration, memory and settings, which no session reads. Every `CLAUDE*` and `ANTHROPIC_*` variable the caller holds is dropped from the session's environment, and `CLAUDE_CONFIG_DIR` is the only one set. |
| `--strict-mcp-config` | Every MCP server, since the session is given no server list. |
| `--disable-slash-commands` | Every slash command and skill the configuration directory would offer. |
| `--tools Read,Write,Edit,Glob,Grep,Task` | Every other tool, `Bash` included, so a session cannot reach past its workspace, and `Task` is the one tool a dispatch protocol needs. |
| `--permission-mode acceptEdits` | Writes outside the session's fresh workspace. |
| `--no-session-persistence` | A transcript surviving the run beyond the record the eval keeps. |
| The injected-context read | Context the agent added that the run did not supply. |

Neither flag suppresses a plugin's hooks, so the preflight refuses a run whose config directory would let one reach a session. It fails before the first session starts, naming the file to remove:

- `plugins/installed_plugins.json` holding an installed plugin, whose `hooks/hooks.json` may declare a `SessionStart` hook;
- `remote-settings.json` enabling a plugin in `enabledPlugins`, whose `env` the agent applies over the scrubbed environment, as the eval's own directory did with telemetry and an OTLP endpoint;
- `settings.json` declaring a hook for any event in its `hooks` block, which delivers that command to a session with no plugin installed at all. The refusal names each event the block declares, and a settings file holding only preferences is no refusal, so the directory keeps its theme and model.

A run whose config directory holds no login fails the same way, naming the one-time login command.

A session that still carries context the run did not supply fails the run after its sessions finish, naming each one and what it carried. The context read is what makes the boundary observable rather than assumed: a plugin hook's `additionalContext`, an appended system prompt, or a memory file is another instruction set beside the form, and a session carrying one is no evidence of how the agent followed the form. The run raises before it writes `run.json`, so a refused run is never reported as a completed one.

## Running

| Command | Runs |
| --- | --- |
| `make eval-diagrams` | The [runner](run.py) over the default matrix, then the report. Its token budget is `EVAL_BUDGET_TOKENS` and its harness `HARNESS`; `ARGS='...'` passes the runner's options through, a later `--budget-tokens` among them overriding the default. |

The command starts paid agent sessions, so no other target depends on it and `make check` never runs it; `make harness` holds the runner, scorer and report against a stub agent and recorded results instead. The runner's options, each passed through `ARGS`:

| Option | Default | Meaning |
| --- | --- | --- |
| `--budget-tokens` | required | The run's token cap, at least the sessions times `--session-budget-tokens`. A later value in `ARGS` overrides the default. |
| `--session-budget-tokens` | 60 000 | Each session's token cap. |
| `--session-timeout-seconds` | 600 | How long a session runs before it is ended and scored as it stands. |
| `--models` | `claude-haiku-5-5,claude-sonnet-5-5` | The models, comma-separated. |
| `--workflows` | every workflow | The workflows, comma-separated. |
| `--forms` | `bundle,tree,prose,linked,compiled,authored` | The forms, comma-separated. A workflow gives sessions only in the forms it is written in. |
| `--repetitions` | 5 | Sessions per model, form and scenario. |
| `--parallel` | 4 | Sessions running at once. |
| `--eval-root` | `~/projects/eval/prosiform` | The directory holding the login and the workspaces. |
| `--harness` | `claude` | The agent CLI the run drives: `claude` or `cursor`. |
| `--agent-command` | the harness's own command | The agent's command line, overriding the harness. |
| `--results` | `results/` beside this file | Where runs are recorded. |
| `--run-id` | the start time, as `YYYYMMDDTHHMMSSZ` | The run's directory name. |

For example, one model over one workflow:

```bash
make eval-diagrams ARGS='--models claude-haiku-5-5 --workflows linear --repetitions 1 --budget-tokens 100000 --session-budget-tokens 20000'
```

### Default matrix and budget

The default matrix is two models, `claude-haiku-5-5` and `claude-sonnet-5-5`; the six scenarios of the seven workflows, in the forms each is written in; and five repetitions: 280 sessions. The committed baseline records an earlier matrix of three forms — the diagram bundle, its source tree and the prose bundle — and predates the token budget, so its cells carry no token count; a run over four forms records the linked form's sessions on top.

A run is held to tokens, the one measure both harnesses report, and `--budget-tokens` must cover the sessions times `--session-budget-tokens` or it is refused before a session starts, naming the budget, the sessions, the cap and the budget they need. The default matrix's 280 sessions at the 60 000-token session cap need 16 800 000, which `EVAL_BUDGET_TOKENS` covers; a smaller matrix lowers the need by its sessions and a lower `--session-budget-tokens` by the cap.

The Claude harness also passes `--max-budget-usd` to its CLI, which caps dollars between calls and reports no token ceiling. That figure is the harness's own `session_cap_usd`, USD 0.50, not the token cap, so it bounds what one session can spend before the run's guard sees a result. The Cursor CLI accepts neither a spend cap nor a token cap, so a Cursor run is bounded by its timeout and by the run's guard alone.

The run's guard reads each session's reported tokens when it settles: a session starts only when the recorded tokens, plus the cap reserved for each session in flight, plus its own cap, fit the budget, and a run that cannot fit another lists the rest as not started. A session can record more than its cap, since its own CLI checks between calls, and the guard holds the budget against that by reserving caps in flight.

## Reading the report

A run writes its records under `results/<run-id>/`, which git ignores: per session, `<model>/<workflow>/<scenario>/<form>/<repetition>/` with its transcript, its own `trace.log`, each dispatched sub-agent's `trace-<section>.log`, actions, sub-agent record and `session.json`; and `run.json`, the run's options, harness, tokens, state and sessions not started. `subagents.json` holds the sub-agent starts the transcript records, one per entry, in order, so a reader sees what the agent dispatched; `session.json` also holds the scenario's dispatch trace, so a reader sees the sub-agents a correct run starts beside the verdict on the one that ran. The runner then writes `report.md` and `report.json` beside `run.json`. To write them again, against another baseline:

```bash
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --baseline <file>
```

The [report](report.py) gives three tables: per model, per model and form across scenarios, and per model, form and scenario. Each row gives its sessions and passes, the pass rate, each failure class's count, the sessions ended at their timeout, the mean tokens and the mean cost where a harness reports one. The report opens with the run's tokens and the count of sessions not started, and closes with those sessions listed.

A refused run — one every session of which took `errored` — has no row and no comparison. Its report gives the run's `refused` state and the reason `run.json` records, the reason being one session's own `result` text, so a reader sees the limit the agent reported rather than a pass rate. `--write-baseline` refuses a refused run, since it has no cells to write.

`baseline.json` beside this file is the baseline, a reviewed default run's cells: each one's sessions, passes, pass rate and failure counts, with that run's id, date, models, repetitions and cost. [`report.md`](report.md) beside it is that run's report. With a baseline present, each row's Change is its pass rate less the baseline row's, in percentage points, and each failure count is followed by its change in brackets when it moved. A row the baseline lacks reads `new`, and the rows the baseline holds that the run lacks are listed under Baseline Only. With no baseline, Change reads `—`.

## Refreshing the baseline

Run the default matrix, review its report, then write its cells as the baseline and commit `baseline.json` with the run's `report.md` beside it:

```bash
make eval-diagrams
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --write-baseline
cp evals/diagram-following/results/<run-id>/report.md evals/diagram-following/report.md
```

The report written alongside is compared with the baseline being replaced, so it shows what the new baseline moves.
