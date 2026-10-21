# Validation — I00:E11:W23

> The checks this row ran, the revision they ran against, and what each observed.

Revision `44f79cb` on `i00/e11/w23-a-documented-example-read`, cut from the epic base `i00/e11/main` at `ce4483c`. The build under test is the checkout's own, named to the corpus and invocation checks as `uv run --project <worktree>/src --frozen prosiform`.

## A link form inside literal content is passed over

`checks/tests/test_links.py` carries a document whose literal forms each hold a link form, and whose content holds four links beside them.

- `test_a_reference_inside_a_code_span_is_an_example_rather_than_a_reference` — the inline form and the definition form written inside a code span are absent from what the scan read.
- `test_a_reference_inside_an_indented_block_is_an_example` — the same two forms written inside an indented block are absent.
- `test_a_fenced_reference_is_an_example_rather_than_a_reference` — the fenced case the suite already carried, still holding.

## A link beside it is resolved

- `test_a_reference_beside_literal_content_is_read` — the inline link on the line carrying the code span, and the reference definition below the indented block, are both read.
- `test_a_reference_a_nested_bullet_carries_is_read` — a link inside a bullet, and one inside a bullet nested four spaces below it, are both read. A list's continuation is content however far it is indented, so the indented-block rule does not reach it.
- `test_every_reference_the_literal_document_carries_is_read` — the scan returns those four references and nothing else, in the order the document writes them.

## The readings that want a code span kept still have it

- `test_a_heading_naming_a_code_span_still_generates_its_fragment` — ``## The `link` Form`` generates `#the-link-form`, so the heading reading reduces a code span to its code rather than blanking it.
- `make tables` compared 14 commands and 7 declarations in both directions, each cell reduced from a code span.

## The mask over the repository's own documents

Every reference each of the twelve documents carries was read twice, once under the fenced-block mask alone and once under the literal mask, and the difference listed. One reference differs: `../SKILL.md`, the deferral syntax this row writes into `example/README.md` as the example it is. No reference the repository relies on left the scan.

## The check set

`make check` at `44f79cb`, every target passing, exit status 0.

| Target | Observed |
| --- | --- |
| `lock-check` | 22 packages resolved against the lock |
| `lint` | all checks passed |
| `format-check` | every file formatted |
| `typecheck` | no issues in 49 source files |
| `test` | 670 passed |
| `harness` | 501 passed |
| `corpus` | 217 fixtures, 217 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `smoke` | the installed command bundles a reference from a source root outside the repository |
| `layout` | 3 trees present |
| `tables` | 14 commands and 7 declarations, each declared and named |
| `links` | every reference in 12 documents resolved |
| `vocabulary` | 35 contract terms marked, each defined and carried |
| `invocation` | 27 statements of the documented invocation held to the build |

## Limitations

- **The indented-block rule reads a list by its markers.** A block opens at a four-space or tab indent following a blank line, and a line below a list marker is that list's content until a line at the left margin that opens no list item. A document that indents a code block inside a list item writes it where this rule reads content, and a link form there would be resolved. The product's parser decides this from the list item's own content column; the check has no parser and the standard library is its whole dependency, so it reads the common case and leaves the nested one.
- **The code-span rule is the product's, reimplemented.** `checks/` imports no package, `prosiform` among them, so `strip_code_spans()` states the backtick-run rule a second time. The two are held together by their shared behaviour rather than by shared code, and `test_a_code_span_closes_on_a_run_of_its_own_width` is where this check's half is stated.
