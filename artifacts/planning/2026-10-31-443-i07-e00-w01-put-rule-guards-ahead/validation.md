# Validation — W01 Put Rule Guards Ahead of the Corpus

> Evidence · 2026-10-31

Every case below was run in the worktree `.worktrees/i07/e00/w01-put-rule-guards-ahead`, at branch `i07/e00/w01-put-rule-guards-ahead`, cut from `i07/e00/main` at `23882b7d`.

The injected break in each case is a single edit to `example/work-planner/modes/plan-mode.md`, reverted with `git checkout --` before the next case. The build under test is named `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## Baseline, before any change

Both guards pass over the unmodified tree, so a case that reports the rule only after the repair would prove nothing. The baseline is recorded first.

| Command | Result |
| --- | --- |
| `python3 checks/steps.py` | `step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections`, exit 0 |
| `python3 checks/authoring.py` | `authoring check: 0 finding(s)`, exit 0 |
| `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . checks/tests` | 781 passed |
| `uv run --project src --frozen python checks/corpus.py` | `corpus check: 349 fixture(s), 349 pass, 0 fail, 0 awaited, 0 unexpected pass` |
| `cd src && uv run --frozen pytest -q` | 1295 passed, 13 errors (`test_linked_bootstrap`, network) |

## Finding 3 — `make steps` runs last, so `corpus` reports moved bundle bytes

**The break.** In `example/work-planner/modes/plan-mode.md`, the bullet under `### 2. Prepare the Planning Record` became a column-0 numbered list item, which the step convention forbids.

**Before the fix, `make steps` on its own** reported the rule and exited nonzero:

```
FAIL example/work-planner/modes/plan-mode.md:23 — a numbered list item; write each step as an 'N. Action' heading one level below its procedure

step check: 1 place(s) breaking the step convention
```

**Before the fix, `make corpus` reported the symptom instead** — the moved bundle bytes, naming no file and no rule:

```
usage-example/a-procedure-and-everything-it-reaches: fail
  expected.bundles: modes_plan-mode.bundle.md: the bytes differ
    185756 bytes expected, 185758 produced
    first difference at byte 1301, expected line 25 column 1
    expected b're the Planning Record\n\n- For an initiative, epi'
    produced b're the Planning Record\n\n1. For an initiative, ep'
corpus check: 349 fixture(s), 348 pass, 1 fail, 0 awaited, 0 unexpected pass
```

**The defect.** `check:` named `corpus` before `steps`, so the first failure a broken tree met was the byte difference. The guard that names the file and the rule ran last and never ran at all.

**After the fix**, with the same break in place, `make check` stops at the guard:

```
python3 checks/steps.py
FAIL example/work-planner/modes/plan-mode.md:23 — a numbered list item; write each step as an 'N. Action' heading one level below its procedure

step check: 1 place(s) breaking the step convention
make: *** [Makefile:131: steps] Error 1
```

## Finding 11 — `make test` precedes `authoring`, so a link break reports a target-not-found code

**The break.** In the same document, `[Rules](../rules.md)` became `[Rules](rules.md)`, a path that resolves from the root the front matter declares rather than from the file.

**Before the fix, `make authoring` on its own** named the file and the rule:

```
example/work-planner/modes/plan-mode.md:9 — File-relative links: rules.md resolves from the declared root, not from the file

authoring check: 1 finding(s)
```

**Before the fix, the build's own example-reading suite reported the symptom instead** — the build's target-not-found code, naming no rule:

```
tests/test_handoff_round_trip.py:209: AssertionError
E   AssertionError: [{'severity': 'error', 'message': "the reference 'rules.md' names no document under the allowed source root", 'code': 'E_TARGET_NOT_FOUND', 'reference': 'rules.md', ...}]
FAILED tests/test_handoff_round_trip.py::test_each_handoff_the_example_publishes_is_followed
FAILED tests/test_handoff_round_trip.py::test_a_mode_bundle_carries_the_dispatch_protocol_once
```

**The defect.** `check:` named `test` (and `corpus`) before `authoring`, so the first failure a tree with a broken link met was `E_TARGET_NOT_FOUND` from the bundling target. The guard naming the file and the rule ran after it, and where `test` failed, never ran.

**After the fix**, with the same break in place, `make check` stops at the guard and names the file and the rule:

```
python3 checks/authoring.py
  example/work-planner/modes/plan-mode.md:9 — File-relative links: rules.md resolves from the declared root, not from the file

authoring check: 1 finding(s)
make: *** [Makefile:134: authoring] Error 1
```

## The order test

`checks/tests/test_check_order.py` reads the `Makefile` and holds every guard ahead of every bundling target.

**Before the fix** it failed on the repository's own `Makefile`:

```
E   AssertionError: check names test ahead of steps, so a broken step convention is reported as the bundle bytes that moved
E   assert 16 < 4
FAILED checks/tests/test_check_order.py::test_the_makefile_names_every_guard_ahead_of_every_bundling_target
```

**After the fix** both cases pass:

```
checks/tests/test_check_order.py ..                                       [100%]
```

The second case reads a `Makefile` written for the test in both orders, so the reading is held independently of the repository's own file.

## Every check run on the branch head

`make check` was run twice over the repaired tree. Under the sandbox the four static checks pass, then both guards run and pass, and the run stops inside `test` at `test_linked_bootstrap`, which needs network for `uv build`:

```
9:python3 checks/steps.py
10:step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections
11:python3 checks/authoring.py
12:authoring check: 59 document(s) under example/work-planner/
39:authoring check: 0 finding(s)
700:make: *** [Makefile:86: test] Error 1
```

That is the sandbox limitation the brief names, not this change's defect: it reproduces identically on a clean checkout of `origin/i07/e00/main`.

Run unsandboxed, where `test_linked_bootstrap`, `smoke` and `links` reach the network, `make check` passed in full with exit status 0 in 123 seconds, ending at `independence check: every shaped term of every fixture declaration and every report entry is one the contract names`.

| Target | Result | Note |
| --- | --- | --- |
| `lock-check` | pass | |
| `lint` | pass | `All checks passed!` |
| `format-check` | pass | 203 files already formatted |
| `typecheck` | pass | no issues in 80 source files |
| `steps` | pass | runs ahead of `test` |
| `authoring` | pass | runs ahead of `test` |
| `test` | pass unsandboxed; 1295 passed, 13 errors sandboxed | the 13 are `test_linked_bootstrap`'s network need |
| `harness` | 990 passed | `checks/tests` (781) and `evals/diagram-following` |
| `corpus` | 349 fixtures, 349 pass | |
| `smoke` | pass | unsandboxed; needs network for the wheel |
| `layout` | pass | |
| `tables` | pass | 21 commands and 8 declarations |
| `links` | pass | every reference in 237 documents resolved |
| `vocabulary` | pass | 44 contract terms |
| `invocation` | pass | |
| `conformance` | pass | 303 clauses, 0 codes unreported |
| `independence` | pass | every shaped term named by the contract |

`test`, `smoke` and `links` were run unsandboxed because each needs network; the rest under the sandbox.

## No neighbouring behaviour moved

| Observation | Result |
| --- | --- |
| `make -n check` after the repair | `lock-check lint format-check typecheck steps authoring test harness corpus smoke layout tables links vocabulary invocation conformance independence` |
| The status a broken tree meets | The guard, not the bundling target, in both injected cases |
| Checks reading the example | `steps` and `authoring` are the only guards. `harness` reads the example directly but bundles nothing, so it stays after `test` and now follows both guards |
| The example itself | Unmodified; every injected break reverted with `git checkout --` |
