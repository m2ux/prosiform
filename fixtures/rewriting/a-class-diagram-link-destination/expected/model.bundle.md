Before reading on, run `pf` with no arguments and follow the guide it prints.

# Model

```mermaid
classDiagram
    class Ticket
    class Review
    Ticket --> Review

    link Ticket "#ticket" "The ticket type" _blank
    link Review "#review"
```

# Ticket

# Review
