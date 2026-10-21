# Change List — I00:E11:W21

> Recorded 2026-10-21

## Applied

| Change | What it was |
| --- | --- |
| Row delivery | `W21` of [#39](https://github.com/m2ux/prosiform/issues/39) links [#151](https://github.com/m2ux/prosiform/pull/151) and carries a tick in Done. `AC22` of the epic is ticked, and `AC1` of [#144](https://github.com/m2ux/prosiform/issues/144) with it. The epic body was re-read immediately before the patch and compared afterwards; the only lines that moved are W21's row and AC22, and the fourteen planning-folder links the other rows hold are intact. |
| Task closure | [#144](https://github.com/m2ux/prosiform/issues/144) closed as completed, its criterion verified and its pull request merged. |
| Glossary entry | The definition of *resource* in `docs/glossary.md` states the rule the predicate applies — an image whatever file it names — rather than framing a resource by its destination alone. Folded into this row's pull request because the stale phrasing is the behaviour this row changed. |
| Dead imports | `HREF`, `SRC`, `INLINE` and `REFERENCE_USES` leave `cli.py` with the inline walk the shared one replaces. Trivial, and in the same change, because `lint` is what reports them. |

## Held

Nothing. No initiative was needed, no migration arose, and no row was re-prioritised.

## Debt deferred

None. The two limitations the validation records — a remote image warning not at all, and the warning naming no destination — are the design's own wording rather than defects, and both are published by the corpus. Neither is raised as an issue.

## Arising

None. Three notes the epic sync reported — `#100` and `#152` unmatched, and `W15` and `W24` linking task issues rather than pull requests — belong to rows other sessions hold and were left untouched.
