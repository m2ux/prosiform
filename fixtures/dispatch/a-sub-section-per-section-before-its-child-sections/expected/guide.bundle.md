# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

## Prepare

1. [plan](#dispatch-plan).

### Dispatch plan

Dispatch `plan.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

### Detail

What preparing involves.

## Revise

1. [plan](#dispatch-plan-1).
2. Then hand review to one: [review](#dispatch-review).

### Dispatch plan

Dispatch `plan.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

### Dispatch review

Dispatch `review.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.
