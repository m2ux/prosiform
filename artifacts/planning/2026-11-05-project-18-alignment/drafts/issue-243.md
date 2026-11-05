## Overview

A behaviour change moves what the build produces, and the corpus states what it produced before. Triage names each stale fixture under the category its difference falls in, so a change accepts the drift it intended and leaves every other category for a reader. Restatement is a separate task and does not live here.

## Problem

Bringing `main` back from a red run took two hand-written scripts and one judgement no script made.

- **A rewrite at fixture scale is unreviewable by hand.**
  186 fixtures failed that run, and reading 186 diffs by hand is what a maintainer does instead of reading the one that matters.

- **Nothing distinguishes accepting intended drift from accepting all of it.**
  Without a category to select on, a rewrite takes everything a red run names, including the fixtures whose clauses the change was not about.

- **The useful script is unreachable.**
  `scripts/regenerate.py` was committed with the fix and a second copy was written for the planning record, so the next red run writes a third.

## Proposal

- **Drift is classified before a byte is compared.**
  Triage reports whether lines were inserted, removed, both, or rewritten in place, per fixture, under the declared categories.

- **A category can be selected.**
  `--only` limits the triage report to the selected category; the report leaves fixture content untouched.

- **The tool lives where the corpus maintains itself.**
  Triage joins `checks/`, imports the same `runner.py` the corpus uses, and is named in `checks/README.md` beside the checks it serves.

- **Scope boundary.**
  Triage reports and classifies; it adjudicates nothing. Whether a difference is drift or a defect is the reader's judgement.

## Acceptance Criteria

- [ ] **AC1.** Triage reports each fixture's difference as one declared category, and a run over a corpus holding one of each category names each fixture under its own, as that run shows.
- [ ] **AC2.** `--only` reports fixtures in the selected drift category alone, as a run over a corpus holding two categories with one selected shows.
- [ ] **AC3.** A green corpus run produces no drift report, as the tool run over `make corpus`'s passing tree shows.

## References

- **R1.** [Preserved tools and their evidence](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-24-corpus-drift-tools) — the two scripts as the session wrote them, with the runs that establish each property.
- **R2.** [Corpus runner](https://github.com/m2ux/prosiform/blob/main/checks/runner.py) — the run and comparison the tool reads its verdicts from.
- **R3.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-24-243-i01-e03-w13-drift-triage) — the work item for this row and the one after it.
