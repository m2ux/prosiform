# Execution Decisions

- User correction: continue all eligible work items within I10 E07 without stopping after each task. Work remains sequential by dependency and within the epic.
- Retain lane 1 and the `--presets` CLI contract. I11 waits for I10.
- Repository auto-close remains user-confirmed disabled. Task merges into epic bases are authorized; human review requirements govern integrations into long-lived branches.
- Preserve unrelated dirty E04 worktrees and other branches.
- The absent `config/branches` statements on main and engineering remain an explicit integration-check limitation. Names are declared on workspace; target routes are checked directly. Resolve the epic's complete readiness evidence before claiming handoff.
- Fresh active rules require one human approving review on both `main` and `engineering`. Complete all E07 task merges, integration overviews, exact-revision validation and agent reviews before the review handoff. No protection bypass supplies that approval.
- Applied Folded work: the guide specifies `--entry=-guide.md --presets=-checks` for values beginning with a dash. The current immutable design pin is `795bbfb67c66b02193f0313138f59f18aa6c5274`; the CLI/caller/fixture unit adopts it. Only the guide's four-line clarification changes from candidate `c67cf78f020923c4e5bd25d95497ced206be7161`.
