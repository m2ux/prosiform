# Frozen And Planned Specimens

## Executed 0.36.0 Controls

The generic sources are under `specimens/source`. Each case retains its exact entry and its written bundle and diagnostic outputs. The released bundler was invoked locally; no agent or model was called.

| Case | Existing selection | Actual exit | Meaning |
| --- | --- | --- | --- |
| valid-two-bindings | alpha, small | 0 | A component alternative and an ordinary test binding compose |
| missing-component | small | 2 | A required component alternative is refused |
| missing-test-axis | alpha | 0 | Ordinary test presets declare no exclusive required test axis |
| conflicting-components | alpha, beta, small | 2 | Incompatible alternatives are refused |
| conflicting-tests | alpha, small, large | 2 | Conflicting substitution values are refused |

All warnings and refusals remain in the retained diagnostics; a successful build proves construction only. [specimens/baseline.json](specimens/baseline.json) identifies the release, its revision and the exact bundle hashes.

## Proposed-Form Specimen Sets

Each set's README lists its files as real, written in the proposed form, or hand-written.

| Set | Shows |
| --- | --- |
| [Ledger](specimens/ledger/README.md) | The ledger for two real builds, its schema, check-mode output, verification outcomes and refusal |
| [Preset imports](specimens/imports/README.md) | A preset importing levels and substitutions, the inline control its bundles must equal, and each refusal |
| [Choice groups](specimens/choice-groups/README.md) | Two local groups on one document, explicit and open picks, each refusal and the preset listing |
| [Combined](specimens/combined/README.md) | The three features in one run, and every open design point with its candidate answers |

## Deterministic Matrix

- **Ledger.** Selected and unselected output; default and named ordering; whole and fragment selection; layout; source hashes; ordinary and stub substitutions; briefs; dispatch, deferral and pick targets; levels and models; the invocation; check-mode output; serialization and publication refusal; unchanged Markdown bytes; verification of an unchanged, a source-changed, a bundle-changed and a ledgerless set.
- **Imports.** Exact complete names with case and whitespace normalization; missing and impure targets; an explicit target with no implicit default or body; direct and nested equal and conflicting values; an imported and local conflict; cycles; changed and symbolic-link sources; declaring-key and key-relative target origins; ordinary, entry-map and entry-stub reach through dispatch and deferral; ledger origin accounting.
- **Groups.** Every explicit two-axis combination; each missing axis; two values in one axis; irrelevant groups; the unnamed single axis; additive presets and optional stubs; one open axis at a dispatch with the other fixed; several open at a dispatch; one pick for each open group at the entry; brief independence; output identity; dispatch and deferral preservation; ledger group entries; the preset listing.

## Bounded Agent Checkpoint

Deterministic combinations do not each receive a model run. One representative changed pick mechanism is frozen with its exact source and child bundles, inputs, client, bundler, model, effort and receipt instruments. Where the agent-facing path is byte-equivalent to its fixed control, that proof stands with no agent call. Otherwise at most one matched pair runs: one fresh caller and one child in each arm, at most four fresh contexts and six hundred seconds for each arm, under a separate release. The checkpoint stops after the pair and an independent source and binding adjudication; failed attempts are retained and no retry or larger sweep is implied.
