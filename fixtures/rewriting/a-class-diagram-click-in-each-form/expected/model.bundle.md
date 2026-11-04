# § Instructions

Run `pf`, then follow the guidance it prints.

# Model

```mermaid
classDiagram
    class Order
    class Line
    class Price
    Order --> Line
    Line --> Price

    click Order href "#order"
    click Line href "#line" "The order line"
    click Price href "#price" "The price" _blank
```

# Order

# Line

# Price
