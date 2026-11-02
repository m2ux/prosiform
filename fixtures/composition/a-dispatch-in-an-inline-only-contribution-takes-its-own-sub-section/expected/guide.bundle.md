# Prosiform

## Dispatch

Hand the named bundle to one sub-agent with the invoking step's inputs, to follow from its start, and continue with its result. A dispatched run asks nothing: it returns each question, with its context and options, unanswered. The dispatching session puts that question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Guide

## Prepare

Read the path [→](#read), and [log the step](#dispatch-log-the-step).

### Inputs

#### Read

The path to read, then [report the path](#dispatch-report-the-path).

##### Dispatch report the path

[Dispatch](#dispatch) `report.bundle.md` to a sub-agent.

### Dispatch log the step

[Dispatch](#dispatch) `log.bundle.md` to a sub-agent.

## Run

Run the step.
