# Validation — I05:E01 W06 + W07

> Task delivery · Created 2026-10-29

## Delivery Checkpoint

- Epic: [I05:E01] Diagram Following — https://github.com/m2ux/prosiform/issues/333
- Pull request: [#393 Linked Form and Errored Class](https://github.com/m2ux/prosiform/pull/393)
- Branch `i05/e01/w06-linked-form` → base `i05/e01/main`
- Base at validation: `961df526`
- Validated head: `44748235214625b091c6309bdef282d6114afe3b`
- Merged commit: `92c55bb698099bf36f070cc733d4459470ee468e`
- Rows covered: **W06** (AC1, AC11, AC12, AC13, AC14) and **W07** (AC4, AC15, AC16, AC17)

## Test Plan Results

Every row was executed at the validated head in `.worktrees/i05/e01/w06-linked-form/code`, with

```
UV_CACHE_DIR=/tmp/pr393-uv
PROSIFORM_BUILD="uv run --project <worktree> --frozen pf"
```

| Test | Description | Coverage | Result |
| --- | --- | --- | --- |
| T1 | The linked form's three workflows bundle with `pf` at exit 0 carrying every state's section | AC1 | Pass |
| T2 | Stub sessions walk both `branching` scenarios through the linked form | AC11 | Pass |
| T3 | Stub sessions walk both `looping` scenarios through the linked form | AC12 | Pass |
| T4 | A rule stating another label, a rule stating no label, and a decision stating its label inline are each a fault | AC13 | Pass |
| T5 | A rule document resolving from the section's own directory reaches its label | AC14 | Pass |
| T6 | A session whose result sets `is_error` takes `errored` | AC15 | Pass |
| T7 | A session with no result and no trace takes `errored`; a timeout keeps `unfinished` | AC16 | Pass |
| T8 | The report compares against a baseline lacking `errored` without failing | AC17 | Pass |
| T9 | `make harness` over `checks/tests` and `evals/diagram-following` | AC1, AC4 | Pass |

### T9 — Harness

`825 passed in 16.14s` at the validated head. The base at `961df526` gives `812 passed`, so the two rows add thirteen tests.

Instrument: `make harness`, the target `make check` runs for the eval.

### T1 — Bundling

`make corpus` gives `342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass`. Every `linked/` tree bundles through `pf` at exit 0 with no diagnostics, with the rule documents inlined and their links rewritten to the document's anchor, so a bundle carries the same conditional semantics as the source tree.

The eval's workflows are not corpus fixtures, so this run also establishes that the two rows changed nothing the corpus observes.

### T2, T3 — The linked form's walks

Both `branching` scenarios and both `looping` scenarios pass through the linked form, each reaching its scenario's expected path. The asymmetry is what makes them meaningful: `branching` links `escalation.md` for `high` and `queue.md` for `low`, so a reading that takes the first link's first label fails `low-severity`; `looping` links `rework.md` for `revise` and `release.md` for `approve`.

Each test also asserts the session's workspace holds the linked form's rule documents. That assertion is load-bearing: the stub agent finds state headings in any form, so the walk alone passes on a form laid out as a plain tree. With `LINKED_TREE` mapped to `DIAGRAM` the tests fail with `the linked form's rule documents are absent`.

### T4 — The three faults

A rule document stating a label the diagram does not draw is a corpus fault; a rule stating no label is a fault; a decision stating its label inline instead of naming a rule document is refused.

### T5 — Resolution from the section's directory

A rule link resolves against the writing section's own directory, `states/`, reaching `../rules/escalation.md`.

### T6, T7 — `errored`

A session whose `result` message sets `is_error` takes `errored`; a session that printed no result and left no trace takes `errored`; a session ended at its timeout that wrote a trace is scored from that trace and stays `unfinished`. A refused session reports no cost, so the run charges its session cap and the budget still holds.

Removing the `is_error` read makes the test fail with `None != 'errored'`, which is how the path was confirmed reachable rather than incidentally passing.

### T8 — A baseline lacking the class

A baseline whose cells carry no `errored` key compares without failing, its absence read as zero. There are two tolerances: `summed` normalises a baseline cell's failures, and `difference` normalises a row's. Removing the one in `summed` makes the test fail with `KeyError: 'errored'`; removing the one in `difference` alone does not, because `summed` has already normalised the cell. The test is aimed at the site that decides the outcome.

### Static checks

`make lint`, `make format-check` and `make typecheck` each pass at the validated head; mypy reports no issues in 75 source files.

## Tests Added In This Delivery

Three rows stated a test and had none. Four tests were added:

- `test_the_linked_form_walks_every_scenario_of_a_branching_workflow` (T2)
- `test_the_linked_form_walks_every_scenario_of_a_looping_workflow` (T3)
- `test_an_agent_reporting_an_error_is_errored_though_it_wrote_a_trace` (T6)
- `test_a_baseline_without_the_errored_class_still_compares` (T8)

The stub agent gained `STUB_AGENT_ERROR`, so the `is_error` branch can be reached; before this it hardcoded `is_error: false` and only the exit-without-a-trace path was covered.

Each was mutation-checked: the behaviour it covers was removed, the test failed, the behaviour restored. That check found two weak first drafts — T2/T3 passed on a mislaid form, and T8 passed against the wrong tolerance site — both corrected before the merge.

## Live Sessions — Ten-Session Probe

The eval's own login answered `You've hit your weekly limit` until 31 October, so no paid default-matrix run was possible. A ten-session probe exercised the linked form against real agent behaviour instead.

Workspaces were laid out by the eval's own `prepare` semantics — `bundle` as the `pf` bundle, `linked` as its source tree, each holding only its scenario's inputs and no expected path — and scored with the eval's own `score.py`, not by inspection.

| Workflow / scenario | bundle | linked |
| --- | --- | --- |
| branching / high-severity | pass | pass |
| branching / low-severity | pass | pass |
| linear / straight-through | pass | pass |
| looping / no-rework | pass | pass |
| looping / two-rounds | pass | pass |

Ten of ten passed, each walking its scenario's exact expected path and leaving every action file.

**What this establishes.** The linked form's conditional semantics resolve through the rule document in both `branching` and `looping`, including the asymmetric pair where `high` and `low` sit in different documents. The loop counter is read from `inputs/rounds.txt`, producing two `Revise → Check` cycles for `two-rounds` and none for `no-rework`.

**What it does not establish, and is not claimed.**

- One model, one repetition: ten sessions cannot refresh a 150-session baseline, cannot detect a 20% failure rate, and do not populate the cost or token columns.
- No cost, usage or duration is recorded, so the baseline's measured cost remains unrefreshed.
- Isolation is weaker than the eval's: the probe ran without `claude -p`'s tool list, `--strict-mcp-config`, the slash-command ban and the scrubbed environment, so a pass here is not strictly comparable to a baseline pass.

The probe is evidence for the linked form's semantics. It is not a baseline.

## Merge

- Target `i05/e01/main`: no branch protection, no active rules.
- CI `Checks` completed `success` at the validated head before the merge.
- Merge method: merge commit, `sha` pinned to `44748235214625b091c6309bdef282d6114afe3b`; merged `92c55bb6`, and a comparison of head against the merge commit reports no changed file.
