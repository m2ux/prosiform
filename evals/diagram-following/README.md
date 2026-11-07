# Diagram-Following Eval

How well an agent, given a workflow drawn as a Mermaid diagram whose nodes link the sections saying what to do in each state, follows that workflow to completion. The eval gives each workflow to headless agent sessions, scores the path each session took, and compares the pass rates with a committed baseline.

## Forms

Each workflow in [`workflows/`](workflows) is written in the forms [`workflow.py`](workflow.py) describes: a diagram, a prose form whose transitions are sentences, a linked form whose decisions name a document stating the state the branch enters, the two dispatch forms a workflow dispatching a target is written in, and a skill handing over a workflow's sources to compile. A session receives one of the forms below; every form but `bootstrap` and `compiled` is entered at `workflow.md`:

| Form | Material | What it isolates |
| --- | --- | --- |
| `bundle` | The diagram form bundled by `pf` into one file. | The product under test. |
| `tree` | The diagram form's source tree, unbundled. | Against `bundle`, what bundling adds. |
| `prose` | The prose form bundled by `pf` into one file. | Against `bundle`, what the diagram adds. |
| `linked` | The linked form's source tree, unbundled. | Whether a decision is resolved by following its link. |
| `compiled` | The compiled form's sources, with the bundle set `pf` compiles from them in the folder `pf` writes it to: the entry's bundle and every dispatched target's beside it, each opening with the run-pf line, with the build under test as `pf` on the session's path and a shell limited to `pf`. | Whether an agent runs `pf`, follows the guide it prints and the dispatch links of each bundle, and compiles the material a bundle defers as it follows it. |
| `authored` | The authored-protocol form's one bundle, whose state documents write the same protocol as prose. | Against `compiled`, what compilation adds. |
| `bootstrap` | A skill placed where the agent CLI discovers skills, naming the workflow's sources, written as the compiled form is, for the session to compile with `pf`. | Whether an agent compiles a workflow it is handed as sources before following it. |

A workflow gives a session only the forms it is written in: `linear`, `branching`, `looping`, `pricing` and `rework` take `bundle`, `tree`, `prose` and `linked`, the four dispatch scenarios take `compiled` and `authored`, the three [deferral workflows](#deferral-scenarios), the two [composition workflows](#composition-scenarios), `dispatch-depth` and `subagent-first-run` take `compiled` alone, the two [bootstrap workflows](#bootstrap-scenarios) take `bootstrap` alone, and the six workflows built on a feature, `preset-selection`, `group-placement`, `subst-redirect`, `section-entry`, `section-composition` and `declared-inclusion`, take `bundle` and `tree`.

The linked form's entry draws the diagram's flowchart with no branch label, and its decisions name no branch of their own. Each names a rule document, by a name that gives nothing away, stating the one state its branch enters, so the edge a branch takes is recoverable only by opening the document the section links, and the state it states is held to the edges the diagram draws out of the deciding state. Its rule document's destination resolves from the section that writes it, under `states/`.

Each form's entry is held to what it may carry: a prose entry draws no diagram, and a linked entry draws the diagram's edges and no label on any of them.

Every session is given the same [instruction](instruction.md), naming only the entry document; a `bootstrap` session takes [its own](instruction-bootstrap.md), telling it a skill is available to find, and a `compiled` session [its own](instruction-compiled.md), naming the entry's bundle where `pf` wrote it and telling it to compile from the directory holding the sources. Each `[[scenario]]` table in a workflow's `scenarios.toml` declares one scenario:

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

A diagram form's bundle states a path of its own, and a scenario's path is held to it beside the sources' walk. Each state is entered at the heading the previous state's link names, by its text or by the heading it links, as a `↳` composition or a footnote mark does, or else the one the bundle's diagram clicks, and its action and transition are read from what that heading holds. A state `pf` placed into a group or reached through a `subst` pair is followed where the bundle puts it, and the bundle must state the action the sources state, since the scorer reads the sources'. A feature workflow's substitutes therefore state the action and transition of the state they stand in for, so the `tree` form walks the same path the `bundle` form does.

A diagram form's `click` lines carry destinations relative to the document that writes them, so a node opens its section for a reader of the source tree and for a session in its workspace. GitHub draws a Mermaid fence in a frame of its own and resolves such a destination against that frame, so a diagram form's clicks open nothing in the blob view; the state documents sit beside the entry document all the same.

### Dispatch scenarios

The four dispatch scenarios say what a bundled workflow's dispatch protocol is for: whether an agent hands a dispatched section to a sub-agent at all, starts a set's targets together, and puts a sub-agent's question to the user rather than answering it.

| Workflow | Scenario | What it dispatches |
| --- | --- | --- |
| `dispatch-chain` | `chain` | A section whose own step dispatches a second, so a run starts two sub-agents in order. |
| `dispatch-set` | `parallel-set` | Two sections at once, so a run starts two sub-agents together. |
| `dispatch-beside` | `set-beside-a-dispatch` | One section, then two more as a set of their own. |
| `dispatch-question` | `returned-question` | A section returning a question, answered from the scenario's `answers.txt`, then dispatched again with the answer. |

Each dispatched section states an action, a file under `actions/` and the value it holds, as a state's section does, so a sub-agent's file is the evidence that it followed its section. A dispatch scenario's `scenarios.toml` names the trace a correct run produces beside the path it walks: one `[[scenario.trace]]` table per sub-agent start, in the order the walk dispatches it. A scenario whose sub-agent returns a question states its `answers`, which the run writes to `answers.txt` in the session's workspace; the instruction tells the session the user's answers are there, and the sub-agent's action holds the answer it was handed back.

| Field | Meaning |
| --- | --- |
| `dispatch` | The section the sub-agent follows, as `<document>#<heading>`. Both forms name a section, so one trace is the trace of both. |
| `together` | Whether it started beside the entry above it, which marks every member of a set but the one opening it. |
| `action` | The `file` under `actions/` the section has the sub-agent write, and the `value` it holds. A deferred composition's activated material states the action too, as [Sub-agent runs](#sub-agent-runs) states. |

The trace is held to the source: [`dispatch_walk()`](workflow.py) walks each state's steps in path order, following a dispatched section's own steps and the dispatches of the material each deferred composition a step reaches compiles, and the test asserts the corpus states that walk and no other. The compiled form writes a step's targets with `⇉`, and a set's with `⫽`, so `pf` compiles each target into a bundle of its own, and its step is its marks alone: `pf` publishes a `⇉` link to the target's bundle where it stands and a set as a `⫽ Dispatch Set` sub-section of `⇉` items, and the guide bare `pf` prints states what to do with each, so a sentence beside the marks would state the dispatch a second time and is a fault. The authored form writes the same steps as ordinary links to the same sections and the protocol as prose, so it publishes the entry's bundle alone and its prose is its only statement of the dispatch. The two forms therefore hold one statement of the dispatch each, and a pass rate's difference between them is what compilation adds.

`dispatch-depth`, written in the `compiled` form alone, dispatches three hops below the session, the depth `pf` publishes with no `W_DISPATCH_DEPTH`. A sub-agent's own dispatch starts before it returns, so each hop is listed after the one that started it.

| Workflow | Scenario | What it dispatches |
| --- | --- | --- |
| `dispatch-depth` | `three-hop-chain` | A chain of three sections, each dispatching the next. |
| `dispatch-depth` | `three-hop-set` | A section whose first step starts two sections as a set at the second hop, and whose second step starts a section dispatching the third. |
| `dispatch-depth` | `three-hop-question` | A chain of three whose last section returns a question, relayed up each hop to the user, then the chain dispatched again with the answers. |

### Stated runs

A scenario names each `pf` run a correct session and each of its sub-agents makes: one `[[scenario.compile]]` table per run, in the order the walk makes them.

| Field | Meaning |
| --- | --- |
| `by` | Optional. The section of the scenario's trace whose sub-agent makes the run, as `<document>#<heading>`; absent for the session's own run. |
| `entry` | Optional. The one reference supplied as the positional entry, as `<document>` or `<document>#<fragment>`; absent for bare `pf`, which prints the guide. |
| `presets` | Optional. The comma-separated link-title names supplied to `--presets`; needs an entry. Complete names trim, case-fold and deduplicate. Only matching declarations contribute to the effective selection. |

A reference resolves from the directory a shell form runs `pf` in: the skill's directory for `bootstrap`, as the guide states, and the workspace for `compiled`, which holds the compiled form's sources as they stand. The corpus test refuses a reference naming no document there, a `by` naming no section of the trace, and a run stated by a workflow written in neither form.

For example, `entry = "reference/fetch.md#read-mirror"` with `presets = "mirror"` states `pf reference/fetch.md#read-mirror --presets=mirror`. Output and diagnostic options are the agent's to choose. A named selection's expected output includes the compiler's qualifier over its matching declared names. The scorer reads the compiler's command grammar and compares effective selections; missing or different matching presets fail the run check. Informational `--help`, `--version` and `--codes` calls satisfy neither a compile nor the bare guide run.

A `compiled` session reads the bundle set `pf` compiled from the compiled form, so a `↳` line the bundle carries names its target from the workspace, and compiling it there is the run the scenario states where a step its path takes reaches the line, as [Deferral scenarios](#deferral-scenarios) states. The four dispatch scenarios compile nothing, so they state no run.

A stated run a sub-agent makes is read from that sub-agent's own commands, which requires a shell form and the harness's `nested_commands` capability: `claude` in the `compiled` form. `nested_starts` separately states whether child dispatches are observed. Codex exposes nested starts while its start records carry no child commands, so it receives deep chains and omits scenarios requiring per-child compiler runs. A harness reporting no sub-agent's commands is given no scenario stating a sub-agent's run, as it is given no scenario whose trace outruns the starts it reports: those the session makes itself, from its path's own steps and from the bundle its run on a `↳` line writes.

### Sub-agent runs

A sub-agent's `pf` run is stated by the section it follows and read from that sub-agent's commands where its harness reports them; it is also shown by what it makes possible. Every bundle opens with the run-pf line, saying to run bare `pf` and follow the guide it prints, so a sub-agent handed one reads how to compile a `↳` line before it meets one. A trace entry's `action` names the file only the material `pf` compiles on that line states, so a sub-agent that ran no `pf` leaves it unwritten. The corpus test compiles each dispatched bundle a scenario's trace follows, from the entry's set or the set a run on a `↳` line wrote, runs `pf` on each line its steps reach, and holds the entry's `action` to the one that material states and the bundle itself does not, and the runs the scenario states `by` the entry's section to the lines its sub-agents compile, in order. It holds each such bundle to opening with the run-pf line, each `⇉` link a bundle carries, inline or as a dispatch-set item, to a file its run wrote, and each bundle a sub-agent follows to one a `⇉` link names. A scenario stating a sub-agent's run is given to `claude` alone, as [Stated runs](#stated-runs) states.

| Workflow | Scenario | What its sub-agents run |
| --- | --- | --- |
| `subagent-first-run` | `first-hop-run` | The ledger, dispatched from the path, compiles its `↳` line, whose material states its action. |
| `subagent-first-run` | `deep-hop-runs` | The review, at the second hop, compiles its `↳` line, whose material states its action and dispatches the ruling; the ruling, at the third, compiles its own `↳` line, whose material states its own. |

### Bootstrap scenarios

The two bootstrap workflows say whether an agent handed a skill, rather than an entry document, compiles the workflow the skill names before following it. A session finds the skill under `.claude/skills/<workflow>/` in its workspace, where the agent CLI discovers skills. The skill's `SKILL.md` says to run `pf`, then holds one hand-written `[↳ <title>](<path>)` line, titled as the document it names is headed, so the guide bare `pf` prints says to compile that document, read it whole and follow it, and the bundle that run writes is the document stating the workflow. The run puts the build under test on the session's path, so the `pf` a session compiles with is the one the run was configured with.

Compiling runs a command, so the session is given `pf` and a shell as a `compiled` session is. Each scenario states bare `pf`, then `pf` on the line's path, and its path is the walk of the bundle that run writes, as the corpus test compiles it from the skill's directory. `bootstrap-audit`'s sources dispatch sub-agents, so each of its scenarios names the trace a correct run produces as a dispatch scenario does, and a harness that reports no sub-agent's own dispatch is given only the scenarios whose trace it can observe. `inline-bootstrap`'s `SKILL.md` declares no `prosiform`, so its line is held as written, and its sources dispatch nothing.

| Workflow | Scenario | What it walks |
| --- | --- | --- |
| `bootstrap-audit` | `blocking-two-halves` | Source and tests gathered as a set, the appraisal, a blocking verdict, then the repair. |
| `bootstrap-audit` | `clean-one-half` | Source and tests gathered as a set, the appraisal, then a clean verdict straight to publishing. |
| `inline-bootstrap` | `feature-tagged` | The freeze, a feature tagged, then the broadcast. |
| `inline-bootstrap` | `fix-backported` | The freeze, a fix backported, then the broadcast. |

### Deferral scenarios

The three deferral workflows say whether an agent following a `compiled` bundle runs `pf` on each `↳` line its path needs, and on no other. A source writes a deferred composition, `[¬↳ <title>](<path>#<section>)`, and `pf` publishes it as a link from the step writing it to a sub-section holding the `[↳ <title>](<path>#<section>)` line. A step opening with a condition, "If `inputs/<file>` reads `<value>`,", reaches its lines only where that condition holds, and a run's bundle may hold further lines its own steps reach. The corpus test walks the bundles as a session does: it compiles the entry's bundle, runs `pf` from the compiled sources on each line a step of the walk reaches, reads what each run writes as part of the state that reached it, and holds the scenario's runs and path to that walk.

The material a `↳` line compiles may itself dispatch: the run on it writes a bundle linking the bundles of the section's own targets, and those are the sub-agents the agent that ran it starts.

A state may also defer its transition: its document writes no `**Next.**` paragraph, and the material its deferral compiles states "Take the transition labelled `<label>`.", so only a session that ran `pf` on the line knows the edge to take.

| Workflow | Scenario | What it runs |
| --- | --- | --- |
| `deferred-composition` | `deferral-reached` | `pf` on the migration's line, which Relocate's step reaches where `scope.txt` reads `large`. |
| `deferred-composition` | `deferral-passed` | Nothing: Relocate's step does not hold, so its line is passed. |
| `deferred-composition` | `nested-needed` | The migration's line, then the archive's line its bundle holds, whose step holds where `history.txt` reads `kept`. |
| `deferred-composition` | `nested-unreached` | Nothing: the archive's step holds, but the migration's bundle that carries it is never compiled. |
| `deferred-dispatch` | `deferred-dispatch-compiled` | `pf` on `reference/loading.md#crew`, the `↳` line `Pack`'s step reaches where `order.txt` reads `bulk`, whose bundle dispatches `reference/crew.md#work` with `lift`, then `strap`, each selection writing its own action. |
| `deferred-dispatch` | `deferred-dispatch-passed` | Nothing: `Pack`'s step does not hold, so its line is passed and nothing is dispatched. |
| `preset-deferral` | `stand-in-followed` | `pf reference/fetch.md#read-mirror --presets=mirror`. The deferral's title selects `fetch.md`'s `mirror` preset, whose `subst` puts the stored copy in place of the live page, so the transition the stand-in states sends the path to `Restore`, where the live page's would send it to `Serve`. |

### Composition scenarios

The two composition workflows say whether an agent following a `compiled` bundle reads each label as `pf` publishes it. A composition, `[↳ <title>](<path>#<section>)`, composes its section under its title beneath the step writing it, so the bundle carries that material whatever the inputs; a footnote mark such as `[†](<path>#<section>)` is an ordinary link, so `pf` publishes its target as a document of its own and the agent opens it. A state the diagram clicks nowhere is entered where the previous state's composition or footnote leads, so a correct path reaches it only through that label.

| Workflow | Scenario | What it walks |
| --- | --- | --- |
| `conditional-composition` | `composed-entered` | `Convert`, which `Gauge` composes beneath a step holding where `scope.txt` reads `large`. |
| `conditional-composition` | `composed-omitted` | Past `Convert`: the bundle still carries it beneath `Gauge`'s step, which does not hold. |
| `directive-labels` | `footnote-opened` | The house style composed in place beneath `Compose`'s step, then `Vet`, the document its footnote opens. |
| `directive-labels` | `self-composed` | `Issue`, whose `Release` step composes the `Summary` section of its own document, which `pf` publishes with `W_COMPOSE_SELF`. |

### Feature scenarios

The six feature workflows each build on one bundling feature, and each scenario of one fixes a permutation of it. A session takes `bundle` or `tree`.

| Workflow | Scenario | Permutation |
| --- | --- | --- |
| `preset-selection` | `default-alone` | A link whose title selects no preset of its document, so the document's default places the state. |
| `preset-selection` | `title-selected` | A link title selecting one preset of the document it names. |
| `preset-selection` | `two-presets-one-title` | A link title selecting two presets of one document together. |
| `group-placement` | `leaf-group` | Two states that link nothing, placed in one group. |
| `group-placement` | `nested-intermediate` | A state placed in a group inside the group of the state linking it, and a second inside that. |
| `group-placement` | `two-presets-one-document` | One document reached under its default and under a preset, so it stands in two groups. |
| `subst-redirect` | `document-redirect` | A default substitute redirecting a link to another document. |
| `subst-redirect` | `section-redirect` | A default substitute redirecting a link to one section of another document. |
| `subst-redirect` | `preset-over-default` | A preset's substitute holding over the default's. |
| `section-entry` | `document-fragment` | An entry naming one section of a document, which leaves the document's other sections out. |
| `section-composition` | `merged-sources` | Two sections written by one section's links, merged into one. |
| `section-composition` | `deferred-occurrence` | A link whose composition a later run of `pf` defers. |
| `section-composition` | `nested-composition` | A linked section that itself links a further section, composed inside it. |
| `declared-inclusion` | `declared-link-followed` | A state a document links that the diagram also declares, entered along the diagram's edge. |
| `declared-inclusion` | `undeclared-link-as-text` | A link to a document the diagram does not declare, which the session reads as text and does not enter. |

## Scoring

A session records each state it enters as a line of `trace.log` and does each state's action by writing a file under `actions/`. Every instruction tells it to hand each sub-agent it dispatches the name `trace-<section>.log`, since a sub-agent reads only the prompt its session writes, and the run keeps each such trace beside the session's own. The same instruction tells it to name, in that prompt, the file or section it hands over, so a start is identified by what it was given rather than by prose. The [scorer](score.py) passes a session whose trace is its scenario's path with every state's action done. A failing session takes the first of these classes that fits where its trace departs from the path:

| Class | The session |
| --- | --- |
| `missing_action` | walked the path and left a state's action undone or wrong, or, in a dispatch scenario, a sub-agent's. |
| `unfinished` | stopped partway along the path. |
| `invented_state` | entered a state the diagram does not hold. |
| `loop_miscount` | repeated a loop more times than its input requires. |
| `wrong_branch` | took the other branch of a decision on an input. |
| `skipped_state` | jumped ahead, omitting states between. |
| `invalid_transition` | entered a state no edge leads to: a step back, a state after the end, or the same state again. |

A session whose agent reports an error, or prints no `result` message, takes `errored` instead of any of these. It entered no state, so its trace says nothing about how it followed the workflow: a refusal, an expired quota or a crashed command fails `errored` rather than as an `unfinished` run.

### Misreadings the scenarios provoke

Each failure class the scorer defines is produced by some scenario, and the corpus test names any class none produces: it scores each scenario's path departed from once at every point, and a session whose agent reported an error is `errored` on any scenario. Each workflow is written so a plausible misreading departs in a class of its own, so a run's failures say which way an agent departed.

| Workflow | What it makes possible to misread |
| --- | --- |
| `linear` | A state skipped or repeated on a path with no decision. |
| `branching` | One decision's branch. |
| `looping` | A two-round loop, and `Check`, a state no click names, reached only through the link in `Revise`'s section. |
| `pricing` | A second decision after the first, read from its own input, and `Refund`, a state drawn and linked from the terminal `Invoice` that no edge leads to. |
| `rework` | A four-round loop whose bound counts `Retest`, a state no click names, reached only through the link in `Rework`'s section. |

### Dispatch checks

A dispatch scenario states the sub-agents a correct run starts, so a run whose trace is the path and whose actions are done is held to its sub-agent record before it passes. The record is [`subagents.json`](score.py), written from the session's transcript as it settles and sitting beside the trace and the session's cost, so the scorer reads it rather than the transcript. It holds the session's own shell `commands`, null where its harness gives it no shell, and its `starts`. Each start names the section a sub-agent followed, what it returned, whether it started beside the entry above it, `parent`, the index of the start whose sub-agent made it, null for the session's own, and `commands`, the shell commands its sub-agent ran, so each sub-agent's starts and commands sit under the section it followed at every depth the harness's stream reports. A return is the sub-agent's report, read from inside the frame its CLI puts around it, and is `question` when its first line opens `Question:`, as the authored workflow's question procedure states, and `done` otherwise.

The checks hold the dispatch's shape, then the session's handling of each return as the dispatch protocol states it: a start returning `done` moves the session on, and one returning a question is started again with the answers. Each sub-agent's action is then held as a state's is.

| Class | The session |
| --- | --- |
| `undispatched` | left a bundle the scenario dispatches without a sub-agent, or started them in another order. |
| `sequential_set` | started a set's bundles across more than one message, rather than its opener first and every later member alongside it in that message. |
| `unrelayed_question` | went on from a sub-agent's returned question without starting it again with the answers. |
| `missing_action` | left a sub-agent's action unwritten or wrong, named in the verdict's `actions`. |

The four are read in that order, after the run is held to its path and its actions, so a trace that stopped short is `unfinished` however few sub-agents it started, and a record failing two checks takes the earlier. A scenario that dispatches nothing passes all four.

A run passing them is then held to each sub-agent's stated `action`, whatever its harness reports: one absent or wrong is `missing_action`, so a sub-agent that ran no `pf` on its line fails though no stream carries what it ran.

### Run checks

A run that passes the dispatch checks and its sub-agents' actions is held to the `pf` runs its scenario states, wherever its harness reports the commands a session ran. A run is a command, split at `;`, `&&`, `||` and `|`, whose first word is `pf` or a path ending `/pf`; its single destination is the positional entry and its selection is the optional `--presets` value, parsed with the compiler's grammar. The destination names a stated reference when it is that reference or ends `/` and that reference, and the destination's effective matching preset sets must agree. Malformed compile commands satisfy no stated run; informational calls satisfy neither a compile nor the bare guide run. The session's runs, and each sub-agent's from the commands of the starts naming its section, are held to those stated for it:

| Class | The session |
| --- | --- |
| `uncompiled` | left a stated run unmade, or a sub-agent did. |
| `overcompiled` | made a run naming a reference no stated run names, as one on a deferred line its path did not reach does, or a sub-agent did. A bare `pf` beyond those stated prints the guide and compiles nothing, so it is no departure. |
| `misordered_compile` | made its stated runs in another order, or a sub-agent did. |

The three are read in that order, after the dispatch checks, so a sub-agent that never started is `undispatched` rather than leaving its runs unmade. A harness reporting no command, as the Claude harness does in every form but `compiled` and `bootstrap`, holds a session to none of them.

A run in which every session it started took `errored` is **refused**. No session entered a state, so the matrix is no result, and its pass rates would read a spent login as a matrix of failing agents. `run.json` records `"state": "refused"` and a `reason`, and its report names both instead of giving tables or comparing pass rates. The reason is one session's own `result` text, so a reader sees the limit the agent reported. A run its budget stopped part way is refused on the same terms, since the sessions it never started add nothing its errored ones lack; one where some sessions errored on a genuine fault beside sessions that entered a state is a completed run whose failures are its result. The boundary is decided once the sessions settle, before `run.json` is written.

## Login

Sessions run on an agent CLI the run names, `--harness claude`, `--harness cursor` or `--harness opencode`, and each harness states what confines its sessions. The Claude harness runs on the eval's own login, kept apart from yours in `<eval-root>/config`, where the eval root defaults to `~/projects/eval/prosiform`. Log in once:

```bash
CLAUDE_CONFIG_DIR=~/projects/eval/prosiform/config claude
```

then `/login`.

The opencode harness keeps its own login there too, in a credential store the run names under the eval root. Log in once:

```bash
cd ~/projects/eval/prosiform && \
XDG_DATA_HOME=$PWD/config/data XDG_CONFIG_HOME=$PWD/config/config \
XDG_STATE_HOME=$PWD/config/state XDG_CACHE_HOME=$PWD/config/cache \
opencode auth login --provider <provider>
```

## Isolation

A session receives one form of one workflow and the instruction, so a pass measures the agent reading that form. Each mechanism below holds one part of that boundary for the Claude harness; the first two are refused before a session starts, and the last is read back from each session's own transcript.

| Mechanism | What it keeps out |
| --- | --- |
| `CLAUDE_CONFIG_DIR` names the eval's config directory | The caller's own configuration, memory and settings, which no session reads. Every `CLAUDE*` and `ANTHROPIC_*` variable the caller holds is dropped from the session's environment, and `CLAUDE_CONFIG_DIR` is set beside `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`, which runs each sub-agent within the call that starts it, so the call's result is the sub-agent's answer. |
| `--strict-mcp-config` | Every MCP server, since the session is given no server list. |
| `--disable-slash-commands` | Every slash command and skill the configuration directory would offer. |
| `--tools Read,Write,Edit,Glob,Grep,Agent,Bash` | Every other tool; `Agent` dispatches sections and `Bash` runs the build every form receives. |
| `--allowedTools Bash(pf *)` | Admits `pf` with any arguments and output redirects in the workspace. Every form finds the build under test on its path, with no workspace copy. |
| `--permission-mode acceptEdits` | Writes outside the session's fresh workspace. |
| `--no-session-persistence` | A transcript surviving the run beyond the record the eval keeps. |
| The injected-context read | Context the agent added that the run did not supply. |

Neither flag suppresses a plugin's hooks or a settings file's, so the preflight refuses a run whose settings would let one the organisation does not manage reach a session. It fails before the first session starts, naming the file to remove. Each file below is read from the scope shown, and a file holding only preferences is no refusal. Files in the eval's config directory are read under the user scope:

- `plugins/installed_plugins.json` installing a plugin at any scope but `managed`, whose `hooks/hooks.json` may declare a `SessionStart` hook;
- `remote-settings.json` enabling a plugin in `enabledPlugins` with no `remote-settings.json.signature.json` beside it, so no organisation signed it;
- `settings.json` declaring a hook for any event in its `hooks` block, which delivers that command to a session with no plugin installed at all. The refusal names each event the block declares, so the directory keeps its theme and model.

Files in a project's `.claude` directory are read under the project scope, `settings.local.json` being its untracked local variant. A file of either name declaring a hook for any event is refused, naming each event, from two places:

- a workflow's form tree, the source a session's workspace is copied from, so the file reaches every session of that tree; remove the file from the tree;
- the `.claude` directory of every ancestor of the workspaces, the workspace root `<eval-root>/workspaces` included, since Claude Code reads project settings from each directory on the path from a session's working directory to the filesystem root. Remove the file, or pass an `--eval-root` outside that ancestor, which moves the workspaces from under it.

A run whose config directory holds no login fails the same way, naming the one-time login command.

A managed configuration reaches every session wherever the config directory points: a plugin installed at `managed` scope or enabled by the signed `remote-settings.json`, the environment settings that file's `env` applies over the scrubbed environment, and the hooks a managed plugin or the host's managed settings file, `/etc/claude-code/managed-settings.json` on Linux, which belongs to the host's administrator, delivers. The run records it rather than refusing it, and names none of it: `run.json` and the report state how many managed plugins, environment settings and hooks the sessions carried, and a fingerprint, a SHA-256 digest over the plugin identifiers and versions, the environment keys and the hook events, so two runs on one configuration show one fingerprint and a changed configuration shows another. The hooks are counted from the transcripts once the sessions finish: each hook event a session's transcript shows a hook responding to counts once, its output never read, since no file the harness reads states every hook a managed plugin brings. A host with nothing managed records zero counts and a null fingerprint, and the sessions start either way.

A session that still carries context the run did not supply fails the run after its sessions finish, naming each one and what it carried. The context read is what makes the boundary observable rather than assumed: an appended system prompt, a memory file, or a hook's `additionalContext` where no managed plugin is present and the host's managed settings file declares no hook is another instruction set beside the form, and a session carrying one is no evidence of how the agent followed the form. Otherwise a hook's response is the managed configuration's, since the preflight admits no other hook. The run raises before it writes `run.json`, so a refused run is never reported as a completed one.

### opencode

The opencode harness keeps the same boundary by naming each directory the CLI would otherwise share with the caller under the eval root, and by writing the one settings file a session reads. A run whose credential store under that root holds no login is refused before its first session.

| Mechanism | What it keeps out |
| --- | --- |
| `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME` and `XDG_CACHE_HOME` name directories under the eval root | The caller's configuration, installed plugins, remembered projects, credential store and cache. Every `OPENCODE*` variable the caller holds is dropped from the session's environment. |
| `OPENCODE_CONFIG` names `<eval-root>/config/harness.json` | Every other settings file, and the permissions a workflow's own `opencode.json` would add. |
| `OPENCODE_PURE` and `OPENCODE_DISABLE_DEFAULT_PLUGINS` | Every plugin, the CLI's own among them, so no hook or tool they register reaches a session. |
| `OPENCODE_DISABLE_EXTERNAL_SKILLS` and `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS` | Every skill of the caller's, under `.claude/skills` and `.agents/skills`, which the CLI would otherwise offer beside the form. |
| `OPENCODE_DISABLE_PROJECT_CONFIG` | A project's own `opencode.json`, whose permissions or instructions would arrive beside the form. |
| `OPENCODE_DISABLE_MODELS_FETCH` and `OPENCODE_DISABLE_AUTOUPDATE` | The network calls a catalogue fetch and an update check make. |
| The written `permission` block | Every command but `pf`, and every path but the session's workspace: `bash` admits `pf *` and denies the rest, `external_directory` denies a read, a write and a shell command outside the workspace, and `webfetch` and `websearch` deny the network. `edit`, `read`, `glob`, `grep`, `list` and `task` admit the workspace and the dispatch a compiled bundle states. |

A bootstrap skill is placed at `<workspace>/.opencode/skills/<name>`, which is the root this CLI discovers, rather than the `.claude/skills` root the other two read.

## Running

| Command | Runs |
| --- | --- |
| `make eval-diagrams` | The [runner](run.py) over the default matrix, then the report. Its token budget is `EVAL_BUDGET_TOKENS` and its harness `HARNESS`; `ARGS='...'` passes the runner's options through, a later `--budget-tokens` among them overriding the default. |

Each live run follows its runbook in [`RUNBOOK.md`](RUNBOOK.md), which also holds the triage rubric every failing session is decided by. The command starts paid agent sessions, so no other target depends on it and `make check` never runs it; `make harness` holds the runner, scorer and report against a stub agent and recorded results instead. The runner's options, each passed through `ARGS`:

A run id requires fresh results and workspaces. An existing `results/<run-id>` or `<eval-root>/workspaces/<run-id>` refuses the run before bundling or starting a session. The runbook's [rerun procedure](RUNBOOK.md#repeating-a-stopped-run) removes both.

| Option | Default | Meaning |
| --- | --- | --- |
| `--budget-tokens` | required | The run's token cap, at least the sessions times `--session-budget-tokens`. A later value in `ARGS` overrides the default. |
| `--session-budget-tokens` | 2 830 000 | Each session's token cap. |
| `--session-timeout-seconds` | 600 | How long a session runs before it is ended and scored as it stands. |
| `--models` | `openrouter/deepseek/deepseek-v4.1-flash-1017` | The models, comma-separated. |
| `--workflows` | baseline workflows | The workflows, comma-separated. |
| `--forms` | `bundle,tree,prose,linked,compiled,authored,bootstrap` | The forms, comma-separated. A workflow gives sessions only in the forms it is written in. |
| `--repetitions` | 5 | Sessions per model, form and scenario. |
| `--parallel` | 4 | Sessions running at once. |
| `--eval-root` | `~/projects/eval/prosiform` | The directory holding the login and the workspaces. |
| `--harness` | `opencode` | The agent CLI the run drives: `claude`, `cursor`, `opencode` or `codex`. |
| `--agent-command` | the harness's own command | The agent's command line, overriding the harness. |
| `--results` | `results/` beside this file | Where runs are recorded. |
| `--run-id` | the start time, as `YYYYMMDDTHHMMSSZ` | The run's directory name. |

For example, one model over one workflow:

```bash
make eval-diagrams ARGS='--workflows linear --repetitions 1 --budget-tokens 100000 --session-budget-tokens 20000'
```

The nested-dispatch scenarios, `dispatch-depth`'s and `subagent-first-run`'s, are written in `compiled` alone, whose Claude session carries the shell limited to `pf`:

```bash
make eval-diagrams ARGS='--forms compiled --workflows dispatch-depth,subagent-first-run --repetitions 1 --budget-tokens 600000'
```

### Default matrix and budget

The default matrix is one model, `openrouter/deepseek/deepseek-v4.1-flash-1017` on the `opencode` harness, which the [runbook](RUNBOOK.md#shakedown-1) records as the user's choice; the thirty scenarios of the sixteen workflows, in the forms each is written in, 74 cells in all; and five repetitions: 370 sessions. The committed baseline covers six forms, every one but `bootstrap`, whose dispatched sections state no states to trace: 360 sessions.

A run is held to tokens, the one measure every harness reports, and `--budget-tokens` must cover the sessions times `--session-budget-tokens` or it is refused before a session starts, naming the budget, the sessions, the cap and the budget they need. The default matrix's 370 sessions at the 2 830 000-token session cap need 1 047 100 000, which `EVAL_BUDGET_TOKENS` covers; a smaller matrix lowers the need by its sessions and a lower `--session-budget-tokens` by the cap.

The committed baseline measured USD 2.50148 over 92 601 825 tokens for its 360 sessions, so a rerun spends about the same. It is one harness's run: its sessions all record exit status 0, so `opencode` crashed on no form the run covers. A harness with no committed baseline has no such evidence of its own.

The Claude harness also passes `--max-budget-usd` to its CLI, which caps dollars between calls and reports no token ceiling. That figure is the harness's own `session_cap_usd`, USD 0.50, not the token cap, so it bounds what one session can spend before the run's guard sees a result. The Cursor and opencode CLIs accept neither a spend cap nor a token cap, so a run on either is bounded by its timeout and by the run's guard alone.

The run's guard reads each session's reported tokens when it settles: a session starts only when the recorded tokens, plus the cap reserved for each session in flight, plus its own cap, fit the budget, and a run that cannot fit another lists the rest as not started. A session's tokens are every model's its CLI reports, its sub-agents' among them. A session can record more than its cap, since its own CLI checks between calls, and the guard holds the budget against that by reserving caps in flight.

## Reading the report

A run writes its records under `results/<run-id>/`, which git ignores: per session, `<model>/<workflow>/<scenario>/<form>/<repetition>/` with its transcript, its own `trace.log`, each dispatched sub-agent's `trace-<section>.log`, actions, sub-agent record and `session.json`; and `run.json`, the run's options, each form's command line, harness, managed configuration, tokens, state and sessions not started. `subagents.json` holds the session's commands and the sub-agent starts the transcript records, one per entry, in order, each with its parent and its commands, so a reader sees what the agent dispatched and ran; `session.json` also holds the scenario's dispatch trace, so a reader sees the sub-agents a correct run starts beside the verdict on the one that ran. The runner then writes `report.md` and `report.json` beside `run.json`. To write them again, against another baseline:

```bash
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --baseline <file>
```

The [report](report.py) gives three tables: per model, per model and form across scenarios, and per model, form and scenario. Each row gives its sessions and passes, the pass rate, each failure class's count, the sessions ended at their timeout, the mean tokens and the mean cost where a harness reports one. The report opens with the run's tokens, the managed configuration its sessions carried, counted and fingerprinted, its cost, the sum of every session's reported cost, and the count of sessions not started. It then lists each failing session with the disposition its triage gave it in `dispositions.json` beside `run.json`, as the [runbook](RUNBOOK.md#dispositions-file) states, and closes with the sessions not started.

A refused run — one every started session of which took `errored` — has no row and no comparison. Its report gives the run's `refused` state and the reason `run.json` records, the reason being one session's own `result` text, so a reader sees the limit the agent reported rather than a pass rate. `--write-baseline` writes only from a run whose report holds a cell, so a refused run, or one that started nothing, leaves the committed baseline as it was.

`baseline.json` beside this file is the baseline, a reviewed default run's cells: each one's sessions, passes, pass rate and failure counts, with that run's id, date, models, repetitions and cost. [`report.md`](report.md) beside it is that run's report. With a baseline present, each row's Change is its pass rate less the baseline row's, in percentage points, and each failure count is followed by its change in brackets when it moved. A row the baseline lacks reads `new`, and the rows the baseline holds that the run lacks are listed under Baseline Only. With no baseline, Change reads `—`.

## MVP proof

[`mvp-proof.json`](mvp-proof.json) records a live run of the [feature scenarios](#feature-scenarios), with its [report](mvp-proof.md) beside it: 150 sessions on the `claude` harness and `claude-haiku-5-5`, fifteen scenarios in `bundle` and `tree`, five repetitions each. It proves that an agent given a feature workflow in either form follows it to completion: 148 sessions pass, all 75 in `bundle` and 73 of 75 in `tree`. The two failures, in `section-composition`'s `nested-composition`, are triaged as misses in the file. The run measured USD 0.67671 over 19 268 512 tokens, so a rerun spends the same budget.

The managed platform configuration the sessions carried is recorded by count and fingerprint, as [Isolation](#isolation) states. [`RUNBOOK.md`](RUNBOOK.md#mvp-proof) states how the run is made.

## Refreshing the baseline

The committed baseline and MVP proof are historical live-run evidence at the revisions their records name. They do not measure the current link-tag preset implementation. The deterministic workflow and scorer tests exercise the current tagged deferrals and dispatched variants; a new paid run requires separate authorization.

Run the default matrix, review its report, then write its cells as the baseline and commit `baseline.json` with the run's `report.md` beside it:

```bash
make eval-diagrams
uv run --project src --frozen python evals/diagram-following/report.py evals/diagram-following/results/<run-id> --write-baseline
cp evals/diagram-following/results/<run-id>/report.md evals/diagram-following/report.md
```

The report written alongside is compared with the baseline being replaced, so it shows what the new baseline moves.
