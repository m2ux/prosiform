# Validation

The checks this unit ran, the revision they ran against and what each observed.

**Revision:** `i01/e02/w03-title-case-for-every` at `1d12607`, cut from `origin/i01/e02/main` at `a56a738`.
**Build under test:** `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"`.

## Repository checks

`make check` runs the repository's whole set — lock, lint, format, typecheck, unit tests, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence — and stops at the first failure. It ran unsandboxed in the unit's worktree.

```text
736 passed in 0.72s            (src/tests)
599 passed in 7.97s            (checks/tests)
corpus check: 243 fixture(s), 243 pass, 0 fail, 0 awaited, 0 unexpected pass
smoke check: the installed command is named on the path, independent of the
  working directory, independent of this repository
link check: every reference in 23 document(s) resolved
vocabulary check: 36 contract term(s) marked in
  artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering,
  every one defined in docs/glossary.md
invocation check: 29 statement(s) of the documented invocation, each held to
  the build PROSIFORM_BUILD names
conformance report: 245 clause(s) the design states, 0 covered by no fixture,
  0 declaration(s) naming no clause
independence check: every word of every fixture declaration and every report
  entry is one the contract states
```

Exit status 0.

The corpus carries two fixtures more than it did, and every expected bundle that carried a file heading now declares it in title case. The 158 expected outputs that changed were rewritten only where the produced bytes matched the declared bytes under case folding, so each difference is a letter and nothing else; two manifests whose declared references are written as Unicode escapes were corrected by hand to the same rule.

## Generated headings in one spelling

`grouping/one-spelling-for-every-generated-heading` declares a hyphenated document, a nested one and a merged directory in one closure, bundled with `--group rules:2`:

```markdown
This bundle was built for [Entry-Point](#entry-point); everything else is material it references.

# Entry-Point

# Guides/Field-Notes

# Rules
```

A hyphenated name keeps its hyphen and capitalizes each part of it; a nested one keeps its separator and capitalizes each segment; a merged group's heading is its directory slug capitalized as it always was. One bundle, one convention.

`src/tests/test_bundle.py` states the convention directly over nested paths, hyphens, underscores, spaces, a name already capitalized, one spelled in capitals throughout, a dotted name and a name carrying diacritics, and over the file heading each path produces.

Observed: AC4.

## The spelling a source wrote

`headings/an-authored-heading-beside-a-generated-one` declares a document whose author wrote a lower-case title and a lower-case section heading, and which defers a link to a document under `rules/`:

```markdown
# Field-Guide

## the field guide

### a lower-case section

It defers [¬ the shared rules](rules/shared-rules.md#every-rule) to a run of its own.
```

The file heading is the compiler's and carries the convention. The two headings the author wrote carry their author's spelling, and the deferred link's destination carries the path the filesystem holds. `deferral/a-deferred-destination-named-from-the-root` states the same boundary from the other side: `# Topic/Guide` heads the group and the deferred destination is `shared/rules.md`.

Observed: AC5.

## What the convention did not reach

`src/prosiform/grouping.py` composes the merged group's heading, its member subsection headings and its variant headings, and each already carried the convention. No edit was made there, which keeps this unit clear of the two sessions extending that file.

## A consequence recorded rather than repaired

Generated-input detection reads a source's opening file heading and asks whether a supported suffix appended to it names a document under the allowed source root. A file heading now carries its path in title case, so a bundle of a root whose paths the filesystem spells in lower case opens on a heading naming no path under that root and is not detected. Reading the heading against another capitalization was tried and withdrawn: it refuses an authored title that happens to name a sibling document, which `identity/paths-differing-only-by-suffix` demonstrates, and a legitimate source refused is the costlier of the two mistakes. The design records the weaker reach and the reason for it, and the repair is deferred.
