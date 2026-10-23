## Overview

Agents authoring Markdown for Prosiform need reusable guidance that connects the writing request to the compiler's syntax, section-selection and dependency rules. The goal is a skill in this repository that helps an agent create general Prosiform-compatible Markdown and report evidence for its compatibility.

## Problem

Markdown that renders correctly can still omit required context or fail when compiled from its intended entry point.

- **Compatibility rules are spread across several sources.**
  The [authoring plan's evidence record](https://github.com/m2ux/prosiform/blob/bcdbe4b0fea4cd256f15d80d0f51c1b7f707af31/artifacts/planning/2026-10-22-prosiform-author-skill/evidence.md) identifies the design, invocation guide and fixture corpus an author must reconcile.
- **Section selection does not inherit governing prose.**
  The [source-structure contract](https://github.com/m2ux/prosiform/blob/4cbd8a7a7e63dd145321d4d786bd57a762f1afd1/artifacts/planning/2026-10-17-prosiform-v1/design.md#explicitly-linked-source-structure) requires explicit dependencies; a heading-only ancestor supplies no governing instructions.
- **Conditional wording does not defer a dependency.**
  The [link-classification contract](https://github.com/m2ux/prosiform/blob/4cbd8a7a7e63dd145321d4d786bd57a762f1afd1/artifacts/planning/2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling) follows ordinary local Markdown links under the root and gives deferred links their own semantics.
- **A compatibility claim needs an identified validation baseline.**
  The [runtime observation](https://github.com/m2ux/prosiform/blob/bcdbe4b0fea4cd256f15d80d0f51c1b7f707af31/artifacts/planning/2026-10-22-prosiform-author-skill/evidence.md#runtime-observation) records source version 0.9.0 alongside an executable reporting 0.1.0.

## Goal

- An agent using the skill can create general Markdown documents whose intended entries compile successfully under an identified Prosiform build and profile.
- A selected document or section carries its required context through explicit dependencies, with intended later branches deferred to separate compilations.
- Authored documents preserve the requested content and destination conventions without imposing agent-skill structure on ordinary Markdown.
- The agent reports the tested entries, compiler identity and results, distinguishing successful compilation from unverified compatibility.

- A missing root inherits the linking parent root; a direct entry defaults to its containing directory. Entries and linked files can declare their own link-resolution roots through `metadata.prosiform-root`, resolved relative to the file, so the agent can invoke `pf <file>` and resolve library references from the declaring file's root.
- The skill advises hyphens rather than underscores in file and directory names and predicts entry-derived bundle filenames; combined selections supply an explicit output destination.

## Non-Goals

- Changing the Prosiform compiler, contract or Markdown profile.
- Migrating or auditing an entire existing document repository.
- Installing toolchains or building a second Markdown validator.
- Executing instructions embedded in authored documents or publishing those documents.
- Restricting the skill to authoring agent skills.

## References

- **R1.** [Skill guidelines](https://github.com/m2ux/workflow-server/blob/workspace/skills/guidelines.md) — The requested conventions for the skill's own files.
- **R2.** [Prosiform authoring skill plan](https://github.com/m2ux/prosiform/blob/bcdbe4b0fea4cd256f15d80d0f51c1b7f707af31/artifacts/planning/2026-10-22-prosiform-author-skill/plan.md) — The scoped design, compatibility coverage and implementation acceptance checks.
- **R3.** [Prosiform invocation](https://github.com/m2ux/prosiform/blob/ea82c8bb03acb2f3c3ca64f6003005d4bf53ebd6/invocation.md) — Entry references, deferred links, validation and exit statuses.
- **R4.** [File-owned invocation plan](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/design.md) — root metadata, automatic naming and authoring requirements delivered by epic #218 before this skill consumes them.
