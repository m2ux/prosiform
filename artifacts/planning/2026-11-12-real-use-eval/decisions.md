# Decisions

## Goal

Confirmed by the user, 2026-11-12: every diagram-following eval scenario is a real-use scenario. A session starts from a skill placed where the agent's CLI discovers skills, and opens with the task in plain words. The CLI's own skill mechanism, name and description up front, `SKILL.md` on use and linked material on demand, is the disclosure the agent works under; the eval adds nothing to it. A bare prompt naming an entry file is not an eval.

## Confirmed

Settled by the user, 2026-11-12. Each names the options set aside.

1. **Skill entry.** Each session's workflow is a skill in the CLI's discovery root: `.claude/skills/<name>/` for `claude` and `cursor`, `.opencode/skills/<name>/` for `opencode`, as the `bootstrap` form already places one. Set aside: a disclosure strategy of any kind, since disclosure is the CLI's own behaviour and no strategy file, instruction or system prompt is planned.
2. **Opening prompt.** The task in plain words, built from the scenario's inputs; the CLI chooses the skill from its description, so discovery is part of what is measured. Set aside: naming the skill; both styles as forms.
3. **Forms become skill variants.** The comparisons stay, each behind a skill: the product variant's skill links sources for `pf` to compile; the controls are plain-Markdown skills of the same workflow (`tree`, `prose`, `linked`, `authored`), as skills are written without prosiform. Set aside: the product alone; the product and one plain control.
4. **Harnesses.** Each CLI with native skill discovery stays: `opencode`, `claude`, `cursor`. Codex stays only if its CLI discovers skills natively, established from its documentation in analysis; otherwise it is retired. Set aside: all four through the bridge; `opencode` alone.
5. **Records.** Every bare-prompt record (`baseline.json`, `report.md`, `mvp-proof.json` and `.md`, the composition-edges records, `agent-pick.json` and `.md`) is deleted with its README and runbook sections, and one new baseline is measured on the skill-entry eval as the initiative's last epic; the harness and model are the user's choice at run time. Set aside: keeping them as history; deleting without a new run.
6. **Shape.** Three epics, each depending on the one before: Skill Entry, Skill Variants, Real-Use Baseline, about 13 rows and 12 to 15 criteria.
7. **Downstream.** The agent-pick remeasurement (#733 W00) depends on this initiative's Real-Use Baseline epic.
8. **Standing rules.** `read_source` stays: sources sit where the skill keeps them, an agent that strays into them fails, and no instruction names or forbids them. Fixtures and tests one per distinct rule. Eval design rows are design work; run rows follow `RUNBOOK.md` and name no model.

## Planning

Taken in Plan mode, 2026-11-12, by this session; each can be reopened.

- **The initiative takes I16**, I15 being the highest of any state.
- **No lanes.** Every row extends the runner, the corpus test or the README, so rows land one at a time on each epic's base.
- **E00 W03 and E00 W04 are joined.** The plain-words prompt replaces the instruction files, so one pull request makes the swap.
- **Twelve rows and thirteen criteria.** E00 four rows and five criteria, E01 five and five, E02 three and three.

## Joins

Each line names a candidate unit the dependency check prints and why its rows stay split.

- E00:W01 and E00:W02 stay split: retiring or keeping Codex is decided from its documentation before placement is built on the harnesses that remain.
- E00:W01, E00:W02, E00:W03 and E00:W04 stay split: they share the runner and README but each states one rule with its own tests, and together they exceed one pull request's worth.
- E00:W02 and E00:W03 stay split: placement is proven on the bootstrap pair before their prompts change.
- E00:W02, E00:W03 and E00:W04 stay split: the joined prompt and retirement pull request rebases on placement.
- E01:W01, E01:W02, E01:W03, E01:W04 and E01:W05 stay split: each converts one family with its own corpus fixtures, and one pull request for all twenty-three workflows is too large to review.
- E02:W01 and E02:W02 stay split: the deletion is design work and the shakedown a paid run under the runbook.
- E02:W01, E02:W02 and E02:W03 stay split: the deletion, the shakedown and the run each commit on their own, and the run starts only on caps the shakedown recorded.

## Dependency Check

- **Problems.** None.
- **Epic priority.** E00 takes 3, E01 2, E02 1: each epic waits on the one before through whole-epic edges.
- **Contention.** Every cross-epic pair shares the README, and E00's placement, prompt and retirement rows share `workflow.py` and `test_workflow.py` with E01's rows; the priority numbers separate them.
- **Longest chains.** Ten of seven steps, each through E00 W01, E00 W02, E02 W01, E02 W02 and E02 W03.

## Findings for the User

Put to the user before publication, one at a time.

1. **E00 cannot retire the bare-prompt path and leave the other families running.** Retiring the instructions and entry wiring in E00 leaves every family not yet a skill without a prompt. Recommended: E00 leaves the bootstrap pair as the eval's only runnable workflows, and each E01 row brings a family back as skills. Alternative: move the retirement row to the end of E01.
2. **The bootstrap family needs no E01 row.** Its two workflows are already product-variant skills with no controls; E00 W02 moves them to the variant layout as its end-to-end proof. E01 drops to five rows. Recommended: as drafted.
3. **The deferral family is four workflows.** The README's "four deferral workflows" already include `agent-pick`; the family is `deferred-composition`, `deferred-dispatch`, `agent-pick` and `preset-deferral`. Recommended: as drafted.
4. **No composition-edges record exists.** `composition-edges-<harness>.json` is planned by the runbook's Edge Run section but was never committed; only that section and the `EDGE_WORKFLOWS` split leave. Recommended: as drafted.
5. **The Claude harness disables skills today.** `--disable-slash-commands` and a `--tools` list without the skill tool keep a placed skill from being offered; E00 W02 drops the switch, admits the tool, and refuses a configuration directory holding skills. Recommended: as drafted.
6. **I14 overlaps.** I14, Evaluation Refinement, plans committed bare-prompt edge records and a baseline over the old matrix; this initiative deletes that kind of record and replaces the baseline. Recommended: close I14 as not planned once I16 is published, linking I16 as the issue that takes its work. Alternative: re-scope I14 to the skill-entry eval after I16.
7. **The #733 edge names a row.** I15 E02 W00 consumes the agent-pick skill variant and the real-use runbook; the row producing the last of those is E02 W02, while the baseline run, E02 W03, produces nothing it reads. Recommended: W00 depends on `[I16:E02:W02]`. Alternative: `[I16:E02:W03]`, as the decision states. Its current cell names an epic, `[E01]`, which the row rules refuse; the edit replaces it.
8. **The baseline's matrix.** The default matrix runs the baseline workflows and leaves the edge workflows to an edge run this initiative deletes. With every harness carrying a shell, recommended: the real-use baseline covers every workflow and `EDGE_WORKFLOWS` leaves in E02 W01. Alternative: keep the split and measure the baseline workflows alone.

## Defaults Taken

Details settled without a question; each can be reopened.

- **Variant layout.** A variant is a `SKILL.md` text at `workflows/<workflow>/skills/<variant>.md` and a material tree; the runner places the text as `SKILL.md` and copies the tree under `sources/`. The bootstrap pair's `skill/SKILL.md` becomes `skills/compiled.md` and `skill/sources/` becomes `compiled/`.
- **Variant names.** The product variant is `compiled`; `bundle` and `bootstrap` retire into it. The controls keep `tree`, `prose`, `linked` and `authored`. `--forms` becomes `--variants`.
- **The product variant's material.** `compiled/` where a workflow has it, else `diagram/`.
- **`prose` is read unbundled.** As a plain-Markdown skill it is the prose tree as written, so against the product it isolates the diagram and compilation together.
- **One name and description per workflow.** Every variant of a workflow shares them, so a difference in pass rate is the material, not discovery.
- **The task.** A top-level `task` in `scenarios.toml`, with `{<input file>}` placeholders filled from the scenario's inputs; the inputs stay files, since the workflow's conditions read them.
- **The Claude harness's isolation.** Its preflight refuses a configuration directory holding `skills/`, so the eval's own configuration offers no skill.

## Open Questions

- **Where the tracing duty lives.** `trace.log`, the sub-agent trace names and `answers.txt` are measurement the instruction states today, and the plain-words prompt carries none of it. Recommended: one paragraph shared by every variant's `SKILL.md`, read under the CLI's own disclosure. Alternatives: the opening prompt carries it after the task; the scorer reads the path from the transcript's action writes, with no trace file.
