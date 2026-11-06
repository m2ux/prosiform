# Epic Integration Validation

## Revision And Delivery Evidence

- Epic: [I10:E07 #662](https://github.com/m2ux/prosiform/issues/662). All W00-W10 rows and AC1-AC23 are complete in fresh tracker evidence.
- Product integration: [#666](https://github.com/m2ux/prosiform/pull/666), `i10/e07/main` head `3164e8a5c8f695f965a464d8cefef0847cff4a72`, target `main` at `d8265c82e797355a55cf7ec7d921949b4d7eb6c0`.
- Design integration: [#664](https://github.com/m2ux/prosiform/pull/664), `i10/e07/engineering` head `4e076e6082d86aa74374bee6359f411ecaf89714`, target `engineering` inspected at `905b3a86ca2544c7a795410949c22ddf1109e38a`.
- The clean product epic checkout fast-forwards to its remote task-complete head; its current long-lived target is already an ancestor. The design epic merges the current engineering target without conflict. Inspection confirms the target-side commits contain planning/validation records and no design-file delta; the resulting PR diff remains exactly the one design file. No workspace history or branch configuration is merged into product or design.
- Actual product task merges: [665](https://github.com/m2ux/prosiform/pull/665), [667](https://github.com/m2ux/prosiform/pull/667), [668](https://github.com/m2ux/prosiform/pull/668), [669](https://github.com/m2ux/prosiform/pull/669), [670](https://github.com/m2ux/prosiform/pull/670), [671](https://github.com/m2ux/prosiform/pull/671), [672](https://github.com/m2ux/prosiform/pull/672) and [673](https://github.com/m2ux/prosiform/pull/673). Joined W04/W05 and W06/W07 share their recorded merge. Design task merge: [663](https://github.com/m2ux/prosiform/pull/663), plus documented contract amendments preserving the confirmed `--presets` spelling and leading-dash guidance.

## Correct Branch Configuration

Fresh `sync.py` evaluates `--revision origin/workspace`, which resolves to `543e1a830c64d7bccd6a541e6c7db268b19ed842`. `config/branches` there declares engineering, main and workspace. The result reports only the expected two unmerged draft integration PRs, with no incomplete task, criterion, citation, changed-path or target-route finding.

`config/branches` is tooling-workspace configuration. Its absence from historical product/design bases is not a missing product feature and is not repaired by introducing workspace content into those branches. Prior task records' historical unevaluable-sync statements do not describe this corrected integration survey.

## Full Product Check

Command from the clean product epic checkout at exact head `3164e8a5c8f695f965a464d8cefef0847cff4a72`:

```sh
env -u VIRTUAL_ENV make check PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/main/src --frozen pf'
```

Result: **PASS, exit 0**, 2026-11-06. Complete output is [make-check.log](make-check.log). The command uses this checkout's local build, outside the no-network sandbox; it starts no paid evaluation.

- 1,901 source tests pass.
- 1,662 deterministic harness tests pass.
- 537 corpus fixtures pass; zero failure, awaited fixture or unexpected pass.
- Installed-wheel smoke passes from outside the repository, including explicit tagged compilation.
- Lock, lint, formatting and strict typing pass: 472 formatted files and 94 typed source files.
- Layout, tables, online links, vocabulary and invocation checks pass. Every reference in 398 documents resolves; 47 marked contract terms are defined, and 29 documented invocation statements are held to the configured build.
- Conformance and independence pass with zero nonexistent clause declarations and zero declared/reported code disagreements.
- Conformance measures 365 clauses, 67 without fixture coverage, 16 clauses no run can state, three nonbehavioral sections and three installation claims outside corpus observation. Passing is not total behavioral conformance.
- Both product and design target-to-head `git diff --check` pass; the validated product checkout remains clean at the recorded head.
- `make examples` passes at this exact integration head: eight successful examples and the declared refused example, all nine SVGs reproduced byte-identically. [Output](examples.log) records each result.
- GitHub [Checks run 42234869005](https://github.com/m2ux/prosiform/actions/runs/42234869005) succeeds at the exact product integration head, separate from W10's earlier task-head CI.

## Exact Design Check

The updated design head's complete target-to-head diff is read: one design file, 85 additions and 56 deletions. Its content is byte-identical to the product's immutable contract pin `795bbfb67c66b02193f0313138f59f18aa6c5274`.

[design-check.py](design-check.py), run with the product checkout's locked interpreter and this exact design checkout, passes; complete output is [design-check.log](design-check.log).

- All 11 distinct internal destinations resolve.
- Six pre-existing external URLs are not fetched by this offline design instrument; product's online check resolves the pinned contract references.
- All 47 marked contract terms are defined.
- No stale operative heading-selector, multi-entry grammar or deferred heading-mismatch claim matches the explicit scan.
- Compact JSON/SHA-256 example and fenced-block pairing agree.
- Current 537-fixture declaration mapping and code agreement pass against this byte-identical design, with the same 365/67 coverage observations.
- No GitHub check workflow runs on this engineering-only head; there is no required status-check rule in the fetched target rules. Absence is recorded, not called a passing CI result.

## Acceptance Evidence Inspected

- **AC1:** Exact updated design, immutable product pin, W00 clause review, confirmed `--presets` and leading-dash amendments, fresh design instrument and current conformance mapping.
- **AC2-AC3:** Shared tag reader; source/CLI consumer parity, Unicode whitespace/case folding, immutable equivalent sets and the executable parser/guide tests.
- **AC4-AC5:** Inline and resolved reference occurrences in preambles/sections; image/external/Mermaid exclusions; source tests and resource/diagram corpus fixtures.
- **AC6-AC7:** Reference-resolution/substitution transport, destination-owned matching and effective identity; selection and closure tests, source-capture deduplication and equivalent/distinct identity controls.
- **AC8-AC11:** Exactly-one-entry grammar, destination defaults/layering/conflicts, no heading/label selection and actual relative/fragment/quoted/leading-dash guide commands; CLI/entry tests, corpus and installed smoke.
- **AC12-AC16:** Variant scheduling and names, equivalent-request deduplication, cycle/depth/budget behavior, parallel-set destinations, candidate selection checks and injected collision refusal preserving the existing output set.
- **AC17-AC18:** Published deferred titles prescribe later commands; actual output is parsed and recompiled, comparing selected payload with immediate composition independently of headings. W08's 40-case parity instrument and four corpus cases are included in the current full check.
- **AC19-AC20:** Smoke/corpus/renderer/eval callers share the command specification. Tagged deferred and same-destination dispatched workflows and scorer negative controls are inspected; deterministic harness runs, no paid agent sessions.
- **AC21:** Plain guide, invocation, focused guides and checked examples; executable authoring, vocabulary and invocation checks.
- **AC22-AC23:** W10's whole-page claim audit and contract-to-documentation matrix; 1,964 classified documentation paths, 954 claim-observing tests at both task and merged revisions, historical/report/rendering exclusions. Both instruments repeat successfully at the exact integration head: [inventory](inventory-check.log) and [954 observing tests](observing-tests.log), exit 0. The collection count is independently summed from pytest collection. Counts alone are not used as semantic review.

## Target Requirements And Merge Boundary

For both `main` and `engineering`, legacy branch protection returns 404. Active branch rules are nevertheless present: one approving human review, deletion/non-fast-forward/creation/update restrictions, and the repository pull-request rule. No status-check requirement appears in those fetched rules. No approving reviews are present; both REST mergeable states are blocked. Protection 404 is not interpreted as absence of rules.

The user has already confirmed automatic issue closure disabled. No repository setting changes. Both long-lived integration merges remain human-owned; neither merge endpoint is called.

## Readiness Blockers

### Engineering Evidence Freshness

The review-record schema requires the exact full target SHA and publication on `engineering`, with validation against fresh PR metadata before ready, board and user-handoff actions. Publishing this record advances the very target of PR664. A record naming the prepublication target is stale immediately after publication; naming its own containing publication commit creates a self-referential commit identity. Repeating publication does not establish a stable current record under this contract.

No tree-equivalence waiver, hot-fix `base_ref` exception, stale-metadata snapshot or unpublished evidence is substituted for the required epic review. PR664 remains draft and the epic remains In Progress. A procedure-supported evidence location outside the target, or an explicitly authorized freshness-contract decision, is needed before the design handoff can satisfy the current schema.

### Documentation-Only Overview

The exact design-head graph reports 22 changed sections in one file, no execution edges and zero processes. Change Overview requires a graph-derived functional sequence; fabricating a runtime trace for a design-only diff would not meet that requirement. [Graph measurements](graph-measurements.md) records this limitation rather than marking a design overview complete.

## Handoff State

Complete product review and its linked JSON record are published only after the independent scope reviews are reconciled. A passing product record cannot make the epic board eligible while the design integration lacks current complete evidence. Both PRs remain draft until all applicable preparation gates hold; human approval alone is not represented as the remaining gate while these preparation blockers stand.
