---
prosiform: {}
---
# Choice

The diagram is the workflow. Each state's section says what to do in that state and what it hands to a sub-agent.

```mermaid
flowchart TD
    Entry(( )) --> Enquire
    Enquire --> Confirm
    Confirm --> Exit((( )))

    click Entry href "states/entry.md"
    click Enquire href "states/enquire.md"
    click Confirm href "states/confirm.md"
    click Exit href "states/exit.md"
```
