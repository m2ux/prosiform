# W01 Test Evidence

Results for the W01 pull request, tested at commit 6bc4937f3 on `i19/e02/w01-indented-fences`, based on `i19/e02/main` at 6eb02cb5c.

## T1 Shared Reading

`checks/tests/test_documents.py` holds the reading to these cases, each passing:

- `test_a_fence_inside_a_bullet_is_blanked_and_the_bullet_is_read`: a fence indented two columns under a bullet is blanked with its delimiters, while the bullet's own link and a nested bullet's link survive `strip_literal`. This observes AC1.
- `test_a_fence_at_the_margin_is_blanked_with_its_delimiters`: a fence at the left margin is blanked as before.
- `test_a_fence_closes_only_at_a_fence_of_its_own_character`: a backtick line inside a tilde fence does not close it.
- The indented-block cases carry over unchanged, now against `strip_code_blocks`.

## T2 Make Check

`make check` with `PROSIFORM_BUILD` set to the worktree's own build exited 0, the links target run online. The checks suite reported 2125 passed and the evaluation suite 1237 passed.

## T3 Before and After

A script read every repository document `documents()` yields (445) with the base reading and again with the change, recording each document's references (`links.references`), heading fragments (`links.fragments_of`) and tables (`documents.tables`). The two outputs are identical: no reference, heading or table moves.

No repository document holds a fence indented inside a list item today, so the change guards future documents and alters no present reading.
