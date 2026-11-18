# Alternative Diagnostics — November 2026

> Hot-fix · Created 2026-11-18

## Executive Summary

A `default` pair agreeing with a picked alternative's pair leaves the redirect silent, where the routing-pair rule makes it a stand-in that warns `W_SUBST_USED`. A `?` dispatch whose brief an alternative routes, or whose target's alternative names a brief of its own, is refused under a remedy that would remove the pick.

The fix counts an agreeing `default` pair as a stand-in, gives a picking dispatch's routed brief a remedy naming the brief's section and stating that it must compile with no alternative in force, and names the picking dispatch whose target's alternative names a brief, with a remedy stating that the brief must not vary by alternative.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f23.md](f23.md) | The work item: the agreeing `default` pair and the picking dispatch's remedies |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request's reviewed heads and base |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F23] Alternative Diagnostics](https://github.com/m2ux/prosiform/issues/800) |
| Folded issue | [#801](https://github.com/m2ux/prosiform/issues/801) |
| Folded issue | [#807](https://github.com/m2ux/prosiform/issues/807) |
| Delivering pull request | [[F23] Alternative Diagnostics](https://github.com/m2ux/prosiform/pull/803) |
| Found by | [[F19] Tagged Compositions](https://github.com/m2ux/prosiform/pull/794) |
