# Name the Build Tree `src`

A repository-structure change. Not a task row, no acceptance criterion.

The implementation tree is named for the slot it occupies rather than for the
language or the delivery stage that fills it. A later build substitutes into
`src/` without the Makefile, the workflow, the checks or the READMEs changing.
Planning artifacts on `engineering` keep the word *prototype*, where it
describes a stage rather than a directory.

## What Moved

`git mv prototype src`, history preserved. The packaging root sits at the same
place relative to the tree, so `pyproject.toml` needed no edit and
`[tool.hatch.build.targets.wheel] packages = ["src/prosiform"]` still resolves;
the package path from the repository root is now `src/src/prosiform/`.

| Branch | Tracked files under the tree |
| --- | --- |
| `main` | 15 |
| `i00/e04/main` | 19 — the four the epic adds: `access.py`, `closure.py`, `test_access.py`, `test_closure.py` |
| `i00/e07/main` | 15 |

## Path References Updated

| File | What |
| --- | --- |
| `Makefile` | `UV_RUN`, `TOOL_CONFIG`, `PYTHON_SOURCES`, the `test` and `lock-check` recipes, and the header comment naming the lockfile |
| `.github/workflows/checks.yml` | `PROSIFORM_BUILD` and the lockfile note on the uv install step |
| `checks/tables.py` | `PYPROJECT`, the module docstring, and the four failure messages that name the file |
| `checks/layout.py` | the `REQUIRED_TREES` key |
| `checks/smoke.py` (E07 only) | `PROJECT`, and the two docstring references |
| `README.md` | layout table, `make tables` row, lockfile sentence, `PROSIFORM_BUILD` example, `pip install`, `cd` |
| `checks/README.md` | the `tables.py` row and the `smoke.py` paragraph (E07) |
| `src/README.md` | the `cd` in the environment block |

## Prose Judged Rather Than Substituted

Changed, because it labelled the build provisional or encoded the language in
a structural assertion:

- `checks/layout.py` — the tree's purpose reads "the build", not "the Python
  build". A layout assertion should survive a substitution into the slot.
- `checks/README.md` — the `layout.py` row follows: "one for the build".
- `fixtures/README.md` — "the Python prototype and the production build" becomes
  "the Python build and the production build"; "the first epic of the prototype
  initiative" becomes "the first epic of the first initiative".
- `README.md`, I02 row — "with the prototype retained as its differential
  oracle" becomes "with the Python build retained as its differential oracle".
- `src/README.md` title — `# Prototype` becomes `# Source`, matching the
  one-word titles the other tree READMEs carry (Fixtures, Checks,
  Documentation).
- `checks/tests/test_runner.py` — `"prototype"` leaves `IMPLEMENTATION_NAMES`.
  The guard holds `runner.py` to naming no build; the tree's path is already
  covered by the list's `"src/prosiform"`, and a bare `"src"` would match the
  word "source" in any ordinary sentence.
- `checks/tests/test_manifest_schema.py` — the arbitrary value proving an
  unknown field is rejected reads `"src"`.

Left as written, because each states a fact about the build that exists today
rather than labelling the slot:

- `README.md` layout table: "The Python build: the contract's first
  implementation, retained as a differential oracle."
- `README.md` installation: "prosiform installs from the Python build in
  `src/`".
- `src/README.md`: "The Python build of prosiform."
- Every mention of Python version, Python tooling, or the Python toolchain in
  the Makefile, the workflow and the dependency tables.

Left alone and reported:

- `README.md` status table, I00 row — `I00 Prototype`, linking issue #2, whose
  title is "[I00] Prototype Compiler: The Contract Proven in Python". That is a
  planning object named by its own title. Renaming the link text would make the
  README misname the issue, and renaming the issue is planning work this change
  does not own.

## Branches

| Branch | Commit | `git ls-files prototype` |
| --- | --- | --- |
| `main` | `15ff22f`, merge of PR #78 from `chore/name-the-build-tree-src` (`10c7493`) | empty |
| `i00/e04/main` | `f51e722`, merge of `main` | empty |
| `i00/e07/main` | `4cff587`, merge of `main` | empty |

### Stragglers

E04's base carried four files `main` had never seen. Git's rename detection
flagged each as a file-location conflict and staged it at the new path
unmerged; resolving was `git add` at `src/`, not a hand move. The four:
`src/src/prosiform/access.py`, `src/src/prosiform/closure.py`,
`src/tests/test_access.py`, `src/tests/test_closure.py`.

E07 carried `checks/smoke.py` and the `make smoke` target, which `main` has
never seen, so the merge left three `prototype` references inside them and one
content conflict in `README.md` where both sides rewrote the same sentence.
Resolved by keeping E07's smoke wording on `main`'s renamed paths.

## Fixture Counts

| Branch | Before | After |
| --- | --- | --- |
| `main` | 67 — 65 pass, 2 awaited | 67 — 65 pass, 2 awaited |
| `i00/e04/main` | 96 — 94 pass, 2 awaited | 96 — 94 pass, 2 awaited |
| `i00/e07/main` | 40 — 38 pass, 2 awaited | 67 — 65 pass, 2 awaited |

E07's base predates `main`'s current corpus, so merging `main` brings `main`'s
fixtures with it. No fixture was lost: the 40 E07 carried are a subset of the
67, and the awaited pair is unchanged.

`make check` passes whole on all three. On E07 that is twelve targets, `smoke`
among them, and the wheel installs and bundles from outside the repository, so
the packaging root survived the rename.

## Not Touched

- `artifacts/planning/2026-10-17-prosiform-v1/design.md` and everything else
  under `artifacts/planning/`. Nothing in the rename called for an edit there.
- The package name `prosiform`, the module names, the profile identifier
  `skill-markdown-v1`, the console entry point.
- Issue bodies, epics, initiatives, board items.
