---
prosiform:
  default:
    level: judgement
  alpha:
    choice:
      group: component
      states: The requested component is alpha.
    imports:
      - path: shared/settings.md
        preset: alpha-component
  beta:
    choice:
      group: component
      states: The requested component is beta.
    imports:
      - path: shared/settings.md
        preset: beta-component
  small:
    choice:
      group: test
      states: The test is small.
    imports:
      - path: shared/settings.md
        preset: small-test
  large:
    choice:
      group: test
      states: The test is large.
    imports:
      - path: shared/settings.md
        preset: large-test
---
# Check Component

Read the [component](component.md) and apply the [test](test.md), then answer with their names.
