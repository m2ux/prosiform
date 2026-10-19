# Validation — I00:E02:W07

Procedure, tested revisions and observations for the checks the pull request's Test Plan cites. Each failing case below is an observed run: the tree was made to carry one fault, the command was run, its output was recorded, and the fault was reverted.

## Tested revisions

| Revision | What it is |
| --- | --- |
| `7f8fe64` | The epic base the branch was cut from, and the base measurement |
| `fbfa9aa` | The task branch's head: the schema's catalogue, the command's codes and six fixtures |
| `a073271` | The design on `engineering`, carrying the seven codes |

The build under test is the prototype wheel installed into `prototype/.venv`, invoked as `prototype/.venv/bin/prosiform`.

## The design-push window

The catalogue test reads the design from `origin/engineering` and the catalogue from the schema on the branch under test, so the two halves of this change cannot both hold on every branch at once. The implementation was finished and every other check was green before the design was pushed, so the window is bounded by the two pushes rather than by the work.

| Event | UTC |
| --- | --- |
| Design pushed to `engineering` as `a073271` | 2026-10-19T10:45:36Z |
| Task branch pushed as `fbfa9aa` | 2026-10-19T10:45:42Z |
| Continuous integration green on `fbfa9aa` | 2026-10-19T10:46:05Z |

Six seconds separate the two pushes. One continuous-integration run fell inside the window and failed for it: run `39239750538` on `i00/e02/main`, started 2026-10-19T10:45:40Z, which is the base run for the parallel W03 merge (`#50`). It failed the catalogue test alone, because that base carried the design's new codes and not yet the schema's. Merging this unit into that base is what returns it to green.

A branch that has not yet taken this schema fails the catalogue test the same way and for the same reason until the change reaches it. `main` is in that state until the epic base merges.

## T1 The command's own suite

**Observes AC12.** Every outcome the command returns, and the code each diagnostic now carries.

```bash
cd prototype && uv run --frozen pytest
```

**Pass.** Exit 0. One hundred and four tests, the ninety-eight at the base among them. The six this task adds: four faults in the command line, a missing `--root`, and an output path naming an input source, each carrying `E_INVALID_USAGE`. Six tests changed from asserting a diagnostic carries no code to asserting which code it carries: the placeholder internal error as `E_UNEXPECTED_INTERNAL_ERROR`, two raw-HTML refusals as `E_RAW_HTML` and four construct refusals as `E_UNSUPPORTED_CONSTRUCT`. A source root naming no directory now asserts `E_ROOT_NOT_FOUND`, an entry suffix outside the profile `E_UNSUPPORTED_ENTRY_SUFFIX`, and a refused write `E_PUBLICATION_FAILED`.

At the base the same command reports 98 passed.

## T2 The catalogue held to the design, in both directions

**Observes AC12.** The schema's catalogue against the set of codes the design carries, with the tree made to carry each disagreement in turn.

```bash
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
```

**Pass.** Exit 0. One hundred and six tests, against the design at `a073271` and the schema at `fbfa9aa`. Eighty-six at the base; the twenty added are the schema's own cases for the seven new codes and the six new fixtures.

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

**Pass, as a measurement.** At `7f8fe64` the run reports **3 of 10 fixtures pass**. At `fbfa9aa` it reports **9 of 16 fixtures pass**. The six added are the six that pass:

```text
cli/diagnostics-format-unknown: pass
cli/fragment-only-reference-without-from: pass
cli/output-naming-an-input-source: pass
profile/entry-suffix-outside-the-profile: pass
profile/raw-html-in-selected-content: pass
profile/unsupported-construct: pass
```

Each declares a failure, and a failing run returns its status without reaching the bundling stage, so none of them waits on the emitter W04 delivers. The seven that still fail are the seven that declare a successful bundling or a resolved reference, and each fails on its exit status exactly as it did at the base. Their count is unchanged at 0 of 7.

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

**Pass.** Exit 0 from each. Ruff reports all checks passed over twenty files; mypy reports no issues in nineteen source files under `strict`; `uv lock --check` resolves twenty-two packages unchanged, since the change adds no dependency. The layout check reports fifty-two tracked files under `fixtures/`, eighteen more than the base's thirty-four. The vocabulary check reports thirty-four marked contract terms, unchanged: the design's new prose italicises no term. The link check resolves every reference in six documents; no heading was added to the design, so no anchor another document links to has moved.

## T5 Continuous integration on the exact head

**Observes AC12.** `make check` in full, on the branch's head, in the repository's own runner.

```bash
gh run list --repo m2ux/prosiform
gh run view <id> --repo m2ux/prosiform
```

**Pass.** Run `39239759699` on `fbfa9aa`, concluded `success` at 2026-10-19T10:46:05Z, the first run of the branch and the first after the design was pushed.
