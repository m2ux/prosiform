# Delivery Decisions

- User, 2026-11-06: I10 E07 is next, on its assigned lane 1. I11 waits until I10 completes.
- Release measurement depends on issue #464 closing, alongside its existing completed prerequisites. No I11 work is reserved or started.
- The authorized delivery boundary is I10 E07; lane 1 is selected through the user's explicit direction to deliver that epic.
- Existing E04 integration review and its retained worktrees stay separately owned.
- Long-lived branch names are declared by config/branches on origin/workspace: engineering, main and workspace. The main and engineering revisions do not carry that configuration. This difference remains explicit in automated delivery diagnostics.
- Planning documents are published from the one shared engineering worktree under Planning Record. W00 is a design-document delivery, and Task Delivery admits a commit as its delivery link.

- E07 task-file links use blob/engineering so the delivery survey reads their declared components.

- W00 uses task PR #663 into i10/e07/engineering. Its raw design and current-pin conformance reports are published in the W00 record. The task remains undelivered while the PR is open.
- Exact variant naming is --p- plus the full lowercase SHA-256 of canonical UTF-8 compact JSON: matched declared preset names, distinct, declared spelling retained, sorted by Unicode code point. The design supplies a fixed example.
- Main's design pin and the old fixture clause identifiers are adopted together by the joined CLI/caller/fixture unit. W00's immutable candidate pin does not assert current compiler support.
- Epic sync links W00 to its PR and reports missing config/branches at the engineering base, leaving automated base/target checks unevaluable. The target branch, SHA, protection and active rules were inspected directly; no full epic readiness is claimed.
- Repository automatic issue closure is unexposed through REST and GraphQL. A native confirmation question is pending; no delivery merge or Development-link edit is attempted without that answer.
