# Integration Graph Measurements

## Exact Revisions

- Product head: `3164e8a5c8f695f965a464d8cefef0847cff4a72` in detached `.worktrees/pr/666`.
- Product target: `d8265c82e797355a55cf7ec7d921949b4d7eb6c0` (`main`).
- Design head: `4e076e6082d86aa74374bee6359f411ecaf89714` in detached `.worktrees/pr/664`.
- Design target inspected: `905b3a86ca2544c7a795410949c22ddf1109e38a` (`engineering`).
- GitNexus 1.6.12 indexes were created at those exact heads. Status confirms current indexed commit and all covered file hashes. Generated guidance files were removed/restored to leave detached checkouts clean before final measurements.

## Product Surface

`detect-changes --scope compare --base-ref origin/main` reports 834 changed paths, 781 changed symbols and 245 affected processes. Graph risk is critical, reflecting the broad integration surface; it is not a defect verdict. The index holds 6,525 nodes, 16,444 edges and 468 processes across 524 covered files. Fixture and expected-output paths contribute to the Git diff but need not have executable graph symbols.

The complete MCP change-surface response and all reported ordered process steps are retained beside this record. A context capture is requested for every changed symbol rather than treating the CLI's short display as the complete symbol set.

## Measured Component Edges

- `source.uses` calls `tags.read`.
- `cli.execute` calls `tags.read`, `compiled`, `dispatched_set`, `dispatch.cycle`, `dispatch.analysed`, captured-source revalidation and publication helpers.
- `cli.compiled` calls `closure.bundle_selection`, traversal, governing, composition, naming and per-bundle budget helpers.
- `cli.dispatched_set` calls `cli.compiled` for scheduled effective selections.
- `cli.compose` calls `composition.contributions`, `dispatch.subsections`, `dispatch.anchors`, `dispatch.collisions`, `bundle.assemble` and `candidate.validate`.
- `cli.traverse` calls source occurrence/region helpers and local selection/governing/resolution helpers.
- `workflow.activated` calls the nested `compiled_walk.activate` callback, whose outgoing calls include `compile_reference`, `effective_presets` and `entry_bundle`.

The overview's component areas group these measured responsibilities; edges correspond to measured calls, not directory adjacency.

## Ordered Functional Traces

GitNexus Cypher returns zero-based stored source coordinates; CLI context/query displays one-based coordinates. Published code links use the latter.

### Deferred Activation

Process `proc_129_activated`:

1. `workflow.activated`, `workflow.py:1314-1333`.
2. `compiled_walk.activate`, `workflow.py:1472-1485`.
3. `compile_reference`, `workflow.py:1150-1165`.

Related processes `proc_130_activated` and `proc_131_activated` share the first two steps and terminate at `effective_presets` and `entry_bundle`, respectively. These are separate ordered traces; their relative order is not invented from the graph.

### Selected Dispatch Identity

Process `proc_212_dispatched_file`:

1. `compiled.dispatched_file`, `cli.py:3603-3609`.
2. `closure.bundle_selection`, `closure.py:209-217`.
3. `closure.matching_presets`, `closure.py:180-192`.

Process `proc_98_compose` separately orders `compose`, `placement`, `pair` and `matching_presets`. Both traces identify matching as destination-owned and supply the selected-identity functional diagram.

### Invalid Fault Configuration

Process `proc_146_execute`:

1. `cli.execute`, `cli.py:3780-3876`.
2. `cli.conformance_fault`, `cli.py:1366-1382`.
3. `cli.usage_failure`, `cli.py:375-391`.

This is a refusal branch involving configured conformance faults. It establishes no total ordering of all command-parser or successful compiler operations.

### Rewritten Title Reader

Process `proc_138_rewrite`:

1. `bundle.rewrite`, `bundle.py:552-656`.
2. `rewrite.destinations`, `rewrite.py:448-470`.
3. `tags.read`, `tags.py:11-17`.

## Design Surface And Overview Constraint

The clean exact-head design comparison reports one changed file, 22 changed sections and zero affected execution processes. The changed path is `artifacts/planning/2026-10-17-prosiform-v1/design.md`, 85 additions and 56 deletions. Contexts for Presets, Guide and Automatic output names have no incoming/outgoing execution relationships or containing processes.

The change-overview procedure requires a measured structural diagram and a measured ordered functional diagram for each integration PR. There is no measured execution flow in this documentation-only design change. A manually invented sequence would violate the procedure's graph provenance requirement. The design overview is therefore explicitly incomplete, not presented as a completed architecture overview.

## Completeness Boundaries

- Process discovery reports 279 of 479 candidate entry points not ranked, 696 skipped callees, 30 budget-cut walks and one depth-capped trace. No absent process is interpreted as proof of absent behavior.
- The `tags.read` context is a lower bound: two receiver-typing call sites were unresolved. Its known source/CLI callers are confirmed in source and shared-reader regression tests.
- The index identifies one cross-language `stdout` property boundary.
- Every response is checked against exact indexed head/status. This CLI version omits a staleness envelope from some response formats; exact-head status and content hashes are retained rather than claiming that an absent envelope asserts freshness.
- Complete diff/definition/caller review and executable regression evidence complement the bounded graph measurements.
