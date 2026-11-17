# Diagram Link Text — November 2026

> Hot-fix · Created 2026-11-17

## Executive Summary

A diagram link reads its operator from the marks opening its `click` or class diagram `link` tooltip, and the rest of the tooltip is its title, whose words select presets. Prose in a tooltip therefore selects presets, the node text a reader sees carries nothing `pf` reads, and a node may carry several links of which a rendered Mermaid diagram opens only the last.

The fix reads a diagram link's operator from the text of the node it is drawn on, as a Markdown link reads its operator from its link text, keeps the tooltip as the title alone, and refuses a second diagram link on one node.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f15.md](f15.md) | The work item: the element text as a diagram link's text, the tooltip as its title, and one link per element |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F15] Diagram Link Text](https://github.com/m2ux/prosiform/issues/783) |
| Follow-on | [[F16] Dispatch Brief](https://github.com/m2ux/prosiform/issues/784) |
| Precedent | [Click Titles](https://github.com/m2ux/prosiform/pull/744) |
| Design | [Link classification and resource handling](../2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling) |
