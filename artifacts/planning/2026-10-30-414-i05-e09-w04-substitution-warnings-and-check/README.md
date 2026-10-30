# I05:E09 W04 Substitution Warnings and Check Mode — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

The two warnings a substituted run emits. A bundle of stand-in material is the same kind of output as a bundle of the material that ships, so a skill rehearsed against stand-ins would otherwise read as a skill validated. The complementary defect is quieter: a mapping that matched nothing mocks nothing, and whatever the run asserts then passes for the wrong reason.

`W_MOCK_SUBSTITUTED` states each distinct redirected target at the first reference that redirects it, naming the identity the reference would have resolved to and the substitute. `W_MOCK_UNUSED` states each key no reference named. Both accompany a published bundle and exit `0`, as `W_RESOURCE_PORTABILITY` already does, and an empty mapping raises neither because neither has a subject.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W04 work item](w04.md) | The two substitution warnings, the check-mode run and the codes' registration |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Predecessor | [W01 Mapping, option and identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w01-mapping-option-and-identity) |
