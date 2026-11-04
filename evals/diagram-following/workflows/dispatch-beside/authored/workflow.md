---
prosiform: {}
---
# Change

The diagram is the workflow. Each state's section says what to do in that state and what it hands to a sub-agent.

```mermaid
flowchart TD
    Entry(( )) --> Prepare
    Prepare --> Deliver
    Deliver --> Exit((( )))

    click Entry href "states/entry.md"
    click Prepare href "states/prepare.md"
    click Deliver href "states/deliver.md"
    click Exit href "states/exit.md"
```
