# Validation

Candidate: `aa1baf2f97720a94854fbeabdf66e3abdb407a48` on `786-comment-cleanup`.
Baseline: `e2dde5e569800e5584797bb194bb989f8fb2843b` on `main`.

## Module Review

AC1 was reviewed against [the repository convention](https://github.com/m2ux/prosiform/blob/aa1baf2f97720a94854fbeabdf66e3abdb407a48/AGENTS.md), delivered by #788. Its final home is AGENTS.md; the issue's src/README.md citation predates that final scope. Every docstring, attribute document and comment in all 21 modules was read. All 21 modules have prose corrections. Owner-local details remain at implementing units, while callers name the owner and rule.

The inventory covers 687 docstrings and attribute documents plus 19 comments. Counts identify this revision's review scope, not an automated proof of prose meaning. The [reference audit](owner-references.json) resolves each package-qualified owner reference against the source AST and finds none missing. Cross-group reviews checked factual accuracy, ownership, residual paraphrases and caller invariants. Review corrections include fragment allocation, suffix removal, the operator's required ASCII space, unmatched fragments, preamble boundaries, generated-heading collisions, parser invocation and narrow owner attributions. These are documentation corrections to existing behavior.

| Module | Documents | Comments | Owner review |
| --- | --- | --- | --- |
| __init__.py | 2 | 0 | Package responsibility and PROFILE identifier. |
| access.py | 12 | 0 | opened and walked_directory own access; read_source owns overflow reads. |
| bundle.py | 54 | 4 | rewrite owns emission edits; diagram_labels owns label edits; shifted owns heading shifts. |
| candidate.py | 49 | 0 | validate and comparison helpers own candidate checks; source.Click owns diagram fields. |
| cli.py | 133 | 7 | Argument actions own option rules; selection owns region union; traverse owns discovery; publish_folder owns publication. |
| closure.py | 76 | 0 | resolve owns path grammar; named and resolvable own classification; operators owns admitted operations. |
| composition.py | 29 | 0 | Composing.copy owns body emission; flush owns groups; cycle owns cycle refusal. |
| diagnostics.py | 9 | 0 | Diagnostic.fields owns field omission; json/text own rendered formats. |
| dispatch.py | 56 | 7 | Placing.place owns dispatch sections; briefed owns hand-off placement; element_text owns label fallback. |
| entry.py | 6 | 0 | markdown_link, diagram_link and published own accepted entry forms; source.Click owns diagram fields. |
| grouping.py | 38 | 0 | prepared owns member preparation; assembled owns grouping; joined_title and related helpers own names. |
| heading.py | 3 | 0 | title_cased owns word capitalization; worded owns the word test. |
| limits.py | 10 | 0 | Budget holds declarations; Limits.hold owns crossing; in_force owns default completion. |
| marks.py | 4 | 0 | opened owns opening recognition; marked owns title-mark recognition. |
| metadata.py | 29 | 0 | decode owns payload validation; _kind owns scalar typing; _scalar owns scalar construction. |
| preamble.py | 5 | 0 | selected owns the H1 preamble boundary; rewritten_preamble and grouped describe their own operations. |
| profile.py | 29 | 1 | parser owns dialect configuration; parse orchestrates; refusal helpers own construct refusals. |
| provenance.py | 28 | 0 | Value records describe fields; link_at and click_at own occurrence identity. |
| rewrite.py | 38 | 0 | rewritten and its lexical helpers own inline edits; gained owns title extension. |
| source.py | 74 | 0 | section owns source selection; uses owns occurrences; Click owns diagram fields; linked owns line grammar. |
| tags.py | 3 | 0 | read owns name normalization; picks owns agent-pick recognition. |

## Diagram Rule

AC2: source.Click describes the diagram-link fields, including the element text supplying operator marks and the tooltip supplying preset tags. Other modules refer to source.Click. Source grammar, construction, profile refusals and emission each describe their own operations without repeating that field interpretation. The all-module reading and [owner inventory](owner-references.json) include closure, tags, candidate, dispatch, profile and entry, which the issue identifies as repeated descriptions.

## Behavior Comparison

AC3: [comparison.json](comparison.json) records all 708 fixtures and their outputs. Both builds use the same pristine fixture paths through the existing corpus runner. Every fixture passes for both revisions; exit status and verdict agree, and all 614 generated files, totaling 175886 bytes, compare directly equal as byte strings. The report records each file's name, size and SHA-256. Executable AST structure is identical across all 21 modules after string-expression documentation is excluded. No imports, signatures, runtime values, tests or fixtures change.

The [comparison driver](compare.py) uses [invoke.py](invoke.py) to select source trees while sharing the locked interpreter. Its recorded paths identify the exact local checkouts. From the candidate worktree, the run is:

```sh
SBX_EXTRA_ROOTS=/home/mike1/projects/dev/ghsa-classifier/.worktrees/prosiform-786-base /home/mike1/projects/dev/ghsa-classifier/scripts/sbx src/.venv/bin/python /tmp/prosiform-786-compare.py
```

## Required Checks

AC3: `make check` exits 0 at the candidate revision. [make-check.log](make-check.log) records lock verification, lint, formatting, strict typing, 2303 compiler tests, 1153 harness tests, all 708 corpus fixtures, installed-wheel smoke, layout, documentation tables, online links, vocabulary, invocation, conformance and independence checks. Conformance reports its existing uncovered clauses; this prose-only task adds no conformance coverage.

```sh
PROSIFORM_BUILD=/home/mike1/projects/dev/ghsa-classifier/.worktrees/prosiform-786/src/.venv/bin/pf make check
```

[GitHub Actions Checks](https://github.com/m2ux/prosiform/actions/runs/45009844790) also passes at the candidate revision. Its optional eval-harness step is skipped by the workflow.

`git diff --check` passes. New runtime tests are unnecessary because executable syntax and fixture bytes are identical.

## Delivery Boundary

The target is main. Its live rules require one approving review. The PR is handed to its human reviewer for approval and merge; the issue remains open until merge and closure readback. The user confirmed repository auto-close is disabled on 2026-11-22. PR #843 is linked to issue #786 through Development; development-link.py read both ends back and verified the relation. No repository setting is changed.
