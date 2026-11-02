# W00 Validation

Each check the [work item](w00.md) names, run in the task worktree on branch `i08/e08/w00-the-example-tree-and`.

## Revision

- Tested head: `492bd87ecc544c74ff549e79a567d40a9ff201ac`, on `00f166920ec242f3565376e06a8838de72f8dc34` (epic base and `main`).
- Commits: `0ea712270` removes the tree, the `usage-example` fixtures and the drawings of `example/my-skill`; `09eef2d72` removes the checks, tests and targets reading the tree; `492bd87ec` repoints the documents at corpus fixtures.

## T1 Search

`git grep -n -i -E "example/|usage-example|example tree|work-planner example|my-skill|mock-scenarios|make (steps|authoring|boundary)" HEAD` returns three lines, each the host `t.example` in a kanban ticket URL of `src/tests/test_profile.py` or `src/tests/test_source.py`; none names the tree. `git ls-tree -r --name-only HEAD` lists no path under `example/` or `fixtures/usage-example/`. The drawings `docs/images/compilation.*` and `docs/images/agent-rules.*` are removed. `scripts/examples.json` holds no case reading the tree: each case writes its sources inline.

Result: ✓

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exits 0: lock, lint, format, type checks, 1586 build tests, 1076 harness tests, the corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass.

- Independence reported `Release` in `inclusion/a-dependencys-preset-comes-from-itself` once the example headings stopped being admitted; the fixture's description now quotes the title it selects by as a code span.
- Conformance reports the design's `Usage examples` clause covered by no fixture, since the `usage-example` family was its only coverage; an uncovered clause is reported and does not fail the check. It is raised as an arising issue, because the design names the specimen tree the clause runs against.

Result: ✓

## T3 Archive Tag

- `git cat-file -t archive/example-work-planner` prints `tag`: the tag is annotated.
- `git rev-parse archive/example-work-planner^{commit}` prints `00f166920ec242f3565376e06a8838de72f8dc34`.
- `git log --diff-filter=D -1 --format=%H -- example/work-planner/SKILL.md` prints `0ea712270792005634e276f08b11d3fa4a543a7a`, and `git rev-parse 0ea712270^` prints `00f166920ec242f3565376e06a8838de72f8dc34`, the tag's commit.
- `git show archive/example-work-planner:example/work-planner/SKILL.md` prints the skill's frontmatter and body.
- `git ls-remote --tags origin archive/example-work-planner` lists the tag on the remote.

Result: ✓
