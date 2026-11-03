---
prosiform: {}
---
# Order

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it.

```mermaid
flowchart TD
    start(( )) --> Submit
    Submit --> Screen
    Screen -->|flagged| Hold
    Screen -->|clear| Price
    Hold --> Price
    Price -->|discount| Discount
    Price -->|list| Invoice
    Discount --> Invoice
    Invoice --> stop((( )))
    Refund --> stop((( )))

    click Submit href "states/submit.md"
    click Screen href "states/screen.md"
    click Hold href "states/hold.md"
    click Price href "states/price.md"
    click Discount href "states/discount.md"
    click Invoice href "states/invoice.md"
    click Refund href "states/refund.md"
```
