# Test Results

Results for F10 at `7abf6065d` on `f10-scorer-shell-reading`, run on 2026-11-13 in the unit checkout.

## T1 Adjacent Redirection

`test_score.py::test_a_duplicated_descriptor_is_its_redirects_operand`: `pf target.md 2>&1>out`, `2>&1>>guide.log`, `>out 2>&1>&2`, `2>&- <&0 >out` and `3>&1- >out` each read as one run of `target.md`, and a scenario stating that run passes its run checks. The first three fail on the base commit `69e4da155`. Held.

## T2 Malformed Adjacent Redirection

`test_score.py::test_a_malformed_adjacent_redirection_satisfies_no_compile`: `2>&1>` at the end, a bare `>&`, `2>& >out`, `> 2>&1`, `>& 2>&1`, `2>&1 <` and `<<< >out` each read as invalid usage, and a scenario stating the run is scored uncompiled. Held.

## T3 Heredoc Body

`test_score.py::test_a_heredoc_body_is_data_rather_than_commands`: a body quoting `pf target.md`, an adjacent-redirected `pf` and a bare `pf`, under `<<'EOF'`, `<<"EOF"`, `<<EOF`, `<<\EOF`, `<< EOF`, `<<-EOF` with tab-indented lines and delimiter, two heredocs on one line, and a body holding a line that only opens with the delimiter, reads as no run: a scenario stating the run is scored uncompiled, and one stating no run passes, so the body creates no compile event. Every case fails on the base commit. Held.

## T4 Runs Beside a Heredoc

`test_score.py::test_runs_beside_a_heredoc_stay_observable`: `pf a.md` and `pf b.md` before and after a heredoc, on the line that opens it, around two heredocs one of which feeds `pf`, and beside a here-string, read as exactly those two runs, which a scenario stating them passes. `test_score.py::test_an_unterminated_heredoc_invalidates_its_segment`: a body no line closes, a heredoc with no body, a tab-indented delimiter under plain `<<`, and a second heredoc left open, each read the opening segment as invalid usage while runs before it stay observable, and the stated run does not pass. Held.

## T5 Eval Harness

`pytest evals/diagram-following`: 815 passed. Held.

## T6 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's built `pf`, exits 0: lint, format, typecheck, `make test` (2137 passed), harness (1054 passed), corpus (615 fixtures, 615 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. `make check` does not run the eval harness; T5 holds it. Held.

## Limitations

- The reading stays lexical. Forms no session record has shown, such as `&>` and comments, keep their earlier reading.
