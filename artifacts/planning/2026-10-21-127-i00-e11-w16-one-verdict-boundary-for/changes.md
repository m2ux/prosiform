# Change List — I00:E11:W16

> Recorded 2026-10-21

## Applied

| Change | What it is |
| --- | --- |
| Task created | [#162 \[I00:E11:W28\] The Tracker Route Exercised by the Repository's Own Run](https://github.com/m2ux/prosiform/issues/162), the debt this delivery deferred |
| Row placed | W28 of [#39](https://github.com/m2ux/prosiform/issues/39), covering the new criterion AC29, with no dependency and no join |
| Row delivered | W16 links [#155](https://github.com/m2ux/prosiform/pull/155) and carries its Done tick; AC17 is ticked on the epic and AC1 on [#127](https://github.com/m2ux/prosiform/issues/127), which is closed |

## Deferred Debt

- **The tracker route is unexercised by the repository's own run.**
  No document `documents.py` finds names an issue, a pull request or a project board, so `make links` never makes a `gh api` call. The route's unit tests hold it to a stand-in, and whether the real command still writes a status line the module can read is observed only by hand. It blocks nothing — the route works, and this record measures it — and fixing it is a change to the documents the check reads rather than to the check, so it is a row of its own. Placed as W28 of the deferred-debt epic.

## Held

- **The delivery procedure's epic sync clears another row's Done tick.**
  `sync.py` reads a row whose Done depends on a task issue it was not given as undelivered, so a session passing only its own task issue to `--tasks` writes a body with other rows' ticks cleared. One sibling row was wiped this way during this wave. The fix belongs to the work-planner skill, which this workspace holds upstream rather than in `m2ux/prosiform`, so no issue is raised here and the defect is reported instead. This session passed every task issue of the epic to `--tasks`, diffed the result against a body read seconds earlier, and patched only its own row and its own criterion.

## Nothing Contradicting D59 or D60

The work is confined to `checks/`, which reads documents rather than compiling them. No reference's classification, no mark and no bundle is touched, so neither decision is engaged.
