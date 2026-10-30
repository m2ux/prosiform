# Prosiform

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Plan

1. Apply: [review](#dispatch-review).

## Dispatch review

[Dispatch](#dispatch) `review.bundle.md` to a sub-agent.
