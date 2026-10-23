# File-Owned Invocation Planning Review

## Goal Trace

| Confirmed outcome | Initiative criterion | Epic criteria | Work |
| --- | --- | --- | --- |
| File-only invocation has a normative contract | AC3, AC13 | AC13 | W06 |
| Root metadata follows Agent Skills string-valued fields | AC13 | AC19 | W07 |
| Linked sources inherit their parent root unless they declare one | AC13 | AC20, AC21, AC22 | W08 |
| Whole-file and section names reflect entry identity | AC13 | AC14 | W09 |
| Combined selections require an explicit destination | AC13 | AC15 | W09 |
| Derived destinations preserve publication safety | AC13 | AC16 | W09 |
| Authors prefer hyphens to avoid flattened-path ambiguity | AC13 | AC17 | W10 |
| File-only invocation preserves compiled content | AC13 | AC18 | W10 |

Existing metadata criteria AC1–AC12 retain their completed work and original goal trace to initiative AC12. The extension belongs to epic #218. Authoring proposal #208 consumes the root and naming requirements; implementing that skill remains separate.

## Decisions

- The normal command is `pf <file>`. Each explicit root resolves relative to its declaring file's directory. A linked file without a root inherits its linking parent's effective root, transitively. A direct entry without a root uses its containing directory. Invalid values fail validation.
- The user selected strict Agent Skills compliance: flat prefixed string fields under `metadata`. Group and depth remain file-owned; only an absent root inherits.
- A linked file can declare a separate library root. Shared physical source bytes remain captured once; traversal preserves inherited-root context. The contract task specifies deterministic deduplication and cycles for files reached through different root contexts, and the resolver task tests them.
- Automatic output is in the working directory. Sections append `__fragment`. Multiple distinct selections require an explicit destination; equivalent repeated references count once. Explicit file and stdout destinations remain available.
- Literal underscores remain literal. Authoring guidance recommends hyphens; it does not promise collision freedom for arbitrary paths.
- Linked roots do not rename the selected entry's bundle. Active consumers migrate in the implementation unit that changes their invocation.

## Dependency Review

The local chain is W01 → W02 → W03 → W04 → W05 → W06 → W07 → W08 → W09 → W10. Completed tasks retain their numbers and evidence. Every new row declares one component and covers at most three criteria. No local dependency or Joins finding remains. The final authoring and corpus audit is a separate last task.

The initiative graph reports no unresolved dependencies. Its older independent-pair Joins and missing component declarations remain the inherited limitations recorded by the original metadata review; this extension does not claim to repair those other epics. Exact component contention is assessed only for supplied work items. Priority 6 and the accepted next-epic ordering are retained.

Freeze E07 W02 consumes E06 W10, including the completed metadata audit through its dependency chain. W05 alone cannot establish the new invocation contract.

## Planning Validation

- Epic task grain, coverage, ordering and local dependency checks pass; see `dependency-local.log`.
- Initiative, freeze and authoring-proposal format checks pass with zero findings; their format logs are retained alongside this review.
- The epic formatter reports one intentional exception: visible review PR links #220 and #222. The user explicitly requested those links, overriding the skill's body-link restriction.
- The initiative dependency report retains the pre-existing limitations described above; see `dependency-initiative.log`.
- Runtime content baseline: `93fe6b354a85e244f64e33af700a55aab4f26044`. No compiler changes or runtime tests are part of this planning request. Implementation test obligations are recorded in W06–W10.

## Plan Changes

- Epic #218 has five completed tasks and five planned tasks, with AC13–AC22 covering the extension.
- Initiative #20 records file-only invocation; freeze #23 consumes W10; proposal #208 records root inheritance and naming guidance.
- Epic status is In Progress. Runtime review #222 remains draft. Contract review #220 is merged; W06 needs a successor contract review. Visible PR references remain in the epic.
