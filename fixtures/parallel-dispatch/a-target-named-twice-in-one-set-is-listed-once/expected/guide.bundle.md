# Prosiform

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

## Parallel dispatch

Dispatch every listed bundle at once, each to a sub-agent of its own per [dispatch](#dispatch); an item the invoking step applies "for each" of several values is dispatched once per value, together. Continue when every item has returned; a failed item cancels nothing, and every failure returns together as blockers. Questions return together once all items have, and only the items that asked are dispatched again.

# Guide

1. Run [the source review](#dispatch-in-parallel) and [the test review](#dispatch-in-parallel).
2. Where the source changed, run [the source review again](#dispatch-in-parallel).

## Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):

- `review__source.bundle.md` (the source review)
- `review__tests.bundle.md` (the test review)
