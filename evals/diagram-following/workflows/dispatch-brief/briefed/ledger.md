---
prosiform:
  default:
    brief: "#contract"
---
# Ledger

## Contract

What the ledger check takes, what it leaves and what it answers. Before you dispatch it, read its [Given](#given), [Leaves](#leaves) and [Answers](#answers) and act on each.

### Given

The ledger's figure, which the dispatching agent hands over before the check starts:

Write `actions/given.txt` containing `ledger-7`.

### Leaves

`actions/finding.txt`, on every answer.

### Answers

- `done`  The finding is written.

## Steps

Write `actions/finding.txt` containing what `actions/given.txt` holds, or `absent` where there is no such file. Adhere to the [Rules](#rules).

## Rules

The check reads no file the dispatching agent writes but `actions/given.txt`.
