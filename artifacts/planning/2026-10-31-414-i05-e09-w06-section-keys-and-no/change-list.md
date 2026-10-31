# Change List — W06 Section Keys and No Chaining

> Plan changes · Created 2026-10-31

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W06 work item](../2026-10-30-414-i05-e09-mock-substitution/w06.md), Test row | The Test row names `src/tests/test_mock.py` "for a link naming a section its key does not", which is one case. The row lands five, because the fixture it names proves the run's output and not the lookup's answer: a section key's unserved state, the substitute's own section, and the end-to-end pair are three separate facts. The row's Test entry now names them as the one table cell it was, and `validation.md` T5 lists them. |
| Folded work | [W06 work item](../2026-10-30-414-i05-e09-mock-substitution/w06.md), Fixtures table | `a-document-key-and-a-section-key-together` declared "Each link compiles the substitute its exact key names" without stating what the run says about them. Both keys serve a reference, so the run states two `W_MOCK_SUBSTITUTED`; the row now says so, because a fixture declaring one where the build emits two fails on the diagnostic count and the failure reads as a defect in the lookup. |
| Folded work | [W06 work item](../2026-10-30-414-i05-e09-mock-substitution/w06.md), `a-fragment-key-redirects-one-section` | The row's fixture text describes `stand-in.md` as "compiled", which does not say which of its sections the bundle carries. The fixture as landed redirects a section to a whole substitute, so the substitute's `## Escalation` is the section the reference's fragment is read against. The row states that, and T6 records the neighbouring case where the substitute's own fragment wins instead. |
| Folded work | [W06 work item](../2026-10-30-414-i05-e09-mock-substitution/w06.md), `## Additions from review` | Four findings the plan could not state are recorded as a table: that no fixture held the lookup's order before this row; that the row's scene did not say which section wins when a substitute carries one; that "no chaining" reads as a guard and is better stated as a structural impossibility with the unused-key warning as its observable half; and that a substitute lacking the section its key names is a resolution defect rather than a whole-document read. |
| Folded work | [W06 record](README.md), reserved folder | The Executive Summary, the Artifacts table and the Links table are written, `w06.md`, `validation.md` and `change-list.md` are registered, and the delivered pull request is linked. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | Row `W06` links pull request [#437](https://github.com/m2ux/prosiform/pull/437) and is ticked done, with `AC3`, `AC12` and `AC14` ticked. `sync.py` reports `linked: W06 → #437`, `ticked: AC3, AC12, AC14`, `done: W06`, and the epic stays open for W03, W05, W07, W08 and W10. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414), `W06`, `AC3`, `AC12`, `AC14` | All three criteria are delivered by this row and ticked on the epic. **No plan change is held against them.** The criteria table at the end of this file records what each fixture states and what this row added. |
| Folded work | [W06 work item](../2026-10-30-414-i05-e09-mock-substitution/w06.md), Component | The row names `closure.py` as its component, and this session changed no line of it. W01's lookup already asks the exact identity before the document-wide one, already takes the substitute's fragment where the key carries one, and already marks the exact key served; the epic's review moved AC14 to this row so the mechanism would not be written twice. Recommend no change: the component is where the row's subject lives, and a row that confirms behaviour another row landed touches it without rewriting it. A future reader looking for the section rule should find it there and find the fixtures here. |
| Folded work | `invocation.md`, `docs/references.md`, `docs/glossary.md` | All three already state that a key carrying a fragment redirects that section alone and takes precedence over a key naming the whole document, and the glossary states that a substitute which is also a key is read from disk rather than followed again. No documentation claim in the tree describes the old behaviour, so nothing was retired. |
| Folded work | `fixtures/manifest.schema.json` | No schema change. The three fixtures declare `W_MOCK_SUBSTITUTED` and `W_MOCK_UNUSED`, both of which W04 added to the warning catalogue, and the declaration's `location` support is W04's. |

## No change

- **The lookup.** An immutable value with one lookup, exact `(path, fragment)` then `(path, None)`, is what W01 landed and what this row observed. Writing a second lookup would give one rule two implementations, which is the defect the epic's review removed.
- **The design's clause.** `Link classification and resource handling — The substitution mapping` is what every mock fixture declares. Its name is unchanged at `827b66fc`, the pin W04 set, and no fixture declaration names another clause.
- **`-m`, `--mock`.** Both spellings, the reach and the refusals are W01's and W02's. This row adds no option and refuses no mapping shape.
- **The fixture names.** `a-fragment-key-redirects-one-section`, `a-document-key-and-a-section-key-together` and `a-substitute-that-is-a-key-is-not-redirected-again` are the names `fixtures.md` and the epic give, landed unchanged.
- **The independent row pairs.** `joins.md` states that W06 takes its own pull request against each of W03, W07 and W08. This session stayed inside `fixtures/mock/` and `src/tests/test_mock.py`, so no sibling's component was touched.

## Criteria

| Criterion | What delivers it | Fixture |
| --- | --- | --- |
| `AC3` | A section key redirects the section it names and leaves the rest of its document real. | `a-fragment-key-redirects-one-section` |
| `AC12` | A substitute whose own path is a key is read from disk, and the key naming it is reported unused. | `a-substitute-that-is-a-key-is-not-redirected-again` |
| `AC14` | A document key and a section key of one document both serve their references, the narrower taking the section. | `a-document-key-and-a-section-key-together` |
