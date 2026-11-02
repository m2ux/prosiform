# I12 Design Patterns — November 2026

> Initiative planning · Created 2026-11-02

## Executive Summary

I12 gives prosiform a catalogue of design patterns: each page takes an established programming paradigm — SOLID, traits, polymorphism, inheritance and composition, contracts, concurrency, staging — and shows the grammar that realises it, on a specimen tree the build compiles and `make check` holds. Pages sit under `docs/patterns/`, declare `prosiform` so an agent can compile one with `pf`, and follow one lean template; an index maps each SOLID principle to the grammar that serves it.

The documentation today describes each feature alone, and the one worked composition, `example/work-planner`, is being removed. Skills such as Work Planner state their own architecture — artifacts with Fields and Operations, modes calling operations by heading link, layers that call downwards — as private rules. The catalogue names those structures and the paradigms behind them, so an author composes a skill from known patterns rather than re-deriving them, and a grammar limit a pattern meets becomes an issue rather than folklore.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [E00 W01 work item](e00/w01.md) | The pattern page check |
| [E00 W02 work item](e00/w02.md) | The page and specimen bundle check |
| [E00 W03 work item](e00/w03.md) | The catalogue index and its SOLID map |
| [E00 W04 work item](e00/w04.md) | The documentation index linking the catalogue |
| [E00 W05 work item](e00/w05.md) | The Shared Rule page, the first through both checks |
| [E01 W01 work item](e01/w01.md) | Artifact |
| [E01 W02 work item](e01/w02.md) | Contract and Implementation |
| [E01 W03 work item](e01/w03.md) | Role Interface |
| [E01 W04 work item](e01/w04.md) | Facade Entry |
| [E01 W05 work item](e01/w05.md) | Layered Calls |
| [E01 W06 work item](e01/w06.md) | The structure-and-contracts section of the index |
| [E02 W01 work item](e02/w01.md) | Generic Procedure |
| [E02 W02 work item](e02/w02.md) | Call-Site Dispatch |
| [E02 W03 work item](e02/w03.md) | Injected Strategy |
| [E02 W04 work item](e02/w04.md) | Hook Section |
| [E02 W05 work item](e02/w05.md) | Null Object |
| [E02 W06 work item](e02/w06.md) | Test Double |
| [E02 W07 work item](e02/w07.md) | Structural Conformance |
| [E02 W08 work item](e02/w08.md) | The polymorphism-and-substitution section of the index |
| [E03 W01 work item](e03/w01.md) | Trait Group |
| [E03 W02 work item](e03/w02.md) | Composite Outline |
| [E03 W03 work item](e03/w03.md) | Decorator Section |
| [E03 W04 work item](e03/w04.md) | Prototype Override |
| [E03 W05 work item](e03/w05.md) | The composition-and-reuse section of the index |
| [E04 W01 work item](e04/w01.md) | Linked Flowchart |
| [E04 W02 work item](e04/w02.md) | Sequence Protocol |
| [E04 W03 work item](e04/w03.md) | Dispatched Command |
| [E04 W04 work item](e04/w04.md) | Fork-Join Set |
| [E04 W05 work item](e04/w05.md) | Staged Compilation |
| [E04 W06 work item](e04/w06.md) | The flow-concurrency-and-staging section of the index |

## Goal

The clauses the user confirmed on 2026-11-02, G5 reworded the same day:

- **G1.** A skill author, human or agent, can find the pattern that realises an established programming paradigm in prosiform, and the page names the grammar features it uses.
- **G2.** Every pattern page has the same sections: Intent, Paradigm (with a citation), Grammar, Structure, Specimen, Consequences and Related. Each page declares `prosiform`, so `pf` compiles it into a bundle an agent can read.
- **G3.** Every pattern's specimen tree compiles to a committed expected bundle, and `make check` fails when a grammar change alters that bundle.
- **G4.** The catalogue index maps each SOLID principle to the grammar features and patterns that satisfy it.
- **G5.** Each limit a pattern hits in the grammar is stated on its page and raised as its own issue.
- **G6.** The catalogue covers structure and contracts; polymorphism and substitution; composition and reuse; and flow, concurrency and staging.

## Goal Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| G1 | AC1, AC6 | E00, E01–E04 | E00 AC2; every family's page criteria | No marked source |
| G2 | AC2 | E00 | E00 AC1, AC4 | No marked source |
| G3 | AC3 | E00 | E00 AC5, and every page criterion's committed bundle set | No marked source |
| G4 | AC4 | E00, E01–E04 | E00 AC6; E01 AC6, E02 AC8, E03 AC5, E04 AC6 | No marked source |
| G5 | AC5 | E00 | E00 AC3 | No marked source |
| G6 | AC6 | E01–E04 | E01 AC1–AC6, E02 AC1–AC8, E03 AC1–AC5, E04 AC1–AC6, E00 AC8 | No marked source |

Every clause has a criterion, every criterion is covered by an epic row, and every epic criterion by a task row. The References are background; none is marked as a source.

### Gaps, Ranked

1. **A limit a page omits is unobservable.** G5's "each limit a pattern hits" is held by the page check only once the page states the limit; whether every limit the pattern meets is stated rests on each work item's probe and review. Named here, as an unobservable item, rather than given a criterion no check can hold.
2. **AC4 and AC6 rest partly on a read.** The index's mapping is inspected, with `make links` holding each link; the page check reads pattern pages, not the index.

### Outside Threats

- **`make links` reads every document.** The committed expected bundles are Markdown; their deferral destinations and dispatch links are written for the bundle's own folder. E00 W02 decides where the set sits and how the link check leaves it, before any specimen is committed.
- **Every build change moves the specimens.** A deliberate change to what the build emits changes the expected bundle sets. E00 W02's re-record mode writes them in one command, and the diff shows what moved.
- **The grammar settles first.** E00 W01–W03 depend on the argument-surface and grouping initiatives (#462, #463) closing; each work item's Analysis reads the documentation as it then stands, so a feature those initiatives change or retire is described as it lands.
- **The example tree is not evidence.** #465 removes `example/work-planner` and the checks built on it; no row here reads, maintains or proves on it, and no page links it.
- **The documentation index is also brought to the build by the grouping initiative's proof.** E00 W04 edits `docs/README.md` only after #463 closes, so the two never write it together.

## Design

- **One page per pattern, one specimen per page.** The specimen is a tree at `docs/patterns/<pattern>/`; its expected bundle set is committed beside it and held by `make pattern-bundles`.
- **A page links its specimen by a deferral.** Compiling the page carries the page alone, and the link stays followable on GitHub and to an agent.
- **Two checks, two components.** `checks/pattern-pages.py` holds the template; `checks/pattern-bundles.py` compiles. Each runs under `make check` and is documented in `checks.md`.
- **The SOLID map reads both ways.** E00 W03 maps each principle to the grammar features that serve it; each family's index section carries a `Principles` column naming the principles each page serves. No family edits the map, so the four families' index rows write disjoint sections of one file.
- **Shared Rule is the exemplar.** It rests on delivered grammar alone, so it proves the template and both checks before any family starts; every family page depends on it.
- **A limit becomes a standalone issue.** Each limit a page states under `Consequences` → `Limits` links an unprefixed `enhancement` issue raised for it, off any board; Hoist mode places it later.

## Dependency Check

`deps.py` over the initiative, the five epics and the thirty work items:

- **Problems.** None.
- **Joins.** No candidate unit: no two rows of one epic declare one component. E00 W03 and W04 are joined by choice, two components in one pull request, since the documentation index links a page that W03 creates.
- **Advisory numbering.** None.
- **Longest chains.** Four steps, each through E00 W05: E00 W01 or W02 → E00 W05 → a family page → that family's index row.
- **Contention.** `main:docs/patterns/README.md` is declared by E00 W03 and by each family's index row (E01 W06, E02 W08, E03 W05, E04 W06).
  - E00 W03 never runs beside them: each family's index row depends on it.
  - The four family rows write disjoint sections — each family's own heading and table — and none edits the SOLID map, so they are independent regions of one file and may share a priority set.
- **Proposed epic priority, as printed.** E00 5, E01 4, E02 3, E03 2, E04 1; the script separates every epic by the file-level contention above.

## Decisions

- **Audience.** (User, 2026-11-02.) Skill authors, human and agent: pages read on GitHub and compile under `pf`.
- **Home.** (User, 2026-11-02.) `docs/patterns/`, linked from `docs/README.md`, published with the build.
- **Proof.** (User, 2026-11-02.) A compile check over committed expected bundles; no live agent-following run.
- **Sequencing.** (User, 2026-11-02.) The initiative starts once the argument-surface (#462) and grouping (#463) initiatives close, and documents the grammar they leave. E00 W01–W03 depend on both.
- **Gaps.** (User, 2026-11-02.) The catalogue changes no grammar; a limit becomes an issue of its own.
- **Template.** (User, 2026-11-02.) Lean: Intent, Paradigm, Grammar, Structure, Specimen, Consequences, Related.
- **Families.** (User, 2026-11-02.) All four: structure and contracts; polymorphism and substitution; composition and reuse; flow, concurrency and staging.
- **Epic cut.** (User, 2026-11-02.) A foundation epic, then one epic per family, the families runnable in parallel.
- **No proposal.** (User, 2026-11-02.) The Proposals board is reserved for major projects; this work goes straight to an initiative. The proposal issue raised first, #526, is converted into the initiative.
- **A limit is a standalone issue.** (User, 2026-11-02.) An unprefixed `enhancement` issue off any board, linked from the page; G5 reads "raised as its own issue".
- **Retired forms are not documented.** (Planning.) Preset `include` and `exclude` (closed not planned in #445), `-m` and `root` reach no page.
- **Epic priority.** (User, 2026-11-02.) E00 `priority: 2`; E01, E02, E03 and E04 `priority: 1`. The four family index rows write disjoint sections of the index, so the families share a set; every family page still waits on E00 W05 through its row's edge.
- **Required criteria.** (Validation, 2026-11-02.) `config/required-criteria.json` on `workspace` declares no criterion, so the epic validator reports the project's required criteria unevaluable; no epic body changes for it.
- **Paradigm sources.** (Planning.) Web research on 2026-11-02 grounds each page's citation: Schärli et al. on traits and flattening, Martin's 2020 module form of SOLID, Cardelli and Wegner on polymorphism, the GoF catalogue, Reenskaug and Coplien on DCI, MacQueen on ML modules, Meyer on contracts, Lieberman on prototypes, Woolf on null objects, Meszaros on test doubles, Hoare on CSP, Hewitt on actors, Morrison on flow-based programming, Harel on statecharts, Taha on staging, and DITA 1.3 as the closest prior art in documentation reuse.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I12 Design Patterns](https://github.com/m2ux/prosiform/issues/526) |
| Epic | [I12:E00 Catalogue Foundation](https://github.com/m2ux/prosiform/issues/527) |
| Epic | [I12:E01 Structure and Contracts](https://github.com/m2ux/prosiform/issues/528) |
| Epic | [I12:E02 Polymorphism and Substitution](https://github.com/m2ux/prosiform/issues/529) |
| Epic | [I12:E03 Composition and Reuse](https://github.com/m2ux/prosiform/issues/530) |
| Epic | [I12:E04 Flow and Concurrency](https://github.com/m2ux/prosiform/issues/531) |
| Prerequisite | [I08 Argument Surface](https://github.com/m2ux/prosiform/issues/462) |
| Prerequisite | [I09 Grouping and Composition](https://github.com/m2ux/prosiform/issues/463) |
| Example removal | [I08:E08 Declared Tree](https://github.com/m2ux/prosiform/issues/465) |
