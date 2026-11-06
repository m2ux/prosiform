# Release cut blocker: the version commit is already on `main`

> Recorded 2026-11-06

## What the plan states

`#525` W02–W04 join as one unit. W02's criterion is:

> **AC2.** `release/vX.Y.Z`, cut from `main`, holds one commit setting the selected version in `src/pyproject.toml` and the prosiform entry in `src/uv.lock`, as `git log main..release/vX.Y.Z` and `make lock-check` show.

So the release branch is cut from `main` and carries the bump as the one commit `main` lacks.

## What the repository holds

`main` already declares the selected version. Commit `98763ec4b` (`2026-10-30`, subject `Link the verb a dispatch sub-section's line opens with`) set `version = "0.16.0"` in `src/pyproject.toml` and the `prosiform` entry of `src/uv.lock`, as part of a 52-file change.

```text
$ git merge-base --is-ancestor 98763ec4b origin/main && echo ancestor
ancestor
$ git log --oneline origin/main..origin/main | wc -l
0
```

A `release/v0.16.0` branch cut from `origin/main` therefore holds no commit `main` lacks, so `git log main..release/v0.16.0` is empty and AC2 cannot hold as written. No `release/v0.16.0` branch and no `contract/v0.16.0` or `python/v0.16.0` tag exists yet.

The previous release did hold the stated shape: `240268522` (`Declare Python build version 0.15.0`) is the one commit `release/v0.15.0` carried beyond its parent, and it reached `main` through the release pull request.

## Why this is not this session's decision

Two resolutions exist and they differ in what the plan becomes:

- **Declare a version `main` has not set.** The release branch carries its own bump commit, which means moving the number off `0.16.0`, since `main` already holds that value.
- **Let the release carry no bump commit.** AC2 and W02 are restated for a version `main` already declares, and the tags and pull request go on the commit that carries it.

`docs/versioning.md` states that a change the contract's numbers move may declare the build's next version as it lands, so `main` reporting an untagged version is expected. That makes the second reading consistent with the repository's own convention, but choosing it rewrites an acceptance criterion and a row's scope, which is a plan change this session is not authorized to apply.

## State left behind

- W01 is delivered by `9380588ce`; AC1 is ticked.
- `#525` is Ready on the board with W02+W03+W04 reserved to no session.
- No branch, tag or pull request was created for W02–W04.
- The epic bases `i11/e00/main` and `i11/e00/engineering` exist and hold nothing beyond their long-lived branches.
