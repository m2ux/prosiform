---
prosiform: {}
---
# Delegation

The diagram is the workflow. Each state's section says what to do in that state, by its marks what it hands on, and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Allot
    Allot -->|entrusted| Entrust
    Allot -->|cascaded| Cascade
    Entrust --> Tidy
    Cascade --> Tidy
    Tidy --> stop((( )))

    click Allot href "states/allot.md"
    click Entrust href "states/entrust.md"
    click Cascade href "states/cascade.md"
    click Tidy href "states/tidy.md"
```
