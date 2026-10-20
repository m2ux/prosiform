# Validation Record — I00:E05:W01

> Measured 2026-10-20 against `i00/e05/main` at `884f0ab` and the delivery branch above it.

## The Renderer Was Measured, Not Read

`Bundle destinations` binds a destination to the fragment the declared renderer generates, so the renderer decides what the numbering runs over. GitHub's own renderer answered through `POST /markdown`, on a document holding a blockquoted heading, a list-item heading and a document-level heading all carrying the text `Run`:

```
# a

> ## Run

- ### Run

# b

### Run
```

The identifiers it generated:

```
id="user-content-a"
id="user-content-run"
id="user-content-run-1"
id="user-content-b"
id="user-content-run-2"
```

A heading a container carries is indexed exactly as a document-level one is, in source order, and takes an ordinal from the same count. Nothing about the container changes the numbering.

## The Behaviour Measured Before the Design Was Built To It

Each run below used the base build against a scratch tree, before any change to the repository.

**A container-nested heading displaced a destination.** `a.md` carrying `> ## Run` inside a blockquote and `b.md` carrying a document-level `## Run`:

```
prosiform --root source a.md b.md#run

This bundle was built for [a](#a) and [Run](#run); everything else is material it references.

# a

Intro.

> ## Run
>
> Quoted.

# b

### Run

Top level.
```

Exit 0. The renderer gives `run` to the quoted heading and `run-1` to the heading the entry line meant, so `[Run](#run)` resolves into the blockquote. This is [#75](https://github.com/m2ux/prosiform/issues/75), reproduced unchanged on this base. The outline epic emits the quoted heading at the level its container holds it at; the numbering was the same before and after.

**A source fragment resolved by ordinal.** `a.md` carrying two document-level headings both reading `Run`:

```
prosiform --root source 'a.md#run'     -> exit 0, selected the first
prosiform --root source 'a.md#run-1'   -> exit 0, selected the second
```

`Source-heading resolution` holds that two headings in one source producing the same slug are not numbered apart and that a fragment requiring one of them fails with `E_AMBIGUOUS_SOURCE_HEADING`. The base assigned the renderer's ordinal inside the source heading index instead, so both runs succeeded and neither refusal existed. AC2's first half had no instrument at all.

**The second half of AC2 already held.** `identity/paths-differing-only-by-suffix` passes on the base, raising `E_AMBIGUOUS_FILE_GROUP` from the file-heading check in `unambiguous`.

**Both codes AC2 declares were already in the catalogue.** `fixtures/manifest.schema.json` carries `E_AMBIGUOUS_SOURCE_HEADING` and `E_AMBIGUOUS_FILE_GROUP` among its twenty-three codes, so this row added none and did not enter the two-branch hazard.

## The Base

```
corpus check: 127 fixture(s), 124 pass, 0 fail, 3 awaited, 0 unexpected pass
```

All eleven targets of `make check` passed on the base before any change.

## The Delivery

Every target of `make check` passed against the delivery branch, with `PROSIFORM_BUILD` naming the build in this unit's worktree.

```
corpus check: 130 fixture(s), 127 pass, 0 fail, 3 awaited, 0 unexpected pass
```

```
destinations/a-heading-a-container-carries: pass
identity/an-ordinal-names-no-source-heading: pass
identity/two-headings-sharing-a-slug: pass
```

`make test` passed 401 tests and `make harness` 271.

Continuous integration run [39382768119](https://github.com/m2ux/prosiform/actions/runs/39382768119) on `cc8a756` concluded `success`. Its first attempt failed on the link check, against two `pypi.org` pages `src/README.md` names and this branch does not touch: `https://pypi.org/project/markdown-it-py/` answered `503` to five consecutive direct requests from the host at the same moment. The run was re-run once the page recovered, and the flakiness is raised as [#84](https://github.com/m2ux/prosiform/issues/84). No merge was taken on local evidence while that run was pending.

## The Behaviour After the Design Was Built To It

```
prosiform --root source a.md b.md#run

This bundle was built for [a](#a) and [Run](#run-1); everything else is material it references.
```

```
prosiform --root source 'guide.md#run'

E_AMBIGUOUS_SOURCE_HEADING: the reference 'guide.md#run' names 2 headings of the
document it selects from, which it cannot tell apart
  reference: guide.md#run
  remedy: retitle one of the headings so each takes a slug of its own
```

Exit 1, and no bundle on standard output. The new destination fixture's expected bundle was put back through `POST /markdown`, and the `#run-2` its entry line carries is the anchor GitHub generates for the heading that reference named.
