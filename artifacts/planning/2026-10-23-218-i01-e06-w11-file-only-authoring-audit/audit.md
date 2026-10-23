# File-Only Authoring Audit

Observed on the tree committed as `1b0de59cb5440f8f7a844d3019a63d408023d2e5` on `i01/e06/w11-file-only-authoring-audit`. `make check` exited 0 with `PROSIFORM_BUILD` set to this checkout's `pf`.

## Author instructions

`checks/tests/test_authoring.py` reads `invocation.md` and requires the file-owned contract: the `pf [OPTIONS] REF` synopsis, full `root`, `group` and `group-depth` keys, a file-relative explicit root, the working-directory default for an absent root, short `-f` and `-o` flags, fragment naming with `__`, and an explicit `-o` destination for distinct selections. Passed inside the harness run of `make check` (619 passed).

## Command examples

The same test reads every `pf` command in `invocation.md`, `README.md` and `example/README.md`. Each source path exists, no command passes `-r`, and output paths such as `-o context.md` are not required to exist beforehand. The worked commands are:

- `pf modes/plan-mode.md`, `pf 'artifacts/epic.md#delivery-findings'`, `pf -o context.md modes/plan-mode.md` and `pf -c modes/plan-mode.md` from `example/work-tracker`
- `pf -f artifacts/epic-issue-body.md '#record-epic-delivery'` from `example/work-tracker`
- `pf -o - procedure.md rules/common.md` from `example/my-skill`
- `pf -o skill-bundle.md example/my-skill/procedure.md example/my-skill/rules/common.md`, `pf example/work-tracker/modes/plan-mode.md` and `pf 'example/work-tracker/artifacts/epic.md#delivery-findings'` from the repository root

The plan-mode excerpt in `example/README.md` matches the source, including root-relative links. `example/work-tracker/SKILL.md` keeps `name`, `description` and `prosiform.root` in one frontmatter block. Passed in the same harness run.

## Root declarations

Every Markdown file under `example/` other than its README opens with frontmatter containing `prosiform`. A declared `root` is a non-empty relative directory path. Passed in the same harness run.

## Hyphen guidance

`invocation.md`, `README.md` and `example/README.md` each recommend hyphens rather than underscores in file and directory names. Example paths contain no underscore. `make invocation` reports the sentence among 28 statements held to the build. Passed.

## Authoring handoff

The [authoring handoff](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/authoring-handoff.md) already registers the requirements this audit teaches. Its goal states that an absent `prosiform.root` uses the invocation working directory, including linked files; that sources declare full `root`, `group` and `group-depth` keys; that explicit roots resolve relative to the declaring file; and that the command is `pf` with short operational flags. It also states that the skill advises hyphens rather than underscores and that combined selections supply an explicit output destination. No handoff edit was required.

Preserved end-to-end examples:

- The [baseline at 93fe6b3](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/e2e/runs/baseline-93fe6b3/README.md) ran three link invocations against a compiler that required `-r`. Each exited 2 with `E_INVALID_USAGE` and produced no bundle. That record demonstrates the gap. It is not a passing authoring example.
- The [installed-command inventory](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-i01-e06-w10-linked-skill-bootstrap-tests/e2e/runs/d8feaa7041e9d2eb58703faac91620ecae167596/inventory.md) at source `d8feaa7041e9d2eb58703faac91620ecae167596` retains successful file-only runs. Paths use hyphens (`pf-bootstrap-specimen`, `assemble.md`). A representative command is `pf -d json -o - ../skills/pf-bootstrap-specimen/modes/assemble.md`, exit 0, with a bundle saved beside it. Failed metadata and depth-conflict runs record that no bundle was produced.

## Pinned baseline

`make corpus` compared 253 fixtures with their pinned stdout. The runner requests that stdout with `-o -`, so the comparison is the bundle content and does not depend on the derived filename. 253 passed, 0 failed, 0 awaited, 0 unexpected pass.

## Full check

`make check` passed: lock, lint, format, mypy, 1038 pytest tests, 619 harness tests, corpus, smoke, layout, tables, links, vocabulary, invocation (28 statements), conformance and independence.

Smoke built and installed the wheel, resolved `pf` outside the repository, and bundled `guide.md`.

## Uncovered clauses

`make conformance` lists clauses no fixture declares. The listing is the report's measurement. The run passed: 296 clauses, 53 covered by no fixture, 0 declarations naming no clause, 16 clauses no run states, 3 sections stating no behaviour, 3 installation claims no run observes.

Uncovered clauses:

- Automatic output names
- Automatic output names — work-planner/modes/align-mode.md, root ".."
- Automatic output names — Same file, fragment prerequisites
- Automatic output names — work-planner/SKILL.md, root "."
- Automatic output names — work-planner/artifacts/epic.markdown, root ".."
- Automatic output names — work-planner/guide.md, root "../library"
- Automatic output names — Equivalent references guide.md and ./guide.md#, absent root
- Automatic output names — guide.md#one and guide.md#two
- Grouping — Consistent depth
- Conversion metadata — prosiform.root
- Conversion metadata — prosiform.group
- Conversion metadata — prosiform.group-depth
- Conversion metadata — YAML grammar
- Conversion metadata — Bounded parsing
- Conversion metadata — Source ownership
- Conversion metadata — Selection boundary
- Conversion metadata — Operational interface
- Metadata failures — E_INVALID_FRONTMATTER
- Metadata failures — E_INVALID_CONVERSION_METADATA
- Metadata failures — E_GROUP_DEPTH_CONFLICT
- Metadata failures — E_ROOT_NOT_FOUND
- Metadata failures — E_SOURCE_SYMLINK
- Metadata failures — E_SOURCE_OUTSIDE_ROOT
- Metadata failures — E_TARGET_NOT_FOUND
- Metadata failures — E_SOURCE_ACCESS
- Metadata failures — E_SOURCE_CHANGED
- Bounded bootstrap capture
- Resolution sequence — ../guide.md positionally
- Resolution sequence — A source link normalized outside its author's root
- Validation and failure contract — Safety
- Metadata conformance cases
- Metadata conformance cases — Per-file ownership
- Metadata conformance cases — Explicit grouping
- Metadata conformance cases — Stable selection
- Metadata conformance cases — Accepted YAML
- Metadata conformance cases — Rejected metadata
- Metadata conformance cases — Safe YAML
- Metadata conformance cases — Body separation
- Metadata conformance cases — Preserved assembly
- Metadata conformance cases — Atomic failure
- Metadata conformance cases — Public interface
- File-owned invocation conformance cases
- File-owned invocation conformance cases — Root defaults
- File-owned invocation conformance cases — Explicit roots
- File-owned invocation conformance cases — Shared identity
- File-owned invocation conformance cases — Root safety
- File-owned invocation conformance cases — Bootstrap limits
- File-owned invocation conformance cases — Self references
- File-owned invocation conformance cases — Multi-root identity
- File-owned invocation conformance cases — Derived filenames
- File-owned invocation conformance cases — Combined selection
- File-owned invocation conformance cases — Publication
- File-owned invocation conformance cases — Deferred handoff
