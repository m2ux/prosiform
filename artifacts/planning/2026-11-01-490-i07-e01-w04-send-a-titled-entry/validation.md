# Validation

Evidence for each check the [work item](w04.md) names, at task branch `i07/e01/w04-send-a-titled-entry`, commit `a1b351f8`.

## T1 Titled entry back-link fixture

`fixtures/destinations/a-whole-document-reference-to-a-titled-entry` bundles `guide.md` (title `Guide`, a `Steps` section) with `notes.md`, whose `[the guide](guide.md)` links back to the entry.

- **With the change.** The back-link reads `[the guide](#guide)`, the entry's title heading, and the fixture passes.
- **Against the parent commit** (`23602423`, the epic base). The same run writes `[the guide](#steps)`, the first H2, so the fixture fails there and observes the change.

Observes `AC4`.

## T2 Repository checks

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'` exits 0: lint, format, types, unit tests, harness, corpus (385 fixtures, 385 pass), smoke, layout, tables, links, vocabulary, invocation, conformance, independence and mock scenarios.

## T2 rerun on the merged head

After merging `origin/i07/e01/main` (W01, `0ad34feb`) into the task branch, `make check` at `e1b4b14c` exits 0 again: corpus 385 fixtures, 385 pass. CI `Checks` passes on that head.
