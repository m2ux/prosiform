## Overview

What decided `I00:E11:AC14`, and what the delivery was measured to do at `d985790`.

## The Measurement That Decided It

The criterion was written "named or ruled out". [#98](https://github.com/m2ux/prosiform/issues/98) carried one live observation for 401 and none at all for 405, so the row probed live hosts for each, with the check's own user agent and then as a browser, repeating W11's method so the two verdicts rest on comparable evidence.

| Address | What it is | `HEAD` | `GET` | `GET` as a browser |
| --- | --- | --- | --- | --- |
| `httpbin.org/post` | An endpoint that exists and accepts `POST` | 405 | 405 | 405 |
| `api.github.com/user` | A resource read with credentials | 401 | 401 | 401 |
| `registry.npmjs.org/-/whoami` | A resource read with credentials | 401 | 401 | — |
| `api.openai.com/v1/models` | A resource read with credentials | 401 | 401 | — |
| `www.reuters.com` | A live home page | 401 | 401 | 401 |
| `commonmark.org`, `pypi.org`, `jsonplaceholder.typicode.com`, `img.shields.io` | Addresses this repository references | 200 | 200 | — |

Two readings come out of the table, and they differ.

**405 is a fact about the target.** The status names which methods the address allows, and that answer does not move with the caller: `httpbin.org/post` returns it to the check and to a browser's user agent alike. The method the check falls back to after a refused `HEAD` is `GET`, which is the method a reader's browser uses, so a host refusing both is serving the reader nothing. There is no reading under which such an address resolves for a reader and fails only for the check, which is the condition the unreachable verdict exists for.

**401 turns on the caller, and is held to anyway.** `www.reuters.com` is the case the failing verdict costs: a correct, live home page answering 401 to both methods and to a browser's user agent, a bot defence wearing an authentication header, which is the 403 shape in another status. Three other hosts in the table answer 401 for the status's ordinary reason, and a document citing one of those is citing an address a reader must hold credentials to follow — something the document should disclose rather than the check wave through. The decisive cost is elsewhere. `gh api` answers 401 when this check's own credentials are missing or stale, and `links.py` reads every tracker reference through it. Counting 401 as silence would turn an unauthenticated run into a green one that verified no issue, pull request or board at all. 401 is the only status that can name the check's own standing, and silence about that is silence about everything the check was asked to read.

The boundary therefore stays where W11 left it: 500 or above, and 403. 401 and 405 are answers about the target and the document is held to both, now by a decision stated in `checks/README.md` and in `verdict` rather than by falling through the branch that forbids 403.

## The Loopback Tests

Measured against the server `checks/tests/test_links.py` runs on the loopback interface, which answers the statuses each case names and counts the requests it received, so the `GET` re-ask is observed rather than assumed. Six tests were added and the suite went from 379 to 385.

| Test | What it holds | Result |
| --- | --- | --- |
| `test_a_host_refusing_the_method_on_both_is_an_unresolved_reference` | A host answering 405 to both methods yields `HTTP 405`, an unresolved reference | Passed |
| `test_a_host_refusing_the_method_on_both_is_asked_with_each_once` | Both methods are asked, and the answer is not retried, so two requests reach the host | Passed |
| `test_a_host_refusing_the_method_on_head_and_serving_get_resolves` | A host refusing only `HEAD` resolves on the page `GET` serves | Passed |
| `test_a_document_naming_a_host_refusing_the_method_fails` | The document naming such an address is a failure, not a warning | Passed |
| `test_an_unauthorised_page_is_an_unresolved_reference` | A host answering 401 yields `HTTP 401`, an unresolved reference | Passed |
| `test_an_unauthorised_page_is_decided_on_the_answer_to_head` | 401 is decided on one request, because credentials do not vary with the method | Passed |
| `test_a_document_naming_an_unauthorised_page_fails` | The document naming such an address is a failure, not a warning | Passed |

## The Gate

`make check` run in the unit's worktree at `d985790`, against the build `PROSIFORM_BUILD` names.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 603 passed |
| `make harness` | 385 passed, up from 379 by this row's six |
| `make corpus` | 203 fixture(s), 201 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `make smoke` | Installed, resolved outside the repository, and bundled |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) held to the build |

## The Review

- **No status changed verdict.** `verdict()` still reads `status >= 500 or status == 403`, and `reach()` still re-asks with `GET` on 403 and 405 alone. The row states a reading the code already carried and holds it with tests; a reader now meets the reason rather than the fall-through.
- **The change is confined to the stated surface.** Three files: `checks/README.md`, `checks/links.py`, `checks/tests/test_links.py`. Nothing in `src/`, no fixture, no `Makefile`.
- **The hosts are named as code spans.** `httpbin.org/post`, `api.github.com/user`, `registry.npmjs.org/-/whoami`, `api.openai.com/v1/models` and `www.reuters.com` appear in `checks/README.md` as code spans rather than links, so `make links` does not reach the addresses whose refusal is the reason for the rule. The passing `make links` run confirms it.
- **The `WARN` line is unaffected.** A host answering 403 or a server status is still named on its own line every run and still leaves the run passing.

## Limitations

The 401 verdict is decided against one live counter-example rather than a survey. Should a second class of live page adopt 401 as a bot defence, the balance the record weighs would shift, and the `gh api` cost would then have to be met by telling the tracker read apart from the direct read rather than by the one boundary both share.

A host answering 401 to `HEAD` while serving `GET` is held to the 401 without the second request being made. No such host was observed, and the status names credentials rather than a method, so the re-ask stays reserved for the two statuses that can be about the method.
