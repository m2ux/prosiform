# W01–W03 Validation

**Branch:** `i05/e02/w01-class-link-form-and` at `cc192743`, cut from `i05/e02/main` at `ad2e7338`. **Pull request:** [#340](https://github.com/m2ux/prosiform/pull/340).

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The design the checks read is `e04d0886` on `engineering`, which the README's design link names.

## T1 The diagram link reader

**Covers:** none. **Result:** ✓

`src/tests/test_source.py`, run by `make test`:

- `test_a_class_link_names_its_quoted_destination`: `link Cls "a.md"`, with a tooltip, a tooltip and `_blank`, `_self`, and a trailing `;`, each yields `a.md` at offset 10.
- `test_a_diagram_link_keyword_matches_in_any_case`: `Click A HREF`, `CLICK … _BLANK`, `cLiCk A hReF`, `LINK A` and `Link A … _Self` each yield `a.md`.
- `test_a_class_link_takes_no_href`: `link Cls href "a.md"` yields nothing.
- `test_a_sequence_menu_entry_names_the_text_after_its_first_at`: the destination is the trimmed text after the first `@`, `docs/a@b.md` whole, a trailing `;` left out, an actor name holding a space accepted; each offset spans the destination.
- `test_a_sequence_menu_line_names_each_string_value_in_written_order` and `…_keyword_matches_in_any_case`: two values in written order, each offset spanning its value; `LINKS … ;` read.
- `test_a_sequence_menu_line_holding_no_json_object_names_nothing`: an array, a string, an unclosed object, trailing text and bare text each yield nothing.
- `test_a_sequence_menu_value_holding_an_escape_names_nothing`: `"docs\/spec.md"` yields nothing and the next value is still read.
- `test_a_sequence_menu_value_that_is_no_string_names_nothing`: a number and a nested object yield nothing.
- `test_each_sequence_menu_destination_is_one_use_on_its_line`: a `link` and a two-value `links` line are three uses on lines 3, 4 and 4, and three occurrences.

## T2 A class diagram link line is bundled and rewritten

**Covers:** AC1. **Result:** ✓

`fixtures/rewriting/a-class-diagram-link-destination` passes in `make corpus`. `link Ticket "types/ticket.md" "The ticket type" _blank` becomes `link Ticket "#ticket" "The ticket type" _blank`, `link Review "types/review.md"` becomes `link Review "#review"`, the `# Ticket` and `# Review` groups follow, and every other fence byte is as written.

## T3 A mixed-case click is bundled and rewritten

**Covers:** AC2. **Result:** ✓

`fixtures/rewriting/a-diagram-link-keyword-in-any-case` passes in `make corpus`. In a `stateDiagram-v2`, whose Mermaid lexer reads these keywords in any case, `Click Open HREF "states/open.md"` becomes `Click Open HREF "#open"` and `CLICK Closed "states/closed.md" "The closed state"` becomes `CLICK Closed "#closed" "The closed state"`; both groups follow.

## T4 A sequence link entry is bundled and rewritten

**Covers:** AC3. **Result:** ✓

`fixtures/rewriting/a-sequence-diagram-link-destination` passes in `make corpus`. `link Client: Client guide @ docs/client.md` becomes `link Client: Client guide @ #client`, the `# Client` group follows, and every other fence byte is as written.

## T5 A two-destination links line is bundled and rewritten

**Covers:** AC4. **Result:** ✓

`fixtures/rewriting/a-sequence-diagram-links-line-destinations` passes in `make corpus`. `links Server: {"Server guide": "docs/server.md", "Operations": "docs/operations.md"}` becomes `links Server: {"Server guide": "#server", "Operations": "#operations"}`, and the `# Server` and `# Operations` groups follow.

## T6 Each links destination counts against -L

**Covers:** AC5. **Result:** ✓

`fixtures/limits/a-link-budget-crossed-by-a-links-line` passes in `make corpus`: one `links` line naming three documents, run with `-L 2`, exits `1` with `E_RESOURCE_LIMIT`, its message naming 3 occurrences against a budget of 2. The same source run with `-L 3` exits `0`.

## T7 pf -v reports skill-markdown-v3

**Covers:** AC6. **Result:** ✓

`fixtures/cli/informational-version-response` declares `stdout_contains = ["pf ", "(skill-markdown-v3)"]` and passes in `make corpus`.

## T8 The rule names every form followed

**Covers:** AC7. **Result:** ✓

Inspection:

- **`invocation.md`** at `cc192743`, the Diagram links rule: names `click` with and without `href`, a class diagram's `link <class> "<destination>"`, a sequence diagram's `link <actor>: <label> @ <destination>` and `links <actor>: {…}`, and keywords matching in any letter case; carries the C4 `$link`, Kanban and escaped-value boundary.
- **`docs/glossary.md`** at `cc192743`, **reference**: names the `click` line, the class `link` line, the sequence `link` and `links` menus, and keywords in any letter case.
- **The design** at `e04d0886`, the Examples rule: names the same forms, any-case keywords and boundary; the profile rule names `skill-markdown-v3`.

A search of the branch for `skill-markdown-v2` finds no statement; the version-history entries hold none.

## T9 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `cc192743`: lock, lint, format and typecheck; `test` (1202 passed); `harness` (666 passed); `corpus` (294 fixtures, 294 pass, 0 fail, 0 awaited); smoke; layout; tables; links; vocabulary; invocation; conformance; independence.

## Findings

- **Mermaid reads `#` as a comment in a sequence diagram.** The sequence lexer ends a `link` or `links` line's text at `#`, so a renderer drawing the bundle's diagram drops a rewritten entry's `#<slug>` destination and fails to parse a rewritten `links` object, which Mermaid logs and skips. The bundle's text carries the anchor. Raised as an arising issue.
- **Flowchart and class keywords are lowercase in Mermaid.** Mermaid 11.16.0's flowchart and class lexers match `click`, `href` and `link` in lowercase alone; its state, Gantt and sequence lexers match any case. prosiform matches any case in every diagram, so a mixed-case line in a flowchart or class diagram, which Mermaid fails to parse, is still bundled.
