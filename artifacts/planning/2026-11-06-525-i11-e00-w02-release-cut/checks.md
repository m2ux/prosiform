# Validation at b10437ea7

> Recorded 2026-11-06

## Lock

```text
$ cd src && uv lock --check
Resolved 24 packages
exit 0
```

## Full configured check

`make check` at `b10437ea7f064715f54e192fad415aba0bdfe692`, with `PROSIFORM_BUILD` naming this checkout's build, as `.github/workflows/checks.yml` supplies it:

```text
$ PROSIFORM_BUILD="uv run --project <release worktree>/src --frozen pf" make check
make check exit: 0
```

Every target, in the Makefile's order:

| Target | Result |
| --- | --- |
| `lock-check` | Resolved 24 packages |
| `lint` | pass |
| `format-check` | pass |
| `typecheck` | pass |
| `test` | 1901 passed |
| `harness` | 1690 passed in 99.33s |
| `corpus` | 537 fixture(s), 537 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `smoke` | the installed command is named on the path, independent of the working directory, independent of this repository; wheel `prosiform-0.17.0-py3-none-any.whl` |
| `layout` | 4 tree(s) present |
| `tables` | pass |
| `links` | pass |
| `vocabulary` | 3249 term(s) from the design, `docs/glossary.md` and 49 declared name(s) |
| `invocation` | 29 statement(s) of the documented invocation |
| `conformance` | 365 clause(s), 0 declaring no clause, 0 declared codes the build reports nowhere |
| `independence` | every shaped term is one the contract names |

## What the run establishes

The build reports `pf 0.17.0 (prosiform-markdown)`, and its own corpus passes in full. The installed-wheel smoke run names the built artefact at the new version, so the bump reaches the package metadata rather than the source alone.

## What it does not establish

Nothing here is a statement about a merged pull request. The head checked is the release branch's commit, and the merge into `main` is the user's.
