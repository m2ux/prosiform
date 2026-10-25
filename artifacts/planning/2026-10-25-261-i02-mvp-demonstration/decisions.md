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
