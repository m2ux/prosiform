## Overview

A Rust build of md-compose is the tool agents invoke, and it passes the fixture corpus without a fixture changing. It retains original source bytes and applies edits to identified spans, so untouched content and code examples survive composition exactly. Before any of that work starts, the two parser viability gates the design names are answered by executed reproducers against a pinned parser version, with a recorded verdict and a recorded route for any gate the parser fails. The build targets one tagged revision of the design and corpus, so later refinement does not move the contract under it.

## Problem

A composition the production build publishes must be trusted byte for byte, and the parser it rests on has not been proven able to supply that.

- **Reconstruction loses what the source said.**
  Regenerating a document through a formatter rewrites spacing, escaping and newline spelling, so composed instructions and code examples stop being the bytes an author wrote.

- **A definition map holds one occurrence per label.**
  The inspected first pass inserts definitions with a first-wins entry, so a later duplicate occurrence has no map entry, and a source transformer removing definitions cannot find it.

- **A suppressed reference looks like ordinary text.**
  The inspected lookup returns nothing when its reference-expansion budget is zero, before definition lookup, so a reference the limit suppressed and bracketed text that was never a link reach the consumer identically.

- **The event range is not the destination range.**
  An enclosing event carries a span for the construct, not for the destination inside it, so an edit placed from that span alone can fall outside the text it means to replace.

- **An unpinned dependency changes the contract.**
  Parser behaviour on duplicate definitions, offsets and option-controlled extensions is what the profile rests on, so an unpinned upgrade can change how existing source is interpreted.

- **A contract read from a branch tip moves under the build.**
  Fixtures and design clauses that change while the build is written leave it satisfying no revision in particular.

## Proposal

- **The gates are answered before the build.**
  Executed reproducers establish whether the pinned parser exposes every reference-definition occurrence and whether it makes a suppressed reference lookup observable. Each answer and its evidence are recorded.

- **A failed gate takes a recorded route.**
  Parser-aware occurrence collection, narrowly scoped instrumentation, a different parser candidate and a separate upstream proposal are the routes. The route taken is a recorded decision, not an implicit fallback.

- **Edits are applied to verified spans.**
  Original bytes are retained and replaced in place. A construct whose exact edit span cannot be established fails rather than falling back to pattern rewriting or whole-document formatting.

- **The corpus is inherited, not rewritten.**
  The production build passes the fixtures established before the freeze. A fixture changing to accommodate the production build is a change to the contract and is decided as one.

- **One tagged revision is the target.**
  The work names the tagged revision of the design and corpus it implements, and adopting a later one is a recorded decision.

- **Both builds stay on one corpus.**
  A differential run composes each corpus input with both builds and compares the results, so a divergence is a defect in one of them rather than a silent difference.

- **Versions are pinned after the fixtures pass.**
  The parser, the slugging component and every other dependency take exact versions, chosen once the fixtures hold against them.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/md-composer/issues/11) | Parser Verdict | AC1 | | |
| [E01](https://github.com/m2ux/md-composer/issues/12) | Source-Range Adapter | AC2, AC3, AC10 | [E00](https://github.com/m2ux/md-composer/issues/11) | |
| [E02](https://github.com/m2ux/md-composer/issues/13) | Profile and Outline | AC4 | [E00](https://github.com/m2ux/md-composer/issues/11) | |
| [E03](https://github.com/m2ux/md-composer/issues/14) | Closure and Budgets | AC5 | [E00](https://github.com/m2ux/md-composer/issues/11) | |
| [E04](https://github.com/m2ux/md-composer/issues/15) | Destination Identity | AC6 | [E00](https://github.com/m2ux/md-composer/issues/11) | |
| [E05](https://github.com/m2ux/md-composer/issues/16) | Validation and Delivery | AC7 | [E04](https://github.com/m2ux/md-composer/issues/15) | |
| [E06](https://github.com/m2ux/md-composer/issues/17) | Differential Conformance | AC8, AC9 | [E05](https://github.com/m2ux/md-composer/issues/16) | |

## Acceptance Criteria

- [ ] **AC1.** Each parser viability gate the design names has an executed reproducer and a recorded verdict against a pinned parser version, as the gate report shows.
- [ ] **AC2.** Untouched source bytes and their newline spelling survive composition exactly, as the corpus's preservation fixtures and the span-fidelity fixtures show.
- [ ] **AC3.** A reference lookup an internal parser limit suppresses is observable to the compiler rather than indistinguishable from literal bracketed text, as the exhaustion fixtures show.
- [ ] **AC4.** A published composite keeps the source outline and the declared Markdown profile, as the corpus's outline and profile fixtures show.
- [ ] **AC5.** A composition resolves its dependency closure and holds every limit the profile names, as the corpus's closure and limit fixtures show.
- [ ] **AC6.** A published composite carries one destination per rewritten reference and no original reference definition, as the corpus's destination and reference fixtures show.
- [ ] **AC7.** A composition that fails validation publishes nothing, exits nonzero and writes its diagnostic, as the corpus's failure fixtures show.
- [ ] **AC8.** Both builds produce identical output for each corpus input, as the differential run shows.
- [ ] **AC9.** Every dependency is pinned to an exact version against which the corpus passes, as the lockfile and that run show.
- [ ] **AC10.** The build implements one tagged revision of the design and corpus, as the recorded target revision and the corpus run against it show.

## Non-Goals

- It does not open an issue or a pull request on another project.
- It does not disable a parser resource protection to satisfy a gate.
- It does not rewrite a corpus fixture to accommodate the production build without a recorded decision.
- It does not replace the prototype, which stays in use as the differential oracle.
- It does not fetch remote documents, resources or URLs.
- It does not accept its own output as a source document.

## References

- **R1.** **Source.** [v1 design](https://github.com/m2ux/md-composer/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-md-compose-v1/design.md) — the behavioural contract these criteria answer to, including the parser viability gates and the source-preserving edit requirement.
- **R2.** **Source.** [Upstream assessment](https://github.com/m2ux/md-composer/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-md-compose-v1/upstream-assessment.md) — the inspected parser state behind the gates, and the routes open when one fails.
- **R3.** [Planning decisions](https://github.com/m2ux/md-composer/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-md-compose-v1/decisions.md) — why gate evaluation precedes the build and why the upstream route is a separate proposal.
- **R4.** [Proposal](https://github.com/m2ux/md-composer/issues/1) — the scoped problem and the goal clauses these criteria trace to.
