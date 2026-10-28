# I05:E03:W11 Review Fixes for Publication and Dispatch — October 2026

> Task delivery · Created 2026-10-28

## Executive Summary

This record holds the delivery of I05:E03 W11–W15, five joined rows sharing one pull request into `i05/e03/main`. They fix the seven findings of the review of the epic as merged to `main` by #355: the run folder's swap follows a link at its path, `-c` passes runs that publication refuses, a source read two ways publishes a mixed set, a failed restore or cleanup misreports, staging names overflow long run names, dispatch link text breaks its heading, two headings are reserved in bundles that never emit them, and the tests and fixture families carry retired names.

The epic's bundle set is the contract an agent follows. Each finding is a run that writes outside its folder, reports a status its outcome contradicts, or ends in an internal error on ordinary input, so each is fixed with the test or fixture the review found missing before the epic's review pull request goes to `main`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W11 work item](w11.md) | The run folder's swap: a link at its path, a refused restore and a refused cleanup |
| [W12 work item](w12.md) | Name collisions, a missing output folder and a source read two ways, refused before any write |
| [W13 work item](w13.md) | Staging and aside names independent of the run folder's |
| [W14 work item](w14.md) | Dispatch link text, empty-text refusal, reserved headings and one dispatched-link reader |
| [W15 work item](w15.md) | Schema-valid test manifests and the renamed fixture families |
| [Findings](findings.md) | The seven review findings, as verified at `main` 8e56baf3 |
| [Validation](validation.md) | Each test-plan check, the revision it ran on and what it observed |
| [Change list](change-list.md) | The plan changes this delivery applied and held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E03 Dispatch Bundles](https://github.com/m2ux/prosiform/issues/351) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Dispatch Bundles planning record](../2026-10-28-351-i05-e03-dispatch-bundles/README.md) |
| Merged epic | [#355](https://github.com/m2ux/prosiform/pull/355) |
| Pull request | [#366 Review Fixes: Publication and Dispatch at Their Edges](https://github.com/m2ux/prosiform/pull/366), merged as 3ec3a1e7 |
| Review pull request | [#369](https://github.com/m2ux/prosiform/pull/369) |
