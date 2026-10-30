# Frontmatter And Root Decisions

## Confirmed Contract

- Frontmatter contains a top-level `prosiform` mapping.
- Keys use full names: `root`, `group`, `group-depth`.
- Root and group are strings; group-depth is an integer from 1 through 6, paired with group.
- Every absent root uses the working directory captured for the invocation, including linked sources.
- An explicit relative root resolves from the declaring file's directory.
- The command is `pf`; operational parameters retain short flags.

```yaml
---
prosiform:
  root: ".."
  group: modes
  group-depth: 2
---
```

## Delivery Obligations

W06 defines this contract. W07 implements the mapping and root value, with schema tests covering AC19 and AC23 and immediately affected consumers. W08 tests working-directory defaults for entries and linked files, including a caller whose directory differs from both source directories. W11 audits authoring guidance and corpus behavior. The reserved W06 row remains held until its release is explicitly authorized.

## Plan Changes

- Applied, folded work, epic #218: top-level settings schema in W06/W07 and AC23; invocation-directory defaults in W08/AC21; short-command and full-key guidance in W11.
- Applied, folded work, proposal #208: matching frontmatter and default-root requirements for the authoring handoff.
- Applied, interview decisions, epics #187 and #218: approved shorter task descriptions, W09-clause removal and removal of review PR entries from References.

## Validation

Planning validation covers issue format, local dependencies and consistency of the active design and work items. Compiler implementation and runtime verification belong to delivery of W06–W11. Completed W01–W05 retain their original delivery evidence; it does not verify AC23.

- Issue format: #218 and #208 each report zero fixes, applications or decisions.
- Local dependency check: all eleven task components supplied; no dependency, Joins, numbering or contention findings.
- Whitespace check: git diff --check passes.
- Active-plan search: no obsolete prefixed keys or parent-root inheritance rules remain in the revised records.

## Linked Bootstrap Task

The confirmed specimen has at least three links in SKILL.md. The agent reads SKILL.md directly and compiles the linked targets separately. W10 owns the installed-command suite and preserves source trees, commands, diagnostics and resulting bundles in planning for visual inspection and later reference. W11 is the final authoring audit; the freeze depends on E06:W11.
