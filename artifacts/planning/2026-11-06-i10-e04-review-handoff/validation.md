# E04 Integration Validation

Reviewed head: `8ca53994e89dab6657c2eea9eef72f74c48764e0`. Target: `main` at `ba93ca60860f0dc46722f27acd471740465279da`. All 15 task rows are delivered through seven merged task PRs, and all 24 retained criteria are verified and ticked. Live edge measurements remain in I14 issue 661.

## Full Check

`PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/pr622-conflict-resolution/src --frozen pf' make check` passes at the reviewed head: 1,731 source tests, 1,586 harness/evaluation tests, 516 external-build corpus fixtures and every remaining repository gate. [Full output](final-make-check.log) records the exact run; [hosted checks](hosted-checks.json) records successful CI at the same head. No paid session ran.

## Criterion Verification

| Criteria | Observing evidence |
| --- | --- |
| AC1 | Typed compile declarations and broken-owner/source cases in test_workflow.py. |
| AC2, AC3 | Real stub-run workspace inputs, compiled bundles, build path and observable-cell tests in test_run.py. |
| AC4 | Source scorer tests for omitted, extra and misordered session and child runs. |
| AC5 | Recorded Claude streams attribute nested starts, parents and commands; Codex actor/group round trips retain native identities. |
| AC6 | Both bootstrap workflows declare guide and compile runs; the undeclared skill entry and executed bundle walk are checked. |
| AC7, AC8, AC9 | Conditional/nested activation and the preset-selected stand-in are compiled and compared with stated runs and paths. |
| AC10, AC11, AC12 | Conditional composition, footnote targets and self-composition use actual bundles and wrong-path counterexamples. |
| AC13 | Deferred-dispatch reached/passed cases compare compiled output links and expected starts. |
| AC14, AC15, AC16 | Three-hop chains, second-hop sets and relayed questions have ordered traces and no unexpected depth warning. |
| AC17, AC18 | First/deep-hop actions are held to material their deferred compile actually supplies; missing actions fail scoring. |
| AC22 | Independent child-command capability excludes native child-run requirements while retaining observed native chains. The before/after regression is retained. |
| AC23 | Runbook tests compare every scorer class with its triage rubric. |
| AC26 | Compiled Claude stub sessions and recorded third-hop streams retain each actor's runs and observe omitted/extra child commands. |
| AC27, AC28, AC29 | Corpus source operators, compiled form admission, generated bundle links and instruction headings are checked. |

## Review Findings

- Fixed stale criterion references and change-history prose in test documentation at commit 3711aabdd. [Documentation attestation](documentation-attestation.json) compares that documentation-only step.
- Fixed the AC22 admission defect at commit 8ca53994e: child-start observation does not establish per-child command attribution. [Before](nested-command-before.txt) fails on native admission; [after](nested-command-after.txt) passes all three focused regressions, including the actual deep-chain matrix. The full gate then passes.

## Delivery And Review Boundaries

[Readiness](readiness.json) verifies task merge ancestry, criterion coverage, the main integration route, matching task References and the Development link. The sync script cannot read a config/branches statement on this product base; its branch-dependent checks are recorded as unavailable in [sync output](sync-report.txt). The explicit published workspace declaration and direct PR/commit/path/link inspection establish those same branch facts for this handoff. This does not claim issue closure: the integration remains unmerged and main requires one human approving review.

The original E04 checkout retains its recorded HEAD, status and all 65 dirty-file hashes, as [preservation readback](preserved-original-worktree.json) confirms. E07 continues independently on its own base.

## Graph Evidence

The final detached checkout is indexed at the reviewed head. All 360 changed-symbol contexts and 39 reported process traces were collected without tool errors or stale responses. Dynamic receiver and process-budget limitations remain explicit in the overview and index log. No embeddings or live evaluation calls ran.
