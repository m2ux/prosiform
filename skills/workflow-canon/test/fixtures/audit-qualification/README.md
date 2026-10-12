# Controlled Audit Qualification

The two cases use four **controlled test criteria**, not the project's complete Workflow Canon. They exercise coverage, independent mapping verification, and evidence gates with a small corpus containing a workflow, activity, routine, leaf technique, and inherited technique contract. Their compact YAML is a qualification dialect: the criterion text defines its bindings and graph semantics. It is not an engine guard-conformance specimen.

Each case is a corpus root for the audit CLI and has its own `scope.json`. The scoped edits name the workflow, activity and leaf technique. The routine and inherited contract remain byte-identical between cases. Reference closure must still include them. An explicit execution relationship carries the workflow, activity call site and inherited contract into the routine instance's context.

The clean control satisfies every test criterion. The seeded case contains six distinct defects: a standalone emission instruction, the later clause of a compound rule, a workflow-wide termination failure, an unchanged consumer's output binding, one routine invocation's arguments, and an inherited destination rule.

`expected-outcomes.json` fixes the expected outcomes before evaluator access. Keep it and these notes outside evaluator and mapping packets. Agents receive captured sources, controlled criteria, scope metadata, and their assignments. Compare returned findings with the manifest only after reconciliation. Several applicable rows may expose the same defect; count its source cause once. A single report row that mentions two distinct causes must still identify both expected findings.

Run the complete row-by-criterion product through mapping, independent verification and evaluation for each case. Repeat with fresh Author and Audit agent contexts. No fixture verdict establishes full-project-canon conformance. Real corpus specimens use the separate full-canon run.

The fixture's guard is `check.py`: it checks parsing, required dialect structure and the complete four-criterion inventory. Capture its actual command, exit status and output for the guard obligation. This is a measured controlled-dialect check, not an engine schema or full-project guard claim. Qualification reconciliation separately checks expected locations and byte equality of unchanged sources.
