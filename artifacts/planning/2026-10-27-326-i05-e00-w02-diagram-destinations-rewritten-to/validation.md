# W02 Validation

**Branch:** `i05/e00/w02-diagram-destinations-rewritten` at `d7355245`, cut from `i05/e00/main` at `b0f5a08e`. **Pull request:** [#329](https://github.com/m2ux/prosiform/pull/329).

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Long-form click bundled and rewritten

**Covers:** AC4. **Result:** ✓

`fixtures/rewriting/a-diagram-click-destination` bundles the epic's Problem source: `lifecycle.md` (`# Lifecycle` and a `mermaid` fence carrying `click Open href "states/open.md"`) with `states/open.md` holding `# Open`. The run exits `0` with no diagnostics. The bundle carries the `# Open` group, the click line reads `click Open href "#open"`, and every other line of the fence is the source's.

Against the base `bundle.py` (restored from `b0f5a08e`), the fixture fails: the bundle carries the `# Open` group and the click still reads `href "states/open.md"`.

## T2 Short-form click bundled and rewritten

**Covers:** AC5. **Result:** ✓

`fixtures/rewriting/a-diagram-short-click-destination` writes `click Open "states/open.md" "The open state" _blank` and `click Closed "states/closed.md#closing";`. The run exits `0` with no diagnostics, bundles `# Open` and `# Closed` with its `### Closing` section, and publishes `click Open "#open" "The open state" _blank` and `click Closed "#closing";`. The title, target and `;` are carried as written.

Against the base `bundle.py`, the fixture fails: both destinations keep their source paths.

## T3 Outside-root and non-Markdown clicks carried as written

**Covers:** AC6. **Result:** ✓

- `fixtures/reference/a-diagram-click-outside-the-root-is-text` writes `click Open href "../states/open.md"` and `click Closed "../states/closed.md"`, both naming documents beside the fixture and above the root. `../states/open.md` links to a document that does not exist, so opening it would fail the run. The run exits `0` with no diagnostics, and the bundle is the source byte for byte.
- `fixtures/resource/a-diagram-click-naming-a-resource` writes `click Open href "states/open.svg"` and `click Closed "states/closed.txt"`, both present under the root. The run exits `0`, the bundle is the source byte for byte, and the one diagnostic is `W_RESOURCE_PORTABILITY`, as for an inline link to such a file.

The base `bundle.py` rewrites no fence, so both pass against it. They discriminate against a build that rewrites every click: with `rewrite` mutated to give an unrewritable click `#mutant`, both fail and every other fixture passes.

## T4 Offset mapping unit tests

**Covers:** AC4, AC5. **Result:** ✓

`src/tests/test_bundle.py` calls `rewrite` directly:

| Test | Observes |
| --- | --- |
| `test_a_diagram_click_destination_is_rewritten_between_its_quotes[document-level]` | `click Open href "open.md"` becomes `href "#open"`. |
| `…[indented-fence]` | A fence indented three spaces, its click carrying a target, is rewritten in place. |
| `…[nested-containers]` | A fence inside a block quote inside a list item: the `  > ` markers and the indent are kept and only the destination changes. |
| `…[crlf]` | A CRLF document keeps its CRLF terminators and the trailing `;`. |
| `test_a_diagram_click_rewrite_keeps_one_entry_per_source_line` | The rewrite returns one entry per source line, and a click naming a non-Markdown file beside a rewritten one keeps its path. |
| `test_a_diagram_click_outside_the_selection_keeps_its_source_path` | Of two diagrams, only the one in the selected section is rewritten. |

Against the base `bundle.py`, all six fail.

## T5 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0`: lock, lint, format, typecheck, `test` (1171 passed), `harness` (660 passed), `corpus` (288 fixtures, 288 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence.

The two `rewriting/` descriptions avoid `href`, `tooltip` and `semicolon`, because the independence check rejects words the contract's vocabulary does not hold.
