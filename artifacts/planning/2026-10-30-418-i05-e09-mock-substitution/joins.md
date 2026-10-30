# Joins

Pairs of independent rows that do not share a pull request, and why.

- E09:W03 and E09:W05 take separate pull requests: W03 changes the derived name a run publishes, and W05 changes what a withheld reference resolves to. Neither edits a line the other does.
- E09:W04 and E09:W05 take separate pull requests: W04 adds warnings beside the ones the run already emits, and W05 has no diagnostic of its own.
- E09:W04 and E09:W06 take separate pull requests: W06 changes the lookup a mapping performs, and W04 reads what that lookup records. The record W04 consumes is W03's, so the two are independent.
