# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by editing the working tree so that it carried one fault and nothing else, running the named command, and reverting the edit.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e01/w05-warning-diagnostics-and-every` |
| Tested revision | `8805d866dc37826b4088b55caa6f06405e509e33` |
| Contract revision | `b5f86bd` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0` |
| Date | 2026-10-19 |

The link check reaches addresses outside the repository and reads the tracker with the caller's credentials, and `uv run --frozen` builds the project into the environment it runs in. The sandbox available to this session has no network, so every run below was performed outside it.

## T1 The set, in one pass

**Observes AC7, AC8.** The repository's checks run together, the two this task changes among them.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order. The `ok` lines each check prints are omitted here; the verdicts are not.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.86ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
16 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 15 source files
cd prototype && uv run --frozen pytest
6 passed in 0.06s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
79 passed in 0.34s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 6 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The corpus suite runs seventy-nine tests where the base ran fifty-two: six are the new discovery suite, two extend the catalogue check, and nineteen are the schema's warning cases. The link check reads six documents where it read five. The vocabulary check is unchanged at thirty-four terms: *warning*, *severity* and *catalogue* are words this task uses and the design does not mark as contract terms, so the glossary neither gains nor needs a definition for one — and the glossary is now read by both checks, so a definition added to it would have to resolve as well as be used.

## T2 The schema's warning cases

**Observes AC7.** A manifest declaring a warning validates, a warning code outside the catalogue fails, and neither catalogue admits the other's codes.

```bash
make corpus
```

**Pass.** Exit 0, seventy-nine tests. The cases `checks/tests/test_manifest_schema.py` carries for this criterion:

| Case | Asserts |
| --- | --- |
| `test_a_manifest_declaring_a_warning_validates` | A manifest for a successful run carrying `severity = "warning"` and `code = "W_RESOURCE_PORTABILITY"` validates. |
| `test_every_code_in_the_warning_catalogue_is_accepted` | Each of the two codes the warning catalogue holds is accepted on a warning, parametrized over the catalogue the schema declares. |
| `test_an_unknown_warning_code_fails` | A warning naming `W_NOT_IN_THE_CATALOGUE` fails validation. |
| `test_an_error_naming_a_warning_code_fails` | An error diagnostic naming each warning code fails, parametrized over the warning catalogue. |
| `test_a_warning_naming_an_error_code_fails` | A warning diagnostic naming each of the twelve error codes fails, parametrized over the error catalogue. |
| `test_a_diagnostic_naming_no_severity_fails` | A diagnostic with no severity belongs to no catalogue and fails. |

The same comparison run directly against `manifests.errors`, so the rejection message is visible rather than only the verdict:

```text
error catalogue:   ['E_AMBIGUOUS_FILE_GROUP', 'E_AMBIGUOUS_SOURCE_HEADING', 'E_GENERATED_INPUT', 'E_HEADING_DEPTH_OVERFLOW', 'E_INVALID_GROUP_RULE', 'E_NESTED_SECTION_TARGET', 'E_PARSER_REFERENCE_LIMIT', 'E_SOURCE_OUTSIDE_ROOT', 'E_SOURCE_SYMLINK', 'E_TARGET_NOT_FOUND', 'E_UNSAFE_BUNDLE_BOUNDARY', 'E_UNTERMINATED_FRONTMATTER']
warning catalogue: ['W_EMPTY_GROUP_RULE', 'W_RESOURCE_PORTABILITY']

error    E_SOURCE_OUTSIDE_ROOT    VALIDATES
warning  W_RESOURCE_PORTABILITY   VALIDATES
error    W_RESOURCE_PORTABILITY   REJECTED
    expected.diagnostics.0.code: 'W_RESOURCE_PORTABILITY' is not one of ['E_AMBIGUOUS_FILE_GROUP', …, 'E_UNTERMINATED_FRONTMATTER']
warning  E_SOURCE_OUTSIDE_ROOT    REJECTED
    expected.diagnostics.0.code: 'E_SOURCE_OUTSIDE_ROOT' is not one of ['W_EMPTY_GROUP_RULE', 'W_RESOURCE_PORTABILITY']
```

`checks/runner.py` is unchanged by this task. It designates a diagnostic by its severity and its code together and compares the declared sequence in order, and nothing in that comparison reads a code's spelling, so a warning is compared as an error is. Its suite runs unchanged.

## T3 A catalogue against the design's text

**Observes AC7.** Each catalogue is exactly the set of codes the design declares under the prefix its severity uses.

```bash
make corpus
```

**Pass.** Exit 0. `test_a_catalogue_is_the_codes_the_design_declares` is parametrized over `error`/`E_` and `warning`/`W_`, reading `design.md` from the branch and path the root README's Design link names. `test_every_severity_a_diagnostic_may_carry_has_a_catalogue` holds the schema's severity enum to the catalogues the reader maps, so a severity added without a catalogue fails rather than leaving its code closed over nothing.

### T3a A warning code the design names that the schema omits

Fault: `W_EMPTY_GROUP_RULE` deleted from the schema's `warningCode` enum.

```bash
make corpus
```

**Pass** — the check failed as it must. Exit 1.

```text
________ test_a_catalogue_is_the_codes_the_design_declares[warning-W_] _________
>       assert catalogue(severity) == codes(prefix, design())
E       AssertionError: assert {'W_RESOURCE_PORTABILITY'} == {'W_EMPTY_GRO..._PORTABILITY'}
E         Extra items in the right set:
E         'W_EMPTY_GROUP_RULE'
1 failed, 76 passed in 0.34s
```

### T3b A warning code the schema carries that the design does not name

Fault: `W_SLOW_RUN` added to the schema's `warningCode` enum.

```bash
make corpus
```

**Pass** — the check failed as it must. Exit 1.

```text
________ test_a_catalogue_is_the_codes_the_design_declares[warning-W_] _________
>       assert catalogue(severity) == codes(prefix, design())
E       AssertionError: assert {'W_EMPTY_GRO... 'W_SLOW_RUN'} == {'W_EMPTY_GRO..._PORTABILITY'}
E         Extra items in the left set:
E         'W_SLOW_RUN'
1 failed, 80 passed in 0.36s
```

## T4 Discovery outside the corpus

**Observes AC8.** Every Markdown document git tracks outside a fixture is found, and no document inside one is.

```bash
make corpus
```

**Pass.** Exit 0. `checks/tests/test_documents.py` holds discovery to the tracked set: that every document found is Markdown git tracks, that no file inside a fixture is among them, that every tracked Markdown file outside a fixture is, that the set holds a document which is not a README, and that the READMEs the table check reads are exactly the documents named `README.md`. The six documents are the root, `checks/`, `docs/`, `fixtures/` and `prototype/` READMEs and `docs/glossary.md`.

### T4a The corpus swept in

Fault: the fixture exception removed from `checks/documents.py`, so discovery returns every tracked Markdown file.

```bash
make corpus
```

**Pass** — the check failed as it must. Exit 1, and the failure names every fixture file that entered.

```text
>       assert inside == set(), f"a fixture's own files entered the check: {sorted(inside)}"
E       AssertionError: a fixture's own files entered the check: ['fixtures/extraction/nested-section-target/expected/stdout.md', 'fixtures/extraction/nested-section-target/source/guide.md', 'fixtures/identity/whole-document/expected/stdout.md', 'fixtures/identity/whole-document/source/guide.md', 'fixtures/normalization/root-escape/expected/stdout.md', 'fixtures/normalization/root-escape/source/guide.md']
FAILED checks/tests/test_documents.py::test_no_document_inside_a_fixture_is_found
FAILED checks/tests/test_documents.py::test_every_tracked_document_outside_a_fixture_is_found
2 failed, 77 passed in 0.35s
```

Under the same fault the link check fails too, on the fixture that exists because its source escapes the source root. This is the exception stated as a run: a widened check that swept the corpus in fails by design, and the fixture that fails it is the one written to carry an unresolvable reference.

```bash
make links
```

```text
FAIL fixtures/normalization/root-escape/source/guide.md: ../outside.md — ../outside.md does not exist

link check: 1 unresolved reference(s)
```

## T5 The link check on the clean tree

**Observes AC8.** Every reference in every document outside the corpus resolves.

```bash
make links
```

**Pass.** Exit 0, six documents and nineteen distinct references. No fixture source is among them.

```text
link check: every reference in 6 document(s) resolved
```

The remote references the run reads are four issues and one user-owned project board, which the GitHub API answers with the caller's credentials, and eleven further addresses — three badge images, `commonmark.org`, the JSON Schema draft and six package pages.

`docs/glossary.md` carries no reference. Nothing in it was unresolved and nothing in it needed fixing: the defect the widening guards against is the reference it has yet to gain, which is now held from the moment it is written.

## T6 An unresolvable reference in a document that is not a README

**Observes AC8.** A reference that resolves to nothing fails the check, naming the document and the reference.

### T6a A path that does not exist

Fault: `The design is stated on the [engineering branch](engineering/design.md).` appended to `docs/glossary.md`.

```bash
make links
```

**Pass** — the check failed as it must. Exit 1.

```text
FAIL docs/glossary.md: engineering/design.md — engineering/design.md does not exist

link check: 1 unresolved reference(s)
```

### T6b A fragment no heading generates

Fault: `The checks are listed in the [README](../README.md#diagnostics).` appended to `docs/glossary.md`.

```bash
make links
```

**Pass** — the check failed as it must. Exit 1. The fragment is resolved against the headings of the document the path names, which is a README reached from a document that is not one.

```text
FAIL docs/glossary.md: ../README.md#diagnostics — no heading in ../README.md generates #diagnostics

link check: 1 unresolved reference(s)
```

## T7 The set in continuous integration

**Observes AC7, AC8.** The same named commands run on the pushed branch, so a check cannot hold on a working copy and be absent remotely.

[Run 39221364222](https://github.com/m2ux/prosiform/actions/runs/39221364222) on `8805d866dc37826b4088b55caa6f06405e509e33`.

**Pass.** Conclusion `success`. The job runs `make check` on `ubuntu-latest` with the full history the link and catalogue checks need to read `origin/engineering`, and the same verdicts as the local run:

```text
Resolved 22 packages in 0.71ms
All checks passed!
16 files already formatted
Success: no issues found in 15 source files
6 passed in 0.11s
79 passed in 0.86s
layout check: 3 tree(s) present
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The same set runs again on the epic base once the pull request merges. [Run 39221989302](https://github.com/m2ux/prosiform/actions/runs/39221989302) on `bf4ae98304ad1bd21e195112eb2ca966e7d39c4e`, the merge commit on `i00/e01/main`, concluded `success`. That revision's tree is identical to the tested head's, because the base carried no change between the branch point and the merge, so every run above is a run against the merged content.

## What these checks do not establish

- **No fixture has been run.** There is no build under test, so the corpus checks validate manifests and exercise the runner's comparison against synthetic runs. That a warning may be declared is established; that a run emits one is not, and cannot be until a build exists.
- **No fixture declares a warning.** The two warning codes are declarable and the schema's cases cover each, but no manifest in `fixtures/` names one. The clauses that emit them — a grouping rule that arranges nothing, and a bundle carrying a resource reference — are corpus content this row does not author.
- **The link check resolves addresses, not content.** A reference that answers resolves; whether the page it reaches says what the sentence around it claims is not checked.
