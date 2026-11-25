# F38 Verification

- **Source suite:** all 2,324 collected cases pass at b8c4fb123bc8ffac151408c49ac54c4a38d3ad55, including installed-wheel bootstrap coverage. Initial wheel setup inside bubblewrap could not write its dependency cache; the complete passing run uses host access for that package-install boundary.
- **Corpus:** 708 fixtures pass, zero fail or awaited. Expected preset qualifiers, filenames and rewritten links agree with the candidate.
- **Final-head affected checks:** all 10 dispatch-publication cases pass; type checking reports no issues in 87 files. The final test-only correction addresses the hashing dependency through its defining module. Compiler implementation bytes equal b8c4fb123bc8ffac151408c49ac54c4a38d3ad55.
- **Formatting/lint:** the five changed Python files pass the repository's explicit configuration; final collision-test imports follow the same configuration.
- **Collision observation:** forcing two distinct full digests to the same 12-character prefix produces E_PUBLICATION_FAILED and preserves every previously published output byte. Existing tests also cover equivalent selections, distinct contents, parallel and heading placements and validation-only refusal.

These checks establish compiler behavior and packaging, not native-agent accuracy or a released version. The initial stale lifecycle expectation and sandbox cache refusal are retained in the originating investigation; the complete passing source/corpus logs above identify the accepted checks.
