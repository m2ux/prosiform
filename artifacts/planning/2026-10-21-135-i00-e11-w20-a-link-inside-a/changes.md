## Overview

The plan changes this delivery session applied, and the ones it holds for the user.

## Applied

| Change | Kind | Where |
| --- | --- | --- |
| The W20 row links its pull request and carries its Done tick, and AC21 is ticked | Delivery record | [#39](https://github.com/m2ux/prosiform/issues/39) |
| The task issue's AC1 and AC2 are ticked and the issue is closed as completed | Delivery record | [#135](https://github.com/m2ux/prosiform/issues/135) |
| The pull request links the task issue in its Development field | Delivery record | [#152](https://github.com/m2ux/prosiform/pull/152) |
| A reference fixture declares a link inside an image an enclosing link carries | Corpus | [#152](https://github.com/m2ux/prosiform/pull/152) |

## Held

| Finding | Why it is held |
| --- | --- |
| The epic's review pull request [#125](https://github.com/m2ux/prosiform/pull/125) does not cite this row's area or its references, which `sync.py` reports as a References disagreement against the pull requests merged into `i00/e11/main` | The edit was refused by this session's permission gate for an external write. The body is also being edited by seven concurrent sessions, so it belongs to one pass over the review pull request once every row has merged. |
| `sync.py` reports W15 and W24 linking their task issues rather than their pull requests, and pull requests [#100](https://github.com/m2ux/prosiform/pull/100) and [#151](https://github.com/m2ux/prosiform/pull/151) as unmatched against epic rows | Each belongs to the row that delivers it, and those rows are being delivered as this one runs. Correcting another row's link here would overwrite that session's record. |

## Against D59 and D60

Nothing this row measured contradicts either decision. [D60](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) states that W20 declares a compiled link rather than a marked one; the fixture resolves both links under the allowed source root, and the deferral mark plays no part in the shape.
