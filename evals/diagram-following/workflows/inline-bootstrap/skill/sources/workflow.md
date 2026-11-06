---
prosiform: {}
---
# Release

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Freeze
    Freeze -->|feature| Tag
    Freeze -->|fix| Backport
    Tag --> Broadcast
    Backport --> Broadcast
    Broadcast --> Exit((( )))

    click Freeze href "states/freeze.md"
    click Tag href "states/tag.md"
    click Backport href "states/backport.md"
    click Broadcast href "states/broadcast.md"
    click Entry href "states/entry.md"
    click Exit href "states/exit.md"
```
