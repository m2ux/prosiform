---
prosiform: {}
---
# Handbook

The team's procedures, one section each.

## Onboarding

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Enrol
    Enrol --> Equip
    Equip --> Greet
    Greet --> stop((( )))

    click Enrol href "states/enrol.md"
    click Equip href "states/equip.md"
    click Greet href "states/greet.md"
```

## Upkeep

The [maintainers' notes](upkeep/notes.md) say who keeps this handbook current.
