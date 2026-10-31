## Overview

`-m` is retired. A conversion setting is stated in a preset, so a compilation that selects no preset substitutes nothing — and the deletion of the only command-line channel is the point, not a side effect.

## Problem

The option is a second channel for one thing.

- **It duplicates the preset.** `-m ORIGINAL=ALTERNATIVE` states a substitution on the command line, and a preset states the same thing in the document. Two channels for one intent means a compilation has two possible answers.
- **It makes `default` optional.** While `-m` exists, a document needs no preset to be substituted; with it gone, a preset is the only way, which is what makes one top-level source the setting for its whole closure.
- **Its scope is the run.** `-m` is read once in `main` and folded into every compilation, so a caller cannot vary a substitution by entry. A preset can.
- **It is delivered and open.** [I08:E07](https://github.com/m2ux/prosiform/issues/414) landed the option, its parser and its documented row, and four fixtures pass it.

## Proposal

- **The option is removed.** `cli.parser()` declares no `-m`, the help output names none, and the documented table has no row.
- **A compilation selecting no preset substitutes nothing.** That is the consequence, and it is stated rather than softened: a document reached with no preset is compiled with its references as authored.
- **A preset's sides resolve from the declaring file.** A preset that replaced the option keeps the pair syntax but not the path basis, because a declaration in a document reads from that document as every other path does.
- **E09's delivered work is superseded, not reverted.** The mapping, the lookup, the refusals and the warnings all stay — they are read from a preset rather than a command line. Its option criterion is marked superseded and its option row withdrawn.
- **Four fixtures are rewritten.** Each `-m` pair becomes a preset entry in the source tree, and each expected result is unchanged, which is the evidence the mechanism moved rather than the behaviour.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, retired option | AC7 | [E01:W00](https://github.com/m2ux/prosiform/issues/436), [I08:E05](https://github.com/m2ux/prosiform/issues/451) | | |
| W01 | The option's removal and the preset read | AC1, AC2 | W00, [I08:E00:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | The declared-file path basis | AC3 | W01 | | |
| W03 | The corpus rewritten to presets | AC4 | W01 | | |
| W04 | E09's superseded criterion and row | AC5 | W03 | | |
| W05 | The guideless document and the table | AC6 | W02 | | |

## Acceptance Criteria

- [ ] **AC1.** `-m` is not an option the build accepts, and a command line carrying it is invalid usage with exit status `2`, as the corpus fixture `fixtures/cli/the-mock-option-is-gone` shows.
- [ ] **AC2.** A compilation selecting a preset substitutes by that preset, where the same tree and the same preset state the same pair the option used to, as the corpus fixture `fixtures/inclusion/a-preset-states-the-pair` shows.
- [ ] **AC3.** A preset's sides resolve from the file that declares it, so the same declaration reads the same from any working directory, as the corpus fixture `fixtures/inclusion/a-preset-pair-resolves-from-its-file` shows.
- [ ] **AC4.** Every corpus fixture that passed `-m` states its pair in a preset, and its expected result is unchanged, as `make corpus` shows.
- [ ] **AC5.** E09's option criterion is marked superseded and its documented row withdrawn, as an inspection of that epic shows.
- [ ] **AC6.** The documented table names no `-m` and agrees with the help output, and the source page states a preset as the only channel, as `make invocation` and `make vocabulary` show.
- [ ] **AC7.** A compilation that selects no preset substitutes nothing and withholds nothing, as the corpus fixture `fixtures/inclusion/no-preset-substitutes-nothing` shows.

## References

- **R0.** Epic — [I08:E06 Preset-Only Substitution](https://github.com/m2ux/prosiform/issues/461).
- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions this removal comes from.
- **R2.** [I08:E07](https://github.com/m2ux/prosiform/issues/414) — the epic whose option this retires.
