# Change List — I05:E06 W10

> Delivery record · Created 2026-10-29

## Applied

| Change | Kind | Where |
| --- | --- | --- |
| `make check` runs `authoring` after `steps`, so a change that breaks an authoring rule fails the repository's checks | Check wiring | `Makefile` |
| The `Makefile` header note stops claiming `make check` leaves the target out, and states what the target holds instead | Documentation correction | `Makefile` |
| A `make authoring` row joins the command table, stating what it asserts; without it `make tables` fails in its second direction | Documentation addition | `checks.md` |
| `checks.md` lists `authoring.py` among the standard-library scripts it describes | Documentation correction | `checks.md` |
| `checks/README.md` no longer says `make check` runs every check but `authoring.py` and `render.py` | Documentation correction | `checks/README.md` |
| Thirteen failing cases join the check's suite: the Inputs and Outputs branches beside the one held, a Commands section holding nothing and one written with emphasis, commands in the preamble, ahead of an operation's steps and in a tilde fence, non-shell and template fences that are no finding, a reference definition carrying an absolute path, a link with no path part, and the check's own verdict naming the file | Rule coverage | `checks/tests/test_authoring_check.py` |
| The check's verdict is held by a test rather than by observation: `main()` returning `1` and printing the offending path, and `0` on a clean file | Rule coverage | `checks/tests/test_authoring_check.py` |
| The demonstrated failure, the wiring evidence and the criterion-to-rail map | Planning record | `validation.md` |
| This change list | Planning record | `change-list.md` |

No plan change was made: the work item, its coverage and its dependencies
stand as the epic states them. W10 is the last open row of the epic's work
breakdown.

## Held

| Item | Why it is held |
| --- | --- |
| `make render` remains outside `make check` | It needs mermaid-cli and a headless browser, which the build does not depend on. Adding it would make the repository's own checks need tooling no dependency declares, and AC12 names the authoring check alone. |
| W09's AC9 and AC10 ticks | Outside this task's coverage. W09 delivered them; the epic body still shows the two criteria unticked and the W09 row's Done cell empty. Closing them belongs to the epic, not to this delivery. W10's own row in the epic body is recorded by the delivery rather than by a plan change. |
| The fixture `source` symlinks | `fixtures/usage-example/*/source` points at `example/work-planner`, so a break in any file a fixture's closure reaches fails `make corpus` before `make authoring` runs. That is correct — the fixture is the stronger statement — but it means an authoring rule break in a reached file is reported by the corpus as a byte difference rather than by the rule it breaks. Raising the authoring check ahead of `corpus` in `check` would report the rule first; it is a change to the check order this task's criteria do not ask for, and is reported rather than taken. |
