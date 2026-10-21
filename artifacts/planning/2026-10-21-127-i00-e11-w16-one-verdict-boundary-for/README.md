# I00:E11:W16 Verdict Boundary: Spelled Twice, Once as a Pattern Over a CLI Message — October 2026

> Work Record · Created 2026-10-21

## Executive Summary

This row gives every remote read of the link check one verdict boundary. The boundary is spelled twice today: once as a comparison on a status code, and once as a regular expression matched against the text `gh` prints when a call fails. A change to one does not reach the other, and the second depends on wording the GitHub CLI is free to change, which is the kind of gap in the standalone checks this epic carries.

The status a tracker call produced is recovered from the response's own status line, which `gh api --include` writes, and given to the function that already decides a direct read. A failure carrying no status line is a call that did not reach the host; a failure under a status that resolves — a GraphQL error arrives under a 200 — keeps the reason the command gave. Nothing matches a CLI's message text for a number.

This row covers AC17 of the deferred-debt epic, which states what fixing the defect establishes rather than the defect it removes. It is delivered on the epic base rebuilt on the design I00:E12 landed, so what it measures is the product as it now stands.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w16.md](w16.md) | The task's plan: the two spellings of the verdict boundary and the one function that replaces them |
| [validation.md](validation.md) | What `gh api --include` reports, the tests that hold both routes to one verdict, and the checks the delivery was held to |
| [changes.md](changes.md) | The plan changes this session applied, the debt it deferred and the issues that arose |

## Links

| Resource | Link |
| --- | --- |
| Task issue | [#127 \[I00:E11:W16\] Verdict Boundary: Spelled Twice, Once as a Pattern Over a CLI Message](https://github.com/m2ux/prosiform/issues/127) |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Base rebuild | [I00:E11 Base Rebuild](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-39-i00-e11-base-rebuild) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
| Pull request | [#155 \[I00:E11\] One Verdict Boundary for Every Remote Read](https://github.com/m2ux/prosiform/pull/155) |
| Raised by this row | [#162 \[I00:E11:W28\] The Tracker Route Exercised by the Repository's Own Run](https://github.com/m2ux/prosiform/issues/162) |
