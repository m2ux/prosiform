# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w14`, branch `i02/e00/w14-runtime-rules-out-of-guidelines`, cut from `i02/e00/main` at `ad8f1a2a`; commits `afbc0004`, `4c2b554c`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`. This row changes nothing under `src/`.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 260 fixture(s), 260 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build `PROSIFORM_BUILD` names | 0 |
| `make conformance` | 304 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1101 passed | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

## Migrated Rule

Before, `guidelines.md` Modes:

```markdown
- **Interview.**
  A question the user must decide is put this way.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
```

and `rules.md`:

```markdown
- **Decisions.**
  Ask one at a time, following the [¬ interview rules](guidelines.md#modes). A decision the run's [allowance](artifacts/plan-change.md#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
```

After, `rules.md` only:

```markdown
- **Decisions.**
  A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](artifacts/plan-change.md#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
```

## Repointed Links

| File | After |
| --- | --- |
| `rules.md` | Decisions carries the rule; no self-link |
| `modes/plan-mode.md` | `… to the user as an [interview](../rules.md), the proposal the recommended answer.` |
| `modes/hoist-mode.md` | `An option put to the user is offered as an [interview](../rules.md).` |
| `modes/deliver-mode.md` | `Confirm the units to dispatch and the rows to release as one [interview](../rules.md).` |
| `modes/revise-mode.md` | `Interview the user, putting each question as the [Rules](../rules.md) state, until the change and its scope are clear.` |
| `protocols/epic-integration.md` | `Put a draft still awaiting its ready mark to the user as an [interview](../rules.md), naming …` |
| `modes/advance-mode.md` | `… is settled as [Held Change](…) states, put as an [interview](../rules.md) where it reaches the user.` |

Each replaced `[¬ Interview](../guidelines.md#modes)` (advance: `[¬ guidelines](../guidelines.md#modes)`; rules: `[¬ interview rules](guidelines.md#modes)`). revise-mode's other links to the guidelines keep their destinations.

## Guidelines

| Rule | Before | After |
| --- | --- | --- |
| Prose — One home per rule | … the procedure step it binds, or the Modes, Artifacts, or References section below. | … the procedure step it binds, [Rules](rules.md) or [Conventions](conventions.md) when it binds every mode, or the Modes, Protocols, Artifacts, or References section below when it governs how that kind of file is written. |
| Modes — Interview | The rule above | Removed |
| Modes — Step rules | A rule that binds every mode is added to this section. | A rule that binds every mode sits in [Rules](rules.md), or in [Conventions](conventions.md) when it is a skill-wide prerequisite. |
| Protocols — Step rules | A rule that binds every protocol is added to this section. | A rule that binds every run of a protocol sits in [Rules](rules.md); a rule on how every protocol is written is added to this section. |
| Artifacts — Step rules | A rule that binds every artifact is added to this section. | A rule that binds every run of an artifact operation sits in [Rules](rules.md); a rule on how every artifact is written is added to this section. |

`example/guidelines.md` already places what binds every mode in the rules and conventions files; it is unchanged.

### Other Runtime Guidance

- `guidelines.md` Operations — Execution, Local scripts and Bodies state how command specifications are written; their runtime counterparts are `conventions.md` Repository, Boards, Scripts and Bodies. No runtime file links them.
- No other link from a mode, protocol, artifact, `rules.md` or `conventions.md` reaches either guidelines file.

## Bundles

Each mode bundled with `pf -o <scratch>/<mode>.md modes/<mode>-mode.md` from `example/work-planner`, default budgets. Every bundle exits 0. Only revise carries links to `guidelines.md` (4, none to `#modes`).

| Mode | Exit | Bytes |
| --- | --- | --- |
| advance | 0 | 172,013 |
| align | 0 | 132,956 |
| deliver | 0 | 246,749 |
| hoist | 0 | 85,645 |
| plan | 0 | 207,472 |
| propose | 0 | 26,340 |
| revise | 0 | 6,793 |
| standup | 0 | 168,176 |
| sync | 0 | 157,999 |
| understand | 0 | 47,326 |

## Fixtures

- `a-procedure-and-everything-it-reaches`: re-recorded. Its three deferred links are gone; the description's closing sentence reads `The bundle carries no deferred link.`, and the clause `Link classification and resource handling — The deferral mark` leaves its list. The three modes reached as whole documents (propose, sync, understand) and the rules and conventions documents still hold.
- `every-document-under-a-directory-merged`: re-recorded; its description names the artifact group, its Overview, Operations, Fields and Commands sections and the References group, all still present.
- `a-bare-fragment-and-its-referring-document`, `two-selected-sections`, `validation-without-publication`: unchanged output, unchanged description.

AC12 holds for all five usage fixtures.
