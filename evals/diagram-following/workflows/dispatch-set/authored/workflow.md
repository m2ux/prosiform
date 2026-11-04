---
prosiform: {}
---
# Audit

The diagram is the workflow. Each state's section says what to do in that state and what it hands to a sub-agent.

```mermaid
flowchart TD
    Entry(( )) --> Survey
    Survey --> Report
    Report --> Exit((( )))

    click Survey href "states/survey.md"
    click Report href "states/report.md"
```
