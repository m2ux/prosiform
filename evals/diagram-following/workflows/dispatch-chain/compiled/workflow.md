# Chain

The diagram is the workflow. Each state's section says what to do in that state and, by its marks, what it hands on.

```mermaid
flowchart TD
    start(( )) --> Request
    Request --> Handover
    Handover --> stop((( )))

    click Request href "states/request.md"
    click Handover href "states/handover.md"
```
