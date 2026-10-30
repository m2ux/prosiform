# Session Retrospective: Restoring Main After a Parent Arrangement Change

> Plan · Created 2026-10-24

## Executive Summary

`main` was red for most of 2026-10-24. The work that fixed it was done in about two hours, and roughly a third of that was spent on misdirections that a script or a stated rule would have removed. This record names them, with the evidence each one turned on, so the next session spends its time on the change rather than on rediscovering how to read the repository.

Three findings are worth more than the rest:

**The check suite reports one failure at a time, and the reported failure is wrong.** `make check` stops at the first failing target. Across six consecutive red commits on `main`, the *reported* failing target moved — `links`, then `corpus`, then `test` — while the set of failures underneath was neither shrinking nor the same. Each commit therefore looked like a different problem and none of them named the real one.

**A behaviour change and a crash look identical from the fixture runner.** `checks/runner.py` reports both as a fixture that failed, and the obvious response — regenerate the expectations from the build's output — records a crash as the corpus's truth. Two fixtures in this session would have been inverted that way, and one of them would have declared that a published bundle compiles.

**The `root` declaration has three jobs and no stated scope.** Two commits had already misread it and were merged red. Reading it correctly took several probes because nothing in the contract distinguishes the three.

## What Went Wrong

| Misdirection | Cost | What would have removed it |
| --- | --- | --- |
| Read the CI log for the tip commit and took `Makefile:50: test` as the whole problem | Two probes to discover `links` and `corpus` were also red | A command that runs every target and reports all failures |
| Hand-wrote seven throwaway classifier scripts | Repeated rebuild-and-guess before the real question was formed | One triage tool that names the category of each difference |
| Regenerated expectations before checking for crashes | Nearly inverted two fixtures; one crash found only by reading | Resolve any internal error before any expectation is touched |
| Rebuilt a fixture manifest from parsed TOML | Escaped every em dash in 177 manifests, hiding the real diff | Edit only the block that changed |
| Created three baseline worktrees and left them behind | Two detached worktrees still present when this record was written | One helper that creates, uses and removes a checkout |
| Probed `root` five times to separate its three jobs | Several rebuilds per question | Runs recorded once, as evidence in [the root note](../2026-10-24-root-declaration-roles/README.md) |
| Wrote `regenerate.py` twice, in two places, differently | ~300 lines duplicated; the copies have since diverged | The tool belongs in `checks/`, where the corpus lives |

## Evidence

### The reported failing target moves

Each commit is `main`'s history immediately before this session. The target named is the one `make check` reported, read from each job's log.

| Commit | Reported failing target |
| --- | --- |
| `3d549a26` | `Makefile:80: links` |
| `52851dd` | `Makefile:56: corpus` |
| `c74d927` | `Makefile:56: corpus` |
| `ee0aac0` | `Makefile:56: corpus` |
| `16306e4` | `Makefile:56: corpus` |
| `15c7805` | `Makefile:50: test` |

The `links` failure was present at `3d549a26` and at every later commit, but from `52851dd` onward `corpus` failed first and `links` never ran. By the tip, `test` failed first and neither of the other two was reached. Reading the tip's log alone would have produced a session that fixed `test`, declared success, and left `main` red on two other targets.

`make -k check` on the same tree reports every failing target rather than the first: four failures where `make check` reports one. On the fixed tree it exits 0 with no failures, so it is a drop-in replacement for a session reading a red run.

### A crash and drift are indistinguishable to the runner

`checks/runner.py` decides a fixture from its manifest and returns `Result.passed`, which is false for both. The distinction lives in the run, not the verdict:

| Fixture | Verdict | What a regeneration would have written |
| --- | --- | --- |
| `depth-overflow/a-source-heading-the-shift-pushes-past-the-sixth` | failed | `exit_status = 0`, contradicting the clause the fixture exists for |
| `generated-input/a-bundle-offered-as-input` | failed | `exit_status = 0`, declaring that a published bundle compiles |
| `self-reference/a-section-link-to-its-whole-document` | failed | nothing — refused, which is how the crash was found |

The third is the one that worked, and it worked only because the tool refused an internal error rather than writing it.

### The two link commits were merged red

Both rewrote a link to drop the `rules/` prefix its declared root required. CI reported `links` on `3d549a26` and reported `corpus` on `a7862b53`'s successor, so neither was caught by a reader taking the reported target at its word.

## What To Do About It

Two changes carry most of the value, and neither is large.

**Read every target, every time.** `make check` reporting one failure is the single largest source of misdirection here. `make -k` already fixes the reading half of it and needs no new code. A `check-all` target that runs every check and summarises would fix the rest.

**Triage before regenerating.** The corpus is the repository's statement of what the build does. A tool that rewrites it from the build's output can delete that statement while leaving it green, and it will, unless it refuses a run that crashed. The two tools written here are already preserved and raised as [issue #243](https://github.com/m2ux/prosiform/issues/243); this record adds what they must not lose.

Both are carried in [findings](findings.md). The scripts that remove the guesswork are in [tooling](tooling.md).

## Links

| Resource | Link |
| --- | --- |
| Findings | [findings.md](findings.md) |
| Tooling | [tooling.md](tooling.md) |
| Corpus drift tools | [Issue #243](https://github.com/m2ux/prosiform/issues/243) |
| Root declaration roles | [Planning record](../2026-10-24-root-declaration-roles/README.md) |
| Root scope proposal | [Issue #245](https://github.com/m2ux/prosiform/issues/245) |
