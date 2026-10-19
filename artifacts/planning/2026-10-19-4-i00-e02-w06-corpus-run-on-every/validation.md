# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by making a tree carry one fault and nothing else, pushing it, recording the job's behaviour, and removing it.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e02/w06-corpus-run-on-every` |
| Tested revision | `785db34475978cec0af52a0630b9e7e8d8ef9475` |
| Base revision | `56ad50f` on `i00/e02/main`, where the base corpus count was measured |
| Contract revision | `d70b05a` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Continuous-integration job | `Checks`, `.github/workflows/checks.yml`, on `ubuntu-latest` |
| Build under test | `uv run --project $GITHUB_WORKSPACE/prototype --frozen prosiform`, named to the corpus run as `PROSIFORM_BUILD` |
| Run from | the repository root, by `make check` |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0`, `markdown-it-py 4.2.0` |
| Date | 2026-10-19 |

**A job's behaviour is a property of the job**, so the four cases below are observed runs in continuous integration rather than local invocations of the same command. Each fault was carried by a branch cut from the tested revision, matching the job's `i[0-9][0-9]/**` trigger, and that branch was deleted once its run completed. The run records remain.

## The corpus at the base and at the head

The base is `56ad50f` on `i00/e02/main`. Nothing in the repository ran the corpus there, so the figure was measured by running this task's command against that tree before the two markers were added:

```text
corpus check: 38 fixture(s), 36 pass, 2 fail, 0 awaited, 0 unexpected pass
```

The two failures are `extraction/nested-section-target`, which exits 4 where the manifest declares 1, and `normalization/root-escape`, which exits 0 and publishes 158 bytes where the manifest declares 1 and an empty bundle. Both declare behaviour a later epic delivers.

At the head, `785db34`, the same 38 fixtures run and the same two fail, each now naming the work it awaits:

```text
corpus check: 38 fixture(s), 36 pass, 0 fail, 2 awaited, 0 unexpected pass
```

**The corpus count is unchanged — 36 of 38 pass at the base and at the head.** This task changes no source of the build. What changes is that the figure now comes from a command, on every change, rather than from a driver written for one session.

## T1 The set, in one pass

**Observes AC11.** The repository's checks run together, the corpus run among them, against the build the same change produces.

```bash
make check
```

**Pass.** Run [39257483649](https://github.com/m2ux/prosiform/actions/runs/39257483649) on `785db34`, conclusion `success`. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `harness`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order.

The same command run locally on the same revision gives the per-check verdicts:

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.91ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
26 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 25 source files
cd prototype && uv run --frozen pytest
245 passed in 0.14s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
164 passed in 0.43s
uv run --project prototype --frozen python checks/corpus.py
corpus check: 38 fixture(s), 36 pass, 0 fail, 2 awaited, 0 unexpected pass
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 12 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 6 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The build's suite runs two hundred and forty-five, as it did at the base: this task adds no build code. The harness suite runs one hundred and sixty-four where the base ran one hundred and thirty; the thirty-four are the schema's description of `awaiting`, twelve of them, and the corpus run's outcome rules, twenty-two. The table check reads twelve commands where the base read eleven, the twelfth being `make corpus` beside the renamed `make harness`.

## T2 Every fixture runs, and a passing corpus does not fail the job

**Observes AC11.** The job runs the whole corpus, not a subset, and a corpus whose only failures await later work leaves the job green.

Run [39257483649](https://github.com/m2ux/prosiform/actions/runs/39257483649) on `785db34`, conclusion `success`. The job's log carries one line per fixture — thirty-eight of them, which is every directory under `fixtures/` holding a `manifest.toml` — then the two awaited lines and the count:

```text
extraction/nested-section-target: awaited, awaiting I00:E03
normalization/root-escape: awaited, awaiting I00:E04
corpus check: 38 fixture(s), 36 pass, 0 fail, 2 awaited, 0 unexpected pass
```

**Pass.** The job is green and the two incomplete expectations are visible in its output rather than hidden by it.

## T3 A failing fixture fails the job and is named by identity

**Observes AC11.** The fault: `fixtures/identity/whole-document/manifest.toml` declares `exit_status = 1` where the build returns 0, which is one fixture failing and nothing else. Carried by branch `i00/e02/w06-check-failing-fixture` at `62e7b88`, since deleted.

Run [39257642321](https://github.com/m2ux/prosiform/actions/runs/39257642321), conclusion **`failure`**:

```text
identity/whole-document: fail
identity/whole-document: fail
  expected.exit_status: expected 1, the run exited 0
corpus check: 38 fixture(s), 35 pass, 1 fail, 2 awaited, 0 unexpected pass
make: *** [Makefile:36: corpus] Error 1
```

**Pass.** The job fails, the fixture is named by its identity — its path under `fixtures/` — both on its verdict line and above the difference, and the difference says which expectation differed and how. The two awaited fixtures stay awaited, so the marker does not swallow a real failure.

## T4 An expected failure that unexpectedly passes fails the job

**Observes AC11.** The fault: `fixtures/identity/whole-document/manifest.toml` carries `awaiting = "I00:E05"` while the build already meets it, which is a spent marker and nothing else. Carried by branch `i00/e02/w06-check-unexpected-pass` at `15ac826`, since deleted.

Run [39257669316](https://github.com/m2ux/prosiform/actions/runs/39257669316), conclusion **`failure`**:

```text
identity/whole-document: unexpected pass, awaiting I00:E05
identity/whole-document: meets its manifest while awaiting I00:E05
  remove awaiting = 'I00:E05' from identity/whole-document/manifest.toml
corpus check: 38 fixture(s), 35 pass, 0 fail, 2 awaited, 1 unexpected pass
make: *** [Makefile:36: corpus] Error 1
```

**Pass.** The job fails, and its output names the manifest the marker is to be lifted from. This is what keeps the mechanism able to retire itself: the change that delivers I00:E03 fails the job until `extraction/nested-section-target` loses its marker, so the marker cannot outlive the work it waits on.

## T5 An unconfigured build fails the job rather than skipping it

**Observes AC11.** The fault: the job's `env` names no `PROSIFORM_BUILD`, which is the one configuration the corpus run needs and nothing else. Carried by branch `i00/e02/w06-check-no-build` at `0333538`, since deleted.

Run [39257692661](https://github.com/m2ux/prosiform/actions/runs/39257692661), conclusion **`failure`**:

```text
corpus check: PROSIFORM_BUILD names the build under test; a fixture has no result without one
make: *** [Makefile:36: corpus] Error 1
```

**Pass.** The job fails. No fixture line is printed, because no fixture ran: the run refuses to produce a verdict rather than reporting a corpus as holding against a build that never ran, and it does not pass the step over and leave the suite green.

## T6 The schema describes the marker, and the run's outcome rules hold

**Observes AC11.** The schema cases and the corpus run's unit cases, both in the harness suite.

```bash
make harness
```

**Pass.** 164 passed, within run [39257483649](https://github.com/m2ux/prosiform/actions/runs/39257483649). The cases this task adds:

- `fixtures/manifest.schema.json` accepts `awaiting = "I00:E03"` and `awaiting = "I00:E03:W02"`, accepts a manifest carrying neither, and rejects `""`, `"E03"`, `"I0:E03"`, `"I00-E03"`, `"I00:E03:W2"`, `"later"`, `"I00:E03 section"` and the boolean `true`. The schema is `additionalProperties: false` throughout, so a manifest could not carry the field until the schema described it, and the shape it states is what keeps the marker machine-readable rather than prose.
- The four outcomes: a fixture with no marker that meets its manifest passes; one with no marker that differs fails; one carrying a marker that differs is awaited; one carrying a marker that meets its manifest is an unexpected pass. Only the second and fourth fail the run.
- A corpus of passing and awaited fixtures returns 0; one holding a failure returns 1; one holding an unexpected pass returns 1; one with no build configured returns 1 and prints the variable's name, having run no fixture; an empty corpus returns 1.
- Every fixture of a three-fixture corpus appears in the output and in the count, so the run is over the whole corpus rather than a sample.

The build under test in these cases is a canned program each case configures, as in the runner's own tests: the comparison belongs to `runner.py`, and what these cases exercise is the verdict drawn from it.

## T7 The same job on the epic base

**Observes AC11.** The merge commit `d8abd5e` on `i00/e02/main` runs the same job, which is the corpus running on a change nobody wrote the command for.

Run [39258458529](https://github.com/m2ux/prosiform/actions/runs/39258458529), conclusion `success`:

```text
corpus check: 38 fixture(s), 36 pass, 0 fail, 2 awaited, 0 unexpected pass
```

**Pass.**

## Limitations

- **The job names this repository's build.** A second implementation of the contract runs the same corpus by naming its own build in `PROSIFORM_BUILD`; nothing here presumes the Python build, and `checks/corpus.py` imports no package of it. That a second build passes the corpus is not observed, because there is no second build.
- **A `make corpus` run needs a configured build.** `make check` therefore fails on a working copy that has not set `PROSIFORM_BUILD`. That is the design — a corpus run that skips states nothing — and the root `README.md` names the variable and gives the value for this build.
- **The marker's retirement is observed, not scheduled.** A later epic's session learns which fixtures its work unblocks from a failing corpus run, and from the `awaiting` values the manifests carry. Nothing reminds it in advance.
