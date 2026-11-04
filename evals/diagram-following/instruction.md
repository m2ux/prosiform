# Instruction

The task every session of the diagram-following eval is given, in every form but `bootstrap`, whose session takes [its own](instruction-bootstrap.md). A run puts the form's entry document in place of `ENTRY`; nothing else in the text differs between forms.

```text
ENTRY describes a workflow. Interpret it as a workflow and follow it to
completion, starting at its first state.

- On entering a state, before anything else, append the state's name as one
  line to trace.log in this directory. Append only a state: a step the
  workflow takes, never the diagram's start or stop marker, the diamond it
  weighs a decision in, the condition beside one of that decision's
  branches, a section heading, or any other name the entry document carries.
- When a state dispatches a sub-agent, name in the sub-agent's prompt the
  file or the section you hand it, as the entry document names it, and tell
  it to append each state it enters as one line to trace-<section>.log in
  this directory, named for the section it is handed, and never to
  trace.log: the sub-agent follows a workflow of its own, and trace.log
  records your path alone.
- When a sub-agent returns a question, the user's answers are in
  answers.txt in this directory. Give that sub-agent the same section again
  with the answer.
- In each state, do the action its section states, then choose the next
  state as its section says.
- The files under inputs/ are what the workflow's decisions read. Do not
  change them.
- Stop when the workflow is complete.
```
