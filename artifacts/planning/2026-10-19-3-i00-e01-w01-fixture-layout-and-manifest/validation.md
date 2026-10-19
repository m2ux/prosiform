# Validation

The checks this task carries, as they were run. The corpus command was run against the tree as written and against a tree deliberately broken in each way the schema forbids, so a pass is known to mean something. Every run below was performed; nothing is reported that was not observed.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e01/w01-fixture-layout-and-manifest` |
| Tested revision | `483f06d49ff5ba36d5df34c967d1b5478d0a3203` |
| Contract revision | `5905fe7` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0` |
| Date | 2026-10-19 |

The lint, format, type and test commands ran with network access, because `uv run --frozen` builds the project into the environment it runs in, and `make links` ran with network access and GitHub credentials. The sandbox available to this session has no network, so those runs were performed outside it.

Nothing here executes a fixture. No build of prosiform exists, so a fixture's expected bytes are a reading of the design rather than an observed result; the runner W02 delivers is what first compares them. This task's checks establish that a fixture is declared in the shape the schema describes, not that any implementation satisfies one.

## The set, in one pass

**Observes AC1, AC5.** The repository's checks run together with the corpus's own among them.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `links` and `vocabulary` in that order.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.82ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
11 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 10 source files
cd prototype && uv run --frozen pytest
6 passed in 0.02s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
30 passed in 0.04s
python3 checks/layout.py
ok   fixtures/ — 11 tracked file(s), the language-neutral fixture corpus
layout check: 3 tree(s) present
python3 checks/links.py --online
link check: every reference resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The layout check counts eleven tracked files under `fixtures/`, so the corpus tree holds real content and the check still passes. The vocabulary check is unchanged at thirty-four terms: *fixture*, *manifest* and *catalogue* are words this task uses and the design does not mark as contract terms, so the glossary neither gains nor needs a definition for one.

## T1 Schema validation over a complete declaration

**Observes AC1.** A manifest declaring its source tree, its invocation, its expected standard output, its expected exit status and its expected diagnostics validates, and one leaving out any of the five does not.

```bash
make corpus
```

**Pass.** Exit 0, thirty tests. `checks/tests/test_manifest_schema.py` holds the five cases as one parametrised test, one per declaration, alongside the complete manifest it removes each from.

```text
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
..............................                                           [100%]
30 passed in 0.04s
```

**Fails on a manifest missing a declaration.** With a fixture added at `fixtures/identity/broken/` whose manifest omits `expected.exit_status`, the command exits nonzero and names the fixture and the absent field.

```text
>       assert errors(manifest) == []
E       assert ["expected: '...red property"] == []
E         Left contains one more item: "expected: 'exit_status' is a required property"
FAILED checks/tests/test_corpus.py::test_a_fixture_manifest_matches_the_schema[identity/broken]
1 failed, 30 passed in 0.04s
```

**Fails on a manifest naming a path its fixture does not hold.** The schema states a path's shape; the check also requires the fixture to carry what the path names.

```text
E         Left contains 2 more items, first extra item: 'invocation.root: absent is not a directory'
FAILED checks/tests/test_corpus.py::test_a_fixture_manifest_matches_the_schema[identity/broken]
1 failed, 30 passed in 0.04s
```

## T2 Schema validation over the catalogue

**Observes AC5.** A manifest naming an error code outside the declared catalogue fails validation, and every code inside it is accepted.

```bash
make corpus
```

**Pass.** Exit 0. `test_an_unknown_error_code_fails` rejects `E_NOT_IN_THE_CATALOGUE`, and `test_every_code_in_the_catalogue_is_accepted` is parametrised over all twelve codes, so the rejection is known to be the catalogue rather than the shape of the field.

**Fails on a fixture expecting a code the contract does not define.** With `fixtures/identity/broken/` naming `E_INVENTED_BY_THE_FIXTURE`, the command exits nonzero and names the code and the catalogue it is absent from.

```text
E         Left contains one more item: "expected.diagnostics.0.code: 'E_INVENTED_BY_THE_FIXTURE' is not one of ['E_AMBIGUOUS_FILE_GROUP', 'E_AMBIGUOUS_SOURCE...RCE_OUTSIDE_ROOT', 'E_SOURCE_SYMLINK', 'E_TARGET_NOT_FOUND', 'E_UNSAFE_BUNDLE_BOUNDARY', 'E_UNTERMINATED_FRONTMATTER']"
FAILED checks/tests/test_corpus.py::test_a_fixture_manifest_matches_the_schema[identity/broken]
1 failed, 30 passed in 0.04s
```

## T3 The catalogue against the design

**Observes AC5.** The catalogue is the set of error codes the design declares, not a list authored beside it.

```bash
make corpus
```

**Pass.** Exit 0. `test_the_catalogue_is_the_codes_the_design_declares` reads the design from the branch and path the README's Design link names, collects every `E_`-prefixed code it carries, and requires the schema's enumeration to equal that set exactly. The observed set is the twelve the planning decision records.

**Fails on a catalogue that drifts.** With `E_NOT_IN_THE_DESIGN` added to the schema's enumeration, the command exits nonzero and names the extra member.

```text
E         Extra items in the left set:
FAILED checks/tests/test_catalogue.py::test_the_catalogue_is_the_codes_the_design_declares
1 failed, 30 passed in 0.04s
```

Each deliberately broken tree was restored and `make corpus` run again, returning exit 0 and thirty passing tests.

## Where each code comes from

Every member of the catalogue is a code the design names, and the clause it appears under is why it exists. The table sits in [`fixtures/README.md`](https://github.com/m2ux/prosiform/blob/main/fixtures/README.md) and in [w01.md](w01.md), and T3 is the mechanical form of the same claim.

## What the checks do not establish

- **No fixture is executed.** No build exists, so an expected bundle's bytes rest on a reading of the design. W02's runner is where they are first compared against a result.
- **The catalogue is closed over errors only.** The design describes a grouping rule that arranges nothing and the portability of a resource reference as warnings on standard error, and names a code for neither. A warning diagnostic therefore cannot be declared in a fixture, and no code was invented to make one declarable.
