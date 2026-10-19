# Validation — I00:E03:W04

> The checks as they were run, and what each establishes.

## The Gate

`make check` was run whole in the delivery worktree, with `PROSIFORM_BUILD` naming the prototype by absolute path, and returned zero.

| Check | Result |
| --- | --- |
| `lock-check` | Resolved 22 packages |
| `lint` | All checks passed |
| `format-check` | 26 files already formatted |
| `typecheck` | Success: no issues found in 25 source files |
| `test` | 300 passed |
| `harness` | 202 passed |
| `corpus` | 67 fixtures, 65 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `layout` | 3 trees present |
| `tables` | 12 commands and 7 declarations, each declared and named by a table |
| `links` | Every reference in 6 documents resolved |
| `vocabulary` | 34 contract terms marked, every one defined and carried |

The fixtures this row adds or restates, as the corpus run reports them:

```text
hierarchy/a-preamble-before-a-kept-title: pass
hierarchy/regions-the-source-separates: pass
identity/a-second-h1-leaves-the-title: pass
identity/a-title-the-path-spells-with-a-space: pass
identity/a-title-the-path-spells-with-hyphens: pass
identity/an-h1-below-the-first-heading: pass
identity/title-the-path-does-not-carry: pass
identity/whole-document: pass
real-source/absorbed-title-and-self-references: pass
real-source/preamble-above-the-first-heading: pass
```

The two markers left in the corpus belong to other work: `normalization/root-escape` awaits `I00:E04` and `extraction/an-unterminated-example-at-the-section-end` awaits `I00:E08`.

## The Defect, Measured Before and After

A document at `My Note.md` headed `# My Note` was run against the build before the change:

```text
# My Note

## My Note

An opening paragraph.

### Run
```

The title is emitted twice and the group shifts, because `bundle.absorbed` slugged the title and compared it with the raw final path segment: `my-note` against `My Note`. The comparison now slugs the segment as it slugs the title, and the same document bundles as `identity/a-title-the-path-spells-with-a-space` publishes it, with one heading and the group at its source levels.

## The Markers Measured

Six candidate deferrals were named ahead of the work. Each was run against the build before it was marked, and none was marked.

| Case | Measured | Marked |
| --- | --- | --- |
| The contract's `My Note.md` example absorbing | Absorbed once the comparison slugs both sides, which is this row's change | No |
| A hyphenated path segment absorbing a title spelled with spaces | Absorbed, both sides slugging to `my-note` | No |
| A document with a second document-level H1 | The title is kept and the group shifts | No |
| A document whose H1 is not its first heading | The title is kept and the group shifts | No |
| Two sections the source separates, named in reverse | Emitted in source order, the section between them absent | No |
| A preamble above a title the path does not carry | Emitted after the file heading and before the first retained heading | No |

The last two were measured against the unchanged build and already held, so AC6's behaviour was delivered before this row and what the row adds is the evidence.

## What the Criteria Rest On

**AC6** — a file group emits its selected regions in their original source order, with a document's preamble before its first retained heading.

`hierarchy/regions-the-source-separates` names two fragments of one document in reverse order on the command line and publishes the bundle those two selections produce: `Alpha` before `Gamma`, the unselected `Beta` absent between them. The order a region reaches the bundle in therefore follows the document rather than the reference that selected it, and it is read off the bytes rather than asserted. `hierarchy/a-preamble-before-a-kept-title` publishes a document whose preamble sits above a title the path does not carry: the preamble is emitted after the file heading and before that first retained heading, which is itself shifted. `identity/whole-document` and `real-source/preamble-above-the-first-heading` state the same placement under a group whose title was absorbed, so the clause is shown under both shifts.

**AC7** — a source whose only H1 slugifies to the final segment of its file heading has that heading absorbed, emitting no duplicate and leaving its group's headings at their source levels, while a source whose H1 differs keeps it and shifts.

`identity/a-title-the-path-spells-with-a-space` is the contract's own example, `My Note.md` titled `My Note`: one heading in the bundle, the group's `## Run` and `### Detail` at the levels their source wrote them. `identity/a-title-the-path-spells-with-hyphens` holds the other spelling the contract names, a segment hyphenating what the title spaces, so the comparison is observed on both sides rather than on a segment that is already its own slug. `identity/title-the-path-does-not-carry` is the criterion's second half, published before this row and passing unchanged: the differing H1 is kept and shifted to H2, and everything below it shifts with it. `identity/a-second-h1-leaves-the-title` and `identity/an-h1-below-the-first-heading` hold the two conditions the clause places on the heading — that it be the document's only H1, and that it be the first — each leaving the title unabsorbed and the group shifting.

## What the Corpus Was Not Asserting

Three fixtures exercised absorption before this row and all three pass unchanged. Each names a lowercase, single-word final segment — `guide`, `repository-labels`, `design-flow` — which is its own slug, so each held under the defective comparison and holds under the corrected one. None of them was asserting the defect. The only two copied sources whose filenames carry capitals are both `SKILL.md`, whose titles slug to nothing near `skill`, so they are unabsorbed before and after. The corpus had no case where slugging the path segment changed anything, which is why the defect survived it.
