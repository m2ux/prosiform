# Validation — I05:E05:W01

Measurements are local, on one developer machine, Python 3.13, `pf 0.15.0`. `main` is `3cf39019`; the fix is `04733a40`.

## Profile

`python -m cProfile` over `pf -d json -o <tmp> modes/deliver-mode.md`, run from `example/work-planner`.

| Function | `main` cumulative | Fix cumulative |
| --- | --- | --- |
| Whole run (profiled) | 54.4 s | 21.1 s |
| `candidate.validate` | 35.4 s | 2.0 s |
| `source.within` | 44.4 s over 1,042,116 calls | 13.3 s over the same calls |

The figures in the fix column are from the first change alone, before the `within()` loop; the loop takes the unprofiled run from 7.1 s to 4.9 s.

- **Root cause.** `validate()` compared each of the run's 5,340 carried regions by calling `carried`, `carrying`, `prose` and `code` with the whole reparsed bundle and the whole source document. Each call filtered every token by line, so the work grew with regions times tokens.
- **Not the dispatch-bundle work.** Before I05:E03 merged into the E04 base, `f4ad4b34` bundles the same entry in 27.5 to 28.2 s, against 18.8 to 19.1 s on `main`. The cost was always there; I05:E03 split it across nine bundles.
- **Remaining cost.** Dispatch placement and traversal read regions through `within()` against their source documents, which are small; they take most of the 4.9 s that remains.

## Timings

`pf -d json -o <tmp> <entry>` per mode of `example/work-planner`, wall clock.

| Mode | `f4ad4b34` | `main` | Fix |
| --- | --- | --- | --- |
| `advance-mode.md` | | 8.53 s | 2.53 s |
| `align-mode.md` | | 5.21 s | 1.41 s |
| `deliver-mode.md` | 27.51 s | 18.81 s | 5.11 s |
| `hoist-mode.md` | | 2.47 s | 0.82 s |
| `plan-mode.md` | | 10.91 s | 2.95 s |
| `propose-mode.md` | | 0.52 s | 0.27 s |
| `revise-mode.md` | | 0.11 s | 0.10 s |
| `standup-mode.md` | | 8.81 s | 2.55 s |
| `sync-mode.md` | 11.32 s | 7.60 s | 2.28 s |
| `understand-mode.md` | | 0.85 s | 0.38 s |

`pytest tests/test_handoff_round_trip.py --durations=3`:

| Test | `main` | Fix |
| --- | --- | --- |
| `test_each_handoff_the_example_publishes_is_followed` | 127.04 s | 18.21 s |
| `test_a_mode_bundle_carries_the_dispatch_protocol_once` | 10.99 s | 2.86 s |

The first test ran every mode twice on `main`; it runs each once with the fix. The 60-second limit is per `pf` run, and the costliest run is 5.1 s, so it holds a runner about twelve times slower. It is kept, since the run is not legitimately that long.

## Byte Identity

Every mode of `example/work-planner` bundled with `main`'s `pf` and with the fix's, each into its own folder, and compared with `diff -r`: identical, 35 bundle files across the ten modes, each run exiting 0.

## make check

`make check PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"` on `04733a40`, run with `uv run --frozen`: exit 0.

- `uv lock --check`, `ruff check`, `ruff format --check` and `mypy`: clean.
- `pytest` (build): 1,302 passed.
- `pytest` (harness): 731 passed.
- Corpus: 342 fixtures, 342 pass, 0 fail.
- Smoke, layout, tables, links, vocabulary, invocation, conformance and independence: pass.

## CI Runs

The Checks workflow on the pull request's head, five consecutive runs.

| Run | Result |
| --- | --- |
| Pending | |
