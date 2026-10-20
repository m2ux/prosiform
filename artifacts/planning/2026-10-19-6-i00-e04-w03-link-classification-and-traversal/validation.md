# Validation Record

> I00:E04:W03 — Link classification and traversal to a fixed point

## What Was Measured Before Anything Was Built

The base `i00/e04/main` at `c3181dd` was run whole before a line changed:

```text
corpus check: 84 fixture(s), 82 pass, 0 fail, 2 awaited, 0 unexpected pass
```

All eleven `make check` targets passed, with `PROSIFORM_BUILD` naming the worktree's build. That is the figure the brief declared and the one the base returned.

Reading the base established that **no traversal existed at all**: `execute` read the entry references and the `--from` referrer, and `compose` grouped and selected from exactly those. Nothing opened a link. So none of the five criteria was already met by the build, and nothing on the row's scope was found already done.

## The Behaviour Measured Before the Design Was Built To It

Three questions were settled by running the parser rather than by reasoning about it, because the classification rests on all three.

| Question | What the parser returned |
| --- | --- |
| Does a marked link's text arrive as a text event? | Yes. `[¬ the outside document](../outside.md)` produces `link_open` with `href`, then a `text` child whose content is `¬ the outside document`. The mark is readable from the first child, which is where the design says it is written |
| Does an apparent link inside a code span or a fence produce a link? | No. Both arrive as `code_inline` and `fence` content, so an example is excluded by the parse rather than by a rule the build has to write |
| Is an image a link? | No. `![a diagram](pic.png)` arrives as an `image` token, so a resource is excluded by the same route |

The third was the one worth measuring: AC12 would otherwise have needed a classification step that the parser already performs.

One further measurement decided where the mark can be read from. A link whose content opens on markup — `[**bold**](x.md)` — produces `strong_open` as its first child, so there is no text to read a mark from. The design says the mark **opens** the link text, so such a link is unmarked, which is what the build does and what a test states.

## Each Criterion and the Instrument That Observes It

| Criterion | Instrument | Verdict |
| --- | --- | --- |
| **AC1** | `traversal/a-marked-dependency-is-bundled`, `traversal/a-marked-link-in-a-code-example` | Ticked |
| **AC2** | `traversal/a-cycle-of-marked-dependencies` | Ticked |
| **AC12** | `traversal/resources-are-not-dependencies` | Ticked |
| **AC15** | `traversal/an-unmarked-link-to-a-bundled-document` | Ticked |
| **AC16** | `citation/an-unmarked-reference-above-the-root`, `citation/marking-a-reference-above-the-root`, `normalization/root-escape` | Ticked |

**AC15 is ticked on the whole of its words and is worth stating plainly.** The fixture's source marks `notes.md` and separately links it unmarked, and the published bundle carries the `notes.md` group and the unmarked link byte-identical to its source. All three clauses — emitted as authored, resolves as no dependency, left unrewritten where the bundle carries the document it names — are observed. What is not yet *contrasted* is a marked link beside it being rewritten, because rewriting is `E05:W02`. The fixture is written so that it holds unchanged when that row lands: the unmarked link stays as authored while the marked one in the same bundle changes.

## The Command Behind Each Row and What It Returned

### The whole check, on the finished branch

```bash
PROSIFORM_BUILD="uv run --project .worktrees/i00-e04-w03/prototype --frozen prosiform" make check
```

```text
All checks passed!                       (ruff check)
30 files already formatted               (ruff format --check)
Success: no issues found in 29 source files   (mypy)
360 passed in 0.18s                      (pytest, prototype)
231 passed in 0.48s                      (pytest, checks/tests)
corpus check: 96 fixture(s), 94 pass, 0 fail, 2 awaited, 0 unexpected pass
layout check: 3 tree(s) present
table check: 12 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked ... every one defined in docs/glossary.md
```

`lock-check` resolved 22 packages and reported no drift. Exit status 0.

### The two markers that remain

```text
extraction/an-unterminated-example-at-the-section-end: awaited, awaiting I00:E08
traversal/a-relative-resource-warns: awaited, awaiting I00:E05:W03
```

`normalization/root-escape` is neither of them: it passes, and its marker is gone.

### The bundle a marked dependency produces

```text
This bundle was built for [guide](#guide); everything else is material it references.

# guide

The procedure requires [¬ the shared rules](rules.md) whole and
[¬ the review step](process.md#review) in part. It mentions
[the changelog](changelog.md), which it cites rather than requires.

# process

### Review

The section the procedure requires.

# rules

Every rule the procedure requires.
```

`changelog.md` exists under the root and the bundle does not carry it, because only a mention names it. `process.md` contributes the one section a dependency named, shifted by one because the group emits no absorbed title, and it enters no entry line because no entry reference named it.

### The refusal a marked reference above the root returns

```json
{"severity": "error", "message": "the reference '../guidelines.md' normalizes above the allowed source root, which cannot contain the document it names", "code": "E_SOURCE_OUTSIDE_ROOT", "reference": "../guidelines.md", "source": "guide.md:3", "remedy": "name a document the source root carries, or cite it without the mark"}
```

The same tree with that one reference unmarked bundles with status 0 and the citation emitted as authored. That pair is AC16.

## What Turned Out Wrong in the Plan

- **The row's Test breakdown names "an unsupported raw HTML document link".** `profile/raw-html-in-selected-content` already declares it, and `E_RAW_HTML` already fires on any source the traversal reads, so no fixture was added for it.
- **The brief states that the mark never reaches the bundle.** True of the finished contract and not of this row: `D32` and `design.md` both make the drop part of the rewrite, which is `E05:W02`. See the work item's closing section.
