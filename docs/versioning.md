# Versioning

This repository holds a contract and the builds that implement it. They change at different rates, so they carry their own version numbers, and a build's number says which contract revision it implements.

## What carries a version

| Thing | Tag | What it covers |
| --- | --- | --- |
| The contract | `contract/vX.Y.Z` | the [fixture corpus](../fixtures/README.md) the tagged commit holds and the design it encodes — the behaviour any implementation is held to |
| A build | `<build>/vX.Y.Z` | one implementation's tree, such as `python/v0.15.0` for [`src/`](../src/README.md) |

The contract is the product and a build answers to it. A production build names a contract revision as the target it implements, so that revision is tagged in its own right rather than read off whichever build shipped beside it.

The Python build declares its version in `src/pyproject.toml`, and `pf -v` reports that version beside the [profile identifier](#the-profile-identifier), as `pf 0.16.0 (prosiform-markdown)`. A change the contract's numbers move may declare the build's next version there as it lands, so `main` can report a version no tag carries yet.

## What the numbers mean

The contract's public surface is the behaviour a corpus fixture can observe: the command-line grammar the [documented invocation](../invocation.md) states, the bytes a run emits, and the diagnostic codes and exit statuses it reports.

- **Major** is a change that makes a conforming build stop conforming: an option removed, an exit status changed, different bytes emitted for an unchanged source. A build changes to keep passing the corpus.
- **Minor** is new observable behaviour that leaves every existing fixture passing: a new option, a new diagnostic code, a case the corpus states no outcome for.
- **Patch** is a change no fixture can observe: wording in the design, a reason string in a report, prose in a guide.

The distinction is settled by running the previous revision's corpus against the new build rather than by judgement. A fixture that fails is a major change, a fixture added is a minor one, and neither is a patch.

## A build and the contract it implements

A build's major and minor are the contract revision it implements. Its patch is its own.

- Two builds carrying the same major and minor implement one contract revision and are expected to agree on every fixture. That is what makes a divergence between them a defect in one of them rather than a difference of version.
- A build that does not meet the current contract keeps the earlier minor, so the gap is visible in the version rather than implied by a failing run.
- A build's patch moves for a defect fix or a change no fixture observes.

## Cutting a release

A release is one commit carrying both tags.

1. **Branch.** `release/vX.Y.Z` is cut from `main`.
2. **Declare.** One commit on it, `Declare Python build version X.Y.Z`, sets the version in `src/pyproject.toml` and the `prosiform` entry of `src/uv.lock`.
3. **Choose the number.** The previous contract tag's corpus runs against the new build, from a worktree of that tag with `PROSIFORM_BUILD` naming the new build. Its passes and failures decide the number, as [What the numbers mean](#what-the-numbers-mean) states.
4. **Tag.** Annotated `contract/vX.Y.Z` and `python/vX.Y.Z` tags name that commit. The contract tag's message records what the revision adds, the current corpus's fixture count, and the previous corpus's passes and failures against this build. The build tag's message records the contract it implements, the profile, and the validation that passed.
5. **Merge back.** The release branch merges into `main`, so `main` reports the shipped version. The branch stays after the merge.

A published tag never moves. Work that merges after a release is tagged ships in the next one.

## The profile identifier

`prosiform-markdown` names the Markdown grammar the parser accepts, and `-v` reports it beside the version. It carries no version of its own: a change to the accepted grammar is a change of contract major, and the contract's number is what states it. What Markdown is read and what contract is implemented are separate statements, and one identifier states each.

## Below 1.0.0

`1.0.0` asserts a settled contract, and the contract is settled by use rather than by implementation. Until the design and the corpus carry the revision that use has settled, versions stay below `1.0.0`, where the convention already states that anything may change.

Below `1.0.0` the minor carries what the major would: a release whose previous corpus fails against it, and one that only adds fixtures, each move the minor, and the patch keeps its meaning.

The settled revision is `contract/v1.0.0`, and a build meeting it carries `1.0.0`.
