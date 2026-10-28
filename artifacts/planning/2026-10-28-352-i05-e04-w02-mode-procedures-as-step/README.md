# I05:E04:W02 Mode Procedures as Step Sub-sections — October 2026

> Task delivery · Created 2026-10-28

## Executive Summary

This record holds the delivery of I05:E04 W02, which converts every procedure under `example/work-planner/modes/` to the step convention W01 states. Each step becomes a sub-section `N. Action`, placed one heading level below its procedure and ahead of the procedure's child sections. A sub-procedure such as Run Delivery Session holds its own steps one level further down. The worked example in `example/README.md` and the usage-example bundles follow the converted text.

A mode's steps are what a dispatching session, a guideline or a reviewer most often needs to point at. Once each step roots its own anchor, a link can name the one step it means, which W05 then uses.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W02 work item](w02.md) | Mode procedures as step sub-sections: scope, design and the checks it requires |
| [Validation](validation.md) | The inspection against AC2 and the results of `make links`, `make corpus` and `make check` |
| [Change list](change-list.md) | The plan changes this delivery session applied and held |

## Decisions

- **Action titles do not bind step headings.**
  - W01 left open whether the no-articles Action titles rule binds a step heading.
  - A step heading is not a procedure title, so its action keeps the step's label as written, articles included: `#### 1. Read the Brief`.
  - `example/work-planner/guidelines.md` states it under Action titles. (Delivery session, under the brief's allowance, 2026-10-28.)

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E04 Corpus Steps](https://github.com/m2ux/prosiform/issues/352) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Corpus Steps planning record](../2026-10-28-352-i05-e04-corpus-step-subsections/README.md) |
| Prior task | [W01 Step Convention in the Corpus Guidelines](../2026-10-28-352-i05-e04-w01-step-convention-in-the/README.md) |
