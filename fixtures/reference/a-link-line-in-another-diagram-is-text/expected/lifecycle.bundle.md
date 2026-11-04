# § Instructions

Run `pf`, then follow the guidance it prints.

# Lifecycle

```mermaid
stateDiagram-v2
    [*] --> link
    link --> done : retry @ ops.md
    link Ops "ops.md"
```
