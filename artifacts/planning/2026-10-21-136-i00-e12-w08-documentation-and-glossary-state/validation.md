# Validation

The checks this row ran, the revision they ran against, and what each observed.

## Revision

- **Branch.** `i00/e12/w08-documentation-and-glossary-state` at `2a78a79`, cut from `i00/e12/main` at `72960bc`, which carries the merges of every behavioural row of the epic: `W01`, `W02`, `W03`, `W04`, `W05`, `W06` and `W07`.
- **Contract.** `artifacts/planning/2026-10-17-prosiform-v1/design.md` on `origin/engineering` at `0767da8`. The vocabulary check reads the design from the branch and path the README's Design link names, so the design edits this row makes are in its reach only once they are pushed.
- **Build under test.** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`, reached through its console entry point.
- **Commands.** Each is a named target of the repository's `Makefile`, run from the worktree root without the sandbox, because `uv` keeps its cache at `~/.cache/uv`, outside the sandbox's writable roots.
- **The base it starts from.** `72960bc` is green end to end, as `W07`'s record states and as the figures below confirm: the unit suite's 652 tests, the harness's 382 and the corpus's 210 fixtures are unchanged by this row, which adds no code and no fixture. The one figure that moves is the vocabulary check's inventory, from 34 contract terms to 35.

## The vocabulary check

`AC9` of the epic.

`make vocabulary` holds `docs/glossary.md` and the contract to one vocabulary, in both directions: a term the design marks that the glossary does not define fails it, and so does a definition neither the design nor an epic's acceptance criteria carry. It reports 35 contract terms marked in the design on `origin/engineering`, every one defined in the glossary, and every definition carried by the contract across 23 sources.

The term this row adds is the one the rule turns on. The design marks *deferral* where it first uses it, in *Explicitly linked source structure*, and `docs/glossary.md` defines it under References: what an author writes, that the target is required to exist and carried nowhere, that the bundle emits the link's text with its mark exactly as authored, and that its destination is the target's path from the root. `dependency` is defined with the condition position states — a target under the allowed source root whose author has not deferred it.

The check observes the statement rather than merely accompanying it. Deleting the glossary's definition leaves the mark in the design and the check fails with that term named:

```text
FAIL deferral — the design marks it as a contract term, and docs/glossary.md does not define it

vocabulary check: 1 term(s) the glossary and the contract disagree on
```

The definition restored, it returns 0 and the inventory it reports is 35. Dropping the design's mark instead leaves a definition the contract does not carry, which is the check's other failing case.

## What the documentation states

`README.md` carries all three answers a reference's position gives, each where the rule it qualifies is stated:

- The How It Works sequence follows supported local Markdown links under the allowed root to a fixed point, and confirms one its author defers rather than following it. Its rewrite step repoints a compiled reference at the fragment a renderer generates and a deferred one at its target's path from the root.
- The architecture list names the deferral as a term of its own, between the closure and the group.
- The paragraph that walks a run states the mark's four properties in the order a reader of a marked link needs them: not compiled by this run, its target confirmed and carried nowhere, the link's text emitted with its mark exactly as authored, its destination the target's path from the allowed source root, and a deferred reference naming no document or no heading failing like any other the root makes the run responsible for. That paragraph's failure list now names a reference under the root resolving to no heading beside one resolving to no document.

The link form the mark is written on is described rather than spelled, because `checks/links.py` resolves a link form inside a code span as a reference, which is the defect `I00:E11:W23` ([#147](https://github.com/m2ux/prosiform/issues/147)) takes.

## The contract's Validation scope

The design's *Validation scope* section names link resolution, supported selected syntax and resource rules within the selected dependency closure, and holds that an unrelated broken link in an unselected sibling must not fail bundling. Self-reference leaves both statements: a link naming the section it sits in resolves to that content's destination like any other reference the bundle carries, so no refusal follows from one in a selected region or in an unselected sibling. The behaviour is stated in *Self-reference and ancestor-reference behavior*, which describes resolution.

*Source and candidate validation modes* keeps its source-owned self-reference clause. Source mode decides identity from source ownership rather than from output structure, which is what makes a link to its own section resolve to that content, so that clause describes a live rule rather than the retired refusal.

## The retired codes

`E_MARKED_RESOURCE` and `E_SELF_REFERENCE` appear nowhere in the repository, in prose or in code. The error catalogue in `fixtures/README.md` declares neither, and the entry it carries for `E_SOURCE_OUTSIDE_ROOT` reads as the entry-reference refusal `W06` confined it to. No published document describes the mark as a request to bundle; `example/README.md` and the design both state the deferral. The grep this row owed is a clean sweep rather than a correction.

## The repository suite

`make check` exited 0 over `2a78a79`, with every target in the order the `Makefile` runs them.

| Command | Result |
| --- | --- |
| `make lock-check` | the lockfile describes the declared dependencies |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | no issues in 44 source files |
| `make test` | 652 tests, all passing |
| `make harness` | 382 tests, all passing |
| `make corpus` | 210 fixtures, 208 passing, 0 failing, 2 awaiting later work, 0 passing while awaiting it |
| `make smoke` | the wheel installs and bundles from a source root, outside the repository |
| `make layout` | 3 trees present |
| `make tables` | 14 commands and 7 declarations, each declared and named |
| `make links` | every reference in 12 documents resolved |
| `make vocabulary` | 35 contract terms, every one defined in the glossary |
| `make invocation` | 27 statements of the documented invocation held to the build |

The two awaiting fixtures are the ones the base carried: `reference/a-link-inside-image-alternative-content` awaits `I00:E11:W10`, and `grouping/a-rule-matching-no-document-in-the-closure` awaits `I00:E11:W14`.

## Links

`make links` resolves every reference the repository's documents carry, the fixture corpus excepted, and reports 12 documents. The three references this row writes into `README.md` are prose and a code span naming the mark's character; the documentation's existing links to the glossary and the design are unchanged and resolve.

The invocation check reads the README's option and exit-status tables against the build's own help output and reports 27 statements held. The prose this row adds sits outside those tables, so the documented invocation is the one the build prints, as it was on the base.
