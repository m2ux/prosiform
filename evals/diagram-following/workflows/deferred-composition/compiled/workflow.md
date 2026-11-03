---
prosiform: {}
---
# Relocation

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Inventory
    Inventory --> Relocate
    Relocate --> Settle
    Settle --> stop((( )))

    click Inventory href "states/inventory.md"
    click Relocate href "states/relocate.md"
    click Settle href "states/settle.md"
```
