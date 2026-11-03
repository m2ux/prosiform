# Instruction

The task every session of the diagram-following eval is given, in every form but `bootstrap` and `staged`, whose sessions take their own: [bootstrap](instruction-bootstrap.md) and [staged](instruction-staged.md). A run puts the form's entry document in place of `ENTRY`; nothing else in the text differs between forms.

```text
ENTRY describes a workflow. Interpret it as a workflow and follow it to
completion, starting at its first state.

- On entering a state, before anything else, append the state's name as one
  line to trace.log in this directory. Append only a state the workflow's
  diagram draws as a node: a section heading, a dispatched sub-agent's
  section, or any other name the entry document carries is not a state.
- When a state dispatches a sub-agent, tell it to append each state it
  enters as one line to trace-<section>.log in this directory, named for the
  section it is handed, and never to trace.log: the sub-agent follows a
  workflow of its own, and trace.log records your path alone.
- In each state, do the action its section states, then choose the next
  state as its section says.
- The files under inputs/ are what the workflow's decisions read. Do not
  change them.
- Stop when the workflow is complete.
```
