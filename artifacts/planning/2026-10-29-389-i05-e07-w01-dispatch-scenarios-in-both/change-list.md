# I05:E07:W01 Change List

The plan changes this delivery session met, each held rather than applied, with the option it recommends.

## Applied

None. This session holds no change allowance, so every plan change below is held.

## Held

- **The authored form publishes one bundle and so carries no dispatch sub-section.** `pf` emits a Prosiform section only where `pf` itself withholds a target. In the authored form the protocol is prose in the state documents and the target's section is compiled in, so an agent reaches the target by following an ordinary link in one bundle. **Recommended:** keep it, since it is what separates the two forms; state it in the epic's design, whose Scenarios bullet says both forms are bundle sets without saying the authored one is a single bundle. Recorded rather than applied: the epic's design is the epic record's, and its wording is its author's.
- **The default matrix is 280 sessions, and `make eval-diagrams` still passes USD 100.** Eight sessions are dispatch scenarios in each of two forms, so the matrix grows from 200 to 280 at USD 0.50 a session: exactly USD 140 at the session cap, above the budget. The budget covers it only because a session records far less than its cap. **Recommended:** raise `EVAL_BUDGET_USD` in the `Makefile` to USD 150 in W03, whose work item is the row that estimates the run's cost and puts it to the user; leave it here, since changing it changes what a run may spend.
- **A workflow's forms are declared by its directories.** `Workflow.forms` reads which of `FORMS` a workflow holds a directory for, so the reader infers a form's presence rather than reading a declaration. **Recommended:** keep it; a declaration would be a second statement of what the directories already state, and the reader fails on a form whose directory is absent.
- **The trace's `returned` field is the scenario's alone.** `dispatch_walk()` derives each sub-agent start, its order and whether it started beside the previous entry, from the source; what a sub-agent returned is stated by the scenario, since the source says a target *may* return a question rather than that it does. **Recommended:** keep the split, and let W02's scorer compare the recorded returns against it. Recorded because the epic's Scenarios bullet says "the sub-agents it starts, in what order, and what each returned" as one walk of the source, which this separates.

## Deferred debt and arising issues

- **Deferred debt.** None fixed here, and none created: the reader's `sections[DIAGRAM]` uses are replaced by `Workflow.walked`, so no caller is left reading a form a workflow may not hold.
- **Arising.** None raised as an issue. The observations above are held placements rather than arising work: the authored form's set shape belongs to the epic's design and the budget to W03's row.
