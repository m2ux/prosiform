## Overview

Each Markdown link selects its target document's presets through its comma-separated title tags. An agent translates that link to one `pf --entry REF --presets PRESETS` invocation, which publishes a validated set of bundles and distinguishes dispatched variants of the same destination.

## Problem

- **Headings control conversion settings.**
  The [preset selector](https://github.com/m2ux/prosiform/blob/ba93ca60860f0dc46722f27acd471740465279da/src/prosiform/cli.py#L2271-L2348) matches section-title words, coupling presentation to grouping and substitution.
- **A direct invocation cannot carry a link's selection.**
  The [entry grammar](https://github.com/m2ux/prosiform/blob/ba93ca60860f0dc46722f27acd471740465279da/src/prosiform/cli.py#L914-L919) accepts destination references alone; the guide states no way to supply title tags.
- **Dispatches share a destination identity.**
  The [dispatch name](https://github.com/m2ux/prosiform/blob/ba93ca60860f0dc46722f27acd471740465279da/src/prosiform/dispatch.py#L175-L190) omits selection, so two tagged uses could share the first one's bundle.

## Proposal

- **The link title names presets.**
  `"checks,draft"` selects complete names case-insensitively after trimming; empty and duplicate tokens add nothing, and unknown names are silently ignored.
- **Selection belongs to each occurrence.**
  Only the target's matching presets layer over its `default`; headings and labels select nothing, and outgoing links use their own tags.
- **The command compiles one entry.**
  `pf --entry guide.md#plan-report --presets checks,draft` compiles one link's destination; `--presets` is optional, and bare `pf` prints the guide.
- **The guide states the command specification.**
  An agent resolves the authored destination and supplies its title tags, including for a deferred link; examples cover relative paths, fragments and shell quoting.
- **A bundle answers one effective selection.**
  Distinct effective selections of one dispatched destination produce distinct, deterministically named bundles; equivalent selections share one file.
- **Deferral preserves explicit selection.**
  A published deferred link keeps its title tags for the later command; no heading-match refusal decides whether the selection can be reproduced.
- **Existing preset settings keep their scope.**
  Default layering, group placement, substitution union and conflict checks apply to explicit selections; images and external references remain resources.
- **The feature ships with its observing checks.**
  Each implementation unit carries its unit and corpus tests; repository callers, eval expectations and public guides use the same command specification.
- **The boundary is explicit.**
  This epic covers Markdown link titles and the CLI; Mermaid tooltip tags, new preset fields, and new paid eval runs are outside its scope.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W00](https://github.com/m2ux/prosiform/pull/663) | The design states explicit preset selection | AC1 | | | 1 | ✓ |
| [W01](https://github.com/m2ux/prosiform/pull/665) | One reader interprets tag lists | AC2 | W00 | | 1 | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/667) | Source links carry title tags | AC4, AC5 | W01 | | 1 | ✓ |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/w03.md) | References carry effective selection identity | AC6, AC7 | W02 | | 1 | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/w04.md) | Entries select presets through tags | AC8, AC9, AC10 | W03 | W05 | 1 | |
| [W05](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/w05.md) | Guide and callers specify tagged compilation | AC3, AC11, AC21 | W03 | W04 | 1 | |
| [W06](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/w06.md) | Compilation schedules distinct selection variants | AC12, AC13, AC14 | W04 | W07 | 1 | |
| [W07](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/w07.md) | Dispatch links name their selected bundles | AC15, AC16 | W04 | W06 | 1 | |
| [W08](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/w08.md) | Deferred links retain their tag selection | AC17, AC18 | W07 | | 1 | |
| [W09](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/w09.md) | Eval workflows exercise tagged command specifications | AC19, AC20 | W08 | | 1 | |

## Acceptance Criteria

- [x] **AC1.** The pinned design defines the link-title and single-entry command contract, as design-to-fixture conformance review shows.
- [x] **AC2.** Comma-separated tag lists normalize complete names independently of whitespace, case, repetition and ordering, as shared tag-reader unit tests show.
- [ ] **AC3.** Authored links and CLI preset arguments use the same tag-list interpretation, as shared-reader integration tests show.
- [x] **AC4.** Inline and reference-style Markdown link occurrences expose their own title tags in preambles and sections, as source-reader tests show.
- [x] **AC5.** Image and external-reference titles, Mermaid tooltips and diagram labels supply no preset-selection tags, as source tests and resource/diagram corpus fixtures show.
- [ ] **AC6.** A reference occurrence retains its tag selection through resolution and substitution, as closure tests show.
- [ ] **AC7.** Bundle selection identity depends on destination and effective named presets, as identity tests covering equivalent and distinct selections show.
- [ ] **AC8.** A compile command accepts exactly one --entry and at most one --presets list, as CLI grammar fixtures and the installed-wheel smoke check show.
- [ ] **AC9.** An occurrence selects its target document's matching presets above default, silently ignoring unknown tags, as authored-link and CLI parity fixtures show.
- [ ] **AC10.** Section headings and link labels select no presets, as fixtures varying them while holding tags fixed show.
- [ ] **AC11.** The plain-text guide specifies the command an agent supplies for a tagged link, as guide fixtures covering relative paths, same-file fragments and shell quoting show.
- [ ] **AC12.** A run compiles a distinct dispatched bundle for each effective selection of one destination, as a dispatch-variant corpus fixture shows.
- [ ] **AC13.** Equivalent effective selections share a deterministic output filename, as variant-name fixtures covering reordered and unmatched tags show.
- [ ] **AC14.** Dispatch cycle and depth checks operate on the bundle variants the run schedules, as dispatch-analysis tests show.
- [ ] **AC15.** Each dispatch or parallel-set link names the bundle for its selected variant, as dispatch publication and candidate-validation tests show.
- [ ] **AC16.** A filename collision between distinct selection variants fails publication, as a collision-injection test shows.
- [ ] **AC17.** A deferred link preserves the tags needed for its later CLI invocation, as deferred-link publication fixtures show.
- [ ] **AC18.** Equivalent immediate and deferred compositions select identical presets independently of their headings, as composition parity fixtures show.
- [ ] **AC19.** Repository command callers use the single-entry command specification, as smoke, corpus and deterministic harness tests show.
- [ ] **AC20.** The eval's deferred and dispatched expectations distinguish the tag selections its workflows require, as deterministic workflow and scorer tests show.
- [ ] **AC21.** The invocation, focused guides and checked examples state link-title selection and the single-entry CLI grammar, as invocation, example and vocabulary checks show.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets) — the confirmed decisions, design, task plans, goal trace and review evidence.
