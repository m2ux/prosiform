# Delivery Progress

- [x] Confirm board queue and prerequisite delivery.
- [x] Implement and verify derived output publication.
- [x] Publish and merge the task pull request; record epic delivery.

## Prerequisite Verification

At merged epic revision `f5e608e85623b39be886e0c22be271072410aec4`, the 19 tests in `src/tests/test_file_roots.py` pass and `make smoke` passes, observing installed file-only invocation and rejection of `-r`. AC20, AC21 and AC22 are verified and W08 is recorded complete on issue 218. The board queue reports no pending change. Review 227 cites both merged contract tasks, 219 and 226.

The user confirms repository issue auto-closing is disabled for this session and authorizes proceeding with W09. The row has no task issue. W10 depends on W09; W11 depends on W10.

## Test Evidence

Observed at `ff10886de3bb4aa3f91454ad8b2fb5b53eb2e6f2` on `i01/e06/w09-derived-output-publication`. `make check` exited 0 with `PROSIFORM_BUILD` set to this checkout's `pf`.

### T1 Whole-file and fragment names

`tests/test_derived_output.py` runs `pf` on one file and on one section, for suffixes `.md`, `.markdown`, `.MD` and `.MARKDOWN`. The derived file in the working directory matches the bundle `-o -` prints for the same selection. Passed inside `cd src && uv run --frozen pytest` (1025 passed).

### T2 Equivalent paths and fragment referrer

Repeated spellings of one path, an empty fragment, a percent-encoded fragment, and `-f` with a fragment-only reference publish one derived file. Check mode with `-f` publishes nothing. Passed in the same pytest run.

### T3 Distinct selections

Two files, two sections of one file, and a whole file with one of its sections each exit 2 without `-o` and publish nothing. The same selections with `-o -` or `-o combined.md` exit 0. Passed in the same pytest run.

### T4 Explicit destinations and check mode

`-o -` and `-o FILE` publish the combined bundle to stdout or that file. `-c` accepts those destinations and leaves no derived file. Passed in the same pytest run.

### T5 Source overlap

A derived path that names a captured source, including a deferred target, exits 2 in normal and check mode and leaves the existing file unchanged. Passed in the same pytest run.

### T6 Atomic publication

One `os.replace` publishes the derived file. A refused replace and a validation failure leave the existing file and no temporary sibling. A filename the filesystem rejects exits 3 with `E_PUBLICATION_FAILED`. Passed in the same pytest run.

### T7 Installed wheel

`make smoke` built and installed the wheel, then published `guide.bundle.md` and `guide__guide.bundle.md`, refused a combined selection without `-o`, and left an unwritable destination in place with no temporary file. Passed.

### T8 Pinned baseline

`make corpus` compared 253 fixtures with their pinned stdout. 253 passed, 0 failed. The runner requests stdout with `-o -`.

### T9 Full check

`make check` passed: lock, lint, format, mypy, 1025 pytest tests, 614 harness tests, corpus, smoke, layout, tables, links (51 documents), vocabulary, invocation (27 statements), conformance and independence.

## Delivery

[Pull request 230](https://github.com/m2ux/prosiform/pull/230) merged into `i01/e06/main` as `e1225559a4236c64efc17051f45791d45dde15dc`. That merge's tree is the tested tree of `ff10886de3bb4aa3f91454ad8b2fb5b53eb2e6f2`. AC14, AC15 and AC16 are ticked, and W09 is Done on issue 218. Review 222 cites the merge and remains a draft. W10 and W11 remain open.

## Change List

No plan change was applied. No plan change is held.
