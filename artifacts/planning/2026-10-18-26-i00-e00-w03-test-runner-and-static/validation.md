# Validation

The eight named commands this task carries, as they were run. Each was run twice: once on the tree as written, and once on a tree deliberately broken in the way the command's check forbids, so a pass is known to mean something. Every run below was performed; nothing is reported that was not observed.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e00/w03-test-runner-and-static` |
| Tested revision | `ad6f9e697ac7e38d6ddb7703bae7d2169b00303f` |
| Contract revision | `2c562fb` on `engineering`, which the vocabulary check reads as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `ruff 0.17.1`, `mypy 2.4.0` |
| Date | 2026-10-18 |

The lint, format and type commands ran with network access, because `uv run --frozen` builds the project into the environment it runs in, and the link command ran with network access and GitHub credentials, because it reaches addresses outside the repository. The sandbox available to this session has no network, so those runs were performed outside it.

## The set, in one pass

**Observes AC3.** Tests, lint, format and type checks each run from one documented command.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `layout`, `links` and `vocabulary` in that order, each reporting its own result.

```text
cd prototype && uv lock --check
Resolved 16 packages in 1ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
6 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 5 source files
cd prototype && uv run --frozen pytest
......                                                                   [100%]
6 passed in 0.02s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/links.py --online
link check: every reference resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

Make stops at the first recipe that exits nonzero, and each failing run below shows it naming the target that failed, so the check that produced a failure is read from the runner's own output.

## T1 Test command

**Observes AC3.** The test command discovers and reports the build's suite.

```bash
make test
```

**Pass.** Exit 0, six tests.

```text
cd prototype && uv run --frozen pytest
......                                                                   [100%]
6 passed in 0.02s
```

**Fails on a failing test.** With one deliberately false assertion appended to `prototype/tests/test_profile.py`, the command exits nonzero and names the test.

```text
>       assert profile().render("plain\n") == "deliberately wrong"
E       AssertionError: assert '<p>plain</p>\n' == 'deliberately wrong'
FAILED tests/test_profile.py::test_a_deliberate_failure - AssertionError: ass...
1 failed, 6 passed in 0.03s
make: *** [Makefile:21: test] Error 1
```

**Fails on an empty discovery.** With `tests/test_profile.py` moved out of the tree, `pytest` collects nothing and exits 5, which the runner reports as a failure of the `test` target.

```text
cd prototype && uv run --frozen pytest

no tests ran in 0.00s
make: *** [Makefile:21: test] Error 5
```

**What it establishes and what it does not.** An empty discovery is a failure for this project, and that is `pytest`'s own exit status rather than a setting: a suite that disappears cannot leave the gate green. The six tests hold the pinned parser to the clauses the declared profile rests on; they establish nothing about a build that does not exist yet.

## T2 Lint command

**Observes AC3.** The linter runs over the package, its tests and `checks/`.

```bash
make lint
```

**Pass.** Exit 0, over six files.

```text
All checks passed!
```

**Fails on a lint error.** With `import os` appended to `prototype/src/prosiform/__init__.py`, the command exits nonzero and names the rule, the file and the line.

```text
F401 `os` imported but unused
 --> prototype/src/prosiform/__init__.py:7:8
Found 1 error.
make: *** [Makefile:24: lint] Error 1
```

## T3 Format check

**Observes AC3.** The formatter runs in check mode over those same files.

```bash
make format-check
```

**Pass.** Exit 0.

```text
6 files already formatted
```

**Fails on a misformatted file.** With `x = {   "a":1,  "b":2 }` appended to `prototype/src/prosiform/__init__.py`, the command exits nonzero and prints the formatting it would apply.

```text
unformatted: File would be reformatted
 --> prototype/src/prosiform/__init__.py:7:1
1 file would be reformatted, 5 files already formatted
make: *** [Makefile:27: format-check] Error 1
```

**What it establishes and what it does not.** The command reports formatting; it does not apply it. Adopting the formatter reformatted `checks/links.py` once, in this task's second commit.

## T4 Type check

**Observes AC3.** The type checker runs in strict mode over those same files.

```bash
make typecheck
```

**Pass.** Exit 0, five source files.

```text
Success: no issues found in 5 source files
```

**Fails on a type error.** With a function returning `int` where its annotation says `str`, the command exits nonzero and names the file, the line and the error.

```text
prototype/src/prosiform/__init__.py:10: error: Incompatible return value type (got "int", expected "str")  [return-value]
Found 1 error in 1 file (checked 5 source files)
make: *** [Makefile:30: typecheck] Error 1
```

## T5 Lock check

**Observes no epic criterion.** It holds the lockfile to the dependency list `prototype/pyproject.toml` declares, which is the guarantee AC2 rests on once a later change edits that list.

```bash
make lock-check
```

**Pass.** Exit 0.

```text
cd prototype && uv lock --check
Resolved 16 packages in 1ms
```

**Fails on a dependency list edited without relocking.** With `mdit-py-plugins==0.5.0` added to `dependencies` and the lockfile untouched, the command exits nonzero and says what is stale.

```text
Resolved 17 packages in 195ms
The lockfile at `uv.lock` needs to be updated, but `--check` was provided. To update the lockfile, run `uv lock`.
make: *** [Makefile:33: lock-check] Error 1
```

## T6 Layout check

**Observes AC1.** Each of the three trees holds a tracked file.

```bash
make layout
```

**Pass.** Exit 0.

```text
ok   docs/ — 2 tracked file(s), the documentation this repository owns
ok   fixtures/ — 1 tracked file(s), the language-neutral fixture corpus
ok   prototype/ — 7 tracked file(s), the Python build

layout check: 3 tree(s) present
```

**Fails on a tree holding no tracked file.** With `fixtures/` removed from the index by `git rm -r --cached fixtures`, the command exits nonzero and names the tree. The index was restored with `git reset` afterwards.

```text
FAIL fixtures/ holds no tracked file; it is the language-neutral fixture corpus

layout check: 1 failure(s)
make: *** [Makefile:36: layout] Error 1
```

## T7 Link check

**Observes AC5.** Every reference the README carries resolves.

```bash
make links
```

**Pass.** Exit 0, sixteen references: nine remote addresses reached over the network, two repository URLs resolved through git against the engineering branch, and five local paths.

```text
ok   repository https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md
ok   local      checks/README.md
ok   remote     https://github.com/m2ux/prosiform/issues/2

link check: every reference resolved
```

**Fails on an unresolvable reference.** With `[a broken reference](docs/absent.md)` appended to the README, the command exits nonzero and names the path. The README was restored afterwards.

```text
FAIL README.md: docs/absent.md — docs/absent.md does not exist

link check: 1 unresolved reference(s)
make: *** [Makefile:39: links] Error 1
```

**Why the named command passes `--online`.** Without the flag a reference outside this repository counts as unresolved, so an offline run of this README reports nine failures and can never pass. A command that cannot pass is not a gate, so the named command supplies the flag and the environment that runs it needs network access and GitHub credentials. An issue, a pull request and a project board are read through `gh api`, because this repository is private and answers an unauthenticated page request with 404. The consequence for W04 is a job step with network access and a token whose scope reaches issues, pull requests and the user project the README links.

## T8 Vocabulary check

**Observes AC6.** The shipped glossary defines every contract term the design and the acceptance criteria use.

```bash
make vocabulary
```

**Pass.** Exit 0. The inventory is the 34 terms the design italicises; the text that uses them is `design.md` and the Acceptance Criteria section of each `i**-e**.md` epic beside it, 20 sources in all; the file under test is `docs/glossary.md` in the working tree.

```text
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

**Fails on a contract term the shipped glossary does not define.** With the `closure` row deleted from `docs/glossary.md`, the command exits nonzero and names the term. The glossary was restored afterwards.

```text
FAIL closure — the design marks it as a contract term, and docs/glossary.md does not define it

vocabulary check: 1 term(s) the glossary and the contract disagree on
```

**Fails on a definition the contract does not carry.** With a `manifest shard` row added under `Addressing`, the command exits nonzero and names it.

```text
FAIL manifest shard — docs/glossary.md defines it, and neither the design nor an acceptance criterion carries it

vocabulary check: 1 term(s) the glossary and the contract disagree on
```

**Where the inventory comes from.** The design italicises a term where it first uses it and states that convention in its opening, so the contract declares its own vocabulary and the check reads it from there. The inventory is therefore independent of the file under test: deleting a glossary row removes a definition, not a probe, which is what the first failing run above shows. No second glossary takes part; the glossary in the planning record remains a planning artifact with no runtime consumer.

**No check holds a dated planning path.** `grep -rn "2026\|artifacts/planning" checks/ Makefile` returns nothing. The check finds the design by reading the README's Design link, taking the branch and path out of it, and reads each epic's criteria from that path's siblings on that branch. The repository's one dated reference is the README's own link, and `links.py` holds it to resolving, so superseding the planning folder is a README edit rather than a code change.

**What it establishes and what it does not.** The check holds the glossary and the contract to one vocabulary in both directions. It does not read a term the design leaves unmarked: `entry point` is defined and used by an acceptance criterion but marked nowhere in the design, so it passes the second direction without entering the inventory. Marking a term on first use is the author's act, as writing its definition is, and the check holds the two together rather than deriving one from the other. It also says nothing about whether a definition is correct, only that one is present.
