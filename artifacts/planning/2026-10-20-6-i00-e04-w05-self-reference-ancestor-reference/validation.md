# Validation Record — I00:E04:W05 and W06

> Measured 2026-10-20 against `i00/e04/main` at `4d0cda2` and the delivery branch above it.

## The Behaviour Measured Before the Design Was Built To It

Each run below used the delivery build against a scratch tree, before any change to the repository.

**A direct self-reference succeeded.** `guide.md` carrying a section `Alpha` whose body marks `guide.md#alpha`:

```
prosiform --root source 'guide.md#alpha'
```

Exited 0 and published the section, the mark still in its text. Nothing in the build classified a reference against the node that carried it, so the clause calling this a compile error had no instrument at all.

**An ancestor reference already held.** `guide.md` with `Alpha` containing `Detail`, whose body marks `guide.md#alpha`:

```
prosiform --root source 'guide.md#detail'
prosiform --root source 'guide.md#alpha'
```

Both exited 0. The first expanded the closure to the ancestor and carried the child once inside it; the second carried the same regions with the child already consolidated. The traversal's identity set is what makes a reference to a present destination add nothing, and that was delivered by [W03](https://github.com/m2ux/prosiform/pull/77).

**Ownership had nothing to be stable about.** The two runs above differ only in what was selected, and they produced the same regions before this row as after it. What the row adds is a classification that could have depended on the selection and does not: the owner is the innermost eligible section containing the link, read from the document's structure.

**A marked resource was published with its mark.** `guide.md` marking `plan.png`:

```
prosiform --root source 'guide.md'
```

Exited 0 and emitted `[¬ diagram](plan.png)` whole, which is the collision [D40](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) settles.

**No budget existed.** `prosiform --root source --max-files 1 guide.md` exited 2 with `E_INVALID_USAGE`: `unrecognized arguments`. None of the eight options was declared, and the catalogue carried no code a crossing could report.

## What the Measurement Changed in the Plan

**AC4 needed a code the contract did not name.** The design holds that a link from section A to the same canonical section A is a compile error and names no code for it, and the catalogue carried none. That is the same gap [D41](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) closed for the budgets, one clause further on, and it made AC4 as undeliverable as AC7 was. It is settled as [D42](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md): `E_SELF_REFERENCE`, landing in the same window as the other two. The error catalogue stood at twenty and ends at twenty-three, which is three more rather than two; with the two warning codes beside it, the two catalogues hold twenty-five.

**Neither AC4 nor AC13 was already delivered.** The previous row found two of its criteria held on the base and needed corpus evidence alone. The half of AC4 about an ancestor reference is in that state; its other half, and AC13's ownership model, are not. One implementation serves both: the owner of a link decides the classification, and because the owner is read from the document rather than from the selection, AC13 follows from AC4's implementation rather than needing one of its own.

## The Instrument Behind Each Criterion

| Criterion | Instrument | Verdict |
| --- | --- | --- |
| AC4 | `self-reference/a-link-to-the-same-section`, `self-reference/a-link-spelled-another-way-to-the-same-section`, `self-reference/a-preamble-link-to-its-own-document`, `self-reference/a-link-back-to-an-including-ancestor`, `self-reference/a-section-link-to-its-whole-document`, `self-reference/a-link-to-another-section-of-the-same-file` | Met |
| AC13 | `ownership/an-ancestor-reference-with-the-child-selected`, `ownership/an-ancestor-reference-after-consolidation`, `ownership/a-self-reference-after-consolidation` | Met |
| AC17 | `marked-resource/marking-a-non-markdown-reference`, `marked-resource/marking-a-reference-carrying-a-scheme`, `marked-resource/the-same-references-unmarked` | Met |
| AC7 | `limits/a-file-count-budget-crossed`, `limits/a-source-byte-budget-crossed`, `limits/an-input-byte-budget-crossed`, `limits/an-output-byte-budget-crossed`, `limits/a-target-budget-crossed`, `limits/a-link-budget-crossed`, `limits/a-nesting-budget-crossed`, `limits/an-expansion-depth-budget-crossed`, `limits/a-zero-override-is-refused`, `limits/a-negative-override-is-refused` | Met |
| AC11 | `limits/an-expansion-depth-budget-crossed`, `limits/a-target-at-the-expansion-depth` | Met |

The ownership pair is one document run twice. Its two expected bundles differ only in the entry line, which names the reference the caller gave; every region below it is identical, which is the criterion stated as an artifact rather than as a comparison a runner performs.

The eight crossings each declare `exit_status = 1` and an empty expected standard output, so no fixture can pass on a run that truncated its bundle to fit. `limits/an-output-byte-budget-crossed` is the one that could only fail by publishing, and it publishes nothing.

## What Each Command Returned

```
PROSIFORM_BUILD="uv run --project .../src --frozen prosiform" make check
```

| Target | Output |
| --- | --- |
| `lock-check` | `Resolved 22 packages` |
| `lint` | `All checks passed!` |
| `format-check` | `31 files already formatted` |
| `typecheck` | `Success: no issues found in 30 source files` |
| `test` | `397 passed in 0.26s` |
| `harness` | `268 passed` |
| `corpus` | `corpus check: 127 fixture(s), 124 pass, 0 fail, 3 awaited, 0 unexpected pass` |
| `layout` | `layout check: 3 tree(s) present` |
| `tables` | `table check: 12 command(s) and 7 declaration(s), each declared by the project and named by a table` |
| `links` | `link check: every reference in 6 document(s) resolved` |
| `vocabulary` | `vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 23 source(s)` |

The base held 104 fixtures, 101 passing and 3 awaited. This unit adds twenty-three fixtures and no marker.

Before the design push, `harness` reported one failure and nothing else: the catalogue test, with the three codes in the schema and not yet in the design on `origin/engineering`. That is the window, and it is the only check either half of this change can fail on its own.

## The Design-Push Window

The catalogue test reads the design from `origin/engineering` and the catalogue from the schema on the branch under test, so the two halves cannot both hold on every branch at once. The implementation was finished and every other check was green before the design push, so the window is bounded by two pushes rather than by the work.

Continuous integration runs on a push to `main` and to an `i00/**` branch, and on nothing else, so the push to `engineering` starts no run of its own and the window is the interval between it and the branch push that closes it.
