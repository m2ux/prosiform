# Validation

The checks [W01](w01.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`99bec9f7`](https://github.com/m2ux/prosiform/blob/99bec9f7548b9910047b7bde663a2eb76efd2e3e/artifacts/planning/2026-10-17-prosiform-v1/design.md#section-composition), the README pin |
| Branch head | `30d4b7bf` on `i09/e04/w01-the-grammar-and-its`, cut from `i09/e04/main` at `a73778f3` |

## T1 Recognition Unit Tests

`src/tests/test_composition.py` reads each case through the source reader, so a label is judged as the parser produced it.

- **Directives.** An arrow, a precomposed letter, a named entity, hexadecimal and decimal references, a supplementary scalar written and as a reference, a no-break space, a titled link, and shortcut, collapsed and full reference links.
- **Not directives.** An ASCII letter, an entity decoding to ASCII, an escaped ASCII mark, a scalar with a leading, a trailing or a surrounding space, emphasis, strong emphasis, a code span, a strikethrough, a hard line break, raw HTML, an image inside the label, two scalars, a combining sequence, a variation-selector sequence, a joined emoji, a two-scalar flag, and a full reference whose own text is ASCII.
- **No label.** An image, an autolink and a link inside code carry no directive; bracketed text no definition resolves is no use.
- **Marks and deferral.** Each lone mark, `¬`, `↳`, `⇉` and `⫽`, is no directive. A deferred glyph with one or two blanks, an entity or a supplementary scalar is a deferred directive; an ordinary deferred label is a deferral and no directive; an immediate glyph is a directive and no deferral. `[¬→]`, `[¬ ¬]`, `[¬ ↳]` and `[¬ → ]` leave no qualifying label. `[⇉ →]`, `[⫽ →]` and `[¬⇉ →]` are dispatches and no directive.

52 cases, all pass.

Result: pass.

## T2 Composition Fixtures

The `fixtures/composition/` family puts each label in a preamble, where a directive has no scope and is refused with `E_UNSUPPORTED_CONSTRUCT` and an ordinary link bundles, so each fixture tells a directive from an ordinary link by the run's result.

| Fixture | Label | Result |
| --- | --- | --- |
| `a-glyph-label-in-a-preamble-has-no-scope` | `[→]` | refused, `guide.md:4` |
| `an-entity-decoding-to-one-scalar-is-a-directive` | `[&rarr;]` | refused |
| `a-supplementary-scalar-label-is-a-directive` | `[𝔸]` | refused |
| `a-reference-style-glyph-label-is-a-directive` | shortcut `[→]` | refused |
| `a-deferred-glyph-label-is-a-deferred-directive` | `[¬ →]` | refused |
| `ascii-and-spaced-labels-are-ordinary-links` | `[A]`, `[&amp;]`, `[ → ]` | bundled |
| `formatted-labels-are-ordinary-links` | emphasis, strong, code span, strikethrough | bundled |
| `multi-scalar-labels-are-ordinary-links` | two scalars, combining, variation selector, joined emoji | bundled |
| `operator-marks-are-no-directive-label` | `[¬]`, `[⇉]`, `[⫽]`, `[↳]`, `[¬→]` | bundled |
| `an-ordinary-deferred-label-is-a-deferral` | `[¬ the output]` | withheld, path destination |
| `a-dispatched-glyph-is-a-dispatch` | `[⇉ →]` | dispatched as `Dispatch →` |
| `a-glyph-in-code-or-unresolved-brackets-is-text` | code span, unresolved `[→]` | carried as text |

All 12 pass. `make conformance` maps them to *Section composition — Recognition* (9), *Operator marks* (4) and *The destination scope* (5), and to *Adversarial acceptance fixtures — Composition*.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `30d4b7bf`, exit 0. Unit tests 1644 pass; the corpus reported 445 fixtures, 445 pass, 0 fail, 0 awaited; conformance read 356 clauses with 0 declarations naming no clause.

Result: pass.
