# The Three Faults a Run Shows Its User — October 2026

> Delivery · Created 2026-10-21

## Executive Summary

Three defects remain in the prototype that a person invoking the tool meets. A document whose whole content is the title its subsection absorbs is emitted nowhere under a grouping rule, and the reference naming it is rewritten to the group's heading, so a bundle loses a selected document and misdirects the link to it while the run exits successfully. A source whose lines are terminated with CRLF bundles to one terminated with LF on every line, against a clause requiring untouched content to keep its newline spelling. An ordinary CommonMark autolink in selected content ends the run with the internal-error status, although the profile names autolinks as core syntax the build supports.

They are delivered together because each is observable from a run of the tool and the rest of this epic's remaining work is not: the checks under `checks/`, the corpus declarations and the design record reach no user of the build, and are carried to [#187 \[I01:E03\]](https://github.com/m2ux/prosiform/issues/187). Two of the three fail silently, which is what makes them worth one pull request rather than a backlog: a bundle that lost a document and a bundle whose every line was rewritten both exit zero, so nothing the user runs tells them it happened.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W29](w29.md) | The work item for the member a merged group emits nowhere |
| [W31](w31.md) | The work item for the newline spelling carried through emission |
| [W37](w37.md) | The work item for the autolink the emission cannot carry |
| [Analysis](analysis.md) | The reproductions against the base, and the criticality reading that placed these three here |
| [Validation](validation.md) | The checks observing each criterion and their results |
| [Changes](changes.md) | The plan changes this delivery applied and held |

## Links

| Resource | Link |
| --- | --- |
| Task issues | [#163 \[I00:E11:W29\]](https://github.com/m2ux/prosiform/issues/163), [#165 \[I00:E11:W31\]](https://github.com/m2ux/prosiform/issues/165), [#181 \[I00:E11:W37\]](https://github.com/m2ux/prosiform/issues/181) |
| Epic | [#39 \[I00:E11\] Deferred Technical Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Carried debt | [#187 \[I01:E03\] Carried Debt](https://github.com/m2ux/prosiform/issues/187) — the rows deferred from this epic because no run of the tool shows them |
| Row joins | [Outstanding row joins](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-39-i00-e11-outstanding-row-joins) |
| Epic review | [#180](https://github.com/m2ux/prosiform/pull/180) — the base's draft review for `main` |
