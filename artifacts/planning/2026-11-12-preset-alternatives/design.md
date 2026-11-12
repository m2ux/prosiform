# Preset Alternatives

## Goal

A document generic over a kind of work declares one preset per kind as an alternative. A deferred link hands the pick to the agent with a `?` title tag, `pf` answers `?` with the alternatives and when to pick each, and the agent compiles the one that fits its task. The picked alternative's `subst` pairs route the document's links to that kind's material.

## Alternatives

A preset holding `choice` is an **alternative**. `choice` holds one line stating when to pick it.

```yaml
---
prosiform:
  Initiative:
    choice: States a goal and lists its epics.
  Epic:
    choice: Lists its tasks in a Work Breakdown table.
  Hot-fix:
    choice: A fix to a long-lived branch beside all queued work.
    subst:
      - board-delivery.md#record-dispatch-status: hotfix.md#record-hot-fix-dispatch-status
---
```

- **Exactly one is in force.** Wherever a document declaring alternatives is compiled, exactly one of them is in force for it in each bundle: the union every reference reaching it selects, the set its `subst` pairs already resolve through. None, or more than one, fails the run with `E_ALTERNATIVE_UNRESOLVED` and exit status 2, naming each alternative with its choice line in declaration order.
- **Alternatives layer like any preset.** The pick layers over `default`, and an ordinary preset, one with no `choice`, may be selected beside it under the existing union and conflict rules.
- **`default` is no alternative.** It is in force wherever its document is compiled, so a `choice` in `default` is refused.
- **An unpicked alternative is silent.** It raises no `W_PRESET_UNUSED`; an ordinary preset warns as before.
- **`?` names no preset.** A preset named `?` is refused.
- A `choice` holding anything but a non-empty one-line string fails with `E_INVALID_CONVERSION_METADATA`.

## The `?` Tag

`?` in a link title hands the pick to the agent. It stands beside fixed tags as one more comma-separated token, as in `"checks, ?"`.

```markdown
Record the status [¬ Record Dispatch Status](../artifacts/work-kind.md#record-dispatch-status "?").
```

- **Deferred links only.** A run cannot pick for a link it compiles, so `?` is accepted on a `¬` or `¬↳` link and refused on an ordinary, `↳`, `⇉` or `⫽` link.
- **A deferred link to alternatives states its pick.** The run publishing a deferral already checks that its target exists and names its heading. It also checks that a link to a document with alternatives names exactly one of them or carries `?`, never both, since every other form fails the later run.
- **`?` needs alternatives.** A `?` link whose target declares none is refused.
- **The bundle carries `?`.** The deferral publishes its title as authored, beside the destination spelled from the working directory:

```markdown
Record the status [Record Dispatch Status](artifacts/work-kind.md#record-dispatch-status "?").
```

## The Pick

The agent passes the title as `--presets`, as it does for every deferred link. `?` selects no preset, so the run finds no alternative in force and answers with the list:

```text
$ pf -o out artifacts/work-kind.md#record-dispatch-status --presets '?'
error: artifacts/work-kind.md needs one alternative in force:
  Initiative  States a goal and lists its epics.
  Epic        Lists its tasks in a Work Breakdown table.
  Hot-fix     A fix to a long-lived branch beside all queued work.
remedy: rerun with --presets naming the alternative that fits your task
exit 2

$ pf -o out artifacts/work-kind.md#record-dispatch-status --presets Hot-fix
exit 0
```

- One diagnostic answers `?`, a mistyped name and an absent `--presets`, so no flag lists alternatives.
- Exit status 2 publishes nothing, as every failed run does; exit 0 still means the bundles were written.
- The pick's bundle carries its preset qualifier (`--p-<digest>`), so each kind's bundle has its own name.
- A fixed title or `--presets` naming one alternative is a pick its author made: `[Record Dispatch Status](work-kind.md#record-dispatch-status "Hot-fix")`.

## Routing

A pick reaches its own document alone; each link that document writes selects for itself. The pick's `subst` pairs route the document's links to the picked kind's sections, and a link no pair redirects keeps its general route:

```markdown
### Record Dispatch Status

Apply [Record Dispatch Status](board-delivery.md#record-dispatch-status).
```

Under `Hot-fix` that link compiles `hotfix.md#record-hot-fix-dispatch-status`; under `Epic` it compiles the general route as written.

A pair of an alternative is **routing**, not a stand-in:

- A routing pair a link used raises no `W_SUBST_USED`.
- A routing pair warns `W_SUBST_UNUSED` only where no link anywhere in its document names its key. A pair whose link sits in a section the run did not compile is silent.
- A pair of an ordinary preset warns as before, so a stand-in build stays flagged.

## Guide

The guide's symbol grammar gains one entry. **Compiling a link** keeps its wording, since its rule to pass the title as `--presets` already carries `?` to `pf`:

```text
  ?  in a link's title, a preset you pick: pass the title as --presets
     as usual and pf lists the alternatives and when to pick each;
     rerun with ? replaced by the one that fits your task
```

## Change Surface

Expected modules, confirmed when the epics are cut.

### Source (`src/prosiform/`)

- `metadata.py` — the `choice` key, a `choice` in `default`, and a preset named `?`.
- `tags.py` — `?` read as the pick token, matching no preset.
- `closure.py` — `?` on deferred links only, and the pick checks on a deferred link to alternatives.
- `cli.py` — the exactly-one rule and its `E_ALTERNATIVE_UNRESOLVED` diagnostic, listed by `-C`; `W_PRESET_UNUSED` skipping alternatives; routing pairs in `W_SUBST_USED` and `W_SUBST_UNUSED`; the `GUIDE` entry.
- Title readers (`candidate.py`, `bundle.py`, `composition.py`, `dispatch.py`, `rewrite.py`) — `?` carried through `tags.read`.

### Corpus

A work-kind-shaped fixture proves the pattern end to end: a router with three alternatives, a mode linking it with `?`, and each pick's bundle. Further fixtures hold one rule each:

- an entry naming no alternative, an unknown one, or two, fails listing them
- two links picking different alternatives of one document in one bundle are refused
- an unpicked alternative raises no warning
- a `choice` in `default`, an empty `choice`, and a preset named `?` are refused
- a `¬` link and a `¬↳` link publish `?`
- `?` on an ordinary, `↳`, `⇉` and `⫽` link is refused
- `?` naming a target without alternatives, and `?` beside a named alternative, are refused
- a deferred link to alternatives naming none is refused
- a used routing pair is silent; a routing pair no link of its document names warns
- a diagram link alone reaching a document with alternatives fails the exactly-one rule

### Documentation

- `docs/sources.md` — `choice` in the frontmatter table.
- `docs/selection.md` — alternatives under Presets in force; routing pairs under The substitution mapping.
- `docs/references.md` — `?` under Selection by reference and Operators.
- `invocation.md` — Conversion metadata, the pick in Examples, and the Guide paragraph.
- `docs/glossary.md` — alternative, choice line, pick, routing pair.
- `docs/validation.md` — `E_ALTERNATIVE_UNRESOLVED` and the refusals.
- The v1 design states each rule, and the docs repin to the commit adding them.

### Release

The bump follows the previous corpus's run against the new build, with paired contract and Python tags.

## Out of Scope

- A pick on a dispatch link (`⇉`, `⫽`). A later change can add one without undoing this design.
- A pick forwarded to the documents a target links, or applied across a run.
- Migrating work-planner's `work-kind.md`; work-planner is pre-migration.

## Related

- [Symbol grammar in the bundle](../2026-11-08-symbol-grammar-in-bundle/README.md) — a planned hot-fix. If it lands first, the `?` entry joins the shared symbol grammar and every bundle carries it.
