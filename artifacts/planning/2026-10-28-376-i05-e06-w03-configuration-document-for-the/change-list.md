# Change List — I05:E06 W03

## Applied

- **Delivery record.** #376 W03 row links [#381](https://github.com/m2ux/prosiform/pull/381) in place of this folder, from a fresh read; no other row or criterion changed.
- **Task merge.** #381 merged into `i05/e06/main` at `c0703645` after CI passed on `2cb35ebd`; the epic base had not moved since the branch was cut. #376 AC3 ticked and W03 Done, from a fresh read.

## Held

- **Epic review pull request.** Task Merge's review step for `i05/e06/main` is held: E06 has no review pull request and the user has not confirmed one. Recommended: open the draft review `i05/e06/main` → `main` when the user confirms it.

## Notes for Later Rows

- **W04.** The conventions' Example values list still names one value set by an outside project's name and holds example board numbers; it is an illustration, not a binding, and stays with Conventions. The Bodies example in Conventions also names an outside project. Configuration is bundled as a whole root document beside Rules and Conventions.
- **W07.** Find Proposals Board, Find Status Field, Find Engineering Worktree and List Planning Records take configured values as parameters (`<proposals-board-title>`, `<status-field-name>`, `<engineering-branch>`, `<records-folder>`); moving those commands inline keeps the parameters and their Inputs links.
- **W11 / #378.** The shared skill guidelines are outside `example/work-planner/` and were not inspected for bindings.
- **Helper limit.** The progress helper holds the standup Ready count as a constant with no argument; the helper is outside this repository, so the example states the value once and links it.
