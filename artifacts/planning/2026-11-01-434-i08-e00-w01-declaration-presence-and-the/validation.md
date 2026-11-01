# Validation

Evidence for each check the [work item](w01.md) names, run in the unit's worktree at `f13855fc` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 metadata tests

`src/tests/test_metadata.py` passes under `make test`.

- `test_an_empty_block_declares`: `prosiform: {}` and its block form decode to `Conversion(declared=True)`.
- `test_absent_settings` and `test_absent_frontmatter_declares_nothing`: an empty or comments-only block, `{}`, unrelated fields and absent frontmatter decode with `declared` false.
- `test_a_declared_root_is_refused_at_its_key`: `root` with a string, an empty string, null, and beside a group pair each fail with `E_INVALID_CONVERSION_METADATA` at the key (line 3, column 3), naming `prosiform.root is refused` and `remove the field`.

## T2 command tests

`src/tests/test_cli.py` passes under `make test`.

- `test_a_declared_root_is_an_input_failure`: exit status 1, no bundle, one `E_INVALID_CONVERSION_METADATA` at `guide.md:2:13`.
- `test_no_code_reports_a_missing_root`: the codes the build declares carry no `E_ROOT_NOT_FOUND`.

## T3 declared root fixture

`fixtures/inclusion/a-declared-root-is-refused: pass` under `make corpus`: exit status 1, no bundle, `E_INVALID_CONVERSION_METADATA` at `rules.md:2:13` with chain `guide.md`, `rules.md`.

## T4 empty block fixture

`fixtures/inclusion/an-empty-block-declares: pass` under `make corpus`: the target declaring `prosiform: {}` is compiled and the link rewritten to `#rules`.

`fixtures/inclusion/no-block-does-not-declare` is `awaited, awaiting I08:E00:W03`: the decode distinguishes the undeclared target (T1), and classification reads that fact when the target-asking row lands.

## T5 conformance

`make conformance` passes: `0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere`. The schema catalogue and the build's `-C` listing carry no `E_ROOT_NOT_FOUND`; `E_SOURCE_ACCESS` is reached by `fixtures/confinement/a-path-the-filesystem-cannot-open`.

## T6 tests

`make test` passes with no test asserting a root-not-found diagnostic: `git grep ROOT_NOT_FOUND` in the worktree returns only the absence assertion in `test_no_code_reports_a_missing_root`. The two root-not-found tests of `src/tests/test_file_roots.py` and `src/tests/test_cli.py` are removed.

## T7 full check

`make check` exits 0: corpus `375 fixture(s), 374 pass, 0 fail, 1 awaited, 0 unexpected pass`. Every `usage-example/` expected bundle is unchanged with `root` dropped from the example tree.

`make examples`, which `make check` does not run, fails on the cases whose panels declare `root`; their re-rendering is the drawings row of this epic.
