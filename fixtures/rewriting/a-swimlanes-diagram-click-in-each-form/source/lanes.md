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

    click Draft href "steps/draft.md"
    click Review "steps/review.md"
    click Approve "steps/approve.md" "The approval"
    click Merge href "steps/merge.md" "The merge" _self
```
