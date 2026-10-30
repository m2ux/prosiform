# Validation — I05:E06 W11

Run on branch `i05/e06/w11-shared-guidelines-under-the` at `89dcc837`, cut from `i05/e06/main` at `1a102cdb`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`.

## T1 Guidelines Inspection

`example/guidelines.md` read whole against `example/work-planner/guidelines.md` and `example/work-planner/conventions.md`, rule by rule, against AC14 and the [replacement table](w11.md#rules-and-replacements). Observes AC14.

- **Commands.**  The Commands section states Commands in steps: a command sits inline, in an unindented fenced block, in the step that runs it, with no Commands section, and a command several procedures run is written in each. One spec per operation, the catalog, the caller and two-owner rules, Spec layout and Named by link are gone. Prose runs nothing stays, as a statement of its own.
- **Procedure files.**  Top-level sections are Procedure, Reference and Rules. The definition of a procedure sits in Procedure files and no longer links Commands. A single-step procedure carries no heading, as the work-planner Step sub-sections rule states. A file in a directory whose sections a skill's own guidelines state takes those sections, so the work-planner modes, protocols and artifacts keep their own.
- **SKILL.md structure.**  The Commands entry is removed; Commands in steps settles it.
- **One home per rule.**  The home is the contract or outcome a rule constrains, the step it binds, the rules or conventions file when it binds every mode, or the guidelines when it governs how a file is written; every other file links it. This is the set the work-planner rule names.
- **Surviving references.**  Prerequisite citation places conventions ahead of the procedures they govern; Applicability selects a check before reading the steps that run it. A search for `spec`, `specification` and `Commands section` finds only the rule that no file has one.
- **Bindings and conventions.**  No repository, label, board field or per-deployment limit; neither helper invocation nor write confirmation is restated.
- **Outside names.**  The Files › Shared entry, the Prerequisite citation example and the Changes › Verified entry name no path or file outside this repository.
- **State or link.**  Every rule is stated generically, as [State or Link](w11.md#state-or-link) records.
- **Result.**  Pass. No rule of `example/guidelines.md` contradicts the work-planner guidelines or conventions.

## T2 Anchor Sweep

The one usage example whose bundle links the shared guidelines, Revise mode's, was regenerated from `example/work-planner` with `pf -o <scratch> modes/revise-mode.md`. The shared guidelines resolve outside the bundle's root and contribute no content, so the bundle is byte-identical to `expected/` and nothing was copied; its `../../guidelines.md#commands` link keeps a heading to name. The sweep over the regenerated bundle and every `expected/` bundle under `fixtures/usage-example/` (15 bundles) reports `unresolved links: 0` and 0 suffixed step anchors. Pass.

## T3 Links

`make links`: `link check: every reference in 107 document(s) resolved`. Pass.

## T4 Steps

`make steps`: `step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections`. Pass.

## T5 Corpus

`make corpus`, run within `make check`: `corpus check: 342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass`. Pass.

## T6 Repository Checks

`make check` exited 0: ruff `All checks passed!`, format `69 files already formatted`, mypy `no issues found in 68 source files`, tests `1302 passed`, harness `758 passed`, corpus 342 pass, links and steps passing. Pass.

## T7 Authoring Check

`make authoring` before and after: 431 findings each, by area unchanged (modes 0/1/3/0, artifacts 244/18/165/0). The check scans `example/work-planner/` only, so the shared file moves no count. Pass.
