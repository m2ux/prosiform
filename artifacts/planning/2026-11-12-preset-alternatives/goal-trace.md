# Goal Trace

## Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| A link leaves the preset to the agent at compile time | AC1, AC4 | E01 | E01 AC1, AC5 | The `?` Tag: deferred links only; the bundle carries `?` |
| The agent sees the target's alternatives and when to pick each | AC4 | E00, E01, E02 | E00 AC5; E01 AC4, AC5, AC7, AC8; E02 AC1, AC2 | The Pick: one diagnostic answers `?` |
| A document generic over a kind compiles for the one kind picked | AC1 | E00, E01 | E00 AC2; E01 AC5 | Alternatives; Routing |
| A missing or wrong pick fails rather than compiling the wrong route | AC2 | E00, E01 | E00 AC3, AC4; E01 AC2, AC3 | Alternatives: exactly one is in force; The `?` Tag: its refusals |
| Routing raises no stand-in warning | AC3 | E00 | E00 AC6, AC7, AC8 | Routing; Alternatives: an unpicked alternative is silent |
| The guide defines the pick | AC4 | E01 | E01 AC4 | Guide |
| The contract and the documentation state every rule | AC5 | E00, E01 | E00 AC1, AC9; E01 AC6 | Change Surface: Documentation |

The source is the record's [design](design.md), the initiative's one marked reference.

## Gaps

Ranked; the flagged ones most threaten the goal.

1. **Resolved.** The initiative criteria restated single epic criteria, and no criterion made "compiles for the one kind picked" true. Five criteria now state what the epics achieve together.
2. **Resolved.** The design lets an ordinary preset stand beside the pick, and no criterion held it. E00 AC2 now does.
3. **Resolved.** E00 AC5, the listing, delivered no initiative criterion E00 covered. E00 now covers AC4.
4. **Flagged: the guide's home may move.** The planned [symbol grammar in the bundle](../2026-11-08-symbol-grammar-in-bundle/README.md) hot-fix moves the guide's symbol entries into every bundle. If it lands before E01 W03, the `?` entry joins that shared grammar and every expected bundle regenerates, and E01 W03 is re-planned then.
5. **Flagged: the corpus binds the Rust build.** The fixtures these rows add fail the Rust build until it implements alternatives. The initiative records the overlap as a reference and plans no row for it.
6. **Noted: the pattern catalogue.** The design-patterns initiative's call-site dispatch page states the pick as the author's; once alternatives land, that page can cite them.

## Checks

- Format: the initiative and both epic drafts report nothing to fix, apply or decide.
- Dependencies: no problems and no open candidate unit; E00 W02 and W03 stay split on a recorded line, and E01 W01 and W02 are joined.
- Saved: #707, #708 and #709 read back with the intended title, labels and body, and the format check of each saved body, with its saved parent or epics, reports nothing to fix, apply or decide.
