# F38 Verification

- **Source suite:** all 2,324 collected cases pass at b8c4fb123bc8ffac151408c49ac54c4a38d3ad55, including installed-wheel bootstrap coverage. Initial wheel setup inside bubblewrap could not write its dependency cache; the complete passing run uses host access for that package-install boundary.
- **Corpus:** 708 fixtures pass, zero fail or awaited. Expected preset qualifiers, filenames and rewritten links agree with the candidate.
- **Final-head affected checks:** all 10 dispatch-publication cases pass; type checking reports no issues in 87 files. The final test-only correction addresses the hashing dependency through its defining module. Compiler implementation bytes equal b8c4fb123bc8ffac151408c49ac54c4a38d3ad55.
- **Formatting/lint:** the five changed Python files pass the repository's explicit configuration; final collision-test imports follow the same configuration.
- **Collision observation:** forcing two distinct full digests to the same 12-character prefix produces E_PUBLICATION_FAILED and preserves every previously published output byte. Existing tests also cover equivalent selections, distinct contents, parallel and heading placements and validation-only refusal.

These checks establish compiler behavior and packaging, not native-agent accuracy or a released version. The initial stale lifecycle expectation and sandbox cache refusal are retained in the originating investigation; the complete passing source/corpus logs above identify the accepted checks.

## Final Eight-Character Candidate

Candidate f41769e7cd7e763ad5182efc835b0e4d64cddaac uses eight characters. All 2,324 source cases pass, including installed-wheel coverage; all 708 fixtures pass; the 59 focused preset/publication cases pass, including the actual eight-character prefix collision; type checking passes for 87 files. Changed Python files pass explicit repository lint/format settings. No previous output-name aliases are published.

The earlier twelve-character candidate and native consumers pinned to it remain distinct evidence. This source/corpus result observes the final eight-character code.
