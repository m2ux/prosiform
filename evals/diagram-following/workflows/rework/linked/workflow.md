---
prosiform: {}
---
# Batch

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it, and a decision names the document stating which of its edges applies.

```mermaid
flowchart TD
    start(( )) --> Load
    Load --> Measure
    Measure --> Rework
    Measure --> Accept
    Rework --> Retest
    Retest --> Measure
    Accept --> stop((( )))

    click Load href "states/load.md"
    click Measure href "states/measure.md"
    click Rework href "states/rework.md"
    click Accept href "states/accept.md"
```
