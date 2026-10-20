# I00:E11:W03 A Manifest Comparison That No Single Build's Text Binds - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the row that lets a fixture state what a run's output must contain without binding the corpus to one build's wording. A diagnostic declaration gains an optional field naming text its message carries, so two faults sharing one error code are told apart, and a run whose standard output legitimately differs between builds is compared on its shape rather than on its bytes.

It matters because the corpus is today weaker than the contract it encodes: three usage fixtures declare identical severity, code and exit status, so each passes against the other's run, and a build answering the wrong fault records conformance. Absence of the field compares nothing, so every fixture now in the corpus stays valid.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w03.md](w03.md) | The task's plan: the declaration's shape, what it compares and the fixtures that exercise it |
| [validation.md](validation.md) | What the comparison was measured to do, against a response it must accept and one it must refuse, and the gate the delivery was held to |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Defect | [#52 Fixture Comparison of Diagnostic Message Text](https://github.com/m2ux/prosiform/issues/52) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
