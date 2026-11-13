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
9. **The tracing duty lives in the skill.** One paragraph shared by every variant's `SKILL.md` states how a session records `trace.log`, names a sub-agent's trace and reads `answers.txt`; the prompt stays the task in plain words. Set aside: appending the duty to the prompt; the scorer inferring the path from the transcript.
10. **The bare-prompt path retires last.** Its retirement is E01's last row, depending on every family row, so the eval stays runnable throughout. Set aside: retiring it in E00, leaving only the bootstrap pair runnable while the families convert.
11. **The bootstrap family takes no E01 row**, the deferral family is four workflows, no composition-edges record exists to delete, and the Claude harness admits skills by dropping `--disable-slash-commands`, adding its skill tool and refusing a configuration directory holding skills. Each as recommended.
12. **I14 is superseded.** I14 (#660) and its open epics close as not planned once I16 is published, each with a comment linking I16. Set aside: re-scoping I14 onto the skill-entry eval.
13. **The #733 edge names a row.** I15's agent-pick run row depends on `[I16:E02:W03]`, the shakedown whose recorded caps it consumes. Set aside: `[I16:E02:W04]`, the baseline run.
14. **The baseline covers every workflow.** Every harness gives a shell, so `EDGE_WORKFLOWS` leaves in E02 W01 and the default matrix holds every workflow. Set aside: keeping the split and measuring the baseline workflows alone.
15. **I16 is unranked.** The initiative and its epics are published with no priority label and placed at Backlog on the Python board; unranked by the user's choice, 2026-11-12. Set aside: the proposed priority map E00 3, E01 2, E02 1.

Settled by the user at alignment, 2026-11-13, each as recommended.

16. **Every composition workflow has a criterion.** E01 AC4 names `conditional-composition`, `directive-labels`, `dispatch-depth` and `subagent-first-run`, the four E01 W04 converts. Set aside: a separate criterion for the first two; moving them to another family.
17. **The tracing paragraph is a criterion.** E00 AC5 holds every skill text in the corpus to its workflow's shared tracing paragraph, delivered by E00 W03; the corpus test binds each family as it converts. Set aside: a work-item detail with no criterion.
18. **E00 AC1 binds the harnesses kept.** Each harness the eval keeps drives a CLI documenting native skill discovery, cited in the harness. Set aside: the wording that also reads as every such CLI becoming a harness.
19. **The runbook section and its shakedown are separate rows.** E02 W02 writes the section and its cap rule (AC4), design work; E02 W03 runs the shakedown under the runbook (AC2); E02 W04 is the baseline run (AC3). Set aside: one row recorded as a run row.
20. **Initiative AC5 names every workflow.** AC4 and AC5 stay as the goal's whole-initiative criteria, and AC5 states decision 14's every workflow. Set aside: keeping AC5 unchanged.
21. **The baseline waits on the first-run scorer.** E02 W04 depends on `[I15:E02:W00]` (#733), so the baseline is never scored before the scorer accepts a first-run `--pick`.

## Planning

Taken in Plan mode, 2026-11-12; each can be reopened.

- **The initiative takes I16**, I15 being the highest of any state.
- **No lanes.** Every row extends the runner, the corpus test or the README, so rows land one at a time on each epic's base.
- **Thirteen rows and fifteen criteria.** E00 three rows and five criteria, E01 six and six, E02 four and four.

## Joins

Each line names a candidate unit the dependency check prints and why its rows stay split.

- E00:W01 and E00:W02 stay split: retiring or keeping Codex is decided from its documentation before placement is built on the harnesses that remain.
- E00:W01, E00:W02 and E00:W03 stay split: they share the runner and README but each states one rule with its own tests.
- E00:W02 and E00:W03 stay split: placement is proven on the bootstrap pair before their prompts change.
- E01:W01, E01:W02, E01:W03, E01:W04, E01:W05 and E01:W06 stay split: each converts one family with its own corpus fixtures, the retirement lands only once every family runs as skills, and one pull request for all of it is too large to review.
- E01:W01 and E01:W06 stay split: the retirement removes the forms the diagram family converts from, so it waits on the conversion.
- E02:W01, E02:W02, E02:W03 and E02:W04 stay split: the deletion and the section are design work, the shakedown and the baseline are paid runs under the runbook, and each run starts only on what the row before it committed.

## Dependency Check

- **Problems.** None.
- **Epic priority.** The check proposes E00 3, E01 2, E02 1; none is applied, by decision 15.
- **Contention.** Every cross-epic pair shares the README, and E00's placement and prompt rows share `workflow.py` and `test_workflow.py` with E01's rows; the whole-epic edges order them.
- **Longest chains.** Five of nine steps, each from E00 W01 through an E01 family row, E01 W06 and E02 W01 to E02 W04.

## Defaults Taken

Details settled without a question and confirmed by the user, 2026-11-12.

- **Variant layout.** A variant is a `SKILL.md` text at `workflows/<workflow>/skills/<variant>.md` and a material tree; the runner places the text as `SKILL.md` and copies the tree under `sources/`. The bootstrap pair's `skill/SKILL.md` becomes `skills/compiled.md` and `skill/sources/` becomes `compiled/`.
- **Variant names.** The product variant is `compiled`; `bundle` and `bootstrap` retire into it. The controls keep `tree`, `prose`, `linked` and `authored`. `--forms` becomes `--variants`.
- **The product variant's material.** `compiled/` where a workflow has it, else `diagram/`.
- **`prose` is read unbundled.** As a plain-Markdown skill it is the prose tree as written, so against the product it isolates the diagram and compilation together.
- **One name and description per workflow.** Every variant of a workflow shares them, so a difference in pass rate is the material, not discovery.
- **The task.** A top-level `task` in `scenarios.toml`, with `{<input file>}` placeholders filled from the scenario's inputs; the inputs stay files, since the workflow's conditions read them.
- **A workflow with skill texts runs as skills.** Until E01 W06, a workflow without them keeps its forms and instruction.

## Open Questions

None.
