# Change List — I05:E01 W09

The allowance for this session is **none**, so every plan change is held. None was applied.

## Held

- **Folded work — epic 333's AC21 states the refused state and the withheld comparison, and not the recorded reason.**
  The criterion as it stands is met: a run whose every session errored is recorded as refused and its report names that rather than comparing pass rates. The reason is also recorded and named, which AC21 does not ask for, because the task issue's own AC1 and the delivery brief both require the agent's own message to stand as the reason. No criterion is unmet; the delivery is wider than AC21's wording.

  Recommended: leave AC21 as it stands. The reason is what makes the state readable — a refusal a reader cannot distinguish from a bare error count is barely better than the silent comparison the run made before — and it is delivered by the same test T1 that observes AC21, so folding it into the wording would state one invariant twice.

- **Folded work — epic 333's AC21 does not name where the boundary between a refusal and a result is decided.**
  The criterion names only the every-session-errored run. The delivery also holds the other side: a run the budget stopped part way, and one with an errored session beside passing ones, stay completed, and both have their own test. That is the same invariant read in both directions, and no criterion states the second.

  Recommended: leave AC21 as it stands. A criterion naming the exclusion would carry two invariants, and the exclusion is what "every session" already means.

## Applied Without An Entry

These follow from the delivery and decide nothing the plan does not already state, so they need no allowance.

- W09's row links [#404](https://github.com/m2ux/prosiform/pull/404) and takes Done; epic 333's AC21 is ticked.
- Task issue [#396](https://github.com/m2ux/prosiform/issues/396) is closed as completed, every criterion ticked and its one Development-linked pull request merged.
- Review pull request #353's body cites the W09 task merge into its base.

## Not Claimed

- AC21 is observed against the stub agent only. No paid session ran, so nothing here shows a real spent login producing `errored` sessions wherever this test's stub does; W07 established that path and W08 held the boundary around it.
- The reason is the first session's own `result` text in matrix order. A run whose sessions were refused for different reasons quotes one of them, and the rest remain in their own session records.
- The refused state is read from the session records the runner writes. A session whose `session.json` is missing reads as not errored, which leaves the run completed; no path in `run` writes a record for a session it started without one.

## Deferred Debt

None. The validation found nothing blocking, nothing trivial left unfixed, and nothing non-trivial that would warrant a work item of its own: each limitation above is either the design the brief states or a path the runner cannot reach.
