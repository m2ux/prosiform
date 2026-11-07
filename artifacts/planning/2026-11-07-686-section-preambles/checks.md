# Checks

## Full Repository Validation

`make check` passed at `d71a9867a88f005b347d39473c158814f25ea1ac`, with the build under test configured to that checkout's `pf`.

- 1,904 Python unit tests passed.
- 973 harness tests passed.
- 537 corpus fixtures passed, including the new shared-preamble fixture.
- Lint, formatting, strict typing, wheel installation, layout, documentation, invocation, conformance and independence checks passed.

## Work-Tracker Example

`pf modes/plan-mode.md` exited 0 and emitted H2 `Artifacts` with H3 `Epic-Issue-Body` and `Epic` preambles. The empty `Overview` member structure was absent.

## Independent Review

The Codex review invocation was refused by the workspace owner's spend cap and returned no findings. The full main-to-head diff was inspected locally. No unresolved local findings remain.

## Merge Boundary

The `main` ruleset requires one approving review. The agent cannot approve its own pull request, so merge remains with the required reviewer. CI passed and PR 687 is ready for review; F04 is In Review on the Python board.
