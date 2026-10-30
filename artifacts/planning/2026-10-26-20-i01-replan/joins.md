# Joins

Pairs the re-plan made, or left, eligible to share a pull request, and why each keeps its own.

| Pair | Decision | Reason |
| --- | --- | --- |
| E00:W02 and E00:W03 | Separate | The capture tool and the run record extend different components; the capture tool reads a recorded entry, which the run record does not need. |
| E00:W02 and E00:W04 | Separate | W04 writes ledger content; W02 builds the tool that reduces it. Joining them would deliver data and tooling under one set of criteria. |
| E01:W02 and E01:W03 | Separate | Traceability regeneration reads the design and corpus; the open-finding summary reads the ledger. |
| E01:W02 and E01:W04 | Separate | W04 changes skills in another repository and keeps only its record here. |
| E01:W03 and E01:W04 | Separate | W04 changes skills in another repository and keeps only its record here. |

E03's pairs are accounted for in [Row joins](../2026-10-21-187-i01-e03-carried-debt-joins/). E12's rows each depend on the one before, so none is eligible.
