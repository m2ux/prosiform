# Validation — I05:E06 W04

Run on branch `i05/e06/w04-shared-conventions-stated-once` at `56494cf6`, cut from `i05/e06/main` at `500aca85`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`.

## T1 Conventions Inspection

`example/work-planner/` inspected against AC4 and the [restatement table](w04.md#restatements-and-links). Observes AC4.

- **One home each.**  `conventions.md` states Helper invocation and Write confirmation, each once.
- **Every helper command links.**  The 21 helper commands, 19 in artifacts and two in Revise mode, each carry `Runs as [Helper invocation](../conventions.md) states.` ahead of the command. A search for `scripts/sbx` outside fenced commands finds only `conventions.md` and the Sandbox dependency in `SKILL.md`.
- **Every write re-read links.**  The 14 steps that re-read or confirm a write, in `board.md`, `board-delivery.md`, `board-queue.md`, `issue.md`, `issue-body.md` and `pull-request.md`, link Write confirmation. The three steps that repeat a board write keep their item-list lag condition beside the link.
- **Restatements removed.**  The guidelines' Local scripts and Bodies rules become one Helpers and bodies rule linking both entries; Check Dependencies' absolute-path bullet is removed; Commit Planning Record links Bodies.
- **Review bar.**  Neither rule is stated outside `conventions.md`.
- **Confidentiality.**  `conventions.md` names nothing outside this repository: the Bodies example is removed and the Example values line names a theme board by role.
- **Result.**  Pass.

## T2 Anchor Sweep

All six usage examples whose bundles carry a changed file were regenerated from `example/work-planner` with `pf -o <scratch> <entry>` and copied into `expected/`: Advance, Plan, Hoist and Revise modes, the bare fragment and the two selected sections. The sweep over every `expected/` bundle under `fixtures/usage-example/` (15 bundles) reports `unresolved links: 0` and 0 suffixed step anchors. Pass.

## T3 Links

`make links`: `link check: every reference in 107 document(s) resolved`. Pass.

## T4 Steps

`make steps`: `step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections`. Pass.

## T5 Corpus

- **Bundles reached.**  Section-selected bundles that reach a helper command now carry Conventions as a whole document; the others change where the conventions and linking steps changed.
- **Corpus.**  `make corpus`, run within `make check`: `corpus check: 342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass`.
- **Result.**  Pass.

## T6 Repository Checks

`make check` exited 0: ruff `All checks passed!`, format `69 files already formatted`, mypy `no issues found in 68 source files`, tests `1302 passed`, harness `758 passed`, corpus 342 pass, links and steps passing. Pass.

## T7 Authoring Check

`make authoring` before and after: 431 findings each, by area unchanged (modes 0/1/3/0, artifacts 244/18/165/0). Only line numbers shift, from the inserted link lines. Pass.
