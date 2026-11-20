# Test Results

Results for F30 at `46d0f3047` on `f30-capability-levels`, run on 2026-11-20 in the unit checkout.

## T1 Dispatch Link Model

`dispatch/a-dispatch-to-a-target-with-a-level-names-its-model`: `[⇉ Gather the Facts](gather.bundle.md) on haiku, then` for a `retrieval` target, `[⇉ Record](record.bundle.md).` with nothing after the link for a target stating no level, and the lifted brief's line `[⇉ Decide](decide.bundle.md) on opus`. Held.

## T2 Set and Pick Lines

`dispatch/a-set-member-and-a-pick-line-name-their-models`: the `⫽ Dispatch Set` lines read `on haiku` and `on opus`, and each `⇉ Dispatch Pick` line carries its own alternative's model before the em dash, `on opus — Lists its tasks.` and `on haiku — One pull request's worth of work.`. Held.

## T3 Dispatch Below a Dispatch

`dispatch/a-dispatch-below-a-dispatch-takes-the-entry-s-map`: `gather.md`, dispatched from the entry, dispatches `decide.md`; its bundle reads `[⇉ Decide](decide.bundle.md) on opus`, the entry's mapping, though `gather.md` maps `judgement` to `haiku` itself. Held.

## T4 Entry Title Tag

`dispatch/an-entry-title-tag-selecting-levels-changes-the-models`: `pf '[Guide](guide.md "trial")'` publishes `on haiku` for both the `retrieval` and the `judgement` target, the `trial` preset mapping `judgement` to `haiku` over `default`'s `opus`. Held.

## T5 Refusals

- `dispatch/an-unmapped-level-fails`: `E_LEVEL_UNMAPPED`, exit 1, naming `'deep'`, at the dispatch's line.
- `dispatch/a-level-on-the-entry-fails`: `E_LEVEL_ON_ENTRY`, exit 1, naming `'judgement'`.
- `frontmatter/a-malformed-level-fails` and `frontmatter/a-malformed-levels-fails`: `E_INVALID_CONVERSION_METADATA`, exit 1, naming `prosiform.default.level` and `prosiform.default.levels` at the value.

Each publishes nothing. Held.

## T6 Guide

`cli/informational-guide-response`: `pf` with no arguments exits 0 and prints "Where on <model> follows a ⇉ link, start its sub-agent on that", "model; where nothing follows, start it as your harness does by", "default.". `test_cli.py` holds the sentence among the dispatch rules. Held.

## T7 Documents

`docs/sources.md` states `level` and `levels` in its field table; `docs/dispatch.md` owns the rule in its Models section and the guide paragraph; `docs/glossary.md` defines level and level map; `docs/validation.md` lists both codes; the design states both fields under Conversion metadata, the rule as Dispatch models, both codes under Metadata failures and the guide's sentence. Held.

## T9 Regressions

- `dispatch/a-shortcut-reference-dispatch-names-its-model`: `[⇉ Gather] and record.` with its definition publishes `[⇉ Gather](gather.bundle.md) on haiku and record.`.
- `dispatch/an-unmapped-level-in-an-unselected-heading-publishes`: a heading outside the selection dispatching at an unmapped level leaves the run publishing, the selected dispatch reading `on opus`.
- `dispatch/a-diagram-dispatch-names-its-model-in-a-comment`: each click to a levelled target gains `%% <node> on <model>` beneath it, at the click line's indent inside a list item too, a tooltip tag selecting the target's other level, and a click to a target with no level gains none.

Held.

## T8 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2282 passed), harness (1139 passed), corpus (696 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T10 Model Specimen

A survey entry mapping `retrieval` to `haiku` and `judgement` to `opus` dispatches Tally (`retrieval`) and Verdict (`judgement`), each writing one file under `actions/`; the `link` arm dispatches by `⇉` links, published with `on <model>` after each, and the `diagram` arm by a flowchart's clicks, published with `%% <node> on <model>` beneath each. Each run is one headless Claude Code session on `claude-opus-5-5`, in a workspace of its own with this branch's `pf` on its path, given `Follow the instructions in the bundle at survey.bundles/survey.bundle.md.`; the model each sub-agent started on is read from its `Agent` call in the session's transcript.

| Arm | Runs | Starts naming the published model | Runs writing every action file |
| --- | --- | --- | --- |
| `link` | 3 | 6 of 6 | 3 of 3 |
| `diagram` | 3 | 6 of 6 | 3 of 3 |

Every Tally started on `haiku` and every Verdict on `opus`. Held.

An earlier round under a restricted tool allowlist is not counted: the allowlist denied the agents' own `pf` invocations and every sub-agent's shell, so four of six runs stopped short. Its seven starts all named the published model.
