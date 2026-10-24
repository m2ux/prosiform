# W13 and W14: Drift Triage — October 2026

> Plan · Created 2026-10-24

## Executive Summary

Two tools keep the corpus honest after a behaviour change. Triage names each stale fixture under the category its difference falls in, so a change accepts the drift it intended rather than every fixture a red run touched. Restatement writes exactly two things and refuses a fixture whose run failed in itself.

This record carries the planning for [W13](w13.md) and [W14](w14.md) under [E03 Carried Debt](https://github.com/m2ux/prosiform/issues/187). The work is raised as [#243](https://github.com/m2ux/prosiform/issues/243), which states W13's criteria and keeps the evidence both rows came from.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W13](w13.md) | Triage: the categories, the selection flag, and the guide entry |
| [W14](w14.md) | Restatement: the dry default, the two files written, and the refusal |

## Evidence

The red run that drove this preceded [#244](https://github.com/m2ux/prosiform/pull/244), the merge that restored `main`. The preserved scripts are in [corpus drift tools](../2026-10-24-corpus-drift-tools/README.md).

- 186 fixtures failed that run.
- Re-rendering the manifest from parsed TOML escaped every em dash in 177 manifests.
- Two copies of `scripts/regenerate.py` exist, neither reachable from `checks/README.md`.

## Row Joins

W13 and W14 both write under `checks/`, and W14 reads the categories W13 declares, so W14 depends on W13 rather than joining it.

- **W01 and W13.** W01 reads `checks/documents.py`, which neither tool imports.
- **W02 and W13.** W02 adds a module under `checks/` and its tests. Triage imports `runner.py`, which W02 does not change.
- **W03 and W13.** W03 writes `fixtures/` and the corpus guide. W13 writes `checks/triage.py` and one guide entry, and neither reads the other's statement.
- **W04 and W13.** W04 gives one repository document a tracker reference. W13 reads none.
- **W05 and W13.** W05 writes `design.md` and `docs/glossary.md`, both on the contract branch. W13 writes neither.
- **W06 and W13.** W06 changes `checks/independence.py`, which neither tool imports.
- **W07 and W13.** W07 changes `checks/independence.py` and one fixture declaration. W13 changes no declaration.
- **W08 and W13.** W08 changes `checks/corpus.py` and writes both guides. W13 writes `checks/triage.py` and one guide entry, and the two entries sit in different sections of the guide.
- **W09 and W13.** W09 adds a repository check for build tags. W13 adds no check.
- **W10 and W13.** W10 changes the checks that read this repository's documents. W13 reads the corpus, not the documents.
- **W11 and W13.** W11 changes a check reading the contract branch. W13 reads no branch of that kind.
- **W12 and W13.** W12 changes `.github/workflows/checks.yml`, `Makefile` and `checks/runner.py`; W13 imports the result type W12 gives three states. W13 depends on W12 and does not join it.

## Links

| Resource | Link |
| --- | --- |
| Issue | [#243](https://github.com/m2ux/prosiform/issues/243) |
| Epic | [E03 Carried Debt](https://github.com/m2ux/prosiform/issues/187) |
| Initiative | [Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Preserved tools | [Corpus drift tools](../2026-10-24-corpus-drift-tools/README.md) |
