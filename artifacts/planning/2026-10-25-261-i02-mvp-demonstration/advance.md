# Advance

The queue decision after the first sync, and the label correction that preceded it.

## The label convention this board uses

A larger `priority:` number is earlier work, confirmed against the prototype initiative, where Deferred Debt carries `priority: 1` and the first epic carries `priority: 8`. The labels written during the planning run were inverted: they treated 1 as first. That put Deferred Debt ahead of the demonstration, and put the initiative at `priority: 1`, the lowest rank, while the initiative that already runs held `2`.

Corrected labels:

| Issue | Was | Now |
| --- | --- | --- |
| `#261 [I02]` | `priority: 1` | `priority: 8` |
| `#258 [I02:E00]` Example Migration | `priority: 2` | `priority: 3` |
| `#262 [I02:E01]` Demonstration Ground | `priority: 1` | `priority: 2` |
| `#263 [I02:E02]` Deferred Debt | `priority: 3` | `priority: 1` |
| `#20 [I01]` | `priority: 2` | `priority: 5` |

The maximum available label is 8, so the demonstration takes it and the refinement initiative moves below it into the 5–6 band its open epics already occupy. The user confirmed the epic order: migration first, then the ground, then the debt.

## Applied queue

| Issue | Move |
| --- | --- |
| `#261 [I02]` | Backlog → In Progress, assigned `m2ux` |
| `#258 [I02:E00]` | Backlog → Ready, assigned `m2ux` |
| `#20 [I01]` | In Progress → Ready |
| `#10 [I03]` | Ready → Backlog, unassigned |

The refreshed queue is current and carries one `next` line: `#261: E00`.

## What the queue says

- **`I02` is the initiative underway.** It holds the highest rank, and its first epic is the one that starts.
- **`I01` is next.** It moves to In Progress when `I02` completes.
- **`I03` waits.** It holds the lowest rank, so its work does not compete with the demonstration.
- **`I02:E01` and `I02:E02` wait behind `E00`.** The ground epic ranks below the migration and above the debt, which is the order the user confirmed.
