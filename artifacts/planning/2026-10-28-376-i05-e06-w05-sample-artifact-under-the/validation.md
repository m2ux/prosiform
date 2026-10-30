# Validation — I05:E06 W05

Run on branch `i05/e06/w05-sample-artifact-under-the` at `bda07166`, cut from `i05/e06/main` at `8440ab31`, with `PROSIFORM_BUILD` set to `uv run --project <worktree>/src --frozen pf`.

## T1 Authoring Check

`make authoring`, counts for `example/work-planner/artifacts/placement.md` by kind. Observes AC5.

| Kind | Before (`8440ab31`) | After (`bda07166`) |
| --- | --- | --- |
| Inputs and Outputs | 10 | 0 |
| Commands section | 1 | 0 |
| Command placement | 2 | 0 |
| File-relative links | 0 | 0 |

The whole example falls from 431 to 418 findings, the 13 the file carried. Pass for the file; the target still exits nonzero for the files W06–W08 convert.

## T2 Inspection

`placement.md` read against each rule of `example/work-planner/guidelines.md`:

- **Operation names.**  Five `###` operations, verb first, no emphasis.
- **Title headings.**  One H1, `# Placement`.
- **Steps.**  Every multi-step operation writes `#### N. Action` sub-sections.
- **Inputs and Outputs.**  Each operation carries one **Inputs:** and one **Outputs:** paragraph of contract links.
- **Contracts.**  Every linked value has a `###` contract under Fields, or another file's Fields or Template; no contract says who supplies or uses a value.
- **Commands in steps.**  The orphans helper runs in Find Placement Candidates step 1, unindented, with its labelled example; step 2 reads its exit code and output. No Commands section.
- **Bindings.**  Theme labels link Configuration; no binding is stated in the file.
- **Conventions.**  The helper step links Helper invocation; the comment-file step links Bodies.
- **One home per rule.**  The disposition rule is stated once, in Disposition.
- **File-relative links.**  Every cross-file link is relative to the file.
- **One subject per file.**  One subject, placement; 9,962 bytes and five operations, under both review limits.
- **Result.**  Pass.

## T3 Anchor Sweep

Every usage example run from `example/work-planner` with `pf -o <scratch> <entry>`: hoist, revise, advance and plan modes, the bare fragment and the two selected sections. Only the hoist entry's two bundles changed, and were copied into `artifacts-and-references-under-declared-groups/expected/`. The sweep over all 15 regenerated bundles reports `unresolved links: 0` and 0 suffixed step anchors. Pass.

## T4 Steps

`make steps`: `step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections`. Pass.

## T5 Links

`make links`: `link check: every reference in 107 document(s) resolved`. Pass.

## T6 Corpus

`make corpus`: `corpus check: 342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass`. Pass.

## T7 Repository Checks

`make check` exited 0: ruff `All checks passed!`, format `69 files already formatted`, mypy `no issues found in 68 source files`, tests `1302 passed`, harness `758 passed`, corpus 342 pass, links and steps passing. Pass.
