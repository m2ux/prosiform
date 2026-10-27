# W05–W08 Validation

**Branch:** `i05/e02/w05-link-forms-as-mermaid` at `69b44aec`, cut from `i05/e02/main` at `c61e9150`. **Pull request:** [#345](https://github.com/m2ux/prosiform/pull/345), merged into `i05/e02/main` as `b3e1df15` once its Checks run passed.

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The design the checks read is `6c053d71` on `engineering`, which the README's design link names. The render ran with `MERMAID_CLI=<npx-cache>/node_modules/.bin/mmdc`: mermaid-cli 11.16.0 (Mermaid 11.16.0) and Chromium 150.0.7871.24 from the puppeteer cache.

## T1 The diagram link reader

**Covers:** none. **Result:** ✓

`src/tests/test_source.py`, run by `make test`:

- `test_a_diagram_type_is_read_as_mermaid_detects_it`: `classDiagram`, `classDiagram-v2`, an indented `sequenceDiagram`, one under front matter, one under a `%%{init}%%` directive, one under `%%` comments and one under blank lines are read; `flowchart`, `stateDiagram-v2` and `title sequenceDiagram` are not.
- `test_a_link_form_is_read_in_its_own_diagram_alone`: a sequence `link` line in a state diagram, flowchart and class diagram, a `links` line in a class diagram, and a class `link` line in a sequence diagram, flowchart and state diagram each name nothing.
- `test_a_sequence_menu_entry_ends_where_mermaid_ends_its_statement`: `@ a.md;b.md`, `@ a.md ; `, `@ a.md # a comment`, `@ a.md#intro` each name `a.md` and leave the rest as written; `@ a.md#35;intro` names `a.md#intro`; `@ #35;intro;x.md` names `#intro`.
- `test_a_sequence_menu_entry_whose_at_follows_its_end_names_nothing` and `test_a_sequence_menu_line_ends_where_mermaid_ends_its_statement`: an `@` after the end names nothing; a `links` value `a.md#35;intro` names `a.md#intro`; a value holding `;` or a bare `#` cuts the object, which names nothing.
- `test_a_repeated_menu_key_names_its_last_value_alone`, `…_whose_last_value_holds_an_escape_names_nothing`, `test_a_value_no_string_a_later_key_replaces_breaks_nothing`: the last value of a key is read alone, with its own offset.
- `test_a_sequence_menu_value_that_is_no_string_breaks_its_line`: a number, a nested object, `null` and an array overwriting a string each break the line, which names nothing.
- `test_a_menu_constant_json_parse_refuses_names_nothing`: `NaN` names nothing.
- `test_a_diagram_link_keyword_matches_in_any_case` now names each case's diagram type.

## T2 Candidate validation reads resolved destinations

**Covers:** none. **Result:** ✓

`src/tests/test_candidate.py`: a candidate carrying `@ #35;note` and `"#35;note"` validates; the same candidate spelling either bare reads a line naming no destination and fails `NO_NEW_LINKS`; one naming `#35;guide` fails `REFERENCE_PRESERVATION`; a `click` spelled `#35;note` still fails `REFERENCE_PRESERVATION`.

## T3 A sequence destination naming a section

**Covers:** AC9. **Result:** ✓

`fixtures/rewriting/a-sequence-diagram-destination-naming-a-section` passes in `make corpus`: `link Client: Setup @ docs/client.md#35;setup` becomes `@ #35;setup` and `links Server: {"Limits": "docs/server.md#35;limits"}` becomes `"#35;limits"`; each document's group carries the section, `### Setup` and `### Limits`.

## T4 A link line in another diagram is text

**Covers:** AC10. **Result:** ✓

`fixtures/reference/a-link-line-in-another-diagram-is-text` passes in `make corpus`: a `stateDiagram-v2` carrying `link --> done : retry @ ops.md` and the class diagram line `link Ops "ops.md"` bundles no `ops.md` group, and the fence is as written.

## T5 A sequence destination ends at a semicolon

**Covers:** AC11. **Result:** ✓

`fixtures/rewriting/a-sequence-diagram-destination-ending-at-a-semicolon` passes in `make corpus`: `link Client: Client guide @ docs/client.md;docs/server.md` becomes `@ #35;client;docs/server.md`; the `# Client` group follows and no `# Server` group.

## T6 A repeated links key

**Covers:** AC12. **Result:** ✓

`fixtures/rewriting/a-sequence-diagram-links-line-repeating-a-key` passes in `make corpus`: `{"Guide": "docs/draft.md", "Guide": "docs/server.md"}` becomes `{"Guide": "docs/draft.md", "Guide": "#35;server"}`, with the `# Server` group alone.

## T7 A links value that is no string

**Covers:** AC13. **Result:** ✓

`fixtures/reference/a-links-value-that-is-no-string` passes in `make corpus`: `links Server: {"Guide": "docs/server.md", "Port": 8080}` exits `1` with `E_UNSUPPORTED_CONSTRUCT` at `exchange.md:6`, the line, and publishes nothing. The refusal is `profile.refusals`, so it reaches the selected content of every source as the profile's other refusals do.

## T8 One home for the anchor spellings

**Covers:** AC14. **Result:** ✓

Inspection at `69b44aec`: `ANCHOR` and `ENTITY_ANCHOR` are assigned in `src/prosiform/source.py` alone; `bundle.py` and `candidate.py` import `ANCHOR` from it and assign neither. The candidate's `Use` carries no anchor.

## T9 One decode per menu, one read per fence

**Covers:** AC15. **Result:** ✓

- `src/tests/test_source.py::test_a_menu_line_is_json_decoded_once_per_read`: a `links` line with a repeated key reads with one call of `decoded`.
- `src/tests/test_source.py::test_a_fence_s_diagram_is_read_once_however_often_it_is_asked`: three `uses` passes and an `occurrences` count over one fence call `read_diagram` once.
- `src/tests/test_cli.py::test_each_diagram_fence_is_read_once_per_parse_of_a_run`: a whole run over a document carrying a sequence and a flowchart fence reads every fence token once, the two source fences among them. The bundle's text is parsed by candidate validation and by the resource warning apart, and each parse's fence is read once.

## T10 Every diagram link form rendered

**Covers:** AC16. **Result:** ✓ for every form but Gantt, which is held.

`make render` exits `0`, 14 fixtures, each rendered anchor opening a heading its bundle carries and the anchors matching the links rewritten:

| Form | Fixture | Anchors |
| --- | --- | --- |
| Flowchart `click`: `href`, none, tooltip, tooltip and target | `rewriting/a-flowchart-click-in-each-form` | `#plan`, `#build`, `#test`, `#ship` |
| Flowchart `click`, long and short | `rewriting/a-diagram-click-destination`, `rewriting/a-diagram-short-click-destination` | `#open`; `#open`, `#closing` |
| Swimlanes `click`: `href`, none, tooltip, tooltip and target | `rewriting/a-swimlanes-diagram-click-in-each-form` | `#draft`, `#review`, `#approve`, `#merge` |
| State `click`: `href`, none with tooltip | `rewriting/a-state-diagram-click-in-each-form` | `#pending`, `#done` |
| State `Click … HREF`, `CLICK` | `rewriting/a-diagram-link-keyword-in-any-case` | `#open`, `#closed` |
| Class `click`: `href`, tooltip, tooltip and target | `rewriting/a-class-diagram-click-in-each-form` | `#order`, `#line`, `#price` |
| Class `link`, with tooltip and target | `rewriting/a-class-diagram-link-destination` | `#ticket`, `#review` |
| Sequence `link` | `rewriting/a-sequence-diagram-link-destination` | `#client` |
| Sequence `links` | `rewriting/a-sequence-diagram-links-line-destinations` | `#server`, `#operations` |
| Sequence `link` and `links` together | `rewriting/a-sequence-diagram-link-and-links-line-anchors` | `#client`, `#server`, `#operations` |
| Sequence `LINK`, `Links` | `rewriting/a-sequence-diagram-menu-keywords-in-any-case` | `#client`, `#server` |
| Sequence section destination | `rewriting/a-sequence-diagram-destination-naming-a-section` | `#setup`, `#limits` |
| Sequence repeated key | `rewriting/a-sequence-diagram-links-line-repeating-a-key` | `#server` |
| Gantt `click … href`, `CLICK … HREF` | `rewriting/a-gantt-diagram-click-destination` | held: no anchor |

**Variants a grammar refuses.** A probe of each `click` variant per type under Mermaid 11.16.0 fails the diagram's parse for: Gantt without `href`, with a tooltip or a target; state with `href` and a tooltip, or with a target; state without `href` and without a tooltip; class without `href`. Each is no link Mermaid renders, so no fixture proves it. Flowchart and class keywords match in lowercase alone in Mermaid, so the any-case forms are proven in state and sequence diagrams.

**Gantt is held.** Mermaid draws a Gantt task's link as no anchor: `setLink` binds a click handler calling `window.open(link, "_self")` when the page runs, and the task's SVG carries the class `clickable` alone. It draws an `<a xlink:href>` only under `securityLevel: "sandbox"`, which mermaid-cli 11.16.0 fails to render (`ReferenceError: warn is not defined`). The fixture proves the bundle; no static render proves the link.

## T11 The forms outside the reader are carried as written

**Covers:** AC17. **Result:** ✓

`fixtures/reference/diagram-links-outside-the-forms-read` passes in `make corpus`: a `C4Context` with `$link="people/user.md"`, a `kanban` whose ticket base URL builds `people/user.md`, a flowchart label holding `<a href='people/user.md'>`, and a `pie` naming `people/user.md` are each carried as written, and no `# User` group is bundled.

## T12 The rules state the forms

**Covers:** none. **Result:** ✓

Inspection:

- **`invocation.md`** at `69b44aec`, the Diagram links rule: each form in its own diagram, the type as Mermaid detects it, the sequence statement's end, `#35;` naming `#`, the repeated key and the `E_UNSUPPORTED_CONSTRUCT` fault; the HTML label anchor among the forms carried as written.
- **The design** at `6c053d71`, the Examples rule: the same statements.
- **`docs/glossary.md`**: unaffected. Its **reference** entry names a class diagram's `link` line and a sequence diagram's menus already, and states neither end nor decode rule.

A search of the branch finds no statement that a `link` line is read in every diagram or that a sequence destination runs to the line's end.

## T13 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `69b44aec`: lock, lint, format and typecheck; `test` (1247 passed); `harness` (679 passed); `corpus` (307 fixtures, 307 pass, 0 fail, 0 awaited); smoke; layout; tables (17 commands); links (107 documents); vocabulary; invocation; conformance; independence. `make render` exits `0` (14 fixtures).

## Findings

- **A Kanban ticket and an HTML label anchor render followable links.** Under Mermaid 11.16.0 the boundary fixture's bundle draws `<a class="kanban-ticket-link" xlink:href="people/user.md">` and `<a href="people/user.md">`: each opens a source path the bundle does not carry. The design names both as carried as written. Raised as an arising issue.
- **A destination cut at a semicolon leaves a diagram Mermaid cannot parse.** The text after the `;` is a statement of its own, so the source diagram and the bundle's alike fail to render; the bundle reads as Mermaid lexes it.
- **The bundle is parsed twice.** Candidate validation and the resource warning each parse the bundle's text, so each reads a bundle fence once per its own parse.
