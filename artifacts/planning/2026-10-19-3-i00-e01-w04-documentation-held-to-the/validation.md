# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by editing the working tree so that it carried one fault and nothing else, running the named command, and reverting the edit.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e01/w04-documentation-held-to-the` |
| Tested revision | `bcb16415dd465f3d15e32aa89e2ed80cfefe207b` |
| Contract revision | `ec11f90` on `engineering`, which the vocabulary check reads as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0` |
| Date | 2026-10-19 |

The link check reaches addresses outside the repository and reads the tracker with the caller's credentials, and `uv run --frozen` builds the project into the environment it runs in. The sandbox available to this session has no network, so every run below was performed outside it.

## T1 The set, in one pass

**Observes AC6, AC8.** The repository's checks run together, the two this task carries among them.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order. The `ok` lines each check prints are omitted here; the verdicts are not.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.77ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
15 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 14 source files
cd prototype && uv run --frozen pytest
6 passed in 0.02s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
52 passed in 0.35s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 5 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The corpus suite is unchanged at fifty-two tests; this task changes no fixture, no manifest and no schema. The vocabulary check is unchanged at thirty-four terms: *table*, *declaration* and *document* are words this task uses and the design does not mark as contract terms, so the glossary neither gains nor needs a definition for one.

## T2 The table check on the clean tree

**Observes AC6.** Every target the `Makefile` declares is named by a command table, and every declaration of the project definition by a dependency table, with nothing in either table that the project does not declare.

```bash
make tables
```

**Pass.** Exit 0. The check prints every target and declaration it compared, with the document that names it, so the set it read is visible in a passing run rather than only in its source.

```text
ok   command     make lock-check — README.md
ok   command     make lint — README.md
ok   command     make format-check — README.md
ok   command     make typecheck — README.md
ok   command     make test — README.md
ok   command     make corpus — README.md
ok   command     make layout — README.md
ok   command     make tables — README.md
ok   command     make links — README.md
ok   command     make vocabulary — README.md
ok   command     make check — README.md
ok   command     make layout — checks/README.md
ok   command     make links — checks/README.md
ok   command     make tables — checks/README.md
ok   command     make vocabulary — checks/README.md
ok   command     make corpus — checks/README.md
ok   command     make corpus — checks/README.md
ok   declared    Python — prototype/README.md
ok   declared    markdown-it-py — prototype/README.md
ok   command     make test — prototype/README.md
ok   command     make corpus — prototype/README.md
ok   command     make lint — prototype/README.md
ok   command     make format-check — prototype/README.md
ok   command     make typecheck — prototype/README.md
ok   command     make lock-check — prototype/README.md
ok   declared    pytest — prototype/README.md
ok   declared    ruff — prototype/README.md
ok   declared    mypy — prototype/README.md
ok   declared    jsonschema — prototype/README.md
ok   declared    types-jsonschema — prototype/README.md

table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
```

The eleven commands are the `Makefile`'s ten targets as this branch leaves them, plus `make check`, which was in prose alone until this task gave it a row. The seven declarations are `requires-python`, the one runtime dependency, and the five of the `dev` group.

**The first run of the check, before any README was edited, found the one real gap:**

```text
FAIL make check — the Makefile declares it and no command table names it

table check: 1 table fault(s)
```

## T3 A declared item no table names

**Observes AC6.** A dependency the project declares and the README does not list fails the check, naming the item and the side it is missing from.

### T3a A dependency removed from the table

Fault: the `jsonschema` row deleted from the dev dependency table of `prototype/README.md`.

```bash
make tables
```

**Pass** — the check failed as it must. Exit 1.

```text
FAIL jsonschema — prototype/pyproject.toml declares it and no declaration table names it

table check: 1 table fault(s)
make: *** [Makefile:46: tables] Error 1
```

### T3b A target no table names

Fault: a tenth working target added to the `Makefile` and documented nowhere.

```makefile
glossary-serve:
	python3 -m http.server --directory docs
```

```bash
make tables
```

**Pass** — the check failed as it must. Exit 1. This is the direction that makes the check self-policing: the target this task itself adds, `make tables`, had to be documented before it would pass.

```text
FAIL make glossary-serve — the Makefile declares it and no command table names it

table check: 1 table fault(s)
make: *** [Makefile:46: tables] Error 1
```

## T4 A table row the project does not declare

**Observes AC6.** This is the direction a check that only catches omissions does not have, and without it a dependency dropped from the project stays documented forever.

### T4a A dependency row with nothing behind it

Fault: a row for `mdit-py-plugins` added to the dev dependency table of `prototype/README.md`, a package `prototype/pyproject.toml` does not declare.

```bash
make tables
```

**Pass** — the check failed as it must. Exit 1.

```text
FAIL prototype/README.md: mdit-py-plugins — the table names it and prototype/pyproject.toml declares no such dependency

table check: 1 table fault(s)
make: *** [Makefile:46: tables] Error 1
```

### T4b A command row naming no target

Fault: the `make vocabulary` row of the root README's command table renamed to `make vocab`.

```bash
make tables
```

**Pass** — the check failed as it must. Exit 1. One failure, not two: `make vocabulary` is also named by the table in `checks/README.md`, so the target remains documented and only the row that names nothing is reported.

```text
FAIL README.md: make vocab — the table names it and the Makefile declares no such target

table check: 1 table fault(s)
make: *** [Makefile:46: tables] Error 1
```

### T4c A row naming another version

Fault: the `mypy` row's Value cell changed from `==2.4.0` to `==2.5.0`.

```bash
make tables
```

**Pass** — the check failed as it must. Exit 1.

```text
FAIL prototype/README.md: mypy — the table names '==2.5.0' and prototype/pyproject.toml declares '==2.4.0'

table check: 1 table fault(s)
make: *** [Makefile:46: tables] Error 1
```

This case was run twice. The first run reported two failures — the version, and `mypy` as a declaration no table names — because a row whose version differed was not counted as naming its item. A row that names a declared item under another version documents the item, and what it is documented as is wrong, so the comparison now counts it as named and reports the version alone. The output above is the second run, on the revision this record names.

## T5 The link check on the clean tree

**Observes AC8.** Every reference in each of the five READMEs the repository owns resolves.

```bash
make links
```

**Pass.** Exit 0. The five are the root, `checks/README.md`, `docs/README.md`, `fixtures/README.md` and `prototype/README.md`, found by `git ls-files` rather than named in the check.

```text
link check: every reference in 5 document(s) resolved
```

**Nothing the widening surfaced was broken.** The four READMEs beyond the root carry thirteen references between them — nine local paths, two blob or tree URLs into the engineering branch, and six remote addresses — and every one resolved on the first run of the widened check. W02's session had read them by hand and reported the same; this run confirms it rather than assuming it, and the check is now what keeps it true.

## T6 An unresolvable reference in a README other than the root

**Observes AC8.** The direction the check could not report before: a defect in a document outside the root.

Fault: two references added to `fixtures/README.md`, one naming a file that does not exist and one naming a heading `checks/README.md` does not carry.

```markdown
See the [corpus charter](charter.md) and the [runner's contract](../checks/README.md#the-runners-contract).
```

```bash
make links
```

**Pass** — the check failed as it must. Exit 1. Both classes of local failure are located in the document that carries them.

```text
FAIL fixtures/README.md: charter.md — charter.md does not exist
FAIL fixtures/README.md: ../checks/README.md#the-runners-contract — no heading in ../checks/README.md generates #the-runners-contract

link check: 2 unresolved reference(s)
make: *** [Makefile:49: links] Error 1
```

## T7 A tree added later, read by both checks unedited

**Observes AC6, AC8.** Neither check names the documents it reads, so a tree added after both were written is covered by committing it.

Fault: a `tools/` tree added and staged, holding a README with one command row naming no target and one reference to a file that does not exist. Neither `checks/tables.py` nor `checks/links.py` was touched.

```bash
make tables
make links
```

**Pass** — both checks failed as they must, each naming `tools/README.md`.

```text
FAIL tools/README.md: make tools — the table names it and the Makefile declares no such target

table check: 1 table fault(s)
```

```text
FAIL tools/README.md: charter.md — charter.md does not exist

link check: 1 unresolved reference(s)
```

The tree was staged rather than merely written, because a document counts when git tracks it: an untracked file is invisible to a fresh checkout. The tree was removed once both runs were recorded.

## T8 The set, in continuous integration

**Observes AC6, AC8.** The same commands the developer calls run on the branch.

The Checks workflow ran `make check` on `bcb1641`, the head of this task's pull request, and completed with conclusion `success`: [run 39211116578](https://github.com/m2ux/prosiform/actions/runs/39211116578). It is the one check that pull request carries.

```text
Resolved 22 packages in 0.63ms
All checks passed!
15 files already formatted
Success: no issues found in 14 source files
6 passed in 0.07s
52 passed in 0.38s
layout check: 3 tree(s) present
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 5 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

It ran again on `1b58d32`, the merge commit on the epic base `i00/e01/main`, and completed with conclusion `success`: [run 39211526354](https://github.com/m2ux/prosiform/actions/runs/39211526354). The trigger names the base as well as the task branch, so the merge result is checked and not only the change that produced it.

**The link check reads five documents from the runner.** The credential the job exports resolves the tracker references in the root README, and the checkout's full history resolves both engineering-branch references, so the widened set needs nothing the job did not already supply.

## What the checks do not establish

- **A table says the right thing, not merely the declared thing.** The comparison holds a row's name and version to the project definition. The Why and Asserts cells beside them are prose no check reads.
- **The declaration sets are the project's dependencies, not every name in `pyproject.toml`.** `requires-python`, `[project] dependencies` and the `dev` group are compared. `[build-system] requires` is the backend that builds the wheel rather than something a reader installs or invokes, and no table names it.
- **A table is located by its header cell.** A table enumerating commands or declarations under some other header is not read, and a passing run prints what it compared so an absent set is visible as a count rather than inferred.
- **Only READMEs are read.** `docs/glossary.md` carries references that no check resolves. AC8 is about the READMEs the repository owns, and widening further is a decision rather than an omission.
- **A remote address resolves as an address.** The link check establishes that a page or a tracker object answers, not that it says what the link claims.
- **The standalone checks carry no unit tests.** `layout.py`, `links.py`, `tables.py` and `vocabulary.py` are validated by running their named commands against a deliberately faulted tree, which is what this record holds. A regression in a check's own parsing would be caught by that procedure being repeated, not by a suite.


