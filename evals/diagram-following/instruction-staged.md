# Instruction: Following a Staged Bundle

The task a session in the `staged` form is given. That form places the bundle
set `pf` compiled from a workflow's sources in the folder `pf` writes it to,
beside the sources and with the build on the session's path, so a line of the
bundle naming further material to compile can be compiled where it stands. A
run puts the entry's bundle in place of `ENTRY`.

```text
ENTRY describes a workflow. Interpret it as a workflow and follow it to
completion, starting at its first state.

- The pf command is on your path, and the documents ENTRY was compiled from
  sit in this directory. Run pf with no arguments for how a bundle names
  material to compile, and run each compile from this directory.
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
