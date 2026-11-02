# Validation

The checks [W00](w00.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`99bec9f7`](https://github.com/m2ux/prosiform/blob/99bec9f7548b9910047b7bde663a2eb76efd2e3e/artifacts/planning/2026-10-17-prosiform-v1/design.md#section-composition), the clause landing in `601cba55` with the cycle code settled in `99bec9f7` |
| Branch head | `960613c8` on `i09/e04/w00-design-clause` |

## T1 Inspection of the Pinned Clauses

Read the design at the pinned revision against AC15 and the clauses W01–W10 will cite.

- **Recognition and the operator marks (W01).** *Section composition — Recognition* states the predicate: the label, read after the deferral mark and its blanks are set aside, is plain text of exactly one scalar above U+007F once entities are decoded, with nothing trimmed or normalised, and names the qualifying and non-qualifying forms. *Operator marks* excludes `¬`, `⇉`, `⫽` and the guide's `↳` from the label set, so a lone mark is an ordinary link; only the deferral mark is set aside, so `[¬ →]` is a deferred directive and `[⇉ →]` a dispatch named `→`.
- **Scope, destination sections and contributions (W02).** *The destination scope*, *Destination sections* and *Contributions* state the nearest containing section as scope, one destination section per title per scope, and a contribution beneath a heading naming the target's immediate parent with its blocks and relative depth kept.
- **Source-relative content and occurrences (W03).** *The source of composed content* and *Every occurrence composes* state resolution against the fragment's source and one contribution per directive.
- **Ordering, matching and failures (W04).** *Order*, *Matching*, *Heading depth*, *Generated heading collisions*, *The destination scope* and *Contributions* state the order, exact matching and each structural refusal with its code: `E_UNSUPPORTED_CONSTRUCT` for no scope or no parent, `E_HEADING_COLLISION`, `E_HEADING_DEPTH_OVERFLOW`, `E_TARGET_NOT_FOUND`. A composed heading's depth under its scope counts toward the H6 limit *Depth overflow* states.
- **Recursion and budgets (W05).** *Nested directives*, *Composition cycles* and *Budgets* state composition inside composed content, the cycle refusal with its chain, and materialised bytes counted toward `output-bytes` as they are composed. No budget name is added, so the clause leaves *Resource limits* to I08:E05.
- **Eligibility, deferral and activation (W06).** *The eligible target*, *Deferred composition* and *Activation* state the refusal of a whole document, a non-declaring document, a remote address or a resource; a deferred directive keeping its destination section and contribution heading, whose body is one `↳` line naming the target; and activation as the run that line names.
- **Publication (W07).** *Failure* links *Publication*: every composition failure publishes nothing, under `-c` as without it.
- **Inline-only targets (W08).** *Inline-only targets* and the amended *Exactly-once coverage* state that a directive-only target joins no group and a contribution is tracked apart from group coverage.
- **Presets and `subst` (W09).** *Presets and `subst`* states that the scope's title selects the target's presets, whose `subst` governs the contribution, and that a `group` pair places no contribution. *The eligible target* states that the writer's `subst` redirects the directive.
- **The surrounding clauses agree.** *Unsupported extensions*, *Compile before publishing* step 6, *A deferred link's destination*, *Preservation*, *Exactly-once coverage* and *Link classification — Composition* name the directive and link the section. *Adversarial acceptance fixtures — Composition* lists the fixtures W01–W09 owe.
- **Every cited title stands.** No existing clause title changes; every new clause is an addition.
- **Revision history.** The clause lands in engineering commits `601cba55` and `99bec9f7`, and the README pin moves to `99bec9f7` in `960613c8`, before any compiler row of the epic changes the build.
- **The requirement trace.** The initiative record's goal trace maps G3 to E04 AC1–AC19; AC15 is this clause.

Result: pass.

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at the README pin `99bec9f7`, exit 2.

- Every target before `conformance` passes, `vocabulary` among them with the *composition directive* row added to `docs/glossary.md`; `independence` and `mock-scenarios`, run on their own, pass.
- `make conformance` fails with eight declarations naming no clause: `Resource limits — -B`, `-E`, `-F`, `-I`, `-L`, `-N`, `-O` and `-T`. The 22 new *Section composition* clauses are listed as covered by no fixture, which the report counts rather than fails.
- The eight failures belong to I08:E05: engineering commit `a7069f30` restates the budgets as `--budget NAME=VALUE`, and its fixtures and build sit on `i08/e05/main`, whose review pull request [#550](https://github.com/m2ux/prosiform/pull/550) has not merged into `main`. Pinning `a7069f30` alone reproduces the same eight failures, so this clause adds none.

Result: fail, blocked on I08:E05 reaching `main`. The check passes once `main` carries #550 and `i09/e04/main` takes `main`.
