# Versioning: What the Numbers Assert — October 2026

> Policy · Created 2026-10-21

## Executive Summary

This repository holds a contract and the builds that implement it, and they change at different rates. The contract is `design.md` and the fixture corpus together; the builds are the Python one this initiative delivered and the Rust one the production initiative will add. One version number across all of them would either assert that the contract is settled when it is not, or move a build's number every time a fixture's prose is reworded.

So the contract and each build are versioned separately, and a build's number says which contract revision it implements. The contract's public surface is what a fixture can observe, which gives *breaking change* a meaning this project can check rather than one a reader has to judge.

## What Is Versioned

| Thing | Tag | What it covers |
| --- | --- | --- |
| The contract | `contract/vX.Y.Z` | `design.md` and `fixtures/` — the behaviour any implementation is held to |
| The Python build | `python/vX.Y.Z` | `src/` |
| The production build | `rust/vX.Y.Z` | the tree the production initiative creates |

The contract is the product and the builds answer to it. The refinement stage ends with one tagged revision of design and corpus that the production build names as its target, so that revision is the contract's rather than any build's.

## What the Numbers Mean

The contract's public surface is the behaviour a corpus fixture can observe: the command-line grammar, the bytes a run emits, and the diagnostic codes and exit statuses it reports.

- **Major.**
  A change that makes a conforming build stop conforming. An option removed, an exit status changed, different bytes emitted for an unchanged source. A build must change to keep passing the corpus.
- **Minor.**
  New observable behaviour that leaves every existing fixture passing. A new option, a new diagnostic code, a case that previously had no stated outcome.
- **Patch.**
  A change no fixture can observe. Wording in the design, a reason string in a report, prose in the corpus guide.

The test is mechanical rather than editorial: run the previous revision's corpus against the new one. A fixture that fails is a major change, a fixture added is a minor one, and neither is a patch.

## How a Build Relates to the Contract

A build's **major and minor are the contract revision it implements**; its patch is its own.

- `python/v1.2.4` and `rust/v1.2.0` both implement `contract/v1.2.x`, and are expected to agree on every fixture. That is what makes differential testing meaningful: one corpus, one revision, two builds.
- A build that cannot yet meet the current contract keeps the older minor. The gap is then visible in the version rather than implied by a failing run.
- A build's patch moves for a defect fix or a performance change that no fixture observes.

## The Profile Identifier Is Separate

`skill-markdown-v1` names the Markdown grammar the parser accepts, and `--version` reports it beside the version. It stays an opaque identifier and is not a semantic version: it changes only when the accepted grammar changes, which is itself a contract major. Folding it into the version would conflate which Markdown is read with which contract is implemented.

## Reaching 1.0.0

**1.0.0 is the freeze.** The refinement stage exists to change the design, the corpus and the build from what real use shows, so a 1.0.0 before it would assert a stability the plan explicitly withholds. Everything before the freeze is `0.y.z`, where the convention already means that anything may change.

At the freeze, the contract takes `contract/v1.0.0` and each conforming build takes `1.0.0`. The production initiative names that revision as its target.

## Decisions

- **The completed prototype initiative is `0.9.0`.**
  Confirmed 2026-10-21. The build meets the contract as written — every behavioural clause carrying a fixture or a recorded reason, every declared code reached, the corpus green — so it is feature-complete, and `0.9.0` says that while leaving the assertion of stability to the freeze. `1.0.0-rc.1` was considered and refused: a release candidate implies the release is near, and the refinement stage has no committed end date.

- **Versioning is per-thing rather than per-repository.**
  Confirmed 2026-10-21. A single repository-wide number was refused because the corpus and the builds change independently, and the plan already requires a contract revision a build can name.

## Outstanding

- **Nothing holds a tag to the version the build reports.**
  A `python/vX.Y.Z` tag whose build answers `--version` with something else would go unnoticed. The check that refuses that is a repository check, so it belongs with the other carried debt on [#187 \[I01:E03\]](https://github.com/m2ux/prosiform/issues/187) rather than in a release.

## Links

| Resource | Link |
| --- | --- |
| Prototype initiative | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Refinement initiative | [#20 \[I01\] Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Production initiative | [#10 \[I02\] Production Compiler](https://github.com/m2ux/prosiform/issues/10) |
| Version pull request | [#190](https://github.com/m2ux/prosiform/pull/190) |
