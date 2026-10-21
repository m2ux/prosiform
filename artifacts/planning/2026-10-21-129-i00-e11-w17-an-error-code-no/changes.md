# Changes

The plan changes this session applied, and those it held.

## Applied

- **Delivery recording** — [#39](https://github.com/m2ux/prosiform/issues/39) W17: the row links [#159](https://github.com/m2ux/prosiform/pull/159) and carries its Done tick, and AC18 is ticked. [#129](https://github.com/m2ux/prosiform/issues/129) carries its own tick and is closed as completed, with its board item moved to Done.
- **Task creation** — [#150](https://github.com/m2ux/prosiform/issues/150) raised for the corpus instrument two of the three runs need, placed as the epic's W24 against a new criterion AC25, under the allowance this session was dispatched with. Two fixtures await it by name.

## Held

None.

## Concurrency

Eight sessions delivered rows of this epic in the same window, and the epic body was read and rewritten by each of them. Every write this session made was a fresh read, an edit of its own lines and a write back, verified line by line against the body it had just read. Two writes were redone: the first because W16's delivery landed between the read and the write, the second because W27 and AC28 were added between them. `sync.py` was given every task issue the epic's rows name — 112, 127, 129, 133, 134, 135, 144, 145, 147, 150, 158 and 160 — because a row whose Done depends on a task issue the script was not given reads as undelivered and loses its tick.

The row this session claimed was W24 at the moment it was written. W25, W26 and W27 were claimed by other sessions afterwards, so the numbering holds and [#150](https://github.com/m2ux/prosiform/issues/150) carries the W24 prefix.
