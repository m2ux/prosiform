---
prosiform: {}
---
# Chain

The diagram is the workflow. Each state's section says what to do in that state and what it hands to a sub-agent.

```mermaid
flowchart TD
    Entry(( )) --> Request
    Request --> Handover
    Handover --> Exit((( )))

    click Entry href "states/entry.md"
    click Request href "states/request.md"
    click Handover href "states/handover.md"
    click Exit href "states/exit.md"
```
