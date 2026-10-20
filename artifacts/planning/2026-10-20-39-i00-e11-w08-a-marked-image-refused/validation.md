## Overview

What the delivery of `I00:E11:W08` was measured to do at `b234484`, and the review the dispatcher ran over it independently of the delivering session's report.

## What Changed

Discovery read links. An image is not a link, so a marked image was never classified, never refused, and reached the bundle carrying the mark that [D32](../2026-10-17-prosiform-v1/decisions.md) says never appears in one — the rewrite drops a mark and a resource is never rewritten, so nothing removed it.

Discovery now reads every reference use, link and image alike, each carrying whether it is a resource. An image is a resource whatever file it names. The refusal happens on the use, before a destination is resolved, because no destination makes a picture a document.

## The Measurement

| Case | Measured |
| --- | --- |
| A marked image naming a picture | Refused with `E_MARKED_RESOURCE` at the authored line |
| A marked image naming a Markdown document | Refused the same way |
| An image whose alternative content opens on a link | Opens with nothing, so it is not marked and not refused |
| An apparent image inside a code span | Produces no use at all |
| An unmarked image | Emitted as authored |

Two corpus fixtures state it: `fixtures/rewriting/marking-an-image`, whose `awaiting` marker this row lifted, and `fixtures/marked-resource/marking-an-image-that-names-a-document`, added by the dispatcher in review for the case below.

## The Gate

Measured by the dispatcher in a separate worktree, not taken from the delivering session's report. At the delivered head `f9db74a`: 486 unit tests, 304 harness tests, 156 fixtures with 152 passing and 4 awaited. After the review fixture at `b234484`: 486, 305, and 157 fixtures with 153 passing and 4 awaited.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 37 files already formatted |
| `make typecheck` | Success: no issues found in 36 source files |
| `make test` | 486 passed |
| `make harness` | 305 passed |
| `make corpus` | 157 fixture(s), 153 pass, 0 fail, 4 awaited, 0 unexpected pass |
| `make layout` | 3 tree(s) present |
| `make tables` | 12 command(s) and 7 declaration(s) |
| `make links` | Every reference in 6 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |

The awaited count fell from five to four, which is the lifted marker and nothing else.

## The Review

- **The change is confined to its surface.** Five files under `src/` and `fixtures/`, nothing in `checks/`, no `Makefile`, no catalogue movement. Two sessions were working in those other trees at the same time and neither was disturbed.
- **`E_MARKED_RESOURCE` already existed**, confirmed from the schema's own enum, so the two-branch window between the schema and the contract stayed shut.
- **`I00:E11:W10` was left alone.** `fixtures/reference/a-marked-link-inside-image-alternative-content` still reports `awaiting I00:E11:W10` in the corpus run. A link inside an image's alternative content sits in that image token's children rather than at the inline level the discovery iterates, and a test pins that boundary, so the later row is still free to decide what happens to it.
- **A widening was reported by the session against itself and confirmed here.** A marked image naming a Markdown document is now refused too. The contract's clause keyed the refusal on the target, which would have left that case with no outcome: neither a resource to refuse nor a link to bundle, and emitting it as authored publishes the mark. The clause was amended and the reasoning recorded as `D49`; the fixture above was added in the same pull request, because a behaviour's fixture belongs with the change that produced it.
