## Overview

Dispatch briefs and authored sections can legitimately share a heading, but compilation currently rejects that combination even though their destinations have distinct identities. Permit those headings while preserving correct links and refusing genuinely ambiguous dispatch selections.

Target: `main`

## Problem

A dispatch named Investigate can lift a brief headed Investigate alongside an authored Investigate section. The compiler reports E_HEADING_COLLISION before publication. Its renderer already assigns distinct ordinal anchors, so this refusal prevents a valid document with separately identifiable destinations.

## Proposal

- **Distinct destinations.**
  Assign generated and authored headings their normal renderer anchors. Ordinary links retain their authored target; dispatch links retain their generated destination, including Mermaid links.
- **Scoped ambiguity checks.**
  Refuse identical dispatch text naming different effective selections. Preserve composition scope checks and heading-depth limits.
- **Published contract and regressions.**
  Align the design and shipped documentation. Exercise both heading orders, briefs, dispatch sets and picks through synthetic corpus fixtures.

## Acceptance Criteria

- [ ] **AC1.** Authored and generated headings with identical text compile with distinct correct destinations in either order, as corpus fixtures with ordinary and Mermaid dispatch links show.
- [ ] **AC2.** Distinct dispatch selections sharing one generated name and conflicting composition scopes remain refused, as their existing negative corpus fixtures show.
- [ ] **AC3.** The published design, documentation and current reviewed implementation agree, as the complete repository checks and revision-bound agent review show.
