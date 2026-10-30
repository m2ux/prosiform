# Change

The diagram is the workflow. Each state's section says what to do in that state and what it hands to a sub-agent.

```mermaid
flowchart TD
    start(( )) --> Prepare
    Prepare --> Deliver
    Deliver --> stop((( )))

    click Prepare href "states/prepare.md"
    click Deliver href "states/deliver.md"
```
