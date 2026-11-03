Before reading on, run `pf` with no arguments and follow the guide it prints.

# Guide

```mermaid
flowchart LR
    A --> B
    click B "#plan" "<a href='plan.md'>the plan</a>"
```

```mermaid
pie title Share
    "<a href='plan.md'>Plan</a>" : 40
    "Other" : 60
```

```mermaid
sequenceDiagram
    Alice->>Bob: hello
    Note over Alice,Bob: <a href="plan.md">the plan</a>
```

# Plan
