# Validation

The checks the task pull request's Test Plan records, run against task branch `i15/e01/w03-the-guide-states-the` at `8eafb1e4b` (guide at `84008a989`, router fixtures at `8eafb1e4b`), from the unit checkout with the locked development environment (`uv sync --frozen`).

## T1 Guide Unit Tests

- **Procedure.** `cd src && .venv/bin/pytest tests/test_cli.py -k "bare_command_prints_the_guide or guide_states_each_rule or guide_is_plain_text or names_the_bare_command"`
- **Observation.** 4 passed. Bare `pf` prints `GUIDE` and writes nothing; the symbol grammar states `? among a link's title tags leaves the pick to you`, to pass the title as `--presets` as usual, read the alternatives `pf` lists, and rerun with `?` replaced by the one that fits; the guide stays plain text, and every earlier rule reads as before.

## T2 Guide Response Fixture

- **Procedure.** `make corpus` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** `cli/informational-guide-response` passes: a bare invocation exits 0 and prints the `?` entry's lines beside the `↳`, `⇉` and `⫽` entries.

## T3 Router Fixtures

- **Procedure.** The T2 corpus run.
- **Observation.** The five fixtures pass, one per step of a pick through the kind router `work-kind.md`:
  - `deferral/a-mode-publishes-its-kind-router-link-with-the-pick-token` — `modes/plan.md` exits 0, its bundle publishing `[Populate the body](work-kind.md#populate-body "?")`, rebased to the working directory, with no diagnostic.
  - `deferral/the-pick-token-command-lists-the-kind-routers-alternatives` — `work-kind.md#populate-body --presets ?` exits 2 with `E_ALTERNATIVE_UNRESOLVED`, listing `initiative`, `epic` and `task` beside their choice lines.
  - `deferral/the-initiative-pick-compiles-the-kind-router`, `deferral/the-epic-pick-compiles-the-kind-router` and `deferral/the-task-pick-compiles-the-kind-router` — each pick exits 0 with no diagnostic, writing the bundle its preset qualifier names, with `the body` routed to that kind's body.

## T4 Repository Checks

- **Procedure.** `make check` with the T2 `PROSIFORM_BUILD`.
- **Observation.** Exit 0. Lint, format, type and lock checks clean; `make test` 2039 passed; `make harness` 1022 passed; corpus 583 fixtures, 583 pass, 0 fail; smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass, the conformance report naming 0 declarations that name no clause.
