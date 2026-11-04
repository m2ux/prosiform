---
prosiform: {}
---
# Batch

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Load
    Load --> Measure
    Measure -->|rework| Rework
    Measure -->|accept| Accept
    Rework --> Retest
    Retest --> Measure
    Accept --> Exit((( )))

    click Load href "states/load.md"
    click Measure href "states/measure.md"
    click Rework href "states/rework.md"
    click Accept href "states/accept.md"
```
