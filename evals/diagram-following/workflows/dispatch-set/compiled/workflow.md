# Audit

The diagram is the workflow. Each state's section says what to do in that state and, by its marks, what it hands on.

```mermaid
flowchart TD
    start(( )) --> Survey
    Survey --> Report
    Report --> stop((( )))

    click Survey href "states/survey.md"
    click Report href "states/report.md"
```
