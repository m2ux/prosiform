---
prosiform: {}
---
# Delivery

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Scope
    Scope -->|test| Lint
    Scope -->|release| Stage
    Lint --> Unit
    Unit --> Release
    Stage -->|build| Compile
    Stage -->|announce| Announce
    Compile --> Package
    Package --> Sign
    Sign --> Release
    Announce --> Notify
    Notify --> Release
    Release --> Exit((( )))

    click Entry href "states/entry.md"
    click Scope href "states/scope.md"
    click Lint href "states/lint.md"
    click Unit href "states/unit.md"
    click Stage href "states/stage.md"
    click Compile href "states/compile.md"
    click Announce href "states/announce.md"
    click Notify href "states/notify.md"
    click Release href "states/release.md"
    click Exit href "states/exit.md"
```
