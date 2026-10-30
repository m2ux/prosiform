# Review of PR #342

A code review of `i05/e02/main` against `main`, run before the epic pull request is marked ready. Findings 2–5 were reproduced against the branch head; 1, 6 and 7 are from reading the code.

## Findings

| # | Location | Finding | Row |
| --- | --- | --- | --- |
| 1 | `source.py` sequence reader | A destination written `doc.md#35;intro`, the only anchor spelling the sequence lexer keeps, resolves as the fragment `35;intro`. | W05 (AC9) |
| 2 | `source.py` `MENU_ENTRY`, `QUOTED_LINK` | The `link` forms match in every diagram type: a state line `link --> done : retry @ ops.md` bundles `ops.md` and rewrites the label. | W05 (AC10) |
| 3 | `source.py` `MENU_ENTRY` | The destination runs past `;`, where Mermaid's sequence lexer ends the statement: `@ a.md;b.md` reads as `a.md;b.md`. | W05 (AC11) |
| 4 | `source.py` `entries` | Every value of a repeated `links` key is bundled; `JSON.parse` keeps the last. | W06 (AC12) |
| 5 | `source.py` `entries` | A value that is not a string is skipped without a fault while its siblings are bundled. | W06 (AC13) |
| 6 | `source.py`, `bundle.py`, `candidate.py` | Each module defines its own `ANCHOR`. | W07 (AC14) |
| 7 | `source.py` `entries`, `clicks` callers | A `links` line is JSON-decoded twice per read, and a fence's uses are read about six times per run. | W07 (AC15) |

## Decisions

- **A value that is not a string faults.** Mermaid renders it as a broken menu entry, so the run names the line rather than bundling its siblings around a gap.
- **Every variant end to end.** The user requires each link form the reader follows to be proven by an end-to-end fixture rendered under Mermaid 11.16.0, and the out-of-scope forms to be shown carried as written (W08).
