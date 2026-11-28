# § Instructions

Run `pf`, then follow the guidance it prints. Follow [Guide](#guide) next.

# Guide

## Flow

```mermaid
flowchart LR
    Read["Read Phase"]; click Read href "#read-phase"
    Inspect@{ shape: rect, label: "Inspect Phase" }
    Later([Later Phase])
    Literal[↳Literal]
    Worker[⇉ Worker]
    Read --> Inspect --> Later --> Worker
    click Inspect href "#read-phase-1"
    click Later href "#later-phase"
    click Literal href "#graph-1"
    click Worker href "worker.bundle.md"
```

### Graph

#### Read Phase

Read the supplied record.

#### Read Phase

Read the supplied record.

#### Later Phase

[↳ Graph](../../source/later.md#graph)

# Read Phase

### Graph

Read the supplied record.
