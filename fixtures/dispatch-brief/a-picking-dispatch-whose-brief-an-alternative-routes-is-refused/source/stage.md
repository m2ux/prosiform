---
prosiform:
  default:
    brief: "#given"
  Task:
    choice: One pull request's worth of work.
    subst: [{body.md: task-body.md}]
  Epic:
    choice: Lists its tasks in a Work Breakdown table.
    subst: [{body.md: epic-body.md}]
---
# Stage

## Given

Read [the body](body.md#body) before you dispatch.

## Steps

1. Do the work.
