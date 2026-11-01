# Review

## Rule

A finding is a defect the source shows and a test does not cover.

## Source

Read the source, and record what it does.

## Tests

Read the tests, and record what they cover.

## Notes

Background for a later run.

## Appraise

```mermaid
flowchart TD
    start(( )) --> Read
    Read --> known{"is the finding known?"}
    known --> prior[already recorded]
    known --> fresh[new]
    prior --> Rank
    fresh --> Rank
    Rank --> weigh{"does it block?"}
    weigh --> fatal[fatal]
    weigh --> minor[minor]
    fatal --> Conclude
    minor --> Conclude
    Conclude --> stop((( )))

    click Read href "appraise/read.md"
    click known href "appraise/known.md"
    click prior href "appraise/prior.md"
    click fresh href "appraise/fresh.md"
    click Rank href "appraise/rank.md"
    click weigh href "appraise/weigh.md"
    click fatal href "appraise/fatal.md"
    click minor href "appraise/minor.md"
    click Conclude href "appraise/conclude.md"
```

## Repair

Rewrite the defective line, and return what changed.
