# Bundle-relative Deferrals — November 2026

> Hot-fix · Created 2026-11-19

## Executive Summary

A deferral published its target's path from the working directory `pf` was run in, which the bundle never names, so a reader handed only the bundle could not resolve it. The compiler now calculates the path at compile time from the folder the bundle is written into, and the guide runs a link from that folder.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f27.md](f27.md) | The work item: deferral paths and the guide's compile step |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request's reviewed heads and base |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F27] Bundle-relative Deferrals](https://github.com/m2ux/prosiform/issues/818) |
| Delivering pull request | [[F27] Bundle-relative Deferrals](https://github.com/m2ux/prosiform/pull/819) |
