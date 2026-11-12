# Test Results

Revision tested: `c04f5d8e6` on `i15/e00/w00-the-v1-design-states`, the v1 design at `artifacts/planning/2026-10-17-prosiform-v1/design.md`.

## T1 Link Check

`python3 checks/links.py --online <design.md>`, the `make links` check named on one document, run from the project checkout at `main` (`6fc54bbf7`).

- Result: exit 0, `link check: every reference in 1 document(s) resolved`.
- Every `ok` line covers a local fragment or a remote URL; no `FAIL` and no `WARN` line.
- The new links resolve: `#presets`, `#exit-status-and-json-diagnostics`, `#link-classification-and-resource-handling` and `#automatic-output-names`.

## T2 Section Read

Each rule of the [Preset Alternatives design](../2026-11-12-preset-alternatives/design.md) read against its home in the v1 design. Every rule has one home; other sections name it by its bold lead or link to it.

| Record rule | Home in the v1 design |
| --- | --- |
| `choice` makes an alternative and holds one line | Conversion metadata: the `choice` row and **`choice` holds one line** |
| A malformed `choice`, a `choice` in `default` and a preset named `?` fail with `E_INVALID_CONVERSION_METADATA` | Conversion metadata: **`choice` holds one line**; indexed in the Metadata failures table |
| Alternatives layer over `default`, beside ordinary presets | Presets: **Alternatives** |
| Exactly one in force on the union, else `E_ALTERNATIVE_UNRESOLVED` with exit status 2 | Presets: **Exactly one alternative**; indexed in Metadata failures and the exit-status table |
| The failure lists each alternative with its choice line in declaration order | Exit status and JSON diagnostics: the `E_ALTERNATIVE_UNRESOLVED` paragraph and its text example |
| One diagnostic answers `?`, an unknown name and an absent pick | Presets: **Exactly one alternative** |
| A diagram link alone fails the rule | Presets: **Exactly one alternative** |
| An unpicked alternative raises no `W_PRESET_UNUSED` | Presets: **A preset nothing selected warns** |
| `?` leaves the pick to the agent; the listing; the pick's qualifier; an author's pick | Presets: **The agent's pick** |
| `?` on `¬` and `¬↳` only; a deferral to alternatives names one or carries `?`; `?` needs alternatives | Link classification: **The pick token** |
| The bundle carries `?` | Link classification: **A deferred link's destination** |
| A routing pair raises no `W_SUBST_USED`, and `W_SUBST_UNUSED` only for a key no link of its document names | Link classification: **The substitution mapping**; Exit status names the exception and links there |
| The guide's `?` entry | Guide: the symbol-grammar entry and the guide's list of what it holds |
| The fixtures | Metadata conformance cases: the Alternatives row |

Consistency read:

- **Selection by tags** and **`default` always applies** name the exactly-one rule where an unmatched name or an empty selection meets a document declaring alternatives.
- A `subst` value is called its *substitute* in Conversion metadata and Presets, so *alternative* names one thing.
- The refusal code for a misplaced `?` and a deferral's pick checks, which the record leaves open, is `E_UNSUPPORTED_CONSTRUCT` with exit 1, as the operator refusals take; the record's Defaults Taken lists it.
- One review round found one contradiction: **`default` is implicit** left `default` alone in force for an unmatched tag list without naming the exactly-one rule. `c04f5d8e6` names it there; T1 and T2 were re-run at that revision.
