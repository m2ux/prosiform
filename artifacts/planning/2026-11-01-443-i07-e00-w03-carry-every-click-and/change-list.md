# Change List — W03 Carry Every Click and Every Link Element

> Delivery record · 2026-11-01

The plan changes this session applied, the ones it held, and the technical debt it classified.

## Applied

| Change | Kind | Why | Where |
| --- | --- | --- | --- |
| A non-empty `links` array is refused under `E_UNSUPPORTED_CONSTRUCT` | Source | Finding 19: the array drew live menu links to documents the run never compiled, at exit 0 | `src/prosiform/source.py`, `src/prosiform/profile.py` |
| An HTML anchor is skipped in a click or class link tooltip, and in the thirteen diagram types Mermaid draws as SVG text | Source | Finding 20: the anchor was refused where Mermaid draws none, a finding confirmed type by type with mermaid-cli | `src/prosiform/source.py` |
| Each line is read as `;`-ended statements outside double quotes, for clicks and for anchors | Source | Finding 25: a second click hid both destinations. The same split keeps a label beside a click refusing its anchor | `src/prosiform/source.py` |
| The unfollowed form is named *HTML anchor in a label* | Source | Edge labels and subgraph titles draw anchors too, so *node label* understated the form | `src/prosiform/source.py` |
| The diagram links page states the statement split, the array refusal and where Mermaid draws an anchor | Docs | A refusal is stated with its case | `docs/references.md` |
| Three corpus fixtures and two render-check entries | Test | Each finding ships with its case, and the render check proves which anchors Mermaid draws | `fixtures/`, `checks/render.py` |

The epic body records the delivery: row `W03` on [#443](https://github.com/m2ux/prosiform/issues/443) links [#484](https://github.com/m2ux/prosiform/pull/484). No task was created, closed or renumbered, and no criterion changed.

## Plan departures recorded here, not in the plan

- **The array is refused, not bundled.** The epic record's W03 work item proposed reading a `links` array as a destination set. AC5 states a refusal with a named code, and the criterion governs.
- **The component is `source.py`.** The epic record names `src/prosiform/diagram.py`, which does not exist. The diagram link reader is in `src/prosiform/source.py`. The refusal wording sits in `src/prosiform/profile.py`, beside the existing broken-menu refusal, because that module holds every profile refusal.

## Held

| Held | Why |
| --- | --- |
| A catalogue row for the array refusal in `fixtures/README.md` | The `E_UNSUPPORTED_CONSTRUCT` row does not list diagram constructs one by one, and W17 (AC27) rewrites that row concurrently. Adding to it here would collide |
| Reading `htmlLabels: false` to stop refusing anchors in a flowchart drawn as text | That configuration is rare and over-refusal is the loud direction. No finding asks for it |

## Technical debt classified

| Debt | Class | Disposition |
| --- | --- | --- |
| A diagram type Mermaid adds later is held to draw anchors until it is verified and listed | Not debt: the deliberate direction | A refusal the author can work around beats a link shipped unbundled |
| The text-drawing type list is verified against mermaid-cli 11.16.0 only | Trivial, not blocking | The render check pins the two fixtures. A Mermaid upgrade that starts drawing anchors in a listed type would show up there |

Nothing blocking or non-trivial was found, so no issue was deferred.

## Placement needs

None. No new initiative, epic or task was needed, and no arising issue needs a home outside this pull request.
