# Diagram-Following Runbook

How each live run of the [diagram-following eval](README.md) is carried out, and how its failing sessions are triaged. A run follows its runbook below to the letter: its arguments, budget, stop rules and committed files are settled here, so the run makes no design judgement of its own. Every argument is an option of the [runner](run.py), whose meanings and defaults the README's [Running](README.md#running) section states.

## Triage Rubric

Every failing session a run records takes one disposition from this rubric before anything is committed.

| Disposition | Meaning | Action |
| --- | --- | --- |
| `miss` | The session had what it needed and did otherwise: its form states the path's walk, its inputs hold the scenario's values, and its records are what its transcript did. | Recorded with its evidence; the run continues. |
| `defect` | Something other than the agent departs: the form, the scenario, the instruction, the harness's reading of the stream, the runner's plumbing or the login. | The run stops, commits nothing, and escalates. |
| `unclear` | The evidence supports neither reading. | The run stops, commits nothing, and escalates, naming what would decide it. |

A run never edits a scenario, a workflow form, the instruction, the harness, the runner or the scorer, never re-runs one session to replace its result, and never removes a session's records. An escalation is an issue naming the session, its class, the evidence and the disposition; the run is repeated from the start once the fix it asks for lands.

### Evidence

A session's records sit at `results/<run-id>/<model>/<workflow>/<scenario>/<form>/<repetition>/`, as the README's [Reading the report](README.md#reading-the-report) section lists them. The rubric reads:

- `session.json`: the exit status, the `result` message and the verdict, whose `divergence` is the first index where `actual` departs from `expected`, and whose `actions` name the states whose action is done;
- `trace.log`, each `trace-<section>.log`, `actions/` and `subagents.json`: what the session left;
- `transcript.jsonl` and `stderr.log`: what the agent read, wrote, ran and dispatched;
- the session's form as the run gave it, rebuilt from `workflows/<workflow>/` with the `pf` the run used, and its `scenarios.toml`.

### By Class

Each class the [scorer](score.py) defines, and `errored`:

| Class | `miss` when | `defect` when | `unclear` when |
| --- | --- | --- | --- |
| `missing_action` | The state's or dispatched section in the session's form names the file and value the scorer reads, and the transcript, the sub-agent's included, writes no such file or another value. | The form states another file or value than the scorer reads, `answers.txt` holds no answer the dispatched section can take, or the transcript writes the right value and `actions/` lacks it. | The transcript's writes cannot be matched to the record. |
| `unfinished` | The session ended on its own before the path's end: its `result` message claims completion, asks a question or gives up, and its exit status is not `timeout`. | The session was cut off while progressing: its exit status is `timeout` or its `result` names its session cap, with the transcript still walking states; or its trace went to a file other than `trace.log`. | The session timed out with no progress the transcript shows. |
| `invented_state` | The name entered at `divergence` is no heading of the session's form, written though the form spells the state as the path does. | The session's form spells that state as the session wrote it, so the form and the path disagree. | The name is close to a heading in a way neither the form nor the instruction settles. |
| `loop_miscount` | `inputs/` holds the scenario's value, the loop's decision in the form reads it as the path does, and the session looped otherwise. | The input as written, or the decision as the form states it, gives the count the session walked. | The decision's wording admits both counts. |
| `wrong_branch` | `inputs/` holds the scenario's value and the deciding section, in the session's form, sends that value down the path's branch. A `linked` session that did not open the rule document is a miss. | The form, or a `linked` rule document, sends that value down the branch the session took. | The condition's wording admits both branches. |
| `skipped_state` | The form links each omitted state from the one before it, and the session jumped past them. | The form gives no way to the omitted states from where the session stood, as a misplaced group or `subst` pair would. | The transcript shows the omitted states read but not traced. |
| `invalid_transition` | The form draws no edge to the state entered, and the session stepped back, repeated a state or went on past a terminal one. | The form draws the edge the session took. | The transcript shows a retry the agent did not explain. |
| `undispatched` | The transcript holds no `Agent` prompt naming a dispatched section's compiled file or authored reference, or holds them in another order, while the form states the dispatch. | The transcript holds those prompt targets in the scenario's order and `subagents.json` omits or reorders them. | A prompt's target cannot be matched to the form's files or authored references. |
| `sequential_set` | The transcript starts the set's members across more than one assistant message. | The transcript starts them in one message and `subagents.json` records them apart. | The stream's message boundaries are absent. |
| `unrelayed_question` | The sub-agent's report in the transcript opens with a question, and the session went on without starting it again with the answers. | `subagents.json` reads the return otherwise than the report inside the transcript's hand-back frame holds it. | The report's text is cut off. |
| `uncompiled` | A run a `[[scenario.compile]]` table states for an agent is in neither that agent's `commands` in `subagents.json` nor the transcript's shell calls, while the session's form states the line, link or guide run it compiles on a step the path reached. | The transcript's shell calls make that run and `subagents.json` omits it or gives it to another agent; or the form states no line, link or guide run for it on the path. | The transcript's shell calls are cut short, or a command's words cannot be split to read its references. |
| `overcompiled` | An agent's `commands` run `pf` on a reference no `[[scenario.compile]]` table states for it, as on a line whose step does not hold for the scenario's `inputs/`, and the form states no such line on the path. | The form states that reference on the path and the tables omit it; the reference is a stated one spelled in a way the scorer does not match; or the harness, not the agent, ran the command. | The step's condition admits reaching the line either way. |
| `misordered_compile` | The agent made every stated run, the transcript's shell calls make them in the order its `commands` record, and the form's steps reach their lines in the tables' order. | The transcript's shell calls make them in the tables' order and `subagents.json` records another; or the form's steps reach the lines in another order than the tables state. | One assistant message holds several of the runs, so their order is not settled. |
| `errored` | Never: the session entered no state. | The `result` text or `stderr.log` names the cause: a refusal, a spent or expired login, an unknown model or flag, a crash, a provider error. | Neither names a cause. |

### Dispositions File

The run writes each disposition to `results/<run-id>/dispositions.json`, mapping the session's place, `<model>/<workflow>/<scenario>/<form>/<repetition>`, to its `disposition` and the `evidence` that decided it:

```json
{
  "claude-haiku-5-5/preset-selection/title-selected/tree/3": {
    "disposition": "miss",
    "evidence": "inputs/change.txt holds code; Receive sends code to Assess; the session entered Edit"
  }
}
```

The [report](report.py) lists every failing session under Failing Sessions with the disposition the file gives it, `untriaged` where it gives none, and refuses a disposition outside the three or an entry naming a session that did not fail. Rewrite the report once the file is complete:

```bash
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id>
```

A run is committed only when its report lists no `untriaged` session and no `defect` or `unclear` one.

## Stop Rules

Every runbook below holds these, beside its own:

- **Before the first session.** The run starts only once its runbook's budget and cost cap are set from a recorded shakedown. A preflight refusal, a missing harness binary or a missing provider key stops it before it spends.
- **During the run.** The run's spend so far is every landed session's `cost_usd`, summed:

  ```bash
  jq -s 'map(.cost_usd // 0) | add' evals/diagram-following/results/<run-id>/*/*/*/*/*/session.json
  ```

  When it reaches the cost cap, the run's process is ended and nothing is committed. A harness reporting no cost is held to its token budget alone.
- **After the run.** A `refused` run, a run failing on carried context, and a run whose triage gives any `defect` or `unclear` disposition commit nothing.

### Repeating a Stopped Run

A run id owns both `evals/diagram-following/results/<run-id>` and `<eval-root>/workspaces/<run-id>`. Either existing path refuses a run before bundling or starting a session. After its escalation is settled, inspect those two exact paths and remove both before repeating the whole run:

```bash
ls -ld evals/diagram-following/results/<run-id> <eval-root>/workspaces/<run-id>
rm -rf evals/diagram-following/results/<run-id> <eval-root>/workspaces/<run-id>
```

Use the eval root the stopped run recorded; its default is `~/projects/eval/prosiform`. Keep the stopped attempt's spend in the shakedown's aggregate allowance when its directories are removed.

## MVP Proof

The live proof of the feature workflows, run by [I10:E05](https://github.com/m2ux/prosiform/issues/594) W01.

| Item | Value |
| --- | --- |
| Harness | Asked at the start of the run: `claude`, `cursor` or `opencode`. |
| Model | Asked at the start of the run: any model the chosen harness reaches. |
| Workflows | `preset-selection,group-placement,subst-redirect,section-entry,section-composition,declared-inclusion` |
| Forms | The default `--forms`; the feature workflows are written in `bundle` and `tree`, so each scenario takes those two. |
| Repetitions | 5 |
| Sessions | 150: fifteen scenarios, two forms, five repetitions. |
| Session cap | 420 000 tokens: the shakedown's largest session, 206 458 tokens, doubled and rounded up to the next 10 000. |
| Token budget | 63 000 000 tokens: 150 times the session cap. |
| Cost cap | USD 2: 150 times the shakedown's mean session cost of USD 0.004123, doubled and rounded up to the next dollar. |
| Committed | `report.json` as `evals/diagram-following/evidence/mvp-proof.json`, with its `dispositions.json` read into it. `evidence/baseline.json` is untouched. |

```bash
make eval-diagrams HARNESS=<harness> ARGS='--models <model> --workflows preset-selection,group-placement,subst-redirect,section-entry,section-composition,declared-inclusion --repetitions 5 --session-budget-tokens 420000 --budget-tokens 63000000 --run-id mvp-proof'
```

The run's own stop rule: where its harness or model differs from the shakedown's below, it first repeats the shakedown on its own, records it here, and takes its session cap, token budget and cost cap from that.

### Shakedown

One repetition of every feature scenario in each form, on the harness and model the user named for it. Its measured tokens and cost set the proof's session cap, token budget and cost cap above.

| Item | Value |
| --- | --- |
| Harness | `claude`, named by the user on 2026-11-03. |
| Model | `claude-haiku-5-5`, named by the user on 2026-11-03. |
| Spending cap | USD 5 for every live run of the shakedown together. |
| Sessions | 30: fifteen scenarios, two forms, one repetition. |
| Session cap | 400 000 tokens: a session's tokens count its cache reads, so a feature session records over 100 000, past the runner's 60 000 default. |
| Estimate | USD 0.80: 30 sessions at the committed baseline's mean of USD 0.027 a session, its USD 4.01 over 150 sessions. |
| Run | `mvp-proof-shakedown`, 2026-11-03: `completed`, all 30 sessions started and passed, with no failing session to triage. Each session carried a managed plugin's hook response, which the run counts from its transcript. |
| Measured | USD 0.123701 in all, USD 0.004123 a session; 3 593 668 tokens, 119 789 a session, the largest 206 458. These set the proof's session cap, token budget and cost cap above. |

```bash
make eval-diagrams HARNESS=claude ARGS='--models claude-haiku-5-5 --workflows preset-selection,group-placement,subst-redirect,section-entry,section-composition,declared-inclusion --repetitions 1 --session-budget-tokens 400000 --budget-tokens 12000000 --run-id mvp-proof-shakedown'
```

## Baseline

The baseline over the hardened corpus, run by [I10:E00](https://github.com/m2ux/prosiform/issues/403) W02 and shaken down by E00 W04.

| Item | Value |
| --- | --- |
| Harness | `opencode` |
| Model | `openrouter/deepseek/deepseek-v4.1-flash-1017`, named by the user on 2026-11-04. |
| Workflows | The baseline workflows: the default `--workflows`. Edge workflows are selected explicitly for the composition-edge run. |
| Forms | The default `--forms`: each workflow in every form it is written in that the opencode harness runs. |
| Repetitions | 5 |
| Sessions | The matrix's cells times 5, as the run prints them before its first session. |
| Session cap | Set by E00 W04's shakedown, by the proof's rule: its largest session tokens, doubled and rounded up to the next 10 000. |
| Token budget | The sessions times the session cap. |
| Cost cap | Set by E00 W04's shakedown: the sessions times its mean session cost, doubled and rounded up to the next dollar, USD 2 a session at the fifth run's USD 0.007449. The run starts only once the user approves it. |
| Committed | `evidence/baseline.json`, written by `report.py --write-baseline`; the run's `report.md` as `evals/diagram-following/evidence/report.md`; and the run's measured cost in the README. |

```bash
make eval-diagrams ARGS='--session-budget-tokens <session cap> --budget-tokens <token budget> --run-id baseline'
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/baseline --write-baseline
```

### Shakedown

One repetition of every cell of the default matrix, on the baseline's harness and model. Its measured tokens and cost set the baseline's session cap, token budget and cost cap above, and the runner's default session cap and `EVAL_BUDGET_TOKENS` beside them.

| Item | Value |
| --- | --- |
| Harness | `opencode` |
| Model | `openrouter/deepseek/deepseek-v4.1-flash-1017`, named by the user on 2026-11-04. |
| Spending cap | USD 5 for every live run of the shakedown together. |
| Sessions | 74: the default matrix's 74 cells on this harness, one repetition. |
| Session cap | 2 830 000 tokens: the fifth run's largest session, 1 414 151 tokens, doubled and rounded up to the next 10 000. |
| Token budget | 209 420 000 tokens: 74 times the session cap. |
| Estimate | USD 0.57: 76 sessions at the fifth run's mean of USD 0.007449 a session. |
| Run | `baseline-shakedown`, 2026-11-03: at a 400 000-token session cap, stopped at 56 of 74 sessions, USD 0.304038 spent, on a `defect`: every dispatch session failed on the harness's reading of the sub-agent stream, escalated as [#632](https://github.com/m2ux/prosiform/issues/632). It sets no cap. |
| Check | `foreground-check`, 2026-11-03: `dispatch-question` and `dispatch-set` in `compiled`, one session each, on the harness #632 corrects: both `unfinished`, each a `defect` of the dispatch scenarios, escalated as [#637](https://github.com/m2ux/prosiform/issues/637). |
| Second run | `baseline-shakedown`, 2026-11-03, on #632's and #637's fixes and I10:E06's guide: crashed at 65 of 76 sessions on the first run's leftover workspaces, USD 0.359917 spent, 56 passed; 8 failures `defect` (`pf` asked for where no shell is given, `pf` refused under `Bash(pf:*)`, starts the scorer cannot match to their sections) and 1 `miss`, escalated as [#650](https://github.com/m2ux/prosiform/issues/650). It sets no cap; the shakedown repeats once #650 is settled, with `workspaces/baseline-shakedown` removed beside `results/baseline-shakedown`. |
| Fourth run | `baseline-shakedown-2`, 2026-11-04, on #650's decisions and the corpus beginning every workflow at `Entry` and ending it at `Exit`: all 74 sessions started, USD 0.536773 spent, 7 passed. 67 failed `wrong_branch` at divergence 0, each omitting the entry and exit states the scenarios require, because the instruction still forbade tracing "the diagram's start or stop marker". A `defect` of the instruction, not the corpus; it sets no cap. |
| Fifth run | `baseline-shakedown-3`, 2026-11-04, on the instruction corrected to trace a clicked marker: all 74 sessions started, 71 passed, USD 0.551214 spent over 20 815 533 tokens, the largest session 1 414 151 and the mean 281 291. Every charted form passed in full; the three failures are `authored` sessions that named `workflow.md#<heading>` where their step links `review.md`, `plan.md` or `draft.md`, each triaged `miss`. These set the baseline's session cap, token budget and cost cap below, and the runner's default session cap and `EVAL_BUDGET_TOKENS` beside them. |

```bash
make eval-diagrams HARNESS=opencode ARGS='--models openrouter/deepseek/deepseek-v4.1-flash-1017 --repetitions 1 --session-budget-tokens 2830000 --budget-tokens 215080000 --run-id baseline-shakedown'
```

## Edge Run

The edge workflows on every harness carrying a shell, run by [I10:E04](https://github.com/m2ux/prosiform/issues/579) W14 and shaken down by E04 W16. The edge workflows arrive with E04's earlier rows.

| Item | Value |
| --- | --- |
| Harnesses | `cursor` and `opencode`: one run each. |
| Model | The model this runbook records for the baseline, as each harness names it. |
| Workflows | The edge workflows E04 adds. |
| Forms | The forms the edge workflows are written in: `compiled`, and `bootstrap` for a bootstrapping skill. |
| Repetitions | 5 |
| Sessions | Per harness, the cells the run prints times 5. |
| Session cap | Set by E04 W16's shakedown, by the proof's rule. |
| Token budget | The sessions times the session cap, per harness. |
| Cost cap | Set by E04 W16's shakedown, by the proof's rule, per harness. `cursor` reports no cost, so its run is held to its token budget. |
| Committed | Each harness's `report.json` as `evals/diagram-following/evidence/composition-edges-<harness>.json` and its `report.md` beside it. `evidence/baseline.json` and `evidence/mvp-proof.json` are untouched. |

```bash
make eval-diagrams HARNESS=<harness> ARGS='--models <model> --workflows <edge workflows> --forms compiled,bootstrap --session-budget-tokens <session cap> --budget-tokens <token budget> --run-id composition-edges-<harness>'
```
