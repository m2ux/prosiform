## Overview

Every scenario of the diagram-following eval is a real-use scenario: a session starts from a skill placed where its agent CLI discovers skills, and opens with its task in plain words. The CLI's own skill mechanism, name and description up front, `SKILL.md` on use and linked material on demand, is the only disclosure the agent works under. One workflow is a skill of real size, measured compiled against plain. The goal the reviews test against: no session starts from a prompt naming an entry file, the committed baseline measures agents meeting a workflow as real use meets it, and a committed record shows what compiling adds to a skill no session reads whole.

## Problem

Each session starts from a prompt the eval writes, naming the file to read, which no real use of a skill does.

- **The prompt names the entry file.**
  A bundled or tree session is told "[ENTRY describes a workflow](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/instruction.md#L6-L7)", and a compiled one is [handed its bundle](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/instruction-compiled.md#L10-L13) the same way.
- **The skill session is told a skill exists.**
  The one form that starts from a skill [opens by telling the agent to find it](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/instruction-bootstrap.md#L9-L14), so discovery is never measured.
- **Two harnesses switch skills off.**
  The Claude harness [disables slash commands](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/harness.py#L325-L333), skills among them, and the Codex bridge [turns off skill discovery](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/codex_agent.py#L27-L30).
- **The records measure the bare prompt.**
  The [committed baseline](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/README.md#L367), the feature proof and the agent-pick run were all taken from bare prompts; the [agent-pick run](https://github.com/m2ux/prosiform/pull/732) passed no session of twenty although every pick was right.
- **No workflow is the size of a real skill.**
  [`branching`'s diagram form](https://github.com/m2ux/prosiform/tree/8c611259ab407e09e4d50262b79cf2f8eef14a5d/evals/diagram-following/workflows/branching/diagram) is nine files, and the [committed baseline](https://github.com/m2ux/prosiform/blob/8c611259ab407e09e4d50262b79cf2f8eef14a5d/evals/diagram-following/report.md#L16-L25) passes every `bundle`, `tree`, `prose` and `linked` session alike.

## Proposal

- **A session starts from a skill.**
  Each harness places the session's skill under the root its CLI discovers, and the CLI offers it as it offers any skill.
- **The opening prompt is the task.**
  A scenario states its task in plain words from its inputs; the CLI picks the skill from its description, so discovery is part of what is measured.
- **The comparisons become skill variants.**
  The product variant's skill links sources for `pf` to compile; each control is the same workflow as a plain-Markdown skill, as skills are written without prosiform.
- **Only CLIs that discover skills run.**
  A harness stays where its CLI discovers skills natively and leaves the eval otherwise.
- **One real-use baseline replaces the bare-prompt records.**
  The bare-prompt records and their sections leave the eval, and a shaken-down run on the skill-entry eval becomes the baseline.
- **Agent-pick is measured on its own.**
  A dedicated agent-pick run on the skill-entry eval measures whether an agent at a `?` pick keeps to what `pf` prints.
- **One skill of real size is measured.**
  Work Planner runs compiled and plain on captured requests, scored on the context each request requires, with tokens and reads compared in a run of its own.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/735) | Skill Entry | AC1, AC2 | | |
| [E01](https://github.com/m2ux/prosiform/issues/736) | Skill Variants | AC1, AC2, AC3 | | |
| [E02](https://github.com/m2ux/prosiform/issues/737) | Real-Use Baseline | AC4, AC5, AC6 | [E01](https://github.com/m2ux/prosiform/issues/736) | |
| E03 | Field Scale | AC7 | [I16:E07](https://github.com/m2ux/prosiform-skills/issues/9) | |

## Acceptance Criteria

- [ ] **AC1.** Every session of every workflow starts from that workflow's skill, placed where its agent CLI discovers skills, as the harness and corpus tests show.
- [ ] **AC2.** Every session opens with its scenario's task in plain words and carries no instruction of the eval's on finding or reading a skill, as the run and harness isolation tests show.
- [ ] **AC3.** Every comparison the eval draws is between skill variants of one workflow, a product variant whose sources `pf` compiles against plain-Markdown controls, as the corpus test shows.
- [ ] **AC4.** The eval's committed records and their documentation hold no run of a session started from a bare prompt, as the README and runbook tests show.
- [ ] **AC5.** The committed baseline is a run of every workflow of the skill-entry eval with every failing session triaged under the runbook, none a defect or unclear, as the baseline record and its report show.
- [ ] **AC6.** An agent reaching a `?` pick through a skill resolves it from what the bundle and `pf` print without reading a source, in every session of the agent-pick run on the skill-entry eval, as its run record shows.
- [ ] **AC7.** The committed records hold a run of one skill of real size as a compiled variant and as a plain-Markdown control, comparing the required context each session read, its tokens and its reads, as the field-scale record and its report show.

## Non-Goals

- It writes no disclosure strategy: no file, instruction or system prompt states how an agent reads a skill.
- It forbids no read of a source in any prompt or skill; the `read_source` check measures what an agent does unprompted.
- It takes no live measurement of composition edges from a bare prompt.
- It names no model or harness for the baseline run; the runbook records the user's choice at run time.
- It changes no `pf` behaviour.
- It converts no skill to prosiform; the field-scale variants are revisions the skill's own repository holds.
- It grades no output a field-scale session produces.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-real-use-eval) — the confirmed goal, decisions, goal trace and work items.
- **R2.** **Source.** [Decisions](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/decisions.md) — the user's decisions on skill entry, the opening prompt, variants, harnesses and records that the criteria answer to.
- **R3.** [Agent-pick run record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-709-i15-e01-w06-a-measured-agent-pick) — the bare-prompt run whose sessions opened sources beside the bundle, which motivates starting from a skill.
- **R4.** [Preset Alternatives decisions](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-preset-alternatives/decisions.md) — the remeasuring of agent-pick that waits on this eval's real-use baseline.
- **R5.** [Use Through Prosiform](https://github.com/m2ux/prosiform-skills/issues/9) — the Work Planner cutover that supplies the compiled revision and fixes the plain one.
- **R6.** [Reading-route harness](https://github.com/m2ux/workflow-server/pull/1695) — the captured requests and context contracts the field-scale sessions are scored against.



