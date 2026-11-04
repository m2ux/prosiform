---
prosiform: {}
---
# Change

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Receive
    Receive -->|docs| Edit
    Receive -->|code| Assess
    Assess -->|low| Patch
    Assess -->|high| Harden
    Edit --> Proof
    Patch --> Verify
    Harden --> Audit
    Proof --> Merge
    Verify --> Merge
    Audit --> Merge
    Merge --> Exit((( )))

    click Entry href "states/entry.md"
    click Receive href "states/receive.md"
    click Assess href "states/assess.md"
    click Edit href "states/edit.md"
    click Patch href "states/patch.md"
    click Harden href "states/harden.md"
    click Merge href "states/merge.md"
    click Exit href "states/exit.md"
```
