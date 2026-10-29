# Change List — I05:E01 W06 + W07

## Applied

- **Fold (test coverage).** Four tests added for rows that stated one and had none, with `STUB_AGENT_ERROR` added to the stub so the `is_error` branch is reachable. Fixes land in the pull request whose code they cover.
- **Board (W06, W07).** Both rows link [PR #393](https://github.com/m2ux/prosiform/pull/393) and take Done.
- **Criteria.** AC1, AC4 and AC11–AC17 ticked against the evidence in the validation record. AC2, AC3 and AC5–AC10 were already ticked.

## Held

- **Task creation — W08, a refreshed baseline.** The epic has no row for a live baseline carrying the linked form and the `errored` class. W06's own Open Questions state the committed baseline predates both rows, that its `linked` rows read `new`, and that the first baseline carrying them needs a run after 31 October. AC9 is ticked on the strength of the existing 150-session baseline, which is what it asks for, but the form comparison cannot read the linked form until a run refreshes it.

  Recommended: add a task row **W08 — Baseline refreshed carrying the linked form** with coverage **AC18**, depending on W07, and AC18 worded:

  > **AC18.** The committed baseline carries the linked form and the `errored` class, drawn from the default matrix on a run after 31 October 2026, with its report and cost, as the baseline file and the run record show.

  This run holds it because the run was user-driven and carries no allowance for a plan change.

## Not Claimed

- The epic's AC9 is not evidence that the linked form has been measured on a live run. It is ticked for the baseline that exists.
- The ten-session probe is not a baseline and is not recorded as one.
