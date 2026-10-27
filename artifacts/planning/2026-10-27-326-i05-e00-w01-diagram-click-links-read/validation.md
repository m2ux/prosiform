# W01 Validation

**Branch:** `i05/e00/w01-diagram-click-links-read` at `72f1015a`, cut from `i05/e00/main` at `6554db86`.

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Reader unit tests

**Covers:** AC1. **Result:** ✓

`src/tests/test_source.py` holds the reader's grammar:

| Test | Observes |
| --- | --- |
| `test_a_diagram_href_click_is_a_use_on_the_line_it_is_written` | `click Open href "states/open.md"` yields one use at line 6, the line it is written on. |
| `test_a_diagram_short_click_is_a_use_on_the_line_it_is_written` | `click Closed "states/closed.md"` yields one use at line 7. |
| `test_each_diagram_click_is_one_link_use_opening_with_nothing` | Each diagram use is a link (`resource=False`) opening with no text, so it carries no deferral mark. |
| `test_a_click_s_trailing_tooltip_and_target_leave_its_destination` | Six spellings with a tooltip, a target, both, and a trailing `;` each yield the one destination. |
| `test_a_line_naming_no_click_destination_is_no_use` | A callback with and without a tooltip, a `call` form, a click with trailing text, and a node label quoting a click yield nothing. |
| `test_a_click_in_a_fence_holding_no_diagram_is_no_use` | Fences with no info string, `text`, `mermaid-like` and `graph` yield nothing. |
| `test_a_diagram_fence_reads_its_info_string_s_first_word` | `~~~ mermaid title` is a diagram fence. |
| `test_a_click_offset_spans_its_destination_in_the_fence_line` | In a fence a list item carries, the offset spans the destination in the line the fence holds, and the line is the document's. |
| `test_diagram_and_inline_uses_arrive_in_source_order` | Inline and diagram uses arrive interleaved in source order. |
| `test_each_diagram_click_is_counted_once_per_occurrence` | Two clicks and one inline link count three occurrences. |
| `test_a_diagram_click_outside_the_given_regions_is_not_counted` | A click outside the selected section is not counted. |

`make test`: 1165 passed.

## T2 Non-diagram and callback clicks fixture

**Covers:** AC2. **Result:** ✓

`fixtures/reference/a-click-naming-no-diagram-destination-is-text` bundles a document carrying a `text` fence of `href` and short click lines, and a `mermaid` fence whose clicks name a callback and a `call` form. Each names a document the source tree lacks, so a reader treating any as a use would fail with `E_TARGET_NOT_FOUND`. The run exits `0` with no diagnostics and the bundle is the document byte for byte.

## T3 Diagram clicks cross the link budget fixture

**Covers:** AC3. **Result:** ✓

`fixtures/limits/a-link-budget-crossed-by-diagram-clicks` runs `-L 2` over a document whose only references are three `mermaid` click links, each target present. The run exits `1` with `E_RESOURCE_LIMIT` and publishes nothing.

Against the base build, with `source.py` restored to `i05/e00/main`, this fixture fails (the run succeeds) and T2 passes, so T3 observes the new count.

## T4 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0`: lock, lint, format, typecheck, `test` (1165 passed), `harness` (656 passed), `corpus` (284 fixtures, 284 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence.

`click` joins `docs/corpus-vocabulary.md` under Markup, encodings and formats, because the independence check reports a fixture word the contract does not state.
