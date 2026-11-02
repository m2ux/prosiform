Before following this bundle, [run pf first](#run-pf-first).

# Prosiform

## Run pf first

Run `pf` first, with no arguments, and follow the guide it prints.

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Steps

## Procedure

1. Defer [the rules](rules.md) to a later run.
2. Follow [Checks](#dispatch-checks).

### Dispatch Checks

[Dispatch](#dispatch) `checks.bundle.md` to a sub-agent.
