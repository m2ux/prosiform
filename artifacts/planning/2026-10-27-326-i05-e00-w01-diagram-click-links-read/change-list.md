# W01 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| `click` registered in `docs/corpus-vocabulary.md` | Trivial and blocking: the independence check fails on a fixture word the contract does not state. |

## Held

| Change | Reason |
| --- | --- |
| The design's Examples clause (`Link classification and resource handling — Examples`, in `2026-10-17-prosiform-v1/design.md`) says fenced code blocks are never followed, which a `mermaid` click now contradicts. | The design names no diagram rule. W04 carries `invocation.md` and the profile only; the design clause needs an owner, likely W04 or a new row. |
| A diagram click naming a non-Markdown file under the root, such as `diagram.png`, is now a link use, so the published bundle raises the resource warning as an inline link to it does. | AC6 (W02) states such a click is published as written and opens nothing; whether it also warns is for W02's fixture to settle. |
| `Click.offset` is relative to the line the fence holds, which omits the container markers and fence indent of the document line. | W02 maps it onto the physical line it rewrites: the fence line is the trailing text of the document line. |
