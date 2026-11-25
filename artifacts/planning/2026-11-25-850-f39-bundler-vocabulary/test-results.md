# Test Results

Validation observed at `f39-bundler-vocabulary` head 20bd147152b8ee9f2f68e299a35bee7a225ba0c8, based on `main` at 684437c06, with the design pinned at c394f23056ad69400277b008fdd2ccd8841ded5e.

## Vocabulary Search

`git grep -i compil` over the tree finds three things and nothing else:

- calls to `re.compile`;
- the `compile` and `compiler` rows of the avoided-terms table in `docs/glossary.md`;
- the licence text in `LICENSE`.

## Build Tests

`make test`: 2,323 passed. `make lint`, `make format-check`, `make typecheck` and `make lock-check` pass.

## Fixture Corpus

`make corpus` with the build under test: 708 fixtures, 708 pass.

The corpus of `main` at 684437c06, run against this build: 706 pass, 2 fail. Both, `cli/informational-usage-response` and `cli/informational-long-usage-response`, declare the help text's exit-status line as it read, "compilation, validation, or informational". No bundle's bytes differ. A previous corpus that fails moves the contract minor, so the release is 0.35.0.

The corpus of `contract/v0.34.0`, run against this build: 697 pass, 11 fail. Nine of the eleven pass in the corpus of `main`, so they come from changes `main` took after that tag; the other two are the help-text fixtures above.

## Source and Documentation

`make smoke`, `make layout`, `make tables`, `make links` (445 documents), `make vocabulary` (53 contract terms, read from the design at c394f23056ad), `make invocation` (29 statements), `make conformance` and `make independence` pass. `make examples` re-rendered the images under `docs/images`.

## Checks Harness

`make harness`: 1,154 passed, 1 failed. The failure, `checks/tests/test_authoring.py::test_active_guidance_recommends_hyphens_rather_than_underscores`, fails identically on `main` at 684437c06: `README.md` there lacks the sentence recommending hyphens. It stops `make check` at `harness`, so every later target was run with `make -k check`.

## Eval Harness

`make eval-harness`: 819 passed, 39 failed. `main` at 684437c06 gives 819 passed, 39 failed, and the failing tests are the same 39 once their names are read in the new vocabulary. No paid agent session ran.

## Recorded Figures

Every number in `baseline.json`, `agent-pick.json`, `dispatch-brief.json` and `mvp-proof.json` equals its value at 684437c06, read in document order. The records differ in form names, class names, folder names and disposition wording alone.
