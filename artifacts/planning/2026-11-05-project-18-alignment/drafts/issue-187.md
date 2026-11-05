## Overview

This epic holds the work on the repository's checks and on its design record that no run of the tool shows. Each row states a rule the design or a check makes imprecisely, and fixing it leaves what a person invoking the tool sees unchanged. The epic is where that work is planned, so each rule is stated once and the criteria that state it are read where the fix lands.

## Problem

Debt that impairs nothing still has to be somewhere, and the epic that collected it gates an initiative.

- **A row whose fix no run can show gates a product that does not need it.**
  An initiative stays open while any of its rows is undelivered, so work measured by a check's own output rather than by what the tool does is the only thing between a working product and a closed initiative.

- **Repository checks and the design record are not the product.**
  The distribution ships `prosiform` alone. A check under `checks/`, a fixture declaration and the design record on the engineering branch are read by this repository and by a second implementor, and reach no-one who installs the tool. Measuring them by what a user would notice puts them outside the delivery that serves a user.

- **Work with no epic beside it is an orphan.**
  An issue that no initiative links waits for a later pass to find it a place, and until then nothing says when it is fixed or what fixing it makes true.

## Proposal

- **Each row keeps its own issue.**
  A row's issue, its problem and the criterion stating what fixing it makes true stay together, so what the fix establishes is readable where the work is planned.

- **Refinement is where they belong.**
  This initiative reads the design against real use and holds the corpus and the checks to what that use shows. Each row here is a statement the design or a check makes imprecisely, which is the same reading, so the work meets the material it concerns rather than competing with a delivery.

- **Product-side work belongs to a delivery epic.**
  A fix a person invoking the tool would meet — a crash on ordinary syntax, a document lost from a bundle, a source's newline spelling rewritten — is planned where it ships.

- **A row's placement here is not a judgement that it is small.**
  It is a judgement that no run of the tool shows it. A row whose fix proves to change what a run produces belongs to a delivery epic.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/issues/158) | A code block indented inside a list item | AC1 | | | | |
| [W02](https://github.com/m2ux/prosiform/issues/160) | Uncalled functions named only by a check | AC2 | | | | |
| [W03](https://github.com/m2ux/prosiform/issues/161) | A fixture for each group-rule fault | AC3 | | | | |
| [W04](https://github.com/m2ux/prosiform/issues/162) | Tracker route exercised by the repository check | AC4 | | | | |
| [W05](https://github.com/m2ux/prosiform/issues/177) | The options the design does not state | AC5, AC6 | [I00:E11:W24](https://github.com/m2ux/prosiform/issues/39) | | | |
| [W06](https://github.com/m2ux/prosiform/issues/185) | Lowercase build words in the design | AC7 | [I00:E11:W34](https://github.com/m2ux/prosiform/issues/39) | W07 | | |
| [W07](https://github.com/m2ux/prosiform/issues/186) | An avoided term in a corpus declaration | AC8 | [I00:E11:W34](https://github.com/m2ux/prosiform/issues/39) | W06 | | |
| [W08](https://github.com/m2ux/prosiform/issues/189) | One fixture run by its identity | AC9 | | | | |
| [W09](https://github.com/m2ux/prosiform/issues/191) | Build tags matching the reported version | AC10 | | | | |
| [W10](https://github.com/m2ux/prosiform/issues/193) | A document present and not read | AC11 | | | | |
| [W12](https://github.com/m2ux/prosiform/issues/255) | Whether a tree is sound | AC13 | | | | |
| [W13](https://github.com/m2ux/prosiform/issues/243) | A stale fixture classified before it is rewritten | AC14, AC15, AC16 | W12 | | | |
| [W14](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-24-243-i01-e03-w13-drift-triage/w14.md) | Restatement that writes only the expectation | AC17, AC18, AC19 | W13 | | | |

## Acceptance Criteria

- [ ] **AC1.** A code block indented inside a list item is passed over by the link check while that item's own content, a nested bullet included, is read, as the shared reading's own tests show.
- [ ] **AC2.** Every function and method `src/prosiform` defines is named by the package itself or by a stated reason it is reached from outside it, as a repository check run by `make check` shows.
- [ ] **AC3.** Each fault `E_INVALID_GROUP_RULE` names is stated by a corpus fixture that a build reporting another fault under that code fails, and the design's clause, the code's catalogue entry and the corpus guide name the same set, as the corpus run and the corpus guide show.
- [ ] **AC4.** An online run of the link check over the repository's own documents makes at least one tracker call and resolves it, as the check's own output naming that reference shows.
- [ ] **AC5.** The design record's CLI contract states the fault option and each fault name it declares, as the vocabulary check over the design and the repository's documented invocation table read together show.
- [ ] **AC6.** The design record's CLI contract states the option a build reports its codes on, as the vocabulary check over the design and the repository's documented invocation table read together show.
- [ ] **AC7.** A fixture declaration or a report entry naming a word that only a section of the design stating no behaviour carries is reported, as the independence check over a corpus declaring one shows.
- [ ] **AC8.** A fixture declaration stating a term `docs/glossary.md` names as deliberately not used is reported with the reason that table gives, as the independence check shows.
- [ ] **AC9.** The corpus runner asked for one fixture by its identity reports that fixture's verdict under that identity, by the comparison the corpus run performs, and refuses an identity no fixture carries, as the corpus harness shows.
- [ ] **AC10.** A commit carrying a build tag whose version the build does not report fails a repository check, and a commit carrying a build tag and a contract tag whose major and minor differ fails it, as that check's run over each case shows.
- [ ] **AC11.** A Markdown document present in the working tree and not tracked is read by the checks that read this repository's documents, or named by their run as present and unread, as those checks' run over a working tree carrying one shows.

- [ ] **AC13.** A tree's soundness is readable in one run: a pull request is checked whatever its branch is named, every failing target is named rather than the first alone, and a run that failed in itself is distinguished from one whose output moved, as `make check-all` over a tree with several failing targets and a corpus holding one crashing fixture shows.

- [ ] **AC14.** Triage reports each fixture's difference as one declared category, and a run over a corpus holding one of each category names each fixture under its own, as that run shows.

- [ ] **AC15.** `--only` restricts the rewrite to the category it names, as a run over a corpus holding two categories with one selected shows.

- [ ] **AC16.** A green corpus run leaves the tool reporting nothing to rewrite, as the tool run over `make corpus`'s passing tree shows.

- [ ] **AC17.** Restatement without `--write` leaves the working tree unmodified and names every fixture it would rewrite, as `git status` after a run over a corpus with one stale fixture shows.

- [ ] **AC18.** Restatement with `--write` replaces only the declared output and the `[expected]` block, as a manifest carrying a non-ASCII clause and a second declaration compared before and after shows.

- [ ] **AC19.** Both commands are reachable from the corpus guide and import the corpus's own runner rather than a copy of it, as the repository's file check and a read of the imports show.

## References

- **R1.** [#39 \[I00:E11\] Deferred Technical Debt](https://github.com/m2ux/prosiform/issues/39) — the clear-up epic the repository-side rows are stated against.
- **R2.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) — the initiative plan whose refinement stage this epic serves.
- **R3.** [Criticality assessment](https://github.com/m2ux/prosiform/issues/39) — the reading behind this epic's boundary: the distribution ships `prosiform` alone, so a check under `checks/`, a fixture declaration and the design record on the engineering branch reach no user of the tool.
- **R4.** [Row joins](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-187-i01-e03-carried-debt-joins) — the component each row changes, the pair that shares a pull request, and the reason each other pair keeps its own.
- **R5.** [Versioning policy](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) — what the contract tag and each build tag assert.
- **R6.** [I10:E01 Check Coverage](https://github.com/m2ux/prosiform/issues/454) — holds the check that reads a moving contract branch.
