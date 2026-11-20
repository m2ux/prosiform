# Test Results

Results for F30 at `2df103456` on `f30-capability-levels`, run on 2026-11-20 in the unit checkout.

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

## T8 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2282 passed), harness (1136 passed), corpus (693 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
