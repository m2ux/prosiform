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
the branch after it, so the result is attributable to the branch.

## Baseline

The base `i00/e11/main` at the revision this branch was cut from, with no change
applied.

## make check

The whole set, in the order the `Makefile` lists it.

## make test

The build's own suite, which holds the command's informational responses: the
codes response writes every code the build can emit, one per line in sorted
order, and returns the success status; each part of the build that declares a
code publishes it, and the set the command reports is the union of those.

## make harness

The check suite, which holds the conformance report's reading of its inputs: a
declared code the build reports is listed as reported, a declared code it does
not report fails the report, and a code the build reports that the contract
declares nowhere is listed and fails the report.

## make corpus

Every fixture run against the build under test, which holds the command's
existing surface unchanged by the new option.

## make invocation

The documented invocation against the build's own help output in both
directions, which holds the new option's row to the help text word for word.

## make conformance

The report itself, whose declared-surface listing carries the comparison AC35
names.

## make independence

The corpus, the rendered report and the contract's declared names, each scanned
for implementation terms.

## Observations
