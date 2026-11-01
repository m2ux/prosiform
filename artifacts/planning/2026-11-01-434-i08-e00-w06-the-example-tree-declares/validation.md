# Validation

Evidence for each check the [work item](w06.md) names, run in the unit's worktree at 591b42cb with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Authoring

`make authoring`: 59 documents under `example/work-planner/`, 0 findings. The Declaration column reads 0 in modes, protocols, artifacts, references and the entry files (AC11).

## T2 Declaration tests

`make harness`: 1070 passed. The six `test_authoring_check.py` declaration tests pass: no front matter and front matter without `prosiform` are findings at line 1, an empty `prosiform: {}` beside `name` declares, a `root` key is a finding at its line in block and flow form, a `root` key outside the `prosiform` block is not read, and a file-relative link is no finding (AC11).

## T3 Corpus

`make corpus`: 385 fixtures pass, 0 fail. No file under `fixtures/` changed, so every `usage-example/` expected bundle is the one the tree published before.

## T4 Full check

`make check` exits 0 at 591b42cb before opening; the epic base held no newer commit before merging, CI on 591b42cb passes, and #501 merged into `i08/e00/main` as a5a33116.
