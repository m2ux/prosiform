# Validation — I00:E04:W02

The checks behind the pull request's Test Plan, each with the command that was run and the output it returned.

Every run is from the worktree at `i00/e04/w02-root-confinement-and-no`, head `72e7b24`, base `1a74e4a`. The corpus is named a build by configuration, so each corpus run carries `PROSIFORM_BUILD` naming this change's console entry point.

## T0 The behaviour measured before the design was built to it

Each candidate case was run against the build at the base, in a tree written outside the repository, before any of it was designed for. The measurement is what decided which cases this row delivers and which are no case at all.

| Case | At the base | At the head |
| --- | --- | --- |
| A link to a file outside the root | `E_SOURCE_OUTSIDE_ROOT`, status 1 | `E_SOURCE_SYMLINK`, status 1 |
| A path through a directory link pointing outside the root | `E_SOURCE_OUTSIDE_ROOT`, status 1 | `E_SOURCE_SYMLINK`, status 1 |
| A link whose target the root holds | bundled, status 0 | `E_SOURCE_SYMLINK`, status 1 |
| A link to a link, both inside the root | bundled, status 0 | `E_SOURCE_SYMLINK`, status 1 |
| A path through a directory link pointing inside the root | bundled, status 0 | `E_SOURCE_SYMLINK`, status 1 |
| A hard link inside the root | bundled, status 0 | bundled, status 0 |
| A parent segment above the root | `E_SOURCE_OUTSIDE_ROOT`, status 1 | `E_SOURCE_OUTSIDE_ROOT`, status 1 |
| A document the root holds | bundled, status 0 | bundled, status 0 |

The base refused an escaping link under the containment code rather than the policy one, because the join resolved the link and the comparison then saw a path outside the root. Every link the root could hold the target of was followed in silence. A hard link is a second name for one inode and no filesystem call distinguishes it from the file it names, so it reads as the document it is at both ends and the policy has nothing to refuse.

## T1 The corpus, every fixture against the build

```bash
PROSIFORM_BUILD="uv run --project <worktree>/prototype --frozen prosiform" make corpus
```

The five fixtures this row adds:

```text
confinement/a-parent-segment-above-the-root: pass
confinement/a-symlink-chain-below-the-root: pass
confinement/a-symlink-to-a-document-inside-the-root: pass
confinement/a-symlinked-directory-below-the-root: pass
confinement/a-symlinked-source: pass
corpus check: 57 fixture(s), 55 pass, 0 fail, 2 awaited, 0 unexpected pass
```

The corpus held 52 fixtures at the base and holds 57 at the head. The two awaited fixtures are the two it already carried: `extraction/nested-section-target` awaits `I00:E03`, and `normalization/root-escape` awaits `I00:E04` for the traversal that reaches a link inside a source, which is W03's row rather than this one's.

No fixture this row adds carries `awaiting`. Each candidate for one was measured first, and each turned out to be delivered by the walk this row builds, so each is declared as a passing fixture instead.

## T2 The corpus checks, the schema and the runner among them

```bash
make harness
```

```text
192 passed in 0.46s
```

Every manifest this row adds validates against `fixtures/manifest.schema.json`, and every path each one names exists. No code was added to either catalogue: `E_SOURCE_SYMLINK` and `E_SOURCE_OUTSIDE_ROOT` are both already declared, so the error catalogue stands at its 21 codes and `checks/tests/test_catalogue.py` compares the same two sets it compared at the base.

## T3 The command's own suite

```bash
make test
```

```text
292 passed in 0.15s
```

`tests/test_access.py` holds the walk to the cases a fixture directory in git cannot carry: a hard link read as the document it is, a directory named as a document, a document named as a directory, a broken link refused as a link rather than as a missing file, a root that is itself a link read as the caller's own spelling of the root, and the empty, `.`, `..` and leading-separator segment forms refused rather than descended.

## T4 The repository's checks in one pass

```bash
PROSIFORM_BUILD="uv run --project <worktree>/prototype --frozen prosiform" make check
```

That is `lock-check lint format-check typecheck test harness corpus layout tables links vocabulary`, and every one passed.

```text
All checks passed!
Success: no issues found in 29 source files
292 passed in 0.15s
192 passed in 0.46s
corpus check: 57 fixture(s), 55 pass, 0 fail, 2 awaited, 0 unexpected pass
layout check: 3 tree(s) present
table check: 12 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 23 source(s)
```

The two checks that read across the branch boundary both passed against `origin/engineering`: the catalogue comparison, because this row adds no code, and the vocabulary comparison, because it marks no new contract term.

## T5 The fixture format carries a symbolic link

```bash
git ls-files -s fixtures/confinement
```

```text
120000 656dfc3f55927e2e845c06c3d626d03d4adf8d88 0	fixtures/confinement/a-symlink-chain-below-the-root/source/alias.md
120000 8ee3e9b49ae90525a8a5ed393c895bd9f8f80f30 0	fixtures/confinement/a-symlink-chain-below-the-root/source/chain.md
120000 656dfc3f55927e2e845c06c3d626d03d4adf8d88 0	fixtures/confinement/a-symlink-to-a-document-inside-the-root/source/alias.md
120000 d09b80733baa4f6b198f2cf2d62bbfc5b6cbf1f0 0	fixtures/confinement/a-symlinked-directory-below-the-root/source/docs
120000 7ecd6330038a4c2ae8b44e8bc0cc3b07e8b4d830 0	fixtures/confinement/a-symlinked-source/source/guide.md
```

Mode `120000` is git's symbolic link, so each is recorded as a link rather than as a regular file holding a target path. The runner invokes the build against the fixture's own tree in place and copies nothing, so the link the corpus declares is the link the run meets. A checkout unable to create one writes the target path into a regular file, which the run reads as a document and bundles, which fails the fixture on its status rather than passing it against something else.
