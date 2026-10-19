# Validation — I00:E02:W08

Procedure, tested revision and observations for the checks the pull request's Test Plan cites. Every run below was performed and its output is the output it produced. Each failing case was produced by making the tree carry one fault and nothing else, running the command, recording its output, and reverting.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e02/w08-check-fixtures-for-a` |
| Tested revision | `8249cb08f15c9ce67c7faf309081ffa6f435eab4` |
| Base revision | `d8abd5e` on `i00/e02/main`, where the base corpus count was measured |
| Contract revision | `13a94d7` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Continuous-integration job | `Checks`, `.github/workflows/checks.yml`, on `ubuntu-latest` |
| Build under test | the locked environment's console entry point, named to the corpus run as `PROSIFORM_BUILD` |
| Run from | the repository root |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0`, `markdown-it-py 4.2.0` |
| Date | 2026-10-19 |

## The corpus at the base and at the head

The base is `d8abd5e` on `i00/e02/main`:

```text
corpus check: 38 fixture(s), 36 pass, 0 fail, 2 awaited, 0 unexpected pass
```

At the head, `8249cb0`, two fixtures join it and both pass:

```text
corpus check: 40 fixture(s), 38 pass, 0 fail, 2 awaited, 0 unexpected pass
```

**36 of 38 at the base, 38 of 40 at the head.** The two awaited fixtures are unchanged: `extraction/nested-section-target` awaits `I00:E03` and `normalization/root-escape` awaits `I00:E04`.

## The run AC10 names

```bash
prosiform --root fixtures/identity/whole-document/source --check guide.md
```

Exit 0, standard output 0 bytes, standard error 0 bytes.

```bash
prosiform --root <fixture>/source --diagnostics json --check --output bundle.md guide.md
```

Exit 0, standard output 0 bytes, standard error 0 bytes, and no `bundle.md` in the working directory afterwards.

## T1 The corpus, every fixture against the build

**Observes AC10.** Every fixture the corpus holds, run against the build the same change produces, the two this unit adds among them.

```bash
make corpus
```

**Pass.** Exit 0 at `8249cb0`. Forty fixtures, thirty-eight passing, two awaited.

```text
cli/validation-only-run: pass
cli/validation-only-run-with-an-output-file: pass
corpus check: 40 fixture(s), 38 pass, 0 fail, 2 awaited, 0 unexpected pass
```

**A validation-only run that publishes fails both fixtures.** Observed by removing the early return `--check` takes before publication, running the corpus, and reverting:

```text
cli/validation-only-run: fail
  expected.stdout: the bytes differ
    0 bytes expected, 186 produced
    first difference at byte 0, expected line 1 column 1
    expected b''
    produced b'This bundle was built fo'
    the run's output carries 186 bytes beyond the end
cli/validation-only-run-with-an-output-file: fail
  expected.absent: the run created bundle.md
    186 bytes written, beginning b'This bundle was built fo'
corpus check: 40 fixture(s), 36 pass, 2 fail, 2 awaited, 0 unexpected pass
```

The two halves of the criterion fail separately and name themselves: the stream comparison catches the bundle on standard output, and the absent declaration catches the file. `git status` after that run reported the two new fixture directories and no `bundle.md`, so the runner removed the file it reported.

## T2 The corpus checks, the schema and the runner among them

**Observes AC10.** The declaration a fixture uses to state that a file is not created, and the runner's reading of it.

```bash
make harness
```

**Pass.** Exit 0 at `8249cb0`. One hundred and seventy-five tests, where the base runs one hundred and sixty-four: nine this unit adds and two the two new fixtures bring to the per-fixture schema check.

The nine are five on the schema and four on the runner.

- A manifest declaring an absent path validates, and one declaring none validates, so the declaration is optional.
- A declaration naming no path, one naming a path twice, and one naming a path outside the fixture each fail validation.
- A declared path the run leaves absent is the expectation being met.
- A run that creates the path fails, and the difference names `expected.absent`, the path and the bytes written.
- The file the run created is removed, so the fixture directory after the run is the one the manifest declares.
- A fixture already holding a path it declares absent is refused as malformed, the build is never invoked, and the file is left where it is.

## T3 The command's own suite

**Observes no criterion.** The escaping, which completes another row's concern.

```bash
make test
```

**Pass.** Exit 0 at `8249cb0`. Two hundred and forty-eight tests, where the base runs two hundred and forty-five. The three this unit adds hold `escaped` to escaping the number sign, hold a heading carrying an escaped trailing number sign to parsing as one text token whose content keeps the character, and hold `group` to emitting `# notes/draft \#` for the path `notes/draft #.md`.

## T4 The repository's checks in one pass

**Observes AC10.** The set of checks run together, on the exact head, in the job that runs them on every change.

```bash
make check
```

**Pass.** Run [39263535967](https://github.com/m2ux/prosiform/actions/runs/39263535967) on `8249cb0`, conclusion `success`. The same command on the same revision locally returned 0, running `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `harness`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order.

## The escaping has no fixture

The third fixture this unit planned cannot be written. A file heading's visible text is the document's root-relative path, and a path whose final segment ends in a space and a number sign would lose that character to an ATX closing sequence, which is the hazard the escaping removes. No run of this build reaches such a heading.

An entry reference is a document and an optional fragment, and the fragment opens at the first number sign, so `notes/draft #.md` names the document `notes/draft ` and the fragment `.md`:

```text
E_UNSUPPORTED_ENTRY_SUFFIX: the entry reference 'notes/draft #.md' names a document whose suffix is outside the skill-markdown-v1 profile
  reference: notes/draft #.md
  remedy: name a document ending .md or .markdown
```

`--from` splits the same way, and each file group of this build comes from a document an entry reference names, so no command line reaches the heading. A manifest declaring the bundle such a path produces would declare how a reference spells a path carrying a number sign, which no design clause states. The escaping is covered by T3 instead, and the reachability gap is reported as an arising issue.
