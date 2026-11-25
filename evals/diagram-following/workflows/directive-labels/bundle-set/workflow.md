---
prosiform: {}
---
# Release notes

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Compose
    Compose -->|review| Vet
    Compose -->|direct| Issue
    Vet --> Issue
    Issue --> Exit((( )))

    click Compose href "states/compose.md"
    click Issue href "states/issue.md"
    click Entry href "states/entry.md"
    click Exit href "states/exit.md"
```
