---
prosiform: {}
---
# Relocation

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    Entry(( )) --> Inventory
    Inventory --> Relocate
    Relocate --> Settle
    Settle --> Exit((( )))

    click Inventory href "states/inventory.md"
    click Relocate href "states/relocate.md"
    click Settle href "states/settle.md"
    click Entry href "states/entry.md"
    click Exit href "states/exit.md"
```
