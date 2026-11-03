# Validation

The checks W06's work item names, run against task branch `i10/e06/w06-the-pages-stating-the` at `71e7b16e`, with `origin/i10/e06/main` at `05ce8754` merged.

## T1 Pages Read Against The Guide

The guide `pf` prints, and the `dispatch/`, `parallel-dispatch/` and `prosiform/` fixtures, were read against `README.md`, `docs/*.md`, `invocation.md`, `checks.md` and `fixtures/README.md`. A search of those pages for the Prosiform section, protocol paragraphs, generated `Dispatch` sections, `Run pf first` and deferred dispatch found one stale claim, that a bundle may carry `Prosiform` and any heading opening with `Dispatch` as its author's headings; it is removed. `docs/dispatch.md` states the guide as the home of the rules and the returned-question marker `Question:`, and the refusal of `¬⇉` and `¬⫽`; the README, glossary and invocation page state the marker. The `¬⇉` and `¬⫽` mentions that remain state the refusal. Result: held. Observes AC11.

## T2 Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`, after `git fetch origin engineering`: all checks ok, 515 fixtures pass. Result: held. Observes AC11.
