---
prosiform:
  models:
    levels:
      judgement: gpt-6.1-sol
  strict:
    subst:
      - rules.md: strict-rules.md
  lenient:
    subst:
      - rules.md: lenient-rules.md
  routed:
    group:
      stages: 1
    subst:
      - rules.md: strict-rules.md
---
# Shared Settings

Settings the refusal specimens import. `routed` states a layout group, so it is no pure target.
