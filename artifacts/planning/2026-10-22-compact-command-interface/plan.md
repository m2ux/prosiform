# Compact Command Interface

## Decision

The user selected option A: short forms as the primary interface, including `pf`, short flags and a compact command specification. The workspace requires removal of obsolete interfaces, so executable and long-option compatibility aliases are absent. Prosiform remains the package and product name. This is one standalone task; implementation is pending.

## Command Mapping

Flags are case-sensitive and retain their argument grammar and meaning. Budget flags use uppercase letters.

| Baseline | Planned |
| --- | --- |
| `prosiform` | `pf` |
| `--root DIR` | `-r DIR` |
| `--from DOC` | `-f DOC` |
| `-o, --output FILE` | `-o FILE` |
| `--group SLUG:DEPTH` | `-g SLUG:DEPTH` |
| `--check` | `-c` |
| `--diagnostics {text,json}` | `-d {text,json}` |
| `--fault {source-changed,internal}` | `-x {source-changed,internal}` |
| `--max-files N` | `-F N` |
| `--max-file-bytes N` | `-B N` |
| `--max-input-bytes N` | `-I N` |
| `--max-output-bytes N` | `-O N` |
| `--max-targets N` | `-T N` |
| `--max-links N` | `-L N` |
| `--max-nesting N` | `-N N` |
| `--max-expansion-depth N` | `-E N` |
| `--codes` | `-C` |
| `--version` | `-v` |
| `--help` | `-h` |

Example: `pf -r example/work-tracker -g artifacts:2 -g modes:2 modes/plan-mode.md`.

## Implementation Scope

1. Capture the delivery baseline and inventory the option contract, consumers and checks.
2. Update the installed entry point and existing parser, including explicit argument destinations, early diagnostic-format selection, help and budget metadata. Keep one implementation path and existing dependencies.
3. Translate repository invocations and corpus declarations with their readers, expected diagnostics, installation smoke tests and command-spec checks. Cover malformed options, repeated groups, fragment references, JSON usage errors, budgets, fault injection and informational modes.
4. Condense `invocation.md` and help while retaining every stated option meaning, default, constraint, source/dependency rule and outcome. Update the governing design contract on its owning branch and active examples, README instructions, CI and scripts. Preserve historical evidence.
5. Run existing checks, installed-command tests and the token comparison. Audit retired spellings by meaning; package names and imports remain legitimate.

The package remains `prosiform`; environment-variable and module names are outside the executable rename. Source-language changes, bundle compression, another compiler implementation and the authoring skill are outside this task. Related issue #177 concerns fault/code contract declarations; coordinate overlapping edits without adopting its separate scope.

## Verification

- Run updated `make check` with `PROSIFORM_BUILD` pointing to the candidate `pf` build, including corpus, installed-wheel smoke, invocation, conformance and independence checks.
- Exercise every mapped flag and rejected long spelling. Compare defined semantic results with the baseline, allowing spelling-only help and diagnostic differences.
- Extract a fact inventory from the baseline invocation and map every fact to the compact specification. Compression must retain defaults, constraints, operational rules and failure handling.
- Compare complete `invocation.md` files: baseline commit `9e11aedb062d8afdaffe111e6af9af454a1b8a68` and the candidate. Record one tokenizer encoding and pinned library version before comparison and use it throughout. Tokenization is evaluation tooling, not a production dependency.
- Use the four command blocks in the baseline Examples section as the fixed command sample. Translate only executable and options, preserving arguments and whitespace. Report per-command and aggregate counts. The full specification and command aggregate must each be strictly smaller; report exact counts and percentage savings without generalizing to other tokenizers.
- Report help counts separately. Retain measurement inputs, revisions or hashes and the counting script in delivery evidence for reproducibility.

## Evidence

- GitHub `main` resolved to `9e11aedb062d8afdaffe111e6af9af454a1b8a68` on 2026-10-22; its invocation was fetched directly.
- Local implementation inspection at `ea82c8bb03acb2f3c3ca64f6003005d4bf53ebd6`: `src/prosiform/cli.py`, `src/pyproject.toml`, `checks/smoke.py` and `Makefile`. This checkout is older than current main; implementation must refresh it.
- Open repository issues were inspected; no duplicate short-interface task was found. Issue #177 records related contract coverage debt.
- `.project/main/AGENTS.md` is absent. The supplied workspace instructions and `.engineering/AGENTS.md` govern this planning-only change.

## Planning Progress

- [x] Inspect the command surface and resolve interface scope.
- [x] Draft the standalone task and verification plan.
- [x] Validate and publish standalone task #212; format check and saved-body comparison pass.
- [x] Publish the planning record on the engineering branch.
