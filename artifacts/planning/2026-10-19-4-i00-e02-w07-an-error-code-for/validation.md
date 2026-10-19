# Validation — I00:E02:W07

Procedure, tested revisions and observations for the checks the pull request's Test Plan cites. Each failing case below is an observed run: the tree was made to carry one fault, the command was run, its output was recorded, and the fault was reverted.

## Tested revisions

| Revision | What it is |
| --- | --- |
| `7f8fe64` | The epic base the branch was cut from |
| `fbfa9aa` | The branch before its base was updated: the schema's catalogue, the command's codes and six fixtures |
| `3af44a1` | The epic base after W03 merged as `#50`, and the base measurement |
| `959884d` | The branch's head: the base merged in, the ninth code, and seven fixtures |
| `99e06da` | The design on `engineering`, carrying the nine codes |

The build under test is the prototype wheel installed into `prototype/.venv`, invoked as `prototype/.venv/bin/prosiform`.

## The design-push windows

The catalogue test reads the design from `origin/engineering` and the catalogue from the schema on the branch under test, so the two halves of this change cannot both hold on every branch at once. The implementation was finished and every other check was green before each design push, so each window is bounded by two pushes rather than by the work.

| Event | UTC |
| --- | --- |
| Seven codes pushed to `engineering` as `a073271` | 2026-10-19T10:45:36Z |
| Branch pushed as `fbfa9aa` | 2026-10-19T10:45:42Z |
| Continuous integration green on `fbfa9aa`, run `39239759699` | 2026-10-19T10:46:11Z |
| The ninth code pushed to `engineering` as `99e06da` | 2026-10-19T10:52:42Z |
| Branch pushed as `959884d` | 2026-10-19T10:52:48Z |
| Continuous integration green on `959884d`, run `39240599685` | 2026-10-19T10:53:12Z |

Six seconds separate each pair of pushes. One continuous-integration run fell inside the first window and failed for it: run `39239750538` on `i00/e02/main`, started 2026-10-19T10:45:40Z, which is the base run for the parallel W03 merge (`#50`). It failed the catalogue test alone, because that base carried the design's new codes and not yet the schema's. Merging this unit into that base is what returns it to green.

A branch that has not yet taken this schema fails the catalogue test the same way and for the same reason until the change reaches it. `main` is in that state until the epic base merges.

## The ninth code

W03 landed the encoding requirement in the epic base while this unit was in flight. A source that is not valid UTF-8 fails as an input failure, and it is a failing outcome the contract names at its Encoding clause, so it takes a code of its own. `E_INVALID_ENCODING` is declared at that clause, carried by the catalogue, named by the command's diagnostic and declared by `profile/source-not-utf8`. AC8 reads *a source that is not valid UTF-8 fails rather than being decoded with replacements, as the encoding fixtures show*, and a fixture can now state it.

## T1 The command's own suite

**Observes AC12.** Every outcome the command returns, and the code each diagnostic now carries.

```bash
cd prototype && uv run --frozen pytest
```

**Pass.** Exit 0. One hundred and seventy-six tests at `959884d`. The six this unit adds: four faults in the command line, a missing `--root`, and an output path naming an input source, each carrying `E_INVALID_USAGE`. Nine tests changed from asserting a diagnostic carries no code to asserting which code it carries: the placeholder internal error as `E_UNEXPECTED_INTERNAL_ERROR`, two raw-HTML refusals as `E_RAW_HTML`, four construct refusals as `E_UNSUPPORTED_CONSTRUCT`, a source root naming no directory as `E_ROOT_NOT_FOUND`, and a source that is not valid UTF-8 as `E_INVALID_ENCODING`. An entry suffix outside the profile now asserts `E_UNSUPPORTED_ENTRY_SUFFIX` and a refused write `E_PUBLICATION_FAILED`.

A diagnostic's code is required rather than optional, so a failing outcome added later without one is a type error rather than a gap found by reading.

## T2 The catalogue held to the design, in both directions

**Observes AC12.** The schema's catalogue against the set of codes the design carries, with the tree made to carry each disagreement in turn.

```bash
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
```

**Pass.** Exit 0. One hundred and eighteen tests at `959884d`, against the design at `99e06da`. Both catalogues are equal sets: twenty error codes and two warning codes.

**A code the schema carries that the design does not name fails.** Observed at `fbfa9aa` before the design was pushed, with the catalogue already carrying the seven codes:

```text
AssertionError: assert catalogue(severity) == codes(prefix, design())
  Extra items in the left set:
  'E_INVALID_USAGE'
  'E_UNSUPPORTED_CONSTRUCT'
  'E_UNEXPECTED_INTERNAL_ERROR'
  'E_RAW_HTML'
  'E_UNSUPPORTED_ENTRY_SUFFIX'
```

**A code the design names that the schema omits fails.** Observed by deleting `E_RAW_HTML` from the schema's enum, running the test, and reverting:

```text
AssertionError: assert catalogue(severity) == codes(prefix, design())
  Extra items in the right set:
  'E_RAW_HTML'
```

**A manifest naming a code the catalogue does not carry fails validation.** Observed by renaming `cli/diagnostics-format-unknown`'s code to `E_BAD_COMMAND_LINE`, running the corpus test, and reverting:

```text
FAILED checks/tests/test_corpus.py::test_a_fixture_manifest_matches_the_schema[cli/diagnostics-format-unknown]
  expected.diagnostics.0.code: 'E_BAD_COMMAND_LINE' is not one of
  ['E_AMBIGUOUS_FILE_GROUP', …, 'E_UNTERMINATED_FRONTMATTER']
```

## T3 The corpus against the build, before and after

**Observes AC12.** Every fixture in the corpus, run against the build under test and compared with its manifest, at the base revision and at the tested revision.

```bash
PROSIFORM_BUILD=…/prototype/.venv/bin/prosiform python corpus.py
```

**Pass, as a measurement.** At the epic base `3af44a1` the run reports **4 of 19 fixtures pass**. At `959884d` it reports **11 of 26 fixtures pass**. The seven added are the seven that pass:

```text
cli/diagnostics-format-unknown: pass
cli/fragment-only-reference-without-from: pass
cli/output-naming-an-input-source: pass
profile/entry-suffix-outside-the-profile: pass
profile/raw-html-in-selected-content: pass
profile/source-not-utf8: pass
profile/unsupported-construct: pass
```

Each declares a failure, and a failing run returns its status without reaching the bundling stage, so none of them waits on the emitter W04 delivers. The fifteen that still fail are the fifteen that declare a successful bundling or a resolved reference, and each fails on its exit status exactly as it did at the base. Their count is unchanged at 0 of 15.

At the branch point `7f8fe64` the same measurement reported 3 of 10, and at `fbfa9aa` 9 of 16; the base update brings W03's ten frontmatter fixtures and one further pass with them.

## T4 The static checks and the documents

**Observes AC12.** The checks that police prose and shape, each over the changed tree.

```bash
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
cd prototype && uv lock --check
python3 checks/layout.py
python3 checks/tables.py
python3 checks/vocabulary.py
python3 checks/links.py --online
```

**Pass.** Exit 0 from each. Ruff reports all checks passed over twenty-two files; mypy reports no issues in twenty-one source files under `strict`; `uv lock --check` resolves unchanged, since the change adds no dependency. The layout check reports three trees present. The vocabulary check reports thirty-four marked contract terms, unchanged: the design's new prose italicises no term. The link check resolves every reference; no heading was added to the design, so no anchor another document links to has moved.

## T5 Continuous integration on the exact head

**Observes AC12.** `make check` in full, on the branch's head, in the repository's own runner.

```bash
gh run list --repo m2ux/prosiform
gh run view <id> --repo m2ux/prosiform
```

**Pass.** Run `39240599685` on `959884d`, concluded `success` at 2026-10-19T10:53:12Z. Run `39239759699` on `fbfa9aa` concluded `success` before the base was updated.
