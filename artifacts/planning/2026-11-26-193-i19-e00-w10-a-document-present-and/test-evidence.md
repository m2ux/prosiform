# W10 Test Evidence

> Revision `b42113e93` on `i19/e00/w10-document-present-not-read`, tested 2026-11-26.

## T1

`make harness` runs `checks/tests/test_documents.py::test_a_reading_check_names_an_untracked_document_as_unread`, once for `links.py` and once for `tables.py`. Each case builds a fresh git repository holding a copy of `documents.py` and the check, with one tracked document, then adds to the working tree:

- `draft.md`, untracked, holding a reference to a missing file;
- `ignored.md`, named by `.gitignore`, holding the same reference;
- `fixtures/new/`, an untracked fixture with a manifest and a document holding the same reference.

Observed: each check exits zero, prints exactly `unread draft.md — present and untracked`, and its summary ends `; 1 untracked document(s) unread`. Neither the ignored document nor the fixture's document is named or read. Result: 1198 passed.

## T2

The same run over this repository's own tree, with `docs/draft-unread.md` written untracked and holding a broken reference, then removed:

```text
unread docs/draft-unread.md — present and untracked
table check: 23 command(s) and 8 declaration(s), each declared by the project and named by a table; 1 untracked document(s) unread
unread docs/draft-unread.md — present and untracked
link check: every reference in 445 document(s) resolved; 1 untracked document(s) unread
```

## T3

`make check` at the revision above, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`, the links target run unsandboxed: every check passed (lint, format, typecheck, test 2125 passed, harness, corpus, smoke, layout, tables, links online over 445 documents, vocabulary, invocation, conformance, independence).
