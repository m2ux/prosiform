---
prosiform: {}
---
# Change

The diagram is the workflow. Each state's section says what to do in that state and, by its marks, what it hands on.

```mermaid
flowchart TD
    Entry(( )) --> Prepare
    Prepare --> Deliver
    Deliver --> Exit((( )))

    click Prepare href "states/prepare.md"
    click Deliver href "states/deliver.md"
```
