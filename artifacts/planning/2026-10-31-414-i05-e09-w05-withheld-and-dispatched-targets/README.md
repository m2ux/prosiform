# I05:E09 W05 Withheld and Dispatched Targets — October 2026

> Task delivery · Created 2026-10-31

## Executive Summary

The targets a run resolves without compiling. A withheld link's target is redirected like any other, and the destination the bundle publishes for it is the substitute's working-directory-relative path, because a later run follows the path the bundle published and must find the stand-in there.

This record holds its delivery of `AC4`: the work item, the validation evidence for every check the work item names, and the plan changes the session applied and held.

The deferred, dispatched and parallel-dispatched paths all resolved through the mapping at the head this row was cut from, because `withholding_target` took it when W01 landed the seam. What did not follow the redirect was the fragment the destination publishes: `rebased` wrote the path the mapping resolved and the fragment the author wrote. A section key redirects the section with the document, so a deferred link's destination named a section the substitute need not carry, and a later run following that destination refused with `E_TARGET_NOT_FOUND` on a bundle this run had declared sound. The run now publishes the fragment it resolved to, which is the contract's own rule.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W05 work item](w05.md) | The withheld and dispatched targets, the fragment a deferred destination publishes, and the fixture that shows it |
| [Validation](validation.md) | The checks T1–T10 at the revisions they ran, with their observations |
| [Change list](change-list.md) | Every plan change this session applied, and every one it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Predecessor | [W01 Mapping, option and identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w01-mapping-option-and-identity) |
| Predecessor | [W04 Substitution warnings and check mode](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w04-substitution-warnings-and-check) |
| Pull request | [#447 Redirect a Withheld Target](https://github.com/m2ux/prosiform/pull/447) |
