# I06 Skill Distribution — October 2026

> Initiative planning · Created 2026-10-29

## Executive Summary

The work-planner skill is published in two places and neither copy is whole. The workspace holds the program behind older documents; prosiform holds the current documents and no program, so thirty-seven command lines in the published example cite a script path that exists only in a workspace checkout. This initiative makes one tree of them, on a `skills` orphan branch in prosiform, and points both users at that tree.

The layout is fixed by two facts rather than chosen. The skill's own procedures cite `../../guidelines.md` from a mode and `skills/scripts/check_skill_files.py` from a workspace root, so the branch root mirrors the workspace's `skills/` folder rather than rooting at `work-planner/`. And the fixture reader takes its corpus root from the repository holding it, so a branch that is to prove its own documents carries the harness that decides a fixture.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | The branch root layout and the documents' move |
| [W02 work item](w02.md) | The scripts and the tests covering them |
| [W03 work item](w03.md) | The citations re-rooted and the section contracts declared |
| [W04 work item](w04.md) | The fixture harness moved to the branch |
| [W05 work item](w05.md) | The fixtures re-rooted beside the tree |
| [W06 work item](w06.md) | The branch's own corpus command |
| [W07 work item](w07.md) | Main dropping the tree and its fixtures |
| [W08 work item](w08.md) | The local fixture replacing the family's unique coverage |
| [W09 work item](w09.md) | The workspace submodule |
| [W10 work item](w10.md) | The live session through the linked skill |

## Design

### The branch root

The root mirrors the workspace's `skills/` folder, which is the shape the procedures already cite.

```text
skills (orphan branch)
├── guidelines.md                  the shared skill guidelines
├── structure.json                 the section contracts the shared check reads
├── scripts/check_skill_files.py   the check Revise mode runs
├── work-planner/                  the skill: entry, modes, protocols, artifacts, references
│   ├── scripts/                   the twelve scripts the procedures run
│   └── test/                      the modules covering them
├── fixtures/                      manifest.schema.json and the usage-example family
├── checks/                        the modules that decide a fixture
└── artifacts/planning/            this record
```

### Why the root is not `work-planner/`

A mode cites `../../guidelines.md`, which reaches the workspace root from `skills/work-planner/modes/`. Rooting the branch at `work-planner/` would put the shared guidelines outside the branch, which is the defect being fixed. The root therefore sits one level above the skill, exactly where the citation already points.

### Why the harness travels

`checks/manifests.py` resolves its corpus as `ROOT / "fixtures"`, with `ROOT` taken from the module's own location. Fixtures standing on a branch with no harness are read by no command, so the manifest reader, the fixture runner and the corpus walker move with the family. The branch holds no compiler, so a run names the build `PROSIFORM_BUILD` supplies and fails without one.

### Corpus coverage on main

Every clause the seven usage-example fixtures declare was counted against the rest of the corpus. Thirteen carry a fixture elsewhere; two do not.

| Clause | Fixtures outside the family | Resolution |
| --- | --- | --- |
| `Input and output contract — Entry references` | 0 | A local fixture's own small tree declares it |
| `Usage examples` | 0 | Retired with the tree; it is a rule about a published example main no longer holds |
| `Link classification — The deferral mark` | 4 | Covered |
| `Link classification — A deferred link's destination` | 4 | Covered |
| `Link classification — Outside the root` | 9 | Covered |
| `Link classification — The dispatch operator` | 11 | Covered |
| `Grouping — Group membership`, `structure`, `naming`, `verbatim names`, `a heading for every member` | 3–10 | Covered |
| `Input and output contract — Whole documents`, `Sections` | 8, and more | Covered |
| `Section extraction — Boundary` | 7 | Covered |
| `Compile before publishing — step 4` | 6 | Covered |
| `Validation scope`, `Grouping — The parent arrangement`, `CLI contract — -c`, `CLI contract — -f DOC` | 6–7 | Covered |

## Decisions

- **The initiative is new, not an epic of I05.** I05's goal is bundling enhancements proven by end-to-end fixtures, and a branch restructure serves none of its criteria. The work stands as I06 with its own goal and criteria. (User, 2026-10-29.)
- **An orphan branch, not a directory on main.** The skill is material the project publishes, so it takes a branch of the project as the planning record does, and main keeps only what reaches it. (User, 2026-10-29.)
- **The example is the source of the documents; the workspace copy is the source of the program.** The example's documents are the current ones, and the workspace copy's scripts are the only ones there are. (User, 2026-10-29.)
- **Every script the skill itself needs migrates; auxiliary test scripts may be deferred.** The tests covering a migrated script travel with it, because a suite left behind stops running. (User, 2026-10-29.)
- **Local fixtures on main replace the family, not a copy of the example.** The corpus's one leaving link is removed in favour of a fixture whose own tree is inside it. (User, 2026-10-29.)
- **The `Usage examples` clause is retired.** With the example leaving main, the rule has no subject there, so its clause and fixtures go rather than leaving a rule reading as covered on nothing. (User, 2026-10-29.)
- **Entry references is refixtured locally.** It is the one clause the family uniquely proves that main still needs, so a fixture with its own multi-entry tree carries it. (User, 2026-10-29.)
- **Priority 9.** The work blocks no other initiative and is blocked by none; it leads its theme so the divergence stops growing. (Planning, 2026-10-29.)

## Component Map

| Row | Component | Further paths written |
| --- | --- | --- |
| W01 | `work-planner/` on the `skills` branch | `guidelines.md`, `artifacts/planning/` |
| W02 | `work-planner/scripts/` | `work-planner/test/` |
| W03 | `work-planner/SKILL.md` | `structure.json`, every document carrying a citation |
| W04 | `fixtures/` on the `skills` branch | `checks/manifests.py`, `checks/runner.py`, `checks/corpus.py`, `fixtures/manifest.schema.json` |
| W05 | `fixtures/usage-example/` | each `source` link and its expected bundles |
| W06 | `Makefile` on the `skills` branch | `README.md` |
| W07 | `example/work-planner` (removed) | `fixtures/usage-example/` (removed), `README.md`, `invocation.md`, `example/README.md`, `fixtures/README.md` |
| W08 | `fixtures/entry-references/` | its source tree and expected bundle |
| W09 | `skills/` in the workspace | `.gitmodules`, `.gitignore` |
| W10 | `skills/` in the workspace | this record |

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I06](https://github.com/m2ux/prosiform/issues/405) |
| E00 Skill Tree | [E00](https://github.com/m2ux/prosiform/issues/406) |
| E01 Fixture Carriage | [E01](https://github.com/m2ux/prosiform/issues/407) |
| E02 One Tree | [E02](https://github.com/m2ux/prosiform/issues/408) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
