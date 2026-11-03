# Validation

The checks W00's work item names, run against task branch `i10/e06/w00-design-clause` at `88e601ad`, whose README pins the design at engineering commit `884681c0cc4caaa9a1740a24fab204fea9a39d1a`.

## T1 Design Inspection

The design at the pinned commit, read against each item `AC1` names. Result: held.

| Item | Where the design states it |
| --- | --- |
| The guide's text | *Guide*: **Plain text** and **The text**, the bytes bare `pf` prints, explaining `↳`, `⇉`, the `In parallel` sub-section, the inputs a dispatch carries, waiting for all and failures returned together |
| The returned-question marker | *Guide*: **The returned question**, a first line reading `Question:` |
| The run-pf line | *Link classification and resource handling*: **The Prosiform section**, the fixed line every bundle opens with; *Clean Markdown* follows |
| The inline `⇉` link | **The dispatch operator** and **Dispatch sub-sections**: the link keeps its mark and points at its target's compiled file; no sub-section is generated |
| The `In parallel` section | **Parallel dispatch sub-sections**: one sub-section per set, listing each member as a `⇉` link under the fixed instruction |
| A set of one | **Parallel dispatch sub-sections**: published as a single inline `⇉` link |
| The withheld link's wording | **The deferral mark**: a plain link to the target's rebased path, its content not bundled |
| `¬⇉` and `¬⫽` refused | **Operators that combine**: `E_UNSUPPORTED_CONSTRUCT` naming the link, no preset behaviour lost |
| `↳` as the composition mark | *Section composition*: **Recognition** (`↳` and `¬↳`), **The directive's link** (title text) |
| Arrow labels refused | *Section composition*: **Operator marks**, `[→](…)`, `[¬→](…)` and every arrow label refused pointing at `[↳ …]`; `[⇉↳ …]` and `[⫽↳ …]` refused as contradicting under **Operators that combine** |

No clause still states a Prosiform section's protocols, a `Run pf first` sub-section, a `Dispatch <text>` sub-section, an admitted `¬⇉` or `¬⫽`, or an arrow label composing; the conformance list (*Adversarial acceptance fixtures*: Deferral, Dispatch, Parallel dispatch, Prosiform section, Composition, CLI) follows the clauses. The revision history is engineering commits `f2ba719ad`, `400586c4c` (a planning sweep carrying part of the clause), `a9fb9948a` and `884681c0c`.

**Limitation.** Fixture-cited clause titles are kept so the conformance report resolves every declaration: **The Prosiform section**, **Dispatch sub-sections** and the fixture group **Prosiform section** now state what a bundle carries in their place, and the glossary rows for *Prosiform section*, *dispatch sub-section*, *arrow* and *composition directive* describe the shipped build until W02–W06 regenerate the fixtures and pages.

## T2 Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`, after `git fetch origin engineering`. Result: exit 0. Conformance: 360 clauses, 0 declarations naming no clause, 0 unfixturable codes; vocabulary: 49 marked terms, each defined in `docs/glossary.md`.
