# I01:E10:W01 Protection on Every Long-Lived Branch — October 2026

> Task delivery · Created 2026-10-26

## Executive Summary

This record holds the delivery of I01:E10 W01: `main` requires a pull request before merge and refuses a force-push and a deletion, while `engineering` and `workspace` refuse a force-push and a deletion and take a direct push through the Admin role's bypass.

Repository ruleset 25628172 already holds that shape, so the row is delivered by recording it rather than by a settings change. The ruleset also requires a pull request on `engineering` and `workspace` for any writer without the bypass; that stricter configuration is kept.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Evidence](evidence.md) | The ruleset governing the long-lived branches, read against AC1 and AC3 |
| [Ruleset](ruleset.json) | Ruleset 25628172 as the API returns it |
| [Rules on main](rules-main.json) | The rules in effect on `main` |
| [Rules on engineering](rules-engineering.json) | The rules in effect on `engineering` |
| [Rules on workspace](rules-workspace.json) | The rules in effect on `workspace` |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I01:E10 Repository Configuration](https://github.com/m2ux/prosiform/issues/257) |
| Decision | [D30 in the initiative planning record](../2026-10-17-prosiform-v1/decisions.md) |
