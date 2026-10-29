# Joins — I05:E05

> Pair record · Created 2026-10-29

Every pair of rows in this epic where neither depends on the other, and why it shares no pull request.

- E05:W01 and E05:W02 stay apart. W01's handoff round-trip limit is closed and merged; W02 is new work against a different target — the order of `make check` — and its tests sit in the check's own suite rather than in `src/tests/test_handoff_round_trip.py`. Neither reaches the other's files.
