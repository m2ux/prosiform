# The Version the Prototype Initiative Closes At — October 2026

> Release · Created 2026-10-21

## Executive Summary

The prototype initiative closed with the contract stated in full and met by the Python build. This record holds the decision about what to call that, and the evidence behind it. The rule the decision applies is documentation rather than a record: it binds every release, so it is published at [`docs/versioning.md`](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md).

## Evidence

Measured on `main` at `8feb44b`, the revision both tags name.

| Measure | Result |
| --- | --- |
| Behavioural clauses | 242 stated, 0 covered by no fixture |
| Fixtures | 239 run, 239 pass, 0 failing, 0 awaiting work |
| Declared codes | 30 reached, 0 the build reports nowhere, 0 the contract declares nowhere |
| Documented invocation | 29 statements, each held to the build |
| Independence | every word of every declaration and report entry one the contract states |
| Unit cases | 723 repository, 595 build |

## Decisions

- **The release is `0.9.0`.**
  The build meets the contract as written, so it is feature-complete, and `0.9.0` states that while leaving the assertion of a settled contract to the revision use settles. Tagged `contract/v0.9.0` and `python/v0.9.0`, both naming `8feb44b`.

  `1.0.0-rc.1` was considered and refused. A release candidate asserts that the release is near, and the refinement stage has no committed end date, so the suffix would be a claim about timing the plan does not make. `0.1.0` unchanged was refused because it predates nearly all of the initiative's delivery, and `0.2.0` because it records that work landed without saying what the build now meets.

- **The policy is documentation, not a planning record.**
  The rule governing version numbers binds every release rather than the one this record holds, so it was published to `docs/versioning.md` and the documentation index names it. This record keeps only the dated decision and the evidence it rested on.

## Notes

- **The tags predate the policy document.**
  `docs/versioning.md` landed after `8feb44b` in [#192](https://github.com/m2ux/prosiform/pull/192). Neither tag covers it: the contract tag covers the design and the corpus, the build tag covers `src/`, and the document is neither, so both remain accurate at the revision they name.

- **Nothing holds a tag to the version its build reports.**
  The three places the number is stated — the tag, `src/pyproject.toml` and the lockfile — agree because one change set them together, not because anything checks it. Raised as [#191 \[I01:E03:W09\]](https://github.com/m2ux/prosiform/issues/191).

## Links

| Resource | Link |
| --- | --- |
| Initiative | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Versioning policy | [`docs/versioning.md`](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md) |
| Version pull request | [#190](https://github.com/m2ux/prosiform/pull/190) |
| Policy pull request | [#192](https://github.com/m2ux/prosiform/pull/192) |
