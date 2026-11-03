# Change List — I10:E04 W05–W07

The plan changes this delivery session made under its allowance, and those it held.

## Applied

- **Folded work** — the README's design-profile badge is repinned from `682cdf7e`, which the rewritten engineering history left on no branch, to its twin `2921f91a`, whose `design.md` is identical, as its own commit on this unit's branch (coordinator, 2026-11-03), so the catalogue check's CI run resolves it. Hot-fix F00 ([#625](https://github.com/m2ux/prosiform/issues/625)) makes the same change on `main`. The unit's rows, criteria and dependencies stand as planned.

## Held

- **Folded work, for W17** — `unbootstrapped` is removed from the scorer and its tests by this unit (user decision, 2026-11-03), so [I10:E04](https://github.com/m2ux/prosiform/issues/579) W17's triage rubric in `RUNBOOK.md`, which is not on this base, drops that class's row when it adds the run classes. Held as a note for W17's work item rather than an edit to it, since W17's file is the session delivering it to write.
- **Design decision, W05** — `inline-bootstrap`'s `SKILL.md` keeps the one sentence "Run `pf`." beside its `↳` line, as `bootstrap-audit`'s does, since the bootstrap instruction names no `pf` and a skill holding the line alone gives a session no way to learn the command exists. Recommended: keep it; the alternative is a bootstrap instruction naming `pf`, which changes every bootstrap session.
- **Design decision, W07** — the material a deferral activates states its one edge as "Take the transition labelled `<label>`.", a sentence the corpus reads only in a bundle; a state document's own transition keeps the existing sentences. Recommended: keep it, so a deferred transition is the only place a label stands without a condition.
