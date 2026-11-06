# W06+W07 Validation

Source head: `cd325d5c3f6c71ef8890c8910adad85cc2b7895c` on `i10/e07/w06-compilation-schedules-distinct-selection`, based on `6578295a1bd40899ab4286a8185203451e159554`.

The runtime design is pinned at [`795bbfb67c66b02193f0313138f59f18aa6c5274`](https://github.com/m2ux/prosiform/blob/795bbfb67c66b02193f0313138f59f18aa6c5274/artifacts/planning/2026-10-17-prosiform-v1/design.md).

The final exact-head full gate **passes**. Its complete output is [make-check.log](make-check.log). Plain `git push` publishes that exact head, the remote tracking ref matches, and the source worktree is clean.

## Distinct Bundle Selections

AC12: real compilations dispatch the same document with different preset-owned substitutions and observe separate files with distinct selected bodies. Scheduling uses canonical document, fragment and matched declared preset names. The source test also selects different fragments of one substitute file and checks both contents and substitution diagnostics.

Instruments: `src/tests/test_dispatch_variants.py`, `src/tests/test_variant_integrity.py` and `dispatch/two-preset-selections-of-one-target`.

## Equivalent Requests And Names

AC13: repeated, reordered, case-folded names, empty tokens, empty whole-document fragments, `default` and unknown names share one effective key. A real-run observation records one target compilation, checks all incoming links and compares the contract's exact `13c9f40c...` filename for checks plus draft. Reversed source occurrence order retains that name.

Instruments: `test_equivalent_requests_compile_once_under_the_contract_name`, `test_unmatched_and_default_requests_share_the_empty_effective_selection` and `dispatch/equivalent-preset-requests-share-one-parallel-member`.

## Variant Graphs And Budgets

AC14: graph and actual-run tests distinguish a sibling selection of the entry from a return to an equivalent entry selection. Distinct variants count as distinct depth hops; equivalent first-hop requests raise one warning, while distinct selections retain their own first warning locations. Dense graph cases terminate. File and output-byte budgets restart from each bundle's own closure rather than summing all variants.

Instruments: `src/tests/test_dispatch.py` and `src/tests/test_dispatch_variants.py`.

## Selected Dispatch Publication

AC15: each raw occurrence retains its tags and operator in provenance. Inline dispatches name their selected file. Parallel aliases share one member; distinct selections retain separate members. Body, heading-inline and H6 cases observe the actual published marks, headings, links and selected bodies. Candidate checks reject a map pointing at the other variant and a generated set listing the wrong variant twice.

The candidate's renderer-assigned heading identities distinguish repeated generated set headings. Source-section ambiguity rules do not resolve candidate headings. Captured conversion metadata supplies effective selection to both heading construction passes; unselected headings require no additional target capture, and an unplaced title dispatch retains its input refusal.

Instruments: `src/tests/test_dispatch_publication.py`, `src/tests/test_candidate.py`, `src/tests/test_variant_integrity.py`, the existing child-section set regression, and `dispatch/a-parallel-set-retains-distinct-preset-selections`.

## Collision Atomicity

AC16: injected equal filenames for distinct effective selections fail with `E_PUBLICATION_FAILED`, identify both selections and preserve a previous output set byte for byte. Normal/check modes and inline, parallel-body and heading-inline placements all run. A local name claim catches a collision before parallel aliasing can change candidate heading text; publication checks the complete run's names before writing anything.

Instrument: `test_distinct_variants_colliding_on_a_filename_preserve_the_previous_set`.

## Review Findings

- Variant substitutions selecting different fragments of one substitute file need separate declared-alternative records. The record retains both, while repeated references served by one declaration retain one warning. Used/unused pair checks also retain the declaring preset and alternative across bundle variants. Observing tests cover both cases.
- The initial full gate at `bf7f61592d569b213d03b53fe2b78d2221bc9191` found candidate set validation applying source ambiguity rules to repeated generated headings. The corrected candidate check follows renderer identities; the original failing log is retained in [make-check-bf7f61592.log](make-check-bf7f61592.log).
- Collision review covers the heading-inline case before candidate validation, including filename-based parallel aliasing. Every finding belongs to this unit and is fixed on this branch.

No criterion or required instrument is waived. No plan change or paid session is required. No open implementation finding remains. Coordinator publication, task PR, hosted checks, merge and tracker reconciliation follow this source handoff.

## Full Check

From the unit worktree:

```text
PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w06-compilation-schedules-distinct-selection/src --frozen pf' make check
```

Result: **passed at `cd325d5c3f6c71ef8890c8910adad85cc2b7895c`** — 1,850 source tests, 1,419 deterministic harness tests and 533 external-build corpus fixtures. Lint, formatting and strict typing (92 source files), installed-wheel smoke, layout, command/dependency tables, online links, vocabulary, invocation, design conformance and independence all pass. Conformance reports zero fixture declarations naming an absent clause. No source byte changes after this gate.

## Merged-Revision Replay

The coordinator can observe this unit at the merged revision with:

```text
uv run --project src --frozen pytest --config-file src/pyproject.toml src/tests/test_dispatch.py src/tests/test_dispatch_variants.py src/tests/test_dispatch_publication.py src/tests/test_variant_integrity.py src/tests/test_candidate.py
```
