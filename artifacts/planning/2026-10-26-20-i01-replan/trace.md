# Goal Trace

The refinement goal traced after the re-plan. Clauses are the outcomes the initiative's Overview names.

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| What real use reveals is recorded and can be re-run | AC1, AC2, AC9 | E00 | E00 AC1–AC9 | R1 residual policy |
| An accepted finding changes the design, then the corpus, then the build | AC3, AC4, AC8 | E01, E02, E06, E09, E12 | E01 AC1–AC7; E12 AC1 | R1, R2 |
| The contract extensions this stage takes are settled | AC12, AC13, AC15, AC17 | E06, E09, E12 | E06, E09 all ticked; E12 AC2–AC6 | R5, R6, R7, R8 |
| Every entry is resolved or deferred, and design and corpus carry one tagged revision after the exposure set is bundled | AC5, AC6, AC7 | E13, with E00 declaring the set | E13 AC1–AC4; E00 AC6, AC9 | R1, R2 |
| The prototype's deferred debt is delivered or deferred | AC10 | E03 | E03 AC1–AC19 | — |
| The branch shape is held by the platform | AC16 | E10 | E10 AC1, AC2 | — |

## Gaps

Ranked, most threatening first.

1. **E01 W04 against E12.** Porting the example's grouping to the workspace skills before E12 changes it would be done twice. A row edge from E01 to E12 would point at a later epic, so the order is held by priority instead: E12 takes a higher priority than E01, and its three rows can start now while E01 W04 waits on the ledger.
2. **E12's open question.** How a parent assigns links to groups is undecided, and W01 cannot state the rule without it. It blocks delivery, not publication; the recommendation is in [R7](decisions.md#r7--how-a-parent-assigns-links-to-groups-is-open).
3. **AC16 traces to no Overview clause.** Branch protection was folded in from a standalone issue and is not a refinement outcome. It stays, as the initiative's standing home for repository configuration; no criterion depends on it.
4. **E03 W11's delivery is unrecorded.** Issue 204 is closed with its criterion unticked and no pull request of its own; a sync settles it.

## Outside Threats

- **The demonstration tag is fixed.** E12 W03 regenerates the example's usage fixtures and README excerpts; `demo/i02` keeps the revision it names, so the closed demonstration's evidence is unaffected.
- **The workspace skills live in another repository.** E01 W04's edits land there; the removal record here is the instrument, independent of the skill text it judges.
- **Source R8's root clause depended on cancelled work.** Issue 234 asks leaves to stop declaring a root on the strength of root inheritance, which R3 records as not planned. A Non-Goal excludes it, and E12 moves grouping alone.
