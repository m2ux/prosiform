---
prosiform:
  default:
    level: judgement
  alpha:
    choice: The requested component is alpha.
    choice-group: component
    imports:
      - path: shared/settings.md
        preset: alpha-component
  beta:
    choice: The requested component is beta.
    choice-group: component
    imports:
      - path: shared/settings.md
        preset: beta-component
  small:
    choice: The test is small.
    choice-group: test
    imports:
      - path: shared/settings.md
        preset: small-test
  large:
    choice: The test is large.
    choice-group: test
    imports:
      - path: shared/settings.md
        preset: large-test
---
# Check Component

Read the [component](component.md) and apply the [test](test.md), then answer with their names.
