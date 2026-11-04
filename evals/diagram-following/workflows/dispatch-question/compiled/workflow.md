---
prosiform: {}
---
# Choice

The diagram is the workflow. Each state's section says what to do in that state and, by its marks, what it hands on.

```mermaid
flowchart TD
    Entry(( )) --> Enquire
    Enquire --> Confirm
    Confirm --> Exit((( )))

    click Enquire href "states/enquire.md"
    click Confirm href "states/confirm.md"
```
