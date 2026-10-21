# Validation — I00:E11:W16

> Recorded 2026-10-21 against `i00/e11/w16-one-verdict-boundary-for`, cut from `i00/e11/main` at `ce4483c`.

## What Was Measured

The link check reads a tracker reference through `gh api`, which keeps the response's status out of its exit code. The question this record answers is where the status can be recovered from, what each route then decides, and whether the two routes agree.

## The Status `gh` Reports

`gh api --include` writes the response's status line ahead of its headers, on standard output, whether the call succeeded or failed. Three live calls were made against `m2ux/prosiform` with the host's credentials:

| Call | Exit | First line of standard output | Last line of standard error |
| --- | --- | --- | --- |
| `repos/m2ux/prosiform/issues/127` | 0 | `HTTP/2.0 200 OK` | — |
| `repos/m2ux/prosiform/issues/99999999` | 1 | `HTTP/2.0 404 Not Found` | `gh: Not Found (HTTP 404)` |
| `graphql` naming `projectV2(number: 999)` | 1 | `HTTP/2.0 200 OK` | `gh: Could not resolve to a ProjectV2 with the number 999.` |

Two observations decide the design.

- **The status line is the response's own.** Its form is fixed by the HTTP specification rather than composed by the command, so reading the number from it does not rest on wording the GitHub CLI is free to change.
- **A GraphQL error arrives under a resolving status.** The transport answered 200 and the error sits in the body. A status that resolves therefore cannot be the whole verdict for a failing call: the reason the command gave stands where the status states nothing against it.

A call that never received a response — a timeout, or a name that does not resolve — writes no status line, and is the host saying nothing for a reason of its own.

## Tests

`checks/tests/test_links.py` measures the tracker route against a stand-in for `gh api` answering the status line and the message each case names, and the direct route against the loopback server it already used.

| Check | What it holds |
| --- | --- |
| `test_a_tracker_read_and_a_direct_read_take_one_verdict` | 503, 403, 404, 401 and 405 each take, on a tracker call, the outcome `verdict()` states for that status |
| `test_a_tracker_call_reporting_a_server_status_is_unreachable` | A tracker call reporting 503 carries the unreachable verdict with the reason `HTTP 503` |
| `test_a_tracker_call_the_host_forbade_is_unreachable` | A tracker call reporting 403 carries the unreachable verdict with the reason `HTTP 403` |
| `test_a_tracker_call_naming_a_missing_target_is_unresolved` | A tracker call reporting 404 is an unresolved reference, reported as `HTTP 404` |
| `test_a_tracker_call_carrying_no_status_is_unreachable` | A failure with no status line carries the unreachable verdict with the command's own reason |
| `test_a_graphql_error_under_a_resolving_status_is_unresolved` | A failing call under a 200 is an unresolved reference carrying the reason the command gave |
| `test_a_tracker_call_is_read_with_the_response_included` | The call is made with `--include`, which is what writes the status line |
| `test_a_document_naming_a_forbidden_tracker_reference_passes` | A document naming a forbidden tracker reference warns and leaves the run passing |
| `test_a_document_naming_a_missing_tracker_reference_fails` | A document naming a missing tracker reference fails the run |

## Live Observation

The check was run over a document naming four tracker references with the host's credentials:

```
FAIL https://github.com/m2ux/prosiform/issues/99999999 — HTTP 404
FAIL https://github.com/users/m2ux/projects/9999 — gh: Could not resolve to a ProjectV2 with the number 9999.
ok   remote     https://github.com/m2ux/prosiform/issues/39
ok   remote     https://github.com/users/m2ux/projects/18
```

A missing issue is reported in the words a direct read of the same status uses. A missing project board keeps the reason the command gave, because its status resolved. Both live references resolve.

The same document was then read with a credential the host rejects, and the reference came back `HTTP 401` — an unresolved reference, which is the reading [W12](../2026-10-20-98-i00-e11-w12-a-host-answering-401/) settled and the one that keeps a run reading no tracker reference from passing in silence.

## The Repository's Own Check

`make check` was run whole, with `PROSIFORM_BUILD` naming this worktree's build. Every target passed, exit status 0: `lock-check`, `lint`, `format-check`, `typecheck`, `test` (670 passed), `harness` (502 passed), `corpus`, `smoke`, `layout`, `tables`, `links`, `vocabulary` and `invocation`.

## Limitations

- **The tracker route's statuses are measured against a stand-in.** No third-party host answers 503 or 403 to an authenticated `gh api` call on demand, so the status line and the message are supplied to the module rather than produced by GitHub. What the live calls establish is that the status line exists and carries the number; what the stand-in establishes is what the module then decides.
- **One GraphQL shape was observed.** A GraphQL call that fails at the transport rather than in the body would carry a non-resolving status and take the status's verdict. That path follows from the same branch and is not separately measured.
