# File-Owned Invocation Planning Review

## Goal Trace

| Confirmed outcome | Initiative criterion | Epic criteria | Work |
| --- | --- | --- | --- |
| File-only invocation has a normative contract | AC3, AC13 | AC13 | W06 |
| Top-level Prosiform settings have a bounded schema | AC13 | AC19, AC23 | W07 |
| Every absent source root uses the invocation working directory | AC13 | AC20, AC21, AC22 | W08 |
| Whole-file and section names reflect entry identity | AC13 | AC14 | W09 |
| Combined selections require an explicit destination | AC13 | AC15 | W09 |
| Derived destinations preserve publication safety | AC13 | AC16 | W09 |
| Skill links compile independently with divergent frontmatter | AC13 | AC24 | W10 |
| End-to-end artifacts remain inspectable reference examples | AC13 | AC25 | W10 |
| Authors prefer hyphens to avoid flattened-path ambiguity | AC13 | AC17 | W11 |
| File-only invocation preserves compiled content | AC13 | AC18 | W11 |

Existing metadata criteria AC1–AC12 retain their completed work and original goal trace to initiative AC12. The extension belongs to epic #218. Authoring proposal #208 consumes the root and naming requirements; implementing that skill remains separate.

## Decisions

- The normal command is `pf <file>`. Each explicit root resolves relative to its declaring file's directory. Every absent root uses the invocation working directory, including linked files. Invalid values fail validation.
- Frontmatter contains a top-level `prosiform` mapping with full key names: `root`, `group` and `group-depth`. Root and group are strings; group-depth is an integer from 1 through 6, paired with group. An absent root uses the invocation working directory for every source, including linked files. Explicit roots resolve relative to the declaring file's directory. Empty or malformed values fail validation. The command is `pf`, with short operational flags such as `-o` and `-f`. This is a Prosiform frontmatter extension; strict Agent Skills schema compatibility is not a requirement.
- A linked file can declare a separate library root. Shared physical source bytes remain captured once; a source has one effective root per invocation. The contract task specifies deterministic deduplication and cycles for files reached through different parents, and the resolver task tests them.
- Automatic output is in the working directory. Sections append `__fragment`. Multiple distinct selections require an explicit destination; equivalent repeated references count once. Explicit file and stdout destinations remain available.
- Literal underscores remain literal. Authoring guidance recommends hyphens; it does not promise collision freedom for arbitrary paths.
- Linked roots do not rename the selected entry's bundle. Active consumers migrate in the implementation unit that changes their invocation.

## Dependency Review

The local chain is W01 → W02 → W03 → W04 → W05 → W06 → W07 → W08 → W09 → W10 → W11. Completed tasks retain their numbers and evidence. Every new row declares one component and covers at most three criteria. No local dependency or Joins finding remains. The final authoring and corpus audit is a separate last task.

The initiative graph reports no unresolved dependencies. Its older independent-pair Joins and missing component declarations remain the inherited limitations recorded by the original metadata review; this extension does not claim to repair those other epics. Exact component contention is assessed only for supplied work items. Priority 6 and the accepted next-epic ordering are retained.

Freeze E07 W02 consumes E06 W11, including the completed metadata audit through its dependency chain. W05 alone cannot establish the new invocation contract.

## Planning Validation

- Epic task grain, coverage, ordering and local dependency checks pass; see `dependency-local.log`.
- Initiative, freeze and authoring-proposal format checks pass with zero findings; their format logs are retained alongside this review.
- The epic References section contains its source and planning records; delivery links remain in the task table and Development relation.
- The initiative dependency report retains the pre-existing limitations described above; see `dependency-initiative.log`.
- Runtime content baseline: `93fe6b354a85e244f64e33af700a55aab4f26044`. The preserved prototype ran its three link invocations against this baseline; each failed because the compiler requires the root flag. No bundles were produced. These failures demonstrate missing behavior; implementation validation belongs to W06–W11.

## Plan Changes

- Epic #218 has five completed tasks and six planned tasks, with AC13–AC25 covering the extension.
- Initiative #20 records file-only invocation; freeze #23 consumes W11; proposal #208 records working-directory defaults and naming guidance.
- Epic status is In Progress. Runtime review #222 remains draft. Contract review #220 is merged; W06 needs a successor contract review.

- Task creation, epic #218: W10 delivers linked skill bootstrap tests and published reference artifacts (AC24, AC25).
- Re-prioritisation, epic #218 and freeze #23: the unstarted authoring audit is W11 after W10; the freeze consumes E06:W11.
