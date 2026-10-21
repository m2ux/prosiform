# Validation

The checks this row was held to, the revision they ran at, and what they observed.

## Revision

The branch `i00/e11/w24-a-run-time-fault`, cut from `i00/e11/main` at `232a528`. Every run below invoked the Makefile target a developer and continuous integration both call, from the repository root of the task worktree, with `PROSIFORM_BUILD` naming the locked build's console entry point.

## Why the Fault Is the Run's

A fixture declares a source tree, an invocation and the expected result, and the runner decides the verdict from those alone. The two runs this row reaches do not arise from that declaration, and neither can be reached from outside the run either.

| Candidate instrument | Why it does not reach the run |
| --- | --- |
| The runner rewrites the source while the build runs | The rewrite must land after discovery read the bytes and before the recheck reads them again, and nothing outside the process says when either happened. A timed rewrite is a race, and a race in the corpus is a flaky verdict. |
| The runner feeds the source through a named pipe, so the write completing is the build having read it | The contract's rooted, no-follow read returns a regular file and nothing else, so a pipe at a source path names no document and the run never reaches the bytes. |
| The runner denies the build a resource, so it fails in itself | A descriptor or address-space limit low enough to fail the run kills the interpreter before the command starts, and what a build does with an operating-system denial is not an outcome the contract declares. |
| The build performs the fault the run was asked for | Reaches both. The condition is supplied by the request and everything after it — the recheck, the status, the diagnostic, the empty standard output — is the build's own. |

The contract therefore declares `--fault NAME`, and the runner asks for it as it already asks for `--root DIR` and `--diagnostics json`.

## Harness Suite

`make harness`, the corpus's own checks, which carry the runner's and the schema's cases.

```text
538 passed in 9.41s
```

Eleven are new: the schema's cases for a manifest naming each fault, naming none, naming one outside the declared set and naming a bare flag; and the runner's cases for the request reaching the run in order, for a run meeting no fault asking for none, for a fixture declaring a fault being left as it was by a build that writes to its source tree, and for the allowed source root the run is given being the copy's rather than the fixture's.

## Build Suite

`make test`, the build's own tests.

```text
686 passed in 0.75s
```

Four are new, each over a whole run: the `source-changed` fault failing the run on its own recheck with `E_SOURCE_CHANGED` and publishing nothing to either stream or to a named file; the `internal` fault returning status 4 with `E_UNEXPECTED_INTERNAL_ERROR`; a run asking for no fault leaving its sources as it found them; and a fault the contract does not declare being refused as the usage failure it is.

## Corpus Run

`make corpus`, the whole corpus against the build under test.

```text
corpus check: 226 fixture(s), 226 pass, 0 fail, 0 awaited, 0 unexpected pass
```

Both fixtures run unmarked and hold:

```text
diagnostics/a-run-that-fails-in-itself: pass
source-consistency/a-source-that-changes-during-compilation: pass
```

The same run on the base reported `226 fixture(s), 224 pass, 0 fail, 2 awaited, 0 unexpected pass`, those two being the awaited ones. No fixture awaits work now.

## A Build That Reports Neither Outcome

The criterion requires the corpus run against a build that reports each outcome **and** one that does not, because an instrument that cannot fail a wrong build is no instrument. The second build is the same build reached through a wrapper that drops the fault request and runs on, which is what a build performing no fault does.

```python
def kept(arguments: list[str]) -> list[str]:
    """The command line with the fault request removed."""
    remaining = []
    skip = False
    for argument in arguments:
        if skip:
            skip = False
            continue
        if argument == "--fault":
            skip = True
            continue
        remaining.append(argument)
    return remaining
```

The corpus run against it fails exactly the two fixtures and nothing else:

```text
corpus check: 226 fixture(s), 224 pass, 2 fail, 0 awaited, 0 unexpected pass
```

```text
diagnostics/a-run-that-fails-in-itself: fail
  expected.exit_status: expected 4, the run exited 0
  expected.stdout: the bytes differ
    0 bytes expected, 212 produced
    the run's output carries 212 bytes beyond the end
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_UNEXPECTED_INTERNAL_ERROR expected, warning W_ENTRY_DESTINATION produced
source-consistency/a-source-that-changes-during-compilation: fail
  expected.exit_status: expected 1, the run exited 0
  expected.stdout: the bytes differ
    0 bytes expected, 301 produced
    the run's output carries 301 bytes beyond the end
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_SOURCE_CHANGED expected, warning W_ENTRY_DESTINATION produced
```

A build that performs neither fault publishes a bundle and exits 0, so each fixture fails on all three of status, standard output and diagnostics. The 224 fixtures either side of them are unaffected, which is what says the wrapper changed the one thing it was meant to.

## The Fixture Is Left As It Was

A `source-changed` fault writes to the tree it runs over, so a fixture declaring one runs in a copy of itself. After every run above, `git status --porcelain` named the eleven files this branch edits and no fixture source among them.

## The Consistency Family

The brief requires the family the row completes to be named by a fixture the corpus runs, not merely unmarked. The design's *Adversarial acceptance fixtures* list spells it **Consistency**, and the clause inventory writes a family as `Adversarial acceptance fixtures — <Family>, <case>`, which is the form every other family-naming manifest uses.

The declaration was the gap as well as the marker. On the base, no manifest carried the clause:

```bash
git grep -c 'Adversarial acceptance fixtures — Consistency' HEAD -- fixtures
```

returned nothing and exited 1. The source-consistency fixture now declares `Adversarial acceptance fixtures — Consistency, source modification during compilation` beside the two clauses it already carried, and [W01's family listing](../2026-10-21-9-i00-e10-w01-adversarial-fixture-families-and/family-listing.py), read against this branch's corpus, reports it held:

```text
held      Consistency          1
```

The listing's other families read UNHELD here because this branch is cut from `i00/e11/main` and the clauses that hold them were written on epic E10's base. The reading that matters is the one that changed: Consistency goes from held by nothing to held by one fixture.

## Whole Check Suite

`make check`, every target the repository runs, exit status 0.

```text
686 passed in 0.75s
538 passed in 9.41s
corpus check: 226 fixture(s), 226 pass, 0 fail, 0 awaited, 0 unexpected pass
invocation check: 28 statement(s) of the documented invocation, each held to the build PROSIFORM_BUILD names
```

The invocation check's count rises by one: `--fault {source-changed,internal}` is a row of the README's option table, reproducing the option's own help text, so the documented invocation and the command offer the same thing in both directions.

## What the Validation Found

- **The design record does not state `--fault`.** The contract is the design, and the option is now in the build, in the corpus and in the repository's documented invocation while the design's own text says nothing of it. It blocks nothing here and warrants a work item of its own, so it is deferred as [#177](https://github.com/m2ux/prosiform/issues/177).
- **A stale claim about what the corpus can state.** `src/tests/test_cli.py` opened by saying the corpus can state what a run does about a tree and never what it does about a tree being written. That stopped being true with this change and is restated as the design now is.
