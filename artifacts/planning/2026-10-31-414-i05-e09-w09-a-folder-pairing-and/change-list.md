# Change List — W09 A Folder Pairing and Its Precedence

> Plan changes · Created 2026-10-31

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W09 work item](../2026-10-30-414-i05-e09-mock-substitution/w09.md), `AC30`, epic record `fixtures.md` | `AC30` names two invalid shapes — a pair with a separator on one side and a folder side carrying a section — and the epic record's fixture inventory named one fixture for both. The second is landed as its own fixture, `fixtures/mock/a-folder-key-carrying-a-section-is-refused`, because one fixture cannot state two different refusals: the runner compares one exit status and one diagnostic list, and a manifest naming two values states one run. `fixtures.md` records three fixtures for this row; four land, and the fourth is named in the work item's Fixtures table. |
| Folded work | [W09 work item](../2026-10-30-414-i05-e09-mock-substitution/w09.md), the redirected-target record | `AC7` states one `W_MOCK_SUBSTITUTED` per redirected *target*, and a record kept under the served key alone collapses a key's several targets into the first. A document key states one target however many references name it — a document and one of its sections included — so the collapse was invisible. A folder key states one time per document it answers, so it would have hidden all but one of a folder's substitutions. The record is keyed by the served key and the substitute's document. The existing `an-exact-key-beats-a-folder-key` and `a-folder-key-redirects-each-reference-under-it` fixtures both depend on this: each declares two and three warnings where the key alone would give one and one. |
| Folded work | [W09 work item](../2026-10-30-414-i05-e09-mock-substitution/w09.md), the marker's reader | The row states the separator is read "before normalisation" without saying from what. Reading it from the whole side as `text.endswith("/")` refuses `rules/#checks` as a document rather than as a folder carrying a section, and reads `rules/?q` as neither. The marker is read from `components(text).path`, so it is the path that states the folder and a section or query after it does not hide it. |
| Folded work | [W09 work item](../2026-10-30-414-i05-e09-w09-a-folder-pairing-and/w09.md), the fixtures | The epic record states every stub declares `prosiform` so no fixture changes when [I05:E11](https://github.com/m2ux/prosiform/issues/434) makes inclusion a property of the declaration. Every document of each fixture declares `prosiform: {}` from the first. On this branch the declaration bounds inclusion no further than the writing source's root already does; each fixture was run with and without it and expects the same bundle, and only the link's line moved, which the frontmatter shifts. Both manifests declare the coordinate the declaring tree produces. |
| Folded work | [W09 record](../../../README.md), reserved folder | `w09.md`, `validation.md` and `change-list.md` are registered in the folder's `README.md` Artifacts table. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Re-prioritisation | `AC29`, `W11` | `AC29` requires the option's documented row and help string to state the folder form and the precedence, in both directions, and no task owns the option's documented row. `fixtures.md`'s AC15 note places that row with `W01`, and `W01`'s change list folded it there; the folder form and the precedence were not in it. `W11` is the only row naming `AC29`. This row does not claim it. Recommend `W11` lands both the row and the help string, against the behaviour this row now provides. |
| Task creation | A row for the fourth fixture | `AC30`'s second shape is specified in the work item and landed with this row. It is a fourth fixture under a task whose plan names three. That is the same shape as the folded item above rather than a new unit — recommend no new task. |
| Folded work | `fixtures.md`, the stub-declaration rule | `fixtures.md` states every stub declares because a redirect reaches a document under the [I05:E11](https://github.com/m2ux/prosiform/issues/434) rule. On this branch that rule is not in force and a declaration bounds inclusion no further than the writing source's root already does, so the rule reads as current fact where it is a prediction. Recommend `I05:E11`, which lands the rule, restates it beside the boundary it derives — with the row that makes it true, not here. |

## No change

- **The design's clause.** `Link classification and resource handling — The substitution mapping` is what every mock fixture declares, and it already states the folder pairing: "a folder key matches every reference whose normalized path sits under it, the substitute folder takes the same remainder, and the reference keeps its section". The pin does not move and no clause is added, which is why the uncovered clause count is unchanged at 54.
- **The `-m` grammar and the option's identity.** `ORIGINAL=ALTERNATIVE`, both sides from the working directory, both read by the reference grammar, repeatable, appended once per pairing. A folder side is a shape of the value and neither reorganises it.
- **The four refusals `W01`, `W02` and `W12` landed.** A document key, a self-mock, a key carrying no document and a value naming no Markdown document answer as they did. The folder pairing adds a fifth and a sixth shape and changes none of them; the two tests of a pair's own sides still answer before the two that compare them.
- **The fixture names the criteria give.** `a-folder-key-redirects-each-reference-under-it`, `an-exact-key-beats-a-folder-key`, `a-half-folder-pair-is-refused` and `a-folder-key-carrying-a-section-is-refused` are the names `AC25`, `AC26` and `AC30` state.
- **The independent row pairs.** `joins.md` states which rows take separate pull requests, and this row's neighbours are unchanged. `W10` and `W11` depend on this row and land after it.

## Delivery

| Resource | Value |
| --- | --- |
| Branch | `i05/e09/w09-a-folder-pairing-and` |
| Head | `30a669b2` |
| Base | `i05/e09/main` at `3091c65b` |

The pull request, the Development link, the epic row and the merge are recorded in `validation.md` T13.
