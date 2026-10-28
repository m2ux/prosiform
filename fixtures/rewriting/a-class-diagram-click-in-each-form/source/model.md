# Model

```mermaid
classDiagram
    class Order
    class Line
    class Price
    Order --> Line
    Line --> Price

    click Order href "types/order.md"
    click Line href "types/line.md" "The order line"
    click Price href "types/price.md" "The price" _blank
```
