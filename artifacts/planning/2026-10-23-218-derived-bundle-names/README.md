# File-Owned Root And Bundle Names

Planning extension to epic #218. The user confirmed `pf <file>`: root metadata replaces the root option, and the selected file or fragment determines the output filename. This request plans the changes; it implements no compiler behavior.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [Design](design.md) | Accepted command, root metadata, naming and safety boundaries |
| [Epic](epic.md) | Preserved completed work and five follow-on tasks |
| [Initiative](initiative.md) | Parent goal and coverage extension |
| [Freeze](freeze.md) | Final audit dependency |
| [Authoring handoff](authoring-handoff.md) | Root and naming requirements for the planned skill |
| [W06](w06.md) | File-owned invocation contract |
| [W07](w07.md) | Bounded root metadata |
| [W08](w08.md) | Per-file root resolution |
| [W09](w09.md) | Derived output publication |
| [W10](w10.md) | File-only authoring audit |
| [Review](review.md) | Goal trace, dependency and validation findings |
| [Reconciliation](reconciliation.md) | Confirmed frontmatter and default-root decisions |

## Decisions

- Normal command: `pf work-planner/modes/align-mode.md`.
- Root: `prosiform.root: ".."`, relative to the declaring file's directory. Every absent root uses the invocation working directory, including linked files. The root is file-owned.
- Output: `modes_align-mode.bundle.md` in the working directory; a section adds `__fragment`.
- Multiple distinct selections require an explicit combined destination. Explicit file/stdout output overrides remain available.
- Source paths should use hyphens rather than underscores. No escaping scheme is added.
- Completed tasks W01–W05 and criteria AC1–AC12 stay complete. New work is W06–W10, with AC13–AC23.
- Epic #218 remains priority 6 and returns to In Progress. Runtime review #222 remains draft; contract #220 is merged, and new contract work needs a successor review.

## Progress

- [x] Inspect current delivery and accepted decisions.
- [x] Validate root and naming extension with related handoffs.
- [x] Publish the final plan, discussion and board state.

## Frontmatter Schema

Frontmatter contains a top-level `prosiform` mapping with full key names: `root`, `group` and `group-depth`. Root and group are strings; group-depth is an integer from 1 through 6, paired with group. An absent root uses the invocation working directory for every source, including linked files. Explicit roots resolve relative to the declaring file's directory. Empty or malformed values fail validation. The command is `pf`, with short operational flags such as `-o` and `-f`. This is a Prosiform frontmatter extension; strict Agent Skills schema compatibility is not a requirement.
