# I05:E04:W06 Step-Shape Guard Under make check — October 2026

> Task delivery · Created 2026-10-28

## Executive Summary

This record holds the delivery of I05:E04 W06, a guard that `make check` runs over the example corpus. The guard fails on a procedure that writes its steps as a numbered list, on a step heading that is not exactly one level below its parent, and on a step heading that repeats another's number and action. It runs as `make steps`, with tests under `checks/tests`.

Nothing observes the step convention otherwise. A numbered list added to a procedure reads as valid Markdown and publishes, but it loses the anchor a link needs, and `pf` states no rule on a target's shape. The guard keeps the convention in force after the epic closes.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W06 work item](w06.md) | The step-shape guard: scope, rules, the my-skill scope decision and the checks it requires |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E04 Corpus Steps](https://github.com/m2ux/prosiform/issues/352) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Corpus Steps planning record](../2026-10-28-352-i05-e04-corpus-step-subsections/README.md) |
| Prior task | [W04 Artifact Operations as Step Sub-sections](../2026-10-28-352-i05-e04-w04-artifact-operations-as-step/README.md) |
