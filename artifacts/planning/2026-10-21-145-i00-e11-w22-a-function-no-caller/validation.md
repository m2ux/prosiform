# Validation — I00:E11:W22

> Validation Record · 2026-10-21

The checks run over the delivery, what each established, and the readings taken alongside them.

## Procedure

Every check ran from the worktree at `.worktrees/i00-e11-w22`, against the build in that same checkout:

```bash
export PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"
make check
```

The vocabulary check reads the design from `origin/engineering`, so the design's revised clauses were committed and pushed before the run. The link check reaches GitHub, so the run carried host credentials and no token environment.

## Build and repository checks

`make check` ran its fourteen targets in order and every one passed.

| Target | Result |
| --- | --- |
| `lock-check` | The lockfile describes the declared dependency list |
| `lint` | `ruff` reports no error over `src/prosiform`, `src/tests` and `checks` |
| `format-check` | 50 files already formatted |
| `typecheck` | `mypy` strict, no issue in 49 source files |
| `test` | 665 passed |
| `harness` | 487 passed |
| `corpus` | 217 fixtures, 217 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `smoke` | The installed entry point bundles a reference from a source root outside the repository |
| `layout` | 3 trees present |
| `tables` | 14 commands and 7 declarations, each declared and named |
| `links` | Every reference in 12 documents resolved |
| `vocabulary` | 35 contract terms marked in the design, each defined in `docs/glossary.md`, and every definition carried across 23 sources |
| `invocation` | 27 statements of the documented invocation held to the build |

The lint run is the one check that saw the change by itself: removing the five `owner` tests left `prosiform.source.visible` imported and unused in `src/tests/test_source.py`, and `ruff` reported it as `F401`. That is the whole of what the repository's lint can see of a function no caller reaches — the import that named it — and it is why the function itself stayed invisible while the build was green.

## Reachability of every defined function

The criterion is a claim about every function the package defines, so it was read off a listing rather than asserted. An audit parsed each module of `src/prosiform` and each module of `src/tests` with `ast`, collected every module-level function and method definition, and counted the names the package itself writes as a `Name`, an `Attribute` or an import alias. A definition the package never names is one the product does not reach.

Before the change the audit named ten definitions. After it, eight remain, and each is reached by something other than the suite:

| Definition | What reaches it |
| --- | --- |
| `cli.main` | The console script `prosiform = "prosiform.cli:main"` declared in `src/pyproject.toml` |
| `cli.Parser.error` | `argparse`, which calls it on a usage failure |
| `candidate.Use.__eq__`, `__hash__`, `__repr__` | The language, wherever a `Use` is compared, hashed or printed |
| `delivery.deliver`, `Delivery.delivered`, `Delivery.explain` | The package's delivery wrapper, a public interface with no in-repository caller |

The two the change removed were `source.owner`, which the task names, and `limits.defaults`, which the audit found beside it and which no module and no test names at all. The `delivery` wrapper is a published interface rather than an internal path, and whether the product itself must reach it is a question of its own: it is deferred as a row of #39 rather than answered here.

The audit is a reading taken for this record and not a check the repository runs. Nothing standing stops a function from losing its last caller again, which is the limitation below.

## One description of link ownership

The design, the `candidate` module and the `ownership` fixtures were read together after the change.

- The design's self-reference section carries **Link position** — a reference resolves by its target alone, wherever in the source it sits — and **Preamble content**, which keeps the preamble's membership of the document node because a whole-document selection carries it. The paragraph closing the section states that a destination belongs to the target rather than to the region the reference sits in.
- The post-compilation invariant is **Destination stability**: a reference's destination is the one its target was assigned, before and after overlap consolidation.
- `candidate`'s module prose names that invariant and names what holds it: the map `cli.destination_map` builds over every group from the identity each emitted heading answers to, which carries neither a link's position nor the region a run consolidated it into. A check comparing a link's destination before and after consolidation would compare one lookup of a target with another lookup of the same target.
- `source` and `cli` state the same thing in their own terms, and neither describes a section a link belongs to.
- The three `ownership` fixtures and the two `self-reference` fixtures declaring the preamble clause name the clauses as the design now names them, and their descriptions say a destination is read from the target.

The design's coverage map names the three clauses under their new names. Two further uses of the word in the design — retaining original source ownership independently of output heading levels, and preserving saved source ownership through candidate validation — are the outline sense rather than the link sense, describe behaviour the build still has, and were left as they are.

## Review

- No run reads a position's owning section: the corpus passes over the three `ownership` fixtures, which exercise a self-reference and two ancestor references across consolidation, and each resolves to the destination its target was assigned.
- The removal touched no behaviour. Standard output is compared byte for byte by the corpus runner, and all 217 fixtures produce the bytes their manifests declare.
- `limits.defaults` was removed with no test to retire, because no test named it.

## Limitations

- The reachability audit is a reading, not a standing check. The repository runs nothing that would catch the next function to lose its last caller, and `ruff` sees only the import that named it. That gap is deferred as a row of #39.
- The audit compares names rather than resolving calls, so a function reached only through a name built at runtime would read as unreached. The package builds no such name.
