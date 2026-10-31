# Validation — W02 Refuse Distribution Faults and Entry Overwrite

> Evidence · 2026-10-31

Every case below was run in the worktree `.worktrees/i07/e00/w02-refuse-distribution-faults-and`, at branch `i07/e00/w02-refuse-distribution-faults-and`, cut from `i07/e00/main` at `23882b7d` and fast-forwarded onto it at `d99025c1`. The branch merged as [#470](https://github.com/m2ux/prosiform/pull/470) into `i07/e00/main` at `de694350`.

The build under test is named `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`. Tooling ran under the sandbox by absolute path; `git fetch` and `git push` ran unsandboxed.

## Baseline, before any change

Both faults were reproduced against the branch as cut, before a line was edited, so a case that reports a named code only after the repair would prove nothing.

## Finding 4 — a dispatch link in an absorbed document title

**The break.** A linked document titled `# Note [⇉ Plan](plan.md)`, reached from `# Guide` by `Read [the note](note.md).`, with `plan.md` carrying `# Plan` and `1. Go.`.

**Before the fix**, the run raised an unhandled exception and reported it as an internal fault at exit 4:

```
E_UNEXPECTED_INTERNAL_ERROR: unexpected internal error: KeyError((('plan.md', None), False))
exit status 4; no bundle written
```

The traceback reaches `src/prosiform/bundle.py:508`, in `target`, at `return f"{anchor}{held[served]}"`. The map was indexed with `(('plan.md', None), False)` and held no such key, because the title the file heading absorbs is emitted as a heading carrying the title's text rather than as a section — so `Placing.flush` placed no dispatch sub-section for the region that writes the link. Instrumenting `cli.subsections` over the same run showed `placed keys: []` where a body dispatch gives `[('note.md', 2)]`.

The same key was reached from a merged group's member, where the subsection naming the member absorbs its title — `KeyError((('plan.md', None), False))`, exit 4, again with nothing published.

Both operators reach it: `⇉` and `⫽` alike.

**The defect.** A dispatch sub-section stands one level below the section holding its link, and an absorbed title is no section. The link is still in selected content, so the rewrite asks the map for a sub-section nothing placed. The run treated a source construct it cannot carry as a fault in itself.

**After the fix**, the run refuses the link under the code the contract already names for a construct the run cannot carry, naming the link, its source line and the chain that reached it:

```json
{"severity": "error", "message": "the dispatch '⇉ Plan' in 'note.md' names 'plan.md', and the heading that carries it is no section a dispatch sub-section can stand beneath", "code": "E_UNSUPPORTED_CONSTRUCT", "reference": "plan.md", "source": "note.md:1", "chain": ["entry.md", "note.md"], "remedy": "write the dispatch in the body beneath the heading, where a sub-section has a section to follow"}
```

exit status 1, nothing published. The merged-member shape reports the same code against `note-⇉-plan.md:7`, the title's line in the file rather than in the frontmatter-stripped content.

**A third shape, at a second site.** Probing the neighbouring arrangements found one the finding does not name, where the outcome is silent rather than loud. A selection naming a section beneath a title — `Read [the part](note.md#part)` against `# Top [⇉ Plan](plan.md)` with `## Part` beneath — leaves the title above the selection, so no group emits it and the file heading carries its text as literal heading text.

**Before the fix**, the dispatch vanished and the run reported success:

```
status 0
== entry.bundle.md
# Entry

Read [the part](#part).

# Top Plan

### Part

Body.
```

No bundle for `plan.md` was written, no diagnostic was emitted, and `# Top Plan` carries the link's text as heading text. The author's dispatch was dropped without a trace and the run exited 0 — the silent outcome the finding records, at its worst.

**After the fix**, the same refusal, against the title's own line:

```json
{"code": "E_UNSUPPORTED_CONSTRUCT", "source": "note.md:1", "chain": ["guide.md", "note.md#part"], "reference": "plan.md"}
```

**What did not move.** The shapes that already worked still do, each asserted beside the refusals:

| Shape | Result |
| --- | --- |
| The entry document's own title, `# Guide [⇉ Plan](plan.md)` | publishes; the sub-section stands beneath the file heading |
| A heading inside the body | publishes; the sub-section sits one level below it |
| A deferred link in a title, `# Entry [¬ Plan](plan.md)` | publishes; the title rebases to the target's path |

## Finding 18 — a regular file standing where the run folder belongs

**The break.** `a.md` in the working directory, an output folder `out`, and a regular file holding `unrelated bytes` at `out/a.bundles`.

**Before the fix**, the run exited 0 after renaming the file aside and unlinking it:

```
finding18 status: 0
finding18 stderr: ''
finding18 after: ['a.bundles']
finding18 is dir: True
```

The bytes the file held are gone, replaced by a run folder. The run never read them and never reported that it had removed anything.

**The defect.** `publish_folder` renames whatever stands at the run folder's path aside and then removes it, on the reading that only a run writes there. A symbolic link is renamed and unlinked as the link it is, which the contract states; a regular file under the same name is material no run wrote, and removing it destroys bytes the run never read.

**After the fix**, the path is held before anything is written:

```json
{"severity": "error", "message": "the output path '/tmp/…/out/a.bundles' holds a file, which is neither the run folder a run writes nor a link to one, so the bundles cannot be published without removing it", "code": "E_PUBLICATION_FAILED", "remedy": "remove or rename what stands there, or name another output folder"}
```

exit status 3, the file left byte-for-byte as it stood, and no staging folder beside it.

**What did not move.** Each was asserted in the same run:

| Standing at `<entry>.bundles` | Result |
| --- | --- |
| A regular file | refused, `E_PUBLICATION_FAILED`, file intact |
| A regular file, under `-c` | refused the same way, so a check run refuses what a publishing run does |
| A symbolic link, dangling | replaced as the link it is, run publishes — unchanged |
| A folder | the earlier set, swapped out — unchanged |

The check runs under `-c` because every other publication check does, and a check that accepted a path a publishing run refuses would give a verdict no run can act on.

## The case each finding ships with

`src/tests/test_cli.py` and `src/tests/test_derived_output.py`. Every case was run with the source repair stashed and the new cases in place, so the failure is the case's and not a fixture's.

| Case | Without the fix | With it |
| --- | --- | --- |
| `test_a_dispatch_in_an_absorbed_title_is_refused[⇉]` | fail — status 4, `E_UNEXPECTED_INTERNAL_ERROR` | pass |
| `test_a_dispatch_in_an_absorbed_title_is_refused[⫽]` | fail — status 4 | pass |
| `test_a_dispatch_in_an_absorbed_member_title_is_refused` | fail — status 4 | pass |
| `test_a_dispatch_in_a_title_above_the_selection_is_refused` | fail — status 0, the dispatch dropped and no target compiled | pass |
| `test_a_dispatch_in_the_entry_s_own_title_still_publishes` | pass | pass — the control |
| `test_a_file_at_the_run_folder_s_path_is_refused_and_left_untouched[False]` | fail — status 0, bytes destroyed | pass |
| `test_a_file_at_the_run_folder_s_path_is_refused_and_left_untouched[True]` | fail — status 0, bytes destroyed | pass |
| `test_the_file_refusal_leaves_no_staged_folder_beside_it` | fail — status 0 | pass |

The first stashed run, before the title-above-a-selection case was written, reported `6 failed, 1 passed`. The second, over the final set, reported `7 failed, 1 passed`, the pass being the control through both.

## Every check run

`make check` was run over the branch head twice under the sandbox with `PROSIFORM_BUILD` naming the worktree's own build. Each run exercised every target and completed with exit status 0 — in 231 seconds at the first head, and 230 seconds at the final head after the second repair. The figures below are the final run's.

| Target | Result |
| --- | --- |
| `lock-check` | pass |
| `lint` | pass, `All checks passed!` |
| `format-check` | pass, 203 files already formatted |
| `typecheck` | pass, no issues in 80 source files |
| `steps` | pass, runs ahead of `test` |
| `authoring` | pass, 0 findings |
| `test` | 1316 passed |
| `harness` | 992 passed — `checks/tests` and `evals/diagram-following` |
| `corpus` | 349 fixtures, 349 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `smoke` | pass, the installed command named on the path |
| `layout` | pass, 4 trees present |
| `tables` | pass |
| `links` | every reference in 237 documents resolved, except 18 whose host did not answer |
| `vocabulary` | pass, 44 contract terms |
| `invocation` | pass, 29 statements |
| `conformance` | 303 clauses, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere |
| `independence` | pass, every shaped term one the contract names |

The full suite was also run on its own: 1284 passed as cut, 1315 after the first repair's cases, and 1316 after the second repair's.

The brief expected `test_linked_bootstrap` to need network and the publication tests to fail under `/tmp`'s atomic folder swap. Neither failed here: the run above passed in full inside the sandbox, so no failure needed checking against a clean checkout of `origin/i07/e00/main`.

## No neighbouring behaviour moved

| Observation | Result |
| --- | --- |
| The codes the build reports | `CODES` is derived from each module's own tuple; no code was added, so `-C` is unchanged and conformance reports no disagreement in either direction |
| The fixture corpus | 349 fixtures pass unchanged; the refusal reuses a code five `fixtures/dispatch` constructs already reach |
| A published body dispatch | still places its sub-section and rewrites the link, `#dispatch-plan` included |
| A deferred link in a title | still rebases to the target's path |
| A symbolic link at the run folder | still replaced as the link it is, its target left as it was |
| An earlier set that cannot be removed | still publishes and warns with `W_EARLIER_SET_RETAINED` |
| The folder swap's rename order | unchanged; the check reads the path before the swap rather than inside it |
| Files changed | `src/prosiform/bundle.py`, `src/prosiform/cli.py`, `src/prosiform/grouping.py`, and the two test modules |
