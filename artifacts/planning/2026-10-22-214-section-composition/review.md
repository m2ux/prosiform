# Requirement Trace

The user selected Field Refinement #20 and requested this epic next. The source is issue #214, fetched 2026-10-22. Each original criterion retains its number and wording in the epic.

| Goal | Initiative Criteria | Epic Criteria | Delivering Task | Source |
| --- | --- | --- | --- | --- |
| Declared composition contract | AC3 | AC17 | W01 | Initiative design-first invariant |
| Decoded inline occurrence recognition | AC11 | AC1, AC2 | W02 | #214 AC1, AC2 |
| Scoped section composition | AC11 | AC3, AC4, AC15 | W03 | #214 AC3, AC4, AC15 |
| Structural and target diagnostics | AC11 | AC9, AC16 | W04 | #214 AC9, AC16 |
| Source-aware repeated contributions | AC11 | AC5, AC6 | W05 | #214 AC5, AC6 |
| Bounded recursive expansion | AC11 | AC7, AC8 | W06 | #214 AC7, AC8 |
| Deferred destination retention | AC11 | AC10, AC11 | W07 | #214 AC10, AC11 |
| Selected deferred activation | AC11 | AC12 | W08 | #214 AC12 |
| Complete-output failure handling | AC11 | AC13 | W09 | #214 AC13 |
| Authoring grammar and worked examples | AC11 | AC14 | W10 | #214 AC14 |

## Review

- Scope: the parent explicitly permits compiled section composition; ontology inference, workflow execution and sentence-level substitution remain excluded.
- Source coverage: the 16 source criteria each have exactly one delivering task; the design-first criterion preserves the parent initiative invariant.
- Task grain: each row covers at most three criteria and has its tests in the same delivery. Compiler tasks extend the existing `src/prosiform` package; specification and documentation have separate rows.
- Dependencies: each row consumes the preceding stage's validated representation or end-to-end behavior. The longest chain is W01 through W10. There are no independent task pairs or Joins.
- Freeze: no pull request in the fetched full history names the freeze prefix. Its issue identity is retained as #23, its prefix becomes E05, and its tagging row consumes E04:W10. A whole-epic prerequisite is not asserted because freeze deferral work can start independently.
- Queue: priority 5 places this epic ahead of the existing highest priority 4. No whole-epic prerequisite blocks its design task. The user explicitly chose this next; peer priorities are retained.
- Consumers: the authoring docs, compiler help, README, corpus trace and future production-compiler contract must describe occurrence expansion rather than unconditional source deduplication. The specification freeze captures the completed contract.
- Current implementation: main is pinned at `cd3d8e635b8db500ceb7230b26209bdd37f637da`. `cli.py` traversal deduplicates `(path, fragment)` targets and deferred destinations; `confirm` checks destination existence. `bundle.py` rewrites deferred destinations but retains no owning scope for a later activation. These are design inputs, not evidence that the proposed feature exists.
- Deferred activation: the design task specifies a source-based recompilation interface with explicit occurrence selection, complete ancestry and stable destination context. This avoids accepting generated bundles as source. Its executable staged examples are required before compiler work starts.
- Resource safety: the design task declares a positive materialization limit and incremental output accounting. Distinct-source budgets remain separately meaningful. Boundary and multiplicative fixtures accompany the expansion task.
- Existing parent requirements: AC1–AC10 and their delivering rows are preserved; the new row also serves AC3. The original pinned v1 design remains the baseline; issue #214 explicitly supplies its composition extension.

## Planning Checklist

- [x] Read the originating issue and current initiative.
- [x] Record placement and next-epic decisions.
- [x] Draft tasks and trace every source criterion.
- [x] Validate bodies and dependencies.
- [x] Publish epic, parent scope, freeze edge and Ready placement.
- [x] Read back published records and prepare planning evidence for commit.

## Validation Evidence

- Epic, parent and freeze body checks report no content or metadata decisions; mechanical formatting was applied.
- The full initiative graph reports no dependency problems. Its longest chain has 11 steps, E04:W01 through E04:W10 to E05:W02. Existing peer Joins and numbering advisories are outside this epic.
- The parent design permalink at d45c7f0 returns HTTP 404. Design and decisions references use engineering revision 3ff3689.
- REST board item listing returned an empty array; gh project item-list supplied the actual inventory. Board writes and readback use that working API route.

## Published State

- Epic #215: I01:E04, priority 5, Ready on Project 18, assigned to m2ux. Direct GraphQL item read confirms status and assignment; the list snapshot lagged publication.
- Initiative #20: composition scope and AC11, E04 coverage and source reference.
- Freeze #23: I01:E05; tagging consumes E04:W10.
- All three saved bodies exactly match the reviewed local bodies. Each saved-body format check reports 0 fixed, 0 to apply and 0 to decide.
- All 16 originating criteria remain verbatim. AC17 holds the parent design-first requirement.
- The new epic dependency check includes all ten work-item component declarations and reports no dependency, Joins, numbering or contention findings. Priority 5 is the user-selected ordering, not the isolated graph default.
- No compiler code was changed or feature tests reported as run. The specification task is the next delivery unit.
