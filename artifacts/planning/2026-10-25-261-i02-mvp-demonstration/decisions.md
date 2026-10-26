# Decisions

Each design choice the plan rests on, with the evidence behind it.

## D1 — The demonstration target is the example, not the skill

The user directed that the development target is `example/work-tracker`, and withdrew the question of whether the skill itself is compatible. The example is the tree the repository's documentation and fixtures already point at, so a demonstration against it needs no new authority: `invocation.md` and `fixtures/README.md` already name it.

The rejected alternative was making the skill compatible in place. That was tried and failed for a reason worth recording: compiling `skills/work-planner/modes/plan-mode.md` from the workspace as a source root fails with `E_TARGET_NOT_FOUND`, because the file declares no root and `[Propose Mode](propose-mode.md)` then names a sibling under the invocation directory rather than under the source root.

## D2 — The goal is a reproducible run, not a narrative claim

A demonstration that cannot be repeated is a rehearsal. Each initiative criterion therefore names a command or a check rather than a description of what someone saw. The instrument is either `make check` or the corpus run, both of which continuous integration already invokes.

## D3 — The Parent Merge defect is deferred, not taken first

[Parent Merge](https://github.com/m2ux/prosiform/issues/234) proposes that the file writing a link owns that link's grouping rules, so a parent merges its links' composed results. The migration epic instead declares the group on the member file, and a three-folder test showed that model produces a resolving bundle with no unresolved links.

The two models are alternatives rather than a sequence, so neither blocks the other's demonstration. Taking the defect first would reword the migration epic's third task and its fifth criterion, and would put a behaviour change between the demonstration and the feature set it demonstrates. It is deferred to the debt epic and recorded there, so it is neither lost nor silently dropped.

## D4 — The Prerequisites drop proceeds as the migration epic plans it

Thirty-five of the skill's files open with a `## Prerequisites` section listing documents that same file also reaches from its body. The migration epic removes them and requires that every document a list named stays reachable from that file's body.

The user confirmed this proceeds as written rather than gaining a per-file verification row. The risk is recorded rather than mitigated by plan change: a file whose body does not in fact cover its Prerequisites list loses that edge, and the bundles of the rows that follow record the loss as a missing section rather than as a failure.

## D5 — The initiative carries three epics, the debt epic last

The demonstration is delivered by one epic, which is the migration epic's seven rows. A second epic supplies the ground a demonstration needs and that no migration row provides: a tagged baseline, one repeatable command, and the checks held green on the demonstration branch. A third epic holds what the delivery defers.

The debt epic takes the highest number so the epics in flight are planned and delivered ahead of it, and the initiative stays open while its rows are undelivered.

## D6 — What the initiative defers stays in place

The field-refinement initiative's remaining epics are neither closed nor moved. They keep their issues, their rows and their numbers, and the demonstration initiative's boundary is what defers them. Moving them would renumber two tables for no delivery benefit, and an epic closed without delivery would read as complete.

The one edge that breaks is the specification-freeze epic's task, which names the final row of the migration epic as a prerequisite. That reference is to an epic leaving the initiative, so it is recorded as a cross-initiative dependency rather than rewritten.

## D7 — The review of the epic's integration pull request

A review of [#272](https://github.com/m2ux/prosiform/pull/272) against the migration epic's ten criteria found every one held, with three findings the criteria did not catch.

- **AC6 and AC8 are scoped to the example's own tree.** Eight links, four in `guidelines.md` and four in `modes/revise-mode.md`, name the shared skill guidelines at `example/guidelines.md`, outside `example/work-planner`, and are not deferred. The copy is held to the skill's bytes, so those links cannot be rewritten. The user chose to reword both criteria to name `example/work-planner` rather than change the tree.
- **The usage fixtures' descriptions are held to their bundles.** Two manifests describe output their re-recorded bundles do not hold, and two fixtures share one invocation. The user chose a further row on the migration epic, W08, carrying AC11 and AC12.
- **Removing `example/work-tracker` belongs to the debt epic.** Its W06 and W07 already repoint the root README's usage commands and the round-trip suite. The deletion is that epic's W08, depending on both, rather than a row on the migration epic that would plan the same work twice.

## D8 — The parent arrangement is ratified, not reverted

W08's delivery found that an entry document which is itself a titled group member opens its group with its own title and preamble, leads with its own sections, and puts the other members' subsections in an Overview after them. [#236](https://github.com/m2ux/prosiform/pull/236) built that arrangement deliberately, and `src/prosiform/grouping.py` documents it, but the design's Grouping clauses, `invocation.md` and `docs/glossary.md` still state the layout it replaced. Two grouping fixtures' descriptions contradict their expected output, and no fixture pins a titled entry member of a `group-heading: false` group.

The user chose to ratify the build in the contract on the debt epic, as its W10 (the contract text) and W11 (the fixtures citing it), rather than revert the build or record the drift alone.

The same review's merged-group fixture keeps a name stating directory-wide membership, which per-file declarations no longer give. Its rename is the debt epic's W09. W09 and W10 share no file, so neither joins the other.

## D9 — A link resolves from the file that writes it

The example's links were rewritten from the declared root so the bundle would include what they name, and 457 of them then opened nothing for a reader. The user directed that source links are never changed to suit the build: the build follows the path a reader follows. [#274](https://github.com/m2ux/prosiform/pull/274) makes every link resolve from the directory of the file that writes it, with the root as the boundary only, and restores every example link to the skill's own destination. Every mode bundle is byte-identical before and after.

This delivers the debt epic's row on a root naming a sibling and a parent, so that row and its criterion leave that epic and the migration epic's W09 carries the work. The debt epic's criteria and references are renumbered; its row ids keep their numbers.
