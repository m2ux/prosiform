# Validation

Evidence for each check the [work item](w04.md) names, run in the unit's worktree at c26287ed with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 unit tests

`make test` passes (1,400 tests).

- `test_a_link_naming_no_document_is_text` (`test_cli.py`, `test_closure.py`): an unmarked link to a missing document is emitted as authored, no diagnostic (AC7).
- `test_an_operator_naming_no_document_is_a_missing_target` for `¬`, `⇉` and `⫽`: `E_TARGET_NOT_FOUND` at the link, no bundle (AC8).
- `test_an_operator_naming_a_silent_document_is_refused`: `E_UNSUPPORTED_CONSTRUCT` naming the missing declaration.
- `test_a_fragment_only_link_naming_no_heading_is_a_missing_target`: `E_TARGET_NOT_FOUND` naming `#nowhere` (AC8).
- `test_an_entry_naming_a_silent_document_fails_before_any_source_is_read` and `test_an_entry_naming_no_document_is_a_missing_target` (AC15).

## T2 corpus

`make corpus`: 383 fixtures, 383 pass, 0 fail, 0 awaited. `inclusion/a-link-naming-no-document-is-text` (AC7), `inclusion/operators-keep-the-absent-target-refusal` and `inclusion/a-fragment-naming-no-heading` (AC8), `inclusion/an-entry-naming-a-silent-document` (AC15) pass.

## T3 full check

`make check` exits 0 before opening, and the epic base held no newer commit before merging; CI on c26287ed passes.
