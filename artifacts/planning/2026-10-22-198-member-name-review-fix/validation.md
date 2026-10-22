# Validation

At epic revision aea9a90, four regression cases failed: group-word removal, title casing, separator normalization, and group-word removal with no distinguishing directory. The corrected implementation passes these cases and all 48 grouping tests.

The new corpus fixture expects modes/a/plan.md and modes/b/plan-mode.md to become A Plan and B Plan in both overview and variant headings, with distinct whole-document destinations.

Correction revision: a35b38c on i01/e02/main. Governing design revision: d4226f3 on engineering.

Full make check passed with the epic worktree build selected through PROSIFORM_BUILD:

- 758 implementation tests passed.
- 608 harness tests passed.
- All 252 corpus fixtures passed.
- Lock, lint, format, strict typing, installation smoke, layout, tables, authenticated links, vocabulary, invocation, conformance and independence passed.
- The final source-comment adjustment passed targeted lint and format checks.

The four new regression cases failed before implementation and pass with the correction. The corpus fixture confirms A Plan and B Plan in both overview and variant headings and distinct entry destinations. Members in one directory retain Plan and Plan Mode when further qualification is unavailable.

Remote CI pending at a35b38c. PR #198 remains draft.
