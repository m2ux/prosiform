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
