# Check-state requirement review

## Revision and method

On 2026-11-05, a fresh fetch of `main` resolves to `ba93ca60860f0dc46722f27acd471740465279da`. This review reads the workflow, Makefile and runner at that commit. It inspects configuration and source; it runs no check suite and establishes no new completion tick.

## Findings

| Requirement | Current evidence | Disposition |
| --- | --- | --- |
| #255 AC1: checks on pull requests outside the initiative head-name pattern | The [workflow events](https://github.com/m2ux/prosiform/blob/ba93ca60860f0dc46722f27acd471740465279da/.github/workflows/checks.yml#L16) select the target branch; its checked-path selection decides whether the job runs checks. Completed #454 explicitly governs checked changes and reported skips. | Reconcile the older universal wording with the delivered checked-path policy before removing or ticking it. |
| #255 AC2: a push to main runs checks | The same workflow declares push to main. | Configuration is present; a completion tick still requires the criterion's observing workflow record. |
| #255 AC3–AC5: check-all reaches and reports every failing target | The [Makefile](https://github.com/m2ux/prosiform/blob/ba93ca60860f0dc46722f27acd471740465279da/Makefile#L68) declares check and its dependencies, with no check-all target. | Further work remains. |
| #255 AC6: distinguish a failed invocation from output drift | [Result](https://github.com/m2ux/prosiform/blob/ba93ca60860f0dc46722f27acd471740465279da/checks/runner.py#L117) holds differences, exit status and captured output. Its passed property tests only whether differences are empty; it exposes no explicit three-state verdict. | Further work remains; raw exit status is not proof of the proposed classification. |
| #255 AC7: restatement refuses a failed invocation | Restatement is separately planned under #187 W14, downstream of triage. | Preserve the requirement while deciding its ownership and observing test. |
| #187 AC13: one criterion spans trigger, complete failure collection and verdict classification | These are separate conditions, with different delivery evidence and implementation components. | Split only after the user decides how the delivered trigger policy relates to the older requirement. |

## Pending triage decision

#243's Overview and scope boundary say triage reports and classifies, while its Proposal and AC2 say `--only` restricts a rewrite. The same claim appears in #187 AC15 and the registered W13 work item. The pending recommendation is report filtering for triage, leaving writes to restatement. AC3 and parent AC16 would state that a green corpus produces no drift report.

The component declarations in these historical work items remain separate findings; this source review does not silently assign or split their implementation.
