---
prosiform: {}
---
# Retrieval

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Solicit
    Solicit --> Mirror
    Mirror -->|live| Serve
    Mirror -->|stored| Restore
    Serve --> stop((( )))
    Restore --> stop

    click Solicit href "states/solicit.md"
    click Mirror href "states/mirror.md"
    click Serve href "states/serve.md"
    click Restore href "states/restore.md"
```
