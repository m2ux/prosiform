# Validation

Each check ran on `i08/e03/w01-the-parser-the-refusal` at `e24d2114`, with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`, through one `make check` that exited `0`.

## Unit tests

`make test`: 1571 passed.

- `src/tests/test_cli.py::test_a_bare_fragment_is_invalid_usage_naming_the_section_spelling` — `pf -d json '#a-section'` exits `2`, publishes nothing, and its one diagnostic names `#a-section` as its reference and `document#fragment` in its message (AC1).
- `src/tests/test_cli.py::test_every_option_the_contract_declares_is_accepted` passes with no `-f`.
- `src/tests/test_derived_output.py` — `dir/a.md#part` and `dir/a.md#p%61rt` share one derived destination; `a.md#two b.md` publishes `a__two+b.bundle.md`; `dir/a.md#part` publishes into `dir_a__part.bundles/` and `-c` publishes nothing (AC2).
- `src/tests/test_file_roots.py::test_a_parent_section_entry_bootstraps` — `../a.md#part` from a child directory bundles the parent's section.

## Harness

`make harness`: 1148 passed, `checks/tests/test_runner.py` holding `message_contains` against the refusal's `document#fragment` text and `checks/tests/test_authoring.py` holding the guide's sentence `a section written as document#fragment` and every worked command to a file this repository holds (AC3, AC4).

## Corpus

`make corpus`: 421 fixtures, 421 pass, 0 fail.

- `cli/a-bare-fragment-is-invalid-usage` — `#stop` exits `2` with `E_INVALID_USAGE` naming `#stop` and `document#fragment` (AC1).
- `rewriting/a-fragment-only-dependency`, `rewriting/no-link-names-a-source-path`, `deferral/a-deferred-fragment-of-its-own-document` and the two `dispatch/...-by-fragment-...` fixtures pass: a `[Check](#section)` link resolves against the document carrying it (AC6).
- `extraction/section-to-the-next-sibling` (`guide__run.bundle.md`), `usage-example/two-selected-sections` and `usage-example/a-section-entry-and-its-document` (`artifacts_epic-issue-body__record-epic-delivery.bundle.md`, byte-identical to the bundle the `-f` spelling published) derive each name from the document named (AC2, AC3).

## No fixture names the option

A search of every `fixtures/*/*/manifest.toml` for the argument `"-f"` finds none. `cli/fragment-only-reference-without-from` is rewritten as `cli/a-bare-fragment-is-invalid-usage`, `usage-example/a-bare-fragment-and-its-referring-document` as `usage-example/a-section-entry-and-its-document`, and `extraction/a-fragment-alone-selects-from-the-referrer` and `mock/a-redirected-referrer-carries-its-entry` are withdrawn (AC3).

## Invocation

`make invocation`: 29 statements of `invocation.md` held to the build's own `-h` in both directions. The table names no `-f`, the `REF` row reads `document or document#fragment; paths from cwd`, matching the help, and the build declares no `-f` (AC1, AC4).

## Conformance

`make conformance`: 0 declarations naming no clause; every fixture this unit touches names a clause the pinned design (`a0a3264a`) states. `make independence`, `make links` and `make tables` pass.
