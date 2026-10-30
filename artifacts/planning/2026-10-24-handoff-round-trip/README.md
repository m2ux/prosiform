# Handoff Round-Trip — October 2026

> Delivery · Created 2026-10-24

## Executive Summary

The dispatch operator and the deferral both exist so that one bundle can hand material to a later run. Every fixture asserts the form that material takes in the bundle, and no test compiles what was published, so the claim the construct rests on is held by nobody. This record plans an end-to-end suite that bundles a synthetic tree, reads the destinations the first bundle published, compiles each, and compares the result.

The work matters because the handoff is the reason either operator exists. A `¬` link is material reached in a run of its own and a `»` link is material a sub-agent compiles; if the published destination cannot be compiled, both statements are false and the corpus would still be green. The design's own `Deferred handoff` conformance row currently reports zero fixtures.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Design](design.md) | The gap, the measured probes, the decisions and the stacks each row exercises |

## Links

| Resource | Link |
| --- | --- |
| Epic | [#242 \[I01:E09\] Dispatch Operator](https://github.com/m2ux/prosiform/issues/242) |
| Initiative | [#20 \[I01\] Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
