# Change List — W08 Example Skill Scenarios Over the Mechanism

> Plan changes · Created 2026-10-31

Every change this session applied to the plan, and every one it held. "Applied" means the epic record, the reserved folder or the branch carries it; "held" means it was considered and not applied, with the reason.

## Applied

| Change | Where | Why |
| --- | --- | --- |
| The two scenarios are one check rather than a corpus fixture family. | Branch: `checks/mock_scenarios.py`, `Makefile` | `fixtures.md`'s first W08 defect: a `usage-example` fixture reaches its tree through a symbolic link, `execute` takes the resolved working directory, and `access.py` refuses a symbolic link in any traversed component, so a fixture cannot hold a substitute reaching the example tree. A run-time copy is the only form that keeps one tree and checks nothing in twice. |
| Both scenarios run with the output folder outside the trees they read, and both trees are fingerprinted either side. | Branch | `fixtures.md`'s second defect: `cmp` over the tree was wrong because the run wrote its bundle into the skill directory. A published write is now reported as a write. |
| The artifact stand-in is described by the heading it replaces — `## Epic`, a member of the merged `artifacts` group at depth 1 — rather than by "no criteria". | Branch, epic record `w08.md` | `fixtures.md`'s third defect: "no criteria" names nothing the artifact holds. The heading is what the group emits and what the substitution occupies. |
| The stand-in's expectation is the unmocked bundle the same tree produces, not bytes checked in beside it. | Branch | One tree is the source of truth, so material that moves moves both sides and only a difference the substitution makes can be red. |
| A stand-in's blocks are compared only under headings the unmocked bundle carries. | Branch | The mode's closure reaches `artifacts/epic.md` only through the sections its references name, so a stub section no reference reaches is material the run never asks for. Expecting every block was the first design's error, and this is the same fact seen from the bundle's side. |
| `make mock-scenarios` added, and `make check` names it after `steps`. | Branch: `Makefile`, `checks.md`, `checks/README.md` | The row's Test calls for the target, and `make tables` holds a declared target and a documented row to each other in both directions. |
| The check runs from the locked environment. | Branch: `Makefile` | It reads `runner.py` for the build seam and for diagnostic parsing, which the locked environment supplies, so it joins `corpus`, `invocation`, `conformance` and `independence` rather than the standard-library scripts. |
| `checks/README.md` gains the check's row and the paragraph stating why it is a check. | Branch | The table is the repository's own account of what each check asserts, and a check without a row is a name `make check` runs and nothing explains. |

## Held

| Change | Why it was held |
| --- | --- |
| A corpus fixture family under `fixtures/mock/` for these two scenarios. | Cannot be built: `fixtures.md`'s first W08 defect. Recorded there and in `w08.md`. |
| A copied `example/work-planner` under a fixture's `source/`. | Would work and is refused: a copy per fixture is the drift the symbolic link exists to prevent. |
| Bytes checked in beside each scenario as its expected bundle. | Two trees would then have to agree, which is the drift the run-time copy avoids. |
| A third scenario exercising the plan mode against a stubbed `guidelines.md`. | Outside this row's two criteria. The mechanism it would exercise is AC3's section key, held by a corpus fixture W06 lands. |
| Moving `make mock-scenarios` into `make harness`. | The harness runs `pytest` over the suites; this is a command with its own verdict, as `corpus` is, so it sits beside `corpus` rather than under `harness`. |

## Unplaced work

None. Both scenarios the row names are delivered, and the row covers its two criteria without a residual finding.

## Technical debt

None raised. The check reuses `runner.py`'s build seam and diagnostic parser, so it binds the build named by `PROSIFORM_BUILD` and asks diagnostics for `-d json` as the corpus does, and it introduces no second reading of either.
