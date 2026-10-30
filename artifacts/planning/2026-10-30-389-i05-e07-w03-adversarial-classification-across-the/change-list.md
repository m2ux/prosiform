# I05:E07:W03 Change List

The plan changes this delivery session met, each held rather than applied, with the option it recommends.

## Applied

None. This session holds no change allowance, so every plan change below is held.

## Held

- **Half the matrix's cells predict a pass, not a class.** The work item states that each departing script runs every dispatch scenario in both forms and each cell carries the class that script predicts. Two scripts change nothing for most of the corpus: `STUB_AGENT_SEQUENTIAL` only affects a scenario stating a set, and `STUB_AGENT_ANSWER` only one stating a returned question. Their unaffected cells are asserted to pass, and the prediction table records `None` for them, so the table states the corpus's own account of which check each departure fails. **Recommended:** keep it as delivered. A cell forced to carry a class would need a departure the scenario cannot express, and asserting the pass is the stronger reading: it fails when a class fires where its cause is absent, which is the misfire the row exists to catch.

- **`STUB_AGENT_STOP` is a completion departure, not a dispatch one.** AC4 names "the class its departing stub agent states", and the STOP script states a walk that stopped short, so all eight of its cells read `unfinished`. The completion check is read before any dispatch check, so a stopped run is never `undispatched` however few sub-agents it started. **Recommended:** keep it. The script is one of the four the brief names and its value is the ordering held across the corpus rather than one scenario; the Test part of the work item states that reading explicitly.

- **The prediction table lives in the test, not in `scenarios.toml`.** Which class a departure raises for a scenario follows from the scenario's own trace, so the table could be derived. It is stated as a literal instead. **Recommended:** keep the literal. A derivation would assert the scorer against itself; a hand-stated table is the second opinion the matrix exists to be, and `test_the_departure_table_names_every_dispatch_scenario` fails if the corpus gains a scenario the table does not name.

- **One run per script, not one test per cell.** A script's whole corpus is one `eval_run`, and the eight cells are asserted inside a single parametrised test. **Recommended:** keep it. Eight separate runs per script would be thirty-two runs where four suffice, and a failure still names its cell in the assertion message.

- **The departure table is typed `Failure | None`, importing `Failure` from `score.py`.** The test compares each cell against the enum rather than its string. **Recommended:** keep it. `Failure` is already public in `score.py` and the comparison then fails to type-check if a class is renamed, which a string literal would not.

- **`run.py`'s spent-login refusal is not exercised across the corpus.** A run whose every session errored is `refused` and writes no report; that is held by `test_run.py` on one workflow. **Recommended:** hold. It is a run-level state, not a cell's class, and putting it in this matrix would make the class assertion conditional on the run's state.

## Deferred debt and arising issues

- **Deferred debt.** None. The matrix adds tests and no production path, so no behaviour moves and no existing verdict changes.
- **Arising.** None raised as a standalone issue. The observations above are held placements: the `None` cells and the STOP reading belong to how the epic's AC4 is read, and the remaining two are test-shape choices inside this row's component.
