# Symbol Grammar in the Bundle — November 2026

> Hot-fix · Created 2026-11-08

## Executive Summary

Every bundle opens with a `§ Instructions` section whose one line reads ``Run `pf`, then follow the guidance it prints.`` An agent following a bundle must therefore call `pf` with no arguments before it can read a `↳`, `⇉` or `⫽` mark. The marks are the only part of that guide a bundle depends on.

This hot-fix writes the guide's **Symbol grammar** into the `§ Instructions` section of every bundle and drops the run-pf line. Bare `pf` keeps the rest of the guide (usage, compiling a link, exit status) and no longer prints the symbol grammar.

## Artifacts

- [decisions.md](decisions.md) — confirmed decisions, implementation details, open questions
- [issue-body.md](issue-body.md) — the hot-fix issue body
