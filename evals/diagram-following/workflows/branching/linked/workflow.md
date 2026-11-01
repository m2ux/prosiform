---
prosiform: {}
---
# Incident

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it, and a decision names the document stating which of its edges applies.

```mermaid
flowchart TD
    start(( )) --> Intake
    Intake --> Triage
    Triage --> Escalate
    Triage --> Queue
    Escalate --> Notify
    Notify --> Resolve
    Queue --> Resolve
    Resolve --> stop((( )))

    click Intake href "states/intake.md"
    click Triage href "states/triage.md"
    click Escalate href "states/escalate.md"
    click Notify href "states/notify.md"
    click Queue href "states/queue.md"
    click Resolve href "states/resolve.md"
```
