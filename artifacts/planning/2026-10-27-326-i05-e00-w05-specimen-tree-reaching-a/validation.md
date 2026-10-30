# W05 Validation

**Branch:** `i05/e00/w05-specimen-tree-reaching-a` at `d8001c90`, cut from `i05/e00/main` at `829b466d`. **Pull request:** [#332](https://github.com/m2ux/prosiform/pull/332).

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Diagram reached through a linked document

**Covers:** AC10. **Result:** ✓

`fixtures/rewriting/a-diagram-reached-through-a-linked-document` is the [specimen](../2026-10-27-326-i05-e00-mermaid-links/specimen/) copied byte for byte. `guide.md` links `lifecycle.md`, whose `mermaid` fence clicks `states/open.md` (long form with a title), `states/review.md` (short form with `_blank`), `states/closed.md` (long form with a trailing `;`), `#notes`, a callback and an `https://` address.

On the branch build, the corpus reports `rewriting/a-diagram-reached-through-a-linked-document: pass`. The run exits `0` with no diagnostics. The bundle carries `# Ticket Guide`, `# Lifecycle` with its `## Notes`, then `# Open`, `# Review` and `# Closed`. The guide's link reads `#lifecycle`, and the three state clicks read `#open`, `#review` and `#closed`. Every other byte of the fence is the source's, including `#notes`, the callback and the address.

**Fails on `main`.** With `PROSIFORM_BUILD` naming the `main` build at `6554db86` (`pf 0.11.0 (skill-markdown-v1)`), the corpus reports the fixture as failing:

```text
rewriting/a-diagram-reached-through-a-linked-document: fail
  expected.stdout: the bytes differ
    691 bytes expected, 609 produced
    first difference at byte 305, expected line 15 column 22
```

Run directly, the `main` build exits `0` and publishes the guide and the lifecycle only. Its three state clicks keep `states/open.md`, `states/review.md` and `states/closed.md`, and it bundles none of `# Open`, `# Review` or `# Closed`.

## T2 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `d8001c90`: lock, lint, format, typecheck, `test` (1176 passed), `harness` (661 passed), `corpus` (289 fixtures, 289 pass), smoke (`pf 0.11.0 (skill-markdown-v2)`), layout, tables, links, vocabulary, invocation, conformance and independence.

The independence check rejected the first description's `main` ("A main document"), so the description says "An entry document".
