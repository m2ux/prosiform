## Overview

What decided `I00:E11:AC12`, what the delivery was measured to do at `5a6405a`, and the review the dispatcher ran over it independently of the delivering session's report.

## The Measurement That Decided It

The criterion was written "named or ruled out" because nothing this repository references had answered 403. The row probed hosts a technical document routinely names, with the check's own user agent, and then repeated the request as a browser.

| Address | HEAD | GET | GET as a browser |
| --- | --- | --- | --- |
| A national newspaper | 403 | 403 | 403 |
| A programming question site | 403 | 403 | 403 |
| A publishing platform | 403 | 403 | 403 |
| A news agency | 401 | 401 | — |
| commonmark.org, pypi.org, json-schema.org, shields.io | 200 | 200 | — |

The fourth column decided it. The refusal survives a browser user agent, so it is taken on the requesting network rather than on the agent or the target: the same address serves the reader who follows the link and refuses the run that checks it. A status recording where the check ran states nothing about the document, which is the shape of the defect [#84](https://github.com/m2ux/prosiform/issues/84) closed in its other form.

Three of the most commonly cited hosts on the web are already in that state, so the cost is measured rather than hypothetical: the first document to cite one would redden the branch.

All eighteen external addresses this repository actually references answered 200, which is why the evidence had to be gathered rather than observed.

## What Changed

A forbidden response joins a server status, a failed connection and a timed-out request: three bounded attempts, a `WARN` line, a passing run. `verdict()` reads `status >= 500 or status == 403`, and the tracker read through `gh api` reads the same boundary, so the verdict the README states is true of every remote read rather than of one path.

The `HEAD` 403 then `GET` re-ask is unchanged, so a host refusing only the method still resolves.

A status of 401 keeps the failing verdict deliberately, and the README says so: an authorization scheme is one a caller could satisfy. A method refusal of 405 to both methods likewise. Both are carried to [#98](https://github.com/m2ux/prosiform/issues/98) with the live evidence found for the first.

## The Gate

Measured by the dispatcher in a separate worktree at the delivered head, not taken from the delivering session's report.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 37 files already formatted |
| `make typecheck` | Success: no issues found in 36 source files |
| `make test` | 479 passed |
| `make harness` | 309 passed, up from 304 by this row's five |
| `make corpus` | 156 fixture(s), 151 pass, 0 fail, 5 awaited, 0 unexpected pass |
| `make layout` | 3 tree(s) present |
| `make tables` | 12 command(s) and 7 declaration(s) |
| `make links` | Every reference in 6 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |

## The Review

- **The change is confined to the stated surface.** Three files: `checks/links.py`, `checks/tests/test_links.py`, `checks/README.md`. Nothing in `src/`, no fixture, no `Makefile`, no catalogue movement, nothing pushed to `engineering`.
- **No status other than 403 and 500-or-above became a warning.** Confirmed by reading `verdict()`: the test is `status >= 500 or status == 403`, and every other client status falls through to the failing branch.
- **401 is still an unresolved reference**, held by a test of its own rather than left to the reader.
- **Both methods are asked on every attempt.** The loopback harness counts six requests across three attempts for a host refusing both, so the retry is observed rather than assumed.

## Limitations

The evidence for 405 is absent: no host was found refusing `GET` on a live page, so that status keeps the failing verdict without a measurement behind it. It is named in `#98` rather than decided here.

The hosts in the table are named in `checks/README.md` as code spans rather than links, so the link check does not try to reach the addresses whose refusal is the reason for the rule.
