---
prosiform:
  default:
    subst:
      - {states/approve.md: alternates/approve.md}
---
# Release

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

The release uses the [Stage](states/stage.md "release") preset selection.

```mermaid
flowchart TD
    Entry(( )) --> Outline
    Outline -->|minor| Approve
    Outline -->|major| Amend
    Amend --> Inspect
    Inspect -->|ship| Stage
    Inspect -->|hold| Approve
    Stage --> Gate
    Gate --> Approve
    Approve --> Exit((( )))

    click Entry href "states/entry.md"
    click Outline href "states/outline.md"
    click Approve href "states/approve.md"
    click Amend href "states/amend.md"
    click Stage href "states/stage.md"
    click Exit href "states/exit.md"
```
