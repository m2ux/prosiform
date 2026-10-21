# Changes — I00:E10:W01

Delivered by [#166](https://github.com/m2ux/prosiform/pull/166), merged into `i00/e10/main` at `d3ad060`.

## Corpus

| Change | Where |
| --- | --- |
| A selection whose source outline skips a level keeps the gap, the ancestors above it emitted at the levels the source gave them | `fixtures/structural-ancestors/an-outline-that-skips-a-level/` |
| A reference carrying an empty fragment names the whole document | `fixtures/normalization/an-empty-fragment/` |
| A tab in prose and the tabs indenting a code example reach the bundle as the source wrote them, beside a rewritten link | `fixtures/candidate-validation/tabs-beside-a-rewritten-link/` |
| A code example the source terminated with CRLF keeps those terminators, beside a rewritten link | `fixtures/candidate-validation/crlf-lines-beside-a-rewritten-link/` |
| Two definitions of one label spelled in different case resolve to the first and are both removed | `fixtures/reference/a-label-two-definitions-spell-in-different-case/` |
| Thirteen manifests name the adversarial family they encode | `fixtures/{boundary,candidate-validation,cli,consolidation,deferral,delivery,destinations,entry-line,extraction,generated-input,grouping,limits,validation-scope}/` |

## Corpus guide

| Change | Where |
| --- | --- |
| The clause form a fixture uses to name its family, and why the declaration sits in the manifest | `fixtures/README.md` |
| The two families no source tree can state, each with the work that delivers it | `fixtures/README.md` |

## Tracker

| Change | Where |
| --- | --- |
| W01 linked to its pull request and AC6 ticked | [#9](https://github.com/m2ux/prosiform/issues/9) |
| Rows W30 and W31 and criteria AC31 and AC32 added | [#39](https://github.com/m2ux/prosiform/issues/39) |
| Parser exhaustion raised as deferred debt, placed on the Bundling board in Backlog | [#164](https://github.com/m2ux/prosiform/issues/164) |
| CRLF in untouched paragraph content raised as deferred debt, placed on the Bundling board in Backlog | [#165](https://github.com/m2ux/prosiform/issues/165) |

## What remains open

**AC1 is unticked.** Twenty-five of the twenty-seven families the design names are held and named by fixtures. Consistency and Parser exhaustion are held by nothing, each because the condition it turns on belongs to the run or the parser rather than to a source tree, and each is a tracked row: [I00:E11:W24](https://github.com/m2ux/prosiform/issues/150) and [I00:E11:W30](https://github.com/m2ux/prosiform/issues/164). The criterion is also observed by a report W02 builds, so the reading above stands until that report exists.
