# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

1. Hand the fields to a sub-agent: [the fields](#dispatch-the-fields).

## Dispatch the fields

Dispatch `plan__fields.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.
