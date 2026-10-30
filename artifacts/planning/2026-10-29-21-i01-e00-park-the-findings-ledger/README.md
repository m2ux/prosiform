# Park the Findings Ledger Epic

## D1 — E00 Parks at Backlog Until Its Design Settles

[E00](https://github.com/m2ux/prosiform/issues/21) takes Backlog on the theme board and no work is dispatched from it.

Two of its three open rows had started and were stopped. Their work survives on the branches it was committed to, and no row is held:

| Row | Where its work rests |
| --- | --- |
| W02 Fixture capture | [`i01/e00/w02-fixture-capture-from-a`](https://github.com/m2ux/prosiform/tree/i01/e00/w02-fixture-capture-from-a) — the work item, and a shared build-invocation seam in `checks/runner.py`. The capture command and its reduction are unwritten. |
| W03 Run record | [`i01/e00/w03-run-record-counted-against`](https://github.com/m2ux/prosiform/tree/i01/e00/w03-run-record-counted-against) — the work item, `ledger/run.schema.json`, `checks/ledger.py` reading run records, and 56 passing ledger tests. `make check` was interrupted, so the full set is unconfirmed. |

W01 remains delivered by [PR #324](https://github.com/m2ux/prosiform/pull/324): `ledger/` with the entry schema and the exposure set, and `make ledger`.

## Why It Parks

**The design is not settled enough to deliver.** Three points were undecided when delivery began:

- **Nothing writes to the ledger.** No step in a procedure tells an agent to record a finding, `pf` takes no ledger option, and no workspace rule mentions the folder. The epic's Problem — a surprise is absorbed by the nearest workaround — holds as written.
- **No resolution state exists.** The entry schema declares seven fields with `additionalProperties: false` and carries no field for resolved or deferred, so the lifecycle's last two steps have no representation. The freeze condition in [I01](https://github.com/m2ux/prosiform/issues/20) cannot be read against an entry.
- **The record's writer is external and undefined.** A packaged `pf` resolves outside the repository and can write no ledger, so the run record depends on a wrapper or an agent that nothing specifies.

Each is a design question about the ledger, not a defect in a delivered row.

## What This Leaves Open

I01's goal ends when every ledger entry is resolved or deferred and design and corpus carry one tagged revision, so its AC1, AC2, AC5, AC7 and AC9 read the ledger, and E13's freeze does. The initiative cannot complete as written while E00 is parked. That is left as it stands for the user to decide; this record changes no criterion.
