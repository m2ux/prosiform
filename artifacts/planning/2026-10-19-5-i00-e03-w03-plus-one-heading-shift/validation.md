# Validation — I00:E03:W03

> The checks as they were run, and what each establishes.

## The Gate

`make check` was run whole in the delivery worktree, with `PROSIFORM_BUILD` naming the prototype by absolute path, and returned zero.

| Check | Result |
| --- | --- |
| `lock-check` | Resolved 22 packages |
| `lint` | All checks passed |
| `format-check` | 26 files already formatted |
| `typecheck` | Success: no issues found in 25 source files |
| `test` | 297 passed |
| `harness` | 196 passed |
| `corpus` | 61 fixtures, 59 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `layout` | 3 trees present |
| `tables` | 12 commands and 7 declarations, each declared and named by a table |
| `links` | Every reference in 6 documents resolved |
| `vocabulary` | 34 contract terms marked, every one defined and carried |

The fixtures this row touches are among the corpus run's results:

```text
extraction/a-heading-a-blockquote-carries: pass
extraction/a-setext-heading-as-a-root: pass
hierarchy/a-setext-heading-a-quote-carries: pass
hierarchy/a-setext-heading-an-absorbed-title-leaves: pass
hierarchy/a-setext-heading-becomes-atx: pass
hierarchy/a-setext-heading-over-two-lines: pass
hierarchy/a-shift-that-writes-a-level-only: pass
hierarchy/every-level-moves-down-one: pass
hierarchy/headings-a-container-carries: pass
```

The two markers left in the corpus belong to other work: `normalization/root-escape` awaits `I00:E04` and `extraction/an-unterminated-example-at-the-section-end` awaits `I00:E08`.

## The Markers Measured

Seven candidate deferrals were named ahead of the work. Each was run against the build before it was marked, and none was marked.

| Case | Measured | Marked |
| --- | --- | --- |
| A Setext heading inside a list item | Converted to ATX behind the item's indent, which the list keeps | No |
| A Setext heading written over two lines inside a blockquote | Converted to one ATX line behind the quote markers | No |
| A Setext heading a tab-indented quote carries | The tab is the prefix the rewritten line opens with | No |
| A Setext heading inside a doubly nested blockquote | Both markers kept, the heading shifted inside them | No |
| Emphasis spanning two content lines of a Setext heading | The inline source is carried, so the emphasis closes as it did | No |
| A thematic break lazily following a quote line | Not a Setext underline, so the quote and the break stay two regions | No |
| A heading a container carries that the shift would place beyond H6 | Refused as the overflow it is, as a document-level heading is | No |

Two markers came off on measurement, both written by `I00:E03:W02` against this row. Each differed from the build in one respect, and each passes on this row's delivery:

```text
extraction/a-heading-a-blockquote-carries
  the quoted heading now emitted at the level the group's shift puts it at

extraction/a-setext-heading-as-a-root
  the Setext root now emitted as the ATX heading of the same level
```

## What the Criteria Rest On

**AC3** — each emitted source heading in a group carrying its own title sits exactly one level deeper than in its source, with its visible text and relative depth unchanged.

`hierarchy/every-level-moves-down-one` carries H1 through H5 under a title the path does not name: each is emitted one level deeper, the deepest at H6, and the heading that returns to the second source level returns to the second emitted level, so relative depth is read off the bytes rather than asserted. `hierarchy/headings-a-container-carries` shifts a heading inside a blockquote, inside a blockquote the blockquote carries, and inside a list item, while the quote markers, the list structure and the heading-like text inside a fenced example are carried as the source wrote them. `hierarchy/a-shift-that-writes-a-level-only` holds an indented heading and a heading carrying a closing sequence, each emitted with the level changed and nothing else. `identity/title-the-path-does-not-carry` and `real-source/frontmatter-and-a-shifted-group` were already passing and state the same shift over a written and a copied source; `identity/whole-document` and `real-source/absorbed-title-and-self-references` state the group that absorbed its title keeping its source levels.

**AC4** — a Setext heading is emitted as the equivalent ATX heading carrying the same visible text and inline semantics.

`hierarchy/a-setext-heading-becomes-atx` converts a Setext H1 and a Setext H2 carrying emphasis and a code span, in a group that also shifts an ATX heading, so both syntaxes are shown moving alike. `hierarchy/a-setext-heading-over-two-lines` states the multiline source form, which becomes one ATX line because an ATX heading is one line, with the line break read as the space a renderer already read it as. `hierarchy/a-setext-heading-a-quote-carries` states the conversion inside a retained container. `hierarchy/a-setext-heading-an-absorbed-title-leaves` states the group that shifts by nothing, which writes no level and so leaves the Setext heading its source wrote. `hierarchy/a-shift-that-writes-a-level-only` states the text an ATX heading would otherwise lose: a number-sign run ending a converted heading is escaped, because an ATX heading ends at one. `extraction/a-setext-heading-as-a-root` states the conversion of a selected root.

**AC1** — a fragment naming an eligible heading selects that heading and the blocks up to the next document-level heading of equal or higher level, with container-nested headings not terminating it.

The boundary half was shown whole by `I00:E03:W02` and its four fixtures pass unchanged: `section-to-the-next-sibling`, `a-subsection-inside-the-section`, `a-section-the-document-outlasts` and `heading-like-text-in-a-code-example`. The container half is now published by `extraction/a-heading-a-blockquote-carries`, which selects one section by fragment, carries the blockquote and the block written after it, and emits the quoted heading at the level the group's shift puts it at. Both halves are observed through published bytes, so the criterion is ticked on the corpus and `I00:E03:W02` is done with it.
