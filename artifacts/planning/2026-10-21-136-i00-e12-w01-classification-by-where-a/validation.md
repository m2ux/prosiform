# Validation

The checks this row ran, the revision they ran against, and what each observed.

## Revision

- **Branch.** `i00/e12/w01-classification-by-where-a`, cut from `i00/e12/main` at `9ffb716`.
- **Build under test.** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`, the build the change produces, reached through its console entry point.
- **Commands.** Each is a named target of the repository's `Makefile`, run from the repository root.

## Unit suite

`make test` — 621 tests, all passing. 603 of them stood before this row; the 18 added observe the classification.

- **AC1.** `test_a_reference_resolving_under_the_root_is_a_dependency` and `test_a_fragment_of_its_own_document_is_a_dependency` hold `closure.bundled()` to the identity a reference names. `test_a_reference_under_the_root_is_bundled_and_rewritten` and `test_a_reference_to_a_section_under_the_root_carries_that_section` run the command and read the bundle: the target's content is present and the link carries the destination the bundle assigned it.
- **AC2.** `test_a_reference_the_bundle_compiles_none_of_names_no_dependency` holds the classifier to the seven shapes that are not dependencies. `test_a_reference_outside_the_root_is_emitted_as_authored` runs the command against a document above the root carrying raw HTML, which the profile refuses in selected content: the run succeeds, the bundle carries the link as authored, and the refused construct is nowhere in it, so the target was never opened.
- **The mark decides nothing.** `test_a_mark_on_a_reference_outside_the_root_changes_nothing` reads the mark back out of the bundle, because a reference leaving the root is text and a mark on one changes nothing that was going to happen to it.
- **The emission.** `test_a_compiled_link_is_written_to_its_destination` pairs each link a token carries with the destination the bundle assigned it, and holds a link assigned none to the bytes its author wrote.

## Corpus

`make corpus` — 204 fixtures, 202 passing, 0 failing, 2 awaiting later work, 0 passing while awaiting it. The two awaiting fixtures are the ones the corpus already carried: `reference/a-link-inside-image-alternative-content` awaits `I00:E11:W10` and `grouping/a-rule-matching-no-document-in-the-closure` awaits `I00:E11:W14`.

- **AC1.** `reference/a-document-under-the-root-is-a-dependency` declares a source whose two references name a document and a section under the root, with no mark written. The bundle carries both targets and rewrites each link to the destination its target took.
- **AC2.** `reference/a-document-outside-the-root-is-text` declares a source citing a document above the root which carries raw HTML. The run succeeds, the bundle carries `[the shared guidelines](../guidelines.md)` as authored, and the cited document contributes nothing.
- **The same rule from three further angles.** `citation/a-reference-above-the-root`, `citation/a-marked-reference-above-the-root` and `normalization/root-escape` each declare a reference leaving the root as text; the second of them reads the mark back out of the published bundle.
- **The corpus before the build.** Every fixture that selected a dependency with the mark declares it by position, and each run against the build produced the bytes its manifest declares.

## Repository checks

Each ran against the same revision.

| Command | Result |
| --- | --- |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | no issues in 44 source files |
| `make lock-check` | the lockfile describes the declared dependencies |
| `make layout` | 3 trees present |
| `make tables` | 14 commands and 7 declarations, each declared and named |
| `make vocabulary` | 34 contract terms, every one defined in the glossary |
| `make links` | every reference in 12 documents resolved |
| `make invocation` | 27 statements of the documented invocation held to the build |
| `make smoke` | the wheel installs and bundles from a source root, outside the repository |

## The catalogue check

`make harness` reports 379 passing and one failing:

```text
FAILED checks/tests/test_catalogue.py::test_a_catalogue_is_the_codes_the_design_declares[error-E_]
  Extra items in the left set: 'E_SELF_REFERENCE', 'E_MARKED_RESOURCE'
```

**It fails on the base this row was cut from, before any change of this row.** The check derives the manifest schema's error catalogue from the design on the `engineering` branch, and [D59](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) withdrew both codes from the design when it landed on 2026-10-21. The schema still enumerates them because the build still raises them, which is the behaviour this row keeps: `E_MARKED_RESOURCE` is retired by `W04` with the rule that emits a resource wherever it resolves, and `E_SELF_REFERENCE` by `W05` with the rule that rewrites a self reference. The check turns green on the row that removes the code the design no longer declares.

Reproduced on the base: `make harness` at `9ffb716` with no change of this row applied reports `1 failed, 378 passed`.

The published runs say the same thing. Commit `9ffb716` is the head of both `main` and `i00/e12/main`, and the workflow that runs `make check` over it
[succeeded on `main` on 2026-10-20](https://github.com/m2ux/prosiform/actions?query=branch%3Amain) and
[failed on `i00/e12/main` on 2026-10-21](https://github.com/m2ux/prosiform/actions?query=branch%3Ai00%2Fe12%2Fmain).
Nothing in the tree differs between them: the design on `engineering`, which the check reads, is what changed. This branch's own run fails on that one case and nothing else.
