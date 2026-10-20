## Overview

What the delivery of `I00:E07:W03` was measured to do at `937c4f9`, and the review the dispatcher ran over it independently of the delivering session's report.

## What Changed

The repository documents the invocation a caller writes, and a check holds that documentation to the command the build installs, so the two cannot drift apart.

`README.md` carries an option table of seventeen rows — the positional reference and every option — and an exit-status table of five, each cell reproducing the command's own help text word for word. Defaults sit inside those effect texts, where the command states them, rather than in a column of their own that would be a second place for one fact to drift.

Two prose statements were added for `AC5`: that a failed run stops the work and publishes nothing, and that reading the sources instead is unsupported. A third subsection declares the supported environment.

`checks/invocation.py` runs the build named by `PROSIFORM_BUILD`, reading it through the corpus runner's own `build_under_test` so one function serves the corpus and the documentation. It compares arguments and exit statuses in both directions, reads the profile identifier from the version output because the help does not carry it, and holds each prose statement to the sentence that states it.

## The Supported Environment

The build reads every source through rooted, no-follow access, which rests on the `O_NOFOLLOW`, `O_DIRECTORY` and `O_CLOEXEC` open flags, and `access.py` refuses to start where they are absent. The contract requires a platform that cannot enforce the policy to fail or to declare a narrower supported environment; the failing half already existed and this row is the declaring half. The documentation names Linux and macOS and says what the support rests on, so a caller elsewhere reads the limit rather than meeting it as an import failure.

## The Gate

Measured by the dispatcher in a separate worktree, not taken from the delivering session's report.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 42 files already formatted |
| `make typecheck` | Success: no issues found in 41 source files |
| `make test` | 495 passed |
| `make harness` | 319 passed |
| `make corpus` | 157 fixture(s), 152 pass, 0 fail, 5 awaited, 0 unexpected pass |
| `make smoke` | prosiform installs into an environment and bundles a reference from a source root |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 6 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) of the documented invocation, each held to the build |

The invocation check is the thirteenth target of `make check`, and the command table in the README names it, so `tables.py` stayed green in the same change that added it.

## The Review

- **The change is confined to its surface** but for one file. Six files: the README, the new check, its tests, the `Makefile`, `checks/README.md` and `.github/workflows/checks.yml`. The workflow was outside the surface the dispatcher named, and the session flagged it rather than letting it pass unremarked. The dispatcher read the diff: **comment text only**, no behaviour, because `PROSIFORM_BUILD` is already job-level environment and the comment claimed only the corpus read it.
- **Nothing under `src/prosiform/`, `fixtures/` or `checks/links.py` was touched**, which were the two concurrent sessions' surfaces.
- **No catalogue movement and no contract change.** `design.md` and the schema are untouched.
- **A shared helper was deliberately not hoisted.** `tables.py` holds a `plain()` the new check needed, and the session defined a local one rather than editing `documents.py` while two other sessions were running. That is the right call under concurrency and the wrong one to leave standing; folding it into `documents.py` is noted for a later change.

## Limitations

`AC5`'s evidence clause says "as the documentation check shows", and two of its statements are policy rather than an option surface. There is nothing on the command to compare them against. The strongest evidence that can exist is that the check holds each statement to the sentence stating it, so the statement cannot be dropped silently and `make invocation` fails if it is; what makes it *true* is the review that landed it. The session said so in the script, in `checks/README.md` and in the pull request rather than presenting the check as proving more than it does.

The same applies to the supported-environment declaration.
