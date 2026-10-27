# I05:E02:W09–W10 Gantt Clicks and Refused Anchors — October 2026

> Task delivery · Created 2026-10-27

## Executive Summary

This record holds the delivery of I05:E02 W09 and W10, joined in one pull request. W09 proves a Gantt diagram's link in a running page: `make render` clicks each task and records the URL its handler opens. W10 refuses a Kanban ticket link or an HTML label anchor naming a local Markdown document under `E_UNSUPPORTED_CONSTRUCT`, so no rendered link points at a path the bundle lacks.

The evidence that raised both rows is in the [W05–W08 record](../2026-10-27-339-i05-e02-w05-link-forms-as-mermaid/validation.md). The epic's plan and the Mermaid 11.16.0 survey are in the [epic record](../2026-10-27-339-i05-e02-link-forms/README.md).

## Decisions

- **Gantt proven by a click.** Chosen over restating AC16 without Gantt and over carrying a Gantt `click` as written ([#346](https://github.com/m2ux/prosiform/issues/346)).
- **Kanban ticket and label anchors refused.** Chosen over following them and over leaving them as written ([#347](https://github.com/m2ux/prosiform/issues/347)).

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E02 Link Forms](https://github.com/m2ux/prosiform/issues/339) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic pull request | [#342](https://github.com/m2ux/prosiform/pull/342) |
