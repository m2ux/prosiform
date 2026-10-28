# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

## Parallel dispatch

Dispatch every listed bundle at once, each to a sub-agent of its own as [Dispatch](#dispatch) states; an item the invoking step applies "for each" of several values is dispatched once per value, together. Continue when every item has returned. A failed item cancels nothing: the set returns every failure together as blockers. Questions items return are put to the user together once every item has returned, and only the items that asked are dispatched again.

# Guide

1. Run [the reviews](#dispatch-in-parallel), then report.

## Dispatch in parallel

Dispatch these bundles together, each to a sub-agent, as [Parallel dispatch](#parallel-dispatch) states:

- `plan__reviews.bundle.md` (the reviews)
