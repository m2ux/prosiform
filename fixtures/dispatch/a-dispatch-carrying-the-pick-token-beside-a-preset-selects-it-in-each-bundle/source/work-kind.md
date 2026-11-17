---
prosiform:
  epic:
    choice: Lists its tasks in a Work Breakdown table.
    subst: [{body.md: epic-body.md}]
  task:
    choice: One pull request's worth of work.
    subst: [{body.md: task-body.md}]
  checks:
    subst: [{review.md: checked-review.md}]
---
# Work Kind

## Populate

Fill each field [the body](body.md) lists, then [review](review.md) it.
