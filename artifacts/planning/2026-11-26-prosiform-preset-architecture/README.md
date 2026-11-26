# Preset Configuration — November 2026

> Feature plan · Created 2026-11-26

## Executive Summary

The confirmed goal is inspectable effective configuration, explicit pure settings reuse and local independent component/test choices. The plan has three epics and thirteen bounded tasks, ordered manifest, imports, choices with priorities3/2/1 and no lanes.

The fixed0.34 source/bundle baseline, generic valid/refused controls, complete-name/origin/scope constraints and bounded changed-pick checkpoint keep new syntax separate from existing behavior. Runtime profiles, structured effort descriptors and reviewer presets remain deferred. The compiler features are planned; implementation has not started.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [scope.md](scope.md) | Confirmed goal and excluded work |
| [initiative-body.md](initiative-body.md) | Initiative criteria and epic links |
| [e00-body.md](e00-body.md) | Effective-manifest scope and four tasks |
| [e01-body.md](e01-body.md) | Pure-import scope and four tasks |
| [e02-body.md](e02-body.md) | Local-choice scope and five tasks |
| [draft-metadata.json](draft-metadata.json) | Confirmed identities, priorities and task counts |
| [decisions.md](decisions.md) | Accepted boundaries and review decisions |
| [design.md](design.md) | Proposed syntax, origins and selection semantics |
| [specimen-matrix.md](specimen-matrix.md) | Valid, refused and equivalent configurations |
| [goal-trace.md](goal-trace.md) | Goal coverage and resolved review findings |
| [validation.md](validation.md) | Draft and saved-state observing checks |
| [e00/w00.md](e00/w00.md) | Task work item and exact component scope |
| [e00/w01.md](e00/w01.md) | Task work item and exact component scope |
| [e00/w02.md](e00/w02.md) | Task work item and exact component scope |
| [e00/w03.md](e00/w03.md) | Task work item and exact component scope |
| [e01/w00.md](e01/w00.md) | Task work item and exact component scope |
| [e01/w01.md](e01/w01.md) | Task work item and exact component scope |
| [e01/w02.md](e01/w02.md) | Task work item and exact component scope |
| [e01/w03.md](e01/w03.md) | Task work item and exact component scope |
| [e02/w00.md](e02/w00.md) | Task work item and exact component scope |
| [e02/w01.md](e02/w01.md) | Task work item and exact component scope |
| [e02/w02.md](e02/w02.md) | Task work item and exact component scope |
| [e02/w03.md](e02/w03.md) | Task work item and exact component scope |
| [e02/w04.md](e02/w04.md) | Task work item and exact component scope |
| [specimens/baseline.json](specimens/baseline.json) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/alpha.md](specimens/conflicting-components/alpha.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/beta.md](specimens/conflicting-components/beta.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/component.md](specimens/conflicting-components/component.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/diagnostics.txt](specimens/conflicting-components/diagnostics.txt) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/entry.md](specimens/conflicting-components/entry.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/large.md](specimens/conflicting-components/large.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/small.md](specimens/conflicting-components/small.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/test.md](specimens/conflicting-components/test.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-components/worker.md](specimens/conflicting-components/worker.md) | Task work item and exact component scope |
| [specimens/conflicting-tests/alpha.md](specimens/conflicting-tests/alpha.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/beta.md](specimens/conflicting-tests/beta.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/component.md](specimens/conflicting-tests/component.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/diagnostics.txt](specimens/conflicting-tests/diagnostics.txt) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/entry.md](specimens/conflicting-tests/entry.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/large.md](specimens/conflicting-tests/large.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/small.md](specimens/conflicting-tests/small.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/test.md](specimens/conflicting-tests/test.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/conflicting-tests/worker.md](specimens/conflicting-tests/worker.md) | Task work item and exact component scope |
| [specimens/missing-component/alpha.md](specimens/missing-component/alpha.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/beta.md](specimens/missing-component/beta.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/component.md](specimens/missing-component/component.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/diagnostics.txt](specimens/missing-component/diagnostics.txt) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/entry.md](specimens/missing-component/entry.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/large.md](specimens/missing-component/large.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/small.md](specimens/missing-component/small.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/test.md](specimens/missing-component/test.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-component/worker.md](specimens/missing-component/worker.md) | Task work item and exact component scope |
| [specimens/missing-test-axis/alpha.md](specimens/missing-test-axis/alpha.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/beta.md](specimens/missing-test-axis/beta.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/bundles/entry.bundles/entry.bundle.md](specimens/missing-test-axis/bundles/entry.bundles/entry.bundle.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/bundles/entry.bundles/worker-alpha.bundle.md](specimens/missing-test-axis/bundles/entry.bundles/worker-alpha.bundle.md) | Task work item and exact component scope |
| [specimens/missing-test-axis/component.md](specimens/missing-test-axis/component.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/diagnostics.txt](specimens/missing-test-axis/diagnostics.txt) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/entry.md](specimens/missing-test-axis/entry.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/large.md](specimens/missing-test-axis/large.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/small.md](specimens/missing-test-axis/small.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/test.md](specimens/missing-test-axis/test.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/missing-test-axis/worker.md](specimens/missing-test-axis/worker.md) | Task work item and exact component scope |
| [specimens/source/alpha.md](specimens/source/alpha.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/source/beta.md](specimens/source/beta.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/source/component.md](specimens/source/component.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/source/entry.md](specimens/source/entry.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/source/large.md](specimens/source/large.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/source/small.md](specimens/source/small.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/source/test.md](specimens/source/test.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/source/worker.md](specimens/source/worker.md) | Task work item and exact component scope |
| [specimens/valid-two-bindings/alpha.md](specimens/valid-two-bindings/alpha.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/beta.md](specimens/valid-two-bindings/beta.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/bundles/entry.bundles/entry.bundle.md](specimens/valid-two-bindings/bundles/entry.bundles/entry.bundle.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/bundles/entry.bundles/worker-alpha+small.bundle.md](specimens/valid-two-bindings/bundles/entry.bundles/worker-alpha+small.bundle.md) | Task work item and exact component scope |
| [specimens/valid-two-bindings/component.md](specimens/valid-two-bindings/component.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/diagnostics.txt](specimens/valid-two-bindings/diagnostics.txt) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/entry.md](specimens/valid-two-bindings/entry.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/large.md](specimens/valid-two-bindings/large.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/small.md](specimens/valid-two-bindings/small.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/test.md](specimens/valid-two-bindings/test.md) | Generic planning contract, source or retained compiler evidence |
| [specimens/valid-two-bindings/worker.md](specimens/valid-two-bindings/worker.md) | Task work item and exact component scope |

## Links

| Resource | Link |
| --- | --- |
| Python theme board | https://github.com/users/m2ux/projects/18 |
| Existing pattern owner | https://github.com/m2ux/prosiform/issues/526 |
| Branch declaration | https://github.com/m2ux/prosiform/issues/865 |
| Fixed current documentation | https://github.com/m2ux/prosiform/tree/794922d41465b91deb4edb3a7484506cb8f519cd/docs |

## Tracker

- [I20 Preset Configuration](https://github.com/m2ux/prosiform/issues/867)

| Epic | Priority | Tasks |
| --- | ---: | ---: |
| [E00 Effective Manifest](https://github.com/m2ux/prosiform/issues/868) | 3 | 4 |
| [E01 Preset Imports](https://github.com/m2ux/prosiform/issues/869) | 2 | 4 |
| [E02 Local Choice Groups](https://github.com/m2ux/prosiform/issues/870) | 1 | 5 |

- [Publication identities and hashes](publication.json)
- [Saved-state validation](validation-results.json)
