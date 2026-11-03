# Checks

Every check is a named `make` command. Continuous integration runs these same names, so a check cannot pass on a working copy and be missing remotely.

## Running the Checks

One command runs every check in the sections below, from [Python](#python) to [The Contract](#the-contract).

| Command | Runs |
| --- | --- |
| `make check` | Every check in the order the [`Makefile`](Makefile) lists them, stopping at the first failure. |

```bash
make check
```

Three commands sit outside it, because each needs a tool or a budget the others do not. See [Outside `make check`](#outside-make-check).

## What Each Check Asserts

### Python

| Command | Asserts |
| --- | --- |
| `make lock-check` | The lockfile matches the dependencies the project definition declares. |
| `make lint` | The repository's Python has no lint errors. |
| `make format-check` | That Python is formatted as the declared configuration formats it. |
| `make typecheck` | That Python type checks in strict mode. |
| `make test` | The Python build's test suite passes. A run that collects no test fails. |

### The Corpus

| Command | Asserts |
| --- | --- |
| `make harness` | The corpus, its runner and the diagram-following eval are well formed. See [The harness](#the-harness). |
| `make corpus` | Every fixture in the corpus, run against the build under test, produces the result its manifest declares, and every fixture source declares its settings in a preset. |
| `make smoke` | The build installs into an environment, and its entry point bundles a declaring reference. |

#### The Harness

`make harness` checks the corpus and the tools around it, not the build.

- **Fixtures.** Every fixture matches the [manifest schema](fixtures/README.md).
- **Diagnostic codes.** Each catalogue of diagnostic codes is exactly the set the design declares.
- **Runner.** The runner decides a fixture's result from its manifest and files alone.
- **Check readings.** Each check parses its own input correctly on cases written to be misread, and the heading-slug rule generates the anchors GitHub generated for a captured document.
- **Authoring guidance.** Each `pf` command the [invocation guide](invocation.md) and the [README](README.md) show names a file this repository holds and passes only declared options, and both recommend hyphens rather than underscores in names.
- **Diagram-following corpus.** The [corpus](evals/diagram-following/workflow.py) bundles cleanly in every form, reporting only the warnings a workflow declares, and its forms differ only in their transitions. Each scenario's path is the walk through the diagram that its inputs determine, and the walk the bundle `pf` compiles from the diagram form states.
- **Scorer.** The [scorer](evals/diagram-following/score.py) passes a run that walks that path with every action done. It classifies each failing run by how it departs from the path.
- **Eval runner.** The [runner](evals/diagram-following/run.py) is driven by a stub agent, and:
  - starts each session in a fresh workspace holding its form and inputs;
  - refuses a run, before its first session, when the config directory installs a plugin at a scope other than managed, enables one through unsigned remote settings, or declares a hook in its settings file, and records the managed configuration as counts and a fingerprint, naming none of it;
  - fails a run when a session carried context the runner did not supply;
  - records each session's transcript, usage, cost and verdict;
  - records a run whose every started session errored as refused, with the agent's own reason, whether or not its budget stopped it;
  - stops before the recorded tokens would pass the token budget.
- **Report.** The [report](evals/diagram-following/report.py) reads recorded results. It gives the pass rate and failure classes per model, form and scenario, and each one's difference from a baseline, the run's summed cost, and each failing session with the disposition its triage gave it. For a refused run it names the run's state and reason in place of a pass rate, and it writes a baseline only from a run that measured a cell.

#### Corpus and Smoke Details

- **Awaiting fixtures.** A fixture that declares work a later epic delivers is reported as awaiting it. One that already meets its manifest while awaiting fails.
- **No build, no pass.** `make corpus` fails when no build is configured. See [Choosing the build under test](#choosing-the-build-under-test).
- **Smoke location.** `make smoke` resolves the reference by name from a directory unrelated to this repository.

### Documentation

| Command | Asserts |
| --- | --- |
| `make layout` | Each of the four trees, `fixtures/`, `src/`, `docs/` and `evals/`, holds a tracked file. |
| `make tables` | The command and dependency tables in the documentation name every target the [`Makefile`](Makefile) declares and every dependency [`src/pyproject.toml`](src/README.md) declares, and nothing else. |
| `make links` | Every link in every document in this repository resolves, except those in the fixture corpus. |
| `make vocabulary` | The [glossary](docs/glossary.md) defines every contract term the design marks. |
| `make invocation` | The documented invocation names every argument, budget and exit status the build under test reports for itself, and nothing else, each reproducing that build's own help output, and it names the profile `-v` reports and carries the statements the contract requires of it. |

### The Contract

These two checks keep the corpus tied to the design rather than to any one build.

| Command | Asserts |
| --- | --- |
| `make conformance` | Every clause, code and exit status in the design is accounted for by fixtures, or recorded as out of their reach. See [Conformance](#conformance). |
| `make independence` | No fixture declaration and no line of the conformance report names an implementation. See [Independence](#independence). |

#### Conformance

`make conformance` reads the design, the corpus, and the codes the build under test reports for itself. Its coverage and its comparison therefore come from the contract and the build together, never from either alone.

- **Clauses.**
  - Each behavioural clause in the design lists the fixtures that exercise it.
  - A clause no fixture reaches is listed as uncovered.
  - A clause no source tree and invocation can express is recorded as unfixturable, with the reason and what states it instead.
  - A design section that states no behaviour is declared as such and carries no clause.
- **Codes and exit statuses.**
  - Each error code, warning code and exit status the contract declares is listed with the fixtures that reach it.
  - One that only an awaiting fixture declares is named unfixturable, with the work it awaits.
  - Each installation claim that no corpus run observes is listed as unfixturable, with the reason it is out of reach and the smoke-run property that would observe it.
- **Build agreement.** The codes the build under test reports are exactly the codes the contract declares.
- **Needs a build.** It fails when no build is configured.

#### Independence

`make independence` reads the same three inputs as conformance, plus the report between them. It keeps the corpus bound to the behaviour the design states, not to the build that happens to sit beside it.

- **The rule.** Any term written the way a type, function, field, constant, package or language is written must be one the contract names.
- **Where contract names come from.** The design's prose and clause names, the terms the [glossary](docs/glossary.md) defines, and the interface the contract declares.
- **Needs a build.** It renders the conformance report, so it fails when no build is configured.

## Outside `make check`

| Command | Asserts |
| --- | --- |
| `make render` | Each diagram link form the corpus bundles renders under Mermaid as one followable link per link line. See [Rendering](#rendering). |
| `make examples` | Each case in [`scripts/examples.json`](scripts/examples.json) runs against the build, and its drawing under [`docs/images/`](docs/images/) shows the files the run read beside the bundles it wrote. |
| `make eval-diagrams` | Real agents follow the diagram-following workflows over the default matrix, and the report gives each cell's pass rate. See [The Diagram-Following Eval](#the-diagram-following-eval). |

### Rendering

- **What a link must open.** Each link opens the heading of the group its fixture's bundle rewrote it to. That is an anchor in the drawing or, for a Gantt task, the URL a click on it opens in a running page.
- **How it is drawn.** It draws each diagram-link fixture's expected bundle with [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) 11.16.0, which drives a headless Chromium, and reads the anchors in the drawings.
- **Gantt diagrams.** A Gantt diagram binds its links as click handlers only when the page runs. So a Gantt fixture's bundle is loaded in a page, using the Mermaid and Chromium that mermaid-cli ships, and each clickable task is clicked to record the URL it opens.
- **Why it is outside.** Neither tool is a dependency of the build. The check fails when mermaid-cli is not configured.

### Example Drawings

`make examples` re-renders the pictures on the architecture pages. A case that stops producing its declared output is therefore drawn as it now behaves.

### The Diagram-Following Eval

`make eval-diagrams` runs the [diagram-following eval](evals/diagram-following/README.md), which states its budget, harness and options. It starts paid agent sessions, so no check depends on it. Instead, [the harness](#the-harness) holds its runner, scorer and report against a stub agent and recorded results.

## Setup

### Tool Environments

- **Pinned by the lockfile.** [`src/uv.lock`](src/README.md) pins the tools for `make lock-check`, `make lint`, `make format-check`, `make typecheck`, `make test`, `make harness`, `make corpus`, `make examples` and `make eval-diagrams`.
- **Same environment.** `make invocation`, `make conformance` and `make independence` read the corpus through the same manifest reader and the build through the same runner, so they run from that environment too.
- **Standard library only.** `make smoke`, `make layout`, `make tables`, `make links`, `make vocabulary` and `make render` are standard-library scripts in [`checks/`](checks/README.md), run under `python3` directly.

### Network Access

- `make smoke` builds and installs the wheel through `uv`, so it needs network access for the dependencies the wheel declares.
- `make links` reaches addresses outside this repository, so it needs network access and GitHub credentials.

### Choosing the Build Under Test

`make corpus`, `make invocation`, `make conformance` and `make independence` run whichever build configuration names. They never pick one themselves. So one corpus, one documented invocation and one declared surface bind every implementation of the contract.

`PROSIFORM_BUILD` holds that build's command line, split the way a shell splits one. A corpus run resolves it from the fixture's own directory.

```bash
export PROSIFORM_BUILD="uv run --project $PWD/src --frozen pf"
```

There is no default and no fallback. With nothing configured, the run fails rather than skipping the corpus, because a skipped corpus run inside a passing suite says nothing.

### Configuring mermaid-cli

`MERMAID_CLI` holds the mermaid-cli command line for `make render`, with no default. Its last word names `mmdc`, and the click program runs as `node` under the words before it.

```bash
export MERMAID_CLI="npx -p @mermaid-js/mermaid-cli@11.16.0 mmdc"
```
