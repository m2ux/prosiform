# Validation

At epic revision aea9a90, four regression cases failed: group-word removal, title casing, separator normalization, and group-word removal with no distinguishing directory. The corrected implementation passes these cases and all 48 grouping tests.

The new corpus fixture expects modes/a/plan.md and modes/b/plan-mode.md to become A Plan and B Plan in both overview and variant headings, with distinct whole-document destinations.

Full repository checks and remote CI pending.
