# I05:E03:W09 Change List

The plan changes this delivery session made, and those it held.

## Applied

- **Folded work, I05:E03 W09.** Only a command line holding no argument prints the guide; arguments naming no entry reference (`-c`, `-d json`, `-o DIR` alone) stay `E_INVALID_USAGE`. The design's CLI contract states it.
- **Folded work, I05:E03 W09.** The corpus runner invokes a manifest declaring no argument and no fault as the bare command, with no `-d json`, and the manifest schema admits an empty argument list, so `fixtures/cli/informational-guide-response` can state AC19. `checks/runner.py`, `checks/README.md` and `fixtures/README.md` state the rule.
- **Folded work, I05:E03 W09.** `make invocation` holds `invocation.md` to stating that `pf` with no arguments prints the guide.
- **Folded work, I05:E03 W09.** The design's Clean Markdown rule and `invocation.md`'s Output section state that a dispatching bundle opens on its Prosiform section; the design marks *guide* and the glossary defines it. Design pinned at `9545ef64`.
- **Folded work, I05:E03 W09.** `src/tests/test_handoff_round_trip.py` reads the Dispatch protocol a mode bundle opens with in place of the retired bootstrap symbol row.

## Held

None.

## Fixtures outside this unit's families

None under `fixtures/dispatch` or `fixtures/run-set` changed. `cli/a-command-line-naming-no-entry-reference`'s description now states that only a command line holding no argument prints the guide.

## Deferred debt and arising issues

- **Deferred debt.** None.
- **Arising.** None.
