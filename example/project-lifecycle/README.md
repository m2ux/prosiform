# Project Lifecycle Example

A skill whose project lifecycle and engineering lifecycle are independent of each other. The project lifecycle moves issues across a board, one [mode](modes/) per transition. The engineering lifecycle, the SDLC, decides how the work inside an issue is planned, built and verified. The user tells the skill which SDLC the board follows, and each stage needing engineering practice takes it from that SDLC. How the skill does that is under [Ports and adapters](#ports-and-adapters).

This file declares nothing, so no bundle carries it.

## Graph

```mermaid
flowchart TD
  start(["start"]) --> choose["choose SDLC"]
  choose -->|user names one| propose["propose"]
  propose -->|proposed| plan["plan"]
  plan -->|planned| advance["advance"]
  advance -->|dependency open| held(["stays Planned"])
  advance -->|ready| deliver["deliver"]
  deliver -->|in review| sync["sync"]
  sync -->|done| done(["Done"])
  plan -.->|asks| planning[["planning practice"]]
  deliver -.->|asks| implementing[["implementation practice"]]
  sync -.->|asks| verifying[["verification practice"]]
  subgraph sdlc["the SDLC the user chose"]
    planning
    implementing
    verifying
  end
  sdlc -.->|user chose ad-hoc| adhoc["ad-hoc"]
  sdlc -.->|user chose waterfall| waterfall["waterfall"]
```

*Solid edges are board transitions, each labelled with the outcome that takes it. Dotted edges are the practice a stage takes from the SDLC the user chose.*

## Stages

### Choose SDLC

The first time the skill works on a board, it asks the user which SDLC the board follows and offers the ones it knows: `ad-hoc` and `waterfall`. The user answers in their own words, such as "we run waterfall", and the board keeps that choice. The user changes it by asking. A name the skill does not know is refused with the choices listed, and a board whose user has named none follows `ad-hoc`. The rule is [Configure](SKILL.md#configure).

### Propose

A proposal enters the board in **Proposed**, as [Propose Mode](modes/propose-mode.md) states.

### Plan

A proposal is broken into epics and tasks, and the board's SDLC states what that plan holds before it is **Planned**: under waterfall, signed-off requirements and design. The transition is [Plan Mode](modes/plan-mode.md), and the practice is [On Plan](sdlc/port.md#on-plan).

### Advance

Planned work moves to **Ready** once each dependency is **Done** and it carries a priority. Work with a dependency still open stays **Planned**. The transition is [Advance Mode](modes/advance-mode.md).

### Deliver

Ready work moves to **In Progress**, is built as the board's SDLC prescribes, and moves to **In Review** with its pull request. Under waterfall it is implemented to the signed-off design and integrated, and any change to requirements or design waits for sign-off. The transition is [Deliver Mode](modes/deliver-mode.md), and the practice is [On Deliver](sdlc/port.md#on-deliver).

### Sync

Reviewed work shows what the board's SDLC asks, merges, and moves to **Done**. Under waterfall, that is passing system tests and the stakeholders' acceptance. The transition is [Sync Mode](modes/sync-mode.md), and the practice is [On Verify](sdlc/port.md#on-verify).

## Ports and adapters

The skill follows the ports and adapters pattern, with prosiform's link operators as the language it is written in.

| Pattern | Here | prosiform |
| --- | --- | --- |
| core | the board transitions in [`modes/`](modes/) | documents gathered by `group: {modes: 2}` |
| port | the hook sections of [`sdlc/port.md`](sdlc/port.md) | sections a mode reaches by fragment, as `port.md#on-deliver` |
| call through the port | a mode step naming a hook | a deferral, `[¬ Deliver Practice](../sdlc/port.md#on-deliver)`, compiled by a run of its own |
| adapter | [`sdlc/ad-hoc.md`](sdlc/ad-hoc.md), [`sdlc/waterfall.md`](sdlc/waterfall.md) | documents carrying `## Plan`, `## Deliver` and `## Verify` |
| binding an adapter | the port's `waterfall` preset | `subst: [{ad-hoc.md: waterfall.md}]` |
| selecting a binding | the board's recorded SDLC | `pf sdlc/port.md#on-deliver --presets waterfall` |
| default binding | `ad-hoc` | the `default` preset, which substitutes nothing |
| the adapter's practice in the step | the hook's result | composition, `[↳ Practice](ad-hoc.md#deliver)` |
| an adapter missing a hook | a build failure | `E_TARGET_NOT_FOUND` on the composed section |
| which adapter was bound | the run's diagnostics | `W_SUBST_USED` |

The SOLID principles follow from that shape:

- **Single responsibility.** A mode moves an issue between stages, an adapter states one SDLC's practice, and the port binds one to the other.
- **Open–closed.** An SDLC is added as one adapter and one preset in the port. No mode changes.
- **Liskov substitution.** Every adapter carries every section the port composes, so any one stands in for `ad-hoc`; a missing section fails the hook's build.
- **Interface segregation.** A mode step names the one hook it calls, and the hook composes the one section of the adapter it needs.
- **Dependency inversion.** Modes name the port and never an adapter; the preset selected at the hook's build supplies the adapter.

## Building it

From this folder:

| Invocation | Bundle |
| --- | --- |
| `pf SKILL.md` | the skill: the board stages, the modes and the hook links |
| `pf sdlc/port.md#on-deliver` | the delivery practice of a board recording no SDLC |
| `pf sdlc/port.md#on-deliver --presets waterfall` | the delivery practice of a waterfall board |

A hook built without `--presets waterfall` warns `W_PRESET_UNUSED` for the preset it left unselected, and publishes.

[`expected/`](expected/) holds the folder each build writes, one per command, as `pf -o expected/<case> <arguments>` writes it. [The example's tests](../../src/tests/test_example_project_lifecycle.py) compile every hook with and without `waterfall`, and the skill, and hold each written folder to its committed one. The SDLCs they compile are read from the port's presets, so an adapter added to the port needs an expected folder for each hook. They also hold the claims below: the hook links the skill's bundle publishes are the port's hooks, an adapter missing a hook section fails, and an adapter binds without changing the skill's bundle.

![SKILL.md, the five modes and the port on the left. On the right, the skill's bundle: the board stages, Configure, the SDLC hook rule, and the modes under one Modes group, each hook link pointing at sdlc/port.md.](../../docs/images/lifecycle-skill.svg)

*The skill built from its entry point, `SKILL.md`. Each hook stays a link for its own build, so no SDLC's practice is in the bundle.*

![The port and both adapters on the left. On the right, the on-deliver bundle with the ad-hoc adapter's Deliver section composed beneath the hook.](../../docs/images/lifecycle-ad-hoc.svg)

*The `on-deliver` hook built with no `--presets`.*

![The port and both adapters on the left. On the right, the on-deliver bundle with the waterfall adapter's Deliver section composed beneath the hook.](../../docs/images/lifecycle-waterfall.svg)

*The same hook built with `--presets waterfall`: one link, the other adapter.*

## Adding an SDLC

1. Write `sdlc/<name>.md` with `## Plan`, `## Deliver` and `## Verify` sections.
2. Add a `<name>` preset to [`sdlc/port.md`](sdlc/port.md) substituting `ad-hoc.md` with `<name>.md`.
