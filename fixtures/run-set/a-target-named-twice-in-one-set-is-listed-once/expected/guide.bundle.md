# Guide

1. Run [the source review](#dispatch-in-parallel) and [the test review](#dispatch-in-parallel).
2. Where the source changed, run [the source review again](#dispatch-in-parallel).

## Dispatch in parallel

Dispatch these bundles together, each to a sub-agent:

- `review__source.bundle.md` (the source review)
- `review__tests.bundle.md` (the test review)
