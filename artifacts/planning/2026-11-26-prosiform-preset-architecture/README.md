# Preset Configuration — November 2026

> Feature plan · Created 2026-11-26

## Executive Summary

The confirmed goal is inspectable effective configuration, explicit pure settings reuse and local independent component and test choices, each form accepted from specimen files before its contract is written. The plan has four epics and twenty tasks, ordered specimens, ledger, imports, choices, with priorities 4, 3, 2 and 1 and two capability lanes.

The fixed 0.36.0 source and bundle baseline, generic valid and refused controls, complete-name, origin and scope constraints and a bounded changed-pick checkpoint keep new syntax separate from existing behavior. Runtime profiles, structured effort descriptors and reviewer presets remain deferred. The bundler features are planned; implementation has not started.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [decisions.md](decisions.md) | Rulings, the lane map, joins and conventions |
| [design.md](design.md) | Proposed forms, the design link rule and open design points |
| [draft-metadata.json](draft-metadata.json) | Identities, priorities, lanes and task counts |
| [e00/w00.md](e00/w00.md) | Task work item and its declared files |
| [e00/w01.md](e00/w01.md) | Task work item and its declared files |
| [e00/w02.md](e00/w02.md) | Task work item and its declared files |
| [e00/w03.md](e00/w03.md) | Task work item and its declared files |
| [e00/w04.md](e00/w04.md) | Task work item and its declared files |
| [e00-body.md](e00-body.md) | Design-specimen scope and five tasks |
| [e01/w00.md](e01/w00.md) | Task work item and its declared files |
| [e01/w01.md](e01/w01.md) | Task work item and its declared files |
| [e01/w02.md](e01/w02.md) | Task work item and its declared files |
| [e01/w03.md](e01/w03.md) | Task work item and its declared files |
| [e01/w04.md](e01/w04.md) | Task work item and its declared files |
| [e01-body.md](e01-body.md) | Build-ledger scope and five tasks |
| [e02/w00.md](e02/w00.md) | Task work item and its declared files |
| [e02/w01.md](e02/w01.md) | Task work item and its declared files |
| [e02/w02.md](e02/w02.md) | Task work item and its declared files |
| [e02/w03.md](e02/w03.md) | Task work item and its declared files |
| [e02-body.md](e02-body.md) | Pure-import scope and four tasks |
| [e03/w00.md](e03/w00.md) | Task work item and its declared files |
| [e03/w01.md](e03/w01.md) | Task work item and its declared files |
| [e03/w02.md](e03/w02.md) | Task work item and its declared files |
| [e03/w03.md](e03/w03.md) | Task work item and its declared files |
| [e03/w04.md](e03/w04.md) | Task work item and its declared files |
| [e03/w05.md](e03/w05.md) | Task work item and its declared files |
| [e03-body.md](e03-body.md) | Local-choice scope and six tasks |
| [goal-trace.md](goal-trace.md) | Goal coverage and the findings of each review |
| [initiative-body.md](initiative-body.md) | Initiative criteria and epic links |
| [publication.json](publication.json) | Published identities, priorities and lanes |
| [scope.md](scope.md) | Confirmed goal clauses and excluded work |
| [specimen-matrix.md](specimen-matrix.md) | Executed controls, specimen sets and the deterministic matrix |
| [specimens/baseline.json](specimens/baseline.json) | The release, revision and bundle hashes of the five controls |
| [specimens/conflicting-components/alpha.md](specimens/conflicting-components/alpha.md) | Generic source of this control |
| [specimens/conflicting-components/beta.md](specimens/conflicting-components/beta.md) | Generic source of this control |
| [specimens/conflicting-components/component.md](specimens/conflicting-components/component.md) | Generic source of this control |
| [specimens/conflicting-components/diagnostics.txt](specimens/conflicting-components/diagnostics.txt) | Diagnostics the 0.36.0 release wrote for this control |
| [specimens/conflicting-components/entry.md](specimens/conflicting-components/entry.md) | Generic source of this control |
| [specimens/conflicting-components/large.md](specimens/conflicting-components/large.md) | Generic source of this control |
| [specimens/conflicting-components/small.md](specimens/conflicting-components/small.md) | Generic source of this control |
| [specimens/conflicting-components/test.md](specimens/conflicting-components/test.md) | Generic source of this control |
| [specimens/conflicting-components/worker.md](specimens/conflicting-components/worker.md) | Generic source of this control |
| [specimens/conflicting-tests/alpha.md](specimens/conflicting-tests/alpha.md) | Generic source of this control |
| [specimens/conflicting-tests/beta.md](specimens/conflicting-tests/beta.md) | Generic source of this control |
| [specimens/conflicting-tests/component.md](specimens/conflicting-tests/component.md) | Generic source of this control |
| [specimens/conflicting-tests/diagnostics.txt](specimens/conflicting-tests/diagnostics.txt) | Diagnostics the 0.36.0 release wrote for this control |
| [specimens/conflicting-tests/entry.md](specimens/conflicting-tests/entry.md) | Generic source of this control |
| [specimens/conflicting-tests/large.md](specimens/conflicting-tests/large.md) | Generic source of this control |
| [specimens/conflicting-tests/small.md](specimens/conflicting-tests/small.md) | Generic source of this control |
| [specimens/conflicting-tests/test.md](specimens/conflicting-tests/test.md) | Generic source of this control |
| [specimens/conflicting-tests/worker.md](specimens/conflicting-tests/worker.md) | Generic source of this control |
| [specimens/missing-component/alpha.md](specimens/missing-component/alpha.md) | Generic source of this control |
| [specimens/missing-component/beta.md](specimens/missing-component/beta.md) | Generic source of this control |
| [specimens/missing-component/component.md](specimens/missing-component/component.md) | Generic source of this control |
| [specimens/missing-component/diagnostics.txt](specimens/missing-component/diagnostics.txt) | Diagnostics the 0.36.0 release wrote for this control |
| [specimens/missing-component/entry.md](specimens/missing-component/entry.md) | Generic source of this control |
| [specimens/missing-component/large.md](specimens/missing-component/large.md) | Generic source of this control |
| [specimens/missing-component/small.md](specimens/missing-component/small.md) | Generic source of this control |
| [specimens/missing-component/test.md](specimens/missing-component/test.md) | Generic source of this control |
| [specimens/missing-component/worker.md](specimens/missing-component/worker.md) | Generic source of this control |
| [specimens/missing-test-axis/alpha.md](specimens/missing-test-axis/alpha.md) | Generic source of this control |
| [specimens/missing-test-axis/beta.md](specimens/missing-test-axis/beta.md) | Generic source of this control |
| [specimens/missing-test-axis/bundles/entry.bundles/entry.bundle.md](specimens/missing-test-axis/bundles/entry.bundles/entry.bundle.md) | Bundle the 0.36.0 release wrote for this control |
| [specimens/missing-test-axis/bundles/entry.bundles/worker-alpha.bundle.md](specimens/missing-test-axis/bundles/entry.bundles/worker-alpha.bundle.md) | Bundle the 0.36.0 release wrote for this control |
| [specimens/missing-test-axis/component.md](specimens/missing-test-axis/component.md) | Generic source of this control |
| [specimens/missing-test-axis/diagnostics.txt](specimens/missing-test-axis/diagnostics.txt) | Diagnostics the 0.36.0 release wrote for this control |
| [specimens/missing-test-axis/entry.md](specimens/missing-test-axis/entry.md) | Generic source of this control |
| [specimens/missing-test-axis/large.md](specimens/missing-test-axis/large.md) | Generic source of this control |
| [specimens/missing-test-axis/small.md](specimens/missing-test-axis/small.md) | Generic source of this control |
| [specimens/missing-test-axis/test.md](specimens/missing-test-axis/test.md) | Generic source of this control |
| [specimens/missing-test-axis/worker.md](specimens/missing-test-axis/worker.md) | Generic source of this control |
| [specimens/source/alpha.md](specimens/source/alpha.md) | Shared generic source of the five controls |
| [specimens/source/beta.md](specimens/source/beta.md) | Shared generic source of the five controls |
| [specimens/source/component.md](specimens/source/component.md) | Shared generic source of the five controls |
| [specimens/source/entry.md](specimens/source/entry.md) | Shared generic source of the five controls |
| [specimens/source/large.md](specimens/source/large.md) | Shared generic source of the five controls |
| [specimens/source/small.md](specimens/source/small.md) | Shared generic source of the five controls |
| [specimens/source/test.md](specimens/source/test.md) | Shared generic source of the five controls |
| [specimens/source/worker.md](specimens/source/worker.md) | Shared generic source of the five controls |
| [specimens/valid-two-bindings/alpha.md](specimens/valid-two-bindings/alpha.md) | Generic source of this control |
| [specimens/valid-two-bindings/beta.md](specimens/valid-two-bindings/beta.md) | Generic source of this control |
| [specimens/valid-two-bindings/bundles/entry.bundles/entry.bundle.md](specimens/valid-two-bindings/bundles/entry.bundles/entry.bundle.md) | Bundle the 0.36.0 release wrote for this control |
| [specimens/valid-two-bindings/bundles/entry.bundles/worker-alpha+small.bundle.md](specimens/valid-two-bindings/bundles/entry.bundles/worker-alpha%2Bsmall.bundle.md) | Bundle the 0.36.0 release wrote for this control |
| [specimens/valid-two-bindings/component.md](specimens/valid-two-bindings/component.md) | Generic source of this control |
| [specimens/valid-two-bindings/diagnostics.txt](specimens/valid-two-bindings/diagnostics.txt) | Diagnostics the 0.36.0 release wrote for this control |
| [specimens/valid-two-bindings/entry.md](specimens/valid-two-bindings/entry.md) | Generic source of this control |
| [specimens/valid-two-bindings/large.md](specimens/valid-two-bindings/large.md) | Generic source of this control |
| [specimens/valid-two-bindings/small.md](specimens/valid-two-bindings/small.md) | Generic source of this control |
| [specimens/valid-two-bindings/test.md](specimens/valid-two-bindings/test.md) | Generic source of this control |
| [specimens/valid-two-bindings/worker.md](specimens/valid-two-bindings/worker.md) | Generic source of this control |
| [validation-results.json](validation-results.json) | Saved body hashes, labels and check results |
| [validation.md](validation.md) | Draft and saved-state checks |

## Links

| Resource | Link |
| --- | --- |
| Python theme board | https://github.com/users/m2ux/projects/18 |
| Existing pattern owner | https://github.com/m2ux/prosiform/issues/526 |
| Documentation at 0.36.0 | https://github.com/m2ux/prosiform/tree/8cedda4cc06b0486168addc05f057161192a22a6/docs |
| I20 Preset Configuration | https://github.com/m2ux/prosiform/issues/867 |
| E00 Design Specimens | https://github.com/m2ux/prosiform/issues/890 |
| E01 Build Ledger | https://github.com/m2ux/prosiform/issues/868 |
| E02 Preset Imports | https://github.com/m2ux/prosiform/issues/869 |
| E03 Local Choice Groups | https://github.com/m2ux/prosiform/issues/870 |
