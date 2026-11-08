# Symbol Grammar in the Bundle — November 2026

> Hot-fix · Created 2026-11-08

## Executive Summary

Every bundle opens with a `§ Instructions` section whose one line reads ``Run `pf`, then follow the guidance it prints.`` An agent following a bundle must therefore call `pf` with no arguments before it can read a `↳`, `⇉` or `⫽` mark. The marks are the only part of that guide a bundle depends on.

This hot-fix pulls the guide's **Symbol grammar** out into one object in the code. Bare `pf` prints it as it does today, and every bundle's `§ Instructions` section carries it in place of the run-pf line.

## Artifacts

- [decisions.md](decisions.md) — confirmed decisions, implementation details, open questions
- [issue-body.md](issue-body.md) — the hot-fix issue body
