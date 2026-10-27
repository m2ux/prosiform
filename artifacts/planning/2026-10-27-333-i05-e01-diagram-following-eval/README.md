# I05:E01 Diagram Following — October 2026

> Epic planning · Created 2026-10-27

## Executive Summary

This record holds the plan for I05:E01: a repeatable evaluation of how well an agent, told to interpret a bundled Mermaid diagram as a workflow and follow it to completion, does so. It is the question the Mermaid Links epic raises once a diagram's linked sections reach the bundle.

The eval runs synthetic workflows of graded difficulty in three forms — the `pf` bundle, the unbundled source tree, and a bundled prose form with no diagram — through real headless agent sessions, scores each session's path deterministically, and compares a report against a committed baseline. Paid runs are their own command; `make check` exercises everything against a stub agent.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | The workflow corpus, its three forms and its scenarios |
| [W02 work item](w02.md) | The trace scorer and its failure classes |
| [W03 work item](w03.md) | The headless agent runner and its spending cap |
| [W04 work item](w04.md) | The report, baseline comparison and eval command |
| [W05 work item](w05.md) | The first baseline from the default matrix |

## Decisions

- **Repeatable eval, not a one-off.** It lives in prosiform under `evals/diagram-following/`.
- **Real agent sessions.** `claude -p --bare` in a fresh workspace per session; the CLI is already installed, so the runner adds no dependency.
- **Three forms.** Bundle (subject), source tree (does bundling help) and bundled prose (does the diagram help).
- **Default matrix.** `claude-haiku-5-5` and `claude-sonnet-5-5`, five repetitions; both configurable.
- **Synthetic workflows first.** Linear, branching, and branching with a loop and a nested link; a realistic workflow is a later row.
- **Report and committed baseline.** No pass threshold until the baseline shows what is realistic.
- **No initiative edge on E00.** Only W01 consumes E00's work, through E00 W02; the E01 base is cut from `main` once E00 has merged.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Prior epic | [I05:E00 Mermaid Links](https://github.com/m2ux/prosiform/issues/326) |
