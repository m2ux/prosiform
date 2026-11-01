# W01 Validation

Evidence for each check the [W01 work item](w01.md) names, run in the task worktree at head `63c24ab8` on branch `i07/e01/w01-name-the-member-s`.

## T1 Absorbed-member fixture declares the member's chain

- **Procedure.**  `make corpus` (inside `make check`) with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.
- **Fixture.**  `fixtures/dispatch/a-dispatch-in-an-absorbed-member-title-is-refused` declares `chain = ["guide.md", "checklist-⇉-publish.md"]` on its `E_UNSUPPORTED_CONSTRUCT` diagnostic.
- **Observation.**  The build reports `"chain": ["guide.md", "checklist-⇉-publish.md"]` for the dispatch in `checklist-⇉-publish.md:7`; the corpus holds over all 384 fixtures. Before the change the same run reported `["guide.md"]`, the group's first member.

## T2 Overflow in a later member names that member's chain

- **Procedure.**  `uv run --frozen pytest tests/test_cli.py -k later_member` in `src/`.
- **Test.**  `test_a_heading_overflowing_in_a_later_member_names_that_member_s_chain`: `a.md` and `b.md` join group `Notes`, and `b.md` carries a heading reaching level 7.
- **Observation.**  Passes with the change, reporting `source = "b.md"` and `chain = ["guide.md", "b.md"]`. Fails against the unchanged `src/prosiform/cli.py`, which reports the chain of `a.md`.

## T3 Repository checks

- **Procedure.**  `make check` with `PROSIFORM_BUILD` set to the worktree build.
- **Observation.**  Exit 0: unit tests, corpus, invocation, conformance, independence and mock-scenario checks all pass.
