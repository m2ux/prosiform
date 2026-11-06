# Delivery Decisions

- User, 2026-11-06: I10 E07 is next, on its assigned lane 1. I11 waits until I10 completes.
- Release measurement depends on issue #464 closing, alongside its existing completed prerequisites. No I11 work is reserved or started.
- The authorized delivery boundary is I10 E07; lane 1 is selected through the user's explicit direction to deliver that epic.
- Existing E04 integration review and its retained worktrees stay separately owned.
- Long-lived branch names are declared by config/branches on origin/workspace: engineering, main and workspace. The main and engineering revisions do not carry that configuration. This difference remains explicit in automated delivery diagnostics.
- Planning documents are published from the one shared engineering worktree under Planning Record. W00 is a design-document delivery, and Task Delivery admits a commit as its delivery link.

- E07 task-file links use blob/engineering so the delivery survey reads their declared components.
