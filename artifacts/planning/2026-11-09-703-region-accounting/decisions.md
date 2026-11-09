# Decisions

## Confirmed

- The fault is fixed as hot-fix `[F09]` (#703) on the Python board at `priority: 10`, ahead of the work-planner prosiform adoption, which waits for its release (user, 2026-11-09).
- `contract/v0.24.0` and `python/v0.24.0` are cut after merge (user, 2026-11-09).

## Implementation Details

- Reproduction: a copy of work-planner with `prosiform: {}` added to each of its 59 documents. On `pf 0.23.0`, propose and revise compile; SKILL.md and the advance, align, deliver, hoist, plan, standup, sync and understand modes fail the no-accidental-expansion check, by 1 to 8 regions. With `--budget output-bytes=4000000`, the oversized entries fail the same way.
- Isolating the trigger to a minimal fixture is the first step.
- One pull request into `main`, opened as a draft and marked ready once review clears.

## Cause

- Command-block compaction decodes references and drops the wrapper, which can leave a line opening a block: a decoded `&gt;` redirect in `artifacts/pull-request.md` opens a quote. A compacted line that would open a block takes a backslash escape, and the compacted block is parsed once and refused unless it reads as one paragraph.
- Tag removal read a list marker on a later line as a container marker; later lines read only quote markers and indent.
- Work-planner bundle sizes on the fix (default budget 262144): propose 55711, revise 65375, understand 67588, hoist 152928, align 202047, sync 249529, advance 270596, standup 271195, plan 310476, deliver 383108, SKILL 462667.

## Review

- Fixed: the one-paragraph guard.
- Rejected, as no skill source writes them: a decoded table delimiter row or indent (now refused by the guard), indent before a literal `>`, multi-line reference titles in a block, and `&#92;` before punctuation.
