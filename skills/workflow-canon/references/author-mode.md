# Author Mode

Writes definition content: a new definition, or a specified change to existing ones, such as a work item, a finding, or a defect with a location. A finding is closed with the Fix its entry states.

## Prerequisites

Read the [canon prerequisites](canon-context.md#prerequisites), then its [terms](canon-context.md#terms) and [criteria](canon-context.md#criteria).

## Procedure

1. **Resolve to files.**
   - List every file the change adds or edits. A new definition also edits each file that wires it in, such as `workflow.yaml` or the activity that binds it.
   - Add the I/O-contract closure and consumers per the shared [scope](canon-context.md#scope).
   - For a specified change, the surface is the specification, not the diff. Confirm it still holds against the tree: the construct is where it says, the count is what it says, the absence is an absence.
   - What has moved is reported first. Where nothing remains to change, that is the finding.
2. **Read what binds.**
   - Read the [design flow](design-flow.md). Structure is synthesised from expected behaviour. Exposed behaviour is derived from that structure and compared with the expected behaviour. A failed comparison reformulates the structure, the expected behaviour, or the function.
   - Read the shared [change-surface lifecycle](change-surface.md). Intended items can have provisional planning rows; applicability and evaluation bind captured draft bytes.
   - When the change answers a finding, follow that entry's Fix and Do not flag.
3. **Open a live sibling.**  Conformance compares against those files.
4. **Preserve.**  Name what the entries require the change to preserve.
5. **Walk the draft, then write.**
   - Each fix is a draft of its own: its replacement text is walked before it is written.
   - Capture the candidate in an isolated corpus tree, create all four matrices, and follow the shared lifecycle through independent inventory and mapping verification before evaluating the draft. Prioritize the prescribing entry without dropping any AP/DP cell.
   - Rewrite while an entry still fires.
   - Before writing definitions, read the [edit hook](canon-context.md#edit-hook). Apply the evaluated bytes through [Author Byte Agreement](change-surface.md#freshness-and-resume), then run the selected [checks](canon-context.md#checks).
6. **Check what the pass wrote.**
   - Reconcile actual bytes and affected consumers using [freshness](change-surface.md#freshness-and-resume). Every correction receives its current inventory, mapping verification and evaluation.
   - A hit is a `fix` finding, per Audit's [Attribution](audit-mode.md#attribution). Close it by step 5 before any report.
7. **Stop on oscillation.**
   - Stop when an entry fires on text written to satisfy it, or when a round's `fix` findings do not fall below the round before.
   - Report the entries in conflict to the user as a canon defect, with the text each one rejected.
8. **Audit.**
   - Reconcile the current run through the shared [completion gate](change-surface.md#completion). Read [Report Context](reporting.md#report-context) before [report selection](reporting.md#which-report).
   - A draft-only request stops with its measured draft coverage and writes no findings register for a commit.

## Rules

- **Commit gate.**  A definition change commits only once the procedure's audit is complete.
- **Scope.**
  Changes close the specified requirement or confirmed finding, including its affected consumers. Canon defects that prevent convergence are reported with the conflicting entries.
