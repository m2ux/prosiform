# Change List — W02 Key and Self-Mock Refusals

> Plan changes · Created 2026-10-30

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W02 work item](../2026-10-30-414-i05-e09-mock-substitution/w02.md), Fixtures table | Each fixture's manifest is recorded as declaring four clauses rather than the one the epic's `fixtures.md` names as the family's obligation. The mapping's clause is required of every mock fixture; the `CLI contract` heading, the option's row and the exit status are the rules a refusing run actually reaches, and naming them is what makes the refusal's outcome fixtured rather than only its cause. |
| Folded work | [W02 work item](../2026-10-30-414-i05-e09-mock-substitution/w02.md), `## Additions from review` | Two findings the plan could not state are recorded: that the authored spelling is kept beside the identity set because a set alone cannot say which two options to edit, and that a fragment-only key is refused ahead of the self-mock comparison so a pair naming no document reports its own fault rather than a self-mock between two empty identities. |
| Folded work | [W02 record](../../README.md), reserved folder | `w02.md`, `validation.md` and `change-list.md` are registered in the folder's `README.md` Artifacts table. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | Row `W02` links the pull request and is ticked done, with `AC9`, `AC10` and `AC23` ticked. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Folded work | [W02 work item](../2026-10-30-414-i05-e09-mock-substitution/README.md), the epic's `Refused` row | The epic record's mapping table lists a fourth refusal, "a value naming no Markdown document", which no criterion covers and no row of the epic owns. It is absent from the build: `pf -c -m rules.md=notes.txt guide.md` exits `0` and reports nothing, and the `guide.md` that links `rules.md` publishes `[rules](rules.md)` as text, so the entry read as a redirect and took effect as nothing. It is not W02's: `AC9`, `AC10` and `AC23` are the three shapes that state nothing about the mapping, and this one states a substitute the run will not carry, which is a different fault. Raised as [#432](https://github.com/m2ux/prosiform/issues/432) with `tech-debt` and three criteria. Left **unplaced**: it needs a home in an epic's Work Breakdown with an epic-numbered criterion, and the only candidate is I05:E09, whose planning this session does not own and whose fixture inventory names seventeen fixtures. Placing it there needs the epic's next planning pass. |
| Folded work | [W02 work item](../2026-10-30-414-i05-e09-mock-substitution/w02.md), the two-key fixture | `fixtures/mock/a-duplicate-key-is-refused` gives `-m rules.md=a.md -m ./rules.md=b.md`, whose substitutes do not exist. That is deliberate: the refusal precedes any read, so a missing substitute is what proves the ordering. A fixture whose substitutes existed would pass whether or not the refusal ran, because no read happens either way. Recommend keeping the absent substitutes as the ordering's own evidence. |
| Folded work | `checks/corpus.py` | The corpus check takes no fixture-family argument, so a single family cannot be run on its own; the whole 355-fixture corpus runs in about 40 seconds. Not a defect for this row and not measured by anything the row names. Recommend no change. |

## No change

- **The refusals' code.** All three carry `E_INVALID_USAGE`, which the contract gives every command line it refuses, so a caller reading the code has one remedy. The message tells the three apart, and no new code is added to the schema's error catalogue.
- **The design and the pin.** The clause at `a59b62fc` already states all three refusals in prose — "Two keys normalizing to one identity, a key and its value normalizing to one identity, a key carrying no document … are invalid usage". This row makes the build meet it and moves no pin.
- **`closure.py`.** The mapping value and its lookup are unchanged. The refusals read the pairs the grammar produced, so no part of the mapping's own type knows what a malformed mapping is.
- **The option's grammar.** `-m`, `--mock` and the `ORIGINAL=ALTERNATIVE` split are unchanged, and `make invocation` reports the same 30 statements.
- **The independent row pairs.** `joins.md` states which rows take separate pull requests, and this row's neighbours are unchanged. W04 lands its two warnings on the same component and its own fixture directories, and neither row's refusals or warnings depend on the other's.
