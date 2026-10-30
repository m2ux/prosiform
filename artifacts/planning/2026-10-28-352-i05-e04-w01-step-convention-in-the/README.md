# I05:E04:W01 Step Convention in the Corpus Guidelines — October 2026

> Task delivery · Created 2026-10-28

## Executive Summary

This record holds the delivery of I05:E04 W01. The example corpus's guidelines state the step convention: a procedure writes each step as a sub-section one heading level below the procedure's heading. Each sub-section is headed by its position and action, as `N. Action`, in the order performed and ahead of the procedure's child sections. The shared guidelines define a procedure by its step sub-sections.

A numbered list item roots no anchor. A link can therefore name a procedure but not its fourth step, and the corpus writes `step 4` as prose. Every later row of the epic converts a directory of the corpus to this rule, so the rule lands first.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | The step convention in the corpus guidelines: scope, design and the checks it requires |
| [Validation](validation.md) | The inspection against AC1 and the results of `make links`, `make corpus` and `make check` |
| [Change list](change-list.md) | The plan changes this delivery session applied and held |

## Decisions

- **Dependency on E03:W09 met by hand.**
  - W01 depends on I05:E03 W09. That row was delivered by #363 and reached `main` when the user merged E03's review pull request #355 (`8e56baf3`).
  - E03 stays open only for W11, the eval row, which waits on I05:E01 W05.
  - Plan Available Work reads a cross-epic row as waiting for that epic to close, so it reports W01 blocked. W01 is held by hand on the coordinator's instruction, since what it consumes is on `main` and in `i05/e04/main`. (User, through the coordinator, 2026-10-28.)

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E04 Corpus Steps](https://github.com/m2ux/prosiform/issues/352) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Corpus Steps planning record](../2026-10-28-352-i05-e04-corpus-step-subsections/README.md) |
| Upstream task | [I05:E03 W09](https://github.com/m2ux/prosiform/pull/363) |
| Pull request | [I05:E04 W01 Step Convention in the Corpus Guidelines](https://github.com/m2ux/prosiform/pull/364) |
