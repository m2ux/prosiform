# I09:E05 W35 Validation — November 2026

> Validation evidence · Created 2026-11-03

## Executive Summary

Each check the [W35 work item](../2026-11-02-463-i09-grouping-and-composition/e05/w35.md) names, run against branch `i09/e05/w35-separate-the-eval-page` at `d3823737`.

## AC39

- **T1 — Rendered read of `evals/diagram-following/README.md`.**
  The `entry` key, the `warnings` key and the `undeclared/` directory each stand as a paragraph of their own, separated by blank lines, the `warnings` paragraph directly after the `entry` paragraph it extends.

## Make check

- **T2 — `make check` with `PROSIFORM_BUILD` naming the worktree's build.**
  Exit 0: 1663 check tests and 1253 harness tests pass, and `make links`, `make tables` and every other target pass.
