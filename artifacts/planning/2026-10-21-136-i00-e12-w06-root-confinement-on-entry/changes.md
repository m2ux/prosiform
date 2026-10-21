# Plan Changes

The plan changes this session applied, and the ones it held for the user.

## Applied

None. The row was delivered with the scope its epic row carries: one criterion, one component, one pull request.

## Held

None. No change this session met fell outside the allowance it was given — task creation, epic creation, migration, re-prioritisation and folded work — because no change arose.

## Debt and Arising Issues

One defect was observed and none was deferred.

- **The manifest schema's error catalogue still enumerates two withdrawn codes.**
  `make harness` fails `test_a_catalogue_is_the_codes_the_design_declares` because `fixtures/manifest.schema.json` enumerates `E_MARKED_RESOURCE` and `E_SELF_REFERENCE`, which D59 withdrew from the design. It is the epic base's state rather than this row's, and W04 and W05 of this epic retire both codes, so it needs no issue of its own and this row left it alone. [Validation](validation.md#harness) records the observation.

## Blocked

One step of the task merge is outstanding.

- **The epic review's body does not yet carry this row's change.**
  [#139](https://github.com/m2ux/prosiform/pull/139), the draft review from `i00/e12/main` to `main`, states the changes the base carries and cites each task pull request merged into it. The update adding this row's two bullets and citing [#140](https://github.com/m2ux/prosiform/pull/140) was refused by the session's permission layer, so the review still cites #138 alone. The composed body is ready and the edit is one `PATCH` on that pull request's body; every other record of this merge is published.
