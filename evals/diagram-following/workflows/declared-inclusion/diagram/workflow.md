---
prosiform: {}
---
# Delivery

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Receive
    Receive -->|internal| Inspect
    Receive -->|vendor| Liaise
    Inspect --> Verify
    Verify --> Archive
    Liaise --> Archive
    Archive --> Exit((( )))

    click Entry href "states/entry.md"
    click Receive href "states/receive.md"
    click Inspect href "states/inspect.md"
    click Liaise href "states/liaise.md"
    click Archive href "states/archive.md"
    click Exit href "states/exit.md"
```
