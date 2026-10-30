# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w17`, branch `i02/e00/w17-operations-applied-procedures-followed`. Commits: `f1789f38` (Apply), `a0ac8101` (Follow), `7c8d01a8` (guidelines), `f3c6b0e0` (merge of `i02/e00/main` at `f5038166`) and `4504e5b4` (fixtures and README).
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`. This row changes nothing under `src/`.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 250 fixture(s), 250 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `make conformance` | 288 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 37 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1059 passed | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

## Classification

Each link was classified by its target file and the target heading's `##` ancestor:

- An `artifacts/` heading under Operations is an operation (Apply).
- A heading under Commands is a command (Run).
- A `modes/` or `protocols/` file, or a heading under its Procedure, is a procedure (Follow).
- A mode's Operations section is a command spec (Run).

Every link classified. No target was missing or ambiguous.

## Apply (208)

From link verbs: 153 Run, 40 Call and 12 Follow. From plain or reworded references: plan-mode "call Populate Epic Issue Body" and "Run Report Review Finding", and deliver-mode "Each follows [Check Plan Change Autonomy]", which became "Apply [...] to each".

| File | Run | Call | Follow | Other |
| --- | --- | --- | --- | --- |
| artifacts/acceptance-criteria.md | 2 | | | |
| artifacts/board-delivery.md | 12 | | | |
| artifacts/board.md | 2 | | | |
| artifacts/delivery-branches.md | 1 | | | |
| artifacts/delivery-evidence.md | 4 | | | |
| artifacts/epic-issue-body.md | 1 | 3 | | |
| artifacts/epic.md | 2 | | | |
| artifacts/goal-trace.md | | 2 | 1 | |
| artifacts/initiative-issue-body.md | | 1 | 1 | |
| artifacts/issue-body.md | 3 | | | |
| artifacts/issue.md | 6 | | | |
| artifacts/placement.md | 7 | | | |
| artifacts/proposal-body.md | | 1 | | |
| artifacts/pull-request.md | 11 | 2 | | |
| artifacts/review-finding.md | | 1 | | |
| modes/advance-mode.md | 10 | 6 | | |
| modes/align-mode.md | 10 | 2 | 3 | |
| modes/deliver-mode.md | 21 | 3 | 2 | 1 |
| modes/hoist-mode.md | 4 | 1 | | |
| modes/plan-mode.md | 8 | 7 | 1 | 2 |
| modes/propose-mode.md | 2 | 3 | | |
| modes/standup-mode.md | 6 | 2 | | |
| modes/sync-mode.md | 19 | | 2 | |
| protocols/change-overview.md | 2 | 5 | | |
| protocols/epic-integration.md | 3 | 1 | 1 | |
| protocols/issue-closure.md | 7 | | | |
| protocols/issue-delivery.md | 4 | | | |
| protocols/review-pull-request.md | 3 | | | |
| protocols/task-merge.md | 3 | | 1 | |

sync-mode's Run count includes one Re-run, which became "Apply [Record Epic Delivery] again". Four "Apply [...] on" phrases now read "to".

## Follow (13)

| File | Run | Other |
| --- | --- | --- |
| modes/advance-mode.md | 1 | |
| modes/deliver-mode.md | 5 | 2 (agent and dispatched session "running" → "following") |
| modes/plan-mode.md | 2 | |
| modes/standup-mode.md | 1 | |
| modes/sync-mode.md | 1 | 1 (verb added to the Issue Closure step) |

## Left as Run

- Links to command specifications under `## Commands`, about 103 of them.
- revise-mode's Run Tests and Check Skill Files.
- Nouns: "the run", "a call" and "every run of a protocol".
- pull-request.md's "Call [Merge Pull Request]" links a command, so it became Run.

## Guidelines

| Rule | Before | After |
| --- | --- | --- |
| Procedure — Step verbs | — | A step applies an artifact operation and follows a mode, a protocol or a procedure subsection. It runs a command. |
| Modes — Orchestration | … call artifact operations with named inputs … | … apply artifact operations with named inputs … |
| Modes — Procedure | A step calls the body artifact's procedure rather than copying it. | A step applies the body artifact's operation rather than copying it. |
| Modes — Other modes | Invoke another mode with Run or Follow, naming the selected scope and the whole mode or exact subsection to execute. A subsection call executes that subsection only. | Follow another mode, naming the selected scope and the whole mode or exact subsection to follow. Following a subsection follows that subsection only. |
| Operations — One home | Artifact operations call their implementation commands by heading link. | Artifact operations run their implementation commands by heading link. |
| Protocols — Entered whole | A caller runs the file … A sequence worth calling on its own … | A caller follows the file … A sequence worth following on its own … |
| Protocols — No spare parts | A protocol nothing runs is not a protocol. | A protocol nothing follows is not a protocol. |
| Artifacts — Prose API | Modes call operation headings; operations call command headings. | Modes apply operations by heading link; operations run commands by heading link. |
| Artifacts — Operation scope | An operation exists because a procedure calls it. | An operation exists because a procedure applies it. |
| Artifacts — Command implementation | Operations holds the sequences that call them. | Operations holds the sequences that run them. |
| Artifacts — No spare parts | … the operation it would call. | … the operation it would apply. |
| Artifacts — Step rules | … a common procedure that callers invoke. | … a common operation that callers apply. |
| rules.md — Layers | a protocol runs artifact operations and other protocols; an artifact runs neither. | a protocol applies artifact operations and follows other protocols; an artifact does neither. |
| rules.md — Execution | … and is run whole. Run another mode, a protocol, or a named subsection only where the procedure calls it; | … and is followed whole. Follow another mode, a protocol or a named procedure subsection, and apply an artifact operation, only where the procedure calls for it; |
| example/guidelines.md — Commands | State a route as steps to call them. | State a route as steps that run them. |

## Bundles

Each mode was bundled with `pf -o <scratch>/<mode>.md modes/<mode>-mode.md` from `example/work-planner`, with default budgets, after the merge with `f5038166`.

| Mode | Exit | Bytes |
| --- | --- | --- |
| advance | 0 | 172,176 |
| align | 0 | 132,990 |
| deliver | 0 | 247,030 |
| hoist | 0 | 85,650 |
| plan | 0 | 207,650 |
| propose | 0 | 26,324 |
| revise | 0 | 6,767 |
| standup | 0 | 168,327 |
| sync | 0 | 158,133 |
| understand | 0 | 47,325 |

## Fixtures

- `a-procedure-and-everything-it-reaches` and `every-document-under-a-directory-merged` were re-recorded with `scripts/regenerate.py`. Only `expected/stdout.md` changed, and only in verbs. Their manifests are as written, and their descriptions still hold.
- `a-bare-fragment-and-its-referring-document`, `two-selected-sections` and `validation-without-publication` produce unchanged output. Their Record Epic Delivery step runs the Sync Epic command.
- `example/README.md`: both publish-step excerpts read "Apply [Ensure Repository Labels]". Each usage excerpt matches the source or the recorded bundle. The grouping excerpt "# Rules" is not from a usage fixture and this row leaves it as it is.
