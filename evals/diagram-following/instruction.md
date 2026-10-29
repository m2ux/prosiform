# Instruction

The task every session of the diagram-following eval is given, whatever form of a workflow it receives. A run puts the form's entry document in place of `ENTRY`; nothing else in the text differs between forms.

```text
ENTRY describes a workflow. Interpret it as a workflow and follow it to
completion, starting at its first state.

- On entering a state, before anything else, append the state's name as one
  line to trace.log in this directory.
- In each state, do the action its section states, then choose the next
  state as its section says.
- The files under inputs/ are what the workflow's decisions read. Do not
  change them.
- Stop when the workflow is complete.
```
