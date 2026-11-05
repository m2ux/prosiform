# Diagram-Following Report: baseline

- **Run:** `baseline`, 2026-11-05T05:49:46+00:00; models `openrouter/deepseek/deepseek-v4.1-flash-1017`; 5 repetitions.
- **Sessions:** 360 of 360 started; 0 not started.
- **Tokens:** 92601825.
- **Managed configuration:** none.
- **Cost:** USD 2.50148.
- **Baseline:** `baseline`, 2026-11-05T05:49:46+00:00. Change is this run's pass rate less the baseline's, and a failure count's change follows it in brackets.

## By Model

| Model | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | 360 | 341 | 95% | +0 pts | undispatched 19 | 0 | 257227 | 0.006949 |

## By Model and Form

| Model | Form | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `authored` | 15 | 0 | 0% | +0 pts | undispatched 15 | 0 | 233782 | 0.007994 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | 120 | 120 | 100% | +0 pts | none | 0 | 223946 | 0.006086 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | 15 | 11 | 73% | +0 pts | undispatched 4 | 0 | 384021 | 0.01477 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | 45 | 45 | 100% | +0 pts | none | 0 | 224267 | 0.005933 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | 45 | 45 | 100% | +0 pts | none | 0 | 252363 | 0.005989 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | 120 | 120 | 100% | +0 pts | none | 0 | 291774 | 0.007443 |

## By Model, Form and Scenario

| Model | Form | Workflow | Scenario | Sessions | Passed | Pass rate | Change | Failures | Timeouts | Mean tokens | Mean cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `authored` | `dispatch-beside` | `set-beside-a-dispatch` | 5 | 0 | 0% | +0 pts | undispatched 5 | 0 | 252415 | 0.008787 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `authored` | `dispatch-question` | `returned-question` | 5 | 0 | 0% | +0 pts | undispatched 5 | 0 | 231136 | 0.007528 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `authored` | `dispatch-set` | `parallel-set` | 5 | 0 | 0% | +0 pts | undispatched 5 | 0 | 217796 | 0.007666 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `branching` | `high-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 209371 | 0.005153 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `branching` | `low-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 158364 | 0.005633 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `declared-inclusion` | `declared-link-followed` | 5 | 5 | 100% | +0 pts | none | 0 | 226466 | 0.00555 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `declared-inclusion` | `undeclared-link-as-text` | 5 | 5 | 100% | +0 pts | none | 0 | 148051 | 0.004155 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `group-placement` | `leaf-group` | 5 | 5 | 100% | +0 pts | none | 0 | 203575 | 0.004538 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `group-placement` | `nested-intermediate` | 5 | 5 | 100% | +0 pts | none | 0 | 295848 | 0.007023 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `group-placement` | `two-presets-one-document` | 5 | 5 | 100% | +0 pts | none | 0 | 251994 | 0.006322 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `linear` | `straight-through` | 5 | 5 | 100% | +0 pts | none | 0 | 155146 | 0.00445 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `looping` | `no-rework` | 5 | 5 | 100% | +0 pts | none | 0 | 150185 | 0.00438 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `looping` | `two-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 363304 | 0.006788 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `preset-selection` | `default-alone` | 5 | 5 | 100% | +0 pts | none | 0 | 243541 | 0.006297 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `preset-selection` | `title-selected` | 5 | 5 | 100% | +0 pts | none | 0 | 290516 | 0.007938 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `preset-selection` | `two-presets-one-title` | 5 | 5 | 100% | +0 pts | none | 0 | 265244 | 0.007204 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `pricing` | `clear-discount` | 5 | 5 | 100% | +0 pts | none | 0 | 243898 | 0.00622 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `pricing` | `flagged-list-price` | 5 | 5 | 100% | +0 pts | none | 0 | 203865 | 0.005941 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `rework` | `four-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 419154 | 0.008501 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `rework` | `one-round` | 5 | 5 | 100% | +0 pts | none | 0 | 204968 | 0.004886 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `section-composition` | `deferred-occurrence` | 5 | 5 | 100% | +0 pts | none | 0 | 278002 | 0.009487 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `section-composition` | `merged-sources` | 5 | 5 | 100% | +0 pts | none | 0 | 121596 | 0.003589 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `section-composition` | `nested-composition` | 5 | 5 | 100% | +0 pts | none | 0 | 217783 | 0.006451 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `section-entry` | `document-fragment` | 5 | 5 | 100% | +0 pts | none | 0 | 128692 | 0.004723 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `subst-redirect` | `document-redirect` | 5 | 5 | 100% | +0 pts | none | 0 | 134719 | 0.005355 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `subst-redirect` | `preset-over-default` | 5 | 5 | 100% | +0 pts | none | 0 | 227121 | 0.007189 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `bundle` | `subst-redirect` | `section-redirect` | 5 | 5 | 100% | +0 pts | none | 0 | 233301 | 0.008303 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | `dispatch-beside` | `set-beside-a-dispatch` | 5 | 3 | 60% | +0 pts | undispatched 2 | 0 | 409628 | 0.013069 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | `dispatch-question` | `returned-question` | 5 | 3 | 60% | +0 pts | undispatched 2 | 0 | 488550 | 0.019302 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `compiled` | `dispatch-set` | `parallel-set` | 5 | 5 | 100% | +0 pts | none | 0 | 253886 | 0.011939 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `branching` | `high-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 194707 | 0.004924 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `branching` | `low-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 157392 | 0.004711 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `linear` | `straight-through` | 5 | 5 | 100% | +0 pts | none | 0 | 152259 | 0.005422 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `looping` | `no-rework` | 5 | 5 | 100% | +0 pts | none | 0 | 146195 | 0.005141 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `looping` | `two-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 306467 | 0.007542 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `pricing` | `clear-discount` | 5 | 5 | 100% | +0 pts | none | 0 | 209043 | 0.004766 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `pricing` | `flagged-list-price` | 5 | 5 | 100% | +0 pts | none | 0 | 198266 | 0.005971 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `rework` | `four-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 441198 | 0.009092 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `linked` | `rework` | `one-round` | 5 | 5 | 100% | +0 pts | none | 0 | 212876 | 0.005826 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `branching` | `high-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 230401 | 0.00486 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `branching` | `low-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 222381 | 0.005559 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `linear` | `straight-through` | 5 | 5 | 100% | +0 pts | none | 0 | 160645 | 0.003813 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `looping` | `no-rework` | 5 | 5 | 100% | +0 pts | none | 0 | 155040 | 0.004327 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `looping` | `two-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 394934 | 0.009471 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `pricing` | `clear-discount` | 5 | 5 | 100% | +0 pts | none | 0 | 200331 | 0.007959 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `pricing` | `flagged-list-price` | 5 | 5 | 100% | +0 pts | none | 0 | 160024 | 0.004298 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `rework` | `four-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 562796 | 0.008287 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `prose` | `rework` | `one-round` | 5 | 5 | 100% | +0 pts | none | 0 | 184711 | 0.00533 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `branching` | `high-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 182631 | 0.0047 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `branching` | `low-severity` | 5 | 5 | 100% | +0 pts | none | 0 | 161721 | 0.00434 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `declared-inclusion` | `declared-link-followed` | 5 | 5 | 100% | +0 pts | none | 0 | 192767 | 0.005088 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `declared-inclusion` | `undeclared-link-as-text` | 5 | 5 | 100% | +0 pts | none | 0 | 172931 | 0.005648 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `group-placement` | `leaf-group` | 5 | 5 | 100% | +0 pts | none | 0 | 182397 | 0.004938 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `group-placement` | `nested-intermediate` | 5 | 5 | 100% | +0 pts | none | 0 | 250163 | 0.005354 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `group-placement` | `two-presets-one-document` | 5 | 5 | 100% | +0 pts | none | 0 | 223205 | 0.005919 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `linear` | `straight-through` | 5 | 5 | 100% | +0 pts | none | 0 | 148212 | 0.004001 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `looping` | `no-rework` | 5 | 5 | 100% | +0 pts | none | 0 | 113921 | 0.003318 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `looping` | `two-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 250551 | 0.006493 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `preset-selection` | `default-alone` | 5 | 5 | 100% | +0 pts | none | 0 | 309173 | 0.007943 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `preset-selection` | `title-selected` | 5 | 5 | 100% | +0 pts | none | 0 | 574645 | 0.010652 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `preset-selection` | `two-presets-one-title` | 5 | 5 | 100% | +0 pts | none | 0 | 473416 | 0.011995 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `pricing` | `clear-discount` | 5 | 5 | 100% | +0 pts | none | 0 | 202163 | 0.006466 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `pricing` | `flagged-list-price` | 5 | 5 | 100% | +0 pts | none | 0 | 217375 | 0.00655 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `rework` | `four-rounds` | 5 | 5 | 100% | +0 pts | none | 0 | 443097 | 0.010165 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `rework` | `one-round` | 5 | 5 | 100% | +0 pts | none | 0 | 191763 | 0.005045 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `section-composition` | `deferred-occurrence` | 5 | 5 | 100% | +0 pts | none | 0 | 550652 | 0.012068 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `section-composition` | `merged-sources` | 5 | 5 | 100% | +0 pts | none | 0 | 263155 | 0.007578 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `section-composition` | `nested-composition` | 5 | 5 | 100% | +0 pts | none | 0 | 543516 | 0.012059 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `section-entry` | `document-fragment` | 5 | 5 | 100% | +0 pts | none | 0 | 128425 | 0.004475 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `subst-redirect` | `document-redirect` | 5 | 5 | 100% | +0 pts | none | 0 | 249260 | 0.008593 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `subst-redirect` | `preset-over-default` | 5 | 5 | 100% | +0 pts | none | 0 | 566528 | 0.014007 |
| `openrouter/deepseek/deepseek-v4.1-flash-1017` | `tree` | `subst-redirect` | `section-redirect` | 5 | 5 | 100% | +0 pts | none | 0 | 410919 | 0.011238 |

## Failing Sessions

| Session | Class | Disposition | Evidence |
| --- | --- | --- | --- |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-beside/set-beside-a-dispatch/authored/1` | `undispatched` | miss | Its step links plan.md#work, review.md#source, review.md#tests. The trace is Entry Prepare Deliver Exit and the actions are deliver.txt, plan.txt, prepare.txt, source.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#work, workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-beside/set-beside-a-dispatch/authored/2` | `undispatched` | miss | Its step links plan.md#work, review.md#source, review.md#tests. The trace is Entry Prepare Deliver Exit and the actions are deliver.txt, plan.txt, prepare.txt, source.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#work, workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-beside/set-beside-a-dispatch/authored/3` | `undispatched` | miss | Its step links plan.md#work, review.md#source, review.md#tests. The trace is Entry Prepare Deliver Exit and the actions are deliver.txt, plan.txt, prepare.txt, source.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#work, workflow.md#source, workflow.md#tests, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-beside/set-beside-a-dispatch/authored/4` | `undispatched` | miss | Its step links plan.md#work, review.md#source, review.md#tests. The trace is Entry Prepare Deliver Exit and the actions are deliver.txt, plan.txt, prepare.txt, source.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#work, workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-beside/set-beside-a-dispatch/authored/5` | `undispatched` | miss | Its step links plan.md#work, review.md#source, review.md#tests. The trace is Entry Prepare Deliver Exit and the actions are deliver.txt, plan.txt, prepare.txt, source.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#work, workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-beside/set-beside-a-dispatch/compiled/2` | `undispatched` | miss | The trace is Entry Prepare Deliver Exit and the actions are deliver.txt, plan.txt, prepare.txt, source.txt, tests.txt, so every sub-agent ran and wrote its action. The starts were review__source.bundle.md#source, review__tests.bundle.md#tests, plan__work.bundle.md#work, in another order than the scenario's trace states. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-beside/set-beside-a-dispatch/compiled/4` | `undispatched` | miss | The trace is Entry Prepare Deliver Exit and the actions are deliver.txt, plan.txt, prepare.txt, source.txt, tests.txt, so every sub-agent ran and wrote its action. The starts were review.md#source, review.md#tests, plan.md#work, in another order than the scenario's trace states. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-question/returned-question/authored/1` | `undispatched` | miss | Its step links draft.md#choose. The trace is Entry Enquire Confirm Exit and the actions are confirm.txt, draft.txt, enquire.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#choose, workflow.md#choose, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-question/returned-question/authored/2` | `undispatched` | miss | Its step links draft.md#choose. The trace is Entry Enquire Confirm Exit and the actions are confirm.txt, draft.txt, enquire.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#choose, workflow.md#choose, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-question/returned-question/authored/3` | `undispatched` | miss | Its step links draft.md#choose. The trace is Entry Enquire Confirm Exit and the actions are confirm.txt, draft.txt, enquire.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#choose, workflow.md#choose, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-question/returned-question/authored/4` | `undispatched` | miss | Its step links draft.md#choose. The trace is Entry Enquire Confirm Exit and the actions are confirm.txt, draft.txt, enquire.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#choose, workflow.md#choose, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-question/returned-question/authored/5` | `undispatched` | miss | Its step links draft.md#choose. The trace is Entry Enquire Confirm Exit and the actions are confirm.txt, draft.txt, enquire.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#choose, workflow.md#choose, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-question/returned-question/compiled/1` | `undispatched` | miss | The trace is Entry Enquire Confirm Exit and the actions are confirm.txt, draft.txt, enquire.txt, so every sub-agent ran and wrote its action. The starts were draft__choose.bundle.md#draft, draft__choose.bundle.md#draft, in another order than the scenario's trace states. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-question/returned-question/compiled/4` | `undispatched` | miss | The trace is Entry Enquire Confirm Exit and the actions are confirm.txt, draft.txt, enquire.txt, so every sub-agent ran and wrote its action. The starts were draft__choose.bundle.md#draft, draft__choose.bundle.md#draft, in another order than the scenario's trace states. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-set/parallel-set/authored/1` | `undispatched` | miss | Its step links review.md#source, review.md#tests. The trace is Entry Survey Report Exit and the actions are report.txt, source.txt, survey.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-set/parallel-set/authored/2` | `undispatched` | miss | Its step links review.md#source, review.md#tests. The trace is Entry Survey Report Exit and the actions are report.txt, source.txt, survey.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-set/parallel-set/authored/3` | `undispatched` | miss | Its step links review.md#source, review.md#tests. The trace is Entry Survey Report Exit and the actions are report.txt, source.txt, survey.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-set/parallel-set/authored/4` | `undispatched` | miss | Its step links review.md#source, review.md#tests. The trace is Entry Survey Report Exit and the actions are report.txt, source.txt, survey.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#source, workflow.md#tests, so no start matched its section: the step's link names another document. |
| `openrouter/deepseek/deepseek-v4.1-flash-1017/dispatch-set/parallel-set/authored/5` | `undispatched` | miss | Its step links review.md#source, review.md#tests. The trace is Entry Survey Report Exit and the actions are report.txt, source.txt, survey.txt, tests.txt, so every sub-agent ran and wrote its action. Each prompt named workflow.md#tests, workflow.md#source, so no start matched its section: the step's link names another document. |
