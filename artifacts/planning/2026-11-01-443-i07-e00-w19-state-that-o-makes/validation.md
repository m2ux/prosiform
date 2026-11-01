# W19 Validation

Checks the W19 work item names, run on branch `i07/e00/w19-state-that-o-makes`.

## T1 Search

Revision `48ec814d`.

- **Procedure.**  `grep -n -i -E "existing folder|must (already )?exist|which must exist|held to existing|already exist" README.md docs/bundles.md invocation.md src/prosiform/cli.py`, then `uv run --project src --frozen pf -h`.
- **Observation.**  The search finds no line (grep exit 1). `pf -h` describes `-o DIR` as "folder the run's own folder of bundles is written into, made if absent, swapped in whole; default: the working directory". Each edited page now states the folder is made if absent, matching the help text and `publication`, which makes the folder and its parents.
- **Result.**  Holds. Observes AC30.

## T2 Make Check

Revision `48ec814d`.

- **Procedure.**  `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` in the worktree.
- **Observation.**  Exit 0. Every target passed, among them the corpus, the invocation check of `invocation.md` against `pf -h`, conformance, independence and the mock scenarios.
- **Result.**  Holds.
