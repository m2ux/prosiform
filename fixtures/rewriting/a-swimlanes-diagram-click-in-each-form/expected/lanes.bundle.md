# Lanes

```mermaid
swimlane-beta LR
    subgraph Author [Author]
        Draft
    end
    subgraph Reviewer [Reviewer]
        Review
        Approve
        Merge
    end
    Draft --> Review --> Approve --> Merge

    click Draft href "#draft"
    click Review "#review"
    click Approve "#approve" "The approval"
    click Merge href "#merge" "The merge" _self
```

# Draft

# Review

# Approve

# Merge
