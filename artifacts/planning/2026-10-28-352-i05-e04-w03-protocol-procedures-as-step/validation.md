# Validation — I05:E04:W03

The checks the W03 work item names, run on the task branch `i05/e04/w03-protocol-procedures-as-step` at `200071e6ec26a2f801e6fe8d09c4cc7216901561`, cut from `i05/e04/main` at `fa6913e8`. Each ran in the task worktree with `PROSIFORM_BUILD` naming that worktree's own `pf` through `uv run --project <worktree>/src --frozen pf`.

## Inspection

Observes AC3. Result: ✓.

- **Count.** The base held 55 top-level numbered steps across 12 procedures, one `## Procedure` per protocol, and no nested numbered list: change-overview 5, delivery-base-preparation 5, delivery-recording 4, epic-closure 6, epic-integration 5, initiative-publication 6, issue-closure 4, issue-delivery 3, issue-placement 5, review-pull-request 4, task-merge 4, unit-hold 4.
- **Form.** Each became a `### N. Action` sub-section under its `## Procedure`.
- **Nothing left.** `grep -rnE '^\s*[0-9]+\. ' example/work-planner/protocols` returns no line, so no numbered step list and no bold step label remains.
- **Text unchanged.** W02's `verify.py` against `origin/i05/e04/main`, which strips whitespace and reduces each old `N. **Label.**` and new `N. Label` to the lowercased label, finds no difference in any of the twelve files.
- **Prose references.** `epic-closure.md`'s `step 6` and `step 4` stay as written, for W05.

## Anchors

Each step-anchor link in a regenerated bundle lands on its heading. Result: ✓.

- **Method.** A script computes each bundle's heading anchors with ordinal suffixes for repeats, checks that every `](#…)` link resolves to one, and lists each step heading whose anchor takes a suffix.
- **Fixture bundles.** The 13 expected bundles of the plan, advance, hoist and revise fixtures: 0 unresolved of 2,329 fragment links, and no step anchor suffixed.
- **Every entry.** Each of the ten modes and twelve protocols bundled as an entry, 47 bundles in all: 0 unresolved links, and no step anchor suffixed.
- **Repeated titles.** A step heading's anchor carries its number, so `review-pull-request.md`'s `### 3. Publish` (`3-publish`) and plan mode's `### 6. Publish` (`6-publish`) never collide. The full titles repeated across modes and protocols are mode-only (`1. Select`, `3. Read the Evidence`, `6. Report`, `8. Report`), and no bundle carries both of a pair.
- **Step links.** No link in the corpus or a bundle names a step anchor yet; W05 adds them.

## Links

`make links`: exit 0, `link check: every reference in 106 document(s) resolved`. Result: ✓.

## Corpus

`make corpus`: exit 0, `corpus check: 335 fixture(s), 335 pass, 0 fail, 0 awaited, 0 unexpected pass`. Result: ✓.

- Regenerated: the plan and advance fixtures' Sync Mode, Understand Mode, Delivery Recording and Epic Closure bundles, the plan mode bundle, and the hoist fixture's Issue Placement bundle. The revise, hoist mode and artifact-entry bundles reproduce unchanged.
- Each bundle change is the conversion: steps become `####` headings under the bundled protocol's `### Procedure`, and `pf` puts a blank line between an instruction and its bullets.

## Check

`make check`: exit 0. Result: ✓.

- ruff `All checks passed!`; mypy no issues in 64 files; `src` pytest 1281 passed; `checks/tests` 720 passed; corpus 335 pass; smoke, layout, tables, links, vocabulary, invocation, conformance and independence all report ok.
