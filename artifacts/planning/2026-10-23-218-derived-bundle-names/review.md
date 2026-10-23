# Output Naming Planning Review

## Goal Trace

| Confirmed outcome | Initiative criterion | Epic criteria | Work |
| --- | --- | --- | --- |
| Whole-file names reflect the root-relative source path | AC13 | AC13, AC14 | W06, W07 |
| Section names include their fragment identifier | AC13 | AC13, AC14 | W06, W07 |
| Several selections produce one explicitly named bundle | AC13 | AC15 | W07 |
| Automatic destinations preserve publication safety | AC13 | AC16 | W07 |
| Authors use hyphens to avoid underscore ambiguity | AC13 | AC17 | W08 |
| Output naming preserves compiled content | AC13 | AC18 | W08 |
| The normative contract precedes implementation | AC3 | AC13 | W06 |

Existing metadata criteria AC1–AC12 retain their completed work and the original planning record's goal trace to initiative AC12. The user explicitly extends epic #218 rather than creating another epic. Proposal #208 consumes the naming and underscore guidance through its updated goal and reference; this extension does not implement that skill.

## Decisions

- Automatic output is the normal CLI path: the root is the only required option and the entry is positional. The output filename is derived; explicit `-o` remains an override or a combined-selection destination. A single entry writes in the working directory.
- Fragment-only entries resolve through `-f`. Equivalent repeated references have one selection identity. Multiple distinct selections require an explicit destination even when they select sections from the same file.
- Literal underscores are preserved. Advice to prefer hyphens replaces the previously suggested escaping scheme; it does not establish arbitrary-input collision freedom.
- The namespace of linked dependencies and metadata grouping does not supply an output basename. Naming starts with the selected entry source.
- Every affected stdout consumer is migrated in the runtime task if it depends on the default. Historical captures remain evidence of their recorded revision.

## Dependency Review

The local chain is W01 → W02 → W03 → W04 → W05 → W06 → W07 → W08. No existing task is renumbered, unticked or reused to claim new work. All independent pairs are ordered; Joins remains empty. Each new row declares one component and covers at most three criteria. The final corpus audit is its own last task.

The initiative graph reports no unresolved dependencies. It retains independent pairs and missing older component declarations already recorded by the original metadata planning review; this change does not claim to repair unrelated initiative planning. Exact component contention is assessed only for supplied work items. E06 retains priority 6 ahead of E04 at 5: the contract and compiler components already overlap, and the new rows do not introduce a new scheduling relationship.

The freeze's E07 W02 dependency now consumes E06 W08, which includes the delivered metadata audit through its prerequisite chain. The freeze cannot use the earlier completed W05 audit as evidence for the new output contract.

## Planning Validation

- Epic coverage, task grain, ordering and local dependency checks pass.
- Initiative, freeze and authoring-proposal format checks pass with zero findings.
- The epic formatter reports one intentional exception: its References contain review PRs #220 and #222. The user explicitly requested those visible links; preserve them rather than applying the skill's conflicting body-link restriction.
- Source baseline: runtime epic head `93fe6b354a85e244f64e33af700a55aab4f26044`. Current CLI output selection and atomic publication are in `src/prosiform/cli.py`, with the operational interface in `invocation.md`.
- No runtime implementation or runtime-test execution is part of this planning request. Future test obligations are in the new work items.

## Plan Changes

- Applied folded work: add the accepted output naming contract to epic #218 and initiative #20.
- Applied task creation: W06–W08 and AC13–AC18; preserve W01–W05 and AC1–AC12 as complete.
- Applied handoff updates: freeze #23 consumes the new final audit; authoring proposal #208 records underscore and automatic naming requirements.
- Applied board status: the extended epic returns to In Progress, with its two review PRs still draft. Priority and queue order are retained.
