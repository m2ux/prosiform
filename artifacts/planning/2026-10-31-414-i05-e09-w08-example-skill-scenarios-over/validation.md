# Validation — W08 Example Skill Scenarios Over the Mechanism

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w08-example-skill-scenarios-over` on branch `i05/e09/w08-example-skill-scenarios-over`, at branch head `19fec8d4` unless a section names another revision. The build under test was named by `PROSIFORM_BUILD` as the worktree's own `src/.venv/bin/pf`, created with `UV_OFFLINE=1 uv sync --frozen` because `uv run` cannot resolve in the sandboxed shell this session ran in. `src/.venv` is gitignored, so it carries nothing into the branch.

The design clause the scenarios bind is `Link classification and resource handling — The substitution mapping`, at the revision `README.md` pins, `827b66fc`.

## T1 — Both scenarios pass against the mechanism at branch head

**Ran:** `make mock-scenarios`, which is `uv run --frozen python checks/mock_scenarios.py`, invoked directly as `src/.venv/bin/python checks/mock_scenarios.py` with `PROSIFORM_BUILD` naming the same environment's `pf`.

**Observed:** exit `0`:

```text
the copy of the tree: pass
an-example-mode-bundled-against-a-stub: pass
an-example-skill-told-to-use-a-fake-gh: pass
the shipped example tree: pass
the copied tree: pass
mock scenario check: 5 scenario(s), 5 pass, 0 fail, held against the build PROSIFORM_BUILD names
```

Five entries are reported: the copied tree before the runs, the two scenarios, and both trees after them. The tree entries are the fingerprint comparison either side of the scenarios, which is what a run publishing into the skill directory fails on.

## T2 — A plan mode bundles over a stub where the artifact's member heading stood

**Ran:** the first scenario through `-d json`, and the bundle it published compared with the bundle the same copy produces with no mapping.

**Observed:** the run states one substitution and exits `0`:

```text
{"severity": "warning", "message": "the reference 'epic.md#task-matches' is redirected to the substitute '../stubs/epic-minimal.md#task-matches', where it would have resolved to 'artifacts/epic.md#task-matches'", "code": "W_MOCK_SUBSTITUTED", "resolved": "../stubs/epic-minimal.md#task-matches", "source": "epic.md#task-matches", "location": {"file": "artifacts/epic-issue-body.md", "line": 281, "column": 1}}
```

The `## Epic` heading is emitted once, at the depth the stand-in's `group: artifacts` / `group-depth: 1` decides, inside the merged `# Artifacts` range. No `# Epic` title is emitted, so the stand-in is a member of the group rather than a document of its own. Measured directly in T3.

The section beneath the heading carries the stand-in's placeholder prose:

```text
## Epic

### Operations

#### Check Epic Prerequisites

Placeholder for the prerequisite check a drafted epic states.

### Fields

#### Task Matches

Placeholder for the task matches a drafted epic returns.
```

The artifact's own prose — `The evidence required before starting an epic's work.` among it — is absent, and every byte before and after the `## Epic` section is the unmocked bundle's, so the mode's own sections, the `# Rules`, `# Conventions` and `# Artifacts` groups and every dispatched bundle are unchanged.

## T3 — The substituted section is the only byte range that moves

**Ran:** the unmocked and mocked `plan-mode` bundles section by section, over the whole 3,900-line bundle.

**Observed:** the prefix before `## Epic` and the suffix after it compare equal between the two bundles, and the section itself is 23,977 bytes against the artifact's 27,472. The substitute becomes the target outright, which is the design's stated semantic: its title, its groups and its own links are the ones the run uses.

## T4 — A redirected `conventions.md` names the fake and the bundle carries it

**Ran:** the second scenario through `-d json`, and the bundle's `# Conventions` section compared with the shipped one.

**Observed:** exit `0`, one substitution, and the section the session reads:

```text
# Conventions

The prerequisites every mode's run shares: ...

## Session

Every tracker call in this run is written `./fake-gh`, the stand-in for the
tracker. Once per session, before the first `./fake-gh` call, confirm
`GH_TOKEN` and `GITHUB_TOKEN` are unset so the stand-in reads the login the
session was given.
```

The shipped sentence `Once per session, before the first gh call, unset ... so gh uses its keyring login` is absent, and `./fake-gh` is present, so a session following the bundle is told to run the stand-in. The section is 22,429 bytes against the shipped 22,387, and every byte outside it compares equal: the mode still reads the same `# Plan Mode`, `# Rules`, `# Artifacts`, `# Propose Mode`, `# Protocols`, `# Configuration` and `# References` groups it read before.

The `# Conventions` heading is emitted at depth 1, its own document's title, because the stub declares no group — which is the same place the shipped `conventions.md` is emitted.

## T5 — A stand-in read whole is emitted only as far as the mode reaches

**Ran:** the `plan-mode` closure against a stand-in carrying an operation the bundle's own table of contents uses when the stub was supplied under the mode's `-m` mapping but not when the same bundle's `# Artifacts` group renders the stub's `## Epic` member.

**Observed:** the `plan-mode` bundle is only reachable through `-m artifacts/epic.md=...`: `artifacts/epic.md` is never a direct link of `modes/plan-mode.md`. It is reached only through `artifacts/epic-issue-body.md`, `artifacts/delivery-evidence.md`, `artifacts/delivery-branches.md`, `artifacts/issue.md`, `protocols/delivery-recording.md` and `protocols/delivery-base-preparation.md`, and each reaches its own section of `epic.md` rather than the whole document. This is why a stub holding only the fields, and none of the operations, still fails: the run reads the sections the references name and then looks for their headings.

The further consequence, measured in T1's passing run: the check compares a stand-in's blocks only where the unmocked bundle carries the heading they sit under. A block the mode never reaches is material the run never asks for and is not asserted either way. This is what the first design had wrong when it expected every block of the stand-in to appear; `fixtures.md`'s third defect (the stub described by "no criteria") is the same mistake seen from the other side, and both are avoided by holding the difference to the section the artifact held.

## T6 — A run that publishes into the tree it reads is reported

**Ran:** the check with the run's output folder redirected to the tree it reads, in the temporary copy, which is the first design's mistake.

**Observed:** the scenario entries pass on their bundles and the tree entry fails, which is the difference the fingerprint exists to report:

```text
the copied tree 1
    tree the copy: the runs wrote to the tree they read
```

This is the `cmp`-over-the-tree defect `fixtures.md` records: `expected.absent` resolves against the fixture directory rather than the working directory, so a `cmp` over a `usage-example`-style tree asserts nothing. Here the assertion is made after the run, on the tree, and it is red.

## T7 — A stub naming an artifact no link reaches is reported

**Ran:** the check with the first scenario's key changed to `artifacts/absent.md`.

**Observed:** five differences, each naming what departed rather than the check raising:

```text
substitution  the run states 0 substitution(s) where one is expected
bundle        the section carries no 'Placeholder for the prerequisite check a drafted epic states.'
bundle        the section carries 'The evidence required before starting an epic's work.', which the stand-in does not state
bundle        the section still states 'The evidence required ...'
```

## T8 — The check's own readings are held by the harness suite

**Ran:** `checks/tests` through `pytest --config-file src/pyproject.toml --rootdir . checks/tests`, which is one half of `make harness`.

**Observed:** `832 passed`, including the 32 new cases in `checks/tests/test_mock_scenarios.py`. Each supplies input the reading would take wrongly: a section holding headings deeper than itself, a heading the document repeats, a stand-in emitted as a document of its own rather than as a member, a section carrying the artifact's prose beside the stand-in's, a stand-in whose blocks the mode never reaches, a document whose front matter is not content, and a tree a run wrote into.

The other half of that target is `evals/diagram-following`, which fails 62 cases in this session because it writes a temporary directory beside its output path and the sandbox denies it; the brief records it as passing in CI. None of its cases reads anything this row changed.

## T9 — The static checks

**Ran:** `ruff check`, `ruff format --check` and `mypy --config-file src/pyproject.toml` over `checks/` and `src/prosiform`, which is `make lint`, `make format-check` and `make typecheck`. `make lock-check` ran as `uv lock --check`. The `make` targets themselves were not invoked, because the locked environment cannot resolve inside the sandbox; each target's own command was run directly against the worktree's `src/.venv`, which is the same environment `uv sync --frozen` produces.

**Observed:** `All checks passed!`, `53 files already formatted`, `Success: no issues found in 37 source files`, and `Resolved 24 packages`.

## T10 — `make corpus`, `make conformance`, `make invocation`, `make independence`

**Ran:** each target against the same build.

**Observed:** exit `0` throughout.

```text
corpus check: 358 fixture(s), 358 pass, 0 fail, 0 awaited, 0 unexpected pass
conformance report: 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause; 37 declared name(s) reached, 0 unfixturable, 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere, 16 clause(s) no run states, 3 section(s) stating no behaviour, 3 installation claim(s) no run observes
invocation check: 30 statement(s) of the documented invocation, each held to the build PROSIFORM_BUILD names
independence check: every shaped term of every fixture declaration and every report entry is one the contract names
```

This row lands no corpus fixture, so the clause and fixture counts are unchanged from the base at `8734a799`. The design clause the scenarios bind is stated in their own module rather than declared in a manifest, which is what a check rather than a fixture means here: `make conformance` reads manifests, and a check contributes no declaration to that report.

## T11 — `make tables`, `make layout`, `make steps`, `make vocabulary`, `make authoring`, `make links`

**Ran:** each target, and the link check with `--online` over the two documents this row edited.

**Observed:** exit `0` throughout.

```text
table check: 22 command(s) and 8 declaration(s), each declared by the project and named by a table
layout check: 4 tree(s) present
step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections
authoring check: 0 finding(s)
vocabulary check: 46 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on 827b66fc..., every one defined in docs/glossary.md
link check: every reference in 2 document(s) resolved
```

`make tables` reads 22 commands where the predecessor row's report read 21, which is `mock-scenarios`: the `Makefile` declares it and `checks.md` names it, so the table check holds both directions. The command count is the check that the target is documented and the target exists, so neither can land without the other.

## T12 — `make test`

**Ran:** `src/.venv/bin/python -m pytest` from `src`, with `src/.venv/bin` on `PATH`.

**Observed:** every test passing. `tests/test_handoff_round_trip.py` resolves the command by name from `PATH` — it names no configuration and no environment variable, by design — so it reads the environment's own entry point rather than a path written into the suite. Run without that directory on `PATH` its six cases fail with `E_PUBLICATION_FAILED`, which is the suite naming a missing `pf` rather than a defect in the build; `make test` runs it from `cd src && uv run --frozen pytest`, where the locked environment supplies the name.

**One sandbox limitation, not a change.** `tests/test_linked_bootstrap.py` runs `uv build --wheel` and needs network, and the diagram eval writes a temporary directory beside its output path, which the sandboxed shell denies; the brief records both as passing in CI and failing only here.

## T13 — Delivery

Delivery is recorded in `change-list.md` and reported to the user: the pull request number, its base and merge commit, row `W08` on #414 and the two criterion ticks.
