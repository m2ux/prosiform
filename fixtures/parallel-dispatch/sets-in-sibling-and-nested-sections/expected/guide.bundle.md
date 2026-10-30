# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

## Parallel dispatch

Dispatch every listed bundle at once, each to a sub-agent of its own per [dispatch](#dispatch); an item the invoking step applies "for each" of several values is dispatched once per value, together. Continue when every item has returned. A failed item cancels nothing: the set returns every failure together as blockers. Questions items return are put to the user together once every item has returned, and only the items that asked are dispatched again.

# Guide

## Review

1. Review the change: [Review the source](#dispatch-in-parallel) and [Review the tests](#dispatch-in-parallel).

### Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):

- `review__source.bundle.md` (Review the source)
- `review__tests.bundle.md` (Review the tests)

### Recheck

1. Recheck the change: [Recheck the source](#dispatch-in-parallel-1) and [Check the docs](#dispatch-in-parallel-1).

#### Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):

- `review__source.bundle.md` (Recheck the source)
- `review__docs.bundle.md` (Check the docs)

## Release

1. Prepare the release: [Write the notes](#dispatch-in-parallel-2) and [Tag the version](#dispatch-in-parallel-2).

### Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, per [parallel dispatch](#parallel-dispatch):

- `notes.bundle.md` (Write the notes)
- `tag.bundle.md` (Tag the version)
