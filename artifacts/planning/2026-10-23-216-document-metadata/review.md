# Epic Review

## Goal Trace

| Confirmed goal | Initiative criterion | Epic criteria | Delivering work |
| --- | --- | --- | --- |
| Each file owns its structural settings | AC12 | AC1, AC5, AC8 | W01, W03, W04 |
| Caller and section selection preserve those settings | AC12 | AC8, AC9, AC12 | W04, W05 |
| Metadata follows the Agent Skills convention | AC12 | AC1, AC2, AC3, AC4, AC6, AC7, AC11 | W01, W02, W03, W05 |
| No structural CLI arguments are required | AC12 | AC10, AC11, AC12 | W04, W05 |
| Contract precedes implementation | AC3 | AC1 | W01 |

Every epic criterion has exactly one delivering row. Every row covers at most three criteria and declares one component. Tests accompany their implementation units; the authoring task's corpus run is additional release evidence. There are no unobservable acceptance criteria.

## Dependency Review

The epic's local format check reports zero fixes, metadata changes or content decisions. The local graph passes with no unresolved dependencies, numbering findings or independent task pairs. Its longest chain is W01 → W02 → W03 → W04 → W05, five steps. Joins is empty because every pair is ordered by that chain.

Section Composition E04 W01 and Document Metadata E06 W01 both amend the canonical design. Their compiler tasks also overlap by directory containment even though the dependency tool compares exact component strings. Recommend priority 4 for E06 after E04 at 5; this is scheduling separation, not a claim that the metadata contract consumes the composition feature.

No whole-epic prerequisite is inferred merely from shared files. The contract can be specified against current main. At delivery, reconcile the current base with any landed composition changes and preserve its source context and deferral contract. A missing implementation behavior required by a chosen base is an integration finding, not authority to broaden this epic.

The initiative-wide graph has inherited findings: missing component declarations in ledger, revision and freeze work items, and unresolved independent-task pairs in older epics. These are outside this new epic's scope. The local pass is not an initiative-wide clean bill of health or readiness claim. Its relative E04/E06 contention conclusion is supported by inspected task files; other epics retain their existing scheduling labels.

## Freeze Handoff

The freeze's final task must consume this epic's final verification output before tagging the contract. The proposed update adds E06 W05 to that task's dependencies. Because its current E05 identity precedes E06 and no fetched pull request names it, the proposed freeze identity is E07. Preserve its issue number #23, existing criteria, work-item links and other dependencies. No other epic is renumbered. This is a required handoff for the new source-language contract, not delivery of the freeze itself.

## Review Findings Resolved in the Draft

- **Task grain:** The preliminary four architectural stages became five component-scoped work items with no row covering more than three criteria.
- **Source ownership:** Metadata is stored on the captured source, never inherited from a caller or discovered from directory membership.
- **Legacy parsing:** The contract explicitly changes arbitrary discarded frontmatter into validated YAML; the work items require matching fixtures and diagnostics.
- **Deferred contribution:** A normally opened deferred target receives local metadata validation, but only contributing documents participate in group-depth conflicts.
- **Consumer drift:** The implementation task updates immediately affected invocation and corpus checks; the final task audits wider author guidance and representative sources.
- **Publication:** Priority confirmation remains pending. All implementation criteria remain unticked; this review validates planning, not compiler behavior.

## Planning Validation

- Epic, initiative update and freeze handoff format: pass, zero findings.
- New epic dependency graph: pass, five-step chain, no independent pairs.
- Initiative graph: inherited findings retained as described above; no unrelated repair is included.
- Source requirements: proposal #216 and the Agent Skills metadata convention are covered by the trace. The existing normative design is the amendment target, not a claim that it already specifies metadata conversion.
- Tracker publication and saved-body verification: pending priority confirmation.
