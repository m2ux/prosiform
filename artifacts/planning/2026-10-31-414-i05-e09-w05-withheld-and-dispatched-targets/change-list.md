# Change List — W05 Withheld and Dispatched Targets

> Plan changes · Created 2026-10-31

Every plan change this session applied, and every one it held, under the allowance the delivery brief names: task creation, epic creation, migration, re-prioritisation and folded work.

## Applied

| Kind | Subject | Option applied |
| --- | --- | --- |
| Folded work | [W05 work item](../2026-10-30-414-i05-e09-mock-substitution/w05.md), this record's `w05.md` | The Plan part asked whether the substitute's own fragment or the authored one is published, and the Proposal answered "the substitute's own fragment … so a substitute carrying one publishes that section" without the code doing it. `closure.rebased` published `found.path`, which is the substitute's, with `components(text).fragment`, which is the author's. The contract's rule for a deferred destination is *Retain the resolved fragment when present*, so the row's answer was right and its implementation was one field short. The record's work item states the resolved fragment and the review table records why. |
| Folded work | [W05 work item](../2026-10-30-414-i05-e09-mock-substitution/w05.md) | The Problem gains the published destination as the place a redirect is lost unobserved: it is the one point where the resolution is written down rather than read, so no stage disagrees while the destination names a section the substitute need not carry. |
| Folded work | This record's `w05.md`, `## Additions from review` | Three statements the epic's work item could not make: that the published fragment is the resolved one, that a dispatched and a parallel-dispatched target take no corpus fixture (which `fixtures.md` records), and that the run's heading check is asked of the substitute. |
| Folded work | `src/tests/test_mock.py` | Seven cases added for the row's three withheld paths: a deferred destination, a section key's deferred destination and the later run following it, the heading check asked of the substitute, a dispatched target, a parallel-dispatched target, and the candidate comparison. The three the change corrects fail against the pre-change `closure.py`; the two dispatch cases pass on both trees, which is the plan's own recorded finding. |
| Folded work | [This record](../../../README.md), reserved folder | `w05.md`, `validation.md` and `change-list.md` are registered in the folder's `README.md` Artifacts table. |
| Folded work | Epic [#414](https://github.com/m2ux/prosiform/issues/414) | Row `W05` links pull request [#447](https://github.com/m2ux/prosiform/pull/447) and is ticked done, with `AC4` ticked, applied through the planner's `sync.py`. The Development link the mutation would set is blocked: #414 is at GitHub's ceiling of ten manual references, and no record was unlinked to make room. |

## Held

| Kind | Subject | Option recommended |
| --- | --- | --- |
| Folded work | [W05 work item](../2026-10-30-414-i05-e09-mock-substitution/w05.md), its Fixtures table | The fixture declares `-m rules.md=stand-in.md`, a document key, and passes on the tree before this row's change as well as after it, because the document-key redirect arrived with W01's seam. The fixture still holds AC4's statement against the build that ships it, and the section-key case this row corrects is held by `src/tests/test_mock.py`. Recommend no change: a corpus fixture declares one invocation, and the plan chose the document key as the shape the corpus can state. A section key's deferred destination could be added as a second fixture under this row if the corpus is to state it too. |
| Folded work | [W05 work item](../2026-10-30-414-i05-e09-mock-substitution/w05.md), its Test row | The Test part names "a candidate comparison against a mocked bundle". The unit case asserts what `candidate.intended` returns for a mapped and an unmapped deferred link, which is the comparison's own answer; it does not reach `candidate.validate` with a candidate built from a mapped run. Recommend a separate row if the fault path inside `validate` is to be held, since no sound tree reaches it and building one is E00's candidate-fault pattern rather than this row's subject. |
| Folded work | `src/prosiform/bundle.py`, `bundle.target` | The deferred and dispatched branches of `target` each resolve the link a second time through `withholding_target`, as `candidate.intended` does a third. Each takes the mapping, so all three agree; nothing this row found required a change there. Recommend no change: the resolution is idempotent over one mapping and the record is keyed by the served key, so a repeated read adds no warning and no destination. |
| Folded work | `src/tests/test_linked_bootstrap.py`, `src/tests/test_handoff_round_trip.py` | Both fail in this sandbox — the first needs network for `uv build`, the second writes a temporary directory beside its output path and reports `E_PUBLICATION_FAILED` on the atomic folder swap under `/tmp`. Six cases fail with the branch's change and six without it, so neither family is this row's. Recommend no change: continuous integration runs `make check` unsandboxed, and weakening either to run here would weaken what it holds. |
| Folded work | [W05 work item](../2026-10-30-414-i05-e09-mock-substitution/w05.md), the dispatched target | `fixtures.md` gives the reason a dispatched and a parallel-dispatched target carry no corpus fixture, and this row did not add one. Both are redirected already, and what a fixture would observe is a second bundle in the run's folder. Recommend a later row adds a dispatch fixture only if the corpus is to state dispatched destinations, which this epic's inventory says it is not. |

## No change

- **The seam.** `withholding_target` took the mapping before this row, and both operators resolve through it to the substitute. No parameter was added and no call site changed.
- **`rebased`'s path escaping.** The path was already URI-escaped per segment, which is what makes a destination carrying a space or a percent sign decodable once.
- **The document-key case.** A document key leaves the reference's own section on the resolved reference, so the destination publishes the section the author named, and the run has confirmed the substitute carries it. That is the contract's own rule and this row did not change it.
- **The dispatch sub-section.** A dispatched link's destination is still the sub-section its region carries, keyed by the target the mapping resolved. `bundle.target` and `candidate.intended` both read the same key, so the set and the link agree.
- **The design and the pin.** The row states no behaviour the design at `827b66fc` does not already carry, so no amendment landed and `README.md`'s pin did not move. `make conformance` went from `55` uncovered clauses to `54`.
- **The fixture's name.** `a-deferred-target-is-redirected` is the name `fixtures.md` and the epic issue give.
- **The independent row pairs.** `joins.md` states that W05 and W02, W03, W04, W06, W07, W08 and W10 take separate pull requests; this row is the first of each of those pairs.
