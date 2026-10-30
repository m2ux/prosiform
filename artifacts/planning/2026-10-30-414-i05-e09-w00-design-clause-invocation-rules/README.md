# I05:E09 W00 Design Clause and Invocation Rules — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

Every later row of I05:E09 lands its corpus fixtures in the pull request that makes them pass, and each fixture names the design clause it encodes. Conformance reads the design at the revision `README.md` pins, so a fixture naming a clause that revision does not carry fails `make conformance`, which `make check` runs; the clause and the pin that reaches it must therefore exist before any mock fixture can merge.

This record holds the delivery of W00, which states the mapping in the contract's link classification clause, repeats it as a bundling rule, admits the words the epic's declarations use, and moves the pin onto the amended revision. The design amendment merges to `engineering` and the pin, the rule and the vocabulary land on `main`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W00 work item](w00.md) | The design clause, the bundling rule, the vocabulary and the pin |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
