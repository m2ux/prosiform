Closed as not planned: superseded.

- **The freeze gate reads a ledger that never reached `main`.** Its check refuses a tag until every ledger entry is resolved and every exposure-set source has a run record; #21 and #22, which supply both, are closed as not planned.
- **Tagged contracts exist.** Each release cuts a paired `contract/vX.Y.Z` and `python/vX.Y.Z` tag under `docs/versioning.md`, so a later build can name a released contract tag as its target.
- **Real-use evidence now comes from evals.** #734 (I16) and #768 (I18).

Record: https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-13-20-i01-retirement
