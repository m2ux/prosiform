# Joins

Pairs of independent rows that do not share a pull request, and why.

- E06:W02 and E06:W03 take separate pull requests: a repository check and a corpus change are distinct reviews.
- E06:W02 and E06:W04 take separate pull requests: as above.
- E06:W03 and E06:W04 take separate pull requests: each moves a different set of restatements to its own home, and each is reviewed against its own list.
- E06:W06 and E06:W07 take separate pull requests: both rewrite most artifacts, and contracts and commands are each a review of their own size.
- E06:W06 and E06:W08 take separate pull requests: one area each, reviewed apart; each regenerates the usage-example bundles after the one before it merges.
- E06:W07 and E06:W08 take separate pull requests: as above.
- E06:W03 and E06:W11 take separate pull requests: one replaces bindings across the example, the other brings the shared guidelines to the authoring rules; both regenerate the usage-example bundles, so W11 starts after W03 merges.
- E06:W04 and E06:W11 take separate pull requests: as above, and each regenerates the bundles after the one before it merges.
