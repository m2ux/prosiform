# Validation — The Example's Fixtures Regenerated Green

> Delivery Record · Created 2026-10-25

## What was delivered

Five fixtures under `fixtures/usage-example/` source the example tree the migration now delivers, and each expected bundle records what its invocation emits from it.

| Fixture | Source before | Source after | Bundle before | Bundle after |
| --- | --- | --- | --- | --- |
| `a-bare-fragment-and-its-referring-document` | `example/work-tracker` | `example/work-planner` | 4,720 | 11,866 |
| `a-procedure-and-everything-it-reaches` | `example/work-tracker` | `example/work-planner` | 5,057 | 203,906 |
| `every-document-under-a-directory-merged` | `example/work-tracker` | `example/work-planner` | 5,057 | 203,906 |
| `two-selected-sections` | `example/work-tracker` | `example/work-planner` | 4,765 | 11,911 |
| `validation-without-publication` | `example/work-tracker` | `example/work-planner` | 0 | 0 |

Five sources repointed. Five expected bundles re-recorded; the two that compile a procedure now emit the same bytes, because both invocations name `modes/plan-mode.md` and the build emits one bundle for one entry.

## The corpus

`PROSIFORM_BUILD=<worktree>/src/.venv/bin/pf make corpus`:

```text
corpus check: 260 fixture(s), 260 pass, 0 fail, 0 awaited, 0 unexpected pass
```

The figure is unchanged from the base — 260 fixtures, 260 pass — and the five usage examples now pass against the delivered tree rather than the one it replaced. The five lines the run prints for the family:

```text
usage-example/a-bare-fragment-and-its-referring-document: pass
usage-example/a-procedure-and-everything-it-reaches: pass
usage-example/every-document-under-a-directory-merged: pass
usage-example/two-selected-sections: pass
usage-example/validation-without-publication: pass
```

## Checks

| Check | Command | Result |
| --- | --- | --- |
| Corpus | `PROSIFORM_BUILD=…/pf make corpus` | 260 fixtures, 260 pass, 0 fail, 0 awaited, 0 unexpected pass |
| Conformance | `PROSIFORM_BUILD=…/pf make conformance` | 305 clauses, 55 covered by no fixture, 0 declarations naming no clause, 32 declared names reached, 0 unfixturable, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere, 16 clauses no run states, 3 non-behavioural sections, 3 unobserved installation claims — exit 0 |
| Independence | `PROSIFORM_BUILD=…/pf make independence` | 2,561 words, 260 fixtures and their identities, the conformance report — exit 0 |
| Links | `make links --online` | every reference in 101 documents resolved — exit 0 |
| Layout | `make layout` | `docs/` 10 files, `fixtures/` 964 files, `src/` 39 files — exit 0 |
| Superseded tree | `rg -l 'example/work-tracker' fixtures/` | no path |

`make check` was not run.

## The diagnostics each fixture records

Four fixtures compile and emit one `W_ENTRY_DESTINATION`; `two-selected-sections` emits two, one per selected section. Each is expected, and the manifests declare them unchanged:

| Fixture | Exit | Diagnostics |
| --- | --- | --- |
| `a-bare-fragment-and-its-referring-document` | 0 | `W_ENTRY_DESTINATION` `Record Epic Delivery` → `record-epic-delivery` |
| `a-procedure-and-everything-it-reaches` | 0 | `W_ENTRY_DESTINATION` `Procedure` → `procedure` |
| `every-document-under-a-directory-merged` | 0 | `W_ENTRY_DESTINATION` `Procedure` → `procedure` |
| `two-selected-sections` | 0 | `W_ENTRY_DESTINATION` `Record Epic Delivery` → `record-epic-delivery`; `W_ENTRY_DESTINATION` `Delivery Findings` → `delivery-findings` |
| `validation-without-publication` | 0 | `W_ENTRY_DESTINATION` `Record Epic Delivery` → `record-epic-delivery`, with no bytes on standard output |

## `two-selected-sections` needed no completion

The brief and this record's own plan state that `two-selected-sections` declares no entry argument and fails as invalid usage, and that its manifest needs the arguments its sibling names. That was not true of the base at `3a623c9c`. The manifest declares both arguments:

```toml
[invocation]
cwd = "source"
arguments = [
  "artifacts/epic-issue-body.md#record-epic-delivery",
  "artifacts/epic.md#delivery-findings",
]
```

They are the two section references its description names: the first selects the `*Record* Epic Delivery` operation from the epic issue body, and the reference inside that operation carries `artifacts/epic.md#delivery-findings`. They were committed with the fixture at `8ecd7f4e` and no later commit moved them.

So the fixture compiles at exit 0 with two warnings and needed no edit to its invocation. The manifest change this row makes is none: only the source link and the expected bytes move. The claim is corrected in `README.md` and `w06.md`.

## Fixture prose

`fixtures/README.md` named `example/work-tracker` as the tree the family reaches. The sentence naming the link target now reads `example/work-planner`, which is what the brief's own grep requires: a document under `fixtures/` is not a fixture, but the search that proves no fixture sources the superseded tree reads it. No other prose changes; `example/README.md`, `invocation.md` and the rest of the family's documentation are W07's.

## Debt

Nothing non-trivial surfaced. Two observations were classified and neither warrants a row on [#263](https://github.com/m2ux/prosiform/issues/263):

- **Two fixtures record the same bundle.** `a-procedure-and-everything-it-reaches` and `every-document-under-a-directory-merged` both invoke `modes/plan-mode.md`, and one entry produces one bundle, so 203,906 bytes appear twice. The duplication is the corpus recording one invocation twice under two different clause sets, which is what the two fixtures are for.
- **`validation-without-publication` records an empty file.** Its declared outcome is no bytes on standard output, which the check compares as bytes.

## Delivery

Merged as [#270](https://github.com/m2ux/prosiform/pull/270) into `i02/e00/main`, merge commit `714c95c1`. `i02/e00/main` is unmerged into `main`; W07 is the epic's remaining row.

## Not changed

- **No document under `example/work-planner`.** The tree is W01–W05's delivered work, and every fixture passes against it as it stands.
- **No deletion of `example/work-tracker`.** Nothing in this row removes it; it remains the four-file reduction the migration grew from.
- **No fixture invocation.** Every argument list is as the base declares it.
- **No build source, check or manifest schema.**
