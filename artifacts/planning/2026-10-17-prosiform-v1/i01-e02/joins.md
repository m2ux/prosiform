# I01:E02 delivery units

W04 and W06 share one pull request covering AC2, AC3 and AC8. Both work in `src/prosiform/grouping.py`: the pooled section names each contributor, and every heading naming that contributor reads the same group-wide name. Their combined validation checks mixed contribution shapes, a pooled section contributed by a subset of the group, trailing-word removal, and distinct whole-document destinations. Their prerequisites are W02 and W05; neither depends on the other.

W07 takes its own pull request for generated-input detection (AC9). W08 follows W04, W06 and W07 to verify the documented commands and diagrams against their output (AC6).

The user approved this grouping on 2026-10-22. The dependency check reports no problems and no unaccounted independent pairs. The two longest chains are W01 → W02 → W04 → W08 and W01 → W05 → W06 → W08. This epic-only check has no cross-epic component comparison; task numbering retains the delivered row identities.

Each pair below is two rows where neither depends on the other, and each takes its own pull request for the reason given.

The epic's rows fall into three subjects: what the group emits around its pooled sections (W01, W02, W04, W05, W06), the spelling of a generated heading (W03), and what a generated heading means to a later run (W07). A pair drawn from two subjects shares no component and no criterion. W08 records what the others settled and depends on each of them, so it pairs with none.

- E02:W01 and E02:W03: the structures a merged group emits around its sections and the casing of a generated heading share no component. One lands in the grouping arrangement and the other where the bundle's own headings are written.
- E02:W01 and E02:W07: whether a wrapper section is emitted and whether a bundle is readable as input are separate conditions, verified by fixtures the other does not touch.
- E02:W02 and E02:W03: the destination a member resolves to is unchanged by how a generated heading is spelled, and the casing reaches constructions outside the merged group entirely.
- E02:W02 and E02:W05: the destination a whole-document reference reaches and the text the heading at that destination carries are separate conditions, and each is verified by fixtures the other does not touch.
- E02:W02 and E02:W06: the destination a reference reaches and the agreement between a member's two names are separate conditions over the same arrangement.
- E02:W02 and E02:W07: the destination a member resolves to inside one bundle and the readability of that bundle as a later source answer to different criteria.
- E02:W03 and E02:W04: the casing convention over generated headings and the condition a pooled section splits on share no criterion; the casing reaches constructions outside the merged group entirely.
- E02:W03 and E02:W05: the casing convention over generated headings and the path run a member heading carries share no criterion.
- E02:W03 and E02:W06: the casing a heading is written in and the text it carries are separate conditions, and the casing reaches constructions outside the merged group.
- E02:W04 and E02:W05: the condition a pooled section splits on and the run a member heading is shortened to are separate conditions, each with its own fixtures.
- E02:W04 and E02:W07: the headings a pooled section emits and the readability of a bundle as a later source answer to different criteria.
- E02:W05 and E02:W07: the text a member heading carries and the readability of a bundle as a later source answer to different criteria.
- E02:W06 and E02:W07: the agreement between a member's two names and the readability of a bundle as a later source answer to different criteria.
