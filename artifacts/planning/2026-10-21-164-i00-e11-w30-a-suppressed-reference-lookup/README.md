# A Suppressed Reference Lookup Reported by Nothing — October 2026

> Delivery · Created 2026-10-21

## Executive Summary

The design declares `E_PARSER_REFERENCE_LIMIT` for a parser resource limit that suppresses a reference lookup, and requires the run to fail explicitly rather than publish a bundle whose references were silently not expanded. The corpus reaches that code only through the public `--max-nesting` option, so the condition the design's Parser exhaustion family names — reference-expansion suppression below every public input and output limit — is stated by no fixture, and neither is the case that spends the budget on its last valid reference and must claim no omitted reference.

It matters because a suppressed lookup is indistinguishable from an absent reference: a run that publishes such a bundle reports success over content whose dependencies it never discovered. The corpus rather than one build's tests is what says what exhaustion produces. Epic [#9](https://github.com/m2ux/prosiform/issues/9) reads the adversarial family listing for its AC1, so this row is one of the two that decide whether Corpus Conformance can be integrated.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Analysis](analysis.md) | The budget reachable below every public limit, the depths that bound it, and the clause spelling the family takes |
| [W30](w30.md) | The work item: scope, component, breakdown and test requirements |
| [Validation](validation.md) | The boundary measured, the reference the failure names, and the fixtures, unit cases and gate the delivery was held to |
| [Changes](changes.md) | The plan changes this delivery applied and held, and the readings it left as they stand |

## Links

| Resource | Link |
| --- | --- |
| Task issue | [#164 \[I00:E11:W30\] Parser Exhaustion: A Suppressed Reference Lookup Reported by Nothing](https://github.com/m2ux/prosiform/issues/164) |
| Epic | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Preceding row's record | [W13 Parser reference limit](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-20-108-i00-e11-w13-a-parser-resource-limit) |
