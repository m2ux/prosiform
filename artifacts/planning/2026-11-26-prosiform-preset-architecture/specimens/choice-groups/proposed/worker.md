---
prosiform:
  default:
    level: judgement
  alpha:
    choice:
      group: component
      states: The requested component is alpha.
    subst:
      - component.md: alpha.md
  beta:
    choice:
      group: component
      states: The requested component is beta.
    subst:
      - component.md: beta.md
  small:
    choice:
      group: test
      states: The test is small.
    subst:
      - test.md: small.md
  large:
    choice:
      group: test
      states: The test is large.
    subst:
      - test.md: large.md
---
# Check Component

Read the [component](component.md) and apply the [test](test.md), then answer with their names.
