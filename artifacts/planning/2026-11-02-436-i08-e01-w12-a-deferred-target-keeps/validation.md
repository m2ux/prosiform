# Validation

The checks [W12](w12.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `f0c91214` on `i08/e01/w12-a-deferred-target-keeps` |
| Epic base | `44f5df83` on `i08/e01/main` |
| Design pin | unchanged; *Presets — One document under several selections* already states this row |

## T1 Unit Tests

`uv run --project src --frozen pytest src/tests/test_cli.py` at `f0c91214`: every test passes, among them `test_two_sections_reaching_one_document_each_select_its_presets` (`rules.md` under `Reviews` and `Drafts`, its content twice), `test_a_document_a_later_round_reaches_again_takes_that_selection` (`notes.md`'s `## Draft`, discovered in the second round, puts `Draft` in force), `test_two_sections_selecting_two_depths_for_one_group_conflict` (`E_GROUP_DEPTH_CONFLICT`) and `test_a_reference_selecting_again_counts_no_target` (`-T 2` publishes). All four fail at `44f5df83`, where the second link is dropped.

Result: pass.

## T2 Corpus Fixtures

`make corpus` at `f0c91214` reports `inclusion/one-document-two-presets` as `pass`. Before the source change the build placed `rules.md` under `Reviews` alone.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `f0c91214`, exit 0. The unit suite reported 1600 passed and the harness 1149 passed. The corpus reported 424 fixtures, 424 pass, 0 fail, 0 awaited. `make conformance` cites *Presets — One document under several selections* by 1 fixture; `make independence` finds every shaped term one the contract names.

Result: pass.

## Findings

- **The traversal dropped a second link to a carried target.** It now carries one reference per target and title, so each link's selection is in force; every existing fixture holds unchanged.
