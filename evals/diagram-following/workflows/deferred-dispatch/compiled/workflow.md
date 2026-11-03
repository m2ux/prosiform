---
prosiform: {}
---
# Dispatch Floor

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Pick
    Pick --> Pack
    Pack --> Post
    Post --> stop((( )))

    click Pick href "states/pick.md"
    click Pack href "states/pack.md"
    click Post href "states/post.md"
```
