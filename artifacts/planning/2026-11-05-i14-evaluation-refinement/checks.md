# Checks

No implementation changed and no paid session ran.

## Saved body formats

```text
#464 initiative (open): 0 fixed, 0 to apply, 0 to decide
#660 initiative (open): 0 fixed, 0 to apply, 0 to decide
#661 epic (open): 0 fixed, 0 to apply, 0 to decide
#677 epic (open): 0 fixed, 0 to apply, 0 to decide
```

The initiative checks were run with each initiative's linked epics supplied:

```text
#464 validated with #403, #454, #456, #455, #579, #594, #639, #662
#660 validated with #661, #677
```

No required-criteria declaration was read for the epic checks, so no project criterion was evaluated.

## I14 dependency graph

```text
--- problems
none

--- joins: candidate units, rows of one epic extending one component
none

--- advisory: numbering against start order
none

--- levels (0 = can start now)
0 E00:W01 - Shake down the edge-run runbook
0 E01:W01 - Reconcile the default-matrix baseline cells
0 E01:W02 - Record cross-harness crash-free runs
1 E00:W02 - Record the live edge workflow run
1 E01:W03 - Publish the harness coverage evidence
2 E00:W03 - Publish the measured edge workflow results

--- component contention: rows of different epics extending one component
E00:W03 and E01:W03 both extend main:evals/diagram-following/README.md

--- epic priority (epics sharing a number start together)
2 E00
1 E01

--- longest chains: 1, each of 3 steps
on every chain: E00:W01, E00:W02, E00:W03
E00:W01 -> E00:W02 -> E00:W03
```

The one contention is two rows editing `evals/diagram-following/README.md` in different sections from epics the priority map puts at different numbers, so E01 runs after E00 rather than beside it. E01 carries priority 1, the label its sibling carries.

## Retained E04 delivery

```text
#579 epic (open)
  in flight: #622 [I10:E04] Composition Following
  unevaluable: config/branches at 1076ef5293c0da74163d1289adf56ab0ef8cfbb0 in /home/mike1/projects/dev/md-composer/.git is absent
  not checked: epic-base pull requests set apart from task deliveries
  not checked: unmerged epic bases
  not checked: draft epic bases
  not checked: review pull request References
  not checked: review pull request Changes paths
  not checked: review pull request issue links
  not checked: pull request targets
  closable: no (long-lived branches unevaluable)
```

The retained rows and criteria are complete at the epic base; integration and branch-configuration evidence do not permit epic closure. The release queue independently selects I11 as Ready. The [release receipt](release-readiness.json) records its prerequisites and actual status readback.
