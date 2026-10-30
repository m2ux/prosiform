# Validation — I05:E06 W01

Run on branch `i05/e06/w01-authoring-rules-in-the` at `3c2b6a58`, cut from `i05/e06/main` at `b81f034e`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf` (pf 0.15.0).

## T1 Guidelines Inspection

`example/work-planner/guidelines.md` read against #376's Proposal. Observes AC1.

| Proposal rule | Stated in |
| --- | --- |
| One home for every binding | Prose › Bindings |
| Inputs and Outputs are links to contracts | Operations › Inputs and Outputs; Artifacts › Operations, Prose API |
| Every value has a contract | Operations › Contracts; Artifacts › Fields |
| Conditions are steps | Operations › Conditions are steps |
| Commands sit in the step that runs them | Operations › Commands in steps, One command |
| Shared conventions are stated once | Prose › Shared conventions |
| Operation structure | Titles › Operation names; Operations › Operation structure; Prose › No spare parts |
| One home per rule | Prose › One home per rule, Index files, File-relative links |
| One subject per file | Prose › One subject per file |
| Each file keeps its title heading | Titles › Title headings |
| Steps keep their sub-section form | Procedure › Step sub-sections, Step anchors |

- **Not authoring rules.** Findings then a sample then the rollout, Fixtures follow, and Boundary govern the epic's delivery order, so the guidelines state none of them.
- **Retired rules absent.** No match in the file for an italicised operation verb, the Input labels rule, a command specification, a Commands section in any section order, a Result line rule, or a per-kind No spare parts rule.
- **Stated once.** Each rule above has one bold lead; the condition-placement sentences formerly in Artifacts › Fields and Step rules, and the three per-kind spare-parts rules, are folded into the one statement.
- **Result.** Pass.

## T2 Links

`make links`: `link check: every reference in 106 document(s) resolved`. Pass.

## T3 Steps

`make steps`: `step check: every procedure in 58 document(s) under example/work-planner/ writes its steps as sub-sections`. Pass.

## T4 Corpus

- **Bundles reached.** Only `modes/revise-mode.md` links `guidelines.md`, through deferred links that carry no content. The usage example `a-mode-and-the-guidelines-it-defers` was regenerated from `example/work-planner` with `pf -o <scratch> modes/revise-mode.md`; the bundle is byte-identical to its `expected/`, so no fixture changes.
- **Anchor sweep.** The sweep over the regenerated bundle reports 8 links, 0 unresolved, 0 suffixed step anchors.
- **Corpus.** `make corpus`: `corpus check: 342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass`.
- **Result.** Pass.

## T5 Repository Checks

`make check` exited 0: ruff `All checks passed!`, format `67 files already formatted`, mypy `no issues found in 66 source files`, tests `1302 passed`, harness `743 passed`, corpus 342 pass, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and steps each passing. Pass.
