# Validation — I01:E00 W01

Tested revision: `8816903dcc92cf86f47f47f9c22a222c8a7bb4b3` on `i01/e00/w01-ledger-format-and-triage`, cut from `i01/e00/main` at `6554db86`. Every command ran from the task worktree's root.

## Decisions

- **Format.** One TOML file per entry under `ledger/entries/`, validated by JSON Schema through `jsonschema`. The fixture manifests already take this reading (`checks/manifests.py`), so the check adds no dependency and one revision of `main` carries the entries, the schemas and the check.
- **Two schemas.** `ledger/entry.schema.json` and `ledger/exposure.schema.json`, each a document of its own, so the run-record task extends one without touching the other.
- **Room for runs.** An entry takes an optional `run` naming a run record; the run record's own schema, sizes and acted-on field are the run-record task's.
- **Working directory.** `invocation.cwd` is relative to the checkout of the first listed source.
- **Workspace half.** Every `SKILL.md` on `m2ux/workflow-server` branch `workspace` under `skills/`: `server-in-the-loop`, `work-planner`, `workflow-canon`, and the six `gitnexus-*` skills. Named by repository, branch and path; nothing copied in.
- **Example half held to the example.** The check fails when a file under `example/work-planner/modes/` is named by no declared command, or a command names no file, so a mode added later is declared where it lands.

## T1 Entry fields

`checks/tests/test_ledger.py`, run by `make harness`. A complete entry is accepted, and one citing a run. Each required field removed in turn is rejected naming that field: `date`, `invocation`, `invocation.command`, `invocation.cwd`, `sources`, `sources.0.repository`, `sources.0.revision`, `sources.0.path`, `observed`, `expected`, `triage`, `triage.state`, `triage.reason`. An empty `sources`, an abbreviated revision and a command other than `pf` are rejected.

Result: all cases passed (35 passed in the file).

## T2 Triage states

Same file. Each of `design change`, `corpus gap`, `build defect` and `no change` is accepted; a missing state (T1), an unknown state `wont fix`, and a reason that is empty or whitespace are rejected naming `triage.state` or `triage.reason`.

Result: all cases passed.

## T3 Exposure set

Same file. The recorded `ledger/exposure.toml` is accepted. Removing either half, or emptying it, is rejected naming that half. Dropping one example mode entry is rejected naming the omitted mode file; naming an absent entry is rejected.

Result: all cases passed. The recorded set names the ten files under `example/work-planner/modes/`, each as `pf modes/<mode>.md` from `example/work-planner`, as `example/README.md` documents, and nine workspace skills.

## T4 Recorded and empty ledger

Same file. `ledger.check()` over the repository is accepted; an empty entries directory with the recorded exposure set is accepted; an entry file departing from the schema is reported under its file name.

Result: all cases passed. `make ledger`: `ledger check: 0 entry file(s) and the exposure set match their schemas`.

## T5 make check

`PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf" make check` exited 0: build suite 1142 passed, harness 689 passed, corpus 282 of 282, smoke, layout, tables (17 commands), links (108 documents, `ledger/README.md` among them), vocabulary, invocation, conformance, independence and ledger all passed.

## Review

The README's sample entry was reproduced from its fields alone: from `example/work-planner`, `pf -o - modes/plan-mode.md` wrote the plan mode's bundle, opening `# Plan Mode`.
