# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

[the shared rules](#dispatch-the-shared-rules)
and [the draft](#dispatch-the-draft).

## Dispatch the shared rules

Dispatch `shared_rules__every-rule.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

## Dispatch the draft

Dispatch `shared_my rules__run.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.
