# Validation

The checks this row ran, the revision they ran against, and what each observed.

The revision is `0735852` on `i00/e12/w06-root-confinement-on-entry`, cut from `i00/e12/main` at `ea4227c`. Every check below ran from the unit's worktree, with `PROSIFORM_BUILD` naming this checkout's build where the check reads one.

## Build Suite

`make test` — the build's own suite over `access`, `bundle`, `candidate`, `cli`, `closure`, `delivery`, `diagnostics`, `grouping`, `profile`, `rewrite` and `source`.

626 tests passed. Four of them observe the criterion directly:

- `test_an_entry_the_root_cannot_contain_is_an_input_failure` runs the command for each spelling that names a document the root cannot contain — a parent segment above the root, a root-relative path, a drive path, and an authority — and observes one `E_SOURCE_OUTSIDE_ROOT` diagnostic and the input-failure status for each.
- `test_a_root_relative_reference_inside_a_source_is_emitted_as_authored` writes `/rules.md` inside a source beside a `rules.md` the root holds, and observes a successful run whose bundle carries the link as authored and carries none of the document's body.
- `test_a_drive_path_inside_a_source_is_emitted_as_authored` observes the same for `C:/rules.md`.
- `test_a_reference_outside_the_root_is_emitted_as_authored` is the parent-segment half, which the preceding row left standing and this one did not change.

The suite ran again after the corpus fixtures landed, with the same result.

## Corpus

`make corpus` — every fixture in the tree, against this checkout's build.

206 fixtures, 204 pass, 0 fail, 2 awaited, 0 unexpected pass. The two awaited are `reference/a-link-inside-image-alternative-content` and `grouping/a-rule-matching-no-document-in-the-closure`, which name the work that delivers them and were awaited before this row.

The root-confinement family states both halves of the boundary:

| Fixture | What it observed |
| --- | --- |
| `confinement/a-parent-segment-above-the-root` | The entry `../outside.md` fails with `E_SOURCE_OUTSIDE_ROOT`, publishes nothing, and the document beside the root is never read. |
| `confinement/a-root-relative-reference-inside-a-source` | A source's `/rules.md` bundles successfully, the link is carried as authored, and the `rules.md` the root holds joins no group. |
| `confinement/a-drive-path-inside-a-source` | A source's `C:/rules.md` bundles successfully and is carried as authored rather than read as a scheme of one letter. |
| `normalization/root-escape` | A source's parent-segment reference above the root is carried as authored, which the preceding row delivered. |
| `normalization/root-relative-entry-reference`, `normalization/a-drive-path`, `normalization/a-protocol-relative-url` | Each spelling fails as an entry reference with `E_SOURCE_OUTSIDE_ROOT`. |

The baseline before this row's changes was 204 fixtures, 202 pass, 0 fail, 2 awaited, so the two fixtures this row adds are the whole of the difference and no existing fixture changed verdict.

## Repository Checks

Each ran from the unit's worktree and passed:

`make lint`, `make format-check`, `make typecheck`, `make lock-check`, `make layout`, `make tables`, `make links --online`, `make vocabulary`, `make invocation`, `make smoke`.

The vocabulary check reads the design from `origin/engineering` and reported 34 contract terms, each defined in `docs/glossary.md` and carried across 23 sources. The invocation check held 27 statements of the documented invocation against the build's own help output.

## Harness

`make harness` — the corpus harness's own tests over the schema, the runner, the corpus run, the documents, the links and the catalogue.

381 passed, 1 failed. The failure is `checks/tests/test_catalogue.py::test_a_catalogue_is_the_codes_the_design_declares[error-E_]`, which holds the manifest schema's error catalogue to the codes the design declares. The schema enumerates `E_MARKED_RESOURCE` and `E_SELF_REFERENCE`, which [D59](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) withdrew from the design.

This failure is the epic base's, not this row's. It was observed on `ea4227c` before any change here, it is unchanged by every change here, and the row retiring those two codes is W04 and W05 of this epic, which the brief for this row names as work to leave alone. The harness's remaining 381 tests, which include every test over the manifest schema, the runner and the corpus run that this row's fixtures pass through, hold.
