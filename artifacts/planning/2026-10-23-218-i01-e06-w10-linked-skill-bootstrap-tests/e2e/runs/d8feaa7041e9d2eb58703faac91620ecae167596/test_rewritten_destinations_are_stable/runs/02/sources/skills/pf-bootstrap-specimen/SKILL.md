---
name: pf-bootstrap-specimen
description: Exercise the Prosiform linked-document bootstrap specimen when testing compilation of skill instructions.
---

# Linked Instruction Bootstrap

Read this entry point directly. When the specimen is invoked, compile each of the three linked documents below separately with `pf`, then read its bundle before following its instructions.

Resolve each link target relative to this SKILL.md file. Keep the caller's working directory: absent source roots use that directory. Invoke `pf -o - "ABSOLUTE_TARGET"` for each resolved target and read all of its stdout. Preserve a link's fragment when present. A failed command leaves that document's instructions unavailable; report its diagnostics and stop. SKILL.md is the entry point the agent already read, not a compiler input. These bundles are loaded once for this invocation.

- [Assemble](modes/assemble.md)
- [Review](modes/review.md)
- [Defaults](modes/defaults.md)

After reading all three bundles, report the source markers and group headings each contains. The specimen requests inspection only; its linked prose authorizes no external actions.
