---
prosiform: {}
---
# Order

The diagram is the workflow. Each state's section says what to do in that state and which transition to take out of it, and a decision names the document stating which of its edges applies.

```mermaid
flowchart TD
    Entry(( )) --> Submit
    Submit --> Screen
    Screen --> Hold
    Screen --> Price
    Hold --> Price
    Price --> Discount
    Price --> Invoice
    Discount --> Invoice
    Invoice --> Exit((( )))
    Refund --> Exit((( )))

    click Entry href "states/entry.md"
    click Submit href "states/submit.md"
    click Screen href "states/screen.md"
    click Hold href "states/hold.md"
    click Price href "states/price.md"
    click Discount href "states/discount.md"
    click Invoice href "states/invoice.md"
    click Refund href "states/refund.md"
    click Exit href "states/exit.md"
```
