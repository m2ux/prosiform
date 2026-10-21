# I00:E11 Base Rebuild - October 2026

> Validation record - Created 2026-10-21

## Executive Summary

This record holds the rebuild of the [I00:E11] Delivery Clear-Up base on `main` at `68944e8`, which carries the whole of [I00:E12] Positional Dependencies. The epic base `i00/e11/main` is this branch, and its head is `ce4483c`. It delivers no acceptance criterion of its own: it places E11's sixteen delivered commits on the design D60 states they must hold, and re-expresses I00:E11:W10 against the functions E12 left rather than merging into them.

The sixteen commits are replayed in the order they were authored, one per delivered row where a row carried one commit, so the branch records how it was built. Three of them carry a reconciliation the replay put in the row whose criterion states it.

## What Diverged

A trial merge of `origin/main` with `origin/i00/e11/main` at `45a531f` conflicted in four files. Each is resolved below, with the row that owns the resolution.

| File | Conflict | Resolved |
| --- | --- | --- |
| `src/prosiform/rewrite.py` | W10 made `destinations()` walk nested runs and return each marked link's destination; E12 made it return every link as `(destination, opening)` for one classifying pass | W10's `events()` walk under E12's signature and return: every link, as its destination and the opening of the run that carries it |
| `src/prosiform/candidate.py` | W10 changed `uses()` to `(children, at, Use)` and gave `intended()` the run rather than the inline token; E12 rewrote `intended()` around position, deferral and rebasing | W10's shapes with E12's body: `intended()` reads `opening_text(children, at)` and classifies by position, so a deferral written inside an image's alternative content is the deferral the author wrote |
| `src/tests/test_rewrite.py` | Both epics parametrized the same two tests | Both sets of cases kept, with W10's nested-image cases restated in E12's terms: an unmarked link inside an image's alternative content compiles and rewrites, and a deferred one rebases |
| `fixtures/README.md` | E11 added the warning and error rows its fixtures declare; E12 rewrote descriptions and removed `E_SELF_REFERENCE` and `E_MARKED_RESOURCE` | E12's catalogue text, plus E11's `E_ROOT_NOT_FOUND`, `E_PARSER_REFERENCE_LIMIT` and `W_EMPTY_GROUP_RULE` rows and its new sections. The retired codes appear nowhere in the tree |

## What W10's Change Became

The invariant is unchanged: an image's alternative content is a run of inline events of its own, so a link written there is read and compared where the parser puts it, and both sides of every comparison read the run the same way.

`source.events()` is the one walk over a run of inline events. It yields each link and image use with the run that carries it and its position in that run, descending into an image's alternative content where the image sits. Discovery (`source.uses()`), the occurrence count a budget is declared over (`source.occurrences()`), the emission's destinations (`rewrite.destinations()`, `rewrite.carried()`) and the candidate comparison (`candidate.uses()`) all read a run through it.

Two things the re-expression carries that the merge would not have:

- `rewrite.destinations()` keeps E12's signature and the classification it feeds. It returns every link as `(destination, opening_text)`, and the opening comes from the run the link was written in rather than from the top-level token, so position and deferral are still read in one pass and a link inside an image answers them on its own run.
- `candidate.intended()` classifies by position. W10's version tested a mark and stripped it; under D59 the mark defers and the bundle carries it, so the function reads the opening from the run passed in and leaves the mark alone.

`candidate.alternative()` survives as W10 wrote it: an image's own compared text is what its run shows with each nested link's text left out, because that text is compared on the nested link.

## What the Replay Restated

Three of E11's artefacts said "marked" where the old mark meant "bundle this". Under D59 a mark defers a compilation, so each is restated as the unmarked dependency the criterion is about, and each restatement sits in the commit for the row that owns it.

| Artefact | Row | Restated |
| --- | --- | --- |
| `fixtures/reference/a-link-inside-image-alternative-content` | W10 | Already renamed and rewritten on `main` by E12:W04. The replay lifts its `awaiting = "I00:E11:W10"` marker and nothing else |
| `src/tests/test_candidate.py` `NESTED_IMAGE` | W10 | `![of the [shared rules](rules.md) it names](plan.png)` - an unmarked link under the root, which is what AC10 states |
| `surrounded()` and `nested()` with the two `fixtures/parser-limit/` sources | W13 | The nesting ceiling is a bracket count, so the dependency under the brackets carries no mark. Expected output is unchanged, since the old expectation had the mark stripped |

`fixtures/marked-resource/` is not restored. E12:W04 deleted it when a resource became text wherever it resolves, and D60 retires AC9 and the W08 row.

## What Was Verified

`make check` passes whole on this tree, all thirteen targets, exit status 0, with `PROSIFORM_BUILD` naming the worktree's build:

```
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform" make check
```

| Target | Result |
| --- | --- |
| `lock-check` | 22 packages resolved against `src/uv.lock` |
| `lint` | All checks passed |
| `format-check` | 50 files already formatted |
| `typecheck` | no issues found in 49 source files |
| `test` | 670 passed |
| `harness` | 487 passed |
| `corpus` | 217 fixture(s), 217 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `smoke` | `prosiform` installs into an environment and bundles a reference from a source root |
| `layout` | 3 tree(s) present |
| `tables` | 14 command(s) and 7 declaration(s) |
| `links` | every reference in 12 document(s) resolved, online |
| `vocabulary` | 35 contract term(s), each defined and carried across 23 source(s) |
| `invocation` | 27 statement(s) of the documented invocation |

The corpus grows from `main`'s 210 fixtures to 217: the seven E11 adds are one allowed-source-root fixture, one informational version response, three number-sign fixtures and two parser-limit fixtures. No fixture carries the `awaiting` marker, which is what `main`'s two markers being lifted by W10 and W14 leaves.

Every delivered criterion AC1 through AC16, AC9 excepted, holds on the new base. AC9 is retired under D60 and its fixtures stay deleted.

## Contradictions

None. D59 and D60 both hold as written against what the rebuild found. Two details the records do not state, which the rebuild settled:

- `rewrite.carried()` on `main` already descended into an image's alternative content, while `source.uses()` and `source.occurrences()` did not. The emission therefore counted a nested link that discovery never saw. `events()` closes that, which is what W10's criterion is about.
- `main` already carries the W10 fixture under its unmarked name, because E12:W04 rewrote it. The replay had only the marker to lift, so no fixture was added for AC10.

## The Replayed Commits

| Commit | Row | Subject |
| --- | --- | --- |
| `d9c66a0` | W05 | report the fixtures awaiting one named piece of work |
| `eb05677` | W05 | document the request the corpus answers from its markers |
| `a30ed9b` | W12 | hold a document to a host answering 401 or 405 to both methods |
| `83e1be9` | W14 | report a grouping rule the closure leaves idle |
| `4d9fc88` | W04 | Hold a fixture's allowed source root to the outcome it declares |
| `9c17e67` | W02 | hold every declared warning to a fixture that states it |
| `6179822` | W06 | State a source path carrying a number sign in the corpus |
| `34ffb88` | W03 | Declare the text an output carries, and compare it |
| `ce17c86` | W03 | State the version response by what it reports |
| `cf2a7cd` | W03 | Tell the usage faults sharing one code apart |
| `fc66b50` | W10 | read an image's alternative content as the run of events it is |
| `0e99269` | W13 | report the reference lookups the parser's nesting ceiling declines |
| `c6d4f7d` | W13 | separate a declined lookup from a ceiling the last reference consumed |
| `1e641a5` | W01 | Hold the heading-slug rule to the anchors GitHub generates |
| `a462ff5` | W01 | Hold each standalone check's reading to input it would read wrongly |
| `ce4483c` | E11 | State the system as it is in every shipped document |

W07, W11 and W15 landed before the merge base and are carried by `main` already, so the replay adds nothing for them.

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#39 \[I00:E11\] Delivery Clear-Up](https://github.com/m2ux/prosiform/issues/39) |
| Design epic | [#136 \[I00:E12\] Positional Dependencies](https://github.com/m2ux/prosiform/issues/136) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W10 record | [A link inside image alternative content](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-20-89-i00-e11-w10-a-link-inside-image) |
| E12 integration record | [I00:E12 Positional Dependencies](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-136-i00-e12-positional-dependencies) |
