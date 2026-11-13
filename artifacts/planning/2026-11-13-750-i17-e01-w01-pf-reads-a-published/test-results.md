# Test Results

Results for the joined W01–W03 unit at `a9d72f3f2` on `i17/e01/w01-pf-reads-a-published-main`, run on 2026-11-13 with `PROSIFORM_BUILD` naming the worktree's built `pf`.

## T1 Link Entries

`test_cli.py`: a Markdown link, `click` line and class diagram `link` line entry each compile the destination and section under the presets its title or tooltip selects, the bundles identical whatever marks open the link — each single mark, `¬↳⇉⫽`, `⇉¬` and marks opening a tooltip — and an entry carrying no title, or a tooltip of marks alone, selects no named preset. Held.

## T2 Pick

`test_cli.py`: `--pick` beside a Markdown, `click` or class diagram link carrying `?` compiles the named alternative on the first run; the listing's remedy names `--pick` and the rerun on the same link compiles; `--pick` beside a plain path or a link carrying no `?`, a repeated `--pick` and `--pick` without an entry exit `2` with `E_INVALID_USAGE`. Held.

## T3 Invocation

`make invocation` holds 29 statements of `invocation.md` against `pf -h`; `test_cli.py` finds `--presets` refused as an unrecognized argument and absent from the help and the guide. Held.

## T4 Corpus

`make corpus`: 615 fixtures, 615 pass. `make conformance` and `make independence` pass against the design pinned at `005b0ff1d`. New fixtures cover a link opening with each operator mark and a malformed combination, a `click` line and a class diagram `link` line entry, a first-run pick, picks after the listing and a stray, repeated or entry-less pick. `git grep -- '--presets' fixtures` prints nothing. Held.

## T5 Smoke and Eval Harness

`make smoke` passes, run outside the sandbox since it builds a wheel; `make eval-harness`: 771 passed; `make harness`: 1054 passed. `git grep -- '--presets' checks evals` prints nothing. Held.

## T6 Full Check

`make check` passes: lint, format, typecheck, `make test` (2127 passed), harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## Limitations

- `README.md` and `docs/` still name `--presets` in prose; W04 states the invocation there. This unit changed only the README's design pin and the architecture module inventory, which `make conformance` and `make harness` need.
