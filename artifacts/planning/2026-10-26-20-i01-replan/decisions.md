# Re-plan Decisions

## R1 — E01 W00 Is Superseded by the Demonstration

E01 W00 was raised by [D61](../2026-10-17-prosiform-v1/decisions.md#d61--the-emission-the-build-alone-changed-takes-a-preparatory-row-under-e01-and-e08-is-cancelled) to state the bundle's opening sentence and the first entry document's place in the design, and to return `make check` to green. The demonstration resolved all three another way:

- I02:E00:W15 removed the opening sentence. The design's Clean Markdown clause and `invocation.md` state that a bundle opens on its first group's content.
- I02:E02:W10 stated the parent arrangement — a titled entry member opens its group with its own title and preamble, its sections leading — in the design's Grouping clauses, `invocation.md` and `docs/glossary.md`.
- I02:E01:W04 ran the checks and the corpus green at `demo/i02`.

W00 and its criteria AC8, AC9 and AC10 leave E01. No pull request names W00, so W01 drops the edge and nothing is renumbered. The work-item file is removed from the initiative record.

## R2 — E04 Section Composition Is Cancelled

Issue 215 was closed as completed on 2026-10-24 with none of its ten rows delivered and none of its seventeen criteria ticked, and no decision recorded the closure. The design carries no section-composition clause.

The epic is re-closed as not planned. Its row leaves the initiative and AC11 is retired with its id unused, following [D60](../2026-10-17-prosiform-v1/decisions.md#d60--the-clear-up-is-rebuilt-on-the-design-and-a-criterion-another-epic-states-is-retired). Issue 214 stays open as the requirements source for a later stage, and the planning at `2026-10-22-214-section-composition/` stays where it is. A Non-Goal states that this stage adds no inline section composition.

## R3 — E08 Inherited Roots Is Recorded as Not Planned

D61 cancelled E08, and issue 233 was closed as completed. The design now states the opposite of AC14: an absent root uses the captured invocation working directory, linked sources included. The issue is re-closed as not planned, its row leaves the initiative, and AC14 is retired with its id unused. A Non-Goal states that this stage adds no root inheritance from a reaching parent.

## R4 — The Exposure Set Holds the Example and the Skills in Use

The demonstration bundled `example/work-planner`, a full copy of a real skill, mode by mode on a tagged revision. The workspace skills agents invoke are the sources real use reaches. The exposure set declares both, so the freeze needs the demonstrated tree and real use together.

I01 AC7 and E00 AC6 name both. E00 gains W04, which records each demonstration mode bundle as a run and enters the measurements the demonstration recorded outside a ledger — the Understand Mode dispatch saving and the route that pushed `modes/deliver-mode.md` past the default budget — as entries citing `demo/i02`. The freeze's W02 depends on W04 in place of W03, which W04 implies.

## R5 — E01 W04 Applies the Example's Pattern to the Workspace Skills

The demonstration removed the example's prerequisite sections, stated its compile command and symbols in `bootstrap.md`, and opened mode links with `↳`. The workspace skills it was copied from still carry their prerequisite lists. W04 applies the example's pattern to those skills, gated as before on a recorded run supplying what each list named.

The skills live in another repository and the initiative opens no issue or pull request there. The skill edits land in that repository directly; the removal record and the gating runs are kept here, and AC5 to AC7 are judged from them.

## R6 — Parent Merge Takes Its Own Epic, E12

Issue 234 states grouping owned by the file that writes the link. The demonstration deferred it, recording that the member-declared model produces a resolving bundle without it. It is a contract change, so it belongs to refinement, and it takes an epic as the earlier contract extensions did. I01 gains AC17 and R8 marks issue 234 as a source.

E11 is not reused, because pull requests delivered under `I01:E11` before that epic became I02:E00. The new epic is E12. The freeze, which no pull request names, moves from E12 to E13 so its number follows every epic it depends on, and its W02 depends on E12 W03.

Issue 234's references name `example/my-skill` on a deleted branch and a root rule that depended on E08. The epic restates its problem against `example/work-planner` and leaves root resolution as the design states it.

## R7 — A Parent Assigns Links to Groups by Heading

Issue 234 states that a parent can name more than one group and that a directory name assigns no group, and does not state how the parent says which link joins which group. A group rule names a heading of the file that declares it, and the links written under that heading join that group. The assignment reads from the structure an author already writes and adds no list to keep in step with the body. A list of targets in metadata was rejected because it drifts from the body; a target folder was rejected because issue 234 assigns no group by directory.

## R8 — Corrected Delivery Records

- E09 is closed with every row delivered and every criterion ticked, so its row takes Done and AC15 is ticked.
- E03 W11 (issue 204) was closed as completed with its criterion unticked and no pull request of its own. `checks/vocabulary.py` on `main` resolves the contract as `origin/engineering` at run time and names that ref, not the revision it read, so AC12 does not hold. The issue is reopened and the row stays open.
- Issue 31 is closed and E10 carries its requirement. The repository is public and `main` is unprotected, so E10's Problem holds as written.

## R9 — Parent Merge Waits for the Ledger

E12 was closed as not planned before any work landed, and AC17 is retired with its id unused. Two premises failed when the epic was read against the example:

- **Assignment by heading cannot reproduce the example's groups.** A mode writes its artifact and protocol links together in the numbered steps of one Procedure section, so a group rule naming a heading would gather every link into one group. R7 holds for no tree the example contains.
- **A file reached from several parents is the common case.** Most artifacts are linked from several modes and protocols. Issue 234 places that outside its scope, and composing each child inside its parent would repeat a shared file or need an ownership rule no criterion stated.

The member-declared model bundles the example with every link resolving, so no observed failure motivates the change. Issue 234 stays open as a candidate finding: it enters the ledger once the ledger exists, and becomes a revision only where real use shows the member-declared model failing. Any later plan settles link assignment and shared-file ownership before stating the rule.

The epic bases `i01/e12/main` and `i01/e12/engineering` were created and deleted unused, and the W01 hold was released with its record.
