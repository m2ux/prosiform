# Validation

The continuous-integration job as it ran. Every result below is a GitHub Actions run on this repository, recorded with its run id and its conclusion; nothing is reported that was not observed. The job was run on the tree as written, and once for each of the eight checks against a tree deliberately broken in the way that check forbids, so a pass is known to mean something.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e00/w04-continuous-integration-running-those` |
| Tested revision | `56ed75bd616592e8585513e0329dae4addc2c3a1` |
| Workflow | `.github/workflows/checks.yml`, triggered by `push` |
| Runner | GitHub-hosted `ubuntu-24.04`, runner image `20261012.334.1` |
| Toolchain | `uv 0.11.14` installed by the job, CPython 3.13.13 downloaded by `uv`, and the tools `prototype/uv.lock` pins |
| Credential | the repository secret `PROJECT_READ_TOKEN`, exported to the check step as `GH_TOKEN` |
| Date | 2026-10-18 |

Each failing run was produced by pushing one commit on top of the tested revision to a short-lived branch inside the trigger's namespace, which is a push to the repository and so runs the job exactly as any change does. Each commit carried one fault and nothing else. The eight branches were deleted once their runs were recorded; the runs themselves remain in the repository's Actions history, and each section below names the fault its run carried.

## T1 The clean tree

**Observes AC4.** The job runs the documented commands on a change and the clean tree passes.

[Run 39156322095](https://github.com/m2ux/prosiform/actions/runs/39156322095) — **success**, on `56ed75b`, the head this pull request merges.

The job checked the repository out with `fetch-depth: 0`, installed `uv 0.11.14`, and ran `make check` in one step. The runner's output is the Makefile's, target by target:

```text
Resolved 16 packages in 0.70ms
All checks passed!
6 files already formatted
Success: no issues found in 5 source files
6 passed in 0.08s
layout check: 3 tree(s) present
link check: every reference resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

**The credential reaches the tracker.** The link check resolved all four issue references and the project board from the runner:

```text
ok   remote     https://github.com/users/m2ux/projects/18
ok   remote     https://github.com/m2ux/prosiform/issues/1
ok   remote     https://github.com/m2ux/prosiform/issues/2
ok   remote     https://github.com/m2ux/prosiform/issues/20
ok   remote     https://github.com/m2ux/prosiform/issues/10
```

The board line is the `projectV2` GraphQL query, which a user-owned project puts outside the repository scope the built-in token is confined to. It resolved, so the scopes `PROJECT_READ_TOKEN` was issued with — `repo` and `read:project` — are the scopes the check needs. No step prints the token, and `gh` is given it only through the step's environment.

**The checkout carries the branch history.** Both references into the engineering branch resolved through git in the runner, and the vocabulary check read the design and the epic criteria from `origin/engineering`:

```text
ok   repository https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md
ok   repository https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1
```

This is what `fetch-depth: 0` buys: `actions/checkout` fetches a single branch by default, under which both of those references and the whole vocabulary check fail with `no git ref named engineering`, and no token changes that.

**Other runs on this branch.** Two earlier runs sit in the history against commits this branch no longer carries: 39156040702, which failed because the `uv` installer was named by a major tag that project does not publish, and 39156117095, which passed on the revision before the slug rule was widened. Neither is evidence for a criterion.

## T2 Lock check

**Observes AC4.** A dependency list the lockfile does not describe fails the job.

[Run 39156473333](https://github.com/m2ux/prosiform/actions/runs/39156473333) — **failure**. Fault: `mdit-py-plugins==0.5.0` added to `prototype/pyproject.toml` with the lockfile untouched.

```text
cd prototype && uv lock --check
Resolved 17 packages in 84ms
The lockfile at `uv.lock` needs to be updated, but `--check` was provided. To update the lockfile, run `uv lock`.
make: *** [Makefile:33: lock-check] Error 1
```

## T3 Lint check

**Observes AC4.** A lint error fails the job.

[Run 39156473750](https://github.com/m2ux/prosiform/actions/runs/39156473750) — **failure**. Fault: `import os` appended to `prototype/src/prosiform/__init__.py`.

```text
8 | import os
  |        ^^
help: Remove unused import: `os`
Found 1 error.
make: *** [Makefile:24: lint] Error 1
```

## T4 Format check

**Observes AC4.** A file the formatter would reformat fails the job.

[Run 39156473600](https://github.com/m2ux/prosiform/actions/runs/39156473600) — **failure**. Fault: `PROFILE = 'skill-markdown-v1'` appended to `prototype/src/prosiform/__init__.py`, which the formatter writes with double quotes.

```text
  - PROFILE = 'skill-markdown-v1'
8 + PROFILE = "skill-markdown-v1"
1 file would be reformatted, 5 files already formatted
make: *** [Makefile:27: format-check] Error 1
```

## T5 Type check

**Observes AC4.** A type error fails the job.

[Run 39156473603](https://github.com/m2ux/prosiform/actions/runs/39156473603) — **failure**. Fault: a function annotated `-> str` returning `1`.

```text
prototype/src/prosiform/__init__.py:10: error: Incompatible return value type (got "int", expected "str")  [return-value]
Found 1 error in 1 file (checked 5 source files)
make: *** [Makefile:30: typecheck] Error 1
```

## T6 Test command

**Observes AC4.** A failing test fails the job.

[Run 39156473626](https://github.com/m2ux/prosiform/actions/runs/39156473626) — **failure**. Fault: one deliberately false assertion appended to `prototype/tests/test_profile.py`.

```text
FAILED tests/test_profile.py::test_a_deliberate_failure - AssertionError: assert '<p>plain</p>\n' == 'deliberately wrong'
1 failed, 6 passed in 0.12s
make: *** [Makefile:21: test] Error 1
```

## T7 Layout check

**Observes AC4.** A tree holding no tracked file fails the job.

[Run 39156473285](https://github.com/m2ux/prosiform/actions/runs/39156473285) — **failure**. Fault: `fixtures/README.md` deleted, which leaves the fixture tree with nothing tracked in it.

```text
FAIL fixtures/ holds no tracked file; it is the language-neutral fixture corpus

layout check: 1 failure(s)
make: *** [Makefile:36: layout] Error 1
```

## T8 Link check

**Observes AC4.** An unresolvable reference fails the job.

[Run 39156473795](https://github.com/m2ux/prosiform/actions/runs/39156473795) — **failure**. Fault: `[a broken reference](docs/absent.md)` appended to `README.md`. The run resolved every other reference, the issues and the board among them, before reporting this one.

```text
FAIL README.md: docs/absent.md — docs/absent.md does not exist

link check: 1 unresolved reference(s)
make: *** [Makefile:39: links] Error 1
```

## T9 Vocabulary check

**Observes AC4.** A contract term the glossary does not define fails the job.

[Run 39156473369](https://github.com/m2ux/prosiform/actions/runs/39156473369) — **failure**. Fault: the `closure` row deleted from `docs/glossary.md`.

```text
FAIL closure — the design marks it as a contract term, and docs/glossary.md does not define it

vocabulary check: 1 term(s) the glossary and the contract disagree on
```

## T10 Heading slug

**Observes no epic criterion.** It holds the link check's fragment resolution to the anchors a rendered page carries, which is the guarantee AC5 rests on once the README carries a fragment link.

The oracle is GitHub's own rendering of this repository's README, read as HTML through the API and reduced to the anchor ids it generates:

```bash
gh api "repos/m2ux/prosiform/readme?ref=i00/e00/main" -H "Accept: application/vnd.github.html"
```

Each of the README's twelve headings was put through `slug()` at the tested revision and compared with the id GitHub generated for it, the `user-content-` prefix removed. All twelve agree, six of them headings that open with an emoji:

```text
ok   heading='🧩 prosiform'           check='-prosiform'            github='-prosiform'
ok   heading='🎯 Overview'            check='-overview'             github='-overview'
ok   heading='Why?'                   check='why'                   github='why'
ok   heading='How It Works'           check='how-it-works'          github='how-it-works'
ok   heading='Architecture'           check='architecture'          github='architecture'
ok   heading='🗂️ Repository Layout'   check='️-repository-layout'    github='️-repository-layout'
ok   heading='✅ Checks'              check='-checks'               github='-checks'
ok   heading='📦 Installation'        check='-installation'         github='-installation'
ok   heading='🚀 Invocation'          check='-invocation'           github='-invocation'
ok   heading='📏 Measured'            check='-measured'             github='-measured'
ok   heading='🗺️ Status'              check='️-status'               github='️-status'
ok   heading='📐 Scope'               check='-scope'                github='-scope'

12 heading(s), 0 mismatch(es)
```

The two Repository Layout and Status rows carry a variation selector, U+FE0F, which GitHub keeps and which a rule written in terms of word characters drops: the emoji itself is a symbol and goes, the selector is a combining mark and stays. The rule now states which classes survive — letters, numbers and combining marks, plus hyphen, underscore and space — rather than which characters do, which is why those two agree as well.

**What it establishes and what it does not.** It establishes agreement over the one document the check reads, against GitHub's own answer for that document rather than against an expectation written here. It is an observation at a revision, not a standing check: no test in the repository re-runs the comparison, so a later edit to the rule is caught by review rather than by a command.
