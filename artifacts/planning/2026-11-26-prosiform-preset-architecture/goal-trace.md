# Goal Review

## Trace Table

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| Scrutinise every proposed form as files before its contract | AC5 | E00 | E00 AC1–AC5 | [scope.md](scope.md) clause 1 |
| Inspect the exact effective configuration behind a build, unpublished too | AC1, AC3 | E01, E02, E03 | E01 AC1–AC5; E02 AC4; E03 AC4 | [scope.md](scope.md) clause 2 |
| Hold a published set to its record | AC6 | E01 | E01 AC7 | [scope.md](scope.md) clause 2 |
| Reuse narrowly scoped level and substitution settings | AC2, AC3 | E02 | E02 AC1–AC3 | [scope.md](scope.md) clause 3 |
| Select independent local component and test alternatives | AC2, AC3 | E03 | E03 AC1–AC6 | [scope.md](scope.md) clause 4 |
| List a document's choices without bundling it | AC7 | E03 | E03 AC8 | [scope.md](scope.md) clause 4 |
| Preserve readable authored policy and observable outcomes | AC4 | E01, E02, E03 | E01 AC6; E02 AC5; E03 AC7, AC9 | [scope.md](scope.md) clause 5 |

Every epic criterion has one delivering task row; every task has at most three criteria.

## Review Of 2026-11-27

Findings of the review against pf 0.36.0, each with its evidence and disposition.

### Baseline

- **The control was labelled as a release it was not.** `191c0cf8d` describes as `contract/v0.34.0-15`, and docs were linked at `794922d41`, `contract/v0.35.0-19`. Every label and link names 0.36.0. The five controls were re-run under `pf 0.36.0`; exit status, diagnostics and bundle hashes are identical.
- **The plan used avoided terms.** `docs/glossary.md` at 0.36.0 lists `compile` and `compiler` as terms deliberately not used, and `checks/vocabulary.py` fails a page stating one. The bodies and work items use the bundler vocabulary.

### Tracker

- **A dependency was already delivered.** #865 is a docstring hot-fix merged ahead of 0.36.0. Its edge and reference are gone.
- **One word named two things.** `fixtures/manifest.schema.json`, each fixture's `manifest.toml` and `checks/manifests.py` already hold "manifest". The file is the ledger.

### Work Items

- **No row declared a corpus fixture.** Initiative AC1 to AC3 cite the corpus. The fixture schema's `expected` holds exit status, bundles, standard-output text and diagnostics, so a fixture could not state a ledger. Each admitting row declares its fixtures, and the ledger publication row extends the fixture schema and the corpus runner.
- **An option landed apart from its table row.** `checks/invocation.py` compares the help output and the options table in both directions, and `make check` runs it. The row adding an option now states it in `invocation.md`.
- **No row moved the design link.** `checks/conformance.py` reads the contract at the README's design link and holds its codes to `pf -C` in both directions. Each admitting row moves the link and carries the code entries; verification and listing state their own clauses.
- **Example checks were declared in the wrong home.** The existing example check is `src/tests/test_example_project_lifecycle.py`. The three example checks follow it.
- **Two edges gated a row on output it does not use.** Import capture no longer waits on the ledger projection, nor the group resolver on import wiring, nor the group guide on the import guide.

### Design

- **Seven points were unstated.** [design.md](design.md#open-design-points) lists them; each feature epic carries its own as open questions, and the scrutiny ruling settles them before the first contract row.

### Structure

- **No stage showed the design as files.** Design Specimens is the first epic. Its three set rows start together.
- **Lanes were declined for the wrong reason.** A lane marks model class. Every row carries one of two lanes.

## Standing

No content or structural finding remains open in the drafts. Open design points are carried as each epic's open questions and are resolved by the scrutiny ruling.
