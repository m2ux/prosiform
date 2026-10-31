# Validation — W05 Withheld and Dispatched Targets

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w05-withheld-and-dispatched-targets` on branch `i05/e09/w05-withheld-and-dispatched-targets`. The build under test was named by `PROSIFORM_BUILD` as `<worktree>/src/.venv/bin/pf`, the same form the continuous-integration job supplies, because `uv run` cannot build the wheel without network in the sandboxed shell this session ran in.

The branch was cut from `i05/e09/main` at `097160bd`. W10 merged while this row was in progress, so the branch was rebased onto `f21985cc` before the checks below ran, and every count here is that head's.

## T1 — The withheld paths already resolve through the mapping, and the published fragment does not

**Ran:** `pf` from a probe tree at branch head `097160bd`, with `guide.md` deferring one section of `rules.md` and a stand-in carrying a differently-named section.

**Observed:** the destination published was the substitute's path with the *authored* fragment:

```text
$ pf -d json -o out -m 'rules.md#escalation=stand-in.md#answers' guide.md
{"severity": "warning", "code": "W_MOCK_SUBSTITUTED", "resolved": "stand-in.md#answers",
 "source": "rules.md#escalation", "location": {"file": "guide.md", "line": 3, "column": 1}}
$ cat out/guide.bundles/guide.bundle.md
# Guide

Defer [the rules](stand-in.md#escalation) to a later run.
```

The warning states the run resolved `stand-in.md#answers`; the bundle publishes `stand-in.md#escalation`. The contract's rule for a deferred destination is *rebased to the target's path … Retain the resolved fragment when present*, so the fragment published is the authored spelling where the rule names the resolved one.

**A later run following the published destination refuses:**

```text
$ printf '# Later\n\nSee [the rules](stand-in.md#escalation).\n' > later.md
$ pf -d json later.md
{"severity": "error", "message": "the reference 'stand-in.md#escalation' names no heading of the
 document it selects from", "code": "E_TARGET_NOT_FOUND", "resolved": "stand-in.md",
 "source": "later.md:3", "chain": ["later.md", "stand-in.md#escalation"]}
```

That is a bundle this run declared sound, refused by the run it exists for. Both were reproduced before any change was made.

## T2 — The three withheld paths, probed at the pre-change head

**Ran:** `pf` over three probe trees at `097160bd`, one each for a deferred, a dispatched and a parallel-dispatched link, every one under `-m rules.md=stand-in.md`.

**Observed:** all three already redirect, which is the plan's own finding — the seam landed with W01 and `withholding_target` takes the mapping:

| Link | Published destination | Bundle compiled |
| --- | --- | --- |
| `¬ rules.md` | `stand-in.md` | none, which a deferral carries |
| `⇉ rules.md` | `#dispatch-the-rules` | `stand-in.bundle.md` |
| `⫽ rules.md` | `#dispatch-in-parallel` | `stand-in.bundle.md`, listed in the set |

So the dispatched and parallel-dispatched halves of this row need no code, and the deferred half needs the fragment. `fixtures.md` already records that a dispatched target takes no corpus fixture, because its effect is a second run rather than a bundle this run publishes.

## T3 — The fix

**Ran:** `src/tests/test_mock.py`, and the probe of T1 again after the change.

**Observed:** pass, and the destination now names the section the substitution resolved to:

```text
$ pf -d json -o out -m 'rules.md#escalation=stand-in.md#answers' guide.md
$ cat out/guide.bundles/guide.bundle.md
# Guide

Defer [the rules](stand-in.md#answers) to a later run.
$ pf -d json -o out later.md     # a later run following the published destination
$ echo $?
0
```

`closure.rebased` publishes `found.path` with `found.fragment` where the target resolves to a section, and the authored fragment where it does not. A document key leaves the reference's own section on the resolved reference, so it publishes the section the author named — which T1's document-key case shows publishing correctly before the change and T4's fixture holds.

## T4 — The corpus fixture

**Ran:** `make corpus` at branch head `f7900aff`, 367 fixtures.

**Observed:** exit `0`.

```text
mock/a-deferred-target-is-redirected: pass
corpus check: 367 fixture(s), 367 pass, 0 fail, 0 awaited, 0 unexpected pass
```

The count rose from 366 to 367, which is this row's fixture.

**The fixture passes on the pre-change tree as well.** Stashing the `closure.py` change and re-running the corpus left `mock/a-deferred-target-is-redirected: pass` and `367 pass`. That is not a defect in the fixture: it declares `-m rules.md=stand-in.md`, a document key, and the document-key redirect arrived with W01's seam. The fixture holds AC4's statement — the destination a deferral publishes is the substitute's path — against the build that ships it. The fragment case this row corrects is the section-key one, which no corpus fixture declares and which T5 holds.

## T5 — The unit cases, and the three that fail without the change

**Ran:** `src/tests/test_mock.py`, then the same file against the pre-change `closure.py` restored by `git stash`.

**Observed:** the file passes at branch head. Against the pre-change tree three fail:

```text
FAILED src/tests/test_mock.py::test_a_deferred_target_is_redirected_to_the_substitute
FAILED src/tests/test_mock.py::test_a_deferred_destination_publishes_the_section_the_substitution_names
FAILED src/tests/test_mock.py::test_the_candidate_comparison_reads_the_same_substitute
```

The seven cases this row adds:

- `test_a_deferred_target_is_redirected_to_the_substitute` — AC4's statement. The destination is the substitute's path, one `W_MOCK_SUBSTITUTED` is emitted, and neither document's content nor the substitute's heading reaches the bundle, because a deferral compiles nothing here.
- `test_a_deferred_destination_publishes_the_section_the_substitution_names` — the section key's substitute publishes its own section, and a later run following the published destination exits `0` where the authored section exits `1`.
- `test_a_deferred_targets_heading_is_confirmed_of_the_substitute` — a substitution naming a section the substitute lacks is refused with `E_TARGET_NOT_FOUND` and `resolved` the substitute, so the document confirmed is the one the later run reads.
- `test_a_dispatched_target_is_redirected_and_its_bundle_compiled` — `stand-in.bundle.md` is written, `rules.bundle.md` is not, and the sub-section names the substitute's bundle.
- `test_a_parallel_dispatched_target_is_redirected_and_listed_once` — the set a `⫽` mark publishes lists the substitute's bundle once.
- `test_the_candidate_comparison_reads_the_same_substitute` — `candidate.intended` returns the substitute's destination for a mapped deferred link and the authored one unmapped, so emission and comparison read one answer.

The two dispatch cases pass on both trees, because the dispatch hop was already the redirected reference at `097160bd`. They hold the behaviour rather than the change, which is what `fixtures.md` says they are for.

## T6 — A substituted bundle is not a bundle of the material that ships

**Ran:** the fixture's source tree run with and without `-m`.

**Observed:** without the mapping the deferred link's destination is `rules.md`, and the fixture's own tree is unread by every stage that compiles content — `rules.md` is confirmed to exist as a withheld target and is neither opened as a content source nor bundled. The one difference between the two runs is the warning and the destination, so AC4's statement is about the mapping rather than about the tree.

## T7 — The compiler's own checks

**Ran:** `make check` at branch head `f7900aff`, each target in the Makefile's order.

**Observed:** exit `0` throughout.

- `lock-check` — `Resolved 24 packages`.
- `lint` — `All checks passed`; `format-check` — `179 files already formatted`; `typecheck` — `Success: no issues found in 81 source files`.
- `test` — `1377 passed`; `harness` — `1023 passed`.
- `authoring` — `0 finding(s)`.
- `corpus` — `367 fixture(s), 367 pass`.
- `smoke` — the installed command is named on the path, independent of the working directory and of this repository.
- `layout` — `4 tree(s) present`; `tables` — `22 command(s) and 8 declaration(s)`; `links --online` — `every reference in 212 document(s) resolved`.
- `vocabulary` — `46 contract term(s) ... on 827b66fc`.
- `invocation` — `30 statement(s)`.
- `conformance` — `305 clause(s)`, `54 covered by no fixture`, `0 declaration(s) naming no clause`. The uncovered count fell from `55` to `54`, which is this row's clause.
- `independence` — `every shaped term of every fixture declaration and every report entry is one the contract names`.
- `steps` — `every procedure in 59 document(s)`.
- `mock-scenarios` — `5 scenario(s), 5 pass`.

## T8 — The clause the fixture declares, at the pin

**Ran:** `make conformance`, reading the design at `827b66fcd837ec6a9e203a82a1c86fc5ec2b60bb`, which `README.md` pins.

**Observed:** the fixture's three declarations resolve and are reported against it:

```text
Link classification and resource handling — The substitution mapping: 18 fixture(s)
    mock/a-deferred-target-is-redirected
Link classification and resource handling — A deferred link's destination: 9 fixture(s)
    mock/a-deferred-target-is-redirected
Link classification and resource handling — A withheld link's target: 3 fixture(s)
    mock/a-deferred-target-is-redirected
```

The clause count is `305` and no declaration names a clause the design lacks, so the pin needed no move: this row states no behaviour the design does not already carry, which is why it landed against the existing clause rather than amending it. That is the difference between this row and W04, whose clause and warning codes the design gained.

## T9 — The failures this environment reproduces on every settled branch

**Ran:** `src/tests` at branch head `f7900aff`, and the same file set with the branch's `closure.py` stashed.

**Observed:** the same two families fail either way, so neither is this row's:

- `src/tests/test_linked_bootstrap.py` — needs network, because the test runs `uv build` to install a wheel.
- `src/tests/test_handoff_round_trip.py` — six cases, every one reporting `E_PUBLICATION_FAILED` with `[Errno 21] Is a directory` on the atomic folder swap under `/tmp`.

The count is six with and six without the change. The publication tests that fail this way assert a published set under `/tmp`, which this sandbox cannot swap. CI runs `make check` unsandboxed, where both families pass; the pull request's `Checks` run is what confirms it.

## T10 — Delivery

**Ran:** `gh api` against the pull request, the epic, and the base.

**Observed:** pull request [#447](https://github.com/m2ux/prosiform/pull/447) against base `i05/e09/main`, raised through REST, carrying the `bot:ai-assisted` label. Its `Checks` run reported `success` on `f7900aff`, and the base's own run on the merge commit `3091c65b` reported `success` too. #447 merged into `i05/e09/main` at `3091c65b2e912fa1ead90a64a196828e9652773e`.

Row `W05` on [#414](https://github.com/m2ux/prosiform/issues/414) now links #447 and is ticked done, with `AC4` ticked. The planner's `sync.py` made the edit, mapping `W05` to the pull request and ticking the criterion it was reported ready to verify.

**The Development link is not set.** `addCloseIssueReferences` answered `Issue exceeds manual reference limit`: #414 already carries ten connected pull requests (425, 427, 428, 429, 430, 431, 433, 437, 438, 439, 440, 446 among the merged ones), which is GitHub's ceiling. The brief freed one reference for this row, but the ceiling was reached again by rows that landed while this one was in flight. No other row's record was unlinked, because the brief forbids it and the choice of which record to retire is the epic's rather than this row's.
