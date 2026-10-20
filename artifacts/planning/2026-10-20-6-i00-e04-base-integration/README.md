# I00:E04 Base Integration - October 2026

> Integration record - Created 2026-10-20

## Executive Summary

This record holds the integration of `main` at `87ec398`, carrying the closed [I00:E03] Outline Hierarchy epic, into the [I00:E04] Dependency Closure base `i00/e04/main` at `759c379`. The merge commit is `c3181dd`. It delivers no acceptance criterion: it reconciles two designs for the same part of the command so that the epic's next row cuts from a base carrying both.

The two epics changed the same four regions of `prototype/src/prosiform/cli.py`. E04 parses each reference into a path identity through `closure.py` and reads every source through `access.py`'s rooted, no-follow walk; E03 groups references by the document each names and selects regions from that document by fragment. The reconciled command carries both: a parsed, confined reference is grouped by the path it normalized to, and the group selects from its source the regions its decoded fragments root.

## What Diverged

| Region | E04 on the base | E03 via `main` | Reconciled |
| --- | --- | --- | --- |
| `contributing` | Whole-document paths of fragmentless `Reference`s, as a sorted list | References grouped by `relative(root, document(reference))`, as a sorted dict of raw reference strings | References grouped by `Reference.path`, as a sorted dict of `Reference`s |
| `selection` | Absent; a fragment was a refusal | Reads the fragment back out of the raw reference text | Reads `Reference.fragment`, which the normalization decoded |
| `compose` | Keyed `read` by `Reference.path`, emitted whole documents | Took `root` and the raw references, keyed `read` by the authored document text | Keyed by `Reference.path`, emits each group's selection |
| `execute` | Refused every fragment with the unexpected-internal-error status | Passed the raw command line into `compose` | Passes the resolved referrer and references into `compose`; the refusal is gone |

Two things the merge removed rather than carried:

- `relative(root, name)` resolved a group's path on the filesystem. The normalization already produces the root-relative identity, and resolving it would reintroduce the symbolic-link following that `access.py` exists to prevent. Group identity is now the normalization's, and `cli.py` reaches the filesystem for no part of it.
- `document(reference)` and `fragment(reference)` split a reference by string. `closure.resolve` splits before decoding, which is the order the design requires, so both helpers retire with the paths that used them.

Each module kept its reason to change: `closure.py` reaches no filesystem, `access.py` does the walking, `source.py` owns the heading index and the section span, `bundle.py` owns emission, and `cli.py` wires them. Nothing moved between them.

## What Was Verified

`make check` passes whole on the merged base, all eleven targets, with `PROSIFORM_BUILD` naming the worktree's build.

The corpus holds 84 fixtures, the union of the base's 57 and `main`'s 67 across 40 shared: 82 pass, 0 fail, 0 unexpected pass, and 2 awaited. `normalization/root-escape` awaits `I00:E04` and `extraction/an-unterminated-example-at-the-section-end` awaits `I00:E08`; both markers predate this merge.

Three behaviours only the merged base can exhibit were exercised by hand, each returning the bundle the reconciled design states:

- `docs/../guide.md#run-it` - a path a parent segment normalizes, selecting a section.
- `guide.md#run%2Dit` - an escaped fragment, resolved against the heading text it decodes to.
- `guide.md#stop` with `./guide.md#run-it` - two spellings of one document naming one group, which carries both selections in source order.

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#6 \[I00:E04\] Dependency Closure](https://github.com/m2ux/prosiform/issues/6) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W02 record | [Root confinement and no-symlink source access](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-6-i00-e04-w02-root-confinement-and-no) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
