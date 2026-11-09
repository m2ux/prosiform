# Decisions

## Confirmed

- The fault is fixed as hot-fix `[F09]` (#703) on the Python board at `priority: 10`, ahead of the work-planner prosiform adoption, which waits for its release (user, 2026-11-09).
- `contract/v0.24.0` and `python/v0.24.0` are cut after merge (user, 2026-11-09).

## Implementation Details

- Reproduction: a copy of work-planner with `prosiform: {}` added to each of its 59 documents. On `pf 0.23.0`, propose and revise compile; SKILL.md and the advance, align, deliver, hoist, plan, standup, sync and understand modes fail the no-accidental-expansion check, by 1 to 8 regions. With `--budget output-bytes=4000000`, the oversized entries fail the same way.
- Isolating the trigger to a minimal fixture is the first step.
- One pull request into `main`, opened as a draft and marked ready once review clears.
