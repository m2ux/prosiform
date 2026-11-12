# Decisions

## Confirmed

Settled in the design interview (user, 2026-11-12). Each names the options set aside.

1. **A pick reaches its target alone.** The picked alternative's `subst` routes the target's links to that kind's material. Set aside: forwarding a pick to linked documents through a title tag; applying it to every document of the run.
2. **The marker is a `?` title tag on a deferred link.** Set aside: a new operator mark in the link text.
3. **The target declares its alternatives** with `choice: <when to pick it>`, and exactly one is in force wherever it compiles. Set aside: offering every named preset; listing the alternatives in each link's title.
4. **The listing is pf's answer to `?`**: exit 2, each alternative with its choice line, and the same answer for a missing or wrong pick. Set aside: a listing flag; writing the list into the published link.
5. **`?` is accepted on deferred links only** (`¬`, `¬↳`). Set aside: compiling every alternative of a dispatch up front; publishing a dispatch for the agent to compile and hand on.
6. **An alternative's `subst` pairs route quietly**: no `W_SUBST_USED`, and `W_SUBST_UNUSED` only for a pair no link of its document names. Set aside: relaxing both warnings for every pair; keeping them.
7. **Delivery is a new initiative** planned through work-planner. Set aside: one hot-fix pull request; a record with nothing raised.
8. **work-kind is the motivating case.** work-planner is pre-migration, so a fixture shaped like a kind router proves the pattern.
9. **The exactly-one failure has its own code**, `E_ALTERNATIVE_UNRESOLVED`, with exit 2, so a harness matches the pick step by code. Set aside: reusing `E_INVALID_USAGE`, as group and `subst` conflicts do.
10. **A misplaced `?` and a failed deferral pick check refuse with `E_UNSUPPORTED_CONSTRUCT`** and exit 1, as the operator refusals do, since the defect is in the source the run read. Taken as a default in W00 and confirmed in Deliver (user, 2026-11-12). Set aside: a dedicated pick code.

## Delivery

Settled in Deliver mode (user, 2026-11-12).

- **I15 delivers alone.** I12 moves to Backlog with its priority labels removed, so no Advance re-places it. Set aside: I12 alongside I15.
- **An agent proves the pick end to end.** E01 gains W05, an agent-pick workflow in the diagram-following eval's `compiled` form, and W06, its live run under `RUNBOOK.md` with the model the user chooses; initiative AC4 cites the eval. Set aside: a design row alone; fixtures and the bare-command test alone.
- **`read_source` binds every compiled form.** A `compiled` or `bootstrap` session that opens a source document fails, in every workflow; the next rerun of an existing cell records the rule as the cause of any drop. Set aside: agent-pick alone; re-baselining the affected cells in W06.
- **Agent-pick inputs restate their choice lines.** Each scenario's input holds its alternative's choice line verbatim, so a failure points at the pick procedure rather than at interpretation. Set aside: paraphrased inputs; both sets.
- **The agent-pick run follows the baseline's setup.** W06 runs on the harness and model the runbook records for the baseline, five repetitions of the four `compiled` scenarios, its caps set by a one-repetition shakedown. Set aside: another model or harness; both; a ten-repetition run; the baseline's caps without a shakedown.
- **The compiled instruction names no sources.** It says only that each `pf` command runs from the session's directory, and forbids nothing, so `read_source` measures whether an agent keeps to what it was given unprompted. W06's shakedown found the instruction pointing agents at the sources the rule fails them for opening. Set aside: a prohibition beside the line; keeping the line with a prohibition.
- **The agent-pick run has its own record.** It commits `agent-pick.json` and `agent-pick.md`, as an edge run does, and `baseline.json` is untouched; AC8 names that record. Set aside: adding the workflow's cells to `baseline.json`.
- **Keeping agents to what `pf` gives them is I15's.** The agent-pick run (#732) passed no session of twenty although every pick was right: fifteen opened source files and five ran `pf` on references no step states. I15 gains an epic for it, measured by rerunning agent-pick, and closes only once agents keep to the bundle. Set aside: a new initiative; the run record alone.
- **E01 depends on E00.** E01's `?` builds on E00's alternatives, which reach main only when E00's review pull requests merge, so E01 starts from main after them. Set aside: cutting E01's bases from E00's; holding E01 without a plan edit.

## Planning

Settled in Plan mode (user, 2026-11-12).

- **I15 takes the next initiative number**, `I14` being the highest of any state.
- **Two layered epics.** E00 Declared Alternatives leaves main working with author picks; E01 Agent Pick adds `?` on it. Set aside: one epic.
- **No lanes.** Every row extends `cli.py`, `closure.py` or the same pages, so rows run one at a time.
- E00:W02 and E00:W03 stay split: each states one rule with its own fixtures, and the second rebases on the first on the epic base.
- **E01 W01 and W02 are joined** into one pull request for the `?` link grammar, dropping the edge between them.
- **E00 W00 states the whole design**, the agent's pick included, so each epic's documentation pins one design commit.
- **I15 runs first on the Python board.** Advance (user, 2026-11-12) gives I15 priority 2, In Progress with E00 Ready, and I12 priority 1, Ready, so I12's polymorphism pages follow the alternatives they cite. I01 and I14 stay unranked. Set aside: I15 with I14 in parallel; I15 alone; I01 first.
- **No ordering edge with the symbol-grammar hot-fix.** Whichever lands second absorbs the other; E01 W03 is re-planned only if the hot-fix lands first. Set aside: landing the hot-fix first; folding it into E01.

## Dependency Check

- **Epic priority.** E00 takes 2 and E01 takes 1: no whole-epic edge separates them, and their rows contend.
- **Contending pairs.** E00 W02 and E01 W03, and E00 W03 and E01 W03, extend `cli.py`; E00 W04 and E01 W04 extend `invocation.md` and `docs/glossary.md`.
- **Longest chains.** Five of five steps, each from E00 W00 through E00 W01 to E01 W04.

## Context

- **work-kind moved during planning.** Commit `93a2ce585` on workflow-server moved the single-implementer operations to their callers, leaving Populate Body and Validate Body; the design's examples use Populate Body.
- **The pattern catalogue overlaps.** The design-patterns initiative's polymorphism family states call-site dispatch, where the author picks; once alternatives land, its pages can cite them. That initiative is on this board, so the initiative body records the overlap as a Non-Goal rather than a reference.

## Defaults Taken

Details settled without a question; each can be reopened.

- `choice` holds a non-empty one-line string, and a `choice` in `default` is refused.
- A preset named `?` is refused.
- Exactly one alternative is counted on the union of presets every reference reaching the document selects in one bundle.
- `?` selects no preset, in a title or in `--presets`; the listing is the exactly-one failure.
- The run publishing a deferral refuses a link to alternatives that names none, names two, or names one beside `?`, since the later run would fail.
- A diagram link selects no preset, so a document with alternatives reached through diagram links alone fails the exactly-one rule.

## Open Questions

None.
