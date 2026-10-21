# Change List — I00:E11:W23

> The plan changes this session applied, and the ones it held for the user.

## Applied

- **The epic records the delivery.** W23 links [#153](https://github.com/m2ux/prosiform/pull/153) in the Work Breakdown of [#39](https://github.com/m2ux/prosiform/issues/39), its Done cell carries a tick, and AC24 is ticked. The task issue [#147](https://github.com/m2ux/prosiform/issues/147) carries all three of its own criteria ticked and is closed as completed.

- **A new row carries the debt this row's validation found.** [#158 \[I00:E11:W25\] Link Checking: A Code Block Indented Inside a List Item](https://github.com/m2ux/prosiform/issues/158) states the one case the indented-block rule does not reach: a code block indented inside a list item is written where the rule reads content, so a link form there is resolved. It is non-trivial — telling the two apart means reading each open list item's content column, which is a parser's rule — and it blocks nothing, so it is a row of the deferred-debt epic rather than work inside this one. W25 is placed in #39 against a new **AC26**, and the issue sits in the Backlog of the [Bundling board](https://github.com/users/m2ux/projects/18), where W24 sits.

## Observed while syncing

- **An epic sync given no task issue clears a row that links one.** `sync.py` run over #39 with this row's task issue alone produced a body that dropped W15's Done tick, because W15 links issue [#112](https://github.com/m2ux/prosiform/issues/112) rather than a pull request and an absent `--tasks` entry leaves the row undelivered. The patch that landed was produced with #112 and #150 supplied beside #147, and its diff against the body read immediately before it touches this row alone. A session patching an epic whose rows link task issues needs those issues in hand.

## Held

- Nothing. No change this session found was outside its allowance, and no initiative was created or altered.
