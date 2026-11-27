---
prosiform:
  models:
    levels:
      judgement: gpt-6.1-sol
  alpha-component:
    subst:
      - ../component.md: alpha.md
  beta-component:
    subst:
      - ../component.md: beta.md
  small-test:
    subst:
      - ../test.md: small.md
  large-test:
    subst:
      - ../test.md: large.md
---
# Shared Settings

Settings the entry and the worker import. Each key resolves from this folder, so `../component.md` names the component slot beside the worker, and each substitute resolves from its key's folder.
