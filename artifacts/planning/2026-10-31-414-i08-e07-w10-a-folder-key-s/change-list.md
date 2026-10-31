# Change List — W10 A Folder Key's Absent Substitute and Unused Report

> Plan changes · Created 2026-10-31

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W10 work item](../2026-10-30-414-i05-e09-mock-substitution/w10.md), `AC28`'s fixture | The epic record states one fixture for `AC28`: `guide.md` links one reference, `rules/red.md`, and the run passes a used folder key beside an unused one. That fixture proves the warning's wording and that the run publishes, but not the row's other claim — that a folder matching only text is used by nothing — and not the claim that the used set holds a key once. The fixture as landed links two references and carries three entries: `rules/` answering two references (so the key is held once and states no warning), `notes/` answering only a `notes/note.txt` the run classifies as text, and `other/` answering nothing. Two `W_MOCK_UNUSED` are declared, so both readings of "no compiled reference reached it" are in one manifest. |
| Folded work | [W10 work item](../2026-10-30-414-i05-e09-mock-substitution/w10.md), the reading the row was asked to settle | The work item asks whether a folder matching only text is a warning case or a documented non-event. Settled as a **warning case**, and the warning follows from the mechanism rather than being added beside it: `Substitution.redirect` marks a key served only where the substitute it derived is a Markdown document, because a redirect to a resource is one the bundle does not carry out. A folder whose every derived path is a resource therefore answered no compiled reference, and `unserved` reports it as it reports a key nothing named. `w10.md` records the decision and the alternative refused. |
| Folded work | [W10 work item](../2026-10-30-414-i05-e09-mock-substitution/w10.md), the substitute's own record | The row needed the refusal to name the key, and by the time `read_document` raises the absence the key is out of scope. `Reference` gains a `folder` field carrying the key as its caller wrote it, set where the lookup derives the reference. The field is also the only place the caller's spelling survives to the diagnostic, so the message names `rules/` with its separator rather than the normalized `rules`. |
| Folded work | [W10 work item](../2026-10-30-414-i05-e09-mock-substitution/w10.md), the redirect's effect | `Substitution.redirect` now takes effect only where the substitute names a Markdown document. Without it the text case records a substitution for a redirect the bundle never performs — which is the fault T2 shows the base has — and `W_MOCK_SUBSTITUTED` would name a substitution the published link does not show. A document key's substitute is already held to naming a Markdown document when the mapping is read, so the guard is reached only by a folder key's derived remainder. |
| Folded work | [W10 record](../../../README.md), reserved folder | `w10.md`, `validation.md` and `change-list.md` are registered in the folder's `README.md` Artifacts table. |
| Epic row | [#414](https://github.com/m2ux/prosiform/issues/414), row `W10` | `sync.py` mapped `W10` to #469 and reported the row delivered once #469 merged, and `AC27` and `AC28` were ticked from the ready-to-verify report it gave. The row link and the two criteria were published from the sync's own output rather than rewritten. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Re-prioritisation | `AC29`, `W11` | `AC29` requires the option's documented row and the help string to state the folder form and the precedence, in both directions. This row changes neither, and `W11` is the only row naming the criterion. This row does not claim it. Recommend `W11` lands the row against the behaviour `W09` and this row provide. |
| Folded work | `fixtures.md`, the stub-declaration rule | `fixtures.md` states every stub declares because a redirect reaches a document under the [I05:E11](https://github.com/m2ux/prosiform/issues/434) rule. On this branch that rule is not in force and a declaration bounds inclusion no further than the writing source's root already does, so the rule reads as current fact where it is a prediction. Recommend `I05:E11`, which lands the rule, restates it beside the boundary it derives. Both fixtures here declare `prosiform` on every document from the first for the same reason `W09`'s do. |

## No change

- **The design's clause.** `Link classification and resource handling — The substitution mapping` is what both fixtures declare. The pin does not move and no clause is added, which is why the uncovered clause count is unchanged at 54 and the stated clause count at 305.
- **The `-m` grammar and the option's identity.** No new shape is accepted and no existing shape is refused differently. The folder pairing's two refusals, `W09`'s, answer as they did.
- **The document key's absent-target message.** A document key naming a path the run does not hold is still refused with the one-part message every absent target carries, as `T4` records. The three-part message is the folder key's alone, because the path it names is the one nobody wrote.
- **The `W_MOCK_SUBSTITUTED` record's key.** It is still keyed by the served key and the substitute's document, as `W09` left it. This row changes only which references reach the record, not how one is keyed.
- **The independent row pairs.** `joins.md` states which rows take separate pull requests, and this row's neighbours are unchanged. `W11` depends on this row and lands after it.

## Delivery

| Resource | Value |
| --- | --- |
| Pull request | [#469 A Folder Key's Absent Substitute and Unused Report](https://github.com/m2ux/prosiform/pull/469) |
| Base | `i08/e07/main` at `40a3b947` |
| Head | `b4a39250` |
| Merged | `01653cf8725ced5ff737de32dc8cd925ebb62d8a`, `merge_method=merge` |
| Epic row | `W10` reads `✓`, and `AC27` and `AC28` tick with it |
| Development link | **Blocked:** #414 holds ten manual references and `addCloseIssueReferences` answers `Issue exceeds manual reference limit`. #469 is the pull request awaiting one. |

## Debt this row leaves

- **`AC29`'s documented row and help string.** Recommended for `W11` rather than taken here, and recorded under Held above.
- **`fixtures.md`'s stub-declaration rule** reads as current fact on a branch where inclusion is still bounded by the writing source's root. Recommended for `I05:E11`'s record rather than restated here.
- **The Development link for #469.** Blocked at GitHub's ceiling, so the pull request closes nothing and the row's delivery is recorded by its link alone. Clearing it needs a slot freed on #414 by whoever owns one of the ten references held there, after which the mutation is one call: issue `I_kwDOVNSvEM8AAAABbF3srA`, pull request `PR_kwDOVNSvEM8AAAABL9uVFQ`.
- **Eleven epic-row title conflicts the sync reports.** `sync.py` reports `W00`–`W09` and `W12` as linking pull requests whose titles do not name `I08:E07`. Each merged under the epic's old reference, `[I05:E09]`, before the reap of the parent issue, so the conflict is a fact about the titles rather than about the delivery. #469 is the first row whose title names the epic's current reference. It belongs to whoever owns the epic's record, not to this row.
- **`W01` and `W07` Done cells.** `sync.py` reports `AC6`, `AC11` and `AC20` unticked on rows it otherwise reads as delivered, and its rewrite clears their ticks. That is a pre-existing disagreement between the criteria and the rows, not this row's, so the two cells are left as they stood and the criterion ticks are untouched.
