# Prosiform

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

The procedure dispatches [the shared rules](#dispatch-the-shared-rules) to a sub-agent.

## Dispatch the shared rules

[Dispatch](#dispatch) `rules.bundle.md` to a sub-agent.
