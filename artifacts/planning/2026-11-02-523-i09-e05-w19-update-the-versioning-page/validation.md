# Validation — I09:E05 W19–W21

Each page was read whole against the build at `main` 74b00cd9, which the task branch is cut from, and the design pinned at 4958ad38. Each section below lists every claim corrected or added and what showed it; a claim not listed was read and holds.

## T1 Versioning page read against the tags

**Observes:** AC20. **Page:** `docs/versioning.md`. **Read against:** `git tag -l` and `git ls-remote --tags origin` (`contract/v0.9.0`–`v0.15.0`, `python/v0.9.0`–`v0.15.0`), `git cat-file -p` of each tag, the `release/v0.10.0`–`v0.15.0` branches, `git log -- src/pyproject.toml`, and `uv run --frozen pf -v` in `src/`.

| Claim | Change | Evidence |
| --- | --- | --- |
| A build tag's example | Corrected to `python/v0.15.0`, the latest | `git tag -l` |
| What the contract tag covers | Corrected to the corpus the tagged commit holds and the design it encodes | The design lives on `engineering`; each tagged commit holds `fixtures/` |
| The build's declared version and `pf -v` | Added | `src/pyproject.toml` declares `0.16.0`; `pf -v` prints `pf 0.16.0 (skill-markdown-v4)`; `cli.py` reads `importlib.metadata.version` |
| `main` may report an untagged version | Added | 98763ec4 sets `0.16.0` on `main`; no `0.16.0` tag exists |
| Cutting a release | Added: release branch, declaring commit, number chosen by the previous corpus, paired annotated tags, merge back | From v0.10.0 on, both tags of each version peel to one commit `Declare Python build version X.Y.Z` on `release/vX.Y.Z`, changing `src/pyproject.toml` and `src/uv.lock` (`git ls-remote` `^{}` lines; v0.9.0's pair names a merge of `release/python-v0-9-0`); tag messages record the corpus count and the previous corpus's passes and failures; #350 merges `release/v0.15.0` into `main` |
| A published tag never moves | Added | The release practice the project follows; work merged after `v0.14.0` was tagged shipped as `v0.15.0`, one day later |
| Below 1.0.0, the minor carries the major | Added | `contract/v0.10.0`–`v0.13.0` and `v0.15.0` messages record previous-corpus failures "under the pre-1.0 version convention" with a minor bump; `contract/v0.14.0` records 0 failures and two fixtures added, also a minor bump |
| "a case that previously had no stated outcome" | Reworded to the present tense | Workspace rule on describing the design |

## T2 Fixtures README read against the schema and families

**Observes:** AC21. **Page:** `fixtures/README.md`. **Read against:** `fixtures/manifest.schema.json`, the 42 directories under `fixtures/` and their manifests' `clauses`, `checks/runner.py`, and the design's Adversarial acceptance fixtures and Metadata failures sections at 4958ad38.

| Claim | Change | Evidence |
| --- | --- | --- |
| The families are listed in the design | Replaced by a table of every family directory and what its fixtures exercise | `ls fixtures/`; the clauses each family's manifests name |
| Diagnostic fields | Added `location` with its `file`, `line` and `column` | Schema `$defs.diagnostic.properties.location` and `$defs.coordinate`; `checks/runner.py` `DECLARED_FIELDS` |
| Error catalogue | Added `E_SOURCE_ACCESS` | Schema `errorCode` enum; design Metadata failures table; `confinement/a-path-the-filesystem-cannot-open` |
| Consistency and parser exhaustion are named by no fixture | Replaced: every design family is named by a fixture | `source-consistency/a-source-that-changes-during-compilation` names Consistency; `parser-limit/` fixtures name Parser exhaustion and expect `E_PARSER_REFERENCE_LIMIT`; every one of the design's 29 families appears in some manifest's `clauses` |
| `make harness` | Added that it also holds the diagram-following eval | `Makefile` `harness` target runs `checks/tests` and `evals/diagram-following` |
| `composition/` | Linked to `docs/composition.md` | One home per rule |

Every other field row — `description`, `clauses`, `invocation.cwd`, `invocation.arguments`, `expected.exit_status`, `expected.bundles`, `expected.stdout_contains`, `expected.diagnostics`, `awaiting`, `fault` — matches its schema definition, and the four faults match the `fault` enum. The warning catalogue matches the schema's `warningCode` enum.

## T3 Eval page read against the harness

**Observes:** AC22. **Page:** `evals/diagram-following/README.md`. **Read against:** the `harness` and `eval-diagrams` targets of `Makefile`, `workflow.py`, `score.py`, `run.py`, `harness.py` and each `workflows/*/scenarios.toml`.

| Claim | Change | Evidence |
| --- | --- | --- |
| Scenario fields | Added a table of `name`, `inputs`, `path` and `trace` | `workflow.read_scenarios` reads exactly these keys |
| The Cursor CLI alone has no spend cap | Corrected: Cursor and opencode both | `harness.py` `Cursor.argv` and `Opencode.argv` docstrings: no session spend cap |
| Isolation mechanisms | Scoped to the Claude harness | Each flag in the table is `Claude.argv`'s; `Cursor` and `Opencode` carry their own |
| `run.py --harness` help and the Makefile comment | Corrected to name `opencode` (debt fixed in this unit) | `harness.HARNESSES` declares `claude`, `cursor`, `opencode` |

Held without change: the seven forms match `run.FORMS`; the eight path classes, their order, and `errored` match `score.Failure` and `score.score`; the three dispatch classes and their order match `score.dispatched`; the default options match `run.options`; the default matrix of 28 cells and 280 sessions matches the scenarios the seven non-bootstrap workflows declare.

## T4 make check

**Observes:** AC20, AC21, AC22, as the page's links, command tables and vocabulary hold. **Command:** `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` in the task worktree.

**Result:** passed, exit status 0, at e00470f9: lock, lint, format, typecheck, 1161 harness tests, the corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence. `make links tables vocabulary` passed again at cf215036, which adds the `composition/` link: every reference in 143 documents resolved.
