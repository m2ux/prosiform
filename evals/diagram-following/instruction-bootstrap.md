# Instruction: Compiling a Skill

The task a session in the `bootstrap` form is given. That form places a skill
where the agent CLI discovers skills, and hands over the documents it names
without compiling them: the session finds the skill, compiles what it names,
and follows the bundle that comes out.

```text
A skill is available to you. Find it, do what it says, and follow the
workflow it leads you to to completion, starting at its first state.

- The skill names documents to compile and how. Compile them before reading
  any state's section: the bundle the compile writes is the document that
  states the workflow.
- On entering a state, before anything else, append the state's name as one
  line to trace.log in this directory. Append only a state the workflow's
  diagram draws as a node: a section heading, a dispatched sub-agent's
  section, or any other name the entry document carries is not a state.
- When a state hands you a bundle to follow as a dispatched sub-agent, your
  own states go to trace-<section>.log instead, named for the section you
  were handed: the workflow you were dispatched is a workflow of its own, and
  the session that dispatched you records its own path in trace.log.
- In each state, do the action its section states, then choose the next
  state as its section says.
- The files under inputs/ are what the workflow's decisions read. Do not
  change them.
- Stop when the workflow is complete.
```
