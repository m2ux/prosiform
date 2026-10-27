# W09–W10 Validation

**Branch:** `i05/e02/w09-gantt-links-clicked-in` at `edcbe3b2`, cut from `i05/e02/main` at `b3e1df15`. **Pull request:** [#348](https://github.com/m2ux/prosiform/pull/348), merged into `i05/e02/main` as `d5196941` once its Checks run passed.

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The design the checks read is `21f4687d` on `engineering`, which the README's design link names. The render ran with `MERMAID_CLI=<npx-cache>/node_modules/.bin/mmdc`: mermaid-cli 11.16.0 (Mermaid 11.16.0), puppeteer 25.3.0 and Chromium 150.0.7871.24 from the puppeteer cache, under Node 20.19.4.

## T1 Gantt links clicked in a running page

**Covers:** AC18. **Result:** ✓

`make render` exits `0`: 15 fixtures, 15 pass. `rewriting/a-gantt-diagram-click-destination` is listed under `CLICKED`, and `checks/click.mjs` renders its bundle's Gantt fence in a headless page, binds the handlers the render returns, and clicks each `.task.clickable` bar:

| Task | Line in the bundle | Opened |
| --- | --- | --- |
| `freeze` | `click freeze href "#freeze"` | `#freeze` |
| `publish` | `CLICK publish HREF "#publish"` | `#publish` |

Each click opened one URL, through `window.open(…, "_self")`, and each names a heading the bundle carries, `# Freeze` and `# Publish`. The 14 anchor fixtures of W08 pass unchanged.

- **mermaid-cli drives no click.** Its `renderMermaid` sets the SVG into the page and never calls `bindFunctions`, so the page the driver loads is its own: a string page with Mermaid's `mermaid.min.js` from mermaid-cli's package added inline, which needs no network.
- **The driver fails a wrong destination.** The same driver over an unrewritten diagram reports `tasks/a.md` for its task, which `render.py` refuses as opening no heading the bundle carries.
- **Either command line runs it.** The driver ran under the direct `mmdc` path and under `npx -p @mermaid-js/mermaid-cli@11.16.0`, as `node checks/click.mjs mmdc`.

## T2 The unfollowed links and their refusal

**Covers:** none. **Result:** ✓

`make test` (1264 passed):

- `src/tests/test_source.py`: a Kanban ticket renders the link its front matter base builds, `people/user.md` at the ticket's line; an `init` directive's base replaces the front matter's; a ticket with no base, a node with no ticket, and a ticket outside a Kanban diagram render nothing; an HTML anchor renders its `href` single-quoted, double-quoted and bare in any case; a comment line renders nothing.
- `src/tests/test_profile.py`: a ticket link to `people/user.md`, a label anchor to `people/user.md#setup` and a sequence note's anchor to `../people/user.MD` are each refused under `E_UNSUPPORTED_CONSTRUCT` at their line; an `https:` ticket base, an `https:` and a `//` anchor, a `.png` anchor and a fragment-only anchor are refused nowhere.

## T3 A Kanban ticket naming a local document

**Covers:** AC19. **Result:** ✓

`fixtures/reference/a-kanban-ticket-naming-a-local-document` passes in `make corpus`: a `kanban` whose front matter sets `ticketBaseUrl: 'people/#TICKET#.md'` and a node `@{ ticket: user }` exits `1` with `E_UNSUPPORTED_CONSTRUCT` at `guide.md:11`, the ticket's line, and publishes nothing.

## T4 An HTML label anchor naming a local document

**Covers:** AC20. **Result:** ✓

`fixtures/reference/an-html-anchor-in-a-node-label-naming-a-local-document` passes in `make corpus`: a flowchart node `A["<a href='people/user.md'>User</a>"]` exits `1` with `E_UNSUPPORTED_CONSTRUCT` at `guide.md:5`, and publishes nothing.

## T5 Remote addresses carried as written

**Covers:** AC19, AC20. **Result:** ✓

`fixtures/reference/diagram-links-naming-remote-addresses-are-text` passes in `make corpus`: a `kanban` whose `%%{init}%%` directive sets `ticketBaseUrl: "https://tracker.example.com/browse/#TICKET#"` with a ticket, and a label anchor to `https://example.com/people/user.md`, exit `0` with each fence as written. `fixtures/reference/diagram-links-outside-the-forms-read` keeps the C4 `$link` and the pie chart and passes as AC17 states.

## T6 The rules state the proof and the refusals

**Covers:** none. **Result:** ✓

Inspection:

- **`invocation.md`** at `edcbe3b2`, the Diagram links rule: a Gantt task's `click` opens its anchor when clicked in the running page; a Kanban ticket's link and a label anchor naming local Markdown fail with `E_UNSUPPORTED_CONSTRUCT` naming the line, and one naming a remote address is carried as written.
- **The design** at `21f4687d`: the Unsupported local-document syntax rule names both refusals; the Examples rule states the Gantt click and the refusals.
- **`docs/glossary.md`**: unaffected. Its **reference** entry names the link lines the reader follows, and neither refused form is one.
- **`checks.md`, `checks/README.md`, the `Makefile`**: state the click check.

A search of the branch finds no statement that a Kanban ticket's link or a label anchor is carried as written whatever it names.

## T7 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `edcbe3b2`: lock, lint, format and typecheck; `test` (1264 passed); `harness` (682 passed); `corpus` (310 fixtures, 310 pass, 0 fail, 0 awaited); smoke; layout; tables (17 commands); links (107 documents); vocabulary; invocation; conformance; independence. `make render` exits `0` (15 fixtures).

## Findings

- **The scheme and authority test moved to `source.py`.** The profile could not import it from `closure.py`, which imports the profile, so the one test both need sits below both.
- **An anchor on any diagram line is read.** The read takes every diagram line but a comment rather than locating node labels per diagram type, so an anchor in other diagram text, such as a sequence note, is refused with them.
