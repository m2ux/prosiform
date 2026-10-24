# Implementation Evidence — W03

> Delivery · Created 2026-10-24

## Executive Summary

The work-planner entry point declares `prosiform.dispatch`, and deliver mode's links to the delivery brief and the work item carry `»` at the places a dispatched session compiles them. AC2, AC3, AC4 and AC5 hold against the recorded evidence below.

**AC1 does not hold against the brief's stated invocation, and the cause is outside this unit's component.** The documented command bundles a mode's own dependency closure, and `SKILL.md` is not a member of it: no mode links the entry point. The declared text is therefore carried by the bundle only where the entry document contributes a source, which is a different invocation. The declaration is in place and correct; what is missing is a route from a mode to the entry document. That route is a change to `skills/` structure rather than to this unit's declaration, and it is left for the record and the user rather than invented here.

## Branch and Commits

The work is on `i01/e09/w03-the-skill-states-what`, based on `i01/e09/workspace`.

| Commit | Subject |
| --- | --- |
| `bbdb9906` | Declare the dispatch text in the skill's entry point |
| `699819eb` | Mark the brief and work item links a dispatched session compiles |

## Where Each Criterion Is Shown

### AC1 — the entry point declares the dispatch text

`skills/work-planner/SKILL.md` holds the mapping, and the text is a nonblank single line with no character `prosiform.dispatch` refuses:

```yaml
prosiform:
  dispatch: A marked link is compiled by the reading agent and handed to a sub-agent, which is the run its material belongs to.
```

The declared text reaches a bundle's opening line, after the entry sentence, where the entry document is a contributing source. Measured on this branch:

```text
Follow [Conventions](#conventions) and [Deliver-Mode](#deliver-mode). The other sections are material those procedures reference. A marked link is compiled by the reading agent and handed to a sub-agent, which is the run its material belongs to.
```

That is the shape `pf -o - -f ../SKILL.md '#conventions' deliver-mode.md` produces. The same text appears in the corresponding hoist-mode and understand-mode bundles.

**Against the brief's documented invocation it does not appear.** See [AC1 Gap](#ac1-gap-the-entry-document-is-not-in-a-mode-closure) for the measurement and the cause.

### AC1 Gap — the entry document is not in a mode closure

`SKILL.md` is reachable from no mode. Deliver mode's prerequisites name artifacts, protocols, `guidelines.md` and two sibling modes; none names the entry point. A bundle is the closure of its entry references, so the entry document's metadata is never among the contributing sources and the opening line is the entry sentence alone.

The measured consequence, with the declaration committed and the mark applied:

| Invocation | Bundle bytes | Declared text present | Opening line |
| --- | --- | --- | --- |
| `pf -o - deliver-mode.md` (from `modes/`) | 43425 | no | `# Deliver Mode` |
| `pf -o - -f ../SKILL.md '#conventions' deliver-mode.md` | 45230 | yes | entry sentence, then the declared text |

A bare `pf -o - SKILL.md` cannot stand in for a mode bundle on this tree: the skill's own cross-document links are written relative to each document's folder, so the entry point's `modes/propose-mode.md` and `advance-mode.md`'s `sync-mode.md` both fail `E_TARGET_NOT_FOUND` when the root is the skill rather than `modes/`. That failure is the pre-existing link-spelling rule the brief records, not a fault introduced here.

Neither a `prosiform.root` declaration on the mode nor an unmarked prerequisite link to `../SKILL.md` supplies the missing route; both were measured and neither puts the declared text in the opening line.

### AC2 — the deliver-mode links carry the mark

Four occurrences inside deliver mode are marked. All four appear in the emitted bundle:

| Line in `modes/deliver-mode.md` | Occurrence | Why it is marked |
| --- | --- | --- |
| 21 | Prerequisites entry, `[» Delivery Brief](../artifacts/delivery-brief.md)` | The brief is the material the dispatched session executes. |
| 25 | Prerequisites entry, `[» Work Item](../artifacts/work-item.md)` | The work item is the file the dispatched session writes to. |
| 110 | Run Delivery Session step 1, `Read the supplied [» Delivery Brief]` | The dispatch instruction itself: the sub-agent reads the brief. |
| 116 | Run Delivery Session step 3, `Call [» Populate Work Item]` | The step that plans the work item a dispatched session owns. |

The emitted bundle, from `pf -o - deliver-mode.md`:

```text
23:- [» Delivery Brief](../artifacts/delivery-brief.md)
27:- [» Work Item](../artifacts/work-item.md)
112:   Read the supplied [» Delivery Brief](../artifacts/delivery-brief.md).
118:   Call [» Populate Work Item](../artifacts/work-item.md#populate-work-item) for each task ...
```

**Left unmarked deliberately.** Line 94's `Call [Populate Delivery Brief]` belongs to the *orchestrating* mode, which composes the brief before it dispatches anything; that material is the reading session's own. Over-marking it would delete the operation from the orchestrator's bundle and nothing else would report it. The prose sentence at line 98, stating that the sub-agent works in the unit's worktree and reads the brief, stays as written — the metadata states what the mark means, the mode states what a session does.

### AC3 — no marked link's target contributes content

The deliver-mode bundle carries five top-level headings, and neither marked target appears among them:

```text
1:# Deliver Mode
195:# Advance-Mode
275:# Hoist-Mode
337:# Sync-Mode
502:# Understand-Mode
```

Neither `# Delivery Brief` nor `# Work Item` — the H1 each artifact opens with — occurs anywhere in the bundle. Nor does either artifact's body: `Populate Delivery Brief` and `Populate Work Item` occur twice each, both as the link text of an unmarked or marked reference in deliver mode itself, never as a heading or as contributing prose.

This was checked on the headings rather than on the marks, as the brief requires. The four targets reach the bundle as two groups — `advance-mode.md`, `hoist-mode.md`, `sync-mode.md`, `understand-mode.md` are compiled, and the two marked artifacts are not.

### AC4 — the shared check is unchanged

```text
86 files checked, 6 findings
```

All six are in `skills/gitnexus/gitnexus-cli/SKILL.md` — five `command specification in the entry point` and one `inline bold lead too wide`. None is in `skills/work-planner/`. The count and the locations are identical to the baseline recorded before the change.

The skill's own 397 tests pass.

### AC5 — every mode bundles within the default budget

Both shapes are reported, since the count depends on the invocation. The default budget is 262144 bytes (`-O`); no figure is close to it.

| Mode | Baseline, mode closure | After, mode closure | Baseline, entry contributing | After, entry contributing |
| --- | --- | --- | --- | --- |
| advance-mode.md | 21987 | 21987 | 23676 | 23792 |
| align-mode.md | 14283 | 14283 | 15968 | 16084 |
| deliver-mode.md | 43413 | 43425 | 45102 | 45230 |
| hoist-mode.md | 4392 | 4392 | 6077 | 6193 |
| plan-mode.md | 28079 | 28079 | 29762 | 29878 |
| propose-mode.md | 3288 | 3288 | 4977 | 5093 |
| revise-mode.md | 3621 | 3621 | 5308 | 5424 |
| standup-mode.md | 19976 | 19976 | 21665 | 21781 |
| sync-mode.md | 15664 | 15664 | 17347 | 17463 |
| understand-mode.md | 1419 | 1419 | 3114 | 3230 |

Two columns move and neither regression is a regression: mode closure grows only in deliver mode, by 12 bytes, which is the four marks at three UTF-8 bytes each. Entry-contributing grows in every mode by 116 bytes — the declared sentence plus its joining space — plus the same 12 in deliver mode. Every mode remains two orders of magnitude inside the budget.

## Checks Run

| Check | Command | Outcome |
| --- | --- | --- |
| Shared skill check | `python3 skills/scripts/check_skill_files.py skills` | 86 files, 6 findings, all pre-existing in gitnexus-cli |
| Skill tests | `python3 -m unittest discover -s test -q` in `skills/work-planner` | 397 tests, OK |
| Mode closure bundles | `pf -o - <mode>.md` from `modes/` | 10 modes, exit 0, bytes as tabled |
| Entry-contributing bundles | `pf -o - -f ../SKILL.md '#conventions' <mode>.md` | 10 modes, exit 0, bytes as tabled |
| Marked link emission | `pf -o - deliver-mode.md` then grep `»` | 4 occurrences emitted |
| Marked target headings | grep `^# ` on the deliver bundle | 5 headings, neither marked target among them |
| Declared-text emission | `pf -o - -f ../SKILL.md '#conventions' deliver-mode.md` | opening line carries the sentence |
| Entry point as bare entry | `pf -o - SKILL.md` | `E_TARGET_NOT_FOUND`, pre-existing link spelling |
| Stale text | grep `dispatch`/`sub-agent` across the skill | no description of an unmarked brief survives |

## Stale Descriptions Checked

- The mode's prose sentence naming the sub-agent stays: it states what a session does, where the metadata states what the mark means.
- `artifacts/delivery-brief.md`'s "The caller resolves gaps before dispatch" remains accurate; the dispatch marks do not change who composes the brief.
- `propose-mode.md`'s "Delegate broad sweeps to parallel sub-agents" names a different dispatch and is untouched.
- No `¬` occurrence was changed. Whether a deferred link publishes its mark is W02's criterion, not this unit's.

## Change List

No plan change was applied and none was held. This unit changed two skill documents and raised no issue, moved no row and placed nothing.

| Kind | Subject | Option taken |
| --- | --- | --- |
| — | None | No plan change arose. A new initiative stays held regardless. |

## Incomplete

**AC1** is met as a declaration and unmet as a bundle outcome under the brief's stated invocation. The missing route from a mode to the entry document is not this unit's component; it is left recorded rather than patched, because the fix is a structural change to how the skill's documents reference one another and that decision belongs to the user.
