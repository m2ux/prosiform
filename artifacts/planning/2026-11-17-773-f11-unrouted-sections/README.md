# Unrouted Sections — November 2026

> Hot-fix · Created 2026-11-17

## Executive Summary

A document serving several kinds of work declares alternatives, and the reference reaching it picks one. On `main` exactly one must be in force wherever the document is compiled, so a section none of the alternatives changes still fails with `E_ALTERNATIVE_UNRESOLVED` unless its reference names one.

A route that dispatches a stage under each alternative and composes the stage's one contract then writes an arbitrary alternative's name on the composition, and the published link carries it to the reader. The fix makes the rule count what the alternatives change: a pick is needed where one of them states a `group` pair or routes a link the selected content writes, and other content compiles under `default`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f11.md](f11.md) | The work item: the rule on when an alternative must be in force and the checks it carries |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F11] Unrouted Sections](https://github.com/m2ux/prosiform/issues/773) |
| Design | [Presets](../2026-10-17-prosiform-v1/design.md#presets) |

## Plan Changes

None: the session applied no plan change and held none, and no issue arose from the delivery.
