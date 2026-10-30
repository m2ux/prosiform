# Corpus Survey — Numbered Steps

The work-planner example corpus at `example/work-planner/` on `main` at `9851615`, read for numbered procedure steps outside code blocks. Counts come from a script reading each Markdown file line by line, a step being a line opening `<n>. ` at column 0 and a procedure being a list that opens at `1.`.

## Size

| Tree | Files with steps | Procedures | Steps |
| --- | --- | --- | --- |
| `modes/` | 10 | 12 | 86 |
| `protocols/` | 12 | 12 | 55 |
| `artifacts/` | 31 | 118 | 423 |
| **Total** | **53** | **142** | **564** |

The corpus holds 59 Markdown files; the six without steps are `SKILL.md`, `bootstrap.md`, `conventions.md`, `guidelines.md`, `rules.md` and one reference. No step list nests another numbered list.

The largest artifact procedures: `pull-request.md` (54 steps, 14 procedures), `issue.md` (46, 13), `board.md` (37, 10), `delivery-branches.md` (37, 8), `epic-issue-body.md` (33, 9).

## Shape Today

- **Mode and protocol steps carry a bold action label.**
  `1. **Select the board.**` then the instruction on the next line; the label supplies a heading's text.
- **Artifact operation steps carry no label.**
  The corpus guidelines' Operation steps rule forbids one, so each artifact step needs a title written for it.
- **Procedures sit at two levels.**
  A mode's `## Procedure` holds its steps and may hold `###` sub-procedures (`deliver-mode.md`: Run Delivery Session, Hoist Arising Issue); an artifact operation is a `###` section.
- **Two `####` sections sit under procedures today.**
  `issue-body.md` Verifiable, and `delivery-evidence.md` Board Reads.

## References to Steps

About 50 prose references outside the guidelines name a step by number or by role: `step 4` (`plan-mode.md`, `epic-closure.md`, `acceptance-criteria.md`), `the review step`, `the report step`, `this selection step`. None is a link, since a list item roots no anchor.

## Rules Keyed on Numbered Steps

- `example/guidelines.md`: a procedure is "a top-level section carrying a numbered step", and a Procedure is "numbered steps, each opening with a bold label".
- `example/work-planner/guidelines.md`: Numbered steps, Sub-bullets, Separate actions, Procedure steps and Operation steps all state the numbered form.
- `pf`: `W_DISPATCH_NOT_PROCEDURAL` warns on a dispatched target carrying no ordered list item; eight example files are dispatched targets (`sync-mode`, `advance-mode`, `hoist-mode`, `understand-mode`, `task-merge`, `delivery-recording`, `issue-placement`, `epic-closure`).

## Consumers of the Example

- **Usage-example fixtures.**
  Seven fixtures under `fixtures/usage-example/` link `source` to this tree, so every converted file a fixture's entry reaches changes that fixture's expected bundle.
- **Worked examples.**
  `example/README.md` quotes `plan-mode.md` step 6 as an exact excerpt.
- **`make links`.**
  Reads every tracked document, the example among them, so a step anchor a link names must exist.

## The Skill's Own Corpus

`.claude/skills/work-planner/` in the workspace repository holds 49 Markdown files with 118 procedures and 477 steps (modes 95, protocols 24, artifacts 358). It has diverged from the example: six protocols against twelve, `Run`/`Call` verbs against `Apply`/`Follow`, and no bootstrap. Two of its artifacts are copied byte for byte into `fixtures/real-source/` and held to their originals outside the corpus.
