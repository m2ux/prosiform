# I05:E07:W04 Validation

Each check the work item's Test row names, with the revision it ran on and what it observed.

- **Branch.** `i05/e07/w04-dispatch-operator-carries-the`, cut from `i05/e07/main` at `d4da261c`.
- **Tested revisions.** `21f2ad9e` (the reader and the five steps), then `560f5f6f` (the preambles and the re-dispatch clause).
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`, `src/.venv/bin/pf`.
- **No paid session ran and no baseline was written.** The guards are reader tests and run without an agent.

## T1 AC5 — a compiled step states its dispatch by its marks alone

| Test | Observes |
| --- | --- |
| `test_a_compiled_step_stating_its_dispatch_in_prose_is_a_fault` | AC5: `1. Hand the plan to a sub-agent: [⇉ plan](../plan.md#work).` is refused, the fault naming `sub-agent` and quoting the line. |
| `test_a_compiled_step_repeating_its_protocol_is_a_fault` | AC5: `1. [⫽ source](../review.md#source) and [⫽ tests](../review.md#tests) together.` is refused, the fault naming `together`. |
| `test_a_compiled_step_carrying_an_unmarked_link_is_a_fault` | AC5: `1. [⫽ source](../review.md#source) and [tests](../review.md#tests).` is refused, so a partly marked step dispatches nothing it does not say. |

Each fails against the reader at `d4da261c`, where the steps were matched by prose and no restatement was a fault.

## T2 AC5 — the workflows still bundle and still trace

| Test | Observes |
| --- | --- |
| `test_each_form_bundles_cleanly_carrying_every_state[<workflow>-compiled]` | Each compiled workflow bundles at exit 0 with no diagnostic, the entry's bundle carrying every state, and a bundle per target the marks name. |
| `test_each_scenario_path_is_the_walk_its_inputs_determine` | Each dispatch scenario's trace is the walk its marked steps state, in both forms. |
| `test_a_trace_disagreeing_with_the_source_is_a_fault` | A trace dropping a set's `together` is caught in both forms. |

## T3 AC5 — the whole tree holds the split

`make check` at `560f5f6f` exited 0:

- lock check, lint, format check and type check over `src/prosiform`, `src/tests`, `checks` and `evals`;
- the unit tests in `src`;
- 179 harness tests over `checks/tests` and `evals/diagram-following`, up from 176 on the base: three guards added;
- the corpus of 342 fixtures, the installed-wheel smoke run, and the layout, tables, links, vocabulary, invocation, conformance, independence, steps and authoring checks, each clean.

## T4 The split is visible in what a session reads

Bundling each compiled workflow at `560f5f6f` and reading the entry's bundle:

- `# Prosiform`, `## Dispatch` and, where a set is dispatched, `## Parallel dispatch` open the bundle. Each states what a sub-agent is handed and what a returned question does.
- Each step is its marks: `1. [plan](#dispatch-plan).`, `1. [source](#dispatch-in-parallel) and [tests](#dispatch-in-parallel).`
- Each target's `Dispatch <text>` or `Dispatch in parallel` sub-section names the bundle file and links the protocol.

The authored form's bundle at the same revision is one file whose steps carry the prose and no protocol, which is the control.

## What this unit does not claim

- **No measured pass rate.** This row changes what a session reads, so the committed `baseline.json` was measured against the previous text. Its dispatch cells are stale for both forms until a run replaces them; the measured baseline is I05:E08 W02's, whose one run covers every form.
- **The fixture corpus keeps the old form.** 33 fixture sources still write `Hand the … to a sub-agent: [⇉ plan](plan.md).`, and 16 expected bundles carry it as published output. `pf` compiles a dispatched link and carries the sentence beside it, so the corpus's prose-first convention is not refused by the build. The corpus is therefore not the model for this rule; the eval states it, and reconciling the two is a corpus decision this row does not take.
