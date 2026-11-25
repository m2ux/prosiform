# F38 Bundle Identifiers

> Hot-fix · Created 2026-11-25

Preset-qualified bundles expose their selected presets: **workflow-codex.bundle.md**, or **workflow-codex+recorded.bundle.md**. Names preserve canonical selection matching, safe escaping and atomic collision refusal.

Target: main. Reviewed head: [552230b962](https://github.com/m2ux/prosiform/commit/552230b96269ed26511a9652d16571d8aae07655). [F38 #848](https://github.com/m2ux/prosiform/issues/848) is delivered by [PR #849](https://github.com/m2ux/prosiform/pull/849). This is an unreleased change to pf 0.34.0. The initial implementation was recorded retrospectively; the final readable-name design follows the operator's subsequent review.

## Source And Bundles

- [Workflow source](named-specimen/source/workflow.md) and [child source](named-specimen/source/task.md)
- One preset: [entry bundle](named-specimen/one-preset/workflow-codex.bundles/workflow-codex.bundle.md) and [child bundle](named-specimen/one-preset/workflow-codex.bundles/task-codex.bundle.md)
- Two presets: [entry bundle](named-specimen/two-presets/workflow-codex%2Brecorded.bundles/workflow-codex%2Brecorded.bundle.md) and [child bundle](named-specimen/two-presets/workflow-codex%2Brecorded.bundles/task-codex.bundle.md)
- [Generated-file index](named-specimen/entries.json)

## Artifacts

| Artifact | Contents |
| --- | --- |
| [Issue](issue.md) | Confirmed naming contract and verified criteria |
| [Pull request](pull-request.md) | Review overview and observing checks |
| [Verification](test-results.md) | Method, results, source pins and limits |
| [Agent review](agent-review.json) | Exact-head review and criterion evidence |
| [Checklist](todo.md) and [final readback](delivery-readback.json) | Completed delivery steps and confirmed In Review state |
| [Final complete check](named-final-check.log) | Source, harness, corpus, wheel and repository checks |
| [Fixture audit](named-fixture-audit.json) and [audit script](fixture-diff-audit.py) | Exact naming-only transformation review |
| [Reviewed source diff](reviewed-source.diff) | Implementation, tests and specification changes |
| [Consumer validation](consumer-validation.md) | Private downstream compilation summary |
| [Earlier hash verification](hash-candidate-test-results.md) | Twelve- and eight-character checks at their original pins |
| [Earlier issue](eight-digit-issue.md), [PR](eight-digit-pull-request.md) and [README](eight-digit-README.md) | Superseded eight-character plan |
| [Earlier CI failure](eight-digit-ci-failure.log) | Missing README assertion, resolved by integrated F39 |
| [Initial focused run](named-initial-focused.log) and [initial complete run](named-initial-check-failures.log) | Retained URL-assertion failures |
| [Pre-integration complete check](named-pre-integration-check.log) | Passing readable-name check before F39 integration |
| [Earlier source tests](source-tests.log), [count](source-test-count.log), [corpus](corpus.log), [collision tests](collision-tests.log) and [types](types.log) | Twelve-character candidate evidence |
| [Eight-character source tests](eight-digit-source-tests.log), [corpus](eight-digit-corpus.log), [preset tests](eight-digit-preset-tests.log) and [types](eight-digit-types.log) | Eight-character candidate evidence |
