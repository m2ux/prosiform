# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

Run [the shared
rules](#dispatch-the-shared-rules), then [the plan\
steps](#dispatch-the-plan-steps), then [the review ](#dispatch-the-review).

## Dispatch the shared rules

[Dispatch](#dispatch) `rules.bundle.md` to a sub-agent.

## Dispatch the plan steps

[Dispatch](#dispatch) `plan.bundle.md` to a sub-agent.

## Dispatch the review

[Dispatch](#dispatch) `review.bundle.md` to a sub-agent.
