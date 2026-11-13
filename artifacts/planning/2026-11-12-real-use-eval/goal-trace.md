# Goal Trace

## Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| A session starts from a skill placed where its CLI discovers skills | AC1 | E00, E01 | E00 AC1, AC2; E01 AC1–AC5 | Decisions 1, 3, 4 and 11 |
| The session opens with its task in plain words | AC2 | E00, E01 | E00 AC4; E01 AC6 | Decisions 2 and 9 |
| The CLI's own skill mechanism is the only disclosure; the eval adds nothing | AC2 | E00 | E00 AC3, AC4 | Decisions 1, 8 and 9 |
| A bare prompt naming an entry file is not an eval | AC2, AC4 | E01, E02 | E01 AC6; E02 AC1 | Decisions 5 and 10 |
| The comparisons stay, each behind a skill | AC3 | E01 | E01 AC1–AC5 | Decision 3 |
| One baseline is measured on the skill-entry eval, over every workflow | AC5 | E02 | E02 AC2, AC3 | Decisions 5 and 14 |

The marked source is the record's [decisions](decisions.md), Confirmed 1 to 15.

## Gaps

Ranked; the flagged ones most threaten the goal.

1. **Resolved.** The tracing duty had no home; decision 9 puts it in a paragraph every variant's `SKILL.md` shares, and E00 W03 writes it.
2. **Resolved.** Retiring the bare-prompt path in E00 left families unrun; decision 10 moves it to E01 W06, after every family row.
3. **Flagged: discovery depends on harness flags.** The Claude harness disables skills today; E00 AC3 holds the change, and a host-managed configuration still reaches sessions, recorded by count and fingerprint as the README states.
4. **Flagged: the eval runs mixed while E01 is open.** Converted families run as skills and the rest on bare prompts; a run in that window is no baseline, and E02 starts only after E01 W06.
5. **Noted: the downstream edge.** The agent-pick remeasurement waits on E02 W02 (decision 13).
6. **Open, flagged: two composition workflows lack a criterion.** E01 W04 converts `conditional-composition`, `directive-labels`, `dispatch-depth` and `subagent-first-run`; E01 AC4 names the last two alone, so initiative AC1 is not wholly made true for the first two.
7. **Open: the tracing duty has no criterion.** Decision 9 and E00's Proposal put the shared tracing paragraph in every variant's `SKILL.md`; E00 W03 writes it, and no E00 criterion holds it.
8. **Open: E00 AC1 reads two ways.** "The eval's harnesses are the agent CLIs whose documentation states native skill discovery" can also require every such CLI to become a harness.
9. **Open: E02 W02 is design and a paid run.** The runbook section is design work and its shakedown a run under the runbook, while the Joins line splits W01 from W02 on that same distinction.
10. **Open: initiative AC4 and AC5 restate E02 AC1 and AC3.** AC5 also omits decision 14's every workflow, which E02 AC3 alone states.

## Outside Threats

- **Readers of the changed surface.** `make eval-harness` and the `checks.yml` dispatch run the eval's tests; `report.py` reads `baseline.json` and reads `—` with none, so E02 W01 leaves it working before W03 writes the new one.
- **Fail-closed paths.** After E01 W06 the corpus test refuses a workflow with no skill texts, so no workflow silently drops out of the matrix.
- **Instrument independence.** The baseline is fixed by E02 W03 after E01 lands, and the scorer, not the harness, decides each verdict.
- **Ground shift.** I15's `?` pick and guide land on main through I15; the deferral row converts `agent-pick` as it stands when E01 starts.

## Checks

- Format: the initiative and the three epic drafts report nothing to fix, apply or decide.
- Dependencies: no problems; every candidate unit is named on a record line in [decisions](decisions.md#joins), and E02 W01 with W03 is split by rule.
