# Change List — W02 Refuse Distribution Faults and Entry Overwrite

> Delivery record · 2026-10-31

The plan changes this session applied, the ones it held, and the technical debt it classified.

## Applied

| Change | Kind | Why | Where |
| --- | --- | --- | --- |
| `target` refuses a dispatch the map holds no sub-section for, rather than indexing it | Source | The `KeyError` was an internal fault where a source construct could not be carried | `src/prosiform/bundle.py` |
| A title above the selection refuses the dispatch it carries | Source | Probing the neighbouring shapes found a third site where the same dispatch is dropped silently at exit 0, its target compiled by no run — the silent outcome the finding records | `src/prosiform/bundle.py`, `src/prosiform/grouping.py` |
| The refusal carries the line of the file, threaded from the source's first content line | Source | Frontmatter moves the content's line count, and a title in a member with frontmatter reported line 2 of a document whose title is on line 7 | `src/prosiform/bundle.py`, `src/prosiform/grouping.py`, `src/prosiform/cli.py` |
| `overflowing` renamed `assembling` and holding both source faults | Source | It now translates a second source fault; naming it for one of the two would misstate it | `src/prosiform/cli.py` |
| A path at the run folder's own that is neither a folder nor a link is refused before anything is written | Source | A regular file there was renamed aside and unlinked, destroying bytes the run never read while exiting 0 | `src/prosiform/cli.py` |
| The work item's Test row delivered as three dispatch cases and three standing-file cases | Test | The row asks for a run over a document whose absorbed title carries a dispatch link, and a run over a regular file at the bundle path that refuses and leaves the file intact | `src/tests/test_cli.py`, `src/tests/test_derived_output.py` |

No finding moved between tasks, no task was created, closed or renumbered, and no criterion changed. The epic's disposition already carried findings 4 and 18 to W02, and the work item's Test row already named both cases, so the plan as written was followed.

## A plan attribution corrected in the record, not in the plan

The work item names `src/prosiform/bundle.py` as the component, and the epic's row states findings 4 and 18 as its scope. Finding 4's site is in `bundle.py` as stated — `target`, at the map index that raised. Finding 18's is not: the rename and unlink are in `publish_folder`, and the checks that precede a write are in `publication`, both in `src/prosiform/cli.py`.

The repair follows the finding rather than the component name, so it lands where the defect is. `cli.py` holds publication and no other task's scope names it, so the six concurrent deliveries do not collide there. Recorded here rather than amended in the epic: the row states a scope area, and the two findings under it reach two modules of that area.

## Held

| Held | Why |
| --- | --- |
| A corpus fixture for each refusal | Both cases are reachable through a fixture's source tree and exit status, so a fixture would hold them. Neither is taken here: the corpus declares one code per construct, and `E_UNSUPPORTED_CONSTRUCT` already reaches `fixtures/dispatch` for five other constructs while `E_PUBLICATION_FAILED` already reaches `fixtures/publication`. A fixture would restate the code rather than add coverage, and the work item's Test row asks for the run rather than the fixture |
| Refusing a dispatch in an ancestor heading the run did not select | An ancestor heading is emitted as a heading alone and its link is flattened to literal text, so a dispatch there is in principle the same defect. It is not refused here: no finding records a case, and probing showed the ancestor's own region places its dispatch where the group emits it |
| A remedy for a file at the run folder that offers to move it aside | The remedy names removing or renaming it and naming another output folder. A run that moved it would still be destroying a path it did not write, which is the defect |

## Technical debt classified

| Debt | Class | Disposition |
| --- | --- | --- |
| `test_linked_bootstrap` needs network for `uv build` | Deferred, not this task's | The brief names it as reproducing on every settled branch and passing in CI. It passed here, inside the sandbox, so no failure needed checking against a clean checkout |
| The publication tests fail under `/tmp`'s atomic folder swap | Deferred, not this task's | Same standing; the tests passed in this run |
| A dispatch in a document title is refused rather than placed | Deferred to design, not blocking | A title is a name the file heading carries, not a section, so a sub-section beneath it would have no level to take. Making it representable is a contract change no finding asks for. The refusal states the defect and the remedy |
| `rewrite` takes nine positional parameters | Deferred, not blocking | Trivial, but folding them into a value object is a refactor across `bundle.py`, `grouping.py` and `cli.py`, and this branch is one fix. Left as it stands |

Nothing blocking was found. The one trivial candidate inside the changed code — the `first_line` parameter threaded through three modules — is the narrowest form the fix takes, so it is delivered rather than deferred.

## Placement needs

None. No new initiative, epic or task was needed, and nothing was found that needs a home outside this pull request.
