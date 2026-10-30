# Prosiform

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

## Parallel dispatch

Dispatch every listed bundle at once, each to a sub-agent of its own per [dispatch](#dispatch); an item the invoking step applies "for each" of several values is dispatched once per value, together. Continue when every item has returned; a failed item cancels nothing, and every failure returns together as blockers. Questions return together once all items have, and only the items that asked are dispatched again.

# Guide

## Review

1. Apply: [Review the source](#dispatch-in-parallel) and [Review the tests](#dispatch-in-parallel).

### Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):

- `review__source.bundle.md` (Review the source)
- `review__tests.bundle.md` (Review the tests)

### Recheck

1. Apply: [Recheck the source](#dispatch-in-parallel-1) and [Check the docs](#dispatch-in-parallel-1).

#### Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):

- `review__source.bundle.md` (Recheck the source)
- `review__docs.bundle.md` (Check the docs)

## Release

1. Apply: [Write the notes](#dispatch-in-parallel-2) and [Tag the version](#dispatch-in-parallel-2).

### Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):

- `notes.bundle.md` (Write the notes)
- `tag.bundle.md` (Tag the version)
