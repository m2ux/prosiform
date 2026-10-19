# Validation — I00:E07:W01

Procedure, tested revision and observations for the checks the pull request's Test Plan cites. Every run below was performed and its output is the output it produced. The failing case was produced by making the tree carry one fault and nothing else, running the command, recording its output, and reverting.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e07/w01-installation-and-stable-entry` |
| Tested revision | `f555f90` |
| Base revision | `c0ee1ef` on `i00/e07/main` |
| Contract revision | `b83877c` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Continuous-integration job | `Checks`, `.github/workflows/checks.yml`, on `ubuntu-latest` |
| Build under test | the wheel this change builds, installed into a throwaway environment and invoked by name |
| Run from | the repository root |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0`, `markdown-it-py 4.2.0` |
| Date | 2026-10-19 |

## The run AC1 names

The command is resolved by name in the installed environment's executable directory and invoked from a temporary working directory, against a source root written beside it. The invoked process carries `PATH` holding that one directory and `HOME` holding the working directory, and no other variable of the run.

```bash
prosiform --version
prosiform --root <workspace>/sources guide.md
```

Exit 0 for both, nothing on standard error, and standard output carrying the version response and the bundle below.

```text
prosiform 0.0.0 (skill-markdown-v1)
```

```markdown
This bundle was built for [guide](#guide); everything else is material it references.

# guide

The installed command bundles this document.
```

## T1 The installation smoke run

**Observes AC1.** The wheel builds, an environment installs it, the command resolves in that environment and outside the repository, and from an unrelated working directory it reports the profile identifier and bundles a reference from a source root the repository does not hold.

```bash
make smoke
```

**Pass.** Exit 0 at `f555f90`.

```text
ok   wheel        prosiform-0.0.0-py3-none-any.whl
ok   installed    /tmp/prosiform-smoke-xvjxwoyt/environment
ok   resolved     prosiform — /tmp/prosiform-smoke-xvjxwoyt/environment/bin/prosiform, outside the repository
ok   version      prosiform 0.0.0 (skill-markdown-v1)
ok   bundled      guide.md from /tmp/prosiform-smoke-xvjxwoyt/sources, run from /tmp/prosiform-smoke-xvjxwoyt/elsewhere
ok   glossary     glossary.md, shipped

smoke check: prosiform installs into an environment and bundles a reference from a source root, resolved by name outside the repository
```

**An entry point only a checkout resolves fails the run.** Observed by deleting the `[project.scripts]` table from `prototype/pyproject.toml`, running the check, and reverting. The package still imports and the module still runs from the checkout; what the installation no longer carries is a name to resolve.

```text
FAIL the installed environment names no prosiform command, so a caller has nothing to resolve by name

smoke check: the installation does not stand
ok   wheel        prosiform-0.0.0-py3-none-any.whl
ok   installed    /tmp/prosiform-smoke-5c5i3yed/environment
```

Exit 1 from the script, exit 2 from make. The two steps that did hold are printed, so the run names the step that failed rather than the check.

## T2 The command tables

**Observes AC1.** The target that proves the entry point is documented where the repository's other commands are, in both directions.

```bash
make tables
```

**Pass.** Exit 0 at `f555f90`. Thirteen commands, where the base declares twelve.

```text
ok   command     make smoke — README.md
ok   command     make smoke — checks/README.md

table check: 13 command(s) and 7 declaration(s), each declared by the project and named by a table
```

## T3 The whole gate

**Observes AC1.** Every check the repository declares, the smoke run among them in the order `make check` names.

```bash
PROSIFORM_BUILD="uv run --project <workspace>/prototype --frozen prosiform" make check
```

**Pass.** Exit 0 at `f555f90`.

```text
All checks passed!
27 files already formatted
Success: no issues found in 26 source files
248 passed in 0.13s
175 passed in 0.43s
corpus check: 40 fixture(s), 38 pass, 0 fail, 2 awaited, 0 unexpected pass
smoke check: prosiform installs into an environment and bundles a reference from a source root, resolved by name outside the repository
layout check: 3 tree(s) present
table check: 13 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 23 source(s)
```

The corpus is unchanged at forty fixtures: this unit adds no fixture, because the corpus runs a build named by configuration and an installation is not a thing a fixture can name.

## What the smoke run does not observe

Each of these is declared `awaiting = "I00:E10"`.

| Case | Why the run cannot observe it |
| --- | --- |
| Installation on another platform | The run observes this host and the `ubuntu-latest` runner. A Windows script wrapper and its path resolution are a different mechanism. |
| A machine that never held the repository | The repository exists on disk during the run and is merely unreachable by path, working directory and environment. Removing it is not something a check inside it can do. |
| The documented `pip install ./prototype` route | The run installs a built wheel, which is what an environment receives either way, but the command line the README gives a reader is not the one executed. |

## The version the entry point reports

The runs above were performed at `f555f90`, where the project definition still carried the placeholder `0.0.0` and the command reported `prosiform 0.0.0 (skill-markdown-v1)`. [#67](https://github.com/m2ux/prosiform/pull/67) raises it to `0.1.0`, merged into `i00/e07/main` at `8a08e4f`, and the smoke run at `db42849` reports `prosiform 0.1.0 (skill-markdown-v1)`. The profile identifier is unchanged and is what a caller reads to know which contract it is talking to.

The version response is compared with the whole literal in `tests/test_cli.py`, so the number is declared in the project definition and read back where a caller reads it: raising one without the other fails the suite rather than reaching a release.

## The three cases awaiting I00:E10

They are raised as [#68](https://github.com/m2ux/prosiform/issues/68) and placed as row W04 of [#9 I00:E10](https://github.com/m2ux/prosiform/issues/9), covering that epic's AC7. The conformance report's declared-surface listing already names each exit status no fixture can reach with its reason; an installation claim no fixture can reach is the same kind of statement, and the report is where it is read rather than this record.
