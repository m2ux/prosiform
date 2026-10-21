# I00:E10:W02 Clause-to-Fixture Mapping and the Report — October 2026

> Work Record · Created 2026-10-21

## Executive Summary

Each behavioural clause the design states gains the identifiers of the fixtures that exercise it, generated from the design and the corpus rather than maintained by hand. A clause no fixture reaches appears in the report's uncovered list, and the declared surface — the error codes the build emits and the exit statuses the fixtures reach — is listed beside it, so a gap is a visible result of running the report.

This row covers AC2, AC3 and AC5 of Corpus Conformance, and it is the row the rest of that epic reads: the independence check and the installation and internal-error listings all run against the report this work produces. It works on a base cut from `i00/e10/main`, which already carries the completed adversarial families W01 delivered.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | The work item: the component, the problem and what the row proposes. |
| [validation.md](validation.md) | The runs that observed each criterion, what the validation found, and what could not be ticked. |
| [changes.md](changes.md) | What the row changed in the checks, the corpus and the tracker, the plan changes it applied, and what remains open. |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#9 \[I00:E10\] Corpus Conformance](https://github.com/m2ux/prosiform/issues/9) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Planned work item | [i00-e10/w02.md](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1/i00-e10/w02.md) |
| Preceding row | [2026-10-21-9-i00-e10-w01-adversarial-fixture-families-and](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-9-i00-e10-w01-adversarial-fixture-families-and) |
| Pull request | [#167 \[I00:E10\] Clause-to-Fixture Mapping and the Conformance Report](https://github.com/m2ux/prosiform/pull/167) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
