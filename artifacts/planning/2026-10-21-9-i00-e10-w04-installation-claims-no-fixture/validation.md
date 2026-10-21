# Validation — I00:E10:W04+W05

Every run below was made unsandboxed from the worktree `.worktrees/i00-e10-w04`, with the build under test named by

```bash
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"
```

## The base measured first

`make check` at the branch point `68a56a1`, which is `i00/e10/main` as this unit starts, returns 0. Its build suite is 682 tests, its harness suite 553, its corpus run reports 231 fixtures with 229 passing and 2 awaited, and its conformance report closes

```text
conformance report: 253 clause(s) the design states, 66 covered by no fixture,
0 declaration(s) naming no clause; 27 declared name(s) reached, 3 unfixturable
```

A result on the branch is therefore attributable to the branch.

## The installation claims

`make conformance` prints the three claims at the end of its declared-surface listing, each as the unfixturable entry it is, with the reason it is unreachable and the run that would observe it:

```text
installation claim another platform: unfixturable, the smoke run observes this host
and the continuous-integration runner, and a platform whose command wrapper and path
resolution differ is a different mechanism
    observable once a run installs the build and invokes it by name on that platform
installation claim a machine that never held the repository: unfixturable, the
repository is on disk throughout the run and merely unreachable by path, working
directory and environment, and removing it is not something a check inside it can do
    observable once a run installs the build on a machine the repository was never
    copied to
installation claim the command line the documentation gives a reader: unfixturable,
the run installs an artefact it builds rather than running the command line the
documentation's installation section states
    observable once a run executes that documented command line and invokes the
    command it installs
```

The three are the three the I00:E07:W01 installation record states, and they are now read from the report rather than from that dated folder. The closing line counts them beside the declared names:

```text
conformance report: 253 clause(s) the design states, 66 covered by no fixture,
0 declaration(s) naming no clause; 27 declared name(s) reached, 3 unfixturable,
3 installation claim(s) no run observes
```

The declared-name figures are the base's: this row adds no fixture and changes no manifest, because an installation is not a thing a fixture can name.

## The conformance suite

`make harness` grows by the three cases of `checks/tests/test_conformance.py` that hold the listing's shape, from 553 to 556.

- **A claim is listed with the reason it is unreachable.** The rendered report carries the entry in the same shape the unfixturable exit statuses take, `installation claim <name>: unfixturable, <reason>`.
- **A claim states what would observe it.** The line under each entry is that claim's remedy, for every claim declared.
- **The summary counts the claims.** The report's closing line ends with the number of installation claims no run observes.

Each case reads the report rendered over the suite's own small design and corpus rather than this repository's, so what it states is what the check prints rather than what this repository happens to hold.

## The unexpected-internal-error outcome

Two cases in the build's command suite hold the outcome an error the contract names no outcome for produces, taking `make test` from 682 to 684. Each makes the composition the command calls raise an error of a kind the contract names nothing for, which leaves `execute` and reaches the command's generic handler without breaking any invariant of the build's own construction.

- **As the data a caller parses.** The run returns the declared internal-error status, publishes nothing to standard output, and standard error carries exactly one diagnostic, whose severity is `error` and whose code is the declared unexpected-internal-error code.
- **As the line a reader reads.** The same run under the reader's format returns the same status, publishes nothing, and standard error carries exactly one line, headed with the declared code and carrying the error raised. The reader's format renders a diagnostic under its code and prints no severity field, so the severity is observed there through the code being one the error catalogue declares.

The status and the code are named by the declarations `prosiform.cli` makes rather than spelled into the cases, so a build renaming either fails them rather than satisfying a copy of the old spelling.

The case already in the suite — a candidate disagreeing with the provenance its construction recorded — is left as it stands. It reaches the same handler, but what it states is that one of this build's own invariants reports the declared status, which is a narrower claim than the criterion makes and is worth keeping on its own terms.

## The repository check set

`make check` on `i00/e10/w04-installation-claims-no-fixture` at `98e4a86` returns 0. Each of its fifteen targets passes: the lock check, lint, format check, type check, the build's own suite of 684 tests, the harness suite of 556, the corpus, the smoke run, and the layout, table, link, vocabulary, invocation, conformance and independence checks.

```text
corpus check: 231 fixture(s), 229 pass, 0 fail, 2 awaited, 0 unexpected pass
table check: 16 command(s) and 7 declaration(s), each declared by the project and
named by a table
independence check: 60 term(s), named by no fixture declaration, no report entry
and no name the contract declares
```

`make independence` is what holds the new entries to the contract's own words: the check scans the conformance report as it renders, so the three claims pass under it rather than beside it. `make tables` holds the two command tables naming `make conformance` to the listing the check now prints.

## What the validation found

- **The claims are a declaration, and a declaration can outlive what made it true.** They sit beside the surface the report renders, and nothing ties them to the steps the smoke run performs: a run that came to execute the documented command line would leave its claim standing until someone removed it. Binding each claim to the step that would observe it is the direction, and it is non-trivial and blocks nothing here, so it is deferred.

- **The suite states the listing's shape rather than its content.** The three cases read the declared claims and assert the lines the report renders for them, so they hold the entry shape, the remedy line and the count. A claim whose wording went stale would still pass, which is the same gap the point above names.

- **The reader's format carries no severity field.** It renders a diagnostic under its code and prints the rest of the fields it carries, so the severity is a property of the code rather than of the line. The criterion's `error diagnostic` is therefore observed in that format through the code being one of the error catalogue's, and in the data format through the field itself. The reading is correct and there is nothing to fix.

- **An installation is not a thing a fixture can name.** The corpus declares a source tree and the bytes a run returns for it, and it reaches the build under test through configuration. Both rows of this unit are instruments outside the corpus for that reason, and the catalogue entries and the fixture count are the base's.

## What could not be ticked

**AC7 is ticked.** Each installation claim the smoke run cannot observe is listed as unfixturable in the conformance report's declared-surface listing, with the reason it is unreachable and what would make it observable, as `make conformance` shows and the three harness cases hold.

**AC8 is ticked.** A command whose execution raises an error the contract does not name returns the declared internal-error status and emits one error diagnostic carrying its declared code, in both diagnostic formats, as the two cases of the build's command suite show.

**AC1 stays unticked**, which is the epic's reading unchanged. It waits on the two adversarial families W01 left held by nothing, each a tracked row of [#39](https://github.com/m2ux/prosiform/issues/39). The epic is therefore not complete on this merge, and [#168](https://github.com/m2ux/prosiform/pull/168) stays a draft.
