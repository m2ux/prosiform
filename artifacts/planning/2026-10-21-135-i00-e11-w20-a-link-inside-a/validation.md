## Overview

What the build was measured to do on the epic base `i00/e11/main` at `ce4483c`, and on `i00/e11/w20-a-link-inside-a` at `7e0218b` where the delivery was held to the repository's whole check.

## The Defect

Measured on the epic base at `ce4483c`, against a source carrying a link inside an image an enclosing link holds:

```text
$ cat source/guide.md
# Guide

A [picture ![of the [shared rules](rules.md) it names](plan.png) link](rules.md).

$ prosiform --root source guide.md
E_UNEXPECTED_INTERNAL_ERROR: unexpected internal error: Unrewritable('the parser read 3 use(s) against the 2 the emission can edit in place')
$ echo $?
4
```

The parser keeps the outer link, the image and the nested link. The scan reads the nested link, reads the image and discards the outer link as text, so the counts differ by one and the run exits 4 with the status the contract reserves for a fault in the tool. A source document and a command line alone reach it.

## The Fix

At `7e0218b` the same invocation publishes the bundle and exits 0:

```text
This bundle was built for [guide](#guide); everything else is material it references.

# guide

A [picture ![of the [shared rules](#rules) it names](plan.png) link](#rules).

# rules

Every rule the procedure requires.
```

Both links are read as the references they are, each rewritten to its target's destination, and no published link names a source path.

## The Reference Fixture

`fixtures/reference/a-link-inside-an-image-a-link-carries` declares the nesting with two distinct targets under the allowed source root, so the published bundle states where each destination lands rather than one build's tests.

| Declared | Value |
| --- | --- |
| Entry | `guide.md`, root `source` |
| Outer link | `rules.md`, published as `#rules` |
| Link inside the image | `notes.md`, published as `#notes` |
| Image | `plan.png`, published as authored |
| Exit status | 0 |
| Diagnostics | `W_RESOURCE_PORTABILITY`, `W_ENTRY_DESTINATION` |

The fixture carries no `awaiting` marker, so the corpus holds it to its manifest from the commit that adds it. The corpus reports 218 fixtures against the base's 217, all passing and none awaited.

## The Scan

The unit tests state what one run of inline text yields and what the emission edits. They run under `make test`.

| Case | Measured |
| --- | --- |
| A link alone | One use, the count the parser reads |
| An image alone | One use, the count the parser reads |
| An image inside a link | Two uses, the count the parser reads |
| A link inside an image | Two uses, the count the parser reads |
| A link inside an image inside a link | Three uses, the count the parser reads |
| An image inside an image | Two uses, the count the parser reads |
| An image inside a link inside an image | Three uses, the count the parser reads |
| A link inside a link | One use, the count the parser reads |
| An image inside an image inside a link | Three uses, the count the parser reads |
| The kinds of a link inside an image inside a link | Link, resource, link, in written order |
| The emission's edit of that shape | `[picture ![of the [rules](#a) it names](plan.png) link](#b)` from the source span |
| A link an enclosing link's own label holds | The enclosing label stays the text it is, and the nested link alone is rewritten |

## The Gate

Measured in the delivery worktree at `7e0218b`, with `PROSIFORM_BUILD` naming this checkout's build.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 50 files already formatted |
| `make typecheck` | Success: no issues found in 49 source files |
| `make test` | 682 passed |
| `make harness` | 488 passed |
| `make corpus` | 218 fixture(s), 218 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `make smoke` | Installed, resolved and bundled outside the repository |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 35 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) held to the build |

## Limitations

The containment rule reads the uses the scan has already found, which works because a bracket pair closes before the pair enclosing it. A shape the parser accepts and the scan does not pair the same way would therefore be counted differently, and the emission's count check is what catches it — that check is the invariant this row leaves standing rather than one it removes.

An image's alternative content is compared on the candidate side as the text its run shows with each nested link's text left out, so the raw spelling of markup inside that content is held by the byte comparison of the lines around it. This row does not change that reading, and the nested shape validates through it.
