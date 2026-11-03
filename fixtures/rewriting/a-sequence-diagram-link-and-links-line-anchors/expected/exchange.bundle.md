Before reading on, run `pf` with no arguments and follow the guide it prints.

# Exchange

```mermaid
sequenceDiagram
    participant Client
    participant Server
    link Client: Client guide @ #35;client
    links Server: {"Server guide": "#35;server", "Operations": "#35;operations"}
    Client->>Server: Request
    Server-->>Client: Response
```

# Client

# Server

# Operations
