## Overview

What the link check was measured to do on `i00/e11/w07-an-unreachable-host-told` at `502f636`, and the checks the delivery was held to.

## The Verdicts

A server on the loopback interface answers the statuses each case names and counts the requests it received, so the retry is observed rather than assumed. The tests live in [`checks/tests/test_links.py`](https://github.com/m2ux/prosiform/blob/i00/e11/w07-an-unreachable-host-told/checks/tests/test_links.py) and run under `make harness`.

| Case | Measured |
| --- | --- |
| A host answering 503 | Reported as unreachable, reason `HTTP 503` |
| A host answering 404 | Reported as an unresolved reference, reason `HTTP 404` |
| A host answering 503 on every attempt | Requested three times, the bounded number |
| A host answering 503 then 200 | Resolved, requested twice |
| A host answering 404 | Requested once, decided on the first answer |
| A document naming a host answering 503 | No failure, one warning carrying `HTTP 503` |
| A document naming a host answering 404 | One failure carrying `HTTP 404`, no warning |

The last two run the check over a document, so the separation is measured where the run reads it rather than only at the resolver.

## The Gate

Measured in the delivery worktree at `502f636`.

| Target | Result |
| --- | --- |
| `make lock-check` | Passed |
| `make lint` | All checks passed |
| `make format-check` | 34 files already formatted |
| `make typecheck` | Success: no issues found in 33 source files |
| `make test` | 451 passed |
| `make harness` | 298 passed, up from 291 by this row's seven |
| `make corpus` | 150 fixture(s), 145 pass, 0 fail, 5 awaited, 0 unexpected pass |
| `make layout` | 3 tree(s) present |
| `make tables` | 12 command(s) and 7 declaration(s) |
| `make links` | Every reference in 6 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |

## Limitations

`make links` was run while every host it names was answering, so the run exercised the resolving path rather than the warning one. The warning path is measured by the tests above against a server this repository controls, which is the only way to observe a chosen status on demand.

The retry's delay is three attempts two seconds apart and then four, so a document naming many silent hosts takes correspondingly longer to check. No document the repository owns names more than a handful of remote addresses.

A status of 403 or 405 is still read as an answer about the method rather than the target, and the address is asked for again with GET before its status is read. A host that answers 403 to both remains an unresolved reference, which is the behaviour this row leaves unchanged.
