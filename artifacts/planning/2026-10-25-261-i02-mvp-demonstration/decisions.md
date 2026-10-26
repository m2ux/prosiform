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

## D10 — SKILL.md loads each mode through pf

`SKILL.md` is read raw as the skill's entry point. Each mode link in its Modes list opens with `↳` (U+21B3), a skill-level bootstrap mark: it tells the reading agent to run `pf` from the skill's directory on the link's destination as written, writing the bundle to a scratch file outside the repository, then to read the whole bundle and follow it as that mode's procedure. The bundle goes to a file because a mode bundle of 200 KB or more printed to standard output is truncated by agent harnesses.

`pf` never sees the mark, since no mode bundle compiles `SKILL.md`'s Modes list, so the mark needs no compiler operator. `»` stays reserved for sub-agent dispatch, which waits until the skill is factored ([#275](https://github.com/m2ux/prosiform/pull/275), reverted). The section is named Bootstrap so "dispatch" keeps that one meaning.

The Linked sections rule leaves `SKILL.md`: a mode is followed from its bundle, which carries each linked section under its own heading, and the Prerequisites it named are gone from the tree. The migration epic carries this as W11 ([#276](https://github.com/m2ux/prosiform/pull/276)), observed by AC14 and AC15.

## D11 — Rules, conventions and bootstrap sit beside the entry point

The user dictated the skill's structure for the `pf` migration. `rules.md`, `conventions.md` and `bootstrap.md` sit beside `SKILL.md`, which keeps its preamble, Modes and Dependencies. Its Modes section opens with "Read the [bootstrap](bootstrap.md) instructions then select the mode as appropriate to fulfill the user request:". Every mode's preamble closes with "Follow [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.", so every mode bundle carries both files, and the Procedure no longer states that its main path meets Outcomes. The largest bundle, `deliver-mode`, is 246,141 bytes against 262,144.

Every guideline that conflicts with that structure is removed or restated: Prerequisites sections, rules held in `SKILL.md`, the entry point supplying Conventions before mode selection, and reading linked sections by hand. The example's links therefore no longer equal the copied skill's at every place, so the migration epic drops the criterion holding them equal; a link copied from the skill still keeps its destination.

`pf` reports nothing about an entry reference resolving to the destination the entry line links it to: the user ruled such references allowed, so a successful run writes only the bundle unless it names a resource. The design's Entry destinations clause leaves with the warning.

The migration epic carries these as W12 ([#278](https://github.com/m2ux/prosiform/pull/278)), observed by AC16, and W13 ([#277](https://github.com/m2ux/prosiform/pull/277)), observed by AC17 to AC19.

## D12 — The source states the instruction; the bundle is shaped for the agent following it

A routing test sent a fresh agent from `SKILL.md` through `bootstrap.md` to the Sync bundle, which it built from `example/work-planner`, read whole and stopped before any step. What it tripped on, and a review of the bundle's layout, led to these rulings.

- **The preamble carries the instruction.** Every mode's preamble closes with "Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met." The instruction can differ per bundle, so `pf` emits no opening line of its own, and the `prosiform.dispatch` key, whose text followed that line, is gone with it. A bundle is ordinary Markdown: bundling a bundle is legal, its resolved links stay as they are and only its deferred links expand. Expanding one can bring in a document the bundle already holds, under a second heading, and that is accepted.
- **Guidelines serve revision.** A rule a running mode needs sits in `rules.md` or `conventions.md`. The interview rules moved there, and every runtime link to them is a plain link.
- **Operations are applied and procedures followed.** A link to an artifact operation opens with Apply, a link to a mode, protocol or procedure section with Follow, and a link to a command keeps Run. A mode's command specifications sit under Commands.
- **A root bounds inclusion and names nothing.** A file that declares no group is headed by its own H1, or by its working-directory-relative path without one, and the default output name is the entry's working-directory-relative path.
- **Each artifact is one block.** Artifacts group at depth 1 under an Artifacts heading. Merging them by section kind at depth 2 put every artifact's material under the mode's own title and split each artifact across three regions; the Sync bundle's median link jump fell from 899 lines to 147.
- **Order follows the links.** Groups, and the members inside each group, follow the order the bundle first links them, so an author sets order by listing links in the preamble. Rules and Conventions follow each mode's own sections.
- **An anomaly warns.** An entry reference resolving to its own heading reports nothing. Coinciding generated headings, file or member, publish with `W_COINCIDENT_HEADING` and anchors told apart by numbering; repeated headings an author writes do not warn.

Deferred: installing `pf` on this host waits for the epic to reach `main`; a usage fixture showing deferred links is the debt epic's W13; generic heading names in the skill wait for its refactor; script paths naming `skills/work-planner` hold until the example becomes the production skill.

The migration epic carries these as W14 to W21 ([#279](https://github.com/m2ux/prosiform/pull/279), [#280](https://github.com/m2ux/prosiform/pull/280), [#283](https://github.com/m2ux/prosiform/pull/283), [#281](https://github.com/m2ux/prosiform/pull/281), [#282](https://github.com/m2ux/prosiform/pull/282), [#284](https://github.com/m2ux/prosiform/pull/284), [#285](https://github.com/m2ux/prosiform/pull/285), [#286](https://github.com/m2ux/prosiform/pull/286)), observed by AC20 to AC27. AC5 states which files declare a group, and AC25 the artifacts' layout. Its criteria are renumbered from AC14; its row ids keep their numbers.
