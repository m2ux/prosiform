# Per-File Root Resolution Validation

## Revision

Task branch `i01/e06/w08-per-file-root-resolution`, head `af13226c686d8e453864b0485e19a6259e07da38`, targets `i01/e06/main`. The tracked working tree is clean.

## File Roots And Installed Command

AC20 and AC22 are observed by the installed-wheel smoke test: a file-only invocation from an unrelated directory uses the entry's declared root, while `-r` returns invalid usage. AC21 is observed by 19 focused source-root tests and the corpus. Coverage includes working-directory defaults for entry and linked sources, explicit sibling/library roots, distinct roots, shared targets and cycles, fragment-only references outside the source's root, deferred URI destinations, deterministic headings, ambiguous headings, missing roots with physical coordinates, symlink walks before normalization, cached-route validation, confinement, directory mutation and bounded capture.

Source access records file and directory identities, reads at most the remaining byte budget plus one byte, and rechecks captured bytes and identities before publication. Each authored path-bearing dependency resolves against its declaring source's root. Each reached source supplies its own outgoing root. The command rejects `-r`.

## Full Checks

`PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i01/e06/w08-per-file-root-resolution/src --frozen pf' make check` passes at the task head. See [full-check.log](full-check.log).

- Source tests: 993 passed.
- Check-harness tests: 614 passed.
- Corpus: 253 passed, zero failures or awaited fixtures.
- Installed-wheel smoke, lock, lint, formatting, strict typing, layout, tables, online links, vocabulary, invocation, conformance and independence pass.
- `git diff --check` passes.
- The diagram renderer compiles `example/my-skill/SKILL.md` with `--compact` and produces its SVG and review artifacts successfully at this head.

The runtime check profile now pins the accepted W06 contract through the [contract snapshot](design.md). Its report names 53 clauses without fixtures, 16 clauses with no run, and three installation claims not observed by a run. These are explicit coverage gaps, not passing assertions. Automatic output naming/publication remains W09 scope; this unit retains stdout publication.

## Review And Plan Changes

The corpus runner declares invocation working directories rather than a root CLI argument. Active examples declare their intended roots. Affected authored links use root-relative destinations to retain their targets and compiled outputs; the parent-entry fixture now observes the accepted outside-working-directory bootstrap. This is required consumer alignment for AC21, with no task or criterion changes. The documentation link checker reads explicit root declarations while preserving fragment-only self references; its focused test passes. Blocking validation findings were corrected in this unit. No new standalone debt or arising issue was identified.

The existing contract-review #227 reference discrepancy remains outside this runtime unit: it cites #226 while the contract base contains #219 and #226.

## Delivery

Pending task pull request publication and verified merge. The repository auto-close setting is confirmed disabled in the user session. This task row has no task issue.
