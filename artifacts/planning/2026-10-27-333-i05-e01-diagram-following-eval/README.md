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
| [W06 work item](w06.md) | The linked form, whose decisions name the rule stating the branch's label |
| [W07 work item](w07.md) | The `errored` class for a session that entered no state |

## Decisions

- **Repeatable eval, not a one-off.** It lives in prosiform under `evals/diagram-following/`.
- **Real agent sessions.** `claude -p --bare` in a fresh workspace per session; the CLI is already installed, so the runner adds no dependency.
- **Three forms.** Bundle (subject), source tree (does bundling help) and bundled prose (does the diagram help).
- **Default matrix.** `claude-haiku-5-5` and `claude-sonnet-5-5`, five repetitions; both configurable.
- **Synthetic workflows first.** Linear, branching, and branching with a loop and a nested link; a realistic workflow is a later row.
- **Report and committed baseline.** No pass threshold until the baseline shows what is realistic.
- **No initiative edge on E00.** Only W01 consumes E00's work, through E00 W02; the E01 base is cut from `main` once E00 has merged.

## Base Updates

- **2026-10-28, main merged into `i05/e01/main` at `22ae0f2e`.** The base predated I05:E02 and I05:E03; merge `780fea54` brought them in, and `22ae0f2e` then brought #375 and #372, keeping `make steps` beside `make render` and `make eval-diagrams`. Conflicts in `.gitignore`, `Makefile` and `checks.md` kept both sides: the eval results ignore beside the fixture bundle exception, and `make render` beside `make eval-diagrams`.
  - `4faf0120` bundles each eval form with `pf -o <scratch folder>` and reads `workflow.bundles/workflow.bundle.md`, since pf skill-markdown-v4 refuses `-o -`. The corpus test holds that bundle to be the whole set: no form dispatches.
  - `dcfc0c8d` refuses a run whose `--budget-usd` is less than its sessions × `--session-budget-usd`. A calibration of 9 Haiku sessions at `--budget-usd 0.50` had started one and skipped eight, each reserving the USD 0.50 cap against a measured USD 0.003. The default cap stays at USD 0.50, since Sonnet's per-session cost is unmeasured and a session that reaches its cap is ended.
  - Verified at `22ae0f2e` with the worktree's pf 0.15.0: `make check` and CI pass, and a stub-agent run over every workflow and form starts and passes 15 of 15. Review PR #353's Changes and References record both commits.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Prior epic | [I05:E00 Mermaid Links](https://github.com/m2ux/prosiform/issues/326) |
