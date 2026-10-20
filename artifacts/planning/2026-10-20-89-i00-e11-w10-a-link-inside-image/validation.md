## Overview

What the build was measured to do on `i00/e11/w10-a-link-inside-image` at `49325eb`, and the checks the delivery was held to.

## The Defect

Measured on the epic base at `9ffb716`, against the fixture's own sources:

```text
$ prosiform --root source guide.md
W_RESOURCE_PORTABILITY: the bundle names at least one resource, ...
This bundle was built for [guide](#guide); everything else is material it references.

# guide

A picture ![of the [¬ shared rules](rules.md) it names](plan.png).
```

The mark is published as text, `rules.md` is never opened, the bundle carries no group for it, and the published link names a source path. The run exits 0.

## The Reference Fixture

`fixtures/reference/a-marked-link-inside-image-alternative-content` declared this outcome and carried `awaiting = "I00:E11:W10"`. At `49325eb` the same invocation publishes:

```text
This bundle was built for [guide](#guide); everything else is material it references.

# guide

A picture ![of the [shared rules](#rules) it names](plan.png).

# rules

Every rule the procedure requires.
```

The marker is lifted, so the corpus run holds the fixture to its manifest from here on. The corpus reports 203 fixtures, 202 passing and 1 awaited, against 201 passing and 2 awaited on the base; the one remaining marker is `grouping/a-rule-matching-no-document-in-the-closure`, which awaits `I00:E11:W14`.

<a id="the-reference-fixtures"></a>

## The Walk

The unit tests state what one run of inline events yields and what each reader takes from it. They run under `make test`.

| Case | Measured |
| --- | --- |
| A link inside an image's alternative content | Read as a use of its own, opening with the mark its author wrote |
| An image inside an image's alternative content | Read as a resource use of its own |
| A nested link's position | The line the block that holds the run opens on |
| The occurrence count over such a paragraph | 2, the image and the link it carries |
| The emission's marked destinations | The nested link's destination, in written order beside an unnested one |
| An unmarked nested link | No destination, so nothing is rewritten |
| The emission's edit | `![of the [rules](#rules) it names](plan.png)` from the marked source span |
| The candidate comparison | A bundle carrying the nested link as its source wrote it validates |
| A nested link the bundle altered | Refused on `reference preservation` |

## The Gate

Measured in the delivery worktree at `49325eb`.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 613 passed |
| `make harness` | 379 passed |
| `make corpus` | 203 fixture(s), 202 pass, 0 fail, 1 awaited, 0 unexpected pass |
| `make smoke` | Installed, bundled and glossary shipped |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) held to the build |

## Limitations

An image written inside a link, and a link written inside an image written inside a link, are shapes the parser will produce and no fixture states. The walk yields each use it finds there, and the emission's own text scan reads a link whose label already holds a link as text, so the two counts can differ on that one shape and the emission reports it as an unrewritable run rather than publishing it. The behaviour is the one the base carried; this row neither relies on it nor changes it.

An image's alternative content is compared as the text its run shows with each nested link's text left out, so the raw spelling of markup inside that content — an emphasis delimiter, an entity — is held by the byte comparison of the lines around it rather than by the use comparison. That is how a link's own visible text is compared, and both sides read it the same way.
