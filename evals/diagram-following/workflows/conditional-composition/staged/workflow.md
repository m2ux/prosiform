---
prosiform: {}
---
# Upgrade

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Sample
    Sample --> Gauge
    Gauge -->|large| Convert
    Gauge -->|small| Finish
    Convert --> Finish
    Finish --> stop((( )))

    click Sample href "states/sample.md"
    click Gauge href "states/gauge.md"
    click Finish href "states/finish.md"
```
