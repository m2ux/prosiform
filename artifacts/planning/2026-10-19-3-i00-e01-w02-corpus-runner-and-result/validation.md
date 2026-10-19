# Validation

The checks this task carries, as they were run. Every run below was performed; nothing is reported that was not observed. Where a check could not run, it says so and why.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e01/w02-corpus-runner-and-result` |
| Tested revision | `0e3d191ab39fc74632453ab99e05e78e708ca1ed` |
| Contract revision | `2d0ed50` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0` |
| Date | 2026-10-19 |

**No build of prosiform exists.** `prototype/src/prosiform/` is a docstring, and the compiler starts in E02. Nothing below runs a fixture against the tool. What the runner's tests exercise is the comparison: a fixture written for the run that reads it, a build under test that is a canned program, and the verdict the two produce. A fixture's result against a real build is a thing only a real build can produce, and the runner refuses to return one without a configured command.

The lint, format, type and test commands ran with network access, because `uv run --frozen` builds the project into the environment it runs in, and `make links` ran with network access and GitHub credentials. The sandbox available to this session has no network, so those runs were performed outside it.

## The set, in one pass

**Observes AC2, AC3.** The repository's checks run together, the corpus's own among them.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `links` and `vocabulary` in that order.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.79ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
13 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 12 source files
cd prototype && uv run --frozen pytest
6 passed in 0.02s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
52 passed in 0.33s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/links.py --online
link check: every reference resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The corpus suite is thirty tests from W01 and twenty-two added here. The vocabulary check is unchanged at thirty-four terms: *runner*, *expectation* and *difference* are words this task uses and the design does not mark as contract terms, so the glossary neither gains nor needs a definition for one.

The named link command reads `README.md` alone, so the other four READMEs were checked by passing them to the script, and every reference in each resolved.

```bash
python3 checks/links.py --online fixtures/README.md checks/README.md docs/README.md prototype/README.md
```

```text
link check: every reference resolved
```

## The set, in continuous integration

**Observes AC2, AC3.** The same command the developer calls runs on the branch.

Recorded after the pull request's check completed; see [Continuous integration](#continuous-integration-result).

## T1 A fixture decided from its manifest and files

**Observes AC2.** The runner reads one fixture's manifest, runs the configured build against its source tree, and returns a verdict from the declaration and the fixture's files.

```bash
make corpus
```

**Pass.** Exit 0, fifty-two tests. `checks/tests/test_runner.py` writes each fixture it uses into a temporary directory — manifest, source tree and expected bytes — and validates it against the corpus schema before the run, so every fixture the runner is exercised on is a fixture the schema describes.

```text
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
....................................................                     [100%]
52 passed in 0.33s
```

| Case | Test |
| --- | --- |
| A success fixture whose run matches passes | `test_a_passing_fixture_is_decided_from_its_manifest` |
| A failure fixture whose run matches, diagnostic included, passes | `test_a_failure_fixture_is_decided_from_its_manifest` |
| A diagnostic carrying a message and a remedy the manifest does not declare still matches | `test_a_diagnostic_carrying_more_than_the_manifest_declares_passes` |
| The run receives `--root` resolved to an absolute path, `--diagnostics json`, and then the manifest's arguments in order | `test_the_run_receives_the_allowed_root_and_the_diagnostic_format` |
| A fixture is identified by its path under the corpus | `test_a_fixture_is_identified_by_its_path_under_the_corpus` |

## T2 The build under test, named by configuration

**Observes AC2.** The build is configuration, not knowledge the runner carries, and an absent one is refused rather than passed.

```bash
make corpus
```

**Pass.** Exit 0.

| Case | Test |
| --- | --- |
| One fixture, two configured builds, two verdicts, and neither program is the tool | `test_the_verdict_follows_the_configured_build` |
| An unset or blank `PROSIFORM_BUILD` raises `BuildNotConfigured` | `test_an_unconfigured_build_is_refused` |
| A fixture the schema does not describe is refused, and the configured build is never invoked | `test_a_malformed_fixture_is_refused_without_invoking_the_build` |
| `checks/runner.py` carries no language or ecosystem name | `test_the_runner_names_no_implementation_or_language` |

**Observed against the corpus's own fixtures.** With `PROSIFORM_BUILD=/bin/true` — a program that is not prosiform and reads none of its arguments — two corpus fixtures were run and reported. The run states what the configured build produced; it establishes nothing about either fixture's expectations beyond that they were compared.

```text
normalization/root-escape: fail
  expected.exit_status: expected 1, the run exited 0
  expected.diagnostics: the run emits 0 diagnostics where 1 diagnostic is expected
    position 1: error E_SOURCE_OUTSIDE_ROOT expected, the run emits none

identity/whole-document: fail
  expected.stdout: the bytes differ
    186 bytes expected, 0 produced
    first difference at byte 0, expected line 1 column 1
    expected b'This bundle was built fo'
    produced b''
    the run's output ends 186 bytes early
```

**Refused with no build.** The same call with `PROSIFORM_BUILD` removed raises rather than returning a verdict.

```text
BuildNotConfigured: PROSIFORM_BUILD names the build under test; a fixture has no result without one
```

## T3 A difference located in each expectation kind

**Observes AC3.** A mismatch names the expectation that differed and locates the difference inside it. Each case below asserts on the located region, not merely on the verdict.

```bash
make corpus
```

**Pass.** Exit 0.

| Expectation | Case | Test |
| --- | --- | --- |
| `expected.exit_status` | The status expected and the status returned | `test_a_differing_exit_status_names_the_expectation` |
| `expected.stdout` | Byte offset, line and byte column, and a window of each side | `test_differing_stdout_bytes_are_located` |
| `expected.stdout` | Bytes differing only in newline spelling, CRLF against LF | `test_stdout_differing_only_in_newline_spelling_is_located` |
| `expected.stdout` | A missing trailing newline, reported as output ending early | `test_stdout_missing_its_trailing_newline_is_located` |
| `expected.stdout` | Output carrying bytes beyond the expected end | `test_stdout_carrying_more_than_expected_is_located` |
| `expected.diagnostics` | One expected diagnostic the run does not emit, by position | `test_a_missing_diagnostic_is_reported` |
| `expected.diagnostics` | One the run emits that no expectation declares, by position | `test_an_extra_diagnostic_is_reported` |
| `expected.diagnostics` | The expected diagnostics in another order, with both orders | `test_diagnostics_out_of_order_are_reported` |
| `expected.diagnostics` | A diagnostic carrying another code, by position | `test_a_diagnostic_carrying_another_code_is_reported` |
| `expected.diagnostics` | A declared field carrying another value, and a declared field absent | `test_a_declared_diagnostic_field_that_differs_is_reported` |
| `expected.diagnostics` | A standard error line that is not a JSON diagnostic | `test_a_standard_error_line_that_is_not_a_diagnostic_is_reported` |
| all three | Every expectation differing at once, each named in the report | `test_every_expectation_that_differed_is_reported` |
| `invocation` | A run that does not complete within the configured bound | `test_a_run_that_does_not_complete_is_reported` |

The newline case is the one the preservation invariant turns on, and the assertion is on the rendered windows rather than on a verdict:

```text
first difference at byte 7, expected line 1 column 8
expected b'# Guide\r\n'
produced b'# Guide\n'
```

**The comparison is bytes, not text.** The CRLF case fails if either side is decoded before comparison, because a text comparison that normalizes newlines reports two identical lines.

## T4 The runner read for implementation-specific assumptions

**Observes AC2.** A test can only catch the names it was told about, so the module was read line by line for anything it assumes about what it invokes.

| Read | Finding |
| --- | --- |
| Imports | `json`, `os`, `shlex`, `subprocess`, `dataclasses`, `pathlib`, `typing`, and `manifests`, the corpus's own reader. No package under test is imported, and nothing is imported conditionally. |
| Flags written | `--root` and `--diagnostics json`, and nothing else. Both are the design's own command line, which every implementation honours, and W01 settled that the runner supplies them. Everything else on the command line comes from the manifest's `arguments`. |
| Invocation | The configured value is split as a shell splits a command line, so a build reached through an interpreter, a wrapper or a release binary is named the same way. The runner does not assume the build is one executable, nor where it lives. |
| Standard output | Read as bytes and never decoded, including in the report, where a window is rendered with its control bytes spelled out. |
| Standard error | Split into lines and parsed as JSON, which the declared format defines as UTF-8. A line that does not parse is reported as a line that does not parse, not assumed away. |
| Diagnostic matching | On `severity` and `code` as values, and on the further fields the manifest declares. No message text, no wording, no field ordering, and no mapping from an exit status to a code. |
| The catalogue | The runner enumerates no error code. A diagnostic's name is built from the values the run and the manifest carry, so W05 adding warning codes to the schema needs no change here. |
| Exit status | Compared as the integer the manifest declares. The runner does not know the contract's five categories; the schema does. |
| Working directory | The fixture directory, with `--root` passed absolute, so resolution does not depend on where the runner was invoked from. |

**Finding: none.** No implementation-specific assumption was found. One contract-level obligation is deliberate and recorded: whatever configuration names must accept `--root DIR` and `--diagnostics json`. That is the contract every build implements, not a property of one of them.

**The mechanical guard.** `test_the_runner_names_no_implementation_or_language` reads `checks/runner.py` and fails on any of `python`, `pytest`, `pyproject`, `prototype`, `cargo`, `rust`, `node`, `npm`, `src/prosiform` or `import prosiform`. The module carries no shebang, so the guard is not satisfied trivially. `PROSIFORM_BUILD` names the product, which both builds are, rather than an implementation of it.

## Continuous integration result

Recorded below once the pull request's Checks run completed.

## What the checks do not establish

- **No fixture is executed against the tool.** No build exists. The runner's tests exercise its comparison against a canned program, and the two corpus fixtures run under T2 were run against `/bin/true` to show a located difference, not to establish a result.
- **`identity/whole-document`'s expected bytes remain unverified.** They are W01's reading of the design, and this task gives no reason to doubt that reading: the entry line, the file heading carrying the root-relative path without its Markdown extension, the absorbed title and the unshifted `## Run` are each what the design's clauses describe. Nothing here confirms them, and nothing here was adjusted to make a comparison pass. The first real confirmation is the walking skeleton in E02.
- **A warning expectation cannot be written yet.** The schema's catalogue is closed over `E_` codes, which is W05's row. The comparison needs no change when it opens: severity is already half of what a diagnostic is matched on.
- **The command line is split as a POSIX shell splits one.** The corpus runs on POSIX hosts; a Windows host would need another splitting rule.
- **The whole corpus is not yet run on each change.** `make corpus` runs the manifest validation and the runner's own cases. Running every fixture against a configured build is W03.
