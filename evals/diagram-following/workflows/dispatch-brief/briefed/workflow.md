---
prosiform: {}
---
# Casework

The diagram is the workflow. Each state's section says what to do in that state, by its marks what it hands on, and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Receive
    Receive -->|ledger| Trace
    Receive -->|payroll| Audit
    Trace --> Exit((( )))
    Audit --> Exit

    click Entry href "states/entry.md"
    click Receive href "states/receive.md"
    click Trace href "states/trace.md"
    click Audit href "states/audit.md"
    click Exit href "states/exit.md"
```
