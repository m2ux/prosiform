# W04 Validation

Runtime revision: `f139b253ab954bb2f2241a8d3d428e03600b35da`, based on W03 at `dd2e087060701f8472cfa9a8d2c2b81bea0a437f`. Contract snapshot: `d26ae99b7e989f0978d20f7d9bdc098c16319797` in this record.

## Source Ownership

Pass. The implementation suite has 905 passing tests. `src/tests/test_conversion_compilation.py` exercises destination-owned settings through direct, fragment, repeated, transitive, diamond and cyclic references, an unannotated sibling, deferred-only exclusion and subsequent active inclusion. Exact group identities remain distinct from filesystem paths and from other group spellings. Existing grouping and candidate-validation fixtures preserve overview, variant, anchor, ordering and overflow behavior. Coverage: AC8.

The independent [compilation probe](compilation-probe.py) compares W03 CLI grouping with equivalent W04 metadata on files in unrelated directories: output bytes match. It also checks punctuation and whitespace in group identities, case distinctions, file/group heading collisions, deterministic conflict ordering and output preservation. Run from the task worktree with its locked Python environment; the probe names the local W03/W04 worktrees explicitly.

## Conflict Publication

Pass. The integration tests cover text and JSON diagnostics under stdout, file output and check mode. Reversing entries produces identical errors identifying both original metadata locations. Existing output bytes remain intact and stdout is empty. The corpus includes `grouping/conflicting-member-depths`, exercising `E_GROUP_DEPTH_CONFLICT`. The independent compilation probe also verifies these properties. Coverage: AC9.

## Installed Interface

Pass. The [installed-wheel probe](installed-probe.py) builds and installs the wheel in a temporary environment outside the checkout. The installed `pf` compiles metadata groups, rejects `-g`, attached `-gVALUE` and `--group` with usage status 2, and exercises help, roots, whole/fragment entries, referrer, JSON diagnostics, check mode, atomic file output and byte limits. The repository installed-wheel smoke also passes. Coverage: AC10.

Run from the task worktree: `uv run --project src --frozen python PATH/installed-probe.py`.

## Repository Checks

The local check sequence passes lint, formatting, types, 905 implementation tests, 611 harness tests, all 252 corpus fixtures, installed-wheel smoke, layout, command tables, online links, vocabulary, invocation, conformance and independence. A final complete `make check` run is in progress on the recorded revision; its result is recorded before merge.

Equivalent annotated grouping fixtures retain their expected output bytes. Three shared usage-example outputs intentionally reflect the groups now declared by their shared source files. The grouped usage-example output itself is byte-identical. Four fixture descriptions use the final contract vocabulary, and the glossary defines its metadata grouping rule.

Conformance reports 22 clauses without a fixture and three installation claims that no corpus invocation observes. This is a coverage report, not a claim of exhaustive corpus coverage; the final corpus audit remains W05.

## Remote Checks

Pending: [Checks on the exact head](https://github.com/m2ux/prosiform/actions/runs/39915942493/job/120289433013). Merge requires success and refreshed target requirements.
