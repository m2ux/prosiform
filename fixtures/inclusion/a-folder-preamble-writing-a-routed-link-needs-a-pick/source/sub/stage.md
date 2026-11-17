---
prosiform:
  default:
    group: {stages: 1}
  alpha:
    choice: The work is of kind alpha.
    subst: [{body.md: alpha-body.md}]
  beta:
    choice: The work is of kind beta.
    subst: [{body.md: beta-body.md}]
---
# Stage

Every stage reads the [body](body.md) first.

## Hand-off

The stage takes one folder and answers one line.
