# Validation

The checks [W04](w04.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `99bec9f7`, whose *Section composition* states *Order*, *Matching*, *The destination scope*, *The eligible target*, *Contributions*, *Heading depth* and *Generated heading collisions* |
| Branch head | `5de2eba6` on `i09/e04/w04-ordering-matching-and-diagnostics`, with `i09/e04/main` merged at `32568729` (W08 included) |

## T1 Order and Matching Fixtures

Each success fixture also links its target documents whole, so each target keeps its own file group.

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `destination-sections-follow-first-reference-order` | Two steps name the same sections in different orders. Each step's destination sections follow the order their first directive is written, after the step's content and before its child section, and contributions follow their directives' order. | AC7 |
| `titles-match-exactly-as-written` | Targets titled with a precomposed accent, a combining accent and lower case each take their own destination section: no normalisation or case folding. | AC7 |
| `same-titled-parents-keep-a-contribution-each` | Two parents titled `Call` keep one contribution each under one `Inputs` section, linked as `#call` and `#call-1`. | AC7 |

Result: pass.

## T2 Structural Failure Fixtures

Each run fails, publishes nothing, and names the directive's link, its source line and its chain.

| Fixture | Code | Criterion |
| --- | --- | --- |
| `a-directive-in-an-absorbed-title-has-no-scope` | `E_UNSUPPORTED_CONSTRUCT` at `step.md:4` | AC8 (missing containing heading) |
| `a-directive-in-a-title-above-the-selection-has-no-scope` | `E_UNSUPPORTED_CONSTRUCT` at `step.md:4` | AC8 (missing containing heading) |
| `a-glyph-label-in-a-preamble-has-no-scope` (W01) | `E_UNSUPPORTED_CONSTRUCT` at `guide.md:4` | AC8 (missing containing heading) |
| `a-directive-naming-a-missing-document-is-refused` | `E_TARGET_NOT_FOUND` at `guide.md:8` | AC8 (missing source) |
| `a-directive-naming-a-missing-section-is-refused` | `E_TARGET_NOT_FOUND` at `guide.md:8`, resolved `read.md` | AC8 (missing section) |
| `a-target-with-no-parent-heading-is-refused` (W02) | `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8` | AC8 (missing parent) |
| `an-authored-heading-equal-to-a-destination-section-is-refused` | `E_HEADING_COLLISION` at `guide.md:8`, message naming `guide.md:10` | AC8 (conflicting child heading) |
| `a-directive-composing-past-the-sixth-level-is-refused` | `E_HEADING_DEPTH_OVERFLOW` at `guide.md:14`, reference `read.md#inputs` | AC8 (unsupported depth) |

`a-heading-equal-to-the-dispatch-protocol-is-refused` now pins the authored heading's file line, 10, which the dispatch collision diagnostic named as its content line before.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `5de2eba6`. Results:

- Unit tests: 1655 passed. The harness ran 1202.
- Corpus: 472 fixtures, all pass.
- Conformance: 356 clauses read, and no declaration names a missing clause.

Result: pass.
