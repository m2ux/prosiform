# W04 Validation

**Branch:** `i05/e02/w04-sequence-diagram-anchors-mermaid` at `84a11524`, cut from `i05/e02/main` at `7195b0a0`. **Pull request:** [#343](https://github.com/m2ux/prosiform/pull/343), merged into `i05/e02/main` as `c61e9150` once its Checks run passed.

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. The design the checks read is `dcb342d6` on `engineering`, which the README's design link names.

## Decision

#341's open question is settled with its recommendation: a rewritten sequence `link` or `links` destination is spelled `#35;<slug>`. Mermaid 11.16.0's `encodeEntities` turns every `#<word>;` in a diagram's text into a placeholder before lexing, and `decodeEntities` turns it back into `&#35;` in the rendered SVG, so the sequence lexer never sees a `#` and the menu entry's `xlink:href` reads `#<slug>`. The render below confirms it. The spelling belongs to the reader of the forms, so `Click` in `source.py` carries it, and the rewrite and candidate validation read it from there.

## T1 Each form spells its anchor

**Covers:** none. **Result:** ✓

`src/tests/test_source.py`, run by `make test`: `test_each_diagram_link_form_spells_its_anchor` reads `#` from a `click` and a class `link` line, and `#35;` from a sequence `link` entry and from each value of a `links` line.

## T2 Candidate validation reads the spelling back

**Covers:** none. **Result:** ✓

`src/tests/test_candidate.py`, run by `make test`:

- `test_a_candidate_carrying_rewritten_sequence_menu_destinations_validates`: a `link` entry and a `links` value naming `note.md` are bundled as `@ #35;note` and `"#35;note"`, and the candidate validates.
- `test_a_sequence_menu_entry_spelling_its_anchor_bare_fails` and `…_value_spelling_its_anchor_bare_fails`: the same candidate with `#note` on either line fails `REFERENCE_PRESERVATION`.
- `test_a_click_spelling_its_anchor_as_an_entity_fails`: a `click` destination spelled `#35;note` fails `REFERENCE_PRESERVATION`.

## T3 The sequence fixtures carry the entity spelling

**Covers:** none. **Result:** ✓

`make corpus` passes both updated fixtures:

- `fixtures/rewriting/a-sequence-diagram-link-destination`: `link Client: Client guide @ docs/client.md` becomes `link Client: Client guide @ #35;client`.
- `fixtures/rewriting/a-sequence-diagram-links-line-destinations`: the `links` values become `"#35;server"` and `"#35;operations"`.

## T4 The rendered menus open their groups' headings

**Covers:** AC8. **Result:** ✓

The fixture is `fixtures/rewriting/a-sequence-diagram-link-and-links-line-anchors`: participant `Client` carries `link Client: Client guide @ docs/client.md`, and participant `Server` carries `links Server: {"Server guide": "docs/server.md", "Operations": "docs/operations.md"}`. `make corpus` passes it; its bundle carries `@ #35;client`, `"#35;server"` and `"#35;operations"`, followed by the `# Client`, `# Server` and `# Operations` groups.

The render is documented here rather than run by the project's checks: it needs mermaid-cli and a headless Chromium, which the build's dependencies do not hold. The script is [render-menus.py](render-menus.py) in this record. It renders the bundle's `mermaid` fences with `mmdc`, reads each participant's popup menu from the SVG, and exits `0` only when every entry is a link whose href is `#<slug>` for a heading the bundle carries.

Run from the fixture's `source/` directory with mermaid-cli 11.16.0 (Mermaid 11.16.0) installed by `npx -p @mermaid-js/mermaid-cli@11.16.0`, and Chromium 150.0.7871.24 from the puppeteer cache:

```bash
uv run --project <worktree>/src --frozen pf -o <work>/bundle.md exchange.md
cmp <work>/bundle.md ../expected/stdout.md
python3 render-menus.py <npx-cache>/node_modules/.bin/mmdc <work>/bundle.md <work>/out-bundle
```

`cmp` reports no difference, and the render prints, exiting `0`:

```text
rendered-1.svg Client:
  'Client guide' -> '#client' heading
rendered-1.svg Server:
  'Server guide' -> '#server' heading
  'Operations' -> '#operations' heading
```

The SVG's popup groups hold `<a xlink:href="#client">` under `actor0_popup` and `<a xlink:href="#server">` and `<a xlink:href="#operations">` under `actor1_popup`.

**Control.** The same bundle with each `#35;` replaced by `#`, the spelling `i05/e02/main` writes at `7195b0a0`, renders the `Client` menu entry as a link with no href and no `Server` menu at all:

```text
rendered-1.svg Client:
  'Client guide' -> '' NO HEADING
```

## T5 The rules state the spelling

**Covers:** none. **Result:** ✓

Inspection:

- **`invocation.md`** at `84a11524`, the Diagram links rule: a sequence diagram's `link` and `links` destinations spell the anchor `#35;<slug>`, the entity Mermaid renders as `#`.
- **The design** at `dcb342d6`, the Examples rule: the same statement.
- **`docs/glossary.md`**: unaffected. Its **destination** entry names the slug a renderer generates, which the spelling leaves as it is, and no entry states how a diagram line writes it.

A search of the branch for a sequence destination written `@ #<slug>` or `": "#<slug>"` finds only the bare-spelling candidate tests of T2.

## T6 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0` at `84a11524`: lock, lint, format and typecheck; `test` (1210 passed); `harness` (667 passed); `corpus` (295 fixtures, 295 pass, 0 fail, 0 awaited); smoke; layout; tables; links; vocabulary; invocation; conformance; independence.

## Findings

- **The W01–W03 records state the bare spelling as of their delivery.** The epic record's `w02.md` and the W01–W03 validation describe `#<slug>` sequence destinations; they record that delivery and are left as written.
