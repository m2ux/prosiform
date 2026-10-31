## Overview

`prosiform` admits named **profiles** and argument names. A profile is a block of `-m` entries and budget overrides. A profile named for the section an entry reference selects applies to that compilation alone, so one artifact is compiled against stand-in material and a budget of its own while the rest of the run is unaffected.

## Problem

A run is one set of options, and one artifact is not the run.

- **Options are run-wide.**
  `-m` and the budgets `argparse` reads are properties of the invocation. Exercising one artifact against stand-ins means running the whole closure against them, so a mode's unrelated dependencies are mocked too and the run proves less than it appears to.
- **The key set is closed.**
  `prosiform` admits `root`, `group` and `group-depth`, and `metadata.decode` fails any other key with `E_INVALID_CONVERSION_METADATA`. A profile has nowhere to be written, so a caller keeping stand-in settings beside the document has to keep them on the command line, where they are neither versioned with the document nor reviewed with it.
- **A stand-in is attached to a section, not to a run.**
  The material that needs substituting belongs to the artifact under authoring — the epic body being drafted, the conventions file being revised — and that artifact is a section of a larger closure rather than the whole of it.
- **Nothing states what a profile reached.**
  A bundle compiled against a profile and one compiled without are the same kind of output, and a profile no section named is indistinguishable from one that applied.

## Proposal

- **Two kinds of key, decided by the value.**
  A `prosiform` key that is an argument name holds that argument's value and applies it to every compilation of the file. Any other key whose value is a mapping is a **profile**, named by the key and holding a substitution and budget overrides. A key that is neither an argument name nor a mapping is refused, because it is a misspelled field rather than a profile.
- **A profile applies to one compilation.**
  A **bundle compilation** is one entry reference and everything it reaches: the run's own entry, and each dispatched target's. A profile applies to a compilation when the **section** that compilation's entry reference names has a heading text matching the profile's name. The name matched is the resolved heading text, not the fragment as written, because a fragment is written in a different document from the one that declares the profile and a URL-escaped fragment names no profile directly.
- **A matched profile governs its compilation's own resolution.**
  The profile's substitution entries join the run's mapping for that compilation only, and its budget overrides replace the run's for that compilation only. Each compilation starts from a fresh count already, so the count a profile overrides is that compilation's.
- **A profile collision is refused.**
  Two entries in one profile substitution pair normalising to one identity, or a key and its value normalising to one identity, is invalid usage — the same two refusals `-m` carries, stated where the profile is read. A profile entry restating a `-m` entry for the same identity is refused too, because the two state one redirection twice and only one order makes a run reproducible.
- **A profile nothing applied warns.**
  `W_PROFILE_UNUSED` names the document, the profile and the sections the run compiled, and accompanies a published bundle and exit status `0`. A profile on a document reached only through a deferral is not unused: the run that follows the deferral compiles that document and reads the profile then.
- **A declared profile is inert where the document is merged.**
  A profile governs a compilation's resolution, not its inclusion. A document whose section is merged into another compilation carries its content as that compilation's own profile directed, because one bundle answers to one set of options.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| W00 | Design clause and pin | AC12 | | | |
| W01 | The profile key and the argument-name key | AC1, AC2 | W00 | | |
| W02 | Matching a section name to a profile | AC3, AC4, AC7 | W01 | | |
| W03 | A profile's entries bound and collisions refused | AC5, AC6 | W02 | | |
| W04 | A profile nothing applied warns | AC8 | W03 | | |
| W05 | A deferred target keeps its profile | AC9 | W03 | | |
| W06 | The profile stated in the invocation and the source page | AC10, AC11 | W04 | | |

## Acceptance Criteria

- [ ] **AC1.** A `prosiform` key naming a profile whose value is a mapping is accepted, and the same key whose value is a scalar fails with `E_INVALID_CONVERSION_METADATA`, as the corpus fixtures `fixtures/inclusion/a-profile-key-holds-a-mapping` and `fixtures/inclusion/a-profile-key-holding-a-scalar-is-refused` show.
- [ ] **AC2.** A `prosiform` key naming an argument holds that argument's value and applies it to every compilation of that document, as the corpus fixture `fixtures/inclusion/an-argument-key-applies-to-every-compilation` shows.
- [ ] **AC3.** An entry reference naming a section whose heading text matches a profile in the entry document compiles under that profile's substitution, as the corpus fixture `fixtures/inclusion/a-section-matching-a-profile-is-compiled-under-it` shows.
- [ ] **AC4.** A section whose heading text matches no profile compiles under the run's own options, as the corpus fixture `fixtures/inclusion/a-section-matching-no-profile-is-unaffected` shows.
- [ ] **AC5.** A profile's substitution applies to that compilation alone, and a sibling compilation reached by the same run resolves the same identities without it, as the corpus fixture `fixtures/inclusion/a-profile-leaves-a-sibling-compilation-alone` shows.
- [ ] **AC6.** Two entries in one profile normalising to one identity, a key and value normalising to one identity, and a profile entry restating a `-m` entry are each invalid usage with exit status `2`, as the corpus fixtures `fixtures/inclusion/a-duplicate-profile-key-is-refused` and `fixtures/inclusion/a-profile-entry-restating-a-m-argument-is-refused` show.
- [ ] **AC7.** A budget override in a profile bounds that compilation and leaves the run's budget governing every other compilation, as the corpus fixture `fixtures/inclusion/a-profile-budget-bounds-one-compilation` shows.
- [ ] **AC8.** A profile no compiled section named raises `W_PROFILE_UNUSED`, and the run publishes with exit status `0`, as the corpus fixture `fixtures/inclusion/an-unused-profile-warns` shows.
- [ ] **AC9.** A profile on a document reached only through a deferral raises no warning, and the run that compiles the deferral reads it then, as the corpus fixture `fixtures/inclusion/a-deferred-target-keeps-its-profile` shows.
- [ ] **AC10.** The invocation states the profile, its key rule and what it governs, and agrees with the command's help output, as `make invocation` shows.
- [ ] **AC11.** The source page states the two kinds of `prosiform` key and the profile's shape, as an inspection of that page shows.
- [ ] **AC12.** The design states profiles as a property of a compilation chosen by a section's heading text, and every fixture in this epic names a clause the pinned design carries, as `make conformance` shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — the decisions and the work items.
- **R2.** [Declared Inclusion](epic-a-declared-inclusion.md) — the epic that opens the key set this one fills.
- **R3.** [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) — the mapping a profile's entries join.
