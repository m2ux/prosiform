---
prosiform: {}
---
# Upgrade

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Sample
    Sample --> Gauge
    Gauge -->|large| Convert
    Gauge -->|small| Finish
    Convert --> Finish
    Finish --> Exit((( )))

    click Sample href "states/sample.md"
    click Gauge href "states/gauge.md"
    click Finish href "states/finish.md"
    click Entry href "states/entry.md"
    click Exit href "states/exit.md"
```
