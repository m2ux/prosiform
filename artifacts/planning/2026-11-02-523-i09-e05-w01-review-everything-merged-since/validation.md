# Validation

Evidence for AC1 and AC2 at `main` 74b00cd9 and design 4958ad38.

## AC1

- **Every changed clause has a row.** The clause diff between `21f4687d` and `4958ad38` yields 166 changed or added clauses and 32 retired ones. A read of the review's Clauses table against that list finds 166 rows, none missing, and no empty Code, Evidence or Verdict cell.
- **Every code citation resolves.** Each function or constant a row cites is defined in the module it names under `src/prosiform/`.
- **The build passes its corpus.** `make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'` exits 0: 498 of 498 fixtures, 1161 build tests, 1663 check tests; `make conformance` reports 59 clauses no fixture names across the whole design, each changed one among them carrying a probe, a code read or the families its case list names in the review.
- **Probes.** Run in scratch trees against the same build; each is stated in the row it evidences and in the review's *Where the Epics Meet*.
- **Second reading.** The session re-read four departing rows and a sample of meeting rows against the design text and the probes; the brief forbids dispatching a second agent.

## AC2

- **Each finding is a row.** F1 is W30 (AC34), F2 W31 (AC35), F3 W32 (AC36) in #523's Work Breakdown.
- **The body holds its format.** `format.py` on the revised #523 with the initiative and the workspace's required criteria: 0 fixed, 0 to apply, 0 to decide.
- **The graph holds.** `deps.py` over #463, E02, E04, the revised E05 and the W01, W30–W32 work items reports no problem on an E05 row; W30–W32 form one joined unit; W30's numbering after W29 is advisory. The problems it reports sit on E04 W10 and the initiative's E05 row, which this row does not own.
