# I05:E06 W10 Authoring Guard — October 2026

> Task delivery · Created 2026-10-29

## Executive Summary

The authoring rules the example now meets are held by review alone, so the next change could restate a value or detach a command and nothing would fail. This task wires `make authoring` into `make check`, so a change that breaks a rule fails the repository's own checks.

It also gives the check a failing case per rule, so a rule the check stops detecting is a test that fails rather than a silence.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work item](w10.md) | What this task delivers, its parts and its test obligations |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Example Authoring](https://github.com/m2ux/prosiform/issues/376) |
| Epic plan | [Planning record](../2026-10-28-376-i05-e06-example-authoring/README.md) |
| Predecessor | [W09 delivery](https://github.com/m2ux/prosiform/pull/394) — the ownership pass this guard holds |
