# Validation — I00:E04:W01

The checks behind the pull request's Test Plan, each with the command that was run and the output it returned.

Every run is from the worktree at `i00/e04/w01-reference-normalization-and-path`, head `951bd00`, base `c0ee1ef`. The corpus is named a build by configuration, so each corpus run carries `PROSIFORM_BUILD` naming this change's console entry point.

## T1 The corpus, every fixture against the build

```bash
make corpus
```

The twelve fixtures this row adds, and the one it inherits for the entry suffix:

```text
normalization/a-double-encoded-escape: pass
normalization/a-drive-path: pass
normalization/a-non-utf8-escape-sequence: pass
normalization/a-parent-segment-reaching-the-root-boundary: pass
normalization/a-protocol-relative-url: pass
normalization/a-scheme-and-an-authority-in-selected-content: pass
normalization/an-encoded-path-separator: pass
normalization/an-over-long-percent-escape: pass
normalization/bare-text-paths: pass
normalization/query-on-an-entry-reference: pass
normalization/root-escape: awaited, awaiting I00:E04
normalization/root-relative-entry-reference: pass
profile/entry-suffix-outside-the-profile: pass
profile/markdown-suffixes-in-mixed-case: pass
corpus check: 52 fixture(s), 50 pass, 0 fail, 2 awaited, 0 unexpected pass
```

The corpus held 40 fixtures at the base and holds 52 at the head. The two awaited fixtures are the two it already carried: `extraction/nested-section-target` awaits `I00:E03` and `normalization/root-escape` awaits `I00:E04`, which delivers the traversal that reaches a link inside a source.

No fixture this row adds carries `awaiting`. Each of the seven adversarial cases was declared with `awaiting = "I00:E10"` and each met its manifest against the build, which the corpus reports as an unexpected pass and fails the run for, so each marker was lifted on the fixture it no longer describes.

## T2 The corpus checks, the schema and the runner among them

```bash
make harness
```

```text
187 passed in 0.45s
```

Every manifest this row adds validates against `fixtures/manifest.schema.json`, and every path each one names exists. No code was added to either catalogue: the grammar refusal draws `E_INVALID_USAGE` and the containment refusal `E_SOURCE_OUTSIDE_ROOT`, both already declared, so the error catalogue stands at its 21 codes and `checks/tests/test_catalogue.py` compares the same two sets it compared at the base.

## T3 The command's own suite

```bash
make test
```

```text
279 passed in 0.15s
```

`tests/test_closure.py` holds the resolution sequence step by step: the components split before any escape is decoded, an escape validated as a percent and two hexadecimal digits, one decoding and no second, escapes spelling one character decoded together, a separator or a control character a segment decodes to refused, `.` and `..` normalized against the directory the reference is written in, a walk above the root refused, a scheme and an authority classified rather than resolved, a drive letter read as a path rather than as a scheme, and a fragment looked up as the exact text it decoded to.

## T4 The repository's checks in one pass

```bash
make check
```

That is `lock-check lint format-check typecheck test harness corpus layout tables links vocabulary`, and every one passed.

```text
All checks passed!
Success: no issues found in 27 source files
279 passed in 0.15s
187 passed in 0.45s
corpus check: 52 fixture(s), 50 pass, 0 fail, 2 awaited, 0 unexpected pass
layout check: 3 tree(s) present
table check: 12 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 23 source(s)
```

The two checks that read across the branch boundary both passed against `origin/engineering`: the catalogue comparison, because this row adds no code, and the vocabulary comparison, because it marks no new contract term.
