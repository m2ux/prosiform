---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Plan Change

One change to the plan that a run makes as it works, and whether the run applies it or the user decides it.

## Operations

### *Check* Plan Change Autonomy

One pending change assessed against the run's allowance.

**Inputs:** The pending change, its subject, the option recommended for it, and the allowance the caller was supplied.

1. Match the change to one kind in [Change Kinds](#change-kinds).
2. Return it as automatic where the supplied allowance names that kind, with the supplied recommendation as the option the caller applies.
3. Return it as [held](#held-change) otherwise.
   - A change matching no kind is held, as is one matching [Initiative Creation](#initiative-creation).
   - An absent allowance holds every change, so a run the user drives decides nothing on their behalf.

### *Record* Plan Change

One entry in the run's list, for a change it applied or held.

**Inputs:** The change, its kind, the option applied or recommended, the affected issue identities and the run's current list.

1. Add one entry meeting [Entry](#entry) to the supplied [Change List](#change-list), marked applied or held.
2. Return the updated list for the caller to publish and report.

### *Settle* Plan Change

One pending change carried to its outcome: applied, held, or answered by the user.

**Inputs:** The pending change, its subject, the option recommended for it, the affected issue identities, the allowance the caller was supplied, and the run's current [Change List](#change-list).

1. Apply [Check Plan Change Autonomy](#check-plan-change-autonomy) with the change, its subject, the recommended option and the supplied allowance.
2. Settle the change by what it returns:
   - **Automatic.**
     - Take the recommended option as the applied option.
     - Apply [Record Plan Change](#record-plan-change) with the change, its kind, that option, the affected issue identities and the current list, marked applied.
   - **Held, with an allowance supplied.**
     - Leave the change unapplied, meeting [Held Change](#held-change).
     - Apply Record Plan Change with the change, its kind, the recommended option, the affected issue identities and the current list, marked held.
     - Ask nothing, since the work the run was dispatched for does not wait on an answer.
   - **Held, with no allowance supplied.**
     - Put the change to the user as an [interview](../rules.md), with the recommended option marked, and wait for the answer.
     - Where the answer applies a change, apply Record Plan Change with the change, its kind, the option the user chose, the affected issue identities and the current list, marked applied.
     - An answer leaving the work where it is takes no entry, as [Change Kinds](#change-kinds) states.
3. Return the applied option, held, or the user's answer, with the updated change list.

## Fields

### Allowance

The caller names the change kinds its run applies without asking. A run the user drives directly is supplied none.

### Change Kinds

| Kind | What It Covers |
| --- | --- |
| Task creation | A new task row, and the task issue that delivers it |
| Epic creation | A new epic, and the initiative row that carries it |
| Migration | Work moved from one issue to another, with the renumbering that move forces |
| Re-prioritisation | A priority label, a queue order or a board status |
| Folded work | Criteria, scope or design added to an existing issue because the work in hand needs it |

An option deciding to leave work where it is changes no plan, so it needs no allowance and takes no entry, unlike a change [held](#held-change) for the user to decide.

### Initiative Creation

A new initiative is outside every allowance. The work stays where it is, open and unplaced, until the user decides where it belongs.

### Change List

One list for the run, holding every change it applied and every change it held. It is what the run reports and what its record keeps.

### Entry

One line: the kind, the issue or row it concerns, and the option applied or recommended. The entry states the change, not the alternatives weighed against it.

### Held Change

A held change is left unapplied and its subject stays as it stands, so the next run sees the same decision. Its entry carries the recommended option, which is what the user is answering.
