# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

1. Hand the run to a sub-agent: [Run](#dispatch-run).

## Dispatch Run

[Dispatch](#dispatch) `guide__run.bundle.md` to a sub-agent.

## Run

1. Hand planning to a sub-agent: [plan](#dispatch-plan).

### Dispatch plan

[Dispatch](#dispatch) `plan.bundle.md` to a sub-agent.
