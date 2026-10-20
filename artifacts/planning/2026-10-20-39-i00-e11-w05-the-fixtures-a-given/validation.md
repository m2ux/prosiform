## Overview

What this row was measured to do at `97ca793`, the checks it was held to, and the review of the delivered change against the surface it was planned to touch.

## The Tests That Observe AC6

`AC6` asks for the report's run against a corpus carrying fixtures awaiting two different pieces of work. `checks/tests/test_corpus_run.py` builds that corpus — one fixture awaiting `I00:E03`, one awaiting `I00:E04:W02`, one awaiting nothing — and asks it each question.

| Case | What it observes |
| --- | --- |
| `test_the_report_names_what_one_piece_of_work_unblocks` | Each of the two names returns its own fixture and not the other's, which is the discrimination the criterion asks for. |
| `test_the_report_names_no_fixture_awaiting_other_work` | The whole report for one name: the fixture's identity, then the count, and nothing from the fixture awaiting the other work or from the fixture awaiting nothing. |
| `test_work_no_fixture_awaits_unblocks_nothing` | A name no manifest declares reports a count of zero rather than printing nothing. |
| `test_a_marker_naming_an_epic_is_not_the_task_within_it` | `I00:E04` finds no fixture although `I00:E04:W02` does, so the grain a marker was written at is the grain it answers. |
| `test_the_report_answers_without_a_build` | With `PROSIFORM_BUILD` unset the request returns zero and names the fixture, so the answer is available before anything is built. |
| `test_a_request_names_the_work_it_asks_about` | `--awaiting I00:E03` reaches the report as that name. |
| `test_a_run_naming_no_work_runs_the_corpus` | An invocation naming no work asks nothing, so `make corpus` still runs the corpus. |

The request was also exercised against this repository's own corpus at the delivered head, which is the live counterpart of the test corpus: it carries two fixtures awaiting two different pieces of work.

| Request | Answer |
| --- | --- |
| `--awaiting I00:E11:W10` | `reference/a-marked-link-inside-image-alternative-content`, 1 fixture(s) |
| `--awaiting I00:E11:W14` | `grouping/a-rule-matching-no-document-in-the-closure`, 1 fixture(s) |
| `--awaiting I00:E11` | 0 fixture(s) |

## The Gate

Every target of `make check`, run in the unit's worktree at `97ca793`. `make corpus` and `make invocation` were given `PROSIFORM_BUILD` naming this checkout's build by absolute path, because a fixture's run has the fixture's own directory as its working directory.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved, no change |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 603 passed |
| `make harness` | 386 passed, up from 379 by this row's seven |
| `make corpus` | 203 fixture(s), 201 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `make smoke` | Installs and bundles a reference from a source root, resolved by name outside the repository |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) of the documented invocation held to the build |

## The Review

- **The corpus run is untouched.** The request is read before the run begins and returns on its own path; every verdict, line, summary and exit status below it is the code that was there, and the suite's existing corpus-run cases pass unchanged.
- **The report adds no make target.** It takes an argument, so it belongs to the command rather than to the check set, and `make corpus` keeps naming the run alone. Nothing was added to the command tables that `make tables` holds in both directions.
- **No second reader of the marker was introduced.** The report calls the same `awaiting()` the run calls, over the same manifests the same walk discovers, so there is one reading of the declaration and no list to drift.
- **The change is confined to the stated surface.** Four files: `checks/corpus.py`, `checks/tests/test_corpus_run.py`, `checks/README.md`, `fixtures/README.md`. Nothing in `src/`, no fixture, no manifest, no schema, no `Makefile`.

## Limitations

The report has no check of its own in `make check`, deliberately: it answers a question rather than asserting a claim, and a report whose answer is zero fixtures is correct. Its behaviour is held by the harness suite, which does run with the others.

A name is matched exactly, so asking about an epic finds nothing when its fixtures were marked at task grain. This is the decision rather than an oversight — the two grains are separate questions — but it means a session must ask with the identity the marker carries, which `fixtures/README.md` says.
