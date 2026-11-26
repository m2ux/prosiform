# F42 Verification

- Source: e271c2252afb5ff3f23845dac3860ed0b6832fad
- Base: 6eb02cb5c44bf8942ad16e5c4e6104438a969438
- Build metadata: 0.35.0; this source revision contains the fix, not every build reporting that version
- Governing design: 119c12e2e223cf32d18b71186ba274d8da75c8d2

## T1: Distinct Heading Destinations

Pass. Four successful corpus cases cover both lifted/authored heading orders, ordinary links and Mermaid clicks, brief-child links, a dispatch set and a dispatch pick. Expected complete bundles retain each distinct destination. An initial eight-case focused run also retains the conflicting-selection and composition refusal controls.

## T2: Complete Repository Checks

Invocation: env UV_PROJECT_ENVIRONMENT=/tmp/f42-product-venv PROSIFORM_BUILD=/tmp/f42-product-venv/bin/pf make check. The host dependency cache is available; no offline override is set.

Pass. The complete make check exits zero: 2,121 build tests; 1,235 harness tests and one existing skip; 710 corpus fixtures. Lock, lint, format, type, reachability, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and release checks pass.

[Complete successful log](make-check.log), SHA256 2a9f8519b20de2f924b684fbd7844980adad12be3f583f1442da36bb0f49167b.

The first runs retained local dependency-cache failures, obsolete refusal assertions and then fixture-description vocabulary failures. Locked dependency setup, removal of the assertions contradicted by the approved behavior, and corrected vocabulary precede this successful run. Earlier logs remain local; they are not accepted validation results.

Conformance retains the repository's reported limits: 75 clauses have no fixture, 16 clauses state no run, and three installation claims have no observing run. This hot-fix claims its observed destination and refusal behavior; no paid native-agent evaluation occurs in this compiler check.

## T3: Revision-bound Review

Pass. [Exact-head agent review](agent-review.json) records no unresolved finding.

The review inspects the complete target-to-head change, source.fragments allocation, cli.destination_map target identities, dispatch.anchors generated positions, Placing.named distinct-selection refusal and composition's separate scope refusal. The published review record binds the actual pull request and its revisions.

The design pin also carries two previously approved editorial refinements: production packaging/parser obligations are co-located and obsolete source-boundary claims are removed. Contract, corpus and independence checks pass with this design. Neither requires an additional runtime feature in this hot-fix.
