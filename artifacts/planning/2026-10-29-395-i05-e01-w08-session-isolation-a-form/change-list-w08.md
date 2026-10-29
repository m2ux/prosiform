# Change List — I05:E01 W08

The allowance for this session is **none**, so every plan change is held. None was applied.

## Held

- **Folded work — the epic's AC18–AC20 wording names the preflight and the read as one criterion each, and the boundary they hold is now two refusals and a read.**
  The criteria as they stand are accurate: AC18 names the plugin refusal, AC19 the injected-context read, AC20 the documentation. W08's work makes a second refusal true — a `remote-settings.json` that enables a plugin — which no criterion names on its own, and which is delivered only because the same preflight holds it. No criterion is unmet; the coverage is simply wider than the wording.

  Recommended: leave the criteria as they stand. The remote-settings refusal is the same invariant AC18 states — a directory the eval did not write cannot supply a plugin — reached through the other file that states one, and folding it into AC18's wording would state one invariant twice.

- **Task creation — W09's row states `Depends on W08` and covers AC21–AC22, and this session's outcome does not change that.**
  No change is needed and none is recommended. Recorded only so the row's state is read in one place with the rest: W08 is delivered, W09 remains available to a session that has the model credit the paid run needs.

- **Re-prioritisation — the W08 row's link.**
  The row links the planning folder while reserved. `Task Delivery` gives the pull request's link as the replacement once one is open, and that replacement is a delivery record rather than a plan change, so it is made by the pull request step and takes no entry here.

- **Task creation — the deferred settings-file refusal, [issue #402](https://github.com/m2ux/prosiform/issues/402).**
  A `settings.json` in the eval's config directory can deliver a `SessionStart` hook without installing a plugin, and the preflight reads neither that file nor its `hooks` block. The injected-context read still refuses such a run, so W08's own criteria hold; what is deferred is refusing it before a paid run spends its sessions, and the tests that state it.

  Recommended: place it as **W03 — Session isolation: a settings file's hook refused** in the Deferred Debt epic, [I05:E05](https://github.com/m2ux/prosiform/issues/374), whose coverage is the epic's **AC3** (added to that epic's criteria, since the epic's AC1 and AC2 are ticked and this is one invariant). The work extends the preflight W08 delivered, so it is not a new initiative's work. `Hoist Mode` reports the placement as held: the allowance is none, and a task row and the criterion behind it are `Task creation`, which the allowance does not name.

- **Folded work — the review pull request [#353](https://github.com/m2ux/prosiform/pull/353)'s body.**
  Its References cited #335–#338 and #379 but neither #393 nor #400, so it did not state the two task merges into its base. Its Changes now carry a heading for the linked form and the `errored` class, and a heading for session isolation, with R9 and R10 citing them. This is a record of the merge, not a change to the plan, and it holds no entry against the allowance.

## Applied Without An Entry

These follow from the delivery and decide nothing the plan does not already state, so they need no allowance.

- W08's row links [#400](https://github.com/m2ux/prosiform/pull/400) and takes Done; epic 333's AC18, AC19 and AC20 are ticked.
- Task issue [#395](https://github.com/m2ux/prosiform/issues/395) is closed as completed, every criterion ticked and its one Development-linked pull request merged.
- Review pull request #353's body cites both task merges into its base.

## Not Claimed

- AC1, AC2 and AC3 of task issue #395 are observed by the stub agent only. No paid session ran, so nothing here establishes how a real agent behaves under the boundary, only that the boundary is enforced before and after a session.
- The preflight refuses the two files the observed plugin wrote. A hook reached through a `settings.json` is not refused at preflight; the injected-context read is what would catch it, and that read is not exercised against a real plugin. [#402](https://github.com/m2ux/prosiform/issues/402) takes it.
- Epic 333 is not closable: W09 (#396) is undelivered and AC21–AC22 are unticked. The epic stays on the board at In Progress.
