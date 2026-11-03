---
prosiform: {}
---
# Release

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Freeze
    Freeze -->|feature| Tag
    Freeze -->|fix| Backport
    Tag --> Broadcast
    Backport --> Broadcast
    Broadcast --> stop((( )))

    click Freeze href "states/freeze.md"
    click Tag href "states/tag.md"
    click Backport href "states/backport.md"
    click Broadcast href "states/broadcast.md"
```
