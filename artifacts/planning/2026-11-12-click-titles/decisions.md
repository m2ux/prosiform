# Decisions

## Goal

Approved by the user, 2026-11-12, as a new initiative: a Mermaid `click` line's quoted tooltip is read as the link's title, so `click Intake href "activities/intake.md" "⇉"` bundles as a dispatch and `"¬"` as a deferral. Both `click <node> href "<destination>" "<tooltip>"` and `click <node> "<destination>" "<tooltip>"` are covered, the Diagram links documentation states it, and a release carries it.

## Confirmed

1. **A new initiative.** Feature-scale work, raised straight as an initiative with no proposal. Approved by the user, 2026-11-12.
2. **Plan only.** No delivery is dispatched from planning; the user dispatches the rows.
3. **The release follows the project's procedure.** [Cutting a release](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md#cutting-a-release): a release branch, one version commit, the number chosen by the previous contract tag's corpus, the release merged into `main`, and the paired tags on that merge.

## Defaults Taken

Taken in Plan mode, 2026-11-12, and confirmed by the user the same day: 1 and 3 (with 4) as the tooltip design, 7 as the epic shape.

1. **The tooltip carries the operator and the tags.** A Markdown link carries its operator at the start of its text and its preset tags in its title; a click has one quoted string beside its destination, so the tooltip carries both. Marks opening the tooltip, followed by a blank or by the tooltip's end, state the operator under the [Operators](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/references.md#operators) rules, combinations and refusals alike. The rest of the tooltip is read as a Markdown link's title is, `?` included. So `"⇉"` is a dispatch, `"¬ ?"` a deferral leaving the pick to an agent, and `"checks"` an ordinary link selecting `checks`. Set aside: the tooltip as tags alone, which cannot carry `⇉`; the tooltip as the operator alone, which leaves a deferral no way to pick an alternative.
2. **A mark needs no text after it in a tooltip.** A link's text needs a blank and text after its marks, because the text is what the reader sees; a tooltip `"⇉"` is all mark. A mark followed directly by text, `"⇉Intake"`, opens no operator and is an unknown tag, as `[⇉Sync](sync.md)` is an ordinary link.
3. **Every operator.** `¬`, `⇉`, `⫽` and `↳` and their accepted combinations, each published as Operators states. Set aside: `⇉` and `¬` alone, which would leave a second operator rule for diagrams.
4. **A class diagram's `link` with a tooltip reads alike.** It shares the quoted-destination grammar with `click`, so one rule covers every quoted diagram destination. A sequence diagram's `link` and `links` carry no tooltip and stay operator-less.
5. **The tooltip is carried as written.** Only the destination is rewritten, as each operator's publication states; every other byte of the fence stays as written.
6. **The retired rule leaves.** The design's and documentation's statements that a Mermaid tooltip selects no preset and a diagram link carries no operator are replaced, and the fixture encoding them, `diagram-tooltips-supply-no-preset-selection`, is removed rather than kept as a refusal.
7. **Two epics.** The release is its own epic after the feature epic. Its pull request is the release branch into `main`, and its tags go on the merge, which can only happen once the feature epic has reached `main`; a release row inside the feature epic would wait on that epic's own merge. Set aside: one epic holding the release row.
8. **The build and its fixtures join.** The build change turns the retired fixture red, so the build row and the fixture row share one pull request and `make check` stays green on the epic base.

## Planning

Taken in Plan mode, 2026-11-12; each can be reopened.

- **The initiative takes I17**, I16 being the highest of any state.
- **No lanes.** Five rows, landing one unit at a time.
- **Five rows and twelve criteria.** The initiative three criteria; E00 four rows and six criteria; E01 one row and three criteria.
- **Epic priority.** E00 `priority: 2`, E01 `priority: 1`, the map the dependency check proposes, applied by the user's decision, 2026-11-12. The initiative carries no priority label, so Advance leaves it at Backlog.

## Board

- **I15 E02 and I16 take their board fields.** By the user's decision, 2026-11-12, the Python board's Initiative and Epic fields gained I16's options and `I15:E02 Agent Pick in Real Use`, and #733 to #737 carry them; recorded in [board placement](board.json).
- **Advance after planning.** Run on the Python board, 2026-11-12: Sync found no delivery to record on I01, I12, I15, I16 or I17, and the queue proposed no move. Its `rank` lines name I12 E00, I15 E02 and I16 E00 to E02 as unranked epics.

- **I17 ranked and started.** The user labelled I17 `priority: 2`, beside I15, 2026-11-12. Advance then moved I17 to In Progress and E00 to Ready, each assigned to the user.

## Delivery Branches

- **E00's bases.** `i17/e00/engineering` and `i17/e00/main`, cut 2026-11-12 from `engineering` at `f90d0cf` and `main` at `4cb6b5c`. `config/branches` is absent at both; the names come from `workspace`, which states `engineering`, `main` and `workspace`.
- **E00's review pull requests open with the first task merge.** GitHub refuses a pull request between a base and the branch it was cut from, since there are no commits between them.
- **E02 releases from `release/vX.Y.Z`.** By the user's decision, 2026-11-12, the release row follows [Cutting a release](https://github.com/m2ux/prosiform/blob/4cb6b5c4eda9fb6728b4a378714c474dc47eaf2d/docs/versioning.md#cutting-a-release): a `release/vX.Y.Z` branch from `main`, pull-requested into `main`, with no `i17/e02/main` base. Set aside: an epic base for the release.

## Joins

- E00:W01 and E00:W02 join: the build change fails the retired fixture until the fixtures change with it.
- E00:W00 and E00:W01 stay split: the design is on `engineering` and the build on `main`, two long-lived branches.
- E00:W01 and E00:W03 stay split: the docstrings travel with the build, the documentation pages follow once the behaviour is on the epic base.

## Link Invocation

Hoisted from [#747](https://github.com/m2ux/prosiform/issues/747), 2026-11-13, by the user's decision: a new epic, E01 Link Invocation, ahead of the release, which becomes E02, so one release ships the tooltip rule and the link entry. #747 is closed as not planned, tracked in E01.

1. **Operator marks are ignored at the entry.** By the user's decision, 2026-11-13: marks opening a link's text or a tooltip are agent directives at the content level, acted on before the agent runs `pf`, and checked when `pf` compiled the source; the entry strips them unchecked and compiles the destination with the link's presets. `?` is a title tag and keeps its meaning. Set aside: checking marks under the Operators rules, which only blocks an agent on a link `pf` itself published; refusing dispatch links; an operator shaping the run.
2. **A stray pick is invalid usage.** `--pick` beside an entry carrying no `?`, a plain path included, exits `2`. Set aside: a pick on a plain path; ignoring it.
3. **Preset Alternatives is reworded on delivery.** Its statement that a pick passes as `--presets` is reworded by the documentation row, once the build is on the epic base.
4. **Five rows, three joined.** The design on `engineering` first; the build, the corpus fixtures and the checks and eval harness in one pull request, since retiring `--presets` turns each red; the documentation last.
5. **`priority: 2`.** Beside E00, ahead of the release's `priority: 1`.
6. **Task-level edges to E00.** Each row names the E00 row it consumes; the initiative edge E01 on E00 is overbroad, so the release names both epics.

## Alignment

By the user's decisions, 2026-11-13, on the I17 alignment findings.

1. **Cutting a release states the tag target within E02.** The procedure tags the version commit, while the project tags the release merge on `main`. E02 gains W00, which states that the release pull request merges before tagging and the tags name that merge, and AC4; W01 depends on W00. Set aside: a Non-Goal keeping the procedure as written; tagging the version commit.
   - **Re-pin pending.** Once W00 lands on `main`, the initiative's R3 and E02's R2 are re-pinned to that commit.
2. **Open criteria hold one condition each.** The initiative's AC3 splits into AC3 and AC5, and its AC4 into AC4, AC6 and AC7; E02's AC2 splits into AC2 and AC5. Delivered criteria stay as written.
3. **Review fixes take no row.** #756 stays without an E01 row, as E00's review fixes did.

## Dependency Check

Recorded in [Goal trace](goal-trace.md#checks).

## Open Questions

None.
