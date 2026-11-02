## Overview

`-m` is retired. A conversion setting is stated in a preset, so a document whose presets state no `subst` substitutes nothing — and the deletion of the only command-line channel is the point, not a side effect.

## Problem

The option is a second channel for one thing.

- **It duplicates the preset.**
  `-m ORIGINAL=ALTERNATIVE` states a substitution on the command line, and a preset states the same thing in the document. Two channels for one intent means a reference has two possible answers.
- **It makes a preset optional.**
  While `-m` exists, a document needs no preset to be substituted; with it gone, a preset is the only way, which is what lets the section that links a document select which of that document's presets governs it.
- **Its scope is the run.**
  `-m` is read once in `main` and folded into every compilation — every document's links, the entry reference and every dispatched bundle — so a caller cannot confine a substitution to the document under test. A preset can.
- **Its name states the wrong mechanism.**
  The option and the preset entry were both called `mock`, a word that names the test scaffolding the feature was raised for rather than the thing it does: it substitutes the path a reference resolves to. The entry is `subst`.
- **It is delivered and open.**
  The option, its parser, its documented row and a folder form are on the epic base. All 25 corpus fixtures under `fixtures/mock/` pass it, and so do the 5 scenarios `make mock-scenarios` runs.

## Proposal

- **The option is removed.**
  `cli.parser()` declares no `-m`, the help output names none, and the documented table has no row.
- **The setting is `subst`, and no preset stating one substitutes nothing.**
  That is the consequence, and it is stated rather than softened: a link written by a document whose governing presets state no `subst` is compiled as authored.
- **A pair reaches only the links its declaring document writes.**
  The document that links it, the documents it links, a substitute and a dispatched target are each governed by their own presets alone. A substitute's fragment-only link names a section of that substitute, so it resolves there.
- **An entry reference is compiled as named.**
  It is written by no document, so no preset substitutes it, and the run derives its name from the path the caller wrote.
- **A preset's sides resolve from the declaring file.**
  A preset states a pair as a colon mapping rather than the option's `=` string, and its sides read from the declaring document as every other path in a document does.
- **The folder pair retires.**
  A preset states one pair per entry, so a side ending in a separator is refused. The folder lookup, its refusals and its six fixtures are removed.
- **The two warnings are named for the entry.**
  `W_SUBST_USED` names the reference a pair redirected, the identity it would have resolved to and the substitute; `W_SUBST_UNUSED` names a pair no reference named. A code keeps naming the mechanism it reports, so neither carries the retired option's word.
- **The lookup stays; its channel is the preset.**
  The lookup, section precedence, the document-pair refusals and the warnings are read from a preset rather than a command line, and the `subst` entry takes its shape from the preset grammar. No page, help string or fixture names `-m`.
- **A substitution is recorded where the run compiles it.**
  A key is served only by a reference in content the run selected, so a key whose only reference is a withheld link in a heading outside the selection warns as unused.
- **The corpus moves to presets.**
  Each surviving `-m` pair becomes a preset entry in the source tree with its expected result unchanged, which is the evidence the mechanism moved rather than the behaviour. A fixture for a retired capability — `root`, the referrer, the entry redirect, the folder form — is withdrawn by the row that retires it.
- **The example scenarios state their stand-ins in presets.**
  Each scenario writes its `subst` entry into the copied document that writes the link, because a pair reaches only that document's links.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause, retired option | AC13 | | | |
| W01 | The option's removal and the preset read | AC1, AC2 | W00, [I08:E00:W00](https://github.com/m2ux/prosiform/issues/434) | | |
| W02 | The declared-file path basis | AC3 | W01 | | |
| W03 | The corpus rewritten to presets | AC4 | W01 | | |
| W04 | The option's documented row withdrawn | AC5 | W03 | | |
| W05 | A reference under no `subst`, and the table | AC6, AC7 | W02 | | |
| W06 | A pair reaches only its own document's links | AC8, AC9 | W01 | | |
| W07 | An entry reference is compiled as named | AC10 | W01 | | |
| W08 | The folder pair retires | AC11 | W01 | | |
| W09 | The example scenarios state their stand-ins in presets | AC12 | W03 | | |
| W10 | A heading outside the selection records no substitution | AC14 | W01 | | |

## Acceptance Criteria

- [ ] **AC1.** `-m` is not an option the build accepts, and a command line carrying it is invalid usage with exit status `2`, as the corpus fixture `fixtures/cli/the-mock-option-is-gone` shows.
- [ ] **AC2.** A link written by a document whose governing preset states `subst` is substituted by that pair, compiling the substitute the option's pair compiled, as the corpus fixture `fixtures/inclusion/a-preset-states-the-pair` shows.
- [ ] **AC3.** A preset's sides resolve from the file that declares it, so the same declaration reads the same from any working directory, as the corpus fixture `fixtures/inclusion/a-preset-pair-resolves-from-its-file` shows.
- [ ] **AC4.** Every corpus fixture that passed `-m` and whose behaviour survives states its pair in a preset with its expected result unchanged, and each fixture for a retired capability — `root`, the referrer, the entry redirect, the folder form — is withdrawn by the row that retires it, as `make corpus` shows.
- [ ] **AC5.** No page, help string or fixture names `-m`, and the invocation documents substitution only as the `subst` entry of [I08:E01](https://github.com/m2ux/prosiform/issues/436), as `make invocation` and a search of the tree show.
- [ ] **AC6.** The documented table names no `-m` and agrees with the help output, and the source page states a preset's `subst` as the only channel, as `make invocation` and `make vocabulary` show.
- [ ] **AC7.** A link written by a document whose governing presets state no `subst` is compiled as authored, as the corpus fixture `fixtures/inclusion/no-preset-substitutes-nothing` shows.
- [ ] **AC8.** A `subst` pair declared in one document redirects no link another document writes — the document it links, the document linking it, or the substitute — and a substitute's fragment-only link resolves against that substitute, as the corpus fixture `fixtures/inclusion/a-subst-pair-stays-in-its-document` shows.
- [ ] **AC9.** A dispatched target's bundle resolves its links under its own document's presets alone, as the corpus fixture `fixtures/inclusion/a-dispatched-bundle-reads-its-own-subst` shows.
- [ ] **AC10.** A positional entry compiles the document it names and derives its run name from that path, whatever its document's presets state, as the corpus fixture `fixtures/inclusion/an-entry-is-not-substituted` shows.
- [ ] **AC11.** A `subst` side ending in a separator fails with `E_INVALID_CONVERSION_METADATA` naming the entry, as the corpus fixture `fixtures/inclusion/a-folder-subst-is-refused` shows.
- [ ] **AC12.** Each scenario `make mock-scenarios` runs states its stand-in as a `subst` entry in the copied document that writes the link, and passes no command-line pair, as `make mock-scenarios` shows.
- [ ] **AC13.** The design states `subst` as the only substitution channel, resolved from the declaring file and reaching only the links that file writes, names the retired option and the renamed codes, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.
- [ ] **AC14.** A `subst` key whose only reference is a withheld link in a heading outside the selected content raises `W_SUBST_UNUSED` and no `W_SUBST_USED`, as the corpus fixture `fixtures/inclusion/a-pair-reached-only-outside-the-selection-is-unused` shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions this removal comes from.
