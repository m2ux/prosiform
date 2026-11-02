# Validation

The checks [W12](w12.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `4958ad38`. It narrows *Recognition* to one arrow and *Operator marks* to `⇉` and `↳`, adds *Composing its own document* and `W_COMPOSE_SELF`, and adds the `Run pf first` sub-section to *The Prosiform section*, with *Clean Markdown* and both fixture lists following. |
| Branch head | `a86a81ed` on `i09/e04/w12-arrow-directives-self-composition` |

## T1 Arrow Labels

| Check | Shows | Criterion |
| --- | --- | --- |
| `test_composition.py` | Arrows from each Arrows block, a Dingbats arrow, a Miscellaneous Symbols and Arrows arrow, entities and a supplementary arrow are directives; `†`, `‡`, `&dagger;`, `¹`, `é`, `𝔸`, `٣`, `★`, `⬒`, `➤`, an unassigned Supplemental Arrows-C scalar and `¬†` are not. | AC22 |
| `a-supplementary-arrow-label-is-a-directive` | `[🡒]` in a preamble: refused for want of a scope, so recognised as a directive. | AC22 |
| `an-entity-decoding-to-one-arrow-is-a-directive` | `[&rarr;]` in a preamble: refused likewise. | AC22 |
| `non-arrow-labels-are-ordinary-links` | `†`, `‡`, `&dagger;`, `¹`, `é`, `𝔸`, `★` and invisible scalars in a preamble: exit 0, each an ordinary link rewritten to `#output`. | AC22 |

Fixtures rewritten for the new rule: `a-supplementary-scalar-label-is-a-directive` (label `𝔸`, a directive before) became `a-supplementary-arrow-label-is-a-directive` with `🡒`; `invisible-scalar-labels-are-ordinary-links` became `non-arrow-labels-are-ordinary-links`, adding the non-arrow labels; `an-entity-decoding-to-one-scalar-is-a-directive` was renamed for its arrow; descriptions of `a-glyph-label-in-a-preamble-has-no-scope`, `a-reference-style-glyph-label-is-a-directive` and `ascii-and-spaced-labels-are-ordinary-links` now say arrow. The unit cases `[é]`, `[𝔸]`, `[&#x1D538;]`, `[¬𝔸]` and `[⇉𝔸]` moved from directives to ordinary links or to `🡒`.

Result: pass.

## T2 Self-Composition

| Check | Shows | Criterion |
| --- | --- | --- |
| `a-directive-composing-a-section-of-its-own-document-by-fragment-warns` | `[→](#rules)` in `guide.md`'s Run step: exit 0, the section composed, `W_COMPOSE_SELF` naming `#rules` and `guide.md#rules`. | AC23 |
| `a-directive-composing-a-section-of-its-own-document-by-path-warns` | `[→](guide.md#rules)`: the same, naming `guide.md#rules`. | AC23 |
| `test_cli.py` | The warning's location is `guide.md:10`; a deferred `[¬→](#rules)` raises none. `a-directive-composing-its-own-section-is-refused` still fails as a cycle. | AC23 |

Result: pass.

## T3 First Run of a Dispatched Bundle

| Check | Shows | Criterion |
| --- | --- | --- |
| `a-deferred-dispatch-in-a-dispatched-bundle` | `steps.bundle.md` opens `Before following this bundle, [run pf first](#run-pf-first).`, then `# Prosiform`, `## Run pf first` and ``Run `pf` first, with no arguments, and follow the guide it prints.`` | AC24 |
| `a-deferred-directive-in-a-dispatched-bundle-opens-with-a-first-run` | A dispatched bundle carrying `[↳ Body](rules.md#body)` opens alike; the entry's bundle carries Dispatch alone. | AC24 |
| `a-dispatched-bundle-needing-a-first-run-and-dispatching` | `Run pf first` precedes `Dispatch` in one Prosiform section. | AC24 |
| `a-plain-deferral-in-a-dispatched-bundle-takes-no-first-run` | `[¬ the rules]` alone: no Prosiform section. | AC24 |
| `test_cli.py` | A dispatched bundle opens with the line and section; an entry carrying `[¬⇉ b]` opens on `# Guide`. | AC24 |

Result: pass.

## T4 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `a86a81ed`. Results:

- Unit tests: 1663 passed. The harness ran 1161.
- Corpus: 498 fixtures, all pass.
- Conformance: 355 clauses. *Section composition — Recognition* has 10 fixtures, *Composing its own document* 2, *The Prosiform section* 12.
- Vocabulary: 49 contract terms, *arrow* among them, each defined in the glossary.
- Independence: every term is one the contract names.

Result: pass.
