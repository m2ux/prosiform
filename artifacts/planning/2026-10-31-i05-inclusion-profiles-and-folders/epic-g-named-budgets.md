## Overview

The eight budget options collapse into one repeatable `--budget NAME=VALUE`. Each ceiling gains a name and loses its letter, so the family appears in the help output as one option with a named set rather than as eight siblings of identical shape.

## Problem

Eight options of one shape are one decision printed eight times.

- **They are generated, not chosen.** `cli.parser()` loops over `BUDGETS` and registers each letter, so no option was decided on its own terms. Eight siblings of identical shape is the case a namespace exists for.
- **The letters carry no meaning.** `-F` is files, `-N` is nesting, `-E` is expansion depth. A reader maps a letter to a count with a table, and nothing in the option suggests which count.
- **Two letters collide in appearance.** `-o` names the output folder and `-O` names the bundle's byte ceiling. They are one case apart and mean unrelated things, which no naming rule explains.
- **The help output is half budgets.** Sixteen option lines, of which eight are the same sentence with a different noun.
- **A family has no completion.** A shell offered neither `--budget` nor `--limit-`, so a caller learns the eight letters by reading the help.

## Proposal

- **One option, repeatable.** `--budget NAME=VALUE`, given once per ceiling. `action="append"` with a value parser, so `--budget files=256 --budget links=100` sets two.
- **Eight names replace eight letters.** `files`, `file-bytes`, `input-bytes`, `output-bytes`, `targets`, `links`, `nesting`, `depth`. Each is held on its `Budget` object beside the option it replaces, so `limits.py` remains the one table.
- **An unknown name is invalid usage.** `--budget key=1` fails with `E_INVALID_USAGE`, exit status `2`, naming the name and the eight admitted. Validity moves from the grammar into the value parser, which is the trade this shape makes.
- **A malformed entry is invalid usage.** An entry carrying no `=`, an empty name and a value that is no positive decimal integer each fail the same way, so one fault is stated once.
- **A name given twice is refused.** Two entries naming one ceiling fail, because the second states the first again and only one order would make a run reproducible.
- **One `Budget` object per name.** `BUDGETS` gains a `name` and loses its `option`, and `budgets(options)` reads the parsed pairs into `Limits` rather than reading a `Namespace` attribute per budget.
- **The design's CLI contract states one row.** `make invocation` compares the table against the help output in both directions, so eight rows become one and the comparison still holds.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, the names | AC6 | | | |
| W01 | The option, its parser and its refusals | AC1, AC2, AC5 | W00, [I08:E00:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | `Limits` read from the pairs | AC3 | W01 | | |
| W03 | The corpus rewritten to the names | AC4 | W01 | | |
| W04 | The option table and the help output | AC7 | W02 | | |

## Acceptance Criteria

- [ ] **AC1.** `--budget files=512` bounds the count of distinct source documents at 512, and a run crossing it fails with `E_RESOURCE_LIMIT` naming the ceiling, as the corpus fixture `fixtures/limits/a-named-budget-bounds-the-run` shows.
- [ ] **AC2.** An entry naming a ceiling outside the eight, and an entry carrying no `=`, an empty name or a value that is no positive decimal integer, each fail with `E_INVALID_USAGE` and exit status `2`, as the corpus fixtures `fixtures/cli/an-unknown-budget-name-is-invalid-usage` and `fixtures/cli/a-malformed-budget-entry-is-invalid-usage` show.
- [ ] **AC3.** Every ceiling a run does not name stands at its declared default, and `LIMITS` holds one entry per `Budget`, as `src/tests/test_limits.py` shows.
- [ ] **AC4.** Every corpus fixture that passed a budget passes its name instead, and its expected result is unchanged, as `make corpus` shows.
- [ ] **AC5.** Two entries naming one ceiling are refused with `E_INVALID_USAGE`, as the corpus fixture `fixtures/cli/a-budget-named-twice-is-refused` shows.
- [ ] **AC6.** The design states the option, the eight names and their counting rules, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC7.** The documented option table names one budget row and agrees with the help output in both directions, as `make invocation` shows.

## References

- **R0.** Epic — [I08:E05 Named Budgets](https://github.com/m2ux/prosiform/issues/451).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions this change comes from.
