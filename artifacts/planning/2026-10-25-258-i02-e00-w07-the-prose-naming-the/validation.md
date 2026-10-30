# Validation

> Delivery Record · Created 2026-10-25

## Environment

- Worktree: `.worktrees/i02-e00-w07`, branch `i02/e00/w07-the-prose-naming`, cut from `i02/e00/main` at `714c95c1`.
- Build: `.worktrees/i02-e00-w07/src/.venv/bin/pf`, from `cd src && uv sync --frozen`.
- Every command below ran from the directory the page names, and its exit status is recorded as the shell reported it.

## The instrument

| Check | Result | Exit |
| --- | --- | --- |
| `make links` | every reference in 101 document(s) resolved | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s) marked in the design, every one defined in `docs/glossary.md`, every definition carried across 24 source(s) | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `rg -l 'work-tracker' example/README.md invocation.md fixtures/README.md` | no path printed | 1 |
| `make check` | **not run**, as the brief directs | — |

`make links` is AC10's instrument and is the result AC10 is ticked on.

### The documented invocation of the instrument

The brief writes the instrument as `make links --online`. That command line exits `2`: GNU make reads `--online` as one of its own options and refuses it with `unrecognised option '--online'`. The target already passes `--online` to `checks/links.py`, so `make links` is the online run and is what was executed. Nothing in the repository needs to change for that; it is how the brief names the target that is wrong.

## The commands the two pages publish

Each ran from the directory the page names, with the build the venv holds.

| Page | Directory | Command | Exit |
| --- | --- | --- | --- |
| `example/README.md` | `example/work-planner` | `pf modes/plan-mode.md` | 0 |
| `example/README.md` | `example/work-planner` | `pf -f artifacts/epic-issue-body.md '#record-epic-delivery'` | 0 |
| `example/README.md` | `example/work-planner` | `pf modes/plan-mode.md` (the group example) | 0 |
| `example/README.md` | `example/my-skill` | `pf -o - procedure.md rules/common.md` | 0 |
| `invocation.md` | `example/work-planner` | `pf modes/plan-mode.md` | 0 |
| `invocation.md` | `example/work-planner` | `pf 'artifacts/epic.md#delivery-findings'` | 0 |
| `invocation.md` | `example/work-planner` | `pf -o context.md modes/plan-mode.md` | 0 |
| `invocation.md` | `example/work-planner` | `pf -c modes/plan-mode.md` | 0 |

`pf -c` published nothing, as its option text states: the run wrote no bundle and left the directory as it found it.

Each command emits one `W_ENTRY_DESTINATION` warning, which every cited manifest declares. The warning is a successful run's diagnostic, not a failure.

## The outputs, held to the fixtures

A block claiming to be a bundle was compared with the fixture byte for byte. Each run wrote its bundle to a scratch path outside the tree.

| Page command | Compared with | Result |
| --- | --- | --- |
| `pf modes/plan-mode.md` | `fixtures/usage-example/a-procedure-and-everything-it-reaches/expected/stdout.md` | identical, 203,906 bytes |
| `pf modes/plan-mode.md` | `fixtures/usage-example/every-document-under-a-directory-merged/expected/stdout.md` | identical, 203,906 bytes |
| `pf -f artifacts/epic-issue-body.md '#record-epic-delivery'` | `fixtures/usage-example/a-bare-fragment-and-its-referring-document/expected/stdout.md` | identical, 11,866 bytes |
| two section references | `fixtures/usage-example/two-selected-sections/expected/stdout.md` | identical, 11,911 bytes |
| `pf -c` | `fixtures/usage-example/validation-without-publication/expected/stdout.md` | identical, 0 bytes |

The two procedure fixtures hold the same bytes because both invoke `modes/plan-mode.md`, and one entry produces one bundle.

## The excerpts replaced

`example/README.md` calls its blocks exact excerpts. Each was re-read from the source its prose names, and a check script held every quoted block to that file as a literal run of its text. All nine blocks were runs of the file they name.

| Was quoted | Claimed source | Replaced with | Why |
| --- | --- | --- | --- |
| A `## Prerequisites` section linking `Epic Issue Body` and `Epic` | `modes/plan-mode.md`, an exact excerpt | Step 6 of `## Procedure`, the publish step, in `modes/plan-mode.md` | No `## Prerequisites` heading exists in either tree. `example/work-tracker/modes/plan-mode.md` carries `# Plan Mode`, `## Procedure`, `## Outcomes`; `example/work-planner/modes/plan-mode.md` carries `# Plan Mode`, `## Procedure`, `## Outcomes`. The publish step is the step that demonstrates the same point: a link to a document inside the root, a second link to a document inside the root, and a deferred link to `guidelines.md`. |
| The deferred-link sentence: `The caller reached this mode through the routing document [¬ SKILL.md](SKILL.md)` | `modes/plan-mode.md` | The publish step's `[¬ Interview](guidelines.md#modes)` link, quoted inside the same block | The deferral the new tree states is the guidance link, not the routing document. The mode does not name `SKILL.md` at all. |
| The bundle's planning procedure, with a `## Prerequisites` heading and its two rewritten prerequisite links | `a-procedure-and-everything-it-reaches/expected/stdout.md` | The bundle's publish step, as the fixture now holds it | The bundle leads with `Follow [Procedure](#procedure)`. The publish step's two internal links became fragments and its deferred link published as `guidelines.md#modes` with the `¬` marker and the space after it removed. |
| The `*Record* Epic Delivery` operation, verbatim | `artifacts/epic-issue-body.md`, under `## Operations` | Unchanged in the Input block, byte for byte | The operation exists and its bytes still hold. The claim was true; only the output block was stale. |
| The bare-fragment bundle's `# Artifacts` / `## Operations` preamble copy of the operation | `a-bare-fragment-and-its-referring-document/expected/stdout.md` | `## Operations` as the fixture now holds it, with the operation beneath it quoted once | The fixture carries no `# Artifacts` heading: the artifacts group suppresses its own heading with `group-heading: false`, so the operation sits under `## Operations`. The operation's `[Delivery Findings](artifacts/epic.md#delivery-findings)` link now publishes as `#delivery-findings`. |
| Both artifact files' `prosiform` declaration, showing `group: artifacts` and `group-depth: 2` | `artifacts/…` frontmatter | The same declaration with `group-heading: false`, as `artifacts/epic.md` now carries it | The declaration gained a key. A block presented as exact that omits one key of the block it quotes is stale. |
| An `# Artifacts` group heading, then `## Overview` with `### Epic Issue Body` and `### Epic` member headings | `every-document-under-a-directory-merged/expected/stdout.md` | `## Overview` with `### Planning Record`, then `## Operations` with `### Acceptance Criteria` | The fixture now merges the artifacts into `## Overview` and `## Operations` with no `# Artifacts` heading, and its only above-depth prose member is `Planning Record`. |
| The my-skill grouped portion, with `[¬ Codex]` and `[¬ Claude]` deferred links | the my-skill bundle | The same portion as `pf -o - procedure.md rules/common.md` emits, with `[Codex](rules/codex.md)` and `[Claude](rules/claude.md)` | The emitted bundle drops the marker and publishes the working-directory-relative path. The quoted block showed the source's spelling rather than the bundle's. |
| `cd example/work-tracker` before each of three commands | — | `cd example/work-planner` | The tree the corpus sources. |

### What the prose around the blocks now says

- The page's opening paragraph names `work-planner`, its ten modes, six protocols and thirty artifact documents, and the fixture family that sources it.
- The first example's prose states that the publish step links two documents inside the root and defers a third, which is what the quoted block shows.
- The group section states that `group-heading: false` omits the group's own heading and that only a member reached as a whole document contributes prose above the grouping depth, which is why `Overview` holds `Planning Record` alone.
- The closing statement names `work-planner` as the source tree, and the fixture table keeps its five rows against the re-recorded bundles.

## `fixtures/README.md`

Verified and left unchanged. It carries `work-planner` once, at the sentence naming the target the family's `source` links reach, and no occurrence of `work-tracker`. W06's correction stands.

## No document under the example or the corpus was edited

`git diff --stat` on the two commits touches `example/README.md` and `invocation.md` and nothing else. `example/work-planner`, `example/work-tracker` and `fixtures/` are untouched, so this row's claim is prose about the tree rather than a change to it.

## Findings

- **The tree needed nothing to make the commands run.** All eight exit `0` from the directories the pages name. A tree that has to be edited for its own documentation to work would have been a blocker.
- **`example/work-tracker` is still reachable and still bundles.** It is the four-file tree the migration replaced, retained deliberately. Nothing this row publishes names it.
- **Two other places still name it.** `README.md`'s `## Usage` and `src/tests/test_handoff_round_trip.py` both bundle `example/work-tracker`. Neither is in AC10's three documents, so neither is this row's to change. Both are deferred to [#263](https://github.com/m2ux/prosiform/issues/263), with the commands' own exit statuses measured:

| Location | Command | Exit with `work-planner` |
| --- | --- | --- |
| `README.md` `## Usage` | `pf example/work-planner/modes/plan-mode.md` | 0 |
| `README.md` `## Usage` | `pf 'example/work-planner/artifacts/epic.md#delivery-findings'` | 0 |

  Both current `work-tracker` forms also exit `0`, so no reader hits a failure today: the cost is that the repository's own front page demonstrates the tree the epic replaced while its corpus sources the one it delivered. The round-trip suite is the sharper case, because `src/tests/test_handoff_round_trip.py` copies `example/work-tracker` and asserts that the destinations its bundle publishes compile. A green suite therefore holds the superseded tree to the handoff, which is the defect W06 fixed in the fixtures and this row fixed in the prose, still standing in the build's own suite.

## Debt deferred

| Item | Where it is recorded | Why deferred |
| --- | --- | --- |
| `README.md`'s two `## Usage` commands bundle `example/work-tracker` | [#263](https://github.com/m2ux/prosiform/issues/263) W06, AC6 | Outside AC10's three documents; a five-line change with its own check |
| `src/tests/test_handoff_round_trip.py` copies `example/work-tracker` | [#263](https://github.com/m2ux/prosiform/issues/263) W07, AC7 | A test change rather than prose, and the suite would need its dispatch fixture carried over from a tree that declares one |

Nothing trivial was left unapplied: the two files this row names are complete.
