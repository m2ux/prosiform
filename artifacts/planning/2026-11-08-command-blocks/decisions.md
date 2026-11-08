# Decisions

## Confirmed

- The profile accepts exactly one HTML form: a paragraph whose first inline is `<big><pre>` and whose last is `</pre></big>`. Every other raw HTML, `<pre>` or `<big>` alone included, is still refused with `E_RAW_HTML` (user, 2026-11-08).
- The bundle carries the wrapper as written. Links inside it are discovered, resolved and rewritten as any paragraph's are (user, 2026-11-08).
- The rewrite fault that Compute Board Queue raises without its command block is fixed in the same hot-fix (user, 2026-11-08).
- Acceptance is corpus fixtures for both defects, plus a scratch copy of work-planner, given `prosiform` frontmatter, compiling `artifacts/board-queue.md#compute-board-queue` without a diagnostic. Declaring `prosiform` across work-planner is separate work in m2ux/workflow-server (user, 2026-11-08).
- `contract/v0.20.0` and `python/v0.20.0` are cut once the pull request merges (user, 2026-11-08).

## Implementation Details

- A `<pre>` line on its own opens a CommonMark HTML block whose content is not parsed, so the wrapper is recognised only as the `html_inline` pair `<big><pre>` and `</pre></big>` bounding one paragraph. A wrapper opened without being closed in the same paragraph, or one carrying attributes, is still refused.
- No existing fixture uses `<big>` or `<pre>`; the refusal fixtures use `<div>` and `<a href>` and stay unchanged. Fixtures are added and none fail, so the release is a minor, as the previous corpus run confirms.
- The rewrite fault's trigger is not yet isolated. A minimal document with same-document titled links compiles, so the trigger lies in the section's closure (`lane.md`, `hotfix.md` or a reference-style definition). Isolating it to a minimal fixture is the first step of that half.
- `docs/sources.md` states the accepted wrapper beside the raw HTML refusal; `docs/validation.md` keeps `E_RAW_HTML` for everything else.
- One pull request into `main`, opened as a draft and marked ready once review clears.
