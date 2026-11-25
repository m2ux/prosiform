## Overview

Preset-qualified bundle filenames carry opaque SHA-256 strings that hide the selected presets. **Readable preset names** make entry folders and dispatched bundles easier to inspect: `workflow-codex.bundle.md`, or `workflow-codex+recorded.bundle.md` for a combined selection. Canonical selection matching, safe filenames and atomic collision refusal govern the result.

Target: `main`

## Problem

- **Generated names hide useful information.**
  A digest identifies a preset set without telling the reader which presets it contains.
- **Every reference must agree.**
  Entry folders, child filenames, rewritten links, documented examples and exact-output fixtures share the naming contract.

## Proposal

- **Name the effective presets.**
  Append a hyphen and the selected declaration names in Unicode order, separated by plus signs. Equivalent requests share one name; an empty selection adds no qualifier.
- **Keep names unambiguous.**
  Percent-encode each preset name before joining, so literal plus signs, slashes, spaces and Unicode remain filename content. Existing link encoding points to those actual filenames.
- **Refuse collisions atomically.**
  Distinct selections deriving the same filename fail before publication and preserve an earlier output set. A source named task-checks.md can collide with task.md selected under checks; the existing guard covers this case.
- **Align the complete delivery.**
  Update compiler naming, documentation, exact-output fixtures, lifecycle examples and installed-wheel checks. Integrate current main and verify its authoring checks with the complete suite.
- **Retain the retrospective evidence.**
  Local implementation and initial tests preceded registration. The operator subsequently selected readable preset names; earlier twelve- and eight-character candidates remain historical evidence, separate from final acceptance.

## Acceptance Criteria

- [x] **AC1.** Entry folders and dispatched bundles use sorted effective preset names and resolving rewritten links, as source regressions and exact-output fixtures verify.
- [x] **AC2.** Equivalent requests share a bundle, and distinct selections including a literal plus versus a multi-preset selection remain distinct, as preset/dispatch tests verify.
- [x] **AC3.** Distinct selections deriving one filename fail with E_PUBLICATION_FAILED and preserve the earlier output bytes, as the publication regression verifies.
- [x] **AC4.** The naming specification, fixtures and examples agree, with complete source, check-harness, installed-wheel and corpus checks passing on the reviewed head.

## References

- **R1.** [Derived names](https://github.com/m2ux/prosiform/blob/main/docs/bundles.md#derived-names) — Published naming and collision contract.
- **R2.** [Verification](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-25-848-f38-bundle-identifiers/test-results.md) — Source pins, checks, earlier candidates and limits.
- **R3.** [PR #849](https://github.com/m2ux/prosiform/pull/849) — Delivering pull request.
