# W05 Validation

Candidate: `ef1ce19dd93581320050130574ef570f83c0599f`, based on W04 merge `4bb6f261475340f0ea2338c7107c88c942c878fe`. Frozen output oracle: main `cd3d8e635b8db500ceb7230b26209bdd37f637da`. Contract: the complete W01 target pinned at `d26ae99b7e989f0978d20f7d9bdc098c16319797`.

## Authoring Guidance

Pass, AC11. Invocation now states exact frontmatter boundaries, the YAML 1.2 Core mapping, string-valued paired fields, optional ordinary-Markdown skill fields, reserved names, rejected YAML features, resource accounting, destination ownership, deferred selection and atomic errors. The worked example shows the literal declaration present in both artifact sources. Its output excerpt and the invocation output match the annotated shared source. Documentation, invocation agreement, online links and vocabulary checks pass.

An independent review compared the guidance to the decoder and normative contract and found no blocking discrepancy. Active README, invocation, glossary, renderer instructions and example Markdown contain no obsolete structural flags or claims that frontmatter is ignored or membership is directory-wide. Historical `VISUAL-CASES.md` explicitly identifies archived outputs and points to current metadata instructions. The README compilation image was visually inspected: it shows Rules membership and deferred Codex/Claude links, has no obsolete flags, and matches annotated Common/Agents sources. No historical image or capture needs rewriting.

## Representative Corpus

Pass, AC12. [Baseline audit](baseline-audit.py) declares all existing grouping fixtures, grouped entry delivery, structural-ancestor depth overflow and the grouped shared worked example. The new conflicting-depth negative case has no baseline counterpart and is covered by the complete corpus. All 26 baseline comparisons match the frozen output bytes exactly, including empty failure output; each invocation also passes its current manifest's exit and diagnostic assertions. [Comparison report](baseline-comparisons.json) retains fixture identity, exit status, byte count and SHA-256.

Run from the candidate checkout:

```sh
PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i01/e06/w05-metadata-authoring-guidance/src --frozen pf' uv run --project src --frozen python /home/mike1/projects/dev/md-composer/.engineering/artifacts/planning/2026-10-23-218-i01-e06-w05-metadata-authoring-guidance/baseline-audit.py
```

The complete corpus passes all 252 fixtures, including the metadata negatives, source preprocessing, atomic conflicts and all five shared usage examples. Three usage outputs intentionally reflect their shared annotated sources, as W04 records; the grouped representative retains baseline bytes. No expected output is regenerated in W05.

## Full Checks

Pass, AC11 and AC12. `PROSIFORM_BUILD` as above with `make check` exits 0 on the candidate: locked dependencies, lint, formatting, types, 905 implementation tests, 611 harness tests, all 252 fixtures, installed-wheel smoke, layout, command tables, online links, vocabulary, invocation, conformance and independence. The [full log](full-check.log) retains the complete conformance report.

Conformance reports 268 clauses, 22 without fixture coverage, 16 clauses no run can state, three section headings without behavior and three installation claims not observed by this run. Those declarations and their explanations are retained in the log; this audit does not claim exhaustive contract coverage. All 31 declared diagnostic names are reached and the build and contract inventories agree.

## Installed Package

Pass. The repository wheel smoke runs during full checks. The [W04 installed probe](../2026-10-23-218-i01-e06-w04-per-file-compilation-settings/installed-probe.py) also runs from this candidate checkout using `uv run --project src --frozen python PATH/installed-probe.py`. It builds and installs this wheel outside the checkout and checks metadata grouping, retired flags, help, roots, entries, referrer, JSON diagnostics, check mode, output and byte limit. Its [result](installed-wheel.log) is retained.

## Handoffs

The planned authoring skill in issue #208 consumes this metadata contract; implementing that skill is outside W05. The Rust implementation consumes the eventual tagged contract and corpus through the existing source-language handoff. Nested-folder layout and call-site section composition remain separate work. No runtime change, new package, new task or deferred defect arose from this audit.

## Remote Checks

Pending publication of the task pull request and checks on the exact candidate head.

## Delivery

Pending task merge and tracker readback. Epic reviews #220 and #222 remain drafts for the user's review.
