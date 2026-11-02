# Joins

Each candidate unit below is the undelivered rows of one epic declaring one component, and ships as separate pull requests for the reason given.

- E04:W07 E04:W08 E04:W09 — each extends `main:src/prosiform/cli.py` for a separate concern; W07 waits on the composition chain through W06, while W08 and W09 start once W02 lands, so joining them would hold both behind that chain.
