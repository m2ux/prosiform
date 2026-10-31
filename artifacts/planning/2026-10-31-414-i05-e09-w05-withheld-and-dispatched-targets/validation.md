# Validation — W05 Withheld and Dispatched Targets

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w05-withheld-and-dispatched-targets` on branch `i05/e09/w05-withheld-and-dispatched-targets`, at commit `f7900aff`. The build under test was named by `PROSIFORM_BUILD` as `src/.venv/bin/pf` in the worktree itself.

## T1 — The corpus passes on the branch

**Ran:** `python3 checks/corpus.py` with `PROSIFORM_BUILD` naming the worktree's own build.

**Observed:** exit `0`, `corpus check: 367 fixture(s), 367 pass, 0 fail, 0 awaited, 0 unexpected pass`, including `mock/a-deferred-target-is-redirected`.

## T2 — The unit cases hold the change

**Ran:** `pytest src/tests/test_mock.py` against the branch, then against the same tree with `closure.py` reverted to `origin/i05/e09/main`.

**Observed:** the branch passes. Reverted, three cases fail:

- `test_a_deferred_target_is_redirected_to_the_substitute`
- `test_a_deferred_destination_publishes_the_section_the_substitution_names`
- `test_the_candidate_comparison_reads_the_same_substitute`

The change is therefore held by the unit suite.

## T3 — The corpus fixture does not discriminate, stated plainly

**Ran:** `python3 checks/corpus.py` with `closure.py` reverted to `origin/i05/e09/main`.

**Observed:** exit `0`, `367 fixture(s), 367 pass`. **`mock/a-deferred-target-is-redirected` passes with and without the change.**

That is a weakness in the evidence, not a defect in the code. The fixture exercises a **document** key, which the design says keeps the section the reference named — so the authored fragment and the substitute's fragment coincide, and the old `components(text).fragment` line returns the right answer by accident. The behaviour this commit changes is the **section** key's, where the two fragments differ, and its effect is a second run rather than a bundle this run publishes — which is why the epic's `fixtures.md` places that case in the unit suite.

The fixture still earns its place: it pins the destination a deferred link publishes for a document key, which nothing else states. But no corpus fixture currently discriminates W05's change, and a reader comparing fixture counts would not know that. Recorded here so the epic review can decide whether a section-key corpus fixture is worth adding.

## T4 — The change

`closure.rebased` now publishes `found.fragment` — the fragment of the reference the mapping resolved — when there is one, before falling back to the fragment the author wrote. The docstring states the rule: a section key redirects the section with the document, a document key keeps the section the reference named, and a target resolving to no section publishes the authored fragment.
