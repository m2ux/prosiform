# Prosiform

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

1. Hand planning to a sub-agent: [plan](#dispatch-plan).

## Dispatch plan

[Dispatch](#dispatch) `plan.bundle.md` to a sub-agent.

# Mode

1. Hand review to a sub-agent: [review](#dispatch-review).
2. Then hand planning to one: [plan](#dispatch-plan-1).

## Dispatch review

[Dispatch](#dispatch) `review.bundle.md` to a sub-agent.

## Dispatch plan

[Dispatch](#dispatch) `plan.bundle.md` to a sub-agent.
