# Validation

## Design inspection

Revision under test: engineering `5af5013aa70c627675243713017c3db394971701`; the README Design link on `i10/e03/w00-design-clause` names it.

- Post-compilation invariants lists **One destination answers one member** after **Destination stability**, citing the grouping clause *A heading for every member*.
- Every clause title the design carried at the previous pin is present; no clause title changed. Observes AC1.

## Make check

`make check` with `PROSIFORM_BUILD` set, in the task worktree at the new pin: 1265 harness tests passed, and the vocabulary, corpus, conformance and independence targets passed (357 clauses the design states, 0 declarations naming no clause). Observes AC1.

## Changes

- Applied: none.
- Held: none.
