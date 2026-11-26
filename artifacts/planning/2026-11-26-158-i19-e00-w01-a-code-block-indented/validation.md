# W01 Validation

The checks run against branch `i19/e00/w01-code-block-in-list` at `b5a65f447`, cut from `i19/e00/main` at `3c400526d`.

## T1 Shared Reading Tests

`make harness` ran `checks/tests`: 1200 passed.

The cases in `checks/tests/test_documents.py` that state AC1:

| Case | Input | Observed |
| --- | --- | --- |
| `test_a_code_block_inside_a_bullet_is_blanked` | A link form indented six columns under `- A bullet.` | The line is blanked |
| `test_a_nested_bullet_beneath_a_bullet_holding_a_code_block_is_read` | That code block, then `  - A nested bullet with [a link](present.md).` | The code block is blanked and the nested bullet is kept as written |
| `test_a_code_block_beneath_a_list_items_paragraph_is_blanked` | A link form indented seven columns under an ordered item's second paragraph | The line is blanked |
| `test_a_code_block_beneath_a_paragraph_at_the_margin_is_blanked` | A link form indented four columns under a paragraph at the left margin | The line is blanked and the link below it is kept |
| `test_a_nested_bullet_short_of_a_code_block_indent_is_content` | `    - A nested bullet.` under `- A bullet.` | The line is kept |

Against the reading at `3c400526d`, the first two cases fail and the others hold: a line directly below a list marker was held to be content however far it was indented.

## T2 Link Check

`make links` ran online: every reference in 445 documents resolved.

A comparison of the references the old and new readings leave in every document the check reads found no document whose reference set differs. No link is masked or unmasked by the change.

## T3 Repository Checks

`make check` ran with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf` and exited 0: lock check, lint, format check, type check, build tests, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence.

## Limitations

- `strip_code_fences()` recognises a fence at the left margin only. A fence indented inside a list item is read by the parser as a fence rather than an indented code block, so its contents stay in the text the link check reads. That is outside this row's criterion.
