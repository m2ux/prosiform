# Prosiform

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

1. Hand planning to a sub-agent: [the steps](#dispatch-the-steps).

## Dispatch the steps

[Dispatch](#dispatch) `plan__steps.bundle.md` to a sub-agent.
