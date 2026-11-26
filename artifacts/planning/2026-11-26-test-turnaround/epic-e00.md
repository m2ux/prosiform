## Overview

This epic holds the work on the repository's checks and on its design record that no run of the tool shows. Each row states a rule the design or a check makes imprecisely, and fixing it leaves what a person invoking the tool sees unchanged. The epic is where that work is planned, so each rule is stated once and the criteria that state it are read where the fix lands.

## Problem

Debt that impairs nothing still has to be somewhere, and placed beside product work it gates a delivery that does not need it.

- **A row whose fix no run can show gates a product that does not need it.**
  An initiative stays open while any of its rows is undelivered, so work measured by a check's own output rather than by what the tool does is the only thing between a working product and a closed initiative.

- **Repository checks and the design record are not the product.**
  The distribution ships `prosiform` alone. A check under `checks/`, a fixture declaration and the design record on the engineering branch are read by this repository and by a second implementor, and reach no-one who installs the tool. Measuring them by what a user would notice puts them outside the delivery that serves a user.

- **Work with no epic beside it is an orphan.**
  An issue that no initiative links waits for a later pass to find it a place, and until then nothing says when it is fixed or what fixing it makes true.

## Proposal

- **Each row keeps its own issue.**
  A row's issue, its problem and the criterion stating what fixing it makes true stay together, so what the fix establishes is readable where the work is planned.

- **The checks are their own initiative.**
  Each row here is a statement the design or a check makes imprecisely, so the rows share one goal: every check reports what it claims to and refuses what it claims to refuse. Held apart from product deliveries, the work meets the material it concerns rather than competing with a release.

- **Product-side work belongs to a delivery epic.**
  A fix a person invoking the tool would meet — a crash on ordinary syntax, a document lost from a bundle, a source's newline spelling rewritten — is planned where it ships.

- **A row's placement here is not a judgement that it is small.**
  It is a judgement that no run of the tool shows it. A row whose fix proves to change what a run produces belongs to a delivery epic.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/issues/158) | A code block indented inside a list item | AC1 | | | | |
| [W02](https://github.com/m2ux/prosiform/issues/160) | Uncalled functions named only by a check | AC2, AC23 | | | | |
| [W04](https://github.com/m2ux/prosiform/issues/162) | Tracker route exercised by the repository check | AC4 | | | | |
| [W06](https://github.com/m2ux/prosiform/issues/185) | Lowercase build words in the design | AC7 | [I00:E11:W34](https://github.com/m2ux/prosiform/issues/39) | W07 | | |
| [W07](https://github.com/m2ux/prosiform/issues/186) | An avoided term in a corpus declaration | AC8 | [I00:E11:W34](https://github.com/m2ux/prosiform/issues/39) | W06 | | |
| [W08](https://github.com/m2ux/prosiform/issues/189) | One fixture run by its identity | AC9 | | | | |
| [W09](https://github.com/m2ux/prosiform/issues/191) | Build tags matching the reported version | AC10 | | | | |
| [W10](https://github.com/m2ux/prosiform/issues/193) | A document present and not read | AC11 | | | | |

## Acceptance Criteria

- [ ] **AC1.** A code block indented inside a list item is passed over by the link check while that item's own content, a nested bullet included, is read, as the shared reading's own tests show.
- [ ] **AC2.** Every function and method `src/prosiform` defines is named by the package itself or by a stated reason it is reached from outside it, as a repository check run by `make check` shows.
- [ ] **AC4.** An online run of the link check over the repository's own documents makes at least one tracker call and resolves it, as the check's own output naming that reference shows.
- [ ] **AC7.** A fixture declaration or a report entry naming a word that only a section of the design stating no behaviour carries is reported, as the independence check over a corpus declaring one shows.
- [ ] **AC8.** A fixture declaration stating a term `docs/glossary.md` names as deliberately not used is reported with the reason that table gives, as the independence check shows.
- [ ] **AC9.** The corpus runner asked for one fixture by its identity reports that fixture's verdict under that identity, by the comparison the corpus run performs, and refuses an identity no fixture carries, as the corpus harness shows.
- [ ] **AC10.** A commit carrying a build tag whose version the build does not report fails a repository check, and a commit carrying a build tag and a contract tag whose major and minor differ fails it, as that check's run over each case shows.
- [ ] **AC11.** A Markdown document present in the working tree and not tracked is read by the checks that read this repository's documents, or named by their run as present and unread, as those checks' run over a working tree carrying one shows.

- [ ] **AC23.** The delivery wrapper's place is stated where a reader of the package meets it, and the check treats it as that statement says, as the check's own tests and a reading of the README show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-13-20-i01-retirement) — why this epic forms its own initiative and the decisions behind it.
- **R2.** [Criticality assessment](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-21-163-i00-e11-w29-a-member-whose-whole/analysis.md#why-these-three-and-not-the-other-seven) — the reading behind this epic's boundary: the distribution ships `prosiform` alone, so a check under `checks/`, a fixture declaration and the design record on the engineering branch reach no user of the tool.
- **R3.** [Row joins](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-187-i01-e03-carried-debt-joins) — the clear-up epic each row is carried from, the component each row changes, the pair that shares a pull request, and the reason each other pair keeps its own.
- **R4.** [Versioning policy](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) — what the contract tag and each build tag assert.
- **R5.** [Board alignment](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-project-18-alignment/alignment.md) — the confirmed boundaries of the current diagnostic scope.

