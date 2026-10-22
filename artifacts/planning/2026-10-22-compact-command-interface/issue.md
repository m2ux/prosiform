## Overview

Make `pf` and short flags Prosiform's command interface, with a compact command specification that reduces the tokens agents consume when reading and invoking the tool. Deliver this as one standalone task.

## Problem

- **Routine commands carry avoidable text.**
  The [current invocation](https://github.com/m2ux/prosiform/blob/9e11aedb062d8afdaffe111e6af9af454a1b8a68/invocation.md#options) exposes 18 named options, with only output offering a short flag.
- **The command reference consumes context on every read.**
  Option descriptions, examples and operational rules occupy a full document; compression needs a measured comparison that retains their meaning.

## Proposal

- **One compact interface.**
  Install `pf` as the sole executable with the short-option mapping in the planning record. The package and product retain the name Prosiform.
- **Complete command coverage.**
  Preserve positional references, values, defaults, repeatability, validation, budgets, streams, exit statuses and compiler semantics under the short spellings.
- **One compact command specification.**
  Make `invocation.md` the concise, self-contained agent reference: syntax, option meanings and defaults, constraints, examples, operational rules and outcomes.
- **A coherent command surface.**
  Align parser handling, early diagnostic selection, help, packaging, installation checks, repository callers, fixtures, documentation and the governing CLI contract.
- **Measured token savings.**
  Compare pinned baseline and resulting specifications and equivalent command examples using the same recorded tokenizer and version.
- **Bounded delivery.**
  Compiler behavior, package naming, output compression and the proposed authoring skill are outside this task; compatibility aliases are absent.

## Acceptance Criteria

- [ ] **AC1.** A clean installation exposes exactly the planned `pf` command surface, as installed-command smoke tests and parser tests for every mapped option and rejected retired spelling show.
- [ ] **AC2.** Each translated invocation preserves its defined compilation, validation or informational outcome, as the updated corpus, CLI tests and complete `make check` run show, allowing command-spelling changes in help and diagnostics.
- [ ] **AC3.** The compact specification covers every baseline command-contract fact, as a fact-by-fact coverage review and `make invocation` show.
- [ ] **AC4.** The compact specification and aggregate equivalent command sample each use fewer tokens than their pinned baselines, as a reproducible report naming the tokenizer, version, inputs and counts shows.
- [ ] **AC5.** Active repository callers and governing CLI documentation use the planned short interface, as an audited search for retired executable and option spellings shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-22-compact-command-interface) — flag mapping, scope, validation and confirmed decision.
- **R2.** [Baseline invocation](https://github.com/m2ux/prosiform/blob/9e11aedb062d8afdaffe111e6af9af454a1b8a68/invocation.md) — the command contract and measurement baseline.
