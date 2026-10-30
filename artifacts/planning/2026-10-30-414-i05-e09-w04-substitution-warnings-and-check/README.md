# I05:E09 W04 Substitution Warnings and Check Mode — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

The two warnings a substituted run emits, and the mapping applying under `-c`. A bundle of stand-in material is the same kind of output as a bundle of the material that ships, so a skill rehearsed against stand-ins would otherwise read as a skill validated. The complementary defect is quieter: a mapping that matched nothing mocks nothing, and whatever the run asserts then passes for the wrong reason.

`W_MOCK_SUBSTITUTED` states each substitution — one warning per mapping key a reference named, at the first reference that named it, carrying the link's location, the authored destination and the substitute. `W_MOCK_UNUSED` states each key no reference named, with no location, because it states a fact about the invocation. Both accompany a published bundle and a check run alike, at exit `0`, as `W_RESOURCE_PORTABILITY` already does, and an empty mapping raises neither because neither has a subject.

The codes are registered in the contract's exit-status section and in the corpus schema's warning catalogue together with their emission, because a fixture declaring a code the schema does not carry fails validation before the run starts. Three corpus fixtures prove the behaviour, and the corpus gained the ability to declare a diagnostic's `location` for the first of them.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W04 work item](w04.md) | The two substitution warnings, the check-mode run and the codes' registration |
| [Validation](validation.md) | The checks T1–T11 at the revisions they ran, with their observations |
| [Change list](change-list.md) | Every plan change this session applied, and every one it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Predecessor | [W01 Mapping, option and identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w01-mapping-option-and-identity) |
| Pull request | [#433 Substitution Warnings and Check Mode](https://github.com/m2ux/prosiform/pull/433) |
| Design amendment | [5d9a3567](https://github.com/m2ux/prosiform/commit/5d9a3567b334a132b0597833230a28617b477212) |
| Corrected amendment | [827b66fc](https://github.com/m2ux/prosiform/commit/827b66fcd837ec6a9e203a82a1c86fc5ec2b60bb) |
