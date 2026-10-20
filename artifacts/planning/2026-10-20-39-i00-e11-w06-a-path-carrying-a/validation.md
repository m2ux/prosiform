## Overview

What the contract settles for `I00:E11:AC7`, the fixtures that state it, and the checks the delivery was measured against at `87b7ff0`.

## The Reading the Contract Takes

The criterion offers a disjunction, and the design decides which half holds. The resolution sequence splits a reference into its components before any percent escape is decoded, and the design's own table states the result:

| Reference | Required interpretation |
| --- | --- |
| `notes%23draft.md#run` | Section `run` in literal filename `notes#draft.md`. |

So a source path carrying a number sign is nameable by an entry reference, and the fixtures state the naming rather than a refusal. The literal spelling `notes/draft #.md` is the complement of that rule: the fragment opens at the first number sign, so the reference names the document `notes/draft ` and the fragment `.md`, and the run fails with `E_UNSUPPORTED_ENTRY_SUFFIX` on the suffix the remainder leaves. That is a reading of the reference rather than a refusal of the path, and it is declared beside the naming so the split order is itself under test.

The build changes nothing. The behaviour the fixtures declare is the behaviour it has; what this row moves is the obligation, out of one implementation's unit tests and into the language-neutral corpus.

## <a id="fixtures"></a>The Fixtures

| Fixture | Invocation | What it declares |
| --- | --- | --- |
| `normalization/an-encoded-number-sign` | `notes%23draft.md#run` | The design's own table row, run: the reference names a section of the document at `notes#draft.md`, and the file heading reads `# notes\#draft` |
| `identity/a-path-ending-in-a-number-sign` | `notes/draft%20%23.md` | A path ending in a space and a number sign keeps that character in its file heading, `# notes/draft \#`, where an ATX closing sequence would take it off |
| `normalization/an-unencoded-number-sign` | `notes/draft #.md` | The same tree named literally splits at the number sign, so the run fails with `E_UNSUPPORTED_ENTRY_SUFFIX` and exit status 1 |

Each is a directory under `fixtures/` holding `manifest.toml`, a `source/` tree and the expected standard output, which is the shape every fixture of this corpus takes.

## <a id="corpus"></a>The Corpus Run

`make corpus` at `87b7ff0`, with the locked environment's console entry point named to the runner as `PROSIFORM_BUILD`.

```text
corpus check: 206 fixture(s), 204 pass, 0 fail, 2 awaited, 0 unexpected pass
```

Two hundred and six fixtures, where the base runs two hundred and three. The three this row adds each pass, and no fixture of the base changed verdict.

## <a id="mutation"></a>What the Fixtures Catch

A fixture that passes says nothing until a build that denies its claim fails it. Each claim was denied in turn, in the worktree, and the corpus re-run; both mutations were reverted and the delivered tree carries neither.

| Mutation | Corpus |
| --- | --- |
| The number sign removed from the characters a file heading escapes | `identity/a-path-ending-in-a-number-sign` and `normalization/an-encoded-number-sign` fail; the literal-spelling fixture still passes, because its run never reaches a heading |
| The reference decoded before its components are split | The same two fail, joined by two fixtures of the base that declare the decode-exactly-once rule |

The second mutation leaves `normalization/an-unencoded-number-sign` passing, which is correct: that fixture's reference carries no escape, so decoding it first changes nothing about where it splits.

## <a id="gate"></a>The Gate

Every target of `make check`, run in the delivery worktree at `87b7ff0`. The corpus and invocation targets name the locked environment's console entry point as the build under test.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 603 passed |
| `make harness` | 395 passed |
| `make corpus` | 206 fixture(s), 204 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `make smoke` | prosiform installs into an environment and bundles a reference from a source root |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) of the documented invocation |

## The Review

- **The change is confined to the corpus.** Nine files, all of them new, all under `fixtures/`. Nothing in `src/`, nothing in `checks/`, no `Makefile` target and no schema change.
- **Each fixture names the design clauses it encodes.** The encoded reference cites the `notes%23draft.md#run` row and resolution-sequence step 2; the file heading cites the file-scoped hierarchy rule that escapes a path as literal heading text; the literal spelling cites step 2 beside the profile's suffix rule.
- **The warning each passing run emits is declared.** Both passing fixtures carry `W_ENTRY_DESTINATION` in their manifests with the resolved destination, so a build that stopped reporting it would fail rather than pass quietly.
- **The destination `notesdraft-` is the renderer's, not a defect.** The slug rule discards the separator and the number sign and turns the remaining space into a hyphen, so a trailing hyphen is what the path produces. The entry line links the heading it generated, which is what the fixture holds it to.

## Plan Changes

No change of a kind the allowance names was applied: no task or epic was created, nothing migrated, no priority or board status moved, and no issue took on scope it was not planned with. None was held either.

One record correction accompanies the delivery. The epic's reference for AC7's origin read that no entry reference can name a path carrying a number sign. The resolution sequence splits a reference before any escape is decoded, so the encoded spelling names it, and the reference now states the origin with that reading. It moved to the end of the list as R14, which leaves the reference labels in sequence.

## Limitations

The corpus declares what this build does on a filesystem that admits a number sign and a trailing space in a filename. A platform refusing either name cannot materialise the source tree, and the fixture fails there as an unwritable tree rather than as a disagreement about the contract. No fixture of this corpus states what such a platform should do, and nothing in this row changes that.
