# Reference Selection Validation

## Revision and Scope

- Head: `b02538060691f18231c4b9e6933e6fa411c02c5a`.
- Base: `227069a8fed00554deb7f044da37f396f35a3208` (`i10/e07/main`).
- Component: `src/prosiform/closure.py`; supporting occurrence-construction seams in `cli.py` and `dispatch.py`, plus `src/tests/test_selection.py`.
- `Reference.tags` holds normalized requested names. `BundleSelection` holds canonical path, optional fragment and effective declared named presets. Physical capture remains keyed by source path.

## Selection and Retention Checks

At the committed head:

```sh
uv run --project src --frozen pytest --config-file src/pyproject.toml src/tests/test_selection.py src/tests/test_closure.py src/tests/test_subst.py
```

Result: **250 passed**. [Focused output](selection-check.txt) records the run.

- Resolution and substitution retain the occurrence's tags, including fragment-only references and redirected section targets. A substitute's own declarations answer the retained tags.
- Immediate, deferred and dispatched links retain their own selections; same-heading links to one destination with different tags survive traversal while the physical source is captured once. Untagged outgoing links inherit no incoming tags.
- Matching compares complete normalized names case-insensitively in declaration order. Effective identities retain declared spelling and distinguish document, fragment and matched named-preset set.
- Reordering, repetition, unknown names and default tokens cannot create distinct effective identities. Empty and absent fragments share whole-document identity; diagnostic and heading context are absent from the bundle key.

## Full Deterministic Check

At the committed head:

```sh
PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w03-references-carry-effective-selection/src --frozen pf' make check
```

Result: **passed**, exit status 0. [Full output](make-check.txt) records:

- 1,797 source tests, including the selection and traversal checks.
- 1,404 deterministic check/harness tests.
- 518 corpus fixtures.
- Lock, lint, formatting, strict typing, installed-wheel smoke, layout, command tables, online links, vocabulary, invocation, conformance and independence checks all pass.

The runtime contract pin retains its 361 clauses and reports zero invalid fixture declarations or code mismatches. Its existing 64 uncovered clauses and other conformance coverage observations are retained; this task adds no conformance failure. The candidate design pin is adopted with the CLI/caller unit. No paid agent session is started.

## Diff Review

The redirect changes destination fields through an immutable dataclass replacement, preserving occurrence metadata and requested tags. The source-to-reference callers pass each parsed use's own tags through resolution. Dispatch reading uses the shared list reader on the resolved parser attribute. Traversal retention keys include requested tags, while discovery, source capture and source budgets keep their physical-path identity.

The destination matcher and effective identity are separate from activation, output naming and dispatch scheduling. The new API is directly observed by identity tests, and the tag retention seams are observed through actual source traversal. This unit claims reference retention and effective key semantics; the CLI-selection and dispatch-variant units deliver those runtime consumers.

The complete diff and immediate callers were inspected against the candidate design. No unresolved defect or outside-scope debt was found.
