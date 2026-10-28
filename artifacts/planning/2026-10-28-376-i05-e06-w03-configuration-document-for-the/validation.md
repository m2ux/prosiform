# Validation — I05:E06 W03

Run on branch `i05/e06/w03-configuration-document-for-the` at `2cb35ebd`, cut from `i05/e06/main` at `6dc691dd`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`.

## T1 Configuration Inspection

`example/work-planner/` inspected against AC3 and the [binding inventory](w03.md#binding-inventory). Observes AC3.

- **One home.**  `configuration.md` states each binding once, with its meaning and allowed values: kind, theme and priority labels; the proposals board title; the two template titles; the Status field and its options for each board kind; the proposals Priority field; the engineering branch and its records folder; the standup window and Ready count.
- **Entry point.**  `SKILL.md` links `configuration.md` after its opening paragraphs.
- **Bindings rule.**  `guidelines.md` › Prose › Bindings links `configuration.md` in place of the plain words "the configuration document".
- **Every other occurrence links.**
  - Body Titles (`proposal-body.md`, `initiative-issue-body.md`, `epic-issue-body.md`, `task-body.md`, `standalone-body.md`) link Kind Labels and Theme Labels.
  - `board.md`: the Themes table moved to Theme Labels; One Theme, the Proposals field, Copy Project Board, Create Proposals Board, Create Theme Board, Select Project Board and Read Board State link their entries. Find Proposals Board and Find Status Field take `<proposals-board-title>` and `<status-field-name>` parameters their Inputs link.
  - `board-queue.md` › Priority Sets links Priority Labels for the label's name, colour and description.
  - `planning-record.md`: Find Engineering Worktree takes `<engineering-branch>`, List Planning Records takes `<records-folder>`, and the planning-folder path composes from the records folder; the calling steps link Engineering Branch.
  - `pull-request-body.md`, `epic-issue-body.md` › Reserve Row and `propose-mode.md` link Engineering Branch or Proposals Board.
  - `standup-report.md` › Scope, Sections › Next and Summarise Progress link Standup Window and Standup Ready Count.
- **Sweep.**  A search of `example/work-planner/` for every literal the inventory lists finds it only in `configuration.md`, in labelled examples, in the conventions' Example values list, and in step headings naming a template by role. Each of those is outside the binding definition the work item states.
- **Confidentiality.**  The diff adds no name outside this repository; it removes one.
- **Result.**  Pass.

## T2 Anchor Sweep

The three entries whose bundles changed (`modes/advance-mode.md`, `modes/plan-mode.md`, `modes/hoist-mode.md`) were regenerated from `example/work-planner` with `pf -o <scratch> <entry>` and copied into `expected/`. The sweep over those bundles, and over every `expected/` bundle under `fixtures/usage-example/`, reports `unresolved links: 0` and 0 suffixed step anchors. Pass.

## T3 Links

`make links`: `link check: every reference in 107 document(s) resolved`. Pass.

## T4 Steps

`make steps`: `step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections`. Pass.

## T5 Corpus

- **Bundles reached.**  Configuration is bundled as a whole document after the Artifacts and Protocols groups. Three usage examples changed: `a-mode-and-the-board-reads-it-steps-through`, `a-procedure-and-everything-it-reaches` and `artifacts-and-references-under-declared-groups`. The first two manifests' descriptions name the Configuration document their bundles now carry.
- **Corpus.**  `make corpus`: `corpus check: 342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass`.
- **Result.**  Pass.

## T6 Repository Checks

`make check` exited 0: ruff `All checks passed!`, format `67 files already formatted`, mypy `no issues found in 66 source files`, tests `1302 passed`, harness `743 passed`, corpus 342 pass, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and steps each passing. Pass.

## Limits

- **Standup Ready count in the helper.**  The progress helper holds the count as a constant and takes no argument for it, so the Bindings rule's "a helper takes each binding as an argument" holds for the window (`--since`) and not for the count. The helper lives outside this repository; the example states the value once and links it.
