---
prosiform: {}
---
# Change

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Lodge
    Lodge -->|config| Configure
    Lodge -->|code| Assess
    Assess -->|large| Migrate
    Assess -->|small| Amend
    Configure --> Close
    Migrate --> Close
    Amend --> Close
    Close --> Exit((( )))

    click Entry href "states/entry.md"
    click Lodge href "states/lodge.md"
    click Configure href "states/configure.md"
    click Assess href "states/assess.md"
    click Migrate href "states/migrate.md"
    click Amend href "states/amend.md"
    click Close href "states/close.md"
    click Exit href "states/exit.md"
```
