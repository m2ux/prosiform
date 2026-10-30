# Work Planner Link Capture — October 2026

> Plan · Created 2026-10-24

## Executive Summary

The work-planner skill specifies the `links.json` snapshot every sync step depends on, describes reading the Development field across every page and state, and supplies no way to produce either. A run therefore assembles the snapshot by hand, one call per issue or pull request, and nothing checks that what it built is complete.

This record preserves four scripts written while syncing initiative 20 against that gap, in general purpose form: two that read the Development relation in batches of 90, one that reports closed issues whose closure their own evidence does not support, and one that runs a named instrument at a merged revision in a throwaway checkout. Each is tested against the live repository, and the standalone issue raised from this record is [a link capture and closure sweep for the skill](https://github.com/m2ux/prosiform/issues/237).

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Issue capture](links-by-issue.py) | Reads every issue's Development links in one batched call, keyed by issue |
| [Pull request capture](links-by-pull-request.py) | Writes the `links.json` snapshot from the pull request end |
| [Closure sweep](closure-sweep.py) | Reports closed issues whose criteria or links do not support the closure |
| [Revision check](revision-check.py) | Runs a named instrument at one merged revision, then removes the checkout |

## Evidence

Each script ran against `m2ux/prosiform` on 2026-10-24, at the revision this record was written.

| Script | Result |
| --- | --- |
| `links-by-issue.py` | 94 issues read, 52 links, in one batched sweep |
| `links-by-pull-request.py` | 113 pull requests read, 49 links, identical to the snapshot the session assembled by hand |
| `closure-sweep.py` | 6 closures unsupported by their own evidence, 4 closed stating no criteria; exit 1 |
| `revision-check.py` | Ran at `5a3e8c2`, left no worktree and no temporary directory behind |

The pull request capture reproducing the hand-built snapshot exactly is the load-bearing result: it is what establishes that the batched read loses nothing the per-call read found.

## Links

| Resource | Link |
| --- | --- |
| Issue | [Link Capture](https://github.com/m2ux/prosiform/issues/237) |
| Initiative synced | [Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Skill | [`skills/work-planner`](https://github.com/m2ux/prosiform/tree/workspace/skills/work-planner) |
