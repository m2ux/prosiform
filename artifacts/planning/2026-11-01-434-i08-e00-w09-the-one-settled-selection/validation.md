# Validation — I08:E00 W09

Evidence for each check the [work item](w09.md) names, run in the task worktree on branch `i08/e00/w09-the-one-settled-selection` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 corpus

`make corpus` at `3a3364ab`: `inclusion/every-stage-reads-one-selection: pass`; `corpus check: 387 fixture(s), 387 pass, 0 fail, 0 awaited, 0 unexpected pass`.

The fixture runs `pf guide.md#keep` over a tree whose unselected `## Draft` carries a link to a declaring `outside.md`, a dispatch of a declaring `helper.md`, a deferral of `archive.md#missing`, a deferral of the absent `ledger.md` and raw HTML. It exits `0`, writes `guide__keep.bundle.md` alone holding `Keep` and `Rules`, and reports no diagnostic. The same tree entered whole (`pf guide.md`) fails with `E_RAW_HTML`, so the unselected content is live material the selection alone excludes.

## T2 reader mutations

Each reader of the settled selection in `src/prosiform/cli.py` was changed in turn to read its document whole, and the fixture's run observed. Each mutation was reverted; no source file changed on the branch.

| Reader | Mutation | Observed | Fixture |
| --- | --- | --- | --- |
| Discovery (`required`) | regions of the whole document | exit 0, bundle carries `# Outside` | fails (bytes) |
| Operator refusals (`refusals_of_operators`) | regions of the whole document | exit 1, `E_TARGET_NOT_FOUND` naming `ledger.md` | fails (exit, diagnostic) |
| Withheld-target check (`withheld`) | regions of the whole document | exit 1, `E_TARGET_NOT_FOUND`, `archive.md#missing` names no heading | fails (exit, diagnostic) |
| Dispatch placement (`dispatches`) | regions of the whole document | exit 0, run folder also holds `helper.bundle.md` | fails (extra bundle) |
| Candidate validation (`refusals` over selected regions) | refusals over every token | exit 1, `E_RAW_HTML` | fails (exit, diagnostic) |
| Emission (`group` selection) | no selection | exit 4, internal error on `outside.md` | fails (exit) |

Placement order (`placed`) reads the selection only to order documents already selected, and its mutation leaves the run unchanged; it decides no content and no refusal, so AC16 does not reach it.

## T3 conformance

`make conformance`: `0 declaration(s) naming no clause`; the fixture's six clauses are clauses the pinned design states.

## T4 make check

`make check` at `3a3364ab`: every target passed — `1410 passed`, `1072 passed`, authoring 0 findings, boundary 0 links outside their boundary, corpus 387/387, conformance and independence clean, mock scenarios 5/5.
