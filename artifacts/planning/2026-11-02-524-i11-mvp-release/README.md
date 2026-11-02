# I11 MVP Release — November 2026

> Initiative planning · Created 2026-11-02

## Executive Summary

I11 releases the MVP: the argument surface and the grouping and composition work, once both are merged into `main` and proven. It cuts one version commit on a release branch, tags it with an annotated `contract/` and `python/` pair, and raises the release branch into `main`, with the version chosen by running the previous contract's corpus against the build.

A caller names a release by its tags, and a production build names the contract revision it implements by its `contract/` tag. Until the MVP is tagged, the newest name for the contract is `contract/v0.15.0`, which predates every feature the MVP delivers.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [E00 W01 work item](e00/w01.md) | The previous corpus run and the version it selects |
| [E00 W02 work item](e00/w02.md) | The release branch and its version commit |
| [E00 W03 work item](e00/w03.md) | The `contract/` and `python/` tag pair |
| [E00 W04 work item](e00/w04.md) | The release pull request into `main` |

## Goal

The goal is the initiative's Overview: a released MVP a caller can name by its tags. Its clauses:

- **G1.** The release's version is the one the previous contract's corpus selects.
- **G2.** One version commit carries the tag pair and reaches `main` by pull request.

## Goal Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| G1 | AC1 | E00 | E00 AC1 | `docs/versioning.md`: the bump is settled by running the previous revision's corpus |
| G2 | AC2 | E00 | E00 AC2–AC5 | `docs/versioning.md`: a contract and a build each carry a tag |

### Gaps, Ranked

None. Every clause has a criterion, each criterion is delivered by the one epic, and every epic criterion is covered by a task row.

### Outside Threats

- **The release waits on I08 and I09 closing.** E00 W01 depends on #462 and #463, so the corpus run reads the merged MVP.
- **The merge into `main` is the user's.** E00 AC5 holds the pull request open with its checks passing, not merged.

## Design

- **The run selects the version.** Any failure of the `contract/v0.15.0` corpus against the release build is incompatible, which below 1.0 bumps the minor, as `docs/versioning.md` states.
- **One commit, two files.** The release branch `release/vX.Y.Z` from `main` holds one commit bumping `src/pyproject.toml` and the prosiform entry in `src/uv.lock`.
- **The tag messages follow the previous pair.** `contract/v0.15.0` states its subject, profile, corpus count and the previous corpus's result; `python/v0.15.0` states the contract it implements, its profile, package version and validation counts.
- **W02–W04 are one unit.** They declare `main:src/pyproject.toml` and join, so the release branch, its tags and its pull request are delivered together.

## Dependency Check

`deps.py` over the initiative, the epic and its four work items: no problems; W02, W03 and W04 joined; longest chain two steps, W01 then the joined unit; epic priority E00 1.

## Decisions

- **The release is its own initiative.** (User, 2026-11-02.) I11 MVP Release follows I08 and I09 and precedes I10.
- **Cut and tag only.** (User, 2026-11-02.) No 1.0 declaration and no install or quickstart work.
- **The merge is the user's.** (User, 2026-11-02.) A criterion holds the pull request open with passing checks, never its merge.
- **Numbering.** (Planning.) Initiative numbers are per repository; `prosiform`'s highest is I10, so this is I11.
- **Priority.** (User, 2026-11-02.) I11 `priority: 2`, between I09's 3 and I10's 1; E00 `priority: 1`.

## Links

| Resource | Link |
| --- | --- |
| Initiative | [I11 MVP Release](https://github.com/m2ux/prosiform/issues/524) |
| Epic | [I11:E00 Release Cut](https://github.com/m2ux/prosiform/issues/525) |
| Prerequisite | [I08 Argument Surface](https://github.com/m2ux/prosiform/issues/462) |
| Prerequisite | [I09 Grouping and Composition](https://github.com/m2ux/prosiform/issues/463) |
| Previous release | [contract/v0.15.0](https://github.com/m2ux/prosiform/releases/tag/contract%2Fv0.15.0) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
