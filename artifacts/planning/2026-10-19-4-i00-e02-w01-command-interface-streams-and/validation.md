# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by editing the working tree so that it carried one fault and nothing else, running the named command, recording the output, and reverting the edit.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e02/w01-command-interface-streams-and` |
| Tested revision | `7b63a3ece03595758c92635ab2848520b3d8b7a1` |
| Contract revision | `fd87030` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0` |
| Build under test | `prototype/.venv/bin/prosiform`, named to the corpus runner as `PROSIFORM_BUILD` |
| Date | 2026-10-19 |

The link check reaches addresses outside the repository and `uv run --frozen` builds the project into the environment it runs in. The sandbox available to this session has no network and no write access to the `uv` cache, so every `make` run below was performed outside it; the corpus runs, which invoke an already-installed command, were performed inside it.

## T1 The set, in one pass

**Observes AC3, AC4.** The repository's checks run together, over a tree the command now carries.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order. The per-item `ok` lines each check prints are omitted; the verdicts are not.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.73ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
19 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 18 source files
cd prototype && uv run --frozen pytest
48 passed in 0.06s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
82 passed in 0.36s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 6 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The build's suite runs forty-eight tests where the base ran six; the forty-two are the command's. The corpus suite runs eighty-two where the base ran seventy-nine; the three are the schema validation of the three fixtures this task adds. The table check is unchanged at eleven commands and seven declarations: a console entry point is neither a `Makefile` target nor a dependency. The vocabulary check is unchanged at thirty-four terms: *validation-only run*, *entry reference* and *diagnostic format* are phrases the design writes without marking as contract terms, so the glossary neither gains nor needs a definition for one, and a definition added for one would fail the check from the other side.

## T2 The grouping-rule fixtures against the build

**Observes AC3, AC4.** Each fixture this task adds, run against the build under test and compared with its manifest.

```bash
PROSIFORM_BUILD=…/prototype/.venv/bin/prosiform python run_corpus.py cli
```

`run_corpus.py` is six lines over `checks.runner.run_fixture`, the comparison the corpus runner performs; running every fixture against the build on each change is W06, the last row of this epic. The runner supplies `--root`, resolved to an absolute path, and `--diagnostics json`.

**Pass.** Three fixtures, three passes.

```text
cli/group-rule-depth: pass
cli/group-rule-repeated-slug: pass
cli/group-rule-unknown-slug: pass
```

Each compares three things at once, so a pass is a statement about all three: the exit status is the one the manifest declares, standard output is byte-identical to an empty file, and standard error carries exactly one JSON object whose severity and code are `error` and `E_INVALID_GROUP_RULE`. A line on standard error that is not a JSON object is reported as one by the runner, so the pass also establishes that nothing but JSON reaches that stream under `--diagnostics json`.

| Fixture | Invocation beyond the supplied root and format | Status |
| --- | --- | --- |
| `cli/group-rule-depth` | `--group docs:9 guide.md` | 2 |
| `cli/group-rule-repeated-slug` | `--group docs:2 --group docs:3 guide.md` | 2 |
| `cli/group-rule-unknown-slug` | `--group references:2 guide.md` | 1 |

### The three fixtures already in the corpus

`identity/whole-document`, `extraction/nested-section-target` and `normalization/root-escape` each expect bundling. Run against this build they fail on their exit status, which is the state the epic's plan puts them in until W02 through W04 make them pass. They are unedited by this task. The same command over the whole corpus:

```text
extraction/nested-section-target: fail
  expected.exit_status: expected 1, the run exited 4
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_NESTED_SECTION_TARGET expected, error (no code) produced
identity/whole-document: fail
  expected.exit_status: expected 0, the run exited 4
  expected.stdout: the bytes differ
    186 bytes expected, 0 produced
normalization/root-escape: fail
  expected.exit_status: expected 1, the run exited 4
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_SOURCE_OUTSIDE_ROOT expected, error (no code) produced
```

### Deliberate fault: the unknown slug returning the usage status

The refusal for a slug naming no directory under the allowed source root was changed from the input-failure status to the usage-failure status, and the fixtures were run again.

```text
cli/group-rule-depth: pass
cli/group-rule-repeated-slug: pass
cli/group-rule-unknown-slug: fail
  expected.exit_status: expected 1, the run exited 2
    exit status: 2
    stdout: b''
    stderr: b'{"severity": "error", "message": "the grouping rule for \'references\' names no directory under the allowed source root", "code": "E_INVALID_GROUP_RULE", "remedy": "run prosiform --help for usage"}\n'
```

One fixture fails and the two whose status is unaffected pass, so the fixture discriminates the status rather than the code. The same fault fails one unit test and no other:

```text
FAILED tests/test_cli.py::test_a_grouping_slug_naming_no_directory_is_an_input_failure
1 failed, 47 passed in 0.06s
```

The edit was reverted.

### Deliberate fault: progress prose on standard output

One line of progress prose was written to standard output before the grouping rules are read, which is the thing the stream split exists to forbid.

```text
cli/group-rule-depth: fail
  expected.stdout: the bytes differ
    0 bytes expected, 29 produced
    first difference at byte 0, expected line 1 column 1
    expected b''
    produced b'reading 1 entry referenc'
    the run's output carries 29 bytes beyond the end
cli/group-rule-repeated-slug: fail
  expected.stdout: the bytes differ
    0 bytes expected, 29 produced
cli/group-rule-unknown-slug: fail
  expected.stdout: the bytes differ
    0 bytes expected, 29 produced
```

All three fail, each on standard output and on nothing else: the status and the diagnostic are still the declared ones, and the only difference is the twenty-nine bytes that reached the stream the bundle owns. Six unit tests fail with them:

```text
FAILED tests/test_cli.py::test_a_run_the_build_cannot_carry_out_returns_the_internal_error_status
FAILED tests/test_cli.py::test_a_validation_only_run_publishes_nothing
FAILED tests/test_cli.py::test_a_validation_only_run_with_an_output_file_creates_no_file
FAILED tests/test_cli.py::test_a_failing_run_writes_its_diagnostics_as_data
FAILED tests/test_cli.py::test_a_failing_run_writes_its_diagnostics_as_text
6 failed, 42 passed in 0.07s
```

The edit was reverted.

## T3 The command's grammar, streams and statuses

**Observes AC3, AC4, AC10.** The build's own suite, which carries the cases a fixture cannot reach.

```bash
make test
```

**Pass.** Exit 0, forty-eight tests, forty-two of them the command's. What they hold:

| Case | Asserts |
| --- | --- |
| `test_the_version_response_names_the_version_and_the_profile` | `--version` returns 0, standard output carries `prosiform 0.0.0 (skill-markdown-v1)` and nothing else, and standard error is empty. |
| `test_the_help_response_shows_usage_defaults_and_exit_statuses` | `--help` returns 0 and its response carries the usage line, the diagnostic format's default, and each of the five exit statuses. |
| `test_an_informational_response_needs_no_source_root` | Neither informational option requires `--root`. |
| `test_every_option_the_contract_declares_is_accepted` | One invocation naming `--root`, `--from`, `--output`, `--group`, `--check`, `--diagnostics` and an entry reference is a valid command line. |
| `test_an_option_the_contract_does_not_declare_is_refused` | Each of `--max-files`, `--max-output-bytes`, `--max-nesting`, `--manifest` and `--watch` is invalid usage. |
| `test_a_missing_source_root_is_invalid_usage` | A run with no `--root` returns 2 and publishes nothing. |
| `test_a_run_naming_no_entry_reference_is_invalid_usage` | A run with no positional reference returns 2. |
| `test_a_fragment_only_reference_needs_a_referring_document` | `#a-section` without `--from` returns 2 and the diagnostic names `--from`. |
| `test_a_fragment_only_reference_with_a_referring_document_is_valid` | The same reference with `--from` is a valid command line. |
| `test_a_grouping_depth_outside_one_through_six_is_invalid_usage` | Depths 0, 7, 9 and 60 each return 2 with one `E_INVALID_GROUP_RULE`. |
| `test_a_grouping_depth_at_the_boundary_is_accepted` | Depths 1 and 6 are valid. |
| `test_a_malformed_grouping_rule_is_invalid_usage` | `docs`, `docs:`, `:2`, `docs:two` and `a/b:2` each return 2 with that code. |
| `test_a_slug_named_by_two_grouping_rules_is_invalid_usage` | A slug given twice returns 2 with that code. |
| `test_a_grouping_slug_naming_no_directory_is_an_input_failure` | A slug naming no directory under the root returns 1 with that code. |
| `test_a_source_root_naming_no_directory_is_an_input_failure` | A `--root` naming no directory returns 1 and publishes nothing. |
| `test_a_usage_failure_is_reported_before_an_input_failure` | A run carrying both faults returns 2. |
| `test_a_diagnostic_format_the_contract_does_not_declare_is_invalid_usage` | `yaml`, the empty string, `TEXT` and `jsonl` each return 2. |
| `test_an_output_path_naming_an_input_source_is_invalid_usage` | An `--output` resolving to a positional reference's document returns 2. |
| `test_an_output_path_naming_the_referring_document_is_invalid_usage` | An `--output` resolving to `--from`'s document returns 2. |
| `test_an_output_path_naming_no_input_source_is_accepted` | An `--output` elsewhere is a valid command line. |
| `test_standard_output_is_the_default_output_destination` | `--output -` and no `--output` reach the same outcome. |
| `test_a_run_the_build_cannot_carry_out_returns_the_internal_error_status` | A valid run naming an entry reference returns 4, publishes nothing, and emits one error diagnostic carrying no code. |
| `test_a_validation_only_run_publishes_nothing` | `--check` writes nothing to standard output. |
| `test_a_validation_only_run_with_an_output_file_creates_no_file` | `--check --output FILE` is not refused as a combination, writes nothing to standard output, and leaves `FILE` absent. |
| `test_a_refused_write_is_a_publication_failure` | A standard output that raises on every write turns the informational response into status 3. |
| `test_a_failing_run_writes_its_diagnostics_as_data` | Under `--diagnostics json` standard error parses as JSON objects whose keys are the contract's fields. |
| `test_a_failing_run_writes_its_diagnostics_as_text` | Under the default format the same diagnostic opens with its code. |

## T4 The statuses as a process returns them

**Observes AC3, AC4, AC10.** The installed command, run as a process, for the statuses a fixture cannot express.

```bash
prototype/.venv/bin/prosiform --version
prototype/.venv/bin/prosiform --help > /dev/full
prototype/.venv/bin/prosiform --diagnostics json --help > /dev/full
prototype/.venv/bin/prosiform --root . --check --output /tmp/bundle-should-not-exist.md --diagnostics json README.md
```

**Pass.** Each run's status is the one its outcome declares.

```text
prosiform 0.0.0 (skill-markdown-v1)
exit 0

error: standard output refused the response: [Errno 28] No space left on device
exit 3

{"severity": "error", "message": "standard output refused the response: [Errno 28] No space left on device"}
exit 3

{"severity": "error", "message": "this build carries no compilation stage, so the entry references it was given cannot be bundled", "remedy": "use a build that carries one"}
exit 4
ls: cannot access '/tmp/bundle-should-not-exist.md': No such file or directory
```

`/dev/full` accepts an open and refuses every write with `ENOSPC`, so the third status is produced by a write the stream genuinely refused rather than by a stream object written for the test. The run that asked for JSON received JSON, which is what makes the stream usable by a caller that parses it: a publication failure does not fall back to prose.

The fourth run is a validation-only run with an output file. It returns 4 because the stage it needs is absent from this build; it is recorded here for what it does publish, which is nothing — no bytes on standard output, and no file at the path `--output` named.

## T5 Continuous integration

**Observes AC3, AC4.** `make check` on the pushed head, run by the workflow the repository declares.

See the pull request's checks on `7b63a3e`. The workflow runs `make check`, the same set and the same order as T1, on a runner that creates its environment from the lockfile.

## What these checks do not observe

- **AC3, the bundle itself.** The stream discipline is observed on every run this build can make — the response on standard output and nothing else, the diagnostic on standard error and nothing else, standard output empty on every failing run. That the thing on standard output is a bundle cannot be observed until something compiles one, which W04 delivers.
- **AC10, the bundling and validating half.** A validation-only run reaches the absent compilation stage, so no run exists that bundles and validates entry references. The pull request carries a test-plan row with an empty Test cell naming it.
- **AC4, statuses 3 and 4 as corpus fixtures.** Both are observed, by T3 and T4, and neither is expressible in a manifest. A manifest's diagnostic draws its code from the catalogue the design declares, and the design names no code for an unexpected internal error; a refused write is not reachable through a runner that reads both streams to completion.
