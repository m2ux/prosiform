## Overview

This epic finishes the reading the repository checks share and the vocabulary rules they apply. The check gaps epic found four more cases while closing its own: two checks still find code blocks their own way, the build-word rule refuses ordinary words, the documentation states avoided terms no check reads, and the documentation defines a document boundary the build does not compute. Within the initiative it is the last of the work that makes every check exact.

## Problem

- **Two checks keep their own fence reading.**
  [The vocabulary check](https://github.com/m2ux/prosiform/blob/798f11ed93a0f265ac28b1b0a167f2b7edf9337a/checks/vocabulary.py#L41) and [the conformance report](https://github.com/m2ux/prosiform/blob/798f11ed93a0f265ac28b1b0a167f2b7edf9337a/checks/conformance.py#L102) match a fence at the left margin, so an indented fence in the design is read for terms and clauses.
- **An ordinary word becomes a build word.**
  Any word only a section stating no behaviour carries is refused, so "yet" failed two fixture descriptions once a build sentence moved, and the sentence was reworded to pass.
- **The documentation states avoided terms no check reads.**
  Pages under `docs/` write terms the glossary names as deliberately not used, among them "includes" in `docs/composition.md`, and the vocabulary rules read the design and the corpus alone.
- **The documentation defines a boundary the build does not compute.**
  [`docs/sources.md`](https://github.com/m2ux/prosiform/blob/798f11ed93a0f265ac28b1b0a167f2b7edf9337a/docs/sources.md#L36-L38), the glossary and the output-budget page define a document's boundary, and nothing in the build has derived one since its last caller went.

## Proposal

- **Every check reads code blocks through the shared reading.**
  The vocabulary check and the conformance report blank code blocks with the reading the link and table checks use, and their own fence patterns go.
- **A build word is a marked term.**
  A section stating no behaviour contributes the terms it marks, as code or as a defined term, not every word of its prose.
- **The documentation obeys the avoided-term rule.**
  The vocabulary check reads every page under `docs/` for avoided terms, the glossary's own table excepted, and each page stating one is reworded.
- **The documentation states what the build computes.**
  The boundary leaves the documentation; the working directory, which the pages already state, is what confines a run.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e03-check-refinements/w01.md) | Every check reads the shared code-block reading | AC1 | | W03 | | |
| [W02](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e03-check-refinements/w02.md) | Build words are marked terms | AC2 | | | | |
| [W03](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e03-check-refinements/w03.md) | Avoided terms in the documentation | AC3 | | W01 | | |
| [W04](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e03-check-refinements/w04.md) | The documentation without a boundary | AC4 | | | | |

## Acceptance Criteria

- [ ] **AC1.** The vocabulary check and the conformance report pass over a fenced block indented inside a list item of the design, as their tests show.
- [ ] **AC2.** A word a section stating no behaviour writes unmarked is not reported by the independence check, while a term that section marks is, as its tests show.
- [ ] **AC3.** No page under `docs/` states a term the glossary names as deliberately not used, outside the glossary's own table, as the vocabulary check over the repository shows.
- [ ] **AC4.** No page under `docs/` defines a document boundary the build does not compute, as a reading of the build's sources against `docs/sources.md`, `docs/glossary.md` and `docs/output-budget.md` shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-26-770-i19-e03-check-refinements) — each row's work item, where its case was found, and the recommendation on the boundary.
