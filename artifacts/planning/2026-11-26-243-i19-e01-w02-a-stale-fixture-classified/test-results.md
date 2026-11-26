# W02 Test Results

> Tested revision `eed4c86546ae4456c7d779e80b8eaf0579e34597` on `i19/e01/w02-stale-fixture-classified`, 2026-11-26.

## T1 One Fixture per Category

`checks/tests/test_triage.py::test_each_fixture_is_named_under_its_own_category` writes a corpus holding one fixture per drift category, one whose run fails in itself and one that meets its manifest, each carrying the build step its run takes. Triage names each moved fixture under its own category in category order, names the failed one apart as `run failed in itself`, leaves the passing one out, and leaves every file of the corpus byte for byte as it found it. Passed under `make harness`.

## T2 One Category Selected

`checks/tests/test_triage.py::test_only_reports_the_selected_category_alone` writes a corpus holding an `inserted` fixture, a `rewritten` fixture and one whose run fails in itself, and selects `inserted`. The report names the `inserted` fixture alone. Passed under `make harness`.

## T3 Green Corpus

`checks/tests/test_triage.py::test_a_green_corpus_produces_no_report` triages a corpus holding a passing fixture and an awaited one, and prints nothing. Over the repository's own corpus, `make check` with `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"` reported `corpus check: 708 fixture(s), 708 pass, 0 fail, 0 awaited, 0 unexpected pass`, and `make triage` with the same build then printed no report, exited zero and left `git status` clean.

## T4 Content Edits and Selection

`test_content_edits_are_read_line_by_line` holds a newline spelled as CRLF and a lost final newline to `rewritten`, and an insertion, a removal and an unequal replacement to their categories. `test_named_fixtures_are_triaged_alone`, `test_an_identity_no_fixture_carries_is_refused` and `test_triage_without_a_build_fails` hold identity selection, its refusal and the absent build. `checks/tests/test_runner.py::test_the_result_carries_each_file_the_run_wrote` holds the runner's `written` field. A line appended to the expected bundle of `absorbed-title/a-reference-naming-an-absorbed-title`, triaged by identity against the real build, was named `removed`; the change was reverted.

## T5 Repository Checks

`make check` with the build configured as in T3 exited zero, `make links` included.
