# Validation — I05:E04:W04

The checks the W04 work item names, run on the task branch `i05/e04/w04-artifact-operations-as-step` at `5f5cc8f92dbdcd572b5ff8c0e08433b037f731fc`, cut from `i05/e04/main` at `07574eff`. Each ran in the task worktree with `PROSIFORM_BUILD` naming that worktree's own `pf` through `uv run --project <worktree>/src --frozen pf`.

## Inspection

Observes AC4. Result: ✓.

- **Count.** The base held 423 numbered steps across 118 operations in the 31 artifacts, every one under a `###` operation. No operation had a single step and no step list nested another numbered list.
- **Form.** Each became a `#### N. Action` sub-section under its operation: 423 such headings, matching the count file by file. `delivery-evidence.md`'s `#####` board-reads steps were already sub-sections and stay.
- **Nothing left.** No line opening with a number and a full stop remains outside code fences in `example/work-planner/artifacts/`.
- **Text unchanged.** A verify script against `origin/i05/e04/main` reduces each old `N. instruction` and each new `#### N. Action` heading to its step number, keeps the instruction, and compares every other non-blank line stripped. It finds no difference in any of the 31 files.
- **Unique titles.** No `N. Action` pair repeats across the artifacts.
- **Prose references.** `board-delivery.md`'s `as step 1 does`, `board-queue.md`'s `Continue from step 2`, `repository-graph.md`'s `Repeat steps 1 to 5` and `delivery-branches.md`'s `Repeat steps 1 and 2 once` stay as written, for W05.

## Anchors

Each fragment link in a regenerated bundle lands on its heading. Result: ✓.

- **Method.** W03's anchor script computes each bundle's heading anchors with ordinal suffixes for repeats, checks that every `](#…)` link resolves to one, and lists each step heading whose anchor takes a suffix.
- **Scope.** The 14 expected bundles of the usage-example fixtures, and a bundle of each of the 53 modes, protocols and artifacts as an entry with every bundle its dispatches reach: 93 bundles. Every entry bundled with exit 0 and no diagnostic.
- **Result.** 0 unresolved links, and no step anchor suffixed in any bundle.
- **Depth.** The deepest heading in any bundle is `######`, the board-reads steps under `##### Run Board Reads`.

## Links

`make links`: exit 0, `link check: every reference in 106 document(s) resolved`. Result: ✓.

## Corpus

`make corpus`, run within `make check`: `corpus check: 335 fixture(s), 335 pass, 0 fail, 0 awaited, 0 unexpected pass`. Result: ✓.

- Regenerated: the bare-fragment, board-reads, plan, hoist and two-selected-sections fixtures' bundles, 14 in all. The revise fixture reproduces unchanged.
- Each bundle change is the conversion and the Run Board Reads retitle.

## Check

`make check`: exit 0. Result: ✓.

- ruff `All checks passed!`; mypy no issues in 64 files; `src` pytest 1281 passed; `checks/tests` 720 passed; corpus 335 pass; smoke, layout, tables, links, vocabulary, invocation, conformance and independence all report ok.
