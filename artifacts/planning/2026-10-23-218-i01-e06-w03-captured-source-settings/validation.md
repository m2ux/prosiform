# Captured Source Validation

Task head: `65eaabda7238536694b4e7d9289329e6736f07ca`. Base: `5375a66`. Source implementation commit: `a805238`. Conformance snapshot: `a35cb50522c509cd79f57f53095f8d2481eb722d`.

## Source Integration

The implementation suite passes 903 tests, including 23 new captured-metadata integration cases. AC5 is observed through immutable independent source settings and one captured read per source. AC6 is observed through metadata links/headings excluded from Markdown and deferred-only content excluded from contribution. AC7 is observed through BOM/CRLF/both closers, original error coordinates, raw byte bounds before decoding, full-file hashes, metadata-only source changes and atomic output preservation. The deferred mutation case retains its inclusion chain.

The harness suite passes 615 tests. Independent CLI probes also pass: malformed deferred metadata, ignored metadata links, no traversal from deferred-only content, aggregate byte boundary, per-file bound preceding invalid UTF-8, existing output preservation and check-mode failure. Parent review found no remaining code findings.

## Complete Checks

Command: `PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i01/e06/w03-captured-source-settings/src --frozen pf' make check`.

Final result: exit 0 on the task head above. All checks pass: dependency lock, lint, formatting, types, 903 implementation tests, 615 harness tests, 254 corpus fixtures, installed-command smoke, layout, tables, online links, vocabulary, invocation, conformance and independence. Conformance reports zero undeclared runtime codes, zero declared codes absent from the runtime and zero fixture declarations naming no clause. The first full run exposed the snapshot's missing glossary term; the source contract retains that installation term. The invocation check also required the help text to state the independent YAML nesting budget. No check is disabled or weakened.

## GitHub Checks

Remote CI result pending. Merge requires the exact head's passing checks, current target requirements and current review state.

## Scope

The runtime validates and retains settings. Applying metadata to grouping and removing structural CLI arguments belong to W04. The task changes no unrelated workspace files.
