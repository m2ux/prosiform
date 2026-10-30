# I05:E03:W09 Validation

Each check the work item's test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w09-bare-pf-guide-bootstrap`, cut from `i05/e03/main` at `c285144f4c993c714e2151052b147a913dd0b4b5`.
- **Tested revision.** `0503ae73` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **Contract.** The README pins the design at `9545ef6494056e4dc447d16f2b7b851be1c8ad54` on `engineering`, whose CLI contract states the bare usage line, a Guide clause marking *guide*, arguments naming no entry reference as invalid usage, and whose Clean Markdown rule opens a dispatching bundle on its Prosiform section.

## T1 Bare pf (unit)

| Test | Observes |
| --- | --- |
| `test_cli.py::test_a_bare_command_prints_the_guide` | AC19: `main([])` returns `0`, standard output is the guide, standard error is empty, and the working directory holds nothing afterwards. |
| `test_cli.py::test_the_guide_states_the_compile_step_the_inline_rule_and_the_section` | AC19: the guide carries `pf -o <folder> <destination>`, `SKILL.md`, "A non-zero exit stops the run", the `↳` inline-target rule, and "A bundle that opens with a Prosiform section is followed from there". |
| `test_cli.py::test_the_help_response_names_the_bare_command` | AC19: `pf -h` reads "Run with no arguments, pf prints the guide". |
| `test_cli.py::test_an_argument_naming_no_entry_reference_is_no_bare_command` (3 cases) | `-c`, `-d json` and `-o .` alone exit `2`, write nothing to standard output and name the entry reference. |

## T2 Guide fixture

- AC19: `fixtures/cli/informational-guide-response` declares no argument, exit `0`, no diagnostic, no bundle, and a standard output carrying the compile step, `SKILL.md`, the non-zero-exit rule, `↳` and "Prosiform section is followed from there". It passes, and the conformance report maps it to the `Guide` clause.
- `test_runner.py::test_a_fixture_declaring_no_argument_runs_the_bare_command`: the runner invokes the build with no `-d json` and no fault when the manifest declares no argument and no fault.

## T3 Example skill inspection

AC20, by inspection of `example/work-planner/` at the tested revision:

- `SKILL.md`'s Modes section opens "Run `pf` and follow it, then select the mode as appropriate to fulfill the user request:", and the skill carries no other bootstrap instruction.
- `bootstrap.md` is absent, and `git grep bootstrap.md` finds nothing in the repository.
- `rules.md` carries no Bootstrap rule; its Execution rule and `guidelines.md`'s Parallel dispatch, Other modes, Entry Point and Progressive Disclosure rules describe `⇉` and `⫽` calls running in sub-agents as the bundle's Prosiform section states, with no run-set.
- `make links` (`checks/links.py --online`): every reference in 106 documents resolved.

## T4 Documentation inspection

AC21, by inspection of the three documents at the tested revision:

| Statement | `invocation.md` | `docs/glossary.md` | `README.md` |
| --- | --- | --- | --- |
| Output folder | Output: the run's `.bundles` folder under `-o DIR`, swapped in whole | **publication** | Usage preamble |
| Dispatched bundle set | Dispatched links; Output | **bundle** (n.), **dispatched bundle**, **publication** ("its bundle set") | Usage preamble; Dispatch to Sub-agents |
| Dispatch sub-sections | Dispatched links | **dispatch sub-section** | Dispatch to Sub-agents |
| Parallel sub-sections | Parallel dispatch links | **set**, **parallel dispatch sub-section** | Dispatch to Sub-agents |
| Prosiform section | Bundling rules, Prosiform section; Output | **Prosiform section** | Dispatch to Sub-agents |
| Bare-`pf` guide | Guide; the `pf` usage line | **guide** | Print the Guide |

The review search at the tested revision finds no `bootstrap.md`, `run-set` or `W_RUN_SET_SHAPE` outside the `fixtures/run-set` family's directory name; each remaining `-o -` names its refusal.

## T5 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1281 unit tests, 716 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links, vocabulary (44 contract terms, `guide` among them), invocation, conformance and independence.

## T6 make corpus

`corpus check: 331 fixture(s), 331 pass, 0 fail, 0 awaited, 0 unexpected pass`. The usage-example bundles drop the Bootstrap group and carry the rewritten Rules; nothing else changes.

## T7 make conformance and make invocation

- `make conformance`: 303 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere; `Guide` is covered by 1 fixture.
- `make invocation`: 29 statements of `invocation.md`, each held to the build's help, "a bare command prints the guide" among them.

## Epic base update

`i05/e03/main` moved to `b7935828` (the merge of #362, W10's fixtures) before the merge. It was merged into the task branch at `2ef408bb` without conflict. On that head `make corpus` reported `335 fixture(s), 335 pass, 0 fail`, and `make conformance`, `make invocation`, `make independence` and `make vocabulary` held as above.

## Continuous integration

`Checks` ran `make check` on `0503ae73` and passed ([run](https://github.com/m2ux/prosiform/actions/runs/40683264794/job/122799099282)), and again on the merged head `2ef408bb` and passed ([run](https://github.com/m2ux/prosiform/actions/runs/40684254614/job/122802481812)).
