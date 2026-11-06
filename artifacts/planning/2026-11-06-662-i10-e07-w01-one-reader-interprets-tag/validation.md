# Shared Reader Validation

## Revision and Scope

- Head: `27ad770d9f6157a720a0b9f95deda1b2c12d0fff`.
- Base: `ba93ca60860f0dc46722f27acd471740465279da` (`i10/e07/main`).
- Files: `src/prosiform/tags.py`, `src/tests/test_tags.py`.
- The shared `read(str | None) -> frozenset[str]` routine normalizes a decoded list; target declarations decide matching, implicit default and precedence.

## Focused Reader Checks

Command at the recorded head:

```sh
uv run --project src --frozen pytest --config-file src/pyproject.toml src/tests/test_tags.py
```

Result: **14 passed** in 0.04 seconds.

The tests observe absent/empty inputs, Unicode whitespace, Unicode case folding, complete multiword names, duplicates, reordered inputs, literal commas and names retained for destination matching. The returned selection is immutable.

The adapter cases parse actual inline and reference-style Markdown titles containing an encoded comma and compare their decoded values with a shell-decoded argument passed to the same reader. This establishes decoded-input parity. It does not claim the source and CLI consumers are wired to the reader; that runtime integration is verified by the joined CLI/guide unit's AC3.

## Full Deterministic Check

Command at the recorded head:

```sh
PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w01-one-reader-interprets-tag/src --frozen pf' make check
```

Result: **passed**, exit status 0. Results are captured in [make-check.txt](make-check.txt):

- 1,745 source tests, including all 14 reader cases.
- 1,402 deterministic check/harness tests.
- 516 corpus fixtures.
- Lock, lint, formatting, strict typing, installed-wheel smoke, layout, command tables, online links, vocabulary, invocation, conformance and independence checks all pass.

The unchanged runtime contract pin reports 361 clauses and zero invalid fixture declarations or code mismatches. Its 64 uncovered clauses and other reported conformance gaps are existing coverage observations, rather than failures introduced by this reader. The candidate E07 contract becomes the runtime pin with its observing caller/fixture delivery. No paid agent session is part of this command.

## Diff Review

The reader has no mutable state or dependency on source parsing, CLI grammar, preset metadata or output naming. It splits decoded input once on commas, trims each token, case-folds nonempty names and returns a frozen set. There is no substring matching or per-token escape grammar. The operation neither filters unknown names nor treats `default` specially because both decisions require destination selection semantics.

The full diff and immediate consumer boundaries were reviewed against the current candidate design. No defect or outside-scope debt was found. No runtime guide, CLI option, contract pin, package requirement or historical fixture assertion changes in this task.
