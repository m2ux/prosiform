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
| Pull request | _pending_ |
| Base | `i08/e07/main` at `40a3b947` |
| Head | `b4a39250` |
| Merged | _pending_ |
| Epic row | _pending_ |
| Development link | _pending_ |

## Debt this row leaves

- **`AC29`'s documented row and help string.** Recommended for `W11` rather than taken here, and recorded under Held above.
- **`fixtures.md`'s stub-declaration rule** reads as current fact on a branch where inclusion is still bounded by the writing source's root. Recommended for `I05:E11`'s record rather than restated here.
