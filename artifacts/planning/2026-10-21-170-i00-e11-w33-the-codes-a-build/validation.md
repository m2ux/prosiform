# Validation — The Codes a Build Reports for Itself

Every check is a named target of the repository's `Makefile`, run from the
worktree at `.worktrees/i00-e11-w33`. The build under test is the one in this
checkout, named to the checks by `PROSIFORM_BUILD`:

```bash
export PROSIFORM_BUILD="uv run --project $PWD/src --frozen prosiform"
make check
```

`make check` runs every target in order and stops at the first failure, so one
passing run is the whole set. It was run on the base before the change and on
the branch after it, so the result is attributable to the branch, and a third
time once the epic base was merged into the branch and its conflict resolved.

## Revisions

| Run | Revision | Result |
| --- | --- | --- |
| Base, before the change | `8cd9534` on `i00/e11/main` | `make check` passed, exit 0 |
| Branch, after the change | `8961b9e` on `i00/e11/w33-the-codes-a-build` | `make check` passed, exit 0 |
| Branch, with the epic base merged | `8d52e9c` on `i00/e11/w33-the-codes-a-build` | `make check` passed, exit 0 |

The third run is the one every result below is taken from. The base moved while
this work was under way: `i00/e11/main` gained the installation claims bound to
the smoke-run property that would observe them, which touches the same declared
surface this work extends. The conflict was resolved on this branch and the
whole set re-run.

## make check

```
All checks passed!
```

Fifteen targets, in the order the `Makefile` lists them, exit 0.

## make lock-check

The lockfile describes the declared dependency list. No dependency was added.

## make lint

`ruff check` over `src/prosiform`, `src/tests` and `checks`, clean.

## make format-check

`ruff format --check` over the same three trees, clean. The composed import of
each part's published codes is split across statements because the project's
configuration does not combine aliased imports, which is the formatter's own
arrangement.

## make typecheck

`mypy --strict` over the same three trees, clean. The new report field carries
`bool | None`, which is `None` for an exit status, since an exit status is no
code.

## make test

```
696 passed
```

The build's own suite. Three cases hold the new surface:

- the codes response names every code the build can emit, one per line in
  sorted order, with nothing on standard error and the success status;
- the set the command reports is the sorted union of the codes each part of the
  build declares, so a code added to a part and left out of the composition
  fails;
- a codes run needs no allowed source root, like the other informational runs.

## make harness

```
578 passed
```

The check suite. Six cases hold the report's new reading, each supplying the
reported codes directly so the suite runs no build:

- a declared code the build reports is rendered as reported and fails nothing;
- a declared code the build reports nowhere fails the report and is listed;
- a reported code the contract declares nowhere fails the report and is listed;
- an exit status states nothing either way, since it is no code;
- the closing summary counts both directions;
- the independence scan reaches a reported code the contract declares nowhere.

## make corpus

Every fixture of the corpus, run against the build under test, produced the
result its manifest declares. The command's existing surface is unchanged by
the new option.

## make smoke

The wheel built, installed into a throwaway environment and bundled a reference
from a source root outside the repository, with the command resolved by name.

## make layout

Each of the three trees holds a tracked file.

## make tables

The command and dependency tables name every target the `Makefile` declares and
every dependency the project declares, and nothing besides. No target was added.

## make links

Every reference every document in the repository carries resolves.

## make vocabulary

The glossary defines every contract term the design marks. The new option and
the report's new wording introduce no marked term.

## make invocation

```
invocation check: 29 statement(s) of the documented invocation, each held to
the build PROSIFORM_BUILD names
```

```
ok   option      --codes
```

The documented invocation gained the row for `--codes`, and the check holds it
to the build's own help output word for word in both directions. The help line
reads:

```
  --codes               report the error and warning codes this build can emit
```

## make conformance

```
conformance report: 253 clause(s) the design states, 64 covered by no fixture,
0 declaration(s) naming no clause; 30 declared name(s) reached, 0 unfixturable,
0 declared code(s) the build reports nowhere, 0 reported code(s) the contract
declares nowhere, 3 installation claim(s) no run observes
```

This is the evidence for AC35. The declared-surface listing states, for each of
the twenty-five codes the contract declares, whether the build under test
reports it:

```
error E_PUBLICATION_FAILED: 1 fixture(s), the build reports it
warning W_RESOURCE_PORTABILITY: 8 fixture(s), the build reports it
```

Both directions of the comparison are zero, so the set the build reports and the
set the contract declares are the same set. A disagreement in either direction
is a report failure:

```
FAIL error E_RESOURCE_LIMIT is declared by the contract and the build reports it nowhere
FAIL E_INVENTED is reported by the build and the contract declares it nowhere
```

The report reaches the build the way the corpus does — `PROSIFORM_BUILD` names
its command line and it is invoked as a subprocess — so no check reads inside
any build. With no build named, the run fails rather than passing over the
comparison:

```
conformance report: PROSIFORM_BUILD names the build under test; a fixture has
no result without one
```

## make independence

```
ok   corpus      233 fixture(s) and their identities
ok   report      the conformance report as it renders
ok   interface   49 declared name(s)

independence check: 60 term(s), named by no fixture declaration, no report
entry and no name the contract declares
```

The interface count rose by one with the documented option. The check renders
the same report, so it reads the same build and fails without one, and a code a
build reports that the contract declares nowhere is scanned like any other
entry.

## Observations

- **The base moved under this work.** `i00/e11/main` gained the installation
  claims bound to the smoke-run property that would observe them while this
  branch was open. Both changes extend the same declared surface, so the report,
  its tests and the two check descriptions conflicted. The resolution keeps both
  readings: the listing carries the claims and the code comparison, and the
  summary counts both.
- **The report now has three inputs.** It reads the design, the corpus and the
  build. Nothing about the clause mapping or the uncovered list changed, so what
  that part of the report measures is unchanged; what is new is the half of the
  surface a design and a corpus cannot state between them.
- **Nothing holds the design's own option enumeration to the command.** The
  documented invocation is held to the build's help output, and the design is
  held to the glossary and to the schema's catalogues, but no check compares the
  options the design states with the options a build offers. The new option is
  documented and held; the design is not party to that comparison. This is
  deferred rather than fixed here.
