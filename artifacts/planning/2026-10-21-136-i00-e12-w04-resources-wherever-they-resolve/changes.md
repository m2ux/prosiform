# Plan Changes

What this session changed in the plan, and what it held for the user.

## Applied

- **Both rows delivered on one pull request, as the unit was confirmed.**
  W04 and W05 joined on the epic table, and [#142](https://github.com/m2ux/prosiform/pull/142) carries them. Each retires one of the two codes the catalogue check reads, so splitting them would have left `checks/tests/test_catalogue.py` red between two merges. The epic's Joins column already recorded the pairing; this session applied it rather than changing it.

- **`validation-scope/an-unselected-self-link` retired rather than restated.**
  The fixture established that a self-link in an unselected sibling does not fail a run. A self-link in a selected section does not fail a run either now, so the fixture demonstrates nothing about validation scope. `validation-scope/an-unselected-broken-link` carries the scope statement with a link that does fail wherever it sits.

- **Four refusal fixtures and one rewriting fixture retired with the refusals they asserted.**
  The `marked-resource` family and `rewriting/marking-an-image` each asserted `E_MARKED_RESOURCE`. Two fixtures in `fixtures/resource` state what a resource does instead. Corpus coverage of the resource rule is stated rather than reduced.

## Deferred

Both items below are technical debt this unit's validation found. Neither blocks AC6 or AC7, and each would warrant a work item of its own, so each is deferred and the epic keeps the scope it was planned with.

- **`W_RESOURCE_PORTABILITY` does not fire for an image naming a Markdown document.**
  `cli.resource()` reads the destination alone, so any `.md` path answers "not a resource" whatever syntax named it. The design makes an image a resource whatever it points at, so a bundle naming one should warn and does not. AC6 governs what the bundle emits, and the bundle emits the image as authored, so the criterion holds. Raised as [#144](https://github.com/m2ux/prosiform/issues/144), placed as `I00:E11:W21`.

- **`source.owner()` has no caller in the product.**
  Removing `cli.self_referent()` left `source.owner()` reachable only from its own unit tests, and `ruff` does not report a module-level function as unused. Removing it would take the design's **Link ownership** clause out of the code and would rewrite the **Ownership stability** note in `candidate`, which is more than a clean-up. Raised as [#145](https://github.com/m2ux/prosiform/issues/145), placed as `I00:E11:W22`.

## Held for the user

- **The design's Validation scope section still names self-reference as something validated.**
  `design.md` reads "Validate link resolution, self-reference, supported selected syntax, and resource rules within the selected dependency closure", and "An unrelated broken link or self-link in an unselected sibling must not fail bundling". Neither statement has a subject once `E_SELF_REFERENCE` is retired. The design is the contract these rows deliver against rather than a file a delivery row rewrites, and `W08` owns the published prose, so this session changed nothing there and names it here instead.
