# Change List — W04 and W05 Group and Member Names, Title Case and Destinations

> Delivery record · 2026-11-01

The plan changes this session applied, the ones it held, and the technical debt it classified.

## Applied

| Change | Kind | Why | Where |
| --- | --- | --- | --- |
| `src/prosiform/heading.py` created, holding the one title-case convention | Source | The work items name it as the component; metadata validation and heading generation read one definition of a word | `src/prosiform/heading.py`, `bundle.py`, `grouping.py`, `metadata.py` |
| A wordless `prosiform.group` refused with `E_INVALID_CONVERSION_METADATA` | Source | AC8; the existing code and remedy shape for an invalid group, so no new code enters the contract | `src/prosiform/metadata.py` |
| A wordless member takes its path text rather than being refused | Source | AC9 allows either; the Markdown suffix always carries a word, so no refusal path or new code is needed | `src/prosiform/grouping.py` |
| Grouped names keep separators; path runs keep slashes | Source | AC10 and decision D5; `grouping.titled` retired | `src/prosiform/grouping.py` |
| A titled parent's whole-document reference resolves to its title heading | Source | AC11 | `src/prosiform/grouping.py` |
| `Overview` emitted only over content beneath a subsection | Source | AC12 | `src/prosiform/grouping.py` |
| Six expected bundles regenerated, one fixture rewritten, four fixtures added | Test | Each moved bundle moves by generated headings, their destinations or the wrapper alone; `one-spelling-for-every-generated-heading` claimed hyphenated generated headings its sources never produced | `fixtures/grouping`, `fixtures/mock` |
| The design states the convention, the wordless refusal, the overview condition and the parent destination | Contract | The design is the contract `make conformance` and `make vocabulary` read; leaving it stating the replaced rules would be a stale claim | `artifacts/planning/2026-10-17-prosiform-v1/design.md` on `engineering` |

No task was created, closed or renumbered and no criterion changed. Epic delivery was recorded on [#443](https://github.com/m2ux/prosiform/issues/443): rows W04 and W05 link [#488](https://github.com/m2ux/prosiform/pull/488) with Done ticked, and AC8 to AC12 are ticked. The review pull request [#473](https://github.com/m2ux/prosiform/pull/473) cites #488 and states its changes.

## Held

| Held | Why |
| --- | --- |
| Placement of [#490](https://github.com/m2ux/prosiform/issues/490), the file-group parent's first-H2 destination | It is a contract decision, not debt: the bundle docstring states the file-group rule as deliberate, and AC11 was scoped to grouping depths. Whether the two rules should match is the user's call before it becomes a task |

## Technical debt classified

| Debt | Class | Disposition |
| --- | --- | --- |
| `one-spelling-for-every-generated-heading` described generated hyphens its titled sources never produced | Trivial | Fixed here: the fixture now carries untitled hyphenated sources |
| `a-member-named-by-the-title-it-absorbs` described the wrapper it no longer gets | Trivial | Fixed here with its regenerated bundle |

## Placement needs

#490 awaits the user's decision on whether a titled parent resolves one way in a file group and in a merged group.
