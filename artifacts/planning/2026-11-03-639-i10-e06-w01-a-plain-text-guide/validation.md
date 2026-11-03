# Validation

The checks W01's work item names, run against task branch `i10/e06/w01-a-plain-text-guide` at `48233105`, on the design pinned at engineering commit `884681c0cc4caaa9a1740a24fab204fea9a39d1a`.

## T1 Guide Fixture

`fixtures/cli/informational-guide-response` runs bare `pf` and expects exit 0 with the guide's rules in standard output: the run line, `↳` inline, `⇉` hand-on, the `In parallel` section and its inputs, waiting for all, failures returned together, and the first line reading `Question:`. `src/tests/test_cli.py` adds `test_the_guide_states_each_rule_an_agent_follows_a_bundle_by`. Result: held. Observes AC2 and AC4.

## T2 Plain-Text Test

`test_the_guide_is_plain_text` in `src/tests/test_cli.py` refuses a guide carrying a Markdown heading, emphasis, link, code span or code fence. Result: held. Observes AC3.

## T3 Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`, after `git fetch origin engineering`. Result: exit 0. Conformance: 360 clauses, 0 declarations naming no clause, 0 unfixturable codes; corpus: 504 fixtures.
