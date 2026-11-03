# Change List — I10:E04 W18

The plan changes this delivery session made under its allowance, and those it held.

## Applied

- **Folded work** — `subagent-first-run` states each sub-agent's `pf` run with `by`, and the corpus test holds a section's stated runs to the lines its sub-agents compile. Reading each start's commands makes an unstated sub-agent run `overcompiled`, so the nested scenario could not pass without it.
- **Folded work** — four runner tests count the default matrix over the default forms rather than every form, which diverged once Claude ran `staged`.
- **Folded work** — `run.json` records each form's command line as `commands`, since a staged Claude session's differs from the others'.

## Held

- **Design decision, W18** — the staged session's shell is approved for `pf` alone (`--allowedTools Bash(pf:*)`). `acceptEdits` approves no command and a headless session cannot be asked, so some approval is needed. Recommended: keep it; it confines the shell to compiling, which keeps the isolation the README states. The alternative, approving every command, lets a session reach past its workspace.
- **Design decision, W18** — `first-hop-run` now states the ledger's run, so under AC22 Cursor and opencode no longer get it; Claude measures it on its start, run and action. Recommended: keep it; the scenario states its runs in one place. The alternative is for a harness that reports no sub-agent calls to record each start's commands as unknown and be scored on actions alone, which would revise AC22.
- **Overlap, I10:E00 W04 ([#632](https://github.com/m2ux/prosiform/issues/632))** — this base's `Claude` still reads only `Task` starts. This unit reads shell calls by `parent_tool_use_id` and leaves the start tool name alone, so the two changes meet at integration with no conflict in meaning. The stub agent prints `Task`.
- **Live check for W16** — no paid session ran. W16's shakedown confirms in one live staged Claude session that `Bash(pf:*)` approval reaches `Task` sub-agents and that their `Bash` calls carry `parent_tool_use_id`.
