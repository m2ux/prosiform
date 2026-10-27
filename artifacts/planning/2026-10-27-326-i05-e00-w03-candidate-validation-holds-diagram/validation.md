# W03 and W04 Validation

**Branch:** `i05/e00/w03-candidate-validation-holds-diagram` at `50bd29fd`, cut from `i05/e00/main` at `8799bc63`. **Pull request:** [#330](https://github.com/m2ux/prosiform/pull/330). **Design commit:** [`e1b82283`](https://github.com/m2ux/prosiform/commit/e1b82283825281279069188f575806dd11d4be3d) on `engineering`.

Every check ran in the task worktree with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Diagram uses held by reference validation

**Covers:** AC7. **Result:** ✓

`src/tests/test_candidate.py` compiles `guide.md`, whose `mermaid` fence writes `click Open href "note.md"` and a `%%` comment line, with `note.md` holding `# Note`, through the command's own assembly, then alters the candidate:

| Test | Alteration | Invariant |
| --- | --- | --- |
| `test_a_candidate_carrying_a_rewritten_diagram_destination_validates` | none; the bundle carries `click Open href "#note"` | validates |
| `test_a_diagram_destination_pointing_elsewhere_fails` | `href "#note"` becomes `href "#guide"` | `REFERENCE_PRESERVATION` |
| `test_a_diagram_destination_left_as_its_source_wrote_it_fails` | `href "#note"` becomes `href "note.md"` | `REFERENCE_PRESERVATION` |
| `test_a_dropped_diagram_click_fails` | the click line becomes a `%%` comment | `NO_NEW_LINKS` |
| `test_an_added_diagram_click_fails` | the comment becomes `click Note href "#note"` | `NO_NEW_LINKS` |

Against the base `candidate.py` (restored from `8799bc63`), all four rejection tests fail: the two destination tests with `DID NOT RAISE Invalid`, since preservation sets the destination aside and nothing else reads it, and the two count tests with `preservation` in place of `no new links`, since the base reads the changed click line only as an altered byte.

## T2 Informational version reports skill-markdown-v2

**Covers:** AC8. **Result:** ✓

`fixtures/cli/informational-version-response` runs `pf -v` and declares `stdout_contains = ["pf ", "(skill-markdown-v2)"]`; its clause case reads `Markdown and source-heading profile, skill-markdown-v2`. The corpus reports it `pass`, and the smoke check's installed wheel answers `pf 0.11.0 (skill-markdown-v2)`.

Against the base `__init__.py`, the fixture fails: `'(skill-markdown-v2)' is absent`, `produced b'pf 0.11.0 (skill-markdown-v1)\n'` (287 of 288 pass).

## T3 Diagram rule stated in invocation and design

**Covers:** AC9. **Result:** ✓

By inspection. The bundling rules in `invocation.md` carry:

> **Diagram links:** in a fenced code block whose info string opens with `mermaid`, each `click <node> href "<destination>"` and `click <node> "<destination>"` line is a use on the line it is written, counted against `-L`, and is followed like any link. A destination naming a Markdown document or section under the root is bundled, and the characters between its quotes are rewritten to the anchor of the group it names; every other byte of the fence is carried as written. A click naming a callback, a destination outside the root and a destination naming no Markdown document are carried as written and open nothing. A diagram link carries no operator, since a click gives it no link text. Apparent links in any other code span or block are example text and are never followed.

The design's Examples rule, at [`e1b82283`](https://github.com/m2ux/prosiform/blob/e1b82283825281279069188f575806dd11d4be3d/artifacts/planning/2026-10-17-prosiform-v1/design.md#markdown-and-source-heading-profile), reads:

> **Examples:** Do not follow apparent links inside code spans, fenced code blocks, or other literal example content, except a Mermaid diagram's click destinations. In a fenced code block whose info string opens with `mermaid`, each `click <node> href "<destination>"` line and each `click <node> "<destination>"` line is a use on the line it is written, counted against the link budget, and is followed and rewritten as a link is: a destination naming a Markdown document or section under the root is bundled, and the characters between its quotes become the anchor of the group it names, every other byte of the fence carried as written. A click naming a callback, a destination outside the root and a destination naming no Markdown document are carried as written and open nothing. A diagram link carries no operator, because a click gives it no link text to open with one.

The same commit names the profile `skill-markdown-v2` in the design's profile statement. The README's design link names that commit, so `make vocabulary` and `make conformance` read the design stating the rule.

A grep of `src/`, `docs/`, `invocation.md`, `checks.md`, the READMEs and the glossary finds no surviving statement that a code block carries no use without the `mermaid` exception: `source.py` states it beside the exception (W01), `profile.py` now does, and `profile.py`'s recognition rule (a code block carries no unsupported-construct spelling) concerns refused constructs, not uses.

## T4 Repository checks

**Covers:** none. **Result:** ✓

`make check` exits `0`: lock, lint, format, typecheck, `test` (1176 passed), `harness` (660 passed), `corpus` (288 fixtures, 288 pass), smoke, layout, tables, links, vocabulary, invocation, conformance (297 clauses, 0 declarations naming no clause) and independence.
