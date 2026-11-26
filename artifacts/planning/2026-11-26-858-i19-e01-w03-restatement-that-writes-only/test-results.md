# W03 and W04 Test Results

Tested revision: `4b816c87f` on `i19/e01/w03-restatement-writes-only-bundles`, cut from `i19/e01/main` at `81c5ca020`. The harness cases are in `checks/tests/test_restate.py`; each builds a small corpus in a temporary directory whose fixtures carry a shell-script build.

## T1 Dry run

`test_a_dry_run_names_the_stale_fixture_and_leaves_the_tree_clean` commits a corpus holding one met and one stale fixture to a git repository, runs restatement without `--write`, and reads `git status --porcelain --untracked-files=all`. The output is `would restate stale: rewritten`, the status is empty and the exit status is 0. Observes AC6.

## T2 Written bundles and manifest

- `test_writing_replaces_the_bundles_and_leaves_the_manifest` restates two bundles whose content moved. Only the two files under `expected/` change; the manifest, which carries an em-dash clause and a second clause, is byte-identical, and a second run reports nothing.
- `test_a_renamed_bundle_edits_only_its_name_in_the_manifest` restates a run that renames `helper.bundle.md` to `aide.bundle.md`. The manifest after equals the manifest before with that one string replaced, the em dash survives unescaped, the old bundle is removed, and the fixture then passes.

Observes AC7.

## T3 Reachability and imports

- `make links` resolves `../checks/triage.py`, `../checks/restate.py` and `../checks.md#restatement` from `fixtures/README.md`, and `make tables` finds `make restate` named in `checks.md`.
- `test_each_command_reads_the_corpus_run_and_its_runner` reads the imports of `triage.py` and `restate.py`: each imports from `corpus`, `runner` and `manifests`.

Observes AC8.

## T4 Run failed in itself

`test_a_fixture_a_reader_decides_is_refused_and_named[failed]`: a fixture whose build exits 4 beside a stale one. Output `refused failed: run failed in itself`, exit status 1, and only the stale fixture's bundle changes. `test_a_dry_run_refusal_fails_the_run` shows the same refusal fails a dry run. Observes AC9.

## T5 Status and diagnostics

`test_a_fixture_a_reader_decides_is_refused_and_named[status]` and `[streams]`: a fixture exiting 1 against a declared 0, and one emitting an undeclared warning. Each is named `refused <name>: status` or `streams`, left as it was, and the exit status is 1. Observes AC10.

## T6 Number of bundles

`test_a_fixture_a_reader_decides_is_refused_and_named[layout]`: a run writing two bundles where one is declared. Named `refused layout: layout`, left as it was, exit status 1. Observes AC11.

## T7 make check

`make check` with `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"`, run unsandboxed: every target passed. Harness 1196 passed, corpus 708 pass, link check every reference in 445 documents resolved, table check 23 commands each named by a table.

## T8 Real corpus

In the worktree, revertibly, three fixtures were made stale and staged:

- `dispatch-brief/two-briefs-picking-different-alternatives-publish`: `investigate-beta.bundle.md` renamed to `investigate-gamma.bundle.md`, in the file and the manifest.
- `dispatch/a-dispatched-section-of-fields`: a line appended to `plan__fields.bundle.md`.
- `dispatch/a-dispatch-in-a-title-above-the-selection-is-refused`: `exit_status` changed from 1 to 2.

`make restate` printed `would restate ... names`, `would restate ... removed`, `refused ... status`, exited nonzero, and `git status` showed only the staged changes. `make restate ARGS="--write"` printed the same lines as restated; [the unstaged diff](real-corpus-restate.diff) is what it wrote: the manifest's one string back to `investigate-beta.bundle.md`, `investigate-gamma.bundle.md` removed, `investigate-beta.bundle.md` written identical to `HEAD`, the appended line removed, and the refused manifest untouched. The trial was reverted before committing.
