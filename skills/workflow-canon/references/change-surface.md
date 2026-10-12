# Change Surface

Author and Audit use the same captured inventory, applicability matrices and evidence gates. Scripts establish structural coverage; independent agents establish semantic accuracy.

## Capture

1. **Locate the record.**
   Resolve the shared [planning record](planning.md), corpus root and paired engine. Each run has its own directory beneath that record. Read the [audit command conventions](commands.md#audit-command-conventions) before the first audit command.
2. **Declare the scope.**
   Fill the [scope input](../templates/audit-scope.json) with paths relative to the corpus root, the exact base commit when comparing changes, and checks selected through [canon context](canon-context.md#checks). Include supporting resources, READMEs, routines, unchanged consumers and relationship context. The guard obligation is required. Candidate draft bytes must exist in an isolated corpus tree before capture.
3. **Capture the bytes.**
   [Initialize the surface](commands.md#initialize-audit-surface). It captures source bytes, revisions, parser/tool identities, deleted base files, all AP/DP entries and supplemental canon units. Four Markdown documents contain workflow, technique, routine and activity tables separated by source and section; empty types explicitly say so. The coordinator owns the state and generated views.
4. **Check the proposed inventory.**
   Read [Identity](#identity), then assign [independent inventory verification](audit-dispatch.md#phases). Verifiers derive expected items and relationships from captured sources and the corpus manifest. They compare the proposed rows, complete AP/DP inventory, diagnostics and unselected files against those expectations. Automated extraction is a candidate inventory, including unresolved reference candidates; it does not establish completeness.

## Identity

- **Items.**
  Rows use the source path and native section, rule, input, output or step identifier. Nested steps retain their full ancestry and duplicate occurrences. Positional prose, paragraphs and candidate clauses use revision-bound source addresses. Independently testable constraints sharing one line need separate clause rows; verifiers add any missed boundary through the scope input's `rows` list. Whole-section, whole-element, missing-structure and relationship rows retain checks that span items.
- **Relationships.**
  Each call records its source, target, binding site, executing workflow and complete routine reference chain. Instantiations are separate from routine declarations. Check the paired engine's resolution and inheritance semantics; record ancestor sources and both endpoints explicitly. Add relationships and required context through the scope input when extraction cannot resolve them. An unresolved target can be a measured defect, but uncertainty about its actual target or context leaves inventory verification disputed.
- **Supporting material.**
  Resource and README rows belong to Workflow / Supporting Material under their actual namespace and source path. A namespace without a workflow definition remains a namespace. Shared content has one content row; referencing elements have relationship rows.
- **Criteria.**
  AP identity uses the canonical named entry; its current AP number is a display alias. DP aliases retain their numbered source headings and titles. Every row accounts for every captured AP and DP. Fires-on hints can order work; absent metadata or a missing lookup command cannot remove cells. The [canon inventory](canon-map.md#unit-inventory) also supplies family, creation-rule, convention and guard obligations.

## Applicability

Use [mapping assignments](audit-dispatch.md#phases) to decide every cell in the full row × AP/DP product. Each cell links to source evidence and exactly one disposition:

| Status | Evidence |
| --- | --- |
| `A` | The criterion's scope and the construct that makes it apply |
| `N` | The criterion's excluding wording and source facts satisfying it |
| `U` | The evidence or decision still missing |

### Shared Reasons

Shared reasons name the exact assigned row set and hold for every member. A clean result or a Do not flag exception is an evaluation under an applicable criterion; it does not by itself establish inapplicability. Blank cells are unresolved. Table pagination preserves every logical pair exactly once.

### Cell Verification

After all decisions are `A` or `N`, independent verifiers check every cell, including every exclusion, against the original criterion and source. They cannot verify cells they mapped. The receipt binds the exact mapping reason, disposition and evidence. Disputes return to the coordinator for correction through [reset](commands.md#reset-audit-cells) or [refresh](commands.md#refresh-audit-surface), then fresh verification. Open the evaluation gate only when [status requires the map](commands.md#check-audit-status) successfully.

## Evaluation

### Worker Obligations

Assign the verified applicable cells through [dispatch](audit-dispatch.md#phases). Workers follow the complete [walk rules](walk-rules.md), read the full source and required relationship context, and return evidence for each pass, finding or blockage. Reconcile returns through the typed [receipt](audit-dispatch.md#returns). Whole-file reads, supplemental units, selected project checks and independent finding confirmation are separate obligations. A command result carries its command, working directory, exit status and captured output; an unmeasured check stays blocked.

### Remediation Authority

The calling mode owns remediation authority. Corrections to definitions return through Author's draft procedure. Review-only audits report findings. Workers have read authority; authorized edits are serialized by the coordinator or assigned disjoint file ownership before execution.

## Completion

### Required Evidence

The audit is complete only when the current inventory is independently verified, every AP/DP cell has independently verified applicability, every applicable cell has an evidence-backed pass or finding, and every whole-file read, supplemental unit, required check and finding confirmation is settled. Unknown, disputed, stale, unread, unmeasured or blocked work keeps it incomplete. Every required item has one reconciled primary result; retries cannot overwrite accepted items. Use [status requiring completion](commands.md#check-audit-status) for the final claim.

### Coverage and Conformance

Coverage completion and conformance are separate. Confirmed violations can have complete coverage; [reporting](reporting.md#report-context) determines their bands and verdict. A user stop or resource limit leaves a saved incomplete run with its residual, never a finished audit.

## Freshness and Resume

- **Inspect the run.**
  Start with [status](commands.md#check-audit-status), which returns bounded counts, generation identity and artifact paths. Locate residuals through the coverage document's headings and assignment identifiers; issue the relevant [packet](commands.md#write-audit-packet) for source, mapping and ownership detail. The script-owned JSON ledger stores the complete dataset and is accessed through these projections.
- **Source generations.**
  Any corpus membership/byte change, scope correction, canon change, parser/engine change or audit-tool change blocks use of the captured generation. [Refresh](commands.md#refresh-audit-surface) captures the current generation and invalidates all its mapping, verification and evaluation evidence because cross-element dependency reach can exceed local source rows. An identical generation preserves its pending work. Archived state and immutable returns retain prior evidence.
- **Mapping corrections.**
  [Reset](commands.md#reset-audit-cells) invalidates a selected mapping and its verification/evaluation, including intersecting assignments. A reason or evidence edit changes the mapping fingerprint. Renewed evaluation waits for the entire current map to be verified.
- **Interrupted workers.**
  Accepted partial work remains recorded. [Retry](commands.md#retry-audit-assignment) retires an assignment and [planning](commands.md#plan-audit-assignments) assigns its unresolved residual. A fresh agent can continue after the coordinator checks captured identities and current status.
- **Author byte agreement.**
  Before applying a verified draft, compare its captured source hashes with the bytes to write. After writing, capture the actual working tree and run its selected checks. Reuse evidence only for an identical generation; changed roots, contracts or candidate bytes require their current verification. A draft-only request makes no commit-completion claim.

## Artifacts

| Artifact | Role |
| --- | --- |
| `audit-state.json` | Coordinator-owned inventory, evidence, assignments and history |
| `change-surface-{workflow,technique,routine,activity}.md` | Section matrices, including explicit empty types |
| `audit-evidence.md` | Cell reasons, independent receipts and evidence links |
| `audit-coverage.md` | Inventory, criterion aliases, assignments and residuals |
| `sources/` | Captured source and check-output bytes |
| `worker-results/` | Immutable typed returns by assignment and attempt |
| `generations/` | Prior state when the captured generation changes |
| `audit-report.md` | Generated standalone findings and completion status |

For a workflow-owned report, follow [Workflow Reports](reporting.md#workflow-reports) and transfer the generated counts, residuals and links into that guide's layout. The generated coverage remains authoritative.
