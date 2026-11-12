# Goal Trace

## Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| A session starts from a skill placed where its CLI discovers skills | AC1 | E00, E01 | E00 AC1, AC2; E01 AC1–AC5 | Decisions 1, 3 and 4 |
| The session opens with its task in plain words | AC2 | E00 | E00 AC4 | Decision 2 |
| The CLI's own skill mechanism is the only disclosure; the eval adds nothing | AC2 | E00 | E00 AC3, AC4 | Decisions 1 and 8 |
| A bare prompt naming an entry file is not an eval | AC2, AC4 | E00, E02 | E00 AC5; E02 AC1 | Decision 5 |
| The comparisons stay, each behind a skill | AC3 | E01 | E01 AC1–AC5 | Decision 3 |
| One baseline is measured on the skill-entry eval | AC5 | E02 | E02 AC2, AC3 | Decision 5 |

The marked source is the record's [decisions](decisions.md), Confirmed 1 to 8.

## Gaps

Ranked; the flagged ones most threaten the goal.

1. **Flagged: the tracing duty has no home.** The scorer needs `trace.log`, and the plain-words prompt carries no instruction; until the open question is settled, E00 W03 cannot state where a session learns to trace without adding to the CLI's disclosure.
2. **Flagged: E00's retirement leaves families unrun.** Retiring the bare-prompt path before E01 converts the families removes their sessions; E00 W04 restricts the matrix to skill workflows so nothing runs half-converted (finding 1).
3. **Flagged: discovery depends on harness flags.** The Claude harness disables skills today; E00 AC3 holds the change, and a host-managed configuration still reaches sessions, recorded by count and fingerprint as the README states.
4. **Noted: the baseline's matrix.** Whether the edge workflows join the baseline is finding 8; either answer keeps AC5 true.
5. **Noted: I14 plans bare-prompt edge records** this initiative deletes (finding 6).
6. **Noted: the downstream edge.** The agent-pick remeasurement waits on E02; its row-level edge is finding 7.

## Outside Threats

- **Readers of the changed surface.** `make eval-harness` and the `checks.yml` dispatch run the eval's tests; `report.py` reads `baseline.json` and reads `—` with none, so E02 W01 leaves it working before W03 writes the new one.
- **Fail-closed paths.** A workflow without skill texts gives no session rather than a bare-prompt one; the corpus test must refuse such a workflow in the default matrix so the restriction is not silent.
- **Instrument independence.** The baseline is fixed by E02 W03 after E01 lands, and the scorer, not the harness, decides each verdict.
- **Ground shift.** I15's `?` pick and the guide land on main through I15; the deferral row converts `agent-pick` as it stands when E01 starts.

## Checks

- Format: the initiative and the three epic drafts report nothing to fix, apply or decide.
- Dependencies: no problems; every candidate unit is joined or named on a record line in [decisions](decisions.md#joins), and E02 W01 with W03 is split by rule.
