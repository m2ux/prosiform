# Review Findings

> Findings · Created 2026-10-29

Read at head `41d5063b` in a detached worktree, before #386 merged. Each finding below states what the tree showed and what was changed for it. Findings are ordered by what a reader would hit first, not by size.

## Corrected on the epic branch

### The example's quotes were of a tree that no longer existed

`example/README.md` teaches what `pf` produces by quoting a source operation and its expected bundle. Both quotes showed `### *Record* Epic Delivery` with a prose `**Inputs:**` line and numbered list steps, and `#### *Read* Tracker Issue` in the group example. The source had become `### Record Epic Delivery` with contract links and `#### 1. Run Sync Epic` sub-sections, and the bundle at `fixtures/usage-example/artifacts-and-references-under-declared-groups/expected/modes_hoist-mode.bundle.md:169` already read `#### Read Tracker Issue`.

The page sits outside `example/work-planner/`, which is the tree `checks/authoring.py` reads, so `make check` could not see the drift.

- The input quote is taken from `artifacts/epic-issue-body.md` and the output quote from the fixture's expected bundle, both verbatim.
- Each quote shows the operation's opening — contract links and both step headings — and says so, because the full operation is too long to quote and an unmarked elision would misrepresent it.
- `c4222dbd`.

### The configuration named a deployment this project does not have

`configuration.md:26-31` fixed four themes — `theme:canon`, `theme:language`, `theme:mechanical`, `theme:delivery` — as this deployment's values. The repository carries one theme label, `theme:bundling`, and board 18 is the bundling board. Promoting workflow-server's themes from example values to configuration made the sample assert a deployment that does not exist.

- The table names `theme:bundling` alone.
- The two declared-group fixtures that compile the document are regenerated from the build under test.
- `c4222dbd`, `a76b4409`.

### A guideline contradicted the file stating it

`example/guidelines.md:112` read "No file has a Commands section" under the heading `## Commands` at `:109`. Read as absolute, the rule forbade the section that stated it.

- The rule now binds skill files and says where a command lives, so the section it sits in is not the thing it bans.
- `c4222dbd`.

### The epic review said the corpus-ordering defect was unplaced

#386's Open Questions said #398 "proposes reordering `check`; it is outside this epic's rows and is not delivered here". #398 is `[I05:E05:W02]` with a row and criterion, so a reviewer was told the work had no home after it had gained one.

- The bullet names the row and criterion that carry it.
- Pull request body.

## Reported, not corrected

### The Inputs rule accepts a target that is not a contract section

`checks/authoring.py` states in its docstring that each Inputs link's target is a contract section, but `LINK_LIST` requires only a `#fragment`. `[Step](#1-commit)`, `[Gone](#no-such-heading)` and `[Op](#publish-record)` all pass.

`make links` catches the unreadable anchor, so a broken link is not silent; what nothing rejects is a step or operation anchor standing in for a contract. The rule is stated twice — in the check's docstring and in the guidelines — and the two disagree.

Left as it stands because narrowing the check is a change to what the rules accept, not a correction of a departure from them. It belongs with the authoring rules, where the rule and its instrument move together.

## Checked and holding

- **Contract links resolve.** All 715 Inputs and Outputs links across every operation resolve to an existing file and heading.
- **One H1 per file.** All 59 documents under the example carry exactly one.
- **No retired rule survives in the example.** No emphasised operation verbs, no `## Commands`, and no "Spec layout", "Returned output" or "Command implementation" prose remain under `example/work-planner/`.
- **Fixtures agree with the source.** Regenerated for every changed file, and the corpus passes 342 of 342 at the merged head.
- **The checks hold.** `make authoring` (0 findings over 59 documents), `make steps`, `make tables`, `make layout` and `make vocabulary` all pass; `make links` resolves every local link, leaving the 18 references that need the network.
