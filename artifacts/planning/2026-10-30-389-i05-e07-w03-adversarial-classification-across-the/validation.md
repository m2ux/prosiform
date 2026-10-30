# I05:E07:W03 Validation

Each check the work item's Test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e07/w03-adversarial-classification-across-the`, cut from `i05/e07/main` at `8905b2e3`.
- **Tested revision.** `1c2c67dc` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`, `src/.venv/bin/pf`.
- **No paid session ran.** Every session below starts [`stub_agent.py`](https://github.com/m2ux/prosiform/blob/1c2c67dc/evals/diagram-following/stub_agent.py) in place of the agent.
- **No baseline written.** `baseline.json`, `report.md` and `EVAL_BUDGET_USD` are untouched.

## T1 AC4 — each departure over the whole dispatch corpus

Each departing script runs the four dispatch scenarios in both forms once, so one run walks eight cells. A scenario's trace states whether the script's departure changes anything about it: where it does, the cell must read that class and no other; where it does not, the cell must pass. The table is therefore the corpus's own statement of which check each departure fails, and a class firing where its departure is absent fails the same assertion as one that does not fire where it is present.

| Test | Observes |
| --- | --- |
| `test_run.py::test_a_departure_is_classified_across_every_dispatch_scenario[STUB_AGENT_NO_DISPATCH]` | AC4: an agent that starts no sub-agent reads `undispatched` in all eight cells — `chain`, `parallel-set`, `set-beside-a-dispatch` and `returned-question`, each in `compiled` and `authored`. |
| `test_run.py::test_a_departure_is_classified_across_every_dispatch_scenario[STUB_AGENT_SEQUENTIAL]` | AC4: a set started one after another reads `sequential_set` in the four cells whose scenario states a set — `parallel-set` and `set-beside-a-dispatch` in both forms — and passes the four whose scenario states no set, so the class is not raised by a chain or a single start. |
| `test_run.py::test_a_departure_is_classified_across_every_dispatch_scenario[STUB_AGENT_ANSWER]` | AC4: a sub-agent's question answered in its place reads `unrelayed_question` in the two `returned-question` cells and passes the six whose scenario states no question, so the class is not raised where nothing returned one. |
| `test_run.py::test_a_departure_is_classified_across_every_dispatch_scenario[STUB_AGENT_STOP]` | AC4: a walk stopped after one state reads `unfinished` in all eight cells, holding the completion check ahead of every dispatch check across the corpus. |

## T2 AC4 — a clean run passes every cell

With no script set, the stub walks each scenario's diagram and dispatches what the scenario states, so the matrix is not a list of ways to fail a scorer that would pass anything.

| Test | Observes |
| --- | --- |
| `test_run.py::test_a_clean_run_passes_every_dispatch_cell` | AC4: all eight cells pass with no failure class, and each cell's trace is its scenario's expected path. |

## T3 AC4 — the matrix is the corpus's

A run over the four dispatch scenarios in both forms writes eight session records and no more, so a scenario silently absent from a departure's run cannot read as a cell that passed.

| Test | Observes |
| --- | --- |
| `test_run.py::test_the_departure_table_names_every_dispatch_scenario` | Each script's predicted-class table names every scenario in `DISPATCH_SCENARIOS`, so a scenario added to the corpus without a prediction fails here rather than going unobserved. |
| The cell-set assertion in each matrix test | The run's records are exactly the four scenarios by two forms; a missing or duplicated session fails before any class is read. |

## T4 The matrix discriminates

The matrix's value is that it fails when a check fires for the wrong reason, not only when it fails to fire. Held by breaking the scorer on purpose: `dispatched()` in `score.py` made to return `None` unconditionally, so no dispatch check can ever fire.

- `test_a_departure_is_classified_across_every_dispatch_scenario` failed for `STUB_AGENT_NO_DISPATCH`, `STUB_AGENT_SEQUENTIAL` and `STUB_AGENT_ANSWER`, each naming its cell and its missing class — for example `STUB_AGENT_ANSWER over returned-question/authored` reading `passed: True, failure: None`.
- `STUB_AGENT_STOP` still passed, since `unfinished` is raised by the completion check before `dispatched()` is reached. That is the intended reading, not a gap.
- `score.py` was restored, and the file is unchanged on the branch.

## T5 make check

`PROSIFORM_BUILD=/home/mike1/projects/dev/md-composer/.worktrees/i05/e07/w03-adversarial-classification-across-the/src/.venv/bin/pf make check` exited 0:

- lock check, lint, format check and type check over `src/prosiform`, `src/tests`, `checks` and `evals`;
- the unit tests in `src`;
- 947 harness tests over `checks/tests` and `evals/diagram-following`, up from 941 on the base: this branch adds six — four matrix tests, the clean run and the table check;
- the corpus, the installed-wheel smoke run, layout, tables, links, vocabulary, invocation, conformance, independence, steps and authoring checks, each clean.

`make harness` alone: 947 passed in 30.56 s. `ruff check`, `ruff format --check` and `mypy` over `evals`: all clean.

## What this unit does not claim

- **No measured pass rate.** The stub agent walks the workflow's own diagram, so its results are correct by construction. This record reports which class each cell reads, not how an agent behaves.
- **No baseline.** `baseline.json` and `report.md` are not written or refreshed here; the measured baseline is I05:E08 W02's, whose one run covers every form. `EVAL_BUDGET_USD` still reads USD 100.
- **AC3's checks are W02's.** This row exercises them across the corpus; it does not restate them.
