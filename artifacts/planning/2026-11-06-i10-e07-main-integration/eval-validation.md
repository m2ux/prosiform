# E04/E07 evaluation caller integration

The E07 epic-base checkout merges E04 main `d8265c82e797355a55cf7ec7d921949b4d7eb6c0` into `6578295a1bd40899ab4286a8185203451e159554`. This evidence describes the uncommitted integration tree. The coordinator owns final merged-base checks, the merge commit, push and tracker publication.

## Expected runs and callers

`Compile` names one optional entry and a normalized set of requested preset names, plus the trace owner. A run with no entry is the bare guide invocation. Its command words use `--entry` and optional `--presets`; shell serialization quotes each word. Effective selection uses the shared metadata/tag matching helpers, silently discarding unknown names and implicit default. Named output expectations hash the matching declared spellings under the contract's naming rule. Source-walk expected runs compare effective selections, so equivalent request order, case, duplication and unmatched names agree.

MarkdownIt readers retain each link's decoded title separately from the destination. Deferred activation carries that selection to the real compiler subprocess from the workflow form's directory. Fragment readers keep titles outside the href. The preset-deferral source explicitly requests `mirror`; the real bundle walk reaches Restore, while a mutation removing the substitution reaches Serve. A second expected request containing UNKNOWN, MIRROR, mirror and default identifies the same compile.

The scorer uses the compiler's grammar and entry-reference reader. Positional, repeated, abbreviated, missing-value, complete-link and obsolete-option invocations satisfy no compile. Informational help/version/code calls satisfy neither a compile nor a bare guide run. Missing and different matching presets fail. Unknown/default tokens and equivalent case/order requests match the same effective selection. Quoted shell separators and attached leading-dash values retain their meaning.

E04's `nested_commands` capability remains independent of `nested_starts`. Active deterministic traces and six scenario manifests use the command specification; prior paid-run records are untouched.

## Scope

Only these evaluation files are edited by the component contributor:

- `evals/diagram-following/README.md`
- `evals/diagram-following/workflow.py`
- `evals/diagram-following/score.py`
- `evals/diagram-following/stub_agent.py`
- `evals/diagram-following/test_workflow.py`
- `evals/diagram-following/test_score.py`
- `evals/diagram-following/test_harness.py`
- `evals/diagram-following/test_run.py`
- `evals/diagram-following/workflows/bootstrap-audit/scenarios.toml`
- `evals/diagram-following/workflows/deferred-composition/scenarios.toml`
- `evals/diagram-following/workflows/deferred-dispatch/scenarios.toml`
- `evals/diagram-following/workflows/inline-bootstrap/scenarios.toml`
- `evals/diagram-following/workflows/preset-deferral/scenarios.toml`
- `evals/diagram-following/workflows/preset-deferral/compiled/states/mirror.md`
- `evals/diagram-following/workflows/subagent-first-run/scenarios.toml`

The coordinator separately owns the source title-publication repair in composition/provenance/candidate and its focused tests. This is recorded Folded work. W08 retains dedicated deferred corpus/parity acceptance; W09 retains dedicated tagged workflows and dispatch-variant expectations.

## Observing checks

All commands run from `.worktrees/i10/e07/main`; no paid session runs.

- `make harness`: **1627 passed** in 101.65s ([log](harness-final.log)).
- Focused preset-deferral and compiled-scenario replay: **23 passed** ([log](preset-deferral.log)); exercises actual compiler output and workflow paths.
- Real caller and decoded title readers: **2 passed** ([log](caller-reader.log)).
- Manifest schema and nested trace replay: **10 passed** ([log](manifest-traces.log)).
- Explicit-option diagnostics: **4 passed** ([log](diagnostics.log)).
- Scorer: **135 passed** ([log](scorer.log)); includes missing/wrong/equivalent presets, malformed grammar and informational commands.
- `make typecheck`: **90 files pass** ([log](typecheck.log)).
- `uv run --project src --frozen ruff check --config src/pyproject.toml evals/diagram-following`: passes ([log](lint.log)).
- `uv run --project src --frozen ruff format --check --config src/pyproject.toml evals/diagram-following`: passes.
- `git diff --check`: passes.

The initial full harness result, **1617 passed / 7 failed**, is retained in [harness.log](harness.log). Five failures were caller migration details: scenario-injection tests placed the compiler table before a trace action, and a nested stub trace expected unquoted positional command words. The corrected tests preserve the trace action and assert the actual shell-quoted single-entry command. Two failures exposed deferred title omission in generated source; the coordinator repaired the publication and candidate-validation path. The source-driven replay passes without weakening the expected Restore/Serve paths.
