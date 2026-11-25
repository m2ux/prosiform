# Test Results

Validation observed at `f39-bundler-vocabulary` head 6b8d5a6cb1edaabb8f7e86a4f6e459b19ad63073, based on `main` at 684437c06, with the design pinned at c394f23056ad69400277b008fdd2ccd8841ded5e.

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

`make harness`: 1,155 passed. `make check` exits 0, every target passing in order.

On `main` at 684437c06 the harness fails `test_active_guidance_recommends_hyphens_rather_than_underscores`, because `README.md` there states its usage without the sentence recommending hyphens. The branch's last commit holds that recommendation to the invocation guide, which owns it.

## Eval Harness

`make eval-harness`, at 20bd14715, which the last commit leaves untouched: 819 passed, 39 failed. `main` at 684437c06 gives 819 passed, 39 failed, and the failing tests are the same 39 once their names are read in the new vocabulary. No paid agent session ran.

## Recorded Figures

Every number in `baseline.json`, `agent-pick.json`, `dispatch-brief.json` and `mvp-proof.json` equals its value at 684437c06, read in document order. The records differ in form names, class names, folder names and disposition wording alone.
