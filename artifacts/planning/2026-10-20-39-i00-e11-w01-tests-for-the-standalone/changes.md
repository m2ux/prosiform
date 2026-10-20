# Change List — I00:E11:W01

> Plan changes · Created 2026-10-20

## Applied

| Change | Kind | Where |
| --- | --- | --- |
| W01's row links [#131](https://github.com/m2ux/prosiform/pull/131) and carries its delivery mark | Delivery record | [#39](https://github.com/m2ux/prosiform/issues/39) |
| AC1 and AC2 are ticked | Delivery record | [#39](https://github.com/m2ux/prosiform/issues/39) |
| The review body carries this wave's Standalone Check Tests area and cites the pull request and this record | Delivery record | [#125](https://github.com/m2ux/prosiform/pull/125) |

## Held

Nothing. No row was created, migrated or re-prioritised, and no issue was raised.

## Debt classified

| Item | Classification | Where it went |
| --- | --- | --- |
| The slug rule keeps the underscores of a run of emphasis, which GitHub's rendering consumes | Blocking — AC1's comparison cannot pass while it stands | Fixed in this unit, `checks/links.py` |
| The anchor capture is recorded rather than fetched on every run, so a change GitHub makes to its anchor generation waits for a refresh | Not debt | Recorded as a limitation under [T1](validation.md#t1-the-slug-rule-against-githubs-anchors). A check reaching a third party every run reddens a branch over an outage, which is the verdict `checks/README.md` already takes for a reference. |
