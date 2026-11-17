# Stub Presets — November 2026

> Standalone issue · Created 2026-11-17

## Executive Summary

A trial compiles a skill against recorded material in place of what a live run reads. Before this work that material was an ordinary preset, so a name on the entry selected nothing in a document a dispatch reached, a caller had to swap router files to reach it, and every live compile warned that the preset was unused.

The stub preset gives trial material a kind of its own: one name on the entry binds it in every document and bundle of the run, a deferral carries the name to the run compiling it, and a run naming no stub stays silent. Ordinary presets and alternatives keep the selection, warnings and routing they had.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w00.md](w00.md) | The work item: the stub kind, its selection and the checks it carries |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |

## Links

| Resource | Link |
| --- | --- |
| Issue | [Stub Presets: Trial Material Selected by the Run](https://github.com/m2ux/prosiform/issues/772) |
| Delivering pull request | [Stub Presets: Trial Material Selected by the Run](https://github.com/m2ux/prosiform/pull/777) |
| Design | [Presets](https://github.com/m2ux/prosiform/blob/e333bb447/artifacts/planning/2026-10-17-prosiform-v1/design.md#presets) |

## Plan Changes

None applied. Held: the arising defect below, which the delivery did not introduce and which this session had no allowance to file.

- A deferred directive naming a fragment two headings of its document share fails with `E_UNEXPECTED_INTERNAL_ERROR` (exit 4) rather than an input failure; reproduced on `pf` 0.25.0.
