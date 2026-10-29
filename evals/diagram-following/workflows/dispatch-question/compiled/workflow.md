# Choice

The diagram is the workflow. Each state's section says what to do in that state and what it hands to a sub-agent.

```mermaid
flowchart TD
    start(( )) --> Enquire
    Enquire --> Confirm
    Confirm --> stop((( )))

    click Enquire href "states/enquire.md"
    click Confirm href "states/confirm.md"
```
