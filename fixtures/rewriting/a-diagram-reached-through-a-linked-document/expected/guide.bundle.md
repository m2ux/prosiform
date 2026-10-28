# Ticket Guide

A ticket moves through the states the [lifecycle](#lifecycle) diagram shows.

# Lifecycle

```mermaid
flowchart LR
    start(( )) --> Open([Open])
    Open --> Review([Review])
    Review --> Closed([Closed])
    Review -->|rework| Open
    Closed --> Notes[[Notes]]

    click Open href "#open" "The open state"
    click Review "#review" _blank
    click Closed href "#closed";
    click Notes "#notes"
    click start callback "Start a ticket"
    click Docs href "https://mermaid.js.org/syntax/flowchart.html"
```

## Notes

Each state is a document of its own.

# Open

A ticket waits for an owner.

# Review

A reviewer reads the change.

# Closed

The ticket is done.
