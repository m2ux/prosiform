# Alignment check evidence

These checks use the saved issue bodies after the approved corrections. A passing delivery script can still report incomplete delivery or unevaluated branch checks. Closed epic bodies supply context and are outside the body-edit scope. The source review distinguishes genuine findings from wording-check false positives.

Current scope: 25 open issues. #161 and #177 are retired as not planned and absent from the board.

## Format checks

### Issue 20

```text
#20 initiative (open): 0 fixed, 0 to apply, 0 to decide
```

### Issue 464

```text
#464 initiative (open): 0 fixed, 0 to apply, 0 to decide
```

### Issue 21

```text
#21 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 22

```text
#22 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 23

```text
#23 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 187

```text
#187 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 524

```text
#524 initiative (open): 0 fixed, 0 to apply, 0 to decide
```

### Issue 525

```text
#525 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 526

```text
#526 initiative (open): 0 fixed, 0 to apply, 0 to decide
```

### Issue 527

```text
#527 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 528

```text
#528 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 529

```text
#529 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 530

```text
#530 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 531

```text
#531 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 579

```text
#579 epic (open): 0 fixed, 0 to apply, 0 to decide
  source: config/required-criteria.json at 543e1a830c64d7bccd6a541e6c7db268b19ed842 in /home/mike1/projects/dev/md-composer/.git
```

### Issue 158

```text
#158 task (open): 0 fixed, 0 to apply, 1 to decide
  decide: References: names W23; the References section does not link issues or pull requests on the same board
```

### Issue 160

```text
#160 task (open): 0 fixed, 0 to apply, 3 to decide
  decide: title has no "Name: Subtitle" after the prefix
  decide: Proposal: change narrative "names fails the check, so the suite can no longer be what holds a function upri"; state the plan as it is
  decide: Problem: names W22; a Problem or Proposal names no epic, task, or acceptance criterion of its own initiative
```

### Issue 162

```text
#162 task (open): 0 fixed, 0 to apply, 3 to decide
  decide: title has no "Name: Subtitle" after the prefix
  decide: References: names W16; the References section does not link issues or pull requests on the same board
  decide: Problem: change narrative "ether a flag was renamed, or the output moved to another stream — is not obser"; state the plan as it is
```

### Issue 185

```text
#185 task (open): 0 fixed, 0 to apply, 2 to decide
  decide: title has no "Name: Subtitle" after the prefix
  decide: References: names #184; the References section does not link issues or pull requests on the same board
```

### Issue 186

```text
#186 task (open): 0 fixed, 0 to apply, 2 to decide
  decide: title has no "Name: Subtitle" after the prefix
  decide: References: names #184; the References section does not link issues or pull requests on the same board
```

### Issue 189

```text
#189 task (open): 0 fixed, 0 to apply, 1 to decide
  decide: References: names #188; the References section does not link issues or pull requests on the same board
```

### Issue 191

```text
#191 task (open): 0 fixed, 0 to apply, 1 to decide
  decide: References: names #190; the References section does not link issues or pull requests on the same board
```

### Issue 193

```text
#193 task (open): 0 fixed, 0 to apply, 0 to decide
```

### Issue 243

```text
#243 task (open): 0 fixed, 0 to apply, 0 to decide
```

### Issue 255

```text
#255 task (open): 0 fixed, 0 to apply, 1 to decide
  decide: References: names W12, #244; the References section does not link issues or pull requests on the same board
```

## Reference visibility

The visibility checks pass for the remaining open issues. Their References cite public repositories. The source review separately checks same-board membership and obsolete requirement sources.

## Dependencies for issue 20

```text
--- problems
missing Lane data: E02:W04, E02:W06
E01:W01: work item declares no component
E01:W02: work item declares no component
E01:W03: work item declares no component
E01:W04: work item declares no component
E13:W01: work item declares no component
E13:W02: work item declares no component

--- joins: candidate units, rows of one epic extending one component
E00:W03, E00:W04 extend ledger: name each other in Joins, dropping the dependency of E00:W04 on E00:W03, or name exactly these rows on one record line with why they stay split

--- advisory: numbering against start order
E02:W03 (level 0) is numbered after E02:W02 (level 1)
E02:W05 (level 1) is numbered after E02:W04 (level 2)
E02:W07 (level 1) is numbered after E02:W06 (level 2)

--- levels (0 = can start now)
0 E00:W01 - Ledger format and triage states
0 E02:W01 - The overview section emitted only where needed
0 E02:W03 - Title case for every generated heading
0 E03:W01 - A code block indented inside a list item
0 E03:W02 - Uncalled functions named only by a check
0 E03:W04 - Tracker route exercised by the repository check
0 E03:W06 - Lowercase build words in the design
0 E03:W07 - An avoided term in a corpus declaration
0 E03:W08 - One fixture run by its identity
0 E03:W09 - Build tags matching the reported version
0 E03:W10 - A document present and not read
0 E03:W12 - Whether a tree is sound
0 E06:W01 - Declared metadata contract
0 E09:W01 - A second operator and its metadata key
0 E09:W02 - A published link without its mark
0 E10:W01 - Protection on every long-lived branch
1 E00:W02 - Fixture capture from a recorded entry
1 E00:W03 - Run record counted against the declared exposure set
1 E02:W02 - A member reaching an unshared destination
1 E02:W05 - A member heading that names one document
1 E02:W07 - Generated input refused whatever a path spells
1 E03:W13 - A stale fixture classified before it is rewritten
1 E06:W02 - Bounded metadata decoder
1 E09:W03 - The example states what its mark means
1 E10:W02 - Delivery branches unaffected by the settings
2 E00:W04 - Demonstration measurements entered in the ledger
2 E01:W01 - Revision order and its citation record
2 E02:W04 - A pooled section that names its contributors
2 E02:W06 - One name for a member in both places
2 E03:W14 - Restatement that writes only the expectation
2 E06:W03 - Captured source settings
2 E09:W04 - Handoff round-trip
3 E01:W02 - Traceability refreshed on each revision
3 E01:W03 - Open-finding summary from the ledger
3 E01:W04 - Workspace skills following the compilation guide
3 E02:W08 - Documented grouping and its diagrams
3 E06:W04 - Per-file compilation settings
4 E06:W05 - Metadata authoring guidance
4 E13:W01 - Deferral decisions for the remaining entries
5 E06:W06 - File-owned invocation contract
5 E13:W02 - Freeze check and the tagged revision
6 E06:W07 - Bounded root metadata
7 E06:W08 - Per-file root resolution
8 E06:W09 - Derived output publication
9 E06:W10 - Linked skill bootstrap tests
10 E06:W11 - File-only authoring audit

--- component contention: rows of different epics extending one component
none
not checked, no component read: E01:W01, E01:W02, E01:W03, E01:W04, E03:W01, E03:W02, E03:W04, E03:W06, E03:W07, E03:W08, E03:W09, E03:W10, E06:W01, E06:W02, E06:W03, E06:W04, E06:W05, E06:W06, E06:W07, E06:W08, E06:W09, E06:W10, E06:W11, E09:W01, E09:W02, E09:W03, E09:W04, E10:W01, E10:W02, E13:W01, E13:W02

--- epic priority (epics sharing a number start together)
1 E00
1 E01
1 E02
1 E03
1 E06
1 E09
1 E10
1 E13

--- longest chains: 1, each of 11 steps
on every chain: E06:W01, E06:W02, E06:W03, E06:W04, E06:W05, E06:W06, E06:W07, E06:W08, E06:W09, E06:W10, E06:W11
E06:W01 -> E06:W02 -> E06:W03 -> E06:W04 -> E06:W05 -> E06:W06 -> E06:W07 -> E06:W08 -> E06:W09 -> E06:W10 -> E06:W11
```

### Work-item evidence

A missing entry means this review did not locate the registered file, rather than proving none exists.

```text
E00:W01: artifacts/planning/2026-10-26-21-i01-e00-w01-ledger-format-and-triage/w01.md
E00:W02: artifacts/planning/2026-10-29-21-i01-e00-w02-fixture-capture-from-a/w02.md
E00:W03: artifacts/planning/2026-10-29-21-i01-e00-w03-run-record-counted-against/w03.md
E00:W04: artifacts/planning/2026-10-17-prosiform-v1/i01-e00/w04.md
E01:W01: artifacts/planning/2026-10-17-prosiform-v1/i01-e01/w01.md
E01:W02: artifacts/planning/2026-10-17-prosiform-v1/i01-e01/w02.md
E01:W03: artifacts/planning/2026-10-17-prosiform-v1/i01-e01/w03.md
E01:W04: artifacts/planning/2026-10-17-prosiform-v1/i01-e01/w04.md
E02:W01: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w01.md
E02:W02: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w02.md
E02:W03: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w03.md
E02:W04: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w04.md
E02:W05: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w05.md
E02:W06: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w06.md
E02:W07: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w07.md
E02:W08: artifacts/planning/2026-10-17-prosiform-v1/i01-e02/w08.md
E03:W01: MISSING registered work item
E03:W02: MISSING registered work item
E03:W04: MISSING registered work item
E03:W06: MISSING registered work item
E03:W07: MISSING registered work item
E03:W08: MISSING registered work item
E03:W09: MISSING registered work item
E03:W10: MISSING registered work item
E03:W12: artifacts/planning/2026-10-24-187-i01-e03-w12-change-state/w12.md
E03:W13: artifacts/planning/2026-10-24-243-i01-e03-w13-drift-triage/w13.md
E03:W14: artifacts/planning/2026-10-24-243-i01-e03-w13-drift-triage/w14.md
E06:W01: MISSING registered work item
E06:W02: MISSING registered work item
E06:W03: MISSING registered work item
E06:W04: MISSING registered work item
E06:W05: MISSING registered work item
E06:W06: MISSING registered work item
E06:W07: MISSING registered work item
E06:W08: MISSING registered work item
E06:W09: MISSING registered work item
E06:W10: MISSING registered work item
E06:W11: MISSING registered work item
E09:W01: MISSING registered work item
E09:W02: MISSING registered work item
E09:W03: MISSING registered work item
E09:W04: MISSING registered work item
E10:W01: MISSING registered work item
E10:W02: MISSING registered work item
E13:W01: artifacts/planning/2026-10-17-prosiform-v1/i01-e04/w01.md
E13:W02: artifacts/planning/2026-10-17-prosiform-v1/i01-e04/w02.md
```

## Dependencies for issue 464

```text
--- problems
missing Lane data: E06:W02, E06:W03, E06:W04
missing Lane data: E06:W05, E06:W08
E00:W00: depends on E00:W04, not an earlier task in its epic
E00:W02: depends on E00:W04, not an earlier task in its epic
E04:W14: depends on E04:W16, not an earlier task in its epic
E04:W16: depends on E04:W17, not an earlier task in its epic
E04:W16: depends on E04:W18, not an earlier task in its epic
E04:W16: depends on E04:W19, not an earlier task in its epic
E05:W01: depends on E05:W03, not an earlier task in its epic
E00:W02: E00:W01 is already implied by E00:W00
E00:W02: E00:W04 is already implied by E00:W00
E05:W01: E05:W00 is already implied by E05:W03
E06:W10: E06:W03 is already implied by E06:W05

--- joins: candidate units, rows of one epic extending one component
none

--- advisory: numbering against start order
E00:W01 (level 0) is numbered after E00:W00 (level 2)
E00:W04 (level 1) is numbered after E00:W03 (level 4)
E01:W05 (level 1) is numbered after E01:W04 (level 2)
E04:W16 (level 3) is numbered after E04:W15 (level 5)
E04:W17 (level 1) is numbered after E04:W16 (level 3)
E05:W03 (level 1) is numbered after E05:W02 (level 3)
E06:W08 (level 2) is numbered after E06:W07 (level 3)

--- levels (0 = can start now)
0 E00:W01 - Scenarios reaching every failure class
0 E01:W01 - The trigger reads the changed paths
0 E01:W02 - The link check names each revision read
0 E02:W01 - Every project-scope settings file refused
0 E03:W00 - Design clause
0 E04:W01 - Scenarios stating the `pf` runs a session makes
0 E04:W02 - Compiled bundles with a limited `pf` shell
0 E04:W03 - A session held to its stated runs
0 E04:W04 - Sub-agent starts and commands at every depth
0 E05:W00 - Write the runbook and triage rubric
0 E06:W00 - Design clause
1 E00:W04 - Shake down the baseline runbook
1 E01:W03 - A skipped run states itself
1 E01:W05 - Every Markdown document runs the checks
1 E02:W02 - Managed settings hook recorded
1 E03:W01 - A destination answers one member
1 E04:W05 - A scenario bootstrapping a skill's `↳` link
1 E04:W06 - Scenarios activating conditional and nested deferrals
1 E04:W07 - A scenario deferring under matched presets
1 E04:W08 - Scenarios composing under a conditional step
1 E04:W09 - Composition, footnote and self-composition scenarios
1 E04:W10 - Deferred composition reaching a dispatch
1 E04:W11 - Scenarios dispatching three hops deep
1 E04:W12 - Scenarios of a sub-agent's first `pf` run
1 E04:W17 - Triage rubric entries for the run classes
1 E04:W18 - Compiled Claude per-agent command evidence
1 E05:W03 - Record managed configuration by count and fingerprint
1 E06:W01 - A plain-text guide holding the rules
1 E06:W02 - Every bundle opening with the run-pf line
1 E06:W03 - A `⇉` link kept inline at its file
1 E06:W04 - One `In parallel` section per set
2 E00:W00 - The default matrix runs the user's model
2 E01:W04 - The checks page states the trigger rule
2 E02:W03 - The settings the preflight reads
2 E03:W02 - The validation page states the invariant
2 E04:W19 - Edge corpus using the declared bundle grammar
2 E05:W01 - Run the live default-matrix proof
2 E05:W04 - Count managed hooks from the transcripts
2 E06:W05 - Deferred dispatch marks refused
2 E06:W08 - `↳` composing, arrow labels refused
3 E00:W02 - Every-form baseline over the hardened corpus
3 E02:W04 - The check catalogue states every refused scope
3 E04:W16 - Shake down the edge-run runbook
3 E05:W02 - State the proof on the eval page
3 E06:W06 - The pages stating the guide and `⇉`
3 E06:W07 - One compiled form carrying `pf`
3 E06:W09 - The composition page stating `↳`
3 E06:W10 - Dispatch refusals stating no link to publish
4 E00:W03 - Harness criteria read from the baseline
4 E04:W14 - Live run of the edge workflows
5 E04:W15 - The eval page stating the edge workflows

--- component contention: rows of different epics extending one component
E00:W00 and E04:W02 both extend main:evals/diagram-following/run.py
E00:W03 and E02:W03 both extend main:evals/diagram-following/README.md
E00:W03 and E04:W15 both extend main:evals/diagram-following/README.md
E00:W03 and E05:W02 both extend main:evals/diagram-following/README.md
E00:W04 and E04:W16 both extend main:evals/diagram-following/RUNBOOK.md
E00:W04 and E04:W17 both extend main:evals/diagram-following/RUNBOOK.md
E00:W04 and E05:W00 both extend main:evals/diagram-following/RUNBOOK.md
E02:W01 and E04:W04 both extend main:evals/diagram-following/harness.py
E02:W01 and E04:W18 both extend main:evals/diagram-following/harness.py
E02:W01 and E05:W03 both extend main:evals/diagram-following/harness.py
E02:W01 and E06:W07 both extend main:evals/diagram-following/harness.py
E02:W02 and E04:W04 both extend main:evals/diagram-following/harness.py
E02:W02 and E04:W18 both extend main:evals/diagram-following/harness.py
E02:W02 and E05:W03 both extend main:evals/diagram-following/harness.py
E02:W02 and E06:W07 both extend main:evals/diagram-following/harness.py
E02:W03 and E04:W15 both extend main:evals/diagram-following/README.md
E02:W03 and E05:W02 both extend main:evals/diagram-following/README.md
E03:W00 and E06:W00 both extend engineering:artifacts/planning/2026-10-17-prosiform-v1/design.md
E04:W04 and E05:W03 both extend main:evals/diagram-following/harness.py
E04:W04 and E06:W07 both extend main:evals/diagram-following/harness.py
E04:W15 and E05:W02 both extend main:evals/diagram-following/README.md
E04:W16 and E05:W00 both extend main:evals/diagram-following/RUNBOOK.md
E04:W17 and E05:W00 both extend main:evals/diagram-following/RUNBOOK.md
E04:W18 and E05:W03 both extend main:evals/diagram-following/harness.py
E04:W18 and E06:W07 both extend main:evals/diagram-following/harness.py
E05:W03 and E06:W07 both extend main:evals/diagram-following/harness.py
not checked, no component read: E01:W05, E02:W04, E05:W04

--- epic priority (epics sharing a number start together)
5 E00
5 E01
5 E03
4 E02
3 E04
2 E05
1 E06

--- longest chains: 17, each of 6 steps
on every chain: E04:W14, E04:W15, E04:W16, E04:W19
E04:W01 -> E04:W05 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W01 -> E04:W06 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W02 -> E04:W06 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W01 -> E04:W07 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W02 -> E04:W07 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W01 -> E04:W08 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W02 -> E04:W08 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W01 -> E04:W09 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W02 -> E04:W09 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
E04:W01 -> E04:W10 -> E04:W19 -> E04:W16 -> E04:W14 -> E04:W15
... 7 more
```

### Work-item evidence

A missing entry means this review did not locate the registered file, rather than proving none exists.

```text
E00:W00: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e00/w00.md
E00:W01: artifacts/planning/2026-11-03-403-i10-e00-w01-scenarios-reaching-every-failure/w01.md
E00:W02: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e00/w02.md
E00:W03: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e00/w03.md
E00:W04: artifacts/planning/2026-11-03-403-i10-e00-w04-shake-down-the-baseline/w04.md
E01:W01: artifacts/planning/2026-11-03-454-i10-e01-w01-the-trigger-reads-the/w01.md
E01:W02: artifacts/planning/2026-11-03-454-i10-e01-w02-the-link-check-names/w02.md
E01:W03: artifacts/planning/2026-11-03-454-i10-e01-w03-a-skipped-run-states/w03.md
E01:W04: artifacts/planning/2026-11-03-454-i10-e01-w04-the-checks-page-states/w04.md
E01:W05: MISSING registered work item
E02:W01: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e02/w01.md
E02:W02: artifacts/planning/2026-11-03-456-i10-e02-w02-managed-settings-hook-recorded/w02.md
E02:W03: artifacts/planning/2026-11-03-456-i10-e02-w03-the-settings-the-preflight/w03.md
E02:W04: MISSING registered work item
E03:W00: artifacts/planning/2026-11-03-455-i10-e03-w00-design-clause/w00.md
E03:W01: artifacts/planning/2026-11-03-455-i10-e03-w01-a-destination-answers-one/w01.md
E03:W02: artifacts/planning/2026-11-03-455-i10-e03-w02-the-validation-page-states/w02.md
E04:W01: artifacts/planning/2026-11-03-579-i10-e04-w01-scenarios-stating-the-pf/w01.md
E04:W02: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w02.md
E04:W03: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w03.md
E04:W04: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w04.md
E04:W05: artifacts/planning/2026-11-03-579-i10-e04-w05-a-scenario-bootstrapping-a/w05.md
E04:W06: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w06.md
E04:W07: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w07.md
E04:W08: artifacts/planning/2026-11-03-579-i10-e04-w08-scenarios-composing-under-a/w08.md
E04:W09: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w09.md
E04:W10: artifacts/planning/2026-11-03-579-i10-e04-w10-a-scenario-compiling-a/w10.md
E04:W11: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w11.md
E04:W12: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w12.md
E04:W14: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w14.md
E04:W15: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w15.md
E04:W16: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e04/w16.md
E04:W17: artifacts/planning/2026-11-03-579-i10-e04-w17-triage-rubric-entries-for/w17.md
E04:W18: artifacts/planning/2026-11-03-579-i10-e04-w18-a-staged-claude-session/w18.md
E04:W19: artifacts/planning/2026-11-03-579-i10-e04-w19-the-edge-corpus-test/w19.md
E05:W00: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e05/w00.md
E05:W01: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e05/w01.md
E05:W02: artifacts/planning/2026-11-03-594-i10-e05-w02-state-the-proof-on/w02.md
E05:W03: artifacts/planning/2026-11-03-594-i10-e05-w03-record-managed-configuration-by/w03.md
E05:W04: MISSING registered work item
E06:W00: artifacts/planning/2026-11-03-639-i10-e06-w00-design-clause/w00.md
E06:W01: artifacts/planning/2026-11-03-639-i10-e06-w01-a-plain-text-guide/w01.md
E06:W02: artifacts/planning/2026-11-03-639-i10-e06-w02-every-bundle-opening-with/w02.md
E06:W03: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w03.md
E06:W04: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w04.md
E06:W05: artifacts/planning/2026-11-03-639-i10-e06-w05-deferred-dispatch-marks-refused/w05.md
E06:W06: artifacts/planning/2026-11-03-639-i10-e06-w06-the-pages-stating-the/w06.md
E06:W07: artifacts/planning/2026-11-03-639-i10-e06-w07-one-compiled-form-carrying/w07.md
E06:W08: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w08.md
E06:W09: artifacts/planning/2026-11-03-639-i10-e06-w09-the-composition-page-stating/w09.md
E06:W10: artifacts/planning/2026-11-01-464-i10-evaluation-and-checks/e06/w10.md
```

## Dependencies for issue 524

```text
--- problems
none

--- joins: candidate units, rows of one epic extending one component
none

--- advisory: numbering against start order
none

--- levels (0 = can start now)
0 E00:W01 - The version the previous corpus selects
1 E00:W02 - The release branch and its version commit
1 E00:W03 - The `contract/` and `python/` tag pair
1 E00:W04 - The release pull request into `main`

--- component contention: rows of different epics extending one component
none

--- epic priority (epics sharing a number start together)
1 E00

--- longest chains: 3, each of 2 steps
on every chain: E00:W01
E00:W01 -> E00:W02
E00:W01 -> E00:W03
E00:W01 -> E00:W04
```

### Work-item evidence

A missing entry means this review did not locate the registered file, rather than proving none exists.

```text
E00:W01: artifacts/planning/2026-11-02-524-i11-mvp-release/e00/w01.md
E00:W02: artifacts/planning/2026-11-02-524-i11-mvp-release/e00/w02.md
E00:W03: artifacts/planning/2026-11-02-524-i11-mvp-release/e00/w03.md
E00:W04: artifacts/planning/2026-11-02-524-i11-mvp-release/e00/w04.md
```

## Dependencies for issue 526

```text
--- problems
none

--- joins: candidate units, rows of one epic extending one component
none

--- advisory: numbering against start order
none

--- levels (0 = can start now)
0 E00:W01 - Pattern page check
0 E00:W02 - Page and specimen bundle check
0 E00:W03 - Catalogue index and SOLID map
0 E00:W04 - Documentation index links the catalogue
1 E00:W05 - Shared Rule page and specimen
2 E01:W01 - Artifact page and specimen
2 E01:W02 - Contract and Implementation page and specimen
2 E01:W03 - Role Interface page and specimen
2 E01:W04 - Facade Entry page and specimen
2 E01:W05 - Layered Calls page and specimen
2 E02:W01 - Generic Procedure page and specimen
2 E02:W02 - Call-Site Dispatch page and specimen
2 E02:W03 - Injected Strategy page and specimen
2 E02:W04 - Hook Section page and specimen
2 E02:W05 - Null Object page and specimen
2 E02:W06 - Test Double page and specimen
2 E02:W07 - Structural Conformance page and specimen
2 E03:W01 - Trait Group page and specimen
2 E03:W02 - Composite Outline page and specimen
2 E03:W03 - Decorator Section page and specimen
2 E03:W04 - Prototype Override page and specimen
2 E04:W01 - Linked Flowchart page and specimen
2 E04:W02 - Sequence Protocol page and specimen
2 E04:W03 - Dispatched Command page and specimen
2 E04:W04 - Fork-Join Set page and specimen
2 E04:W05 - Staged Compilation page and specimen
3 E01:W06 - Family section of the catalogue index
3 E02:W08 - Family section of the catalogue index
3 E03:W05 - Family section of the catalogue index
3 E04:W06 - Family section of the catalogue index

--- component contention: rows of different epics extending one component
E00:W03 and E01:W06 both extend main:docs/patterns/README.md
E00:W03 and E02:W08 both extend main:docs/patterns/README.md
E00:W03 and E03:W05 both extend main:docs/patterns/README.md
E00:W03 and E04:W06 both extend main:docs/patterns/README.md
E01:W06 and E02:W08 both extend main:docs/patterns/README.md
E01:W06 and E03:W05 both extend main:docs/patterns/README.md
E01:W06 and E04:W06 both extend main:docs/patterns/README.md
E02:W08 and E03:W05 both extend main:docs/patterns/README.md
E02:W08 and E04:W06 both extend main:docs/patterns/README.md
E03:W05 and E04:W06 both extend main:docs/patterns/README.md

--- epic priority (epics sharing a number start together)
5 E00
4 E01
3 E02
2 E03
1 E04

--- longest chains: 42, each of 4 steps
on every chain: E00:W05
E00:W01 -> E00:W05 -> E01:W01 -> E01:W06
E00:W02 -> E00:W05 -> E01:W01 -> E01:W06
E00:W01 -> E00:W05 -> E01:W02 -> E01:W06
E00:W02 -> E00:W05 -> E01:W02 -> E01:W06
E00:W01 -> E00:W05 -> E01:W03 -> E01:W06
E00:W02 -> E00:W05 -> E01:W03 -> E01:W06
E00:W01 -> E00:W05 -> E01:W04 -> E01:W06
E00:W02 -> E00:W05 -> E01:W04 -> E01:W06
E00:W01 -> E00:W05 -> E01:W05 -> E01:W06
E00:W02 -> E00:W05 -> E01:W05 -> E01:W06
... 32 more
```

### Work-item evidence

A missing entry means this review did not locate the registered file, rather than proving none exists.

```text
E00:W01: artifacts/planning/2026-11-02-526-i12-design-patterns/e00/w01.md
E00:W02: artifacts/planning/2026-11-02-526-i12-design-patterns/e00/w02.md
E00:W03: artifacts/planning/2026-11-02-526-i12-design-patterns/e00/w03.md
E00:W04: artifacts/planning/2026-11-02-526-i12-design-patterns/e00/w04.md
E00:W05: artifacts/planning/2026-11-02-526-i12-design-patterns/e00/w05.md
E01:W01: artifacts/planning/2026-11-02-526-i12-design-patterns/e01/w01.md
E01:W02: artifacts/planning/2026-11-02-526-i12-design-patterns/e01/w02.md
E01:W03: artifacts/planning/2026-11-02-526-i12-design-patterns/e01/w03.md
E01:W04: artifacts/planning/2026-11-02-526-i12-design-patterns/e01/w04.md
E01:W05: artifacts/planning/2026-11-02-526-i12-design-patterns/e01/w05.md
E01:W06: artifacts/planning/2026-11-02-526-i12-design-patterns/e01/w06.md
E02:W01: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w01.md
E02:W02: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w02.md
E02:W03: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w03.md
E02:W04: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w04.md
E02:W05: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w05.md
E02:W06: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w06.md
E02:W07: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w07.md
E02:W08: artifacts/planning/2026-11-02-526-i12-design-patterns/e02/w08.md
E03:W01: artifacts/planning/2026-11-02-526-i12-design-patterns/e03/w01.md
E03:W02: artifacts/planning/2026-11-02-526-i12-design-patterns/e03/w02.md
E03:W03: artifacts/planning/2026-11-02-526-i12-design-patterns/e03/w03.md
E03:W04: artifacts/planning/2026-11-02-526-i12-design-patterns/e03/w04.md
E03:W05: artifacts/planning/2026-11-02-526-i12-design-patterns/e03/w05.md
E04:W01: artifacts/planning/2026-11-02-526-i12-design-patterns/e04/w01.md
E04:W02: artifacts/planning/2026-11-02-526-i12-design-patterns/e04/w02.md
E04:W03: artifacts/planning/2026-11-02-526-i12-design-patterns/e04/w03.md
E04:W04: artifacts/planning/2026-11-02-526-i12-design-patterns/e04/w04.md
E04:W05: artifacts/planning/2026-11-02-526-i12-design-patterns/e04/w05.md
E04:W06: artifacts/planning/2026-11-02-526-i12-design-patterns/e04/w06.md
```

## Delivery reconciliation

### Issue 20

```text
#20 initiative (open)
  closable: no (undelivered E00, E01, E03, E13, unticked AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10)
```

### Issue 464

```text
#464 initiative (open)
  ready to verify: AC1 (E00)
  ready to verify: AC2 (E00)
  ready to verify: AC9 (E00)
  ready to verify: AC11 (E00)
  ready to verify: AC12 (E00)
  closable: no (undelivered E04, unticked AC1, AC2, AC9, AC11, AC12, AC13, AC15)
```

### Issue 21

```text
#21 epic (open)
  unevaluable: config/branches at 41f307490fca501469007fb903e52eb602d9163a in /home/mike1/projects/dev/md-composer/.git is absent
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W02, W03, W04, unticked AC3, AC4, AC5, AC7, AC8, AC9)
```

### Issue 22

```text
#22 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W03, W04, unticked AC1, AC2, AC3, AC4, AC5, AC6, AC7)
```

### Issue 23

```text
#23 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, unticked AC1, AC2, AC3, AC4)
```

### Issue 187

```text
#187 epic (open)
  note: W01 links task issue #158; link its pull request
  note: W02 links task issue #160; link its pull request
  note: W04 links task issue #162; link its pull request
  note: W06 links task issue #185; link its pull request
  note: W07 links task issue #186; link its pull request
  note: W08 links task issue #189; link its pull request
  note: W09 links task issue #191; link its pull request
  note: W10 links task issue #193; link its pull request
  note: W12 links task issue #255; link its pull request
  note: W13 links task issue #243; link its pull request
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W04, W06, W07, W08, W09, W10, W12, W13, W14, unticked AC1, AC2, AC4, AC7, AC8, AC9, AC10, AC11, AC13, AC14, AC15, AC16, AC17, AC18, AC19)
```

### Issue 524

```text
#524 initiative (open)
  closable: no (undelivered E00, unticked AC1, AC2)
```

### Issue 525

```text
#525 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W03, W04, unticked AC1, AC2, AC3, AC4, AC5)
```

### Issue 526

```text
#526 initiative (open)
  closable: no (undelivered E00, E01, E02, E03, E04, unticked AC1, AC2, AC3, AC4, AC5, AC6)
```

### Issue 527

```text
#527 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W03, W04, W05, unticked AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8)
```

### Issue 528

```text
#528 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W03, W04, W05, W06, unticked AC1, AC2, AC3, AC4, AC5, AC6)
```

### Issue 529

```text
#529 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W03, W04, W05, W06, W07, W08, unticked AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8)
```

### Issue 530

```text
#530 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W03, W04, W05, unticked AC1, AC2, AC3, AC4, AC5)
```

### Issue 531

```text
#531 epic (open)
  unevaluable: long-lived branches not given
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W01, W02, W03, W04, W05, W06, unticked AC1, AC2, AC3, AC4, AC5, AC6)
```

### Issue 579

```text
#579 epic (open)
  in flight: #622 [I10:E04] Composition Following
  unevaluable: config/branches at 1076ef5293c0da74163d1289adf56ab0ef8cfbb0 in /home/mike1/projects/dev/md-composer/.git is absent
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (undelivered W14, W15, W16, unticked AC20, AC21, AC24, AC25)
```

## Linked task PR plans

```text
https://github.com/m2ux/prosiform/pull/324: test plan unchanged
```

```text
https://github.com/m2ux/prosiform/pull/621: test plan unchanged
```

```text
https://github.com/m2ux/prosiform/pull/626: test plan unchanged
```

```text
https://github.com/m2ux/prosiform/pull/628: test plan unchanged
```

```text
https://github.com/m2ux/prosiform/pull/634: test plan unchanged
```

```text
https://github.com/m2ux/prosiform/pull/638: test plan unchanged
```

```text
https://github.com/m2ux/prosiform/pull/640: test plan unchanged
```

```text
https://github.com/m2ux/prosiform/pull/651: test plan unchanged
```
