# Changes — I00:E10:W04+W05

Delivered by [#173](https://github.com/m2ux/prosiform/pull/173), merged into `i00/e10/main` at `0a090dc`.

## Checks

| Change | Where |
| --- | --- |
| The installation claims no run of the corpus observes, each with the reason it is unreachable and the run that would observe it, rendered in the declared-surface listing and counted in the report's closing line | `checks/conformance.py` |
| Three cases holding an entry's reason, the line stating what would observe the claim, and the summary count | `checks/tests/test_conformance.py` |

## Build

| Change | Where |
| --- | --- |
| Two cases holding a run whose execution raises an error the contract names no outcome for to the declared internal-error status, an empty standard output and one error diagnostic under the declared code, one case in each diagnostic format | `src/tests/test_cli.py` |

## Documentation

| Change | Where |
| --- | --- |
| The conformance check's row stating the installation claims the listing carries | `README.md`, `checks/README.md` |

## Tracker

| Change | Where |
| --- | --- |
| W04 and W05 linked to their shared pull request and ticked, with AC7 and AC8 | [#9](https://github.com/m2ux/prosiform/issues/9) |
| The task issue ticked and closed, its documented installation command line corrected to the project's own directory | [#68](https://github.com/m2ux/prosiform/issues/68) |
| AC8's origin closed as delivered, citing the pull request and the cases that answer it | [#73](https://github.com/m2ux/prosiform/issues/73) |
| Row W35 and criteria AC38 and AC39 added | [#39](https://github.com/m2ux/prosiform/issues/39) |
| The claim bound to no run raised as deferred debt, placed on the Bundling board in Backlog | [#174](https://github.com/m2ux/prosiform/issues/174) |
| The review pull request for `i00/e10/main` carrying this unit's change and citing its pull request | [#168](https://github.com/m2ux/prosiform/pull/168) |

## Plan changes

| Kind | Subject | Applied |
| --- | --- | --- |
| Task creation | W35 on [#39](https://github.com/m2ux/prosiform/issues/39), delivered by [#174](https://github.com/m2ux/prosiform/issues/174) | Applied |
| Folded work | AC38 and AC39 added to [#39](https://github.com/m2ux/prosiform/issues/39), so its new row carries criteria | Applied |
| Re-prioritisation | [#174](https://github.com/m2ux/prosiform/issues/174) placed on the Bundling board in Backlog; [#68](https://github.com/m2ux/prosiform/issues/68) moved to Done | Applied |
| Folded work | [#68](https://github.com/m2ux/prosiform/issues/68)'s documented installation command line corrected to name the project's own directory | Applied |

Nothing was held: no change this session met needed an initiative of its own.

## The components the rows declare

W04 declares `checks/conformance.py`, the component the delivery brief planned. W05 declares `src/tests/test_cli.py` rather than `src/prosiform/cli.py`: the command's generic handler already returns the declared status and emits the declared code, so what this row delivers is the instrument that observes it, and no production file changed.

## What remains open

**An installation claim is bound to no run.** The claims are declared beside the surface the report renders, so a run that came to observe one would leave its entry standing. Binding each claim to the smoke-run property that would observe it is the direction, and [W35](https://github.com/m2ux/prosiform/issues/174) carries it.

**AC1 stays unticked on [#9](https://github.com/m2ux/prosiform/issues/9).** It waits on the two adversarial families W01 left held by nothing, each a tracked row of [#39](https://github.com/m2ux/prosiform/issues/39). The epic's rows are all delivered, so AC1 is the whole of what stands between `i00/e10/main` and integration; [#168](https://github.com/m2ux/prosiform/pull/168) stays a draft and [#9](https://github.com/m2ux/prosiform/issues/9) stays open until the user decides.
