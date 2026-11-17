# Unrouted Deferrals — November 2026

> Hot-fix · Created 2026-11-17

## Executive Summary

A deferral naming a document that declares alternatives must name one of them or carry `?`, whatever section it names. With F11 delivered, the later run compiles a section no alternative changes with none in force, so the check refuses a deferral that run accepts, and its author picks an alternative the section does not depend on.

The fix holds the deferral to the rule the later run applies: it names no alternative where its target, compiled as the entry the deferral publishes, needs none, and is refused where an alternative would change that content.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f14.md](f14.md) | The work item: the deferral pick check following the later run's rule |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request's reviewed heads and base |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F14] Unrouted Deferrals](https://github.com/m2ux/prosiform/issues/780) |
| Delivering pull request | [[F14] Unrouted Deferrals](https://github.com/m2ux/prosiform/pull/781) |
| Precedent | [F11 Unrouted Sections](../2026-11-17-773-f11-unrouted-sections/README.md) |
| Design | [The pick token](../2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling) |
