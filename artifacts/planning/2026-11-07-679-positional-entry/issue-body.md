## Overview

`pf` requires `--entry` before the document it compiles. The option carries nothing the argument does not: a run compiles exactly one document, and the option's only job is to name it. The entry reference returns to a positional argument, so `pf guide.md --presets checks` compiles what `pf --entry guide.md --presets checks` compiles today.

Target: `main`

## Problem

- **The option is noise in every command a caller writes.**
  It appears 1078 times across the corpus, the tests, the checks, the evals and the documentation. An agent reading a tagged link must reproduce it before the destination it already resolved, and the guide spends a line teaching a spelling that carries no decision.
- **It arrived with the tag selection, not because of it.**
  `--entry` and `--presets` landed together in `ad0332c74`, replacing the positional `references` list. The planning record states them as separate decisions, so the option is a grammar choice that can be reversed on its own.
- **A leading-dash entry is not supported.**
  A positional argument cannot take a filename beginning with `-` without a `--` separator. The `--entry=-guide.md` spelling retires with the option, and the guide states that such a name is refused rather than teaching a separator.

## Proposal

- **The entry is a positional argument.**
  The grammar reads `pf [OPTIONS] REF [--presets PRESETS]`, with one `REF` accepted and a second refused as invalid usage. `--presets`, `-o`, `-c`, `-d`, `--budget`, `-C`, `-v` and `-h` are unchanged, and each parses in any order around the entry.
- **The refusal keeps its code and its remedy.**
  A command line naming no entry, naming two, or naming a complete Markdown-link expression is `E_INVALID_USAGE` at exit 2, as it is today. The `entry()` normalization is untouched, so a fragment alone still names `document#fragment` as its remedy.
- **The design is amended and re-pinned.**
  The CLI contract's grammar block, its option table and its refusal list state the positional entry. The amendment lands on `engineering`, and the README badge and the corpus's design links pin that commit, so `make conformance` maps every fixture to a clause the design still states.
- **The contract moves a minor.**
  Removing an option is a major change, and below `1.0.0` the minor carries it: `contract/v0.18.0` and `python/v0.18.0`. The build declares `0.18.0` as the change lands, and the release is cut after merge.

## Acceptance Criteria

- [ ] **AC1.** A run naming its entry positionally compiles the bundle the option form compiled, and a run naming two entries is refused with `E_INVALID_USAGE` at exit 2, as `make corpus` and `make smoke` show.
- [ ] **AC2.** The documented invocation, the help output and the guide state the positional grammar and no `--entry`, and `make invocation` passes against the build.
- [ ] **AC3.** Every fixture, test, check, eval and document names its entry positionally, and `make check` passes.
- [ ] **AC4.** The design's CLI contract states the positional grammar, the README badge and the corpus's design links pin the commit holding it, and `make conformance` reports no fixture naming a clause the design does not state.
- [ ] **AC5.** `src/pyproject.toml` declares `0.18.0` and `pf -v` reports it beside the profile identifier, as `make smoke` shows.

## References

- **R1.** [Link-Tag Presets planning record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/decisions.md) — the decision that introduced `--entry` beside `--presets`.
- **R2.** [Design, CLI contract](https://github.com/m2ux/prosiform/blob/795bbfb67c66b02193f0313138f59f18aa6c5274/artifacts/planning/2026-10-17-prosiform-v1/design.md#cli-contract) — the grammar this hot-fix amends.
