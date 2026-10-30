# Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| An accepted finding changes the design before the corpus or the build | AC3 | E01; this epic records the design before its build | The planning record is that design change. The epic criteria below are the build that follows it | R1, the v1 design: a finding changes the design first |
| A linked file that omits its root follows the root of the context that reached it, and one file is rendered once for each distinct root that reaches it | Proposed AC14, not yet on the initiative | This epic | AC1–AC8 | None. R6 states the opposite rule for the delivered epic. This record is the later decision |

AC12 and AC13 stay with Document Metadata. AC13 answers R6, which requires every absent root to use the invocation working directory, including linked files. This epic does not cite AC13, because its criteria depart from that source.

Proposed initiative row, unpublished:

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| E08 | Inherited Roots | AC3, AC14 | | |

Proposed AC14:

A linked file that omits its root follows the root of the context that reached it, and one file reached under more than one root is rendered once for each, as the root-resolution conformance suite demonstrates.

No whole-epic dependency. W01 consumes the per-file root walk from E06 W08. W03 consumes the author-facing contract from E06 W11. The other rows of that epic produce nothing this plan consumes.
