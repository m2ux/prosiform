# Decisions

## Confirmed

- The epic belongs to I10. Its goal and acceptance criteria extend to link-tag preset selection (user, 2026-11-06).
- The link title holds plain comma-separated preset names, such as `"checks,draft"`; angle brackets are not tag delimiters.
- A tag with no matching preset of the target is silently ignored. A document's `default` continues to apply.
- The command form is `pf --entry guide.md#plan-report --tags checks,draft`. An agent encountering a tagged link is instructed to supply that command specification.
- One invocation takes one entry and produces that entry's set of output bundles. The final clarification supersedes the provisional repeated-entry and full-Markdown-link argument proposals.
- Heading names and visible link labels select no presets. Tags are carried by each individual link.
- Two dispatches to the same document and section with different effective preset selections produce distinct bundles. Identical effective selections share a bundle.
- This request plans the work. Product implementation and paid evaluation are outside this request.

- Delivery lane: every task uses lane 1 (user-confirmed, 2026-11-06).
- Epic priority: 1, initial board status: Backlog (user-confirmed, 2026-11-06).

## Implementation Details

- A tag list splits on commas, trims surrounding whitespace, drops empty tokens and duplicates, and compares complete preset names case-insensitively, preserving the current case-insensitive matching policy.
- A missing or empty title selects `default` alone. A token naming `default` adds nothing. Order and repetition give no precedence.
- Inline and reference-style Markdown links use their parsed title attribute. Images and external links retain their existing resource treatment. Mermaid destinations carry no tags in this epic; tooltip syntax is outside its Markdown-title scope.
- Existing per-document preset layering, grouping, substitution union and conflict rules apply to the selected presets. Tag lists do not propagate into the target's outgoing links.
- Bundle variants use destination plus the canonical effective preset-name set, excluding `default` as an implicit constant. Unknown tags and tag order do not create variants. A deterministic filename qualifier distinguishes named-preset variants; the empty-selection bundle uses the ordinary destination-derived filename.
- A deferred link preserves its title for a later command. Destination paths passed to the command resolve from the chosen invocation directory; a same-file fragment needs its containing document path.
- The heading-comparison refusal for deferred compositions is retired because the later command supplies the selection explicitly.
- Bare `pf` continues to print its guide. A compilation has exactly one `--entry` and at most one `--tags`; positional compilation entries, repeated entry groups, tags without an entry and a full Markdown-link CLI argument are outside the command grammar.

