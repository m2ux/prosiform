---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Repository Graph

The indexed symbols, relationships and ordered flows for a repository revision.

## Operations

### Measure Repository Change

Current graph evidence for the supplied change.

**Inputs:** [Worktree](#revision), [Verified head](#revision), [Base branch](#revision)

**Outputs:** [Changed symbols](#changed-symbols), [Symbol relationships](#symbol-relationships), [Flow traces](#flow-traces)

#### 1. Check the Graph Index Status

Read the graph index status from the supplied repository worktree. Run every command in this operation from that worktree and compare freshness with the supplied verified head.

```bash
gitnexus status
```

#### 2. Refresh a Stale Graph Index

Inspect the status result and return an access error. If the repository is unindexed or behind the verified head, rebuild its index.

```bash
gitnexus analyze
```

#### 3. Measure the Change Surface

If indexing ran, inspect its result and return any failure. Require an index current with the verified head, then measure changes against the supplied base branch.

- `--base-ref` is the pull request's base, so the surface is the change rather than the branch's whole history.

```bash
gitnexus detect-changes --scope compare --base-ref '<base-branch>'
```

**Example:**

```bash
gitnexus detect-changes --scope compare --base-ref main
```

#### 4. Read Each Changed Symbol Context

Inspect the change-surface result and return any execution failure. For each changed symbol it identifies, read that symbol's context. Inspect each invocation before starting another; stop on a failed query.

```bash
gitnexus context '<symbol-identity>'
```

**Example:**

```bash
gitnexus context reserveRow
```

#### 5. Trace Each Reported Flow

Inspect the symbol-context results and return any execution failure. For each flow identified by the change surface, query its ordered symbols. Inspect each invocation before starting another; stop on a failed query. The result meets [Flow Traces](#flow-traces).

```bash
gitnexus query --query '<flow-identity>' --limit 1
```

**Example:**

```bash
gitnexus query --query "Queue Placement" --limit 1
```

#### 6. Re-Measure on a Stale Index

Inspect the flow-query results and return any execution failure. Inspect the staleness block on every response. If any response reports a behind index, discard its measurements and rebuild the index.

```bash
gitnexus analyze
```

#### 7. Verify the Refreshed Measurements

If the preceding step rebuilt the index, inspect its result and return any indexing failure. Repeat [1. Check the Graph Index Status](#1-check-the-graph-index-status) through [5. Trace Each Reported Flow](#5-trace-each-reported-flow) once with the updated index. Inspect every repeated response's staleness block; if any remains behind, return a freshness blocker.

#### 8. Return the Current Graph Evidence

Return only evidence current with the supplied head, meeting [Fields](#fields), or a freshness blocker.

## Fields

### Revision

The graph identifies its worktree and indexed commit. Measurements describe the supplied pull request head and its difference from the supplied base branch.

### Freshness

Graph responses carry a JSON `staleness` block. A behind index is not current with the requested head; measurements from it are invalid.

### Changed Symbols

The surface identifies symbols touched by the diff and the flows containing them. It compares with the supplied base branch, rather than the branch's whole history.

### Symbol Relationships

Each changed symbol has callers, callees, containing flows and file locations. Files group into component areas; their measured relationships determine edges between areas.

### Flow Traces

Each flow contains symbols in step order. Each `process_symbols` entry includes `step_index`, file and lines. Those ordered measurements supply sequence-diagram participants and interactions. A manually inferred call order does not establish a graph trace.
