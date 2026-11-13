# Test Results

Results for the W00 design change at `808d2b711` on `i17/e01/w00-the-v1-design-states-engineering`.

## T1 Invocation and Presets Read

A read of design.md's Input and output contract, CLI contract, Link entries, Guide and Presets sections finds: an entry is a published Markdown link, `click` line or class diagram `link` line, or a plain path selecting no named preset; a link entry's leading operator marks are stripped and ignored; `--pick` names the alternative for an entry whose title or tooltip carries `?`, and is invalid usage, exit `2`, beside any other entry; the `E_ALTERNATIVE_UNRESOLVED` remedy names `--pick`. Held.

## T2 No Presets Option

`grep -n -- '--presets' artifacts/planning/2026-10-17-prosiform-v1/design.md` prints nothing and exits `1`. Held.

## T3 Link Check

The engineering branch carries no Makefile, so `make links`'s check ran from the `i17/e01/main` checkout naming the document: `python3 checks/links.py --online <engineering worktree>/artifacts/planning/2026-10-17-prosiform-v1/design.md` reports `link check: every reference in 1 document(s) resolved`, the new `#link-entries` anchor among them. Held.
