# Delivery

## Todos

- [x] Implement and verify the short command surface.
- [x] Compact the specification and review baseline fact coverage.
- [x] Measure token savings and run the complete checks.
- [ ] Publish commits, evidence and the delivery pull request (in progress).

## Scope

Standalone issue #212 uses the confirmed mapping in `plan.md`. The isolated worktree is `.worktrees/212-compact-commands`, branch `task/212-compact-commands`, based on `9e11aedb062d8afdaffe111e6af9af454a1b8a68`. The governing design is maintained on `engineering`.

## Complete gate

Candidate `f11eb7d` passes the complete `make check` gate. [Full output](make-check.log) records 800 source tests, 609 harness tests and 252 passing corpus fixtures. Lock, lint, formatting, types, installed-wheel smoke, layout, tables, online links, vocabulary, invocation, conformance and independence checks pass. The test environment needed network and loopback access; restricted-sandbox socket errors were resolved by rerunning with that access. A relative build command was corrected to the absolute candidate executable before the passing run.

```bash
PATH=/home/mike1/.local/bin:/usr/local/bin:/usr/bin:/bin PROSIFORM_BUILD=/home/mike1/projects/dev/md-composer/.worktrees/212-compact-commands/src/.venv/bin/pf make check
```

The governing design commit is `e5d8c0b`, published on engineering through `114f79f`, which integrates concurrent engineering work without rewriting it. The source candidate changes the command surface and its consumers; the compiler pipeline retains its behavior. Parser tests reject all 18 retired long spellings, exercise the eight planned budget mappings, and verify short diagnostic forms, option terminators and last-option selection. Installation smoke tests resolve `pf` outside the checkout and reject an environment exposing the retired executable.

Conformance reports no uncovered addressable clauses, unknown clause declarations or code disagreements. Its existing inventory also identifies 16 clauses no run states, three sections stating no behavior and three installation claims outside the corpus; installation smoke observes the installation claims.

## Equivalent examples

All four baseline example invocations and their translated equivalents return status 0 with byte-identical stdout and stderr. [Results](example-equivalence.json) include the byte counts, including zero bundle bytes for validation-only. Run against installed baseline and candidate checkouts:

```bash
python3 compare-examples.py /path/to/baseline /path/to/candidate
```

## Specification coverage

The [66-row fact review](coverage.md) maps the entire pinned baseline contract to the compact reference. `make invocation` verifies 29 statements: every argument row, every exit row, profile and required operating statements. It compares full row meanings with live help, preserving the existing bidirectional check.

## Token measurement

Tokenizer: `tiktoken==0.12.0`, encoding `o200k_base`. [Inputs](measurement-inputs) retain exact UTF-8 texts; [machine-readable results](measurement.json) record their SHA-256 hashes, byte counts and token counts. Baseline: `9e11aedb062d8afdaffe111e6af9af454a1b8a68`. Candidate: `f11eb7d`. Help is captured at `COLUMNS=80` for both builds. The library is evaluation tooling, absent from production dependencies.

| Input | Baseline tokens | Candidate tokens | Saved |
| --- | --- | --- | --- |
| Complete invocation.md | 1360 | 1086 | 274 (20.15%) |
| Four equivalent command blocks | 78 | 74 | 4 (5.13%) |
| Help, reported separately | 607 | 477 | 130 (21.42%) |

The four individual command counts are `14→13`, `20→19`, `28→27`, `16→15`; they sum to `78→74`. Only executable and flag spellings are translated; arguments and whitespace are preserved. Concatenating the retained blocks with two separator newlines also produces `78→74`. The script extracts each original fenced block directly. These savings apply to this encoding and these inputs.

From this planning folder:

```bash
uv run --script measure.py
```

## Retired-spelling audit

[Search output](retired-spellings.txt) records every remaining mapped long spelling on the source candidate. Reviewed exceptions are:

- `src/tests/test_cli.py`: negative tests for all retired options.
- `Makefile` and `src/README.md`: uv, Ruff and pytest options, which belong to those tools.
- `scripts/render-diagram.py` and `docs/diagram-renderer.md`: the diagram renderer's separate argument parser. Its compiler calls use `-r`, `-O` and `-g`.

The retired executable appears only in its negative installation check, package metadata/imports, product prose, repository URLs and historical identifiers. Active compiler invocations, CI, fixture declarations, expected diagnostics, help, documentation and the governing design use `pf` and the planned flags. Historical engineering records and copied upstream skill sources retain their original bytes.

## Delivery state

Implementation is committed and pushed. Repository main has no branch protection or active rules. Linking and merge await confirmation of the repository auto-close setting required by Work Planner; no setting has been changed. No additional implementation scope or deferred debt was introduced.
