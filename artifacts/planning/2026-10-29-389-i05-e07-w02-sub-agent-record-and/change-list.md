# I05:E07:W02 Change List

The plan changes this delivery session met, each held rather than applied, with the option it recommends.

## Applied

None. This session holds no change allowance, so every plan change below is held.

## Held

- **A dispatch start is a `Task` tool call, and the tool list has no declared contract.** The record reads each sub-agent start from a `Task` `tool_use` block in the transcript, its section from that call's `description` and its return from the `tool_result` text opening `question` or `done`. Nothing in the repository states either shape: `run.py`'s `TOOLS` gained `Task`, and the shapes are conventions of the agent's own transcript that the stub now imitates. A change to either name or field would silently record no sub-agent and fail every dispatch scenario as `undispatched`. **Recommended:** pin the shape in the evals documentation and assert it in a test against a recorded transcript, so a renamed field fails loudly; that is a change to the eval's own contract rather than to this row's scope, so it is held.

- **The two forms' calls name a section differently.** A compiled form's `Task` call names `pf`'s bundle (`plan__work.bundle.md`) and an authored form's names the section (`plan#work`), so `score.py`'s `names()` accepts both spellings. The scenario states one form, `<document>#<heading>`, and the bundle name is derived from it. **Recommended:** keep the derivation, since it is the one place the two forms' naming is reconciled and both are compiled from one section; a second field in `scenarios.toml` would restate what the bundle's name already says.

- **The record is read after the workspace is deleted.** `run.py`'s `start()` calls `keep()` to copy the trace and actions out of the workspace, then `record_starts()` reads the transcript and writes `subagents.json` in the records directory, and the scorer reads the records directory rather than the workspace. `score()` is therefore handed `records`, not `workspace`. **Recommended:** keep it; the record's purpose is that the scorer needs no second read of the transcript, and both paths are the workspace's final state.

- **`sequential_set` is decided by the `together` flag alone, not by timing.** Two `Task` calls sharing one assistant message are `together`; a compliant agent that starts a set in one message and one that starts it serially are distinguished by that alone. A harness that emitted two messages microseconds apart with no waiting would read as `sequential_set` although the set did start together. **Recommended:** keep it, because a wall-clock threshold would be a second, tunable source of truth beside the message grouping the protocol states; record the limit here for W03's baseline reading.

- **The stub dispatches in both forms from one scenario trace.** The trace is the scenario's, not the form's, so the stub starts the same sections for `compiled` and `authored`. That is what the epic's design states — one trace is the trace of both — but a form-specific difference in dispatch, were one to appear, would not be observable through the stub. **Recommended:** keep it; a form-specific trace would break the one statement the corpus holds of the dispatch.

- **No check observes a sub-agent's own section content.** The record names the section a start followed and what it returned; it does not verify that the sub-agent read that section, wrote its action or walked its own path. A session could name a section and return `done` without the sub-agent doing anything. **Recommended:** hold; observing a sub-agent's own work needs its transcript, which is a second record and beyond AC3's four checks. Record it for an arising issue if the baseline shows dispatch passing where the target's work is absent.

## Deferred debt and arising issues

- **Deferred debt.** None fixed here, and none created: `input_read`, `successor` and the seven path classes are unchanged, and the three dispatch checks are read only after a run's path and actions hold, so no existing scenario's verdict moves.

- **Arising.** None raised as a standalone issue. The observations above are held placements rather than arising work: the transcript's shape and the record's placement belong to the eval's design, `sequential_set`'s limit to how W03 should read the baseline, and a sub-agent's own work to a record this row does not write.
