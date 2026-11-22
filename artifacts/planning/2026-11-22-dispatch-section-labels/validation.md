# Validation

The local compiler candidate is 1ea933b7b213e2032f700b5bb18d5dd10b02b731 on f34-dispatch-display, based on main at bf42862ef3757c8f62b0b8522481d27c4518dd0d (0.33.0).

- **Full make check passes:** 2,303 compiler tests, 1,153 harness tests, 708 corpus fixtures, lint, formatting, strict typing, wheel/install smoke, layout, tables, links, vocabulary, invocation, conformance and independence.
- **Thirteen focused display regressions pass:** local versus direct destinations, named and pick headings, geometry, quoted and Markdown labels, escaped/aliased metadata, class labels, shared statement lines and plain-name collisions.
- **Classifier integration:** all 52 harness/seam selections pass with the candidate. Paired source-bound bundles retain their dispatch targets/model maps. The production bundles expose eight local graph labels, the route seven; an independent mixed-destination fixture checks two local labels and one direct label.
- **Fixture migration:** displayed headings/anchors and conditional graph labels are updated. One loop fixture uses Recheck to distinguish its generated section from its authored Inv title, preserving selected targets and diagnostics. The plain collision diagnostic expectation follows the new heading name.

The operator authorizes retrospective PR publication. [Fresh standalone make check](make-check.txt) verifies the exact delivering head. Compiler validation establishes no native agent performance or live classification accuracy.

## Merged Revision

Fresh Work Planner revision-check verification runs make check in an isolated checkout at merge e2dde5e569800e5584797bb194bb989f8fb2843b and exits zero. The checkout is removed after the run. Its tree is identical to the original PR head. The [complete log](merged-make-check.txt) records 2,303 compiler tests, 1,153 harness tests and all 708 corpus fixtures passing, with all remaining guards and smoke checks.

| Criterion | Observing evidence at the merged revision |
| --- | --- |
| AC1 | Plain named briefs and Dispatch Pick headings: display regressions and full corpus. |
| AC2 | Contained marked handoff links: display regressions and full corpus. |
| AC3 | Mixed local/direct destination fixture and diagram display regressions. |
| AC4 | Geometry, quoting, Markdown, metadata, class and shared-line display regressions. |
| AC5 | Rewritten local anchor assertions and full validated corpus. |
| AC6 | Plain lifted-heading collision and reserved Dispatch Pick regressions. |
| AC7 | Pinned design and shipped docs inspected; corpus, links, vocabulary and conformance guards pass. |
| AC8 | Full make check at the exact merge revision exits zero. |

[Machine-readable verification](delivery-verification.json) binds these observations to the exact merge. Tracker closure additionally requires every current Development-linked PR to be merged.
