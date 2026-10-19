# Validation — I00:E03:W02

> The checks as they were run, and what each establishes.

## The Gate

`make check` was run whole in the delivery worktree, with `PROSIFORM_BUILD` naming the prototype by absolute path, and returned zero.

| Check | Result |
| --- | --- |
| `lock-check` | Resolved 22 packages |
| `lint` | All checks passed |
| `format-check` | 26 files already formatted |
| `typecheck` | Success: no issues found in 25 source files |
| `test` | 283 passed |
| `harness` | 189 passed |
| `corpus` | 54 fixtures, 50 pass, 0 fail, 4 awaited, 0 unexpected pass |
| `layout` | 3 trees present |
| `tables` | 12 commands and 7 declarations, each declared and named by a table |
| `links` | Every reference in 6 documents resolved |
| `vocabulary` | 34 contract terms marked, every one defined and carried |

The fixtures this row touches are among the corpus run's results:

```text
extraction/a-heading-a-blockquote-carries: awaited, awaiting I00:E03:W03
extraction/a-heading-only-in-a-code-example: pass
extraction/a-list-item-heading-as-a-target: pass
extraction/a-section-the-document-outlasts: pass
extraction/a-setext-heading-as-a-root: awaited, awaiting I00:E03:W03
extraction/a-subsection-inside-the-section: pass
extraction/an-unterminated-example-at-the-section-end: awaited, awaiting I00:E08
extraction/heading-like-text-in-a-code-example: pass
extraction/nested-section-target: pass
extraction/section-to-the-next-sibling: pass
headings/a-heading-with-no-visible-text: pass
```

## The Markers Measured

Four candidate deferrals were named ahead of the work. Each was run before it was marked.

| Case | Measured | Marked |
| --- | --- | --- |
| A section terminated by end of file | Runs to the last region the document holds | No — `extraction/a-section-the-document-outlasts` passes |
| A heading inside a list item | Refused as an unsupported target, as one inside a blockquote is | No — `extraction/a-list-item-heading-as-a-target` passes |
| A fragment naming a heading only a code example spells | No heading of the index carries that fragment, so the reference resolves to nothing | No — `extraction/a-heading-only-in-a-code-example` passes |
| A section whose last block is an unterminated container | The example absorbs the group written after it, which is the unsafe boundary `I00:E08` refuses | Yes — `awaiting = "I00:E08"`, not `I00:E10` |

Two markers already in the corpus came off on measurement. `extraction/nested-section-target` awaited this epic, and `headings/a-heading-with-no-visible-text` awaited `I00:E10` because a fragment selected nothing until section extraction landed; a lookup now reaches both.

Two fixtures this row adds carry a marker naming the next row rather than this one. Each states a section whose extent this row settles and whose headings are emitted in a syntax `I00:E03:W03` decides, and each differs from the build in that one respect alone:

```text
extraction/a-heading-a-blockquote-carries
  9c9
  < > ### Quoted
  ---
  > > ## Quoted

extraction/a-setext-heading-as-a-root
  5c5,6
  < ### Run
  ---
  > Run
  > ---
```

## What the Criteria Rest On

**AC1** — a fragment naming an eligible heading selects that heading and the blocks up to the next document-level heading of equal or higher level, with container-nested headings not terminating it.

The boundary is shown whole by the corpus. `section-to-the-next-sibling` ends a section at the next heading of its own level and leaves the preamble above it out; `a-subsection-inside-the-section` carries the deeper headings and their content and still ends at the next sibling; `a-section-the-document-outlasts` runs to the last region the document holds; `heading-like-text-in-a-code-example` carries an example spelling a heading and the block after it, both inside the section.

The container clause is shown by unit case and declared by fixture. `test_a_heading_a_blockquote_carries_ends_no_section` and `test_a_heading_a_list_item_carries_ends_no_section` observe the regions the selection returns. The fixture that observes it through published bytes, `a-heading-a-blockquote-carries`, selects past the blockquote correctly and differs from the build only in the level its quoted heading is emitted at, which is the shift `I00:E03:W03` applies inside retained containers. The criterion is not ticked on the corpus alone.

**AC2** — a fragment naming a container-nested heading fails with its declared error code.

`extraction/nested-section-target` names a heading inside a blockquote and `extraction/a-list-item-heading-as-a-target` names one inside a list item. Each exits 1, publishes nothing and emits `E_NESTED_SECTION_TARGET` against the reference that named it. Both containers the design lists are covered, and the code came from the catalogue unchanged.
