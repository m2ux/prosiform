# The release version: 0.17.0

> Measured 2026-11-06

## The policy

`docs/versioning.md` fixes the number by measurement rather than judgement:

> The distinction is settled by running the previous revision's corpus against the new build rather than by judgement. A fixture that fails is a major change, a fixture added is a minor one, and neither is a patch.

> Below `1.0.0` the minor carries what the major would: a release whose previous corpus fails against it, and one that only adds fixtures, each move the minor, and the patch keeps its meaning.

It also states that a version may be declared before it is tagged:

> A change the contract's numbers move may declare the build's next version there as it lands, so `main` can report a version no tag carries yet.

## Two candidate baselines

`main` declares `0.16.0` and carries no tag for it, so the "previous revision" is one of two commits. Both were run against the build at `origin/main` (`fb17c2c97524b649dc4b619f1b88cd825a797d85`).

| Baseline | Fixtures | Against this build | Against its own build |
| --- | --- | --- | --- |
| `contract/v0.15.0` (`240268522`) | 312 | 7 pass, 305 fail | 312 pass |
| The `0.16.0` declaration (`98763ec4b`) | 342 | 6 pass, 336 fail | 342 pass |

Both runs are major changes, and both move the minor under the pre-1.0 rule. The two readings therefore agree on the direction and differ only on the starting point.

## Why the starting point is the declaration, not the tag

The `0.16.0` declaration is a distinct contract revision, not an empty claim. At `98763ec4b` the corpus holds 342 fixtures and passes 342 of them against the build of that commit, and that build reports `pf 0.16.0 (skill-markdown-v4)`. The 342 fixtures are 30 more than `contract/v0.15.0` holds, and the profile identifier differs from the one `contract/v0.15.0` names.

Tagging `0.16.0` now would name a revision that has already been superseded: the contract `98763ec4b` states has since moved again, by the measured major change above. A tag names the revision a build implements, so it cannot name a revision whose corpus that build fails.

Re-declaring `0.16.0` on the release branch was rejected for the same reason. It would assert a version whose own corpus fails against the commit carrying it, and `main` already holds that number, so the commit would change nothing but repeat a value.

## The version

`0.17.0`. The minor moves once from the running declaration of `0.16.0`, which is what the pre-1.0 rule prescribes for a release whose previous corpus fails against it.

No patch release has ever been cut in this repository: the tag list runs `contract/v0.9.0` through `contract/v0.15.0` with no `.1` among them, so the established procedure moves the minor.

## Evidence

- [`git tag -l 'contract/v*'`](../2026-11-06-525-i11-e00-w01-the-version-the-previous/release.md) — the tagged history.
- The `0.16.0` declaration: `98763ec4b`, whose message ends "The build is 0.16.0: bytes a conforming build emits have changed, which is the contract's major."
- Both corpus runs are recorded by commit in this document.
