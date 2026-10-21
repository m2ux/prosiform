# Validation

The checks this row ran, the revision they ran against, and what each observed.

## Revision

- **Branch.** `i00/e12/w07-a-deferred-target-confirmed` at `8c88969`, cut from `i00/e12/main` at `b7eac62`, which carries the merges of `W06`, `W03`, `W04`, `W05` and `W02`.
- **Build under test.** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`, the build the change produces, reached through its console entry point.
- **Commands.** Each is a named target of the repository's `Makefile`, run from the worktree root without the sandbox, because `uv` keeps its cache at `~/.cache/uv`, outside the sandbox's writable roots.
- **The base it starts from.** `make check` was run over `b7eac62` before any change: every target passed and the corpus reported 207 fixtures, 205 passing, 2 awaited. The figures below are read against that.

## A deferred reference naming no document

`AC10` of the epic, `AC1` of the task.

`test_a_deferred_reference_naming_no_document_fails` declares a root holding one document that defers a second one the root does not carry. The run exits 1, its only diagnostic is `E_TARGET_NOT_FOUND`, and standard output is empty, so the run publishes nothing.

`deferral/a-deferred-reference-naming-no-document` states the same against the running build. Its manifest declares the exit status, the empty bundle and the diagnostic's reference, source location and chain, so the corpus holds the refusal's wording as well as its code.

On the base, that reference published a bundle and exited 0 while the same reference unmarked was refused. The two halves of the rule now answer alike.

## A deferred reference naming no heading

`AC10` of the epic, `AC2` of the task.

`test_a_deferred_reference_naming_no_heading_fails` defers `rules.md#absent` against a document carrying `## Here` and nothing else. The run exits 1 and publishes nothing, and the diagnostic names the reference `rules.md#absent`, the resolved path `rules.md` and the chain `guide.md → rules.md#absent`, which is the route the run followed to the link.

`deferral/a-deferred-reference-naming-no-heading` states it against the build, with the same fields declared.

`test_a_heading_a_container_carries_confirms_a_deferral` marks the boundary of the question this row asks. A fragment naming a heading written inside a list confirms the deferral and the run succeeds, because confirmation asks whether the document carries the heading. Which section a fragment roots, and whether two headings make it ambiguous, is what the run that compiles the link decides.

## A deferred link's destination

`AC4` of the epic, `AC4` of the task.

`test_a_deferred_destination_is_the_target_path_from_the_root` defers `../shared/rules.md#here` from `topic/guide.md`. The published link carries its mark and the destination `shared/rules.md#here`, which is the target's path from the allowed source root.

`closure.rebased()` is held to the spelling directly by `test_a_deferred_destination_names_its_target_from_the_root`, over five cases: a path rising out of a directory, the same path with a fragment, a fragment-only link naming its own document, an empty fragment carried as authored, and a filename holding a percent-escaped number sign, which is republished escaped so the resolution sequence decodes it once to the name the filesystem carries.

`deferral/a-deferred-destination-named-from-the-root` states it against the build, and `deferral/a-deferred-fragment-of-its-own-document` now publishes `guide.md#beta` where it published `#beta`, which is the same rule read on a link that names no path at all.

`test_a_deferred_reference_leaving_the_root_is_not_confirmed` holds the other side: a mark on a reference that normalizes above the root changes nothing, the destination is the authored one, and no confirmation is attempted.

## A document only a deferral names

`AC3` of the task.

`test_a_document_only_a_deferral_names_contributes_nothing` defers `../shared/rules.md` and reads the bundle back: the target's file heading is absent and so is its body, so the document is confirmed without being bundled, takes no destination of its own and heads no file group.

`deferral/a-deferred-destination-named-from-the-root` shows the same bytes against the build: its bundle is the entry line and the deferring document alone.

`deferral/a-deferral-stands-where-another-reference-carried-its-target` keeps the converse. A document a second reference required is carried by that reference, and the deferred link to it is published with its own destination rather than with the bundle's.

## The example tree

`example/work-tracker/modes/plan-mode.md` named its routing document in prose, because a link to it under the root would have carried it. It now links that document and defers it, which `W01` and `W02` each left to this row because a deferral written before the rebase would have published a destination this row changes.

The two `usage-example/` bundles the tree feeds were regenerated once. Each publishes `[¬ SKILL.md](SKILL.md)` where its author wrote `../SKILL.md`, and neither carries a heading or a line of `SKILL.md`, so the tree now shows every answer position gives and the rebase is visible in a published bundle.

The output budget in `docs/output-budget.md` is unchanged. It measures the `work-planner` closure at `acac858`, which carries no deferral, so no deferred destination enters that figure.

## Unit suite

`make test` — 652 tests, all passing. Twenty of them are this row's: the eight named above, and twelve cases holding `closure.deferring()` and `closure.rebased()` to the rule directly.

The tests that changed are `rewrite`'s own. The destination now arrives at the rewrite whole, so a fragment of the bundle and a path from the root are published the same way, and the cases that passed a bare fragment pass `#rules`. One of them deferred a link and expected no destination; it now expects the rebased one.

## Corpus

`make corpus` — 210 fixtures, 208 passing, 0 failing, 2 awaiting later work, 0 passing while awaiting it. The two awaiting fixtures are the ones the base already carried: `reference/a-link-inside-image-alternative-content` awaits `I00:E11:W10` and `grouping/a-rule-matching-no-document-in-the-closure` awaits `I00:E11:W14`.

Three fixtures are this row's, and two the base carried were regenerated: `deferral/a-deferred-fragment-of-its-own-document` for the rebase, and the two `usage-example/` bundles for the example tree. Every other fixture produced the bytes its manifest declares.

## The harness suite

`make harness` — 382 tests, all passing. The three beyond the base's 379 are the harness's own reading of the three fixtures this row declares.

## Repository checks

Each ran against the same revision, in one `make check` that exited 0.

| Command | Result |
| --- | --- |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | no issues in 44 source files |
| `make lock-check` | the lockfile describes the declared dependencies |
| `make layout` | 3 trees present |
| `make tables` | 14 commands and 7 declarations, each declared and named |
| `make vocabulary` | 34 contract terms, every one defined in the glossary |
| `make links` | every reference in 12 documents resolved |
| `make invocation` | 27 statements of the documented invocation held to the build |
| `make smoke` | the wheel installs and bundles from a source root, outside the repository |

The catalogue the harness enumerates is the catalogue the design declares, as it was on the base. This row adds no code and retires none.

## A check that reads a link inside a code span

`checks/links.py` reported `example/README.md` as naming `../SKILL.md`, a reference the document spells inside a code span as an example of the syntax. The check scans for the link form without masking code first, so an example of a link reads as a link.

The prose was written another way and the check passes. The scanner is the defect, and it belongs to the check rather than to this row: the [change list](changes.md) carries it as deferred debt.
