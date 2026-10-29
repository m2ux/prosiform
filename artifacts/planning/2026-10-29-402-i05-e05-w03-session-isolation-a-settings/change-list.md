# Change List — I05:E05:W03

The plan changes this session met. It held no change allowance, so every one is recorded here as held with its recommended option and none was applied, except the epic row and AC tick the brief directs.

## Applied

The brief directs these and they are not plan changes:

- **Epic #374's W03 row** points at [#409](https://github.com/m2ux/prosiform/pull/409), replacing the planning-folder link, and its Done cell is ticked.
- **Epic #374's AC3** is ticked, the tests holding it.
- **Issue #402** carries `Delivered by #409.`, its AC1–AC3 ticked, and is closed as completed.
- **Board 18:** #402's Status is Done; #374 moves to In Review once its base is complete.
- **Review pull request #401** carries the base-complete note and the new row in its task table; it stays draft for its own review.
- **`checks.md`'s `make harness` row** states all three preflight refusals, carried on the epic base as commit `4f07f2bf` and cited in #401's Changes.

## Held

- **`checks.md`'s `make harness` row enumerated two refusals.**
  The row read "refuses a run whose config directory installs or enables a plugin before its first session". `preflight` now makes three refusals, so the row described a boundary narrower than the one `make harness` holds. The unit's component is `evals/diagram-following/run.py`, its test file and its README, so the session reverted the edit rather than widen its scope.

  **Applied as recommended: the row is carried on the epic base**, commit `4f07f2bf`, because the row describes a check the base runs and the base is where `checks.md` lives. #401's Changes cite it, so the review states the row it carries.

- **Deferred debt: a `settings.local.json` beside `settings.json`.**
  Raised as [#410](https://github.com/m2ux/prosiform/issues/410), `Session Isolation: A Settings Local File's Hook Refused`, labelled `tech-debt`, `theme:bundling` and `bot:ai-assisted`. The agent reads `settings.local.json` from the config directory and applies it over `settings.json`, so a `hooks` block there reaches a session exactly as one in `settings.json` does, and the preflight does not read it. The injected-context read still fails such a run, so the boundary holds; the cost is that a paid run spends its sessions before it is refused.

  Placed as a new task row in #374, it would take a fourth acceptance criterion — AC4, "a run whose config directory holds a `settings.local.json` declaring a hook is refused before its first session starts, naming the file and the events it declares" — since the table's Coverage column holds one criterion per row and AC1–AC3 are each already held by a merged unit.

  **Recommended: hold the row until #401 merges.** The epic's three criteria are all satisfied by merged work; adding AC4 and an open row to an epic whose review pull request is in flight states a criterion the base does not meet, which is what #401 is for. Place #410 after the review merges, in a follow-on epic or as #374's AC4 then.

- **Deferred Debt as I05's last epic, and its numbering.**
  Unchanged and still open from W01's change list. #410 is a deferred-debt issue of the same kind and takes the same treatment.

## Arising Issues

None beyond #410. The five mutation checks found no defect in the repair, and `make check` found none in the tree.