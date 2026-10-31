# Checks

Every check is a named command. Continuous integration runs these same names, so a check cannot hold on a working copy and be absent remotely.

```bash
make check
```

| Command | Asserts |
| --- | --- |
| `make lock-check` | The lockfile describes the dependency list the project definition declares. |
| `make lint` | The repository's Python carries no lint error. |
| `make format-check` | That same Python is formatted as the declared configuration formats it. |
| `make typecheck` | That same Python type checks in strict mode. |
| `make test` | The Python build's suite passes. A run that collects no test fails. |
| `make harness` | Every fixture the corpus holds matches the [manifest schema](fixtures/README.md), each catalogue of diagnostic codes is the set the design declares, the runner decides a fixture from its manifest and files alone, and the [diagram-following corpus](evals/diagram-following/workflow.py) bundles cleanly in every form, its forms differ only in their transitions, each scenario's path is the walk of the diagram its inputs determine, its [scorer](evals/diagram-following/score.py) passes a run that walks that path with every action done and classifies each failing run by how it departs, and its [runner](evals/diagram-following/run.py), driving a stub agent, starts each session in a fresh workspace of its form and inputs, refuses a run whose config directory installs a plugin, enables one, or declares a hook in its settings file, before its first session, fails a run one of whose sessions carried context it did not supply, records each session's transcript, usage, cost and verdict, records a run every session of which errored as refused with the agent's own reason, and stops before its recorded cost would pass its spending cap, and its [report](evals/diagram-following/report.py), over recorded results, gives the pass rate and failure classes per model, form and scenario and each one's difference from a baseline, and names a refused run's state and reason in place of any pass rate. |
| `make authoring` | Every document in the [work-planner example](example/work-planner/SKILL.md) meets the authoring rules its [guidelines](example/work-planner/guidelines.md) state: an operation states its Inputs and Outputs as `None` or a comma-separated list of links to contract sections on one line ahead of its first step, a shell command sits in an unindented fenced block within the step that runs it, no file carries a heading titled `Commands`, and a cross-file link is written from the file that holds it. It reports each departure by file and line, grouped by area. |
| `make corpus` | Every fixture the corpus holds, run against the build under test, produces the result its manifest declares. A fixture declaring work a later epic delivers is reported as awaiting it; one that meets its manifest while awaiting fails, as does a run with no build configured. |
| `make smoke` | The build installs into an environment and its entry point bundles a reference from a source root, resolved by name from a directory unrelated to this repository. |
| `make layout` | Each of the four trees holds a tracked file. |
| `make tables` | The command and dependency tables in the documentation name every target the [`Makefile`](Makefile) declares and every dependency [`src/pyproject.toml`](src/README.md) declares, and nothing besides. |
| `make links` | Every reference every document in this repository carries resolves, the fixture corpus excepted. |
| `make vocabulary` | The [glossary](docs/glossary.md) defines every contract term the design marks. |
| `make invocation` | The documented invocation names every argument and exit status the build under test reports for itself, and nothing besides, each reproducing that build's own help output. |
| `make conformance` | Each behavioural clause of the design carries the fixtures exercising it, each clause no fixture reaches is listed as uncovered, each clause no source tree and invocation can state is recorded as unfixturable with the reason and what states it instead, each section of the design that states no behaviour is declared as such and carries no clause, and each error code, warning code and exit status the contract declares is listed with the fixtures reaching it, one only an awaiting fixture declares named unfixturable with the work it awaits, each installation claim no run of the corpus observes listed as unfixturable with the reason it is unreachable and the smoke-run property that would observe it, and the codes the build under test reports for itself are exactly the codes the contract declares. It fails without a build configured. |
| `make independence` | Every fixture declaration and every line of the conformance report names no implementation: a term written the way a type, a function, a field, a constant, a package or a language is written is one the contract names, whether in the design's prose and clause names, the terms the [glossary](docs/glossary.md) defines, the interface the contract declares, or the headings the [example tree](example/work-planner/SKILL.md) carries. It renders the conformance report, so it fails without a build configured. |
| `make steps` | Every procedure in the [work-planner example](example/work-planner/SKILL.md) writes its steps as `N. Action` headings one level below it, each unique in its document, and carries no numbered list outside a code block. |
| `make check` | All of the above, in the order the [`Makefile`](Makefile) declares, stopping at the first failure. |
| `make render` | Each diagram link form the corpus bundles renders, under Mermaid, as one followable link per link line, opening the heading of the group its fixture's bundle rewrote it to: an anchor in the drawing, or, for a Gantt task, the URL a click on it opens in a running page. It fails without mermaid-cli configured, and `make check` leaves it out. |
| `make examples` | Each case in [`scripts/examples.json`](scripts/examples.json) runs against the build, and its drawing under [`docs/images/`](docs/images/) shows the files the run read beside the bundles it wrote. It re-renders the architecture pages' pictures, so a case that stops producing its declared output is drawn as it now behaves. |

The tooling the checks that read Python and the corpus call — `make lock-check`, `make lint`, `make format-check`, `make typecheck`, `make test`, `make harness` and `make corpus` — is pinned by [`src/uv.lock`](src/README.md), and `make invocation`, `make conformance` and `make independence` read the corpus through the same manifest reader and the build through the same runner, so they run from that environment too; `make smoke`, `make layout`, `make tables`, `make links`, `make vocabulary`, `make steps` and `make authoring` are standard-library scripts in [`checks/`](checks/README.md). `make smoke` builds and installs the wheel through `uv` and needs network access for the dependencies the wheel declares. `make links` reaches addresses outside this repository, so it needs network access and GitHub credentials.

`make conformance` reads the design, the corpus and the codes the build under test reports for itself, so the coverage it reports and the comparison it makes are both read from the contract and the build rather than from either alone. `make independence` reads those same three and the report between them, and holds what the corpus binds to the behaviour the design states rather than to the build that happens to be written beside it. `make corpus`, `make invocation`, `make conformance` and `make independence` run a build named by configuration rather than one they choose, so one corpus, one documented invocation and one declared surface bind every implementation of the contract. `PROSIFORM_BUILD` holds that build's command line, split as a shell splits one, and a corpus run resolves it from the fixture's own directory:

```bash
export PROSIFORM_BUILD="uv run --project $PWD/src --frozen pf"
```

There is no default and no fallback: with nothing configured the run fails rather than passing over the corpus, because a corpus run that skips sits inside a passing suite saying nothing.

The [diagram-following eval](evals/diagram-following/README.md) itself is outside `make check`: `make eval-diagrams` starts paid agent sessions, so no check depends on it, and the checks hold its runner, scorer and report against a stub agent and recorded results instead.

`make render` draws each diagram-link fixture's expected bundle with [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) 11.16.0, which drives a headless Chromium, and reads the anchors the drawings carry. A Gantt diagram binds its links as click handlers when the page runs, so a Gantt fixture's bundle is loaded in a page instead, with the Mermaid and the Chromium mermaid-cli ships, and each clickable task is clicked to record the URL it opens. Neither is a dependency of the build, so the check sits outside `make check`, and `MERMAID_CLI` holds the mermaid-cli command line, with no default. Its last word names `mmdc`, and the click program runs as `node` under the words before it:

```bash
export MERMAID_CLI="npx -p @mermaid-js/mermaid-cli@11.16.0 mmdc"
```
