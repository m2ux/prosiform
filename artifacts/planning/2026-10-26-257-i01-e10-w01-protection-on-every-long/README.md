# I01:E10:W01 Protection on Every Long-Lived Branch — October 2026

> Task delivery · Created 2026-10-26

## Executive Summary

This record holds the delivery of I01:E10 W01: `main` requires a pull request before merge and refuses a force-push and a deletion, while `engineering` and `workspace` refuse a force-push and a deletion and still accept a direct push.

The repository is public and its long-lived branches are unprotected, so the delivery procedure is the only thing holding the branch shape. The settings must leave the procedure working: planning records and workspace changes are pushed directly, and task and epic pull requests are merged by the delivering session.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I01:E10 Repository Configuration](https://github.com/m2ux/prosiform/issues/257) |
| Decision | [D30 in the initiative planning record](../2026-10-17-prosiform-v1/decisions.md) |
