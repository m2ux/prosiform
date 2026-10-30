# Handoff Round-Trip: Delivery Evidence

**Pull request:** [#259](https://github.com/m2ux/prosiform/pull/259) — `i01/e09/w04-handoff-round-trip` → `i01/e09/main`
**Task:** [#250](https://github.com/m2ux/prosiform/issues/250)
**Commit:** `53dc70ad` — Hold the published destination by compiling it

The suite copies `example/work-tracker`, bundles a mode, reads the destinations the bundle published, and compiles each of them in a second run from the same working directory. Each second bundle is compared whole.

## What makes it a round trip

The destination is taken from the first bundle and never restated. A test that wrote `../artifacts/handoff.md#selection` into the second run would assert that one authoring string compiles twice; that string is what the mode linked to and is reachable only because the mode sits one directory down. The destination the bundle published is `artifacts/handoff.md#selection`, which is the path a later run follows from the invocation directory.

Each scenario therefore reaches its artifact by a parent-relative path and compiles the working-directory-relative path the bundle emitted. Every destination is additionally held to three properties before the second run, so an emission that relocates or truncates the path fails at the parse:

- it carries no parent segment,
- it names a document of the copy, once its escapes are decoded,
- it carries a fragment, so the selected section survives.

## The rows

| Test | AC | Destination obtained by | Second bundle compared |
| --- | --- | --- | --- |
| `test_a_dispatched_destination_compiles` | AC1 | `[» Selection](artifacts/handoff.md#selection)` parsed from the first bundle | whole document, `## Selection` and its marker |
| `test_a_deferred_destination_compiles` | AC2 | `[Selection](artifacts/handoff.md#selection)` parsed from the first bundle, label carrying no mark | whole document, `## Selection` and its marker |
| `test_an_escaped_destination_compiles` | AC3 | `artifacts/caf%C3%A9.md#held` parsed from the first bundle | whole document, `## Held` and its marker |
| `test_both_destinations_of_one_bundle_compile` | AC4 | both links parsed from one bundle | each destination's own whole document |
| `test_a_declared_dispatch_text_reaches_the_entry_line` | AC5 | the dispatch text read from the copy's `SKILL.md` | the bundle's entry line ends with that text, once |
| `test_a_published_bundle_offered_as_input_is_refused` | AC6 | the bundle the run wrote to `bundle.md` | `E_GENERATED_INPUT` at the line the declaration occupies |

AC7 is the suite's own registration: it lives in `src/tests/`, so `make test` collects it, and it reads no environment variable.

## The invocation route

`pf`, resolved by name through `shutil.which`, from the environment `make test` runs in. `src/tests/test_delivery.py` takes that same route for the same reason: the console script is what a caller reaches, and `uv run --frozen pytest` puts the project's environment on the path. `sys.executable -m prosiform.cli` was the alternative and was not taken, because `prosiform.cli` declares no `__main__` guard that runs `main()` — `python -m prosiform.cli` exits 0 having published nothing. `test_linked_bootstrap.py` installs a wheel because it asserts an installed command; that is a different claim from this one.

## Sensitivity

Each mutation was applied to the build, the suite run, and the build restored.

| Mutation | Rows that failed |
| --- | --- |
| Publish the destination under a prefix segment (`elsewhere/…`) | the four round-trip rows |
| Drop the fragment from the published destination | the four round-trip rows |
| Withhold the declared dispatch text from the entry line | the dispatch-emission row |
| Publish the path with no URI escaping | the escaped-destination row |

## Checks against the baseline

| Check | Baseline | Result |
| --- | --- | --- |
| `make test` | 1093 passed | 1099 passed |
| `make corpus` | 260 fixtures, 260 pass, 0 fail | unchanged |
| `make harness` | 626 passed | 626 passed |
| `make lint` | clean | clean |
| `make format-check` | clean | clean |
| `make typecheck` | clean | clean |
| `make smoke` | pass | pass |
| `make layout`, `tables`, `links`, `vocabulary` | pass | pass |
| `make invocation`, `conformance`, `independence` | pass | pass |
| `make check` | exit 0 | exit 0 |

`make conformance` still reports `File-owned invocation conformance cases — Deferred handoff: 0 fixture(s)`. That line counts corpus fixtures, and the corpus runs one invocation per fixture; the round-trip is two runs with a parse between them, which is why it is a suite rather than a fixture. The `File-owned invocation conformance cases — Deferred handoff` clause listing names the four deferral fixtures that reach the clause's emitted form, unchanged.
