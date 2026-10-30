# I05:E09 W00 Design Clause and Invocation Rules — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

Every later row of I05:E09 lands its corpus fixtures in the pull request that makes them pass, and each fixture names the design clause it encodes. Conformance reads the design at the revision `README.md` pins, so a fixture naming a clause that revision does not carry fails `make conformance`, which `make check` runs; the clause and the pin that reaches it must therefore exist before any mock fixture can merge.

This record holds the delivery of W00, which states the mapping in the contract's link classification clause, repeats it as a bundling rule, admits the words the epic's declarations use, and moves the pin onto the amended revision. The design amendment merges to `engineering` and the pin, the rule and the vocabulary land on the epic base.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W00 work item](w00.md) | The design clause, the bundling rule, the vocabulary and the pin |
| [Validation](validation.md) | The checks T1–T8 at the revisions they ran, with their observations |
| [Change list](change-list.md) | Every plan change this session applied, and every one it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Pull request | [#425 Design Clause, Invocation Rules and Pin](https://github.com/m2ux/prosiform/pull/425) |
| Correction pull request | [#427 Design Clause Correction: An Absent Key and Check Mode](https://github.com/m2ux/prosiform/pull/427) |
| Design amendment | [57809368](https://github.com/m2ux/prosiform/commit/578093687a55c7ed2dc1110b7347fa80a4f6f0ce) |
| Corrected amendment | [f723a85d](https://github.com/m2ux/prosiform/commit/f723a85dbe5fd2a3e379b951c2dfb5c58670f5e6) |
