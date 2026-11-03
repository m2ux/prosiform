Before reading on, run `pf` with no arguments and follow the guide it prints.

# Lifecycle

```mermaid
stateDiagram-v2
    [*] --> link
    link --> done : retry @ ops.md
    link Ops "ops.md"
```
