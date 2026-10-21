# Validation — I00:E11:W35

> Delivery · Created 2026-10-21

The checks this unit's criteria are observed by, the revisions they ran against, and what each result establishes. The branch is `i00/e11/w35-an-installation-claim-bound`, cut from `i00/e11/main` at `8cd9534`.

## Criteria and the checks that observe them

| Criterion | Observed by |
| --- | --- |
| AC38. Each installation claim the conformance report lists names the smoke-run property that would observe it, as the rendered declared-surface listing shows. | T1 `make harness`, through `test_an_installation_claim_names_the_property_that_would_observe_it`; T2 `make conformance`, which renders the repository's own listing |
| AC39. A claim whose property the smoke run observes fails the conformance check rather than being listed, as the harness case supplying such a run shows. | T1 `make harness`, through `test_a_claim_the_run_observes_fails_the_report` and `test_a_claim_the_run_observes_leaves_the_listing` |

## The restatement each claim's property carries

Each claim's observability line was prose about what a run might do. The property restates that line in the words the smoke run declares its own properties in, without narrowing what the claim covers.

| Claim | Line as it stood | Property it now names |
| --- | --- | --- |
| another platform | observable once a run installs the build and invokes it by name on that platform | named on another platform's path |
| a machine that never held the repository | observable once a run installs the build on a machine the repository was never copied to | installed on a machine that never held this repository |
| the command line the documentation gives a reader | observable once a run executes that documented command line and invokes the command it installs | installed by the command line the documentation gives a reader |

The run declares the three properties it observes as `named on the path`, `independent of the working directory` and `independent of this repository`, which are the names the repository README's installation section already gives them. No restated claim names one of those three, which is the report's own verdict rather than an assertion here: a claim that did would fail the check.

## T1 — make harness

`make harness` on the branch. 572 cases passed, the conformance file carrying four cases bearing on this unit:

- `test_an_installation_claim_names_the_property_that_would_observe_it` — every claim's rendered second line is `    observable once the smoke run observes a command <property>`, read from the claim's own declaration. Observes **AC38**.
- `test_a_claim_names_a_property_no_run_observes` — the three claims as declared are all listed, and the report raises no installation-claim failure.
- `test_a_claim_the_run_observes_fails_the_report` — supplies a run whose declared properties are the first claim's, and asserts the report's failures carry the line naming that claim and the property the run observes. Observes **AC39**.
- `test_a_claim_the_run_observes_leaves_the_listing` — the same supplied run, asserting the claim is absent from the rendered listing and the closing count is one lower. Observes **AC39**.

Result: pass.

## T2 — make conformance

`make conformance` on the branch, against the repository's own design and corpus. The listing renders three installation claims, each with its reason and the property that would observe it:

```text
installation claim another platform: unfixturable, the smoke run observes this host and the continuous-integration runner, and a platform whose command wrapper and path resolution differ is a different mechanism
    observable once the smoke run observes a command named on another platform's path
installation claim a machine that never held the repository: unfixturable, the repository is on disk throughout the run and merely unreachable by path, working directory and environment, and removing it is not something a check inside it can do
    observable once the smoke run observes a command installed on a machine that never held this repository
installation claim the command line the documentation gives a reader: unfixturable, the run installs an artefact it builds rather than running the command line the documentation's installation section states
    observable once the smoke run observes a command installed by the command line the documentation gives a reader

conformance report: 253 clause(s) the design states, 64 covered by no fixture, 0 declaration(s) naming no clause; 30 declared name(s) reached, 0 unfixturable, 3 installation claim(s) no run observes
```

The clause, coverage and surface figures are those the base produced, so the change moved nothing but the claims' second lines. Observes **AC38**. Result: pass.

## T3 — make independence

`make independence` on the branch. The report is scanned whole, which brings the restated property lines under the implementation-term rule: 233 fixtures and identities, the report as it renders, and 48 declared names, against 60 terms. Result: pass.

## T4 — make smoke

`make smoke` on the branch. The run builds, installs, resolves the command outside the repository, answers `--version` with the profile, bundles a reference from a source root beside the environment and carries the glossary, and reports the three properties it observed. Result: pass.

## T5 — make check

The repository's whole set, run on the base before the change and on the branch after it, so the result is attributable to the branch.

| Revision | Command | Result |
| --- | --- | --- |
| `8cd9534`, base `i00/e11/main` | `make check` with `PROSIFORM_BUILD` naming the worktree's build | exit 0 |
| branch head | `make check` with the same build | exit 0 |

Result: pass.

## Observations

- The binding is exact-string membership: a claim's property is compared with the properties `checks/smoke.py` declares. That is the whole mechanism, and it is what makes the check fail the day a property moves into the run's declaration. It does not hold a claim to naming a property any run could ever observe, because no vocabulary of unobserved properties exists to hold it against, and inventing one would declare in the run properties the run has nothing to say about.
- The smoke run's closing summary now states the properties it observed rather than restating its steps, so the declaration the report reads is also what the run reports.
