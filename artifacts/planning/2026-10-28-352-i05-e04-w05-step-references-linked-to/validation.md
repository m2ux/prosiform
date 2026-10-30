# Validation — I05:E04:W05

The checks the W05 work item names, run on the task branch `i05/e04/w05-step-references-linked-to` at `61aa618f`, which merges `i05/e04/main` at `aa826060` into the linking commits `964c7af2` and `44615114`. Each ran in the task worktree with `PROSIFORM_BUILD` naming that worktree's own `pf` through `uv run --project <worktree>/src --frozen pf`.

## Inspection

Observes AC5. Result: ✓.

- **Search.** A scan of every Markdown file under `example/`, outside code blocks and headings, for `step <n>`, `steps <n>`, `the <word> step`, `<word> and <word> steps` and every other line naming a step.
- **Linked.** 54 references in 19 files now name their step's heading and link its anchor, as the work item lists: 35 in modes, 7 in protocols, 8 in artifacts and 4 in the README. Each pair links both steps and each range its first and last.
- **Left.** Every remaining match names no single step: `the following steps` and `the steps below`, a step's own `this step`, Hoist Arising Issue's `the calling step`, generic uses such as `whatever step it is on` and `step order`, and the README's `the step links`, which refers back to the excerpt that follows its link.
- **No numbered list.** The edits replace text within existing bullets and paragraphs, and add no numbered list.

## Links

`make links`: exit 0, `link check: every reference in 106 document(s) resolved`. Result: ✓.

## Anchors

Each fragment link in a bundle lands on its heading. Result: ✓.

- **Method.** W03's anchor script computes each bundle's heading anchors with ordinal suffixes for repeats, checks that every `](#…)` link resolves to one, and lists each step heading whose anchor takes a suffix.
- **Scope.** The 14 expected bundles of the usage-example fixtures, and a bundle of each of the 53 modes, protocols and artifacts as an entry with every bundle its dispatches reach: 93 bundles. Every entry bundled with exit 0 and no diagnostic.
- **Result.** 0 unresolved links, and no step anchor suffixed in any bundle, before and after the merge of `i05/e04/main`.

## Corpus

`make corpus`, run within `make check`: `corpus check: 342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass`. Result: ✓.

- Regenerated: the plan, board-reads and declared-groups fixtures' bundles, 12 in all. The bare-fragment, two-selected-sections and revise fixtures reproduce unchanged, since the sections they bundle carry no step reference.
- Each bundle change is a linked step reference: 63 lines.

## Check

`make check`: exit 0 after the merge of `i05/e04/main`. Result: ✓.

- ruff `All checks passed!`; mypy no issues in 64 files; `src` pytest 1302 passed; `checks/tests` 731 passed; corpus 342 pass; smoke, layout, tables, links, vocabulary, invocation, conformance and independence all report ok.
- Before the merge the same run passed with 1281 and 720 tests and 335 fixtures.

## CI

The repository's `Checks` run on `61aa618f` concluded success ([run 40702767943](https://github.com/m2ux/prosiform/actions/runs/40702767943)). `i05/e04/main` had not moved since `aa826060`, and [#371](https://github.com/m2ux/prosiform/pull/371) merged into it at `37c50a20`. Result: ✓.
