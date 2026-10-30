# Change List — W00 Design Clause, Invocation Rules and Pin

> Plan changes · Created 2026-10-30

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W00 work item](../2026-10-30-414-i05-e09-mock-substitution/w00.md) | The vocabulary bullet names `docs/glossary.md` as the definitions' home and the pinned design as where the words are admitted, replacing `docs/corpus-vocabulary.md`, which no check reads. |
| Folded work | [W00 work item](../2026-10-30-414-i05-e09-mock-substitution/w00.md) | The two-pull-request bullet names the epic base rather than `main` as where the pin, the rule and the entries land, matching the delivery branches this epic's rows use. |
| Folded work | [W00 work item](../2026-10-30-414-i05-e09-mock-substitution/w00.md) | The test row adds `make check` on the branch head and a temporary declaration naming the clause, so the row's evidence shows the report reading the clause from the pin rather than from a branch the clause was written on. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | Row `W00` now links pull request [#425](https://github.com/m2ux/prosiform/pull/425) and is ticked done, with `AC16` and `AC17` ticked. |
| Folded work | [W01 work item](../2026-10-30-414-i05-e09-mock-substitution/w01.md) | The option bullet gains the row it needs in the design's own `CLI contract` table. `make conformance` reads each option row there as a clause, so the option cannot be stated in the contract by the link-classification rule alone. |
| Folded work | [W04 work item](../2026-10-30-414-i05-e09-mock-substitution/w04.md) | Both warning codes are folded into the design's exit-status section and the manifest schema's warning catalogue. A fixture declaring `W_MOCK_SUBSTITUTED` or `W_MOCK_UNUSED` fails schema validation today, and `make conformance` requires the design and the schema to name one set of codes. |
| Folded work | [W09 work item](../2026-10-30-414-i05-e09-mock-substitution/w09.md) | The classification detail moves to `docs/references.md`, the page the guide links for classification, so the matching rule has one home; the guide keeps the one-line form. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | The clause's four refusals corrected from "a key naming no document" to "a key carrying no document", an absent key admitted, and the mapping stated to apply under `-c`, as [#427](https://github.com/m2ux/prosiform/pull/427) records. The row keeps its link to #425: the fix belongs to the delivery that row names, and a second link on one row is a second delivery. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414), `AC17` | The criterion reads "every fixture in this epic names a clause the pinned design carries". Only the clause's own row could show that here; the criterion is fully observable only once W01 lands the first mock fixture. Recommend re-reading it at the epic's review rather than rewording it now, since the wording is what makes the later rows' obligations explicit. |

## No change

- **The clause's name.** `Link classification and resource handling — The substitution mapping` is what every later fixture declares. It was settled in this session and lands in the design, the bundles and the fixture inventory alike.
- **The design's location and branch.** The amendment is `578093687a55c7ed2dc1110b7347fa80a4f6f0ce` on `engineering`, and `f723a85dbe5fd2a3e379b951c2dfb5c58670f5e6` is the corrected revision the pin now names.
- **The option row's `invocation.md` row.** `-m` gains no `invocation.md` row here, which the plan already states; `make invocation` compares the table with the help output in both directions, so a row now would fail as an option no command offers. The design's own `CLI contract` table is held to nothing but its own prose, which is why its row is folded into W01.
