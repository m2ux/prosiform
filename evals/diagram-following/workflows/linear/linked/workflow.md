# Release

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Plan
    Plan --> Build
    Build --> Test
    Test --> Ship
    Ship --> stop((( )))

    click Plan href "states/plan.md"
    click Build href "states/build.md"
    click Test href "states/test.md"
    click Ship href "states/ship.md"
```
