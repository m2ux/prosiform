# Versioning

This repository holds a contract and the builds that implement it. They change at different rates, so they carry their own version numbers, and a build's number says which contract revision it implements.

## What carries a version

| Thing | Tag | What it covers |
| --- | --- | --- |
| The contract | `contract/vX.Y.Z` | the design and the [fixture corpus](../fixtures/README.md) — the behaviour any implementation is held to |
| A build | `<build>/vX.Y.Z` | one implementation's tree, such as `python/v0.9.0` for [`src/`](../src/README.md) |

The contract is the product and a build answers to it. A production build names a contract revision as the target it implements, so that revision is tagged in its own right rather than read off whichever build happened to ship beside it.

## What the numbers mean

The contract's public surface is the behaviour a corpus fixture can observe: the command-line grammar the [documented invocation](../invocation.md) states, the bytes a run emits, and the diagnostic codes and exit statuses it reports.

- **Major** is a change that makes a conforming build stop conforming: an option removed, an exit status changed, different bytes emitted for an unchanged source. A build changes to keep passing the corpus.
- **Minor** is new observable behaviour that leaves every existing fixture passing: a new option, a new diagnostic code, a case that previously had no stated outcome.
- **Patch** is a change no fixture can observe: wording in the design, a reason string in a report, prose in a guide.

The distinction is settled by running the previous revision's corpus against the new one rather than by judgement. A fixture that fails is a major change, a fixture added is a minor one, and neither is a patch.

## A build and the contract it implements

A build's major and minor are the contract revision it implements. Its patch is its own.

- Two builds carrying the same major and minor implement one contract revision and are expected to agree on every fixture. That is what makes a divergence between them a defect in one of them rather than a difference of version.
- A build that does not yet meet the current contract keeps the earlier minor, so the gap is visible in the version rather than implied by a failing run.
- A build's patch moves for a defect fix or a change no fixture observes.

## The profile identifier

`skill-markdown-v3` names the Markdown grammar the parser accepts, and `-v` reports it beside the version. It is an opaque identifier rather than a semantic version: it changes when the accepted grammar changes, which is itself a change of contract major. What Markdown is read and what contract is implemented are separate statements, and one identifier states each.

## Below 1.0.0

`1.0.0` asserts a settled contract, and the contract is settled by use rather than by implementation. Until the design and the corpus carry the revision that use has settled, versions stay below `1.0.0`, where the convention already states that anything may change. That settled revision is `contract/v1.0.0`, and a build meeting it carries `1.0.0`.
