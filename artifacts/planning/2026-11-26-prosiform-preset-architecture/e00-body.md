## Overview

The requester can read every proposed form as files before any contract states it: sources written in the form, the output each should produce, and what the 0.36.0 release already bundles. Each set ends in an accept-or-change ruling that the later contract work follows.

## Problem

- **Proposed forms exist only as prose.**
  The ledger, import and choice-group designs are described in the planning record, with no source or output file showing them.
- **Open design points are not visible.**
  Refusal codes, the budget and warning treatment of imported settings, bundle names under two groups and the ledger's fields are unstated.
- **A contract written first fixes an unseen design.**
  A form rejected after its contract is written costs the contract text and the fixtures drawn from it.

## Proposal

- **One set per feature.**
  Each set holds sources in the proposed form, the expected output, the nearest build the 0.36.0 release accepts, and a README naming what the form needs from the bundler.
- **Real and hand-written output stay apart.**
  Output the 0.36.0 release wrote is retained with its command and diagnostics; every hand-written file says so in its first line.
- **A combined set.**
  One run shows imports feeding grouped alternatives with its ledger, and states each open design point with its candidate answers.
- **A recorded ruling.**
  Each set carries the requester's accept-or-change ruling, and a changed form is restated in the design before contract work starts.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/commit/90fb5502c2e0967c2216df208c14d00a2f6099c6) | Ledger specimen set | AC1 | | | 1 | ✓ |
| [W01](https://github.com/m2ux/prosiform/commit/90fb5502c2e0967c2216df208c14d00a2f6099c6) | Preset import specimen set | AC2 | | | 1 | ✓ |
| [W02](https://github.com/m2ux/prosiform/commit/90fb5502c2e0967c2216df208c14d00a2f6099c6) | Choice group specimen set | AC3 | | | 1 | ✓ |
| [W03](https://github.com/m2ux/prosiform/commit/90fb5502c2e0967c2216df208c14d00a2f6099c6) | Combined specimen set and open points | AC4 | W00, W01, W02 | | 1 | ✓ |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture/e00/w04.md) | Scrutiny ruling folded into the design | AC5 | W03 | | 1 | |

## Acceptance Criteria

- [x] **AC1.** Each proposed ledger behaviour among fields, check-mode output, verification outcome and refusal is shown as a file marked real or hand-written, as the ledger set's README inventory shows.
- [x] **AC2.** Each proposed import behaviour among valid reuse, refusal and the inline control its bundles must equal is shown as a file marked real or hand-written, as the import set's README inventory shows.
- [x] **AC3.** Each proposed choice-group behaviour among explicit selection, an open pick, refusal and the preset listing is shown as a file marked real or hand-written, as the choice-group set's README inventory shows.
- [x] **AC4.** The combined set shows the three features in one run and states each open design point with its candidate answers, as its README shows.
- [ ] **AC5.** Each specimen set carries the requester's accept-or-change ruling and each changed form is restated in the design, as the planning record's decisions show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-prosiform-preset-architecture) — the scope, the proposed design and the specimen sets.
- **R2.** [Source metadata at 0.36.0](https://github.com/m2ux/prosiform/blob/8cedda4cc06b0486168addc05f057161192a22a6/docs/sources.md#frontmatter) — the fields the proposed forms extend.
