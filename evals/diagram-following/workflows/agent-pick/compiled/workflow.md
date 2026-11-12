---
prosiform: {}
---
# Triage

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Classify
    Classify -->|charter| Charter
    Classify -->|breakdown| Breakdown
    Classify -->|change| Change
    Classify -->|hold| Hold
    Charter --> Exit((( )))
    Breakdown --> Exit
    Change --> Exit
    Hold --> Exit

    click Classify href "states/classify.md"
    click Charter href "states/charter.md"
    click Breakdown href "states/breakdown.md"
    click Change href "states/change.md"
    click Hold href "states/hold.md"
    click Entry href "states/entry.md"
    click Exit href "states/exit.md"
```
