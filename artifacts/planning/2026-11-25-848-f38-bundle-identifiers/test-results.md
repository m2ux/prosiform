# F38 Verification

## Reviewed Revision

- Head: 552230b96269ed26511a9652d16571d8aae07655
- Integrated main: 86fcbad07cf279db2b2886265b5404c038b4d37e
- Target at review: 6f103e34db5a814331f9882c7e01330cd2f3aa5a, main
- The subsequent target commit changes only the README description. The PR contains no README edit. Remote CI checks the PR integration.
- Build: pf 0.34.0 with the unreleased F38 change

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Complete source suite | 2,330 passed | [make check](named-final-check.log) |
| Check harness | 1,155 passed | [make check](named-final-check.log) |
| Exact-output corpus | 708 passed, zero failed or awaited | [make check](named-final-check.log) |
| Installed-wheel smoke | Passed from an independent working directory | [make check](named-final-check.log) |
| Lint, format, types | Passed; 513 formatted files and 103 typed source files | [make check](named-final-check.log) |
| Layout, tables, online links, vocabulary, invocation, conformance and independence | Passed | [make check](named-final-check.log) |
| Fixture/example diff audit | 3,033 text files inspected; 60 renamed paths and 63 rewritten bodies; only specified naming changes | [audit](named-fixture-audit.json) |
| GitHub CI | Success on the reviewed head | [Checks](https://github.com/m2ux/prosiform/actions/runs/45578186008) |
| Downstream classifier compilation | 64 expected harness/seam outcomes passed under both harnesses | [consumer summary](consumer-validation.md) |

## Criterion Evidence

- **AC1:** Exact filenames and encoded links are checked for one and multiple presets, fragments, dispatches, Unicode, spaces, slashes, percent signs and literal plus signs. The [specimen](named-specimen/entries.json) retains actual files.
- **AC2:** Existing equivalence tests retain canonical declaration spelling and ignore tag order, case, repetition and unknown names. A literal a+b preset and a selection of a and b publish distinct files.
- **AC3:** A real collision between task.md selected under checks and task-checks.md returns E_PUBLICATION_FAILED. The earlier published file set remains byte-identical. Existing validation-only and dispatch collision checks also pass.
- **AC4:** The full check uses this head. The exact-output corpus, lifecycle example, diagram paths, installed wheel and documentation agree.

## Method And Limits

The naming rule changes once in selection_name. Existing entry-folder naming, dispatch link encoding and publication checks consume it. Each preset is escaped before joining; the existing link encoder then encodes the whole filename as a URL destination. Canonical selection identity and publication behavior remain their existing owners.

The final change is reviewed against the integrated target, including affected callers and all fixture/example transformations. The corpus and consumer matrix establish compilation behavior; this task runs no fresh native-agent evaluation and makes no performance claim. The existing conformance report retains its documented coverage gaps. Long names still face the existing filesystem-length refusal.

## Retained Earlier Attempts

- [Hash-candidate verification](hash-candidate-test-results.md) retains the twelve- and eight-character evidence at its original pins. Those builds remain frozen for earlier downstream evaluations.
- [Earlier CI failure](eight-digit-ci-failure.log) identifies the README authoring assertion; integrated F39 fixes its ownership on main.
- [Initial focused run](named-initial-focused.log) and [initial complete run](named-initial-check-failures.log) retain stale URL assertions. Corrected assertions distinguish filesystem names from encoded destinations.
- [Pre-integration complete check](named-pre-integration-check.log) passed before current main was integrated. Final acceptance uses named-final-check.log.
