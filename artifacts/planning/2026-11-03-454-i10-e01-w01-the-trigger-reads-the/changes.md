# Plan Changes

## Applied

- The epic row W01 links [pull request 607](https://github.com/m2ux/prosiform/pull/607), then ticks Done, and AC1 is ticked.

## Held

None.

## Deviations

- The throwaway evidence pull requests targeted a throwaway base cut from the W01 head rather than `i10/e01/main`. The workflow file's own path matches the path set, so a pull request into `i10/e01/main` would have run the checks whatever else it touched. The base and every head branch are deleted.
