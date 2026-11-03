# Diagram-Following Eval

How well an agent, given a workflow drawn as a Mermaid diagram whose nodes link the sections saying what to do in each state, follows that workflow to completion. The eval gives each workflow to headless agent sessions, scores the path each session took, and compares the pass rates with a committed baseline.

## Forms

Each workflow in [`workflows/`](workflows) is written in the forms [`workflow.py`](workflow.py) describes: a diagram, a prose form whose transitions are sentences, a linked form whose decisions name a document stating the state the branch enters, the two dispatch forms a workflow dispatching a target is written in, a skill handing over a workflow's sources to compile, and a staged form handing over a compiled bundle set beside its sources and the build. A session receives one of the forms below; every form but `bootstrap` and `staged` is entered at `workflow.md`:

| Form | Material | What it isolates |
| --- | --- | --- |
| `bundle` | The diagram form bundled by `pf` into one file. | The product under test. |
| `tree` | The diagram form's source tree, unbundled. | Against `bundle`, what bundling adds. |
| `prose` | The prose form bundled by `pf` into one file. | Against `bundle`, what the diagram adds. |
| `linked` | The linked form's source tree, unbundled. | Whether a decision is resolved by following its link. |
| `compiled` | The compiled form's bundle set: the entry's bundle, every dispatched target's beside it, and the Prosiform section `pf` emits around each. | Whether an agent follows the dispatch protocol `pf` compiles. |
| `authored` | The authored-protocol form's one bundle, whose state documents write the same protocol as prose. | Against `compiled`, what compilation adds. |
| `bootstrap` | A skill placed where the agent CLI discovers skills, naming the workflow's sources, written as the compiled form is, for the session to compile with `pf`. | Whether an agent compiles a workflow it is handed as sources before following it. |
| `staged` | The staged form's sources, written as the compiled form is, with the entry's bundle set in the folder `pf` writes it to and the build under test as `pf` on the session's path. | Whether an agent compiles, as it follows a bundle, the material the bundle defers. |

A workflow gives a session only the forms it is written in: the three workflows walking a decision to a terminal state take `bundle`, `tree`, `prose` and `linked`, the four dispatch scenarios take `compiled` and `authored`, `dispatch-set` takes `staged` beside them, the two [deferral workflows](#deferral-scenarios) take `staged` alone, the two [bootstrap workflows](#bootstrap-scenarios) take `bootstrap` alone, and the six workflows built on a feature, `preset-selection`, `group-placement`, `subst-redirect`, `section-entry`, `section-composition` and `declared-inclusion`, take `bundle` and `tree`.

The linked form's entry draws the diagram's flowchart with no branch label, and its decisions name no branch of their own. Each names a rule document, by a name that gives nothing away, stating the one state its branch enters, so the edge a branch takes is recoverable only by opening the document the section links, and the state it states is held to the edges the diagram draws out of the deciding state. Its rule document's destination resolves from the section that writes it, under `states/`.

Each form's entry is held to what it may carry: a prose entry draws no diagram, and a linked entry draws the diagram's edges and no label on any of them.

Every session is given the same [instruction](instruction.md), naming only the entry document; a `bootstrap` session takes [its own](instruction-bootstrap.md), telling it a skill is available to find, and a `staged` session [its own](instruction-staged.md), naming the entry's bundle and telling it `pf` with no arguments prints how a bundle names material to compile. Each `[[scenario]]` table in a workflow's `scenarios.toml` declares one scenario:

| Field | Meaning |
| --- | --- |
| `name` | The scenario's name, which the run's records and report carry. |
| `inputs` | Each input file a session finds under `inputs/`, by file name and value. A run writes the value followed by a newline, and a condition reads it with surrounding whitespace removed. |
| `path` | The states a correct session enters, in order, held to the edges the diagram draws and to the walk the diagram form's bundle states. |
| `trace` | Optional. The sub-agent starts a correct run makes, as [Dispatch scenarios](#dispatch-scenarios) states. A scenario declaring none dispatches nothing. |
| `compile` | Optional. The `pf` runs a correct run makes, as [Stated runs](#stated-runs) states. A scenario declaring none runs no `pf`. |

A top-level `entry` key names the reference every form of the workflow is compiled from, `workflow.md` when absent. `section-entry` names `workflow.md#onboarding`, so its bundle carries that section's workflow and none of the document's other sections, and its session still receives the bundle as `workflow.md`.

A `scenarios.toml` may also declare, above its tables, `warnings`: the warning codes `pf` reports bundling the workflow. A feature such as `subst` warns wherever it is used, so a workflow built on one declares each code it raises, and its bundle is held to raising those and no other diagnostic.

Every workflow document declares `prosiform` save those under an `undeclared/` directory, which declare nothing, so a link to one is left as written; `declared-inclusion` links one beside a declared state document `pf` follows. A skill's `SKILL.md` is the entry the agent CLI reads rather than a source `pf` compiles, so it may declare nothing too.

A diagram form's bundle states a path of its own, and a scenario's path is held to it beside the sources' walk. Each state is entered at the heading the previous state's link names, or else the one the bundle's diagram clicks, and its action and transition are read from what that heading holds. A state `pf` placed into a group or reached through a `subst` pair is followed where the bundle puts it, and the bundle must state the action the sources state, since the scorer reads the sources'. A feature workflow's substitutes therefore state the action and transition of the state they stand in for, so the `tree` form walks the same path the `bundle` form does.

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

### Stated runs

A scenario names each `pf` run a correct session and each of its sub-agents makes: one `[[scenario.compile]]` table per run, in the order the walk makes them.

| Field | Meaning |
| --- | --- |
| `by` | Optional. The section of the scenario's trace whose sub-agent makes the run, as `<document>#<heading>`; absent for the session's own run. |
| `args` | Optional. Each reference the run compiles, as `<document>` or `<document>#<fragment>`; empty, or absent, for bare `pf`, which prints the guide. An option such as `-o` is the agent's to choose, so a run states none. |

A reference resolves from the directory a shell form runs `pf` in: the skill's directory for `bootstrap`, as the guide states, and the workspace for `staged`, which holds the staged form's sources as they stand. The corpus test refuses a reference naming no document there, a `by` naming no section of the trace, and a run stated by a workflow written in no shell form.

A `staged` session reads the bundle set `pf` compiled from the staged form, so a `↳` line the bundle carries names its target from the workspace, and compiling it there is the run the scenario states where a step its path takes reaches the line, as [Deferral scenarios](#deferral-scenarios) states. `dispatch-set` is written in the form with nothing to compile, so its scenario states no run.

A stated run a sub-agent makes is read from that sub-agent's own commands, which a harness reports only where it carries a shell and its stream carries a sub-agent's own calls. A harness reporting no sub-agent's commands is given no scenario stating a sub-agent's run, as it is given no scenario whose trace outruns the starts it reports.

### Bootstrap scenarios

The two bootstrap workflows say whether an agent handed a skill, rather than an entry document, compiles the workflow the skill names before following it. A session finds the skill under `.claude/skills/<workflow>/` in its workspace, where the agent CLI discovers skills. The skill's `SKILL.md` says to run `pf`, then holds one hand-written `[↳ <title>](<path>)` line, titled as the document it names is headed, so the guide bare `pf` prints says to compile that document, read it whole and follow it, and the bundle that run writes is the document stating the workflow. The run puts the build under test on the session's path, so the `pf` a session compiles with is the one the run was configured with.

Compiling runs a command, so only a harness carrying a shell gives a session in this form or in `staged`: `cursor` and `opencode` do, and `claude`, whose tool list names no shell, is given no `bootstrap` or `staged` session. Each scenario states bare `pf`, then `pf` on the line's path, and its path is the walk of the bundle that run writes, as the corpus test compiles it from the skill's directory. `bootstrap-audit`'s sources dispatch sub-agents, so each of its scenarios names the trace a correct run produces as a dispatch scenario does, and a harness that reports no sub-agent's own dispatch is given only the scenarios whose trace it can observe. `inline-bootstrap`'s `SKILL.md` declares no `prosiform`, so its line is held as written, and its sources dispatch nothing.

| Workflow | Scenario | What it walks |
| --- | --- | --- |
| `bootstrap-audit` | `blocking-two-halves` | Source and tests gathered as a set, the appraisal, a blocking verdict, then the repair. |
| `bootstrap-audit` | `clean-one-half` | Source and tests gathered as a set, the appraisal, then a clean verdict straight to publishing. |
| `inline-bootstrap` | `feature-tagged` | The freeze, a feature tagged, then the broadcast. |
| `inline-bootstrap` | `fix-backported` | The freeze, a fix backported, then the broadcast. |

### Deferral scenarios

The two deferral workflows say whether an agent following a `staged` bundle runs `pf` on each `↳` line its path needs, and on no other. A source writes a deferred directive, `[¬→](<path>#<section>)`, and `pf` publishes it as a `↳` line naming that section, beneath the step writing it. A step opening with a condition, "If `inputs/<file>` reads `<value>`,", reaches its lines only where that condition holds, and a run's bundle may hold further lines its own steps reach. The corpus test walks the bundles as a session does: it compiles the entry's bundle, runs `pf` from the staged sources on each line a step of the walk reaches, reads what each run writes as part of the state that reached it, and holds the scenario's runs and path to that walk.

A state may also defer its transition: its document writes no `**Next.**` paragraph, and the material its deferral compiles states "Take the transition labelled `<label>`.", so only a session that ran `pf` on the line knows the edge to take.

| Workflow | Scenario | What it runs |
| --- | --- | --- |
| `deferred-composition` | `deferral-reached` | `pf` on the migration's line, which Relocate's step reaches where `scope.txt` reads `large`. |
| `deferred-composition` | `deferral-passed` | Nothing: Relocate's step does not hold, so its line is passed. |
| `deferred-composition` | `nested-needed` | The migration's line, then the archive's line its bundle holds, whose step holds where `history.txt` reads `kept`. |
| `deferred-composition` | `nested-unreached` | Nothing: the archive's step holds, but the migration's bundle that carries it is never compiled. |
| `preset-deferral` | `stand-in-followed` | `pf` on `reference/fetch.md#read-mirror`. `Mirror` and `Read mirror` both select `fetch.md`'s `mirror` preset, whose `subst` puts the stored copy in place of the live page, so the transition the stand-in states sends the path to `Restore`, where the live page's would send it to `Serve`. |

## Scoring

A session records each state it enters as a line of `trace.log` and does each state's action by writing a file under `actions/`. Every instruction tells it to hand each sub-agent it dispatches the name `trace-<section>.log`, since a sub-agent reads only the prompt its session writes, and the run keeps each such trace beside the session's own. The [scorer](score.py) passes a session whose trace is its scenario's path with every state's action done. A failing session takes the first of these classes that fits where its trace departs from the path:

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

A dispatch scenario states the sub-agents a correct run starts, so a run whose trace is the path and whose actions are done is held to its sub-agent record before it passes. The record is [`subagents.json`](score.py), written from the session's transcript as it settles and sitting beside the trace and the session's cost, so the scorer reads it rather than the transcript. It holds the session's own shell `commands`, null where its harness gives it no shell, and its `starts`. Each start names the section a sub-agent followed, what it returned, whether it started beside the entry above it, `parent`, the index of the start whose sub-agent made it, null for the session's own, and `commands`, the shell commands its sub-agent ran, so each sub-agent's starts and commands sit under the section it followed at every depth the harness's stream reports.

| Class | The session |
| --- | --- |
| `undispatched` | left a bundle the scenario dispatches without a sub-agent, or started them in another order. |
| `sequential_set` | started a set's bundles across more than one message, rather than its opener first and every later member alongside it in that message. |
| `unrelayed_question` | answered a sub-agent's returned question in its own place, returning `done` where the scenario states `question`. |

The three are read in that order, after the run is held to its path and its actions, so a trace that stopped short is `unfinished` however few sub-agents it started, and a record failing two checks takes the earlier. A scenario that dispatches nothing passes all three.

### Run checks

A run that passes the dispatch checks is held to the `pf` runs its scenario states, wherever its harness reports the commands a session ran. A run is a command, split at `;`, `&&`, `||` and `|`, whose first word is `pf` or a path ending `/pf`; its references are its words other than options and their values, and one names a stated reference when it is that reference or ends `/` and that reference. The session's runs, and each sub-agent's from the commands of the starts naming its section, are held to those stated for it:

| Class | The session |
| --- | --- |
| `uncompiled` | or a sub-agent left a stated run unmade. |
| `overcompiled` | or a sub-agent made a run naming a reference no stated run names, as one on a deferred line its path did not reach does. A bare `pf` beyond those stated prints the guide and compiles nothing, so it is no departure. |
| `misordered_compile` | or a sub-agent made its stated runs in another order. |

The three are read in that order, after the dispatch checks, so a sub-agent that never started is `undispatched` rather than leaving its runs unmade. A harness reporting no command, as the Claude harness's shell-less sessions do, holds a session to none of them.

A run in which every session it started took `errored` is **refused**. No session entered a state, so the matrix is no result, and its pass rates would read a spent login as a matrix of failing agents. `run.json` records `"state": "refused"` and a `reason`, and its report names both instead of giving tables or comparing pass rates. The reason is one session's own `result` text, so a reader sees the limit the agent reported. A run its budget stopped part way is refused on the same terms, since the sessions it never started add nothing its errored ones lack; one where some sessions errored on a genuine fault beside sessions that entered a state is a completed run whose failures are its result. The boundary is decided once the sessions settle, before `run.json` is written.

## Login

Sessions run on an agent CLI the run names, `--harness claude`, `--harness cursor` or `--harness opencode`, and each harness states what confines its sessions. The Claude harness runs on the eval's own login, kept apart from yours in `<eval-root>/config`, where the eval root defaults to `~/projects/eval/prosiform`. Log in once:

```bash
CLAUDE_CONFIG_DIR=~/projects/eval/prosiform/config claude
```

then `/login`.

## Isolation

A session receives one form of one workflow and the instruction, so a pass measures the agent reading that form. Each mechanism below holds one part of that boundary for the Claude harness; the first two are refused before a session starts, and the last is read back from each session's own transcript.

| Mechanism | What it keeps out |
| --- | --- |
| `CLAUDE_CONFIG_DIR` names the eval's config directory | The caller's own configuration, memory and settings, which no session reads. Every `CLAUDE*` and `ANTHROPIC_*` variable the caller holds is dropped from the session's environment, and `CLAUDE_CONFIG_DIR` is the only one set. |
| `--strict-mcp-config` | Every MCP server, since the session is given no server list. |
| `--disable-slash-commands` | Every slash command and skill the configuration directory would offer. |
| `--tools Read,Write,Edit,Glob,Grep,Task` | Every other tool, `Bash` included, so a session cannot reach past its workspace, and `Task` is the one tool a dispatch protocol needs. |
| `--permission-mode acceptEdits` | Writes outside the session's fresh workspace. |
| `--no-session-persistence` | A transcript surviving the run beyond the record the eval keeps. |
| The injected-context read | Context the agent added that the run did not supply. |

Neither flag suppresses a plugin's hooks or a settings file's, so the preflight refuses a run whose settings would let one reach a session. It fails before the first session starts, naming the file to remove. Each file below is read from the scope shown, and a file holding only preferences is no refusal. Files in the eval's config directory are read under the user scope:

- `plugins/installed_plugins.json` holding an installed plugin, whose `hooks/hooks.json` may declare a `SessionStart` hook;
- `remote-settings.json` enabling a plugin in `enabledPlugins`, whose `env` the agent applies over the scrubbed environment, as the eval's own directory did with telemetry and an OTLP endpoint;
- `settings.json` declaring a hook for any event in its `hooks` block, which delivers that command to a session with no plugin installed at all. The refusal names each event the block declares, so the directory keeps its theme and model.

Files in a project's `.claude` directory are read under the project scope, `settings.local.json` being its untracked local variant. A file of either name declaring a hook for any event is refused, naming each event, from two places:

- a workflow's form tree, the source a session's workspace is copied from, so the file reaches every session of that tree; remove the file from the tree;
- the `.claude` directory of every ancestor of the workspaces, the workspace root `<eval-root>/workspaces` included, since Claude Code reads project settings from each directory on the path from a session's working directory to the filesystem root. Remove the file, or pass an `--eval-root` outside that ancestor, which moves the workspaces from under it.

A run whose config directory holds no login fails the same way, naming the one-time login command.

The host's managed settings file, `/etc/claude-code/managed-settings.json` on Linux, belongs to the host's administrator and reaches every session wherever the config directory points. The run records it rather than refusing it: when its `hooks` block declares a hook, `run.json` names the file and each event under `managed.hooks`, so every recorded session reads as carrying that hook. A host with no such file, or one declaring no hook, records none, and the sessions start either way.

A session that still carries context the run did not supply fails the run after its sessions finish, naming each one and what it carried. The context read is what makes the boundary observable rather than assumed: a plugin hook's `additionalContext`, an appended system prompt, or a memory file is another instruction set beside the form, and a session carrying one is no evidence of how the agent followed the form. Where a managed hook is recorded, a hook's response is that hook's, since the preflight admits no other. The run raises before it writes `run.json`, so a refused run is never reported as a completed one.

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
| `--forms` | `bundle,tree,prose,linked,compiled,authored,bootstrap` | The forms, comma-separated. A workflow gives sessions only in the forms it is written in, and a harness only in the forms it can run. `staged` is given only where named. |
| `--repetitions` | 5 | Sessions per model, form and scenario. |
| `--parallel` | 4 | Sessions running at once. |
| `--eval-root` | `~/projects/eval/prosiform` | The directory holding the login and the workspaces. |
| `--harness` | `claude` | The agent CLI the run drives: `claude`, `cursor` or `opencode`. |
| `--agent-command` | the harness's own command | The agent's command line, overriding the harness. |
| `--results` | `results/` beside this file | Where runs are recorded. |
| `--run-id` | the start time, as `YYYYMMDDTHHMMSSZ` | The run's directory name. |

For example, one model over one workflow:

```bash
make eval-diagrams ARGS='--models claude-haiku-5-5 --workflows linear --repetitions 1 --budget-tokens 100000 --session-budget-tokens 20000'
```

### Default matrix and budget

The default matrix is two models, `claude-haiku-5-5` and `claude-sonnet-5-5`; the twenty-four scenarios of the thirteen workflows the Claude harness can run, in the forms each is written in, 58 cells in all; and five repetitions: 580 sessions. The `bootstrap` form adds none, since the Claude harness carries no shell. The committed baseline records an earlier matrix of three forms — the diagram bundle, its source tree and the prose bundle — and predates the token budget, so its cells carry no token count; a run over four forms records the linked form's sessions on top.

A run is held to tokens, the one measure every harness reports, and `--budget-tokens` must cover the sessions times `--session-budget-tokens` or it is refused before a session starts, naming the budget, the sessions, the cap and the budget they need. The default matrix's 580 sessions at the 60 000-token session cap need 34 800 000, which `EVAL_BUDGET_TOKENS` covers; a smaller matrix lowers the need by its sessions and a lower `--session-budget-tokens` by the cap.

The Claude harness also passes `--max-budget-usd` to its CLI, which caps dollars between calls and reports no token ceiling. That figure is the harness's own `session_cap_usd`, USD 0.50, not the token cap, so it bounds what one session can spend before the run's guard sees a result. The Cursor and opencode CLIs accept neither a spend cap nor a token cap, so a run on either is bounded by its timeout and by the run's guard alone.

The run's guard reads each session's reported tokens when it settles: a session starts only when the recorded tokens, plus the cap reserved for each session in flight, plus its own cap, fit the budget, and a run that cannot fit another lists the rest as not started. A session can record more than its cap, since its own CLI checks between calls, and the guard holds the budget against that by reserving caps in flight.

## Reading the report

A run writes its records under `results/<run-id>/`, which git ignores: per session, `<model>/<workflow>/<scenario>/<form>/<repetition>/` with its transcript, its own `trace.log`, each dispatched sub-agent's `trace-<section>.log`, actions, sub-agent record and `session.json`; and `run.json`, the run's options, harness, managed hooks, tokens, state and sessions not started. `subagents.json` holds the session's commands and the sub-agent starts the transcript records, one per entry, in order, each with its parent and its commands, so a reader sees what the agent dispatched and ran; `session.json` also holds the scenario's dispatch trace, so a reader sees the sub-agents a correct run starts beside the verdict on the one that ran. The runner then writes `report.md` and `report.json` beside `run.json`. To write them again, against another baseline:

```bash
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --baseline <file>
```

The [report](report.py) gives three tables: per model, per model and form across scenarios, and per model, form and scenario. Each row gives its sessions and passes, the pass rate, each failure class's count, the sessions ended at their timeout, the mean tokens and the mean cost where a harness reports one. The report opens with the run's tokens and the count of sessions not started, and closes with those sessions listed.

A refused run — one every started session of which took `errored` — has no row and no comparison. Its report gives the run's `refused` state and the reason `run.json` records, the reason being one session's own `result` text, so a reader sees the limit the agent reported rather than a pass rate. `--write-baseline` writes only from a run whose report holds a cell, so a refused run, or one that started nothing, leaves the committed baseline as it was.

`baseline.json` beside this file is the baseline, a reviewed default run's cells: each one's sessions, passes, pass rate and failure counts, with that run's id, date, models, repetitions and cost. [`report.md`](report.md) beside it is that run's report. With a baseline present, each row's Change is its pass rate less the baseline row's, in percentage points, and each failure count is followed by its change in brackets when it moved. A row the baseline lacks reads `new`, and the rows the baseline holds that the run lacks are listed under Baseline Only. With no baseline, Change reads `—`.

## Refreshing the baseline

Run the default matrix, review its report, then write its cells as the baseline and commit `baseline.json` with the run's `report.md` beside it:

```bash
make eval-diagrams
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --write-baseline
cp evals/diagram-following/results/<run-id>/report.md evals/diagram-following/report.md
```

The report written alongside is compared with the baseline being replaced, so it shows what the new baseline moves.
