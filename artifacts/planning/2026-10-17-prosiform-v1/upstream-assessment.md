# md-compose: upstream contribution assessment

An upstream contribution to pulldown-cmark is worth pursuing, but it should be framed as two small observability improvements rather than a new strict parser or a removal of resource protections. The md-compose specification now incorporates the two parser acceptance checks and the two validator clarifications approved by the user.

This assessment inspected upstream `main` at commit `ad1622be42b65cdf24ce41e070e516d8844436f0` and relevant issue history. It does not contain an implemented patch, executed reproducer, submitted issue, or pull request.

## Why upstream is a reasonable route

Source-preserving Markdown tooling is an established upstream use case: issue #423 discussed formatters and diagnostic spans, including a preference for exposing definitions separately rather than forcing renderers to handle new events; it was closed through #512's definition-tracker access ([issue #423 and discussion](https://github.com/pulldown-cmark/pulldown-cmark/issues/423)).

The remaining requirement is narrower than “expose reference definitions”: retain access to every original occurrence, including later duplicate definitions. The inspected current first pass still inserts definitions with `entry(label).or_insert(link_def)`, while the parser exposes the retained map ([current first pass](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/ad1622be42b65cdf24ce41e070e516d8844436f0/pulldown-cmark/src/firstpass.rs), [current parser](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/ad1622be42b65cdf24ce41e070e516d8844436f0/pulldown-cmark/src/parse.rs)).

The expansion limit is intentional protection against quadratic growth, not simply an accidental parsing limitation: its introducing PR discusses both reference-definition and callback costs ([PR #845](https://github.com/pulldown-cmark/pulldown-cmark/pull/845)). Our proposal should preserve that protection and expose when it prevents complete reference resolution.

## Proposed contribution: observable suppressed reference resolution

**Working title:** “Expose when the reference-expansion limit suppresses a lookup.”

The inspected `main` still returns `None` when its reference-expansion budget is zero, before definition lookup or broken-link callback handling ([current lookup implementation](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/ad1622be42b65cdf24ce41e070e516d8844436f0/pulldown-cmark/src/parse.rs)). A strict source transformer needs to distinguish that condition from legitimately unresolved bracketed text.

### Smallest useful contract

- Preserve the existing default event stream, expansion bound, and non-fallible iterator interface.
- Expose that at least one reference lookup was suppressed, preferably with the first affected source span.
- Make the observation available to both ordinary-parser and offset-iterator consumers.
- Report actual suppression, not merely a remaining budget of zero after a successfully emitted final reference.
- Bound any additional state; do not allocate a diagnostic entry for every later suppressed occurrence.
- Allow consumers such as md-compose to discard their buffered output and return an explicit failure.

A sticky status accessor with an optional first span is one possible API. A default-no-op callback is another: current `main` already has a `ParserCallbacks` trait whose methods have default implementations, although its inspected callback handles broken links rather than limit suppression ([callback interface](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/ad1622be42b65cdf24ce41e070e516d8844436f0/pulldown-cmark/src/parse.rs)). The public API shape should be agreed with maintainers rather than treating either sketch as an existing interface.

### Regression and performance checks

- Repeated references with a long destination or title trigger an observable suppression condition.
- Ordinary missing definitions do not falsely report limit suppression.
- A final successful reference that exhausts the budget, with no later lookup, does not falsely report omitted content.
- Callback-generated destinations remain covered by the existing protection.
- The default event and HTML behaviour remains unchanged.
- Normal and adversarial performance remains bounded; benchmark any added state or callback overhead.

**Do not include:** Disabling the limit, making it unlimited by default, replacing the iterator API with `Result` events, or adding a general diagnostics framework without maintainer demand.

## Proposed contribution: complete definition-occurrence access

**Working title:** “Add opt-in source ranges for all reference-definition occurrences.”

Keep the existing winning-definition map and its original resolution semantics. Add an opt-in way for source tools to observe definitions that do not become map entries.

### Smallest useful contract

- Return or report every syntactically recognized definition occurrence in source order.
- Include its source span and label identity, including later duplicates and case-fold-equivalent labels.
- Preserve access to unused definitions and definitions in supported container contexts.
- Keep ordinary rendering behaviour and first-definition-wins resolution unchanged.
- Avoid mandatory collection/allocation for consumers that do not request occurrence data.
- Document whether spans cover container prefixes and multiline syntax so source editors can remove content safely.

An opt-in iterator backed by captured occurrence spans, or an opt-in collector during the first pass, would satisfy the use case. A callback would require deliberate first-pass plumbing: the inspected constructor currently runs the first pass before constructing the callback-owning parser, so adding an inline callback alone would not expose discarded definition occurrences ([constructor](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/ad1622be42b65cdf24ce41e070e516d8844436f0/pulldown-cmark/src/parse.rs)).

### Regression and performance checks

- Duplicate labels expose all occurrence spans while lookups still select the original winner.
- Case-fold-equivalent labels, multiline definitions, CRLF, and supported nested containers are covered.
- Definition-like text inside fenced and inline code is not reported.
- Unused definitions are visible when collection is enabled.
- Default parsing avoids unnecessary storage and shows no unacceptable regression.

**Do not include:** Changing duplicate-definition semantics, emitting new mandatory renderer events, or bundling compositor-specific anchors and path handling into the parser.

## Existing offset-iterator issue to track, not duplicate

Issue #1129 reports an offset-iterator panic on definition-containing list items, including a later printable-character reproducer; an October 16 comment reports that current `main` fixes it and describes a stable-branch backport ([issue #1129](https://github.com/pulldown-cmark/pulldown-cmark/issues/1129)). The inspected current first pass contains the blank-line termination condition discussed in that report, but this assessment has not executed the reproducer ([current first-pass code](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/ad1622be42b65cdf24ce41e070e516d8844436f0/pulldown-cmark/src/firstpass.rs)).

Include those cases when evaluating the exact parser version. Do not open another panic report for the same problem; if a backport or regression test is still needed, coordinate through the existing issue.

## Contribution sequence

The project asks contributors to discuss larger changes through the issue tracker before starting them, and all submissions require review ([contribution guidance](https://raw.githubusercontent.com/pulldown-cmark/pulldown-cmark/main/CONTRIBUTING.md)).

I recommend this sequence:

1. Recheck the relevant open issues and branches immediately before any outreach.
2. Prepare a concise design discussion referencing #423/#512 and #845, distinguishing complete source-occurrence data from winning-definition lookup and suppression reporting from removal of limits.
3. Ask maintainers which API shape they prefer and whether they want separate discussion issues.
4. Once implementation is authorized, reproduce the cases on the selected release and current upstream commit, then prepare two independently reviewable patches.
5. Run the project's test suite, the new regression cases, and performance checks; keep md-compose's own semantics out of the upstream patches.
6. Publish only after the user approves the destination and complete outbound issue or PR payload.

If upstream declines the APIs, consider a narrowly pinned patch while retaining the acceptance gates, or evaluate another parser. Neither a private fork nor an upstream contribution should be assumed necessary before testing the available API and discussing the scope.

## Recommendation

Pursue upstream discussion, prioritizing suppression observability because its contract can remain small and preserve the security limit unchanged. Follow with opt-in definition-occurrence access, which is valuable for source-preserving tools but needs closer performance and API review.

The contribution should remain an explicitly authorized follow-on activity. At this stage, only the md-compose design has been updated; nothing has been posted, committed, or implemented.
